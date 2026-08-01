# Historical Monuments And Urban Expansion

This document covers the historical-monument, Great Pyramid, urban-mission,
city-rivalry, and progressive-decline extensions to City Prestige.

## Placement Rule

Never activate a monument or historical ruin from a plausible name alone.
Confirm both:

1. the exact EU5 location identifier;
2. that the location polygon geographically contains the historical site.

All historical placements are centralized in:

`main_menu/setup/start/07_bronze_historical_monuments.txt`

An active custom-building monument appears inside that file's
`building_manager` block. Giza uses a dedicated Bronze Era building so its
economic effects can be balanced independently. Stonehenge retains its native
`work_of_art_manager` entry from `main_menu/setup/start/11_art.txt` instead of
receiving a duplicate building. Unconfirmed sites remain parse-safe comments
marked `TODO_MANUAL_LOCATION`.

## Confirmed Active Placements

| Monument | Location |
| --- | --- |
| Giza Pyramid Complex | `giza` (`bronze_monument_giza_pyramid_complex`) |
| Citadel of Mycenae | `argos` |
| Cyclopean Fortifications of Tiryns | `nafplio` |
| Palatial Complex of Knossos | `candia` |
| Royal Complex of Ugarit | `latakia` |
| Royal Complex of Yin Xu | `anyang` |
| Stonehenge | `amesbury` (`work_of_art:stonehenge`) |
| Brú na Bóinne | `drogheda` |

Giza is a special building and is snapshotted by the normal ruins conversion.
It grants `+200` City Prestige through the central score effect and no longer
receives vanilla Art Quality multipliers. Stonehenge is detected by its exact
work-of-art key and is destroyed when its location becomes ruins. The Greek
placements reuse explicit Bronze Era mappings already used for palace sites.
`karnak` is deliberately not used for Egyptian Karnak: the mod's location with
that identifier is in Central Asia.

Historical buildings use dedicated Bronze Era maintenance instead of vanilla
`capital_building_maintenance`. Porcelain, glass, paper, books, and other late
goods are excluded. Administrative and religious complexes consume small
amounts of `bronze_age_bronze` and `bronze_age_tablets`; fortified monuments use
bronze fittings, while prehistoric megaliths require only stone, timber, and
tools.

## Prepared But Not Placed

The building definitions, score values, ruin snapshots, and localization are
complete for these monuments:

| Monument | Historical region | Candidate IDs |
| --- | --- | --- |
| Palace of Pylos | Ano Englianos, western Messenia | `kalamata`, `modon`, `kyparissia` |
| Citadel of Troy | Hisarlik, southern Dardanelles | `canakkale`, `ayvacik` |
| Karnak Temple Complex | Thebes/Luxor | `qena`, `qus` |
| Luxor Temple | Thebes/Luxor | `qena`, `qus` |
| Abu Simbel | Lower Nubia | `aswan`, `kalabsha`, `qasr_ibrim` |
| Theban Necropolis | west bank of Thebes | `qena`, `qus` |
| Hattusa Complex | Bogazkale/Corum | `huseyinabad`, `corum` |
| Great Ziggurat of Ur | southern Mesopotamia | `nasiriyah`, `suq_al_shuyukh` |
| Assur Complex | middle Tigris | `al_sinn`, `mosul`, `tikrit` |
| Chogha Zanbil | Khuzestan south-east of Susa | `shush` |
| Su Nuraxi | Barumini | `isili`, `ales`, `seddori` |
| Avebury | Wiltshire | `amesbury` |

To activate a confirmed site, add exactly one line to the centralized
`building_manager`, for example:

```txt
bronze_monument_hattusa_complex = { level = 1 location = confirmed_location }
```

## Prepared Historical Ruins

Dholavira and Mohenjo-daro are fully prepared but inactive:

- `bronze_historical_ruin_dholavira_setup_effect`
- `bronze_historical_ruin_mohenjo_daro_setup_effect`

