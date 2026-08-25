from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
BUILDINGS_DIR = ROOT / "in_game" / "common" / "building_types"
ADVANCES_DIR = ROOT / "in_game" / "common" / "advances"
OUTPUT_DIR = ROOT / "tools" / "reports"


TOP_LEVEL_BLOCK_RE = re.compile(r"^([A-Za-z0-9_]+)\s*=\s*\{")
ASSIGNMENT_RE = re.compile(r"^([A-Za-z0-9_]+)\s*=\s*(.+)$")


@dataclass
class Block:
    name: str
    file_path: Path
    body_lines: list[str]
    raw_lines: list[str]


@dataclass
class BuildingRecord:
    name: str
    source_file: str
    can_build_rural: str = "no"
    can_build_town: str = "no"
    can_build_city: str = "no"
    can_build_megalopolis: str = "no"
    unlock_advances: list[str] = field(default_factory=list)
    tech_levels: list[str] = field(default_factory=list)
    ages: list[str] = field(default_factory=list)
    direct_requires: list[str] = field(default_factory=list)


def strip_comments(line: str) -> str:
    if "#" not in line:
        return line
    return line.split("#", 1)[0]


def iter_top_level_blocks(path: Path) -> Iterable[Block]:
    lines = path.read_text(encoding="utf-8").splitlines()

    current_name: str | None = None
    current_raw: list[str] = []
    current_body: list[str] = []
    brace_depth = 0

    for original_line in lines:
        active_line = strip_comments(original_line)
        stripped = active_line.strip()

        if current_name is None:
            match = TOP_LEVEL_BLOCK_RE.match(stripped)
            if not match:
                continue

            current_name = match.group(1)
            current_raw = [original_line]
            current_body = []
            brace_depth = active_line.count("{") - active_line.count("}")
            continue

        current_raw.append(original_line)
        brace_depth += active_line.count("{") - active_line.count("}")

        if brace_depth > 0:
            current_body.append(original_line)

        if brace_depth == 0:
            yield Block(
                name=current_name,
                file_path=path,
                body_lines=current_body[:-1] if current_body and strip_comments(current_body[-1]).strip() == "}" else current_body,
                raw_lines=current_raw,
            )
            current_name = None
            current_raw = []
            current_body = []


def parse_top_level_assignments(block: Block) -> dict[str, list[str]]:
    assignments: dict[str, list[str]] = {}
    nested_depth = 0

    for original_line in block.body_lines:
        active_line = strip_comments(original_line)
        stripped = active_line.strip()
        if not stripped:
            continue

        if nested_depth == 0:
            match = ASSIGNMENT_RE.match(stripped)
            if match:
                key = match.group(1)
                value = match.group(2).strip()
                if value != "{":
                    assignments.setdefault(key, []).append(value)

        nested_depth += active_line.count("{") - active_line.count("}")
        if nested_depth < 0:
            nested_depth = 0

    return assignments


def load_buildings(buildings_dir: Path) -> dict[str, BuildingRecord]:
    records: dict[str, BuildingRecord] = {}
    for path in sorted(buildings_dir.glob("*.txt")):
        for block in iter_top_level_blocks(path):
            assignments = parse_top_level_assignments(block)
            records[block.name] = BuildingRecord(
                name=block.name,
                source_file=str(path.relative_to(ROOT)).replace("\\", "/"),
                can_build_rural=normalize_value(assignments.get("rural_settlement", ["no"])[0]).lower(),
                can_build_town=normalize_value(assignments.get("town", ["no"])[0]).lower(),
                can_build_city=normalize_value(assignments.get("city", ["no"])[0]).lower(),
                can_build_megalopolis=normalize_value(assignments.get("megalopolis", ["no"])[0]).lower(),
            )
    return records


def normalize_value(value: str) -> str:
    return value.strip().strip('"')


def load_unlocks(advances_dir: Path) -> list[dict[str, object]]:
    unlock_rows: list[dict[str, object]] = []
    for path in sorted(advances_dir.glob("*.txt")):
        for block in iter_top_level_blocks(path):
            assignments = parse_top_level_assignments(block)
            unlocked_buildings = [normalize_value(v) for v in assignments.get("unlock_building", [])]
            if not unlocked_buildings:
                continue

            row = {
                "advance": block.name,
                "source_file": str(path.relative_to(ROOT)).replace("\\", "/"),
                "age": normalize_value(assignments.get("age", [""])[0]) if assignments.get("age") else "",
                "tech_level": normalize_value(assignments.get("starting_technology_level", [""])[0]) if assignments.get("starting_technology_level") else "",
                "requires": [normalize_value(v) for v in assignments.get("requires", [])],
                "unlocked_buildings": unlocked_buildings,
            }
            unlock_rows.append(row)
    return unlock_rows


