$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$BuildingsDir = Join-Path $Root "in_game/common/building_types"
$AdvancesDir = Join-Path $Root "in_game/common/advances"
$OutputDir = Join-Path $PSScriptRoot "reports"

function Get-RelativeRepoPath {
    param(
        [string]$BasePath,
        [string]$TargetPath
    )

    $baseFull = [System.IO.Path]::GetFullPath($BasePath)
    $targetFull = [System.IO.Path]::GetFullPath($TargetPath)

    if ($targetFull.StartsWith($baseFull, [System.StringComparison]::OrdinalIgnoreCase)) {
        $relative = $targetFull.Substring($baseFull.Length).TrimStart('\')
        return $relative.Replace('\', '/')
    }

    return $targetFull.Replace('\', '/')
}

function Remove-InlineComment {
    param(
        [string]$Line
    )

    if ($null -eq $Line) {
        return ""
    }

    $commentIndex = $Line.IndexOf("#")
    if ($commentIndex -ge 0) {
        return $Line.Substring(0, $commentIndex)
    }

    return $Line
}

function Get-TopLevelBlocks {
    param(
        [string]$FilePath
    )

    $lines = Get-Content -Path $FilePath
    $blocks = @()

    $currentName = $null
    $bodyLines = New-Object System.Collections.Generic.List[string]
    $braceDepth = 0

    foreach ($line in $lines) {
        $activeLine = Remove-InlineComment $line
        $stripped = $activeLine.Trim()

        if ($null -eq $currentName) {
            if ($stripped -match '^([A-Za-z0-9_]+)\s*=\s*\{') {
                $currentName = $matches[1]
                $bodyLines = New-Object System.Collections.Generic.List[string]
                $braceDepth = ([regex]::Matches($activeLine, '\{')).Count - ([regex]::Matches($activeLine, '\}')).Count
            }
            continue
        }

        $bodyLines.Add($line)
        $braceDepth += ([regex]::Matches($activeLine, '\{')).Count - ([regex]::Matches($activeLine, '\}')).Count

        if ($braceDepth -eq 0) {
            $trimmedBody = @($bodyLines)
            if ($trimmedBody.Count -gt 0) {
                $lastActive = (Remove-InlineComment $trimmedBody[-1]).Trim()
                if ($lastActive -eq '}') {
                    $trimmedBody = @($trimmedBody[0..($trimmedBody.Count - 2)])
                }
            }

            $blocks += [pscustomobject]@{
                Name = $currentName
                FilePath = $FilePath
                BodyLines = $trimmedBody
            }

            $currentName = $null
            $bodyLines = New-Object System.Collections.Generic.List[string]
            $braceDepth = 0
        }
    }

    return $blocks
}

function Get-TopLevelAssignments {
    param(
        $Block
    )

    $assignments = @{}
    $nestedDepth = 0

    foreach ($line in $Block.BodyLines) {
        $activeLine = Remove-InlineComment $line
        $stripped = $activeLine.Trim()

        if ([string]::IsNullOrWhiteSpace($stripped)) {
            continue
        }

        if ($nestedDepth -eq 0 -and $stripped -match '^([A-Za-z0-9_]+)\s*=\s*(.+)$') {
            $key = $matches[1]
            $value = $matches[2].Trim()

            if ($value -ne "{") {
                if (-not $assignments.ContainsKey($key)) {
                    $assignments[$key] = New-Object System.Collections.Generic.List[string]
                }
                $assignments[$key].Add($value)
            }
        }

        $nestedDepth += ([regex]::Matches($activeLine, '\{')).Count - ([regex]::Matches($activeLine, '\}')).Count
        if ($nestedDepth -lt 0) {
            $nestedDepth = 0
        }
    }

    return $assignments
}

function Normalize-Value {
    param(
        [string]$Value
    )

    if ($null -eq $Value) {
        return ""
    }

    return $Value.Trim().Trim('"')
}

function Get-InferredTechnologyLevel {
    param(
        [string]$AdvanceName,
        $AdvanceData
    )

    if (-not $AdvanceData.ContainsKey($AdvanceName)) {
        return [pscustomobject]@{
            level = ""
            source = ""
        }
    }

    $advance = $AdvanceData[$AdvanceName]
    if (-not [string]::IsNullOrWhiteSpace($advance.explicit_level)) {
        return [pscustomobject]@{
            level = $advance.explicit_level
            source = "explicit"
        }
    }

    $searchModes = @(
        @{ direction = "requires"; source_prefix = "inferred_from_prerequisite_" },
        @{ direction = "required_by"; source_prefix = "inferred_from_dependent_" }
    )

    foreach ($mode in $searchModes) {
        $queue = New-Object System.Collections.Queue
        $visited = New-Object 'System.Collections.Generic.HashSet[string]'
        $matches = New-Object System.Collections.Generic.List[object]
        $bestDistance = $null

        $queue.Enqueue([pscustomobject]@{ name = $AdvanceName; distance = 0 })
        [void]$visited.Add($AdvanceName)

        while ($queue.Count -gt 0) {
            $current = $queue.Dequeue()

            if ($null -ne $bestDistance -and $current.distance -ge $bestDistance) {
                continue
            }

            if (-not $AdvanceData.ContainsKey($current.name)) {
                continue
            }

            $neighbors = @($AdvanceData[$current.name].($mode.direction))
            foreach ($neighbor in $neighbors) {
                if ([string]::IsNullOrWhiteSpace($neighbor)) {
                    continue
                }

                if (-not $visited.Add($neighbor)) {
                    continue
                }

                if (-not $AdvanceData.ContainsKey($neighbor)) {
                    continue
                }

                $nextDistance = $current.distance + 1
                $neighborAdvance = $AdvanceData[$neighbor]

                if (-not [string]::IsNullOrWhiteSpace($neighborAdvance.explicit_level)) {
                    if ($null -eq $bestDistance) {
                        $bestDistance = $nextDistance
                    }

                    if ($nextDistance -eq $bestDistance) {
                        $matches.Add([pscustomobject]@{
                            level = [int]$neighborAdvance.explicit_level
                            advance = $neighbor
                        })
                    }
                }
                elseif ($null -eq $bestDistance) {
                    $queue.Enqueue([pscustomobject]@{
                        name = $neighbor
                        distance = $nextDistance
                    })
                }
            }
        }

        if ($matches.Count -gt 0) {
            $chosen = $matches | Sort-Object level, advance | Select-Object -First 1
            return [pscustomobject]@{
                level = [string]$chosen.level
                source = "$($mode.source_prefix)$($chosen.advance)"
            }
        }
    }

    return [pscustomobject]@{ level = ""; source = "" }
}

function Get-BuildScopeValue {
    param(
        $Assignments,
        [string]$Key
    )

    if ($Assignments.ContainsKey($Key)) {
        return (Normalize-Value $Assignments[$Key][0]).ToLowerInvariant()
    }

    return "no"
}

$buildingRecords = @{}
$advanceData = @{}

Get-ChildItem -Path $BuildingsDir -Filter *.txt | Sort-Object Name | ForEach-Object {
    $relativePath = Get-RelativeRepoPath -BasePath $Root -TargetPath $_.FullName
    foreach ($block in Get-TopLevelBlocks -FilePath $_.FullName) {
        $assignments = Get-TopLevelAssignments -Block $block
        $buildingRecords[$block.Name] = [pscustomobject]@{
            building = $block.Name
            building_source_file = $relativePath
            can_build_rural = Get-BuildScopeValue -Assignments $assignments -Key "rural_settlement"
            can_build_town = Get-BuildScopeValue -Assignments $assignments -Key "town"
            can_build_city = Get-BuildScopeValue -Assignments $assignments -Key "city"
            can_build_megalopolis = Get-BuildScopeValue -Assignments $assignments -Key "megalopolis"
            unlock_advance = ""
            advance_age = ""
            starting_technology_level = ""
            advance_requires = ""
        }
    }
}

$rows = New-Object System.Collections.Generic.List[object]

Get-ChildItem -Path $AdvancesDir -Filter *.txt | Sort-Object Name | ForEach-Object {
    foreach ($block in Get-TopLevelBlocks -FilePath $_.FullName) {
        $assignments = Get-TopLevelAssignments -Block $block
        $explicitLevel = ""
        if ($assignments.ContainsKey("starting_technology_level")) {
            $explicitLevel = Normalize-Value $assignments["starting_technology_level"][0]
        }

        $requiresList = @()
        if ($assignments.ContainsKey("requires")) {
            $requiresList = @($assignments["requires"] | ForEach-Object { Normalize-Value $_ })
        }

        $advanceData[$block.Name] = [pscustomobject]@{
            explicit_level = $explicitLevel
            requires = $requiresList
            required_by = New-Object System.Collections.Generic.List[string]
        }
    }
}

foreach ($advanceName in $advanceData.Keys) {
    foreach ($requiredAdvance in $advanceData[$advanceName].requires) {
        if (-not $advanceData.ContainsKey($requiredAdvance)) {
            continue
        }
        $advanceData[$requiredAdvance].required_by.Add($advanceName)
    }
}

Get-ChildItem -Path $AdvancesDir -Filter *.txt | Sort-Object Name | ForEach-Object {
    foreach ($block in Get-TopLevelBlocks -FilePath $_.FullName) {
        $assignments = Get-TopLevelAssignments -Block $block
        if (-not $assignments.ContainsKey("unlock_building")) {
            continue
        }

        $age = ""
        $requires = ""
        $explicitLevel = ""
        $effectiveLevel = ""
        $levelSource = ""

        if ($assignments.ContainsKey("age")) {
            $age = Normalize-Value $assignments["age"][0]
        }

        if ($assignments.ContainsKey("starting_technology_level")) {
            $explicitLevel = Normalize-Value $assignments["starting_technology_level"][0]
        }

        if ($assignments.ContainsKey("requires")) {
            $requires = (($assignments["requires"] | ForEach-Object { Normalize-Value $_ }) -join ", ")
        }

        $levelInfo = Get-InferredTechnologyLevel -AdvanceName $block.Name -AdvanceData $advanceData
        $effectiveLevel = $levelInfo.level
        $levelSource = $levelInfo.source

        foreach ($building in $assignments["unlock_building"]) {
            $buildingName = Normalize-Value $building
            $buildingSource = "not found in building_types"
            if ($buildingRecords.ContainsKey($buildingName)) {
                $buildingSource = $buildingRecords[$buildingName].building_source_file
            }

            $rows.Add([pscustomobject]@{
                building = $buildingName
                building_source_file = $buildingSource
                can_build_rural = if ($buildingRecords.ContainsKey($buildingName)) { $buildingRecords[$buildingName].can_build_rural } else { "no" }
                can_build_town = if ($buildingRecords.ContainsKey($buildingName)) { $buildingRecords[$buildingName].can_build_town } else { "no" }
                can_build_city = if ($buildingRecords.ContainsKey($buildingName)) { $buildingRecords[$buildingName].can_build_city } else { "no" }
                can_build_megalopolis = if ($buildingRecords.ContainsKey($buildingName)) { $buildingRecords[$buildingName].can_build_megalopolis } else { "no" }
                unlock_advance = $block.Name
                advance_age = $age
                starting_technology_level = $explicitLevel
                effective_starting_technology_level = $effectiveLevel
                technology_level_source = $levelSource
                advance_requires = $requires
            })
        }
    }
}

$unlockedBuildings = $rows | Select-Object -ExpandProperty building -Unique

foreach ($buildingName in $buildingRecords.Keys | Sort-Object) {
    if ($unlockedBuildings -notcontains $buildingName) {
        $rows.Add($buildingRecords[$buildingName])
    }
}

New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null

$csvPath = Join-Path $OutputDir "building_tech_matrix.csv"
$excelCsvPath = Join-Path $OutputDir "building_tech_matrix_excel.csv"
$rows |
    Sort-Object building, unlock_advance |
    Export-Csv -Path $csvPath -NoTypeInformation -Encoding UTF8

$rows |
    Sort-Object building, unlock_advance |
    ConvertTo-Csv -NoTypeInformation -Delimiter ';' |
    Set-Content -Path $excelCsvPath -Encoding UTF8

$previewUnlocked = $rows |
    Where-Object { $_.unlock_advance -ne "" } |
    Sort-Object building, unlock_advance |
    Select-Object -First 40

$previewNoUnlock = $rows |
    Where-Object { $_.unlock_advance -eq "" } |
    Sort-Object building |
    Select-Object -First 40

$reportPath = Join-Path $OutputDir "building_tech_report.md"
$reportLines = New-Object System.Collections.Generic.List[string]
$reportLines.Add("# Building and Advance Report")
$reportLines.Add("")
$reportLines.Add("- Building definitions found: ``$($buildingRecords.Count)``")
$reportLines.Add("- Buildings unlocked by at least one advance: ``$($unlockedBuildings.Count)``")
$reportLines.Add("- Buildings with no matching ``unlock_building`` entry: ``$($buildingRecords.Count - $unlockedBuildings.Count)``")
$reportLines.Add("- Advance/building unlock rows written: ``$($rows.Count)``")
$reportLines.Add("")
$reportLines.Add("## Buildings Unlocked By Advances")
$reportLines.Add("")
$reportLines.Add("| building | unlock_advance | explicit_level | effective_level | level_source | rural | town | city | megalopolis | advance_requires |")
$reportLines.Add("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
foreach ($row in $previewUnlocked) {
    $reportLines.Add("| $($row.building) | $($row.unlock_advance) | $($row.starting_technology_level) | $($row.effective_starting_technology_level) | $($row.technology_level_source) | $($row.can_build_rural) | $($row.can_build_town) | $($row.can_build_city) | $($row.can_build_megalopolis) | $($row.advance_requires) |")
}
$reportLines.Add("")
$reportLines.Add("## Buildings Without Matching Advance Unlock")
$reportLines.Add("")
$reportLines.Add("| building | source_file | rural | town | city | megalopolis |")
$reportLines.Add("| --- | --- | --- | --- | --- | --- |")
foreach ($row in $previewNoUnlock) {
    $reportLines.Add("| $($row.building) | $($row.building_source_file) | $($row.can_build_rural) | $($row.can_build_town) | $($row.can_build_city) | $($row.can_build_megalopolis) |")
}
$reportLines.Add("")
$reportLines.Add("Full data is available in the CSV file written beside this report.")

Set-Content -Path $reportPath -Value $reportLines -Encoding UTF8

Write-Host "Wrote $csvPath"
Write-Host "Wrote $excelCsvPath"
Write-Host "Wrote $reportPath"
Write-Host "Buildings: $($buildingRecords.Count)"
Write-Host "Unlocked by advances: $($unlockedBuildings.Count)"