Candidate IDs are documented but are not activated:

- Dholavira: `kantha`
- Mohenjo-daro: `dubbi`

After verifying a location, activate it only in
`bronze_historical_ruins_initialize_world`:

```txt
location:confirmed_id = {
	bronze_historical_ruin_dholavira_setup_effect = yes
}
```

The effects preserve historical culture, religion, former prestige, ruin type,
and expedition data. They use the normal Ruins Expeditions age restrictions.

## Monument Integration

Buildings are defined in:

`in_game/common/building_types/01_bronze_historical_monuments.txt`

City Prestige points are defined only in:

`in_game/common/scripted_effects/01_bronze_city_prestige_building_points.txt`

This is the only score source, preventing double counting. Stonehenge's exact
native work-of-art key is evaluated in the same effect.
Before razing or voluntary abandonment destroys buildings,
`bronze_historic_monuments_snapshot_for_ruins` stores monument identities and
royal, religious, military, administrative, commercial, and port categories.

## Great Pyramid Project

Egypt uses its real mod tag, `0002G`.

- Giza is the first Great Pyramid complex.
- `bronze_second_great_pyramid_committed` is a persistent global lifetime lock.
- Starting a project consumes the only remaining world slot.
- Destruction or abandonment never clears that lock.
- Suspended work retains the unfinished pyramid and can be resumed.
- The phases take roughly 23-29 years according to player choices.
- Reduced plans finish with 50 fewer City Prestige points than the full design.

Generic actions:

- `bronze_begin_great_pyramid_project`
- `bronze_resume_great_pyramid_project`

Console phase test:

```txt
event bronze_city_prestige_debug.2
```

## Urban Missions

The five-year pass opens one mission window per eligible country. Only one
mission may be active, and the selected city receives a 15-year completion
cooldown.

Available missions:

- Grand Festival
- Artisans and Scribes
- Develop the Market
- Restore Fortifications
- Secure Food Supply

Success adds persistent mission prestige and a temporary thematic modifier.
Failure applies a real loss and an eight-year cooldown. Both outcomes call the
central ranking update immediately.

## Great-City Rivalries

Every five years, an eligible country has a 6% chance to generate a rivalry.
Only Great Cities or higher can participate. Rivalries may be internal or
involve a neighboring country.

Both exact locations store each other as object variables for 40 years.
Countries receive a 30-year cooldown. Rivalries can create investment, a trade
accord, damaged relations, sabotage, or a limited vanilla insult casus belli,
but never directly declare war.

## Progressive Urban Decline

The single world-ranking manager evaluates decline during the existing
five-year scan. No monthly location scan is added.

Pressure comes from persistent combinations of low population, prosperity,
market access, control, food, recent sack/raze damage, and lack of major urban
functions.

Two consecutive bad five-year checks are required to advance one stage. Two
good checks recover one stage:

1. Stagnant City: -10 City Prestige
2. Urban Decline: -25 City Prestige
3. Abandoned Districts: -50 City Prestige
4. Nearly Abandoned City: -80 City Prestige

After twenty years at Stage 4, the owner chooses costly restoration, partial
evacuation, or controlled abandonment. Abandonment uses the existing ancient
ruins pipeline and never happens automatically.

## National Effects

The highest-ranked city owned by each country supplies one modest diplomatic
modifier. No country can stack this reward from several cities. The modifier
is transferred during each world sort.

## Debug

Open the City Prestige debug menu:

```txt
event bronze_city_prestige_debug.1
```

It can rebuild ranks and the ledger, open mission selection, test all four
decline stages, trigger the abandonment event, and restore the capital.

Open the next active pyramid phase:

```txt
event bronze_city_prestige_debug.2
```

Resolve the currently active urban mission immediately:

```txt
event bronze_city_prestige_debug.3
```

Create a rivalry test from eligible Great Cities:

```txt
event bronze_city_prestige_debug.4
```