def build_records() -> tuple[list[BuildingRecord], list[dict[str, object]]]:
    buildings = load_buildings(BUILDINGS_DIR)
    unlock_rows = load_unlocks(ADVANCES_DIR)

    for row in unlock_rows:
        for building_name in row["unlocked_buildings"]:
            record = buildings.setdefault(
                building_name,
                BuildingRecord(name=building_name, source_file="not found in building_types"),
            )
            record.unlock_advances.append(str(row["advance"]))
            record.tech_levels.append(str(row["tech_level"]) if row["tech_level"] else "")
            record.ages.append(str(row["age"]) if row["age"] else "")
            record.direct_requires.append(", ".join(row["requires"]) if row["requires"] else "")

    return sorted(buildings.values(), key=lambda item: item.name), unlock_rows


def write_csv(records: list[BuildingRecord], destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "building",
                "building_source_file",
                "can_build_rural",
                "can_build_town",
                "can_build_city",
                "can_build_megalopolis",
                "unlock_advance",
                "advance_age",
                "starting_technology_level",
                "advance_requires",
            ]
        )
        for record in records:
            row_count = max(1, len(record.unlock_advances))
            for index in range(row_count):
                writer.writerow(
                    [
                        record.name,
                        record.source_file,
                        record.can_build_rural,
                        record.can_build_town,
                        record.can_build_city,
                        record.can_build_megalopolis,
                        record.unlock_advances[index] if index < len(record.unlock_advances) else "",
                        record.ages[index] if index < len(record.ages) else "",
                        record.tech_levels[index] if index < len(record.tech_levels) else "",
                        record.direct_requires[index] if index < len(record.direct_requires) else "",
                    ]
                )


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    header_line = "| " + " | ".join(headers) + " |"
    separator = "| " + " | ".join(["---"] * len(headers)) + " |"
    data_lines = ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join([header_line, separator, *data_lines])


def write_markdown(records: list[BuildingRecord], unlock_rows: list[dict[str, object]], destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)

    total_buildings = len(records)
    unlocked_buildings = sum(1 for record in records if record.unlock_advances)
    buildings_without_tech = total_buildings - unlocked_buildings

    preview_rows: list[list[str]] = []
    for record in records:
        if not record.unlock_advances:
            continue
        preview_rows.append(
            [
                record.name,
                record.unlock_advances[0],
                record.ages[0] or "",
                record.tech_levels[0] or "",
                record.can_build_rural,
                record.can_build_town,
                record.can_build_city,
                record.can_build_megalopolis,
                record.direct_requires[0] or "",
            ]
        )
        if len(preview_rows) >= 40:
            break

    no_unlock_preview = [
        [
            record.name,
            record.source_file,
            record.can_build_rural,
            record.can_build_town,
            record.can_build_city,
            record.can_build_megalopolis,
        ]
        for record in records
        if not record.unlock_advances
    ][:40]

    lines = [
        "# Building and Advance Report",
        "",
        f"- Building definitions found: `{total_buildings}`",
        f"- Buildings unlocked by at least one advance: `{unlocked_buildings}`",
        f"- Buildings with no matching `unlock_building` entry: `{buildings_without_tech}`",
        f"- Advance blocks with `unlock_building`: `{len(unlock_rows)}`",
        "",
        "## Buildings Unlocked By Advances",
        "",
        markdown_table(
            ["building", "unlock_advance", "age", "tech_level", "rural", "town", "city", "megalopolis", "advance_requires"],
            preview_rows or [["(none found)", "", "", "", "", "", "", "", ""]],
        ),
        "",
        "## Buildings Without Matching Advance Unlock",
        "",
        markdown_table(
            ["building", "source_file", "rural", "town", "city", "megalopolis"],
            no_unlock_preview or [["(none found)", "", "", "", "", ""]],
        ),
        "",
        "Full data is available in the CSV file written beside this report.",
    ]

    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract building definitions and their advance unlock requirements."
    )
    parser.add_argument(
        "--output-dir",
        default=str(OUTPUT_DIR),
        help="Directory where CSV and Markdown reports will be written.",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    records, unlock_rows = build_records()
    write_csv(records, output_dir / "building_tech_matrix.csv")
    write_markdown(records, unlock_rows, output_dir / "building_tech_report.md")

    print(f"Wrote {output_dir / 'building_tech_matrix.csv'}")
    print(f"Wrote {output_dir / 'building_tech_report.md'}")
    print(f"Buildings: {len(records)}")
    print(f"Unlocked by advances: {sum(1 for record in records if record.unlock_advances)}")


if __name__ == "__main__":
    main()
