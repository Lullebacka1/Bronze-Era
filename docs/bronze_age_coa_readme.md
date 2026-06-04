# Bronze Age Coat of Arms System

This mod uses EU5 scripted Coat of Arms definitions instead of flat `.tga` flags.

## Files Added

- `main_menu/common/coat_of_arms/coat_of_arms/00_bronze_age_coa.txt`
- `main_menu/common/flag_definitions/00_bronze_age_flags.txt`

The CoA file defines reusable Bronze Age flag compositions. The flag definition file attaches those CoAs to country tags.

## Asset Paths

Vanilla assets are used from:

- `main_menu/gfx/coat_of_arms/patterns/`
- `main_menu/gfx/coat_of_arms/colored_emblems/`
- `main_menu/gfx/coat_of_arms/textured_emblems/`

Custom Bronze Age emblems, if added later, should go in:

- `main_menu/gfx/coat_of_arms/colored_emblems/`
- `main_menu/gfx/coat_of_arms/textured_emblems/`

Recommended custom naming style:

- `ba_egypt_ankh.dds`
- `ba_hittite_storm_disk.dds`
- `ba_mycenaean_lion_gate.dds`
- `ba_trojan_gate.dds`
- `ba_assyrian_winged_sun.dds`
- `ba_phoenician_ship.dds`
- `ba_minoan_labrys.dds`
- `ba_sea_raider_helmet.dds`

## Required External DDS Emblems

None are required for the current implementation. All flags currently use vanilla EU5 CoA patterns and `colored_emblems`.

Optional custom replacements:

| Theme | Optional DDS | Suggested Path |
| --- | --- | --- |
| Egypt ankh | `ba_egypt_ankh.dds` | `main_menu/gfx/coat_of_arms/colored_emblems/ba_egypt_ankh.dds` |
| Hittite storm god disk | `ba_hittite_storm_disk.dds` | `main_menu/gfx/coat_of_arms/colored_emblems/ba_hittite_storm_disk.dds` |
| Mycenaean lion gate | `ba_mycenaean_lion_gate.dds` | `main_menu/gfx/coat_of_arms/colored_emblems/ba_mycenaean_lion_gate.dds` |
| Trojan city gate | `ba_trojan_gate.dds` | `main_menu/gfx/coat_of_arms/colored_emblems/ba_trojan_gate.dds` |
| Assyrian winged sun disk | `ba_assyrian_winged_sun.dds` | `main_menu/gfx/coat_of_arms/colored_emblems/ba_assyrian_winged_sun.dds` |
| Phoenician cedar or ship | `ba_phoenician_ship.dds` | `main_menu/gfx/coat_of_arms/colored_emblems/ba_phoenician_ship.dds` |
| Minoan labrys | `ba_minoan_labrys.dds` | `main_menu/gfx/coat_of_arms/colored_emblems/ba_minoan_labrys.dds` |
| Sea Peoples helmet | `ba_sea_raider_helmet.dds` | `main_menu/gfx/coat_of_arms/colored_emblems/ba_sea_raider_helmet.dds` |

## Tags Covered

Requested short tags:

- `EGY`, `HAT`, `MYC`, `TRO`, `ASS`, `BAB`, `PHO`, `MIN`, `LUK`, `SEA`, `NUB`, `ELA`, `URU`, `AHH`

Local Bronze Era aliases currently included:

- `0002G` for Egypt
- `HATTI` for Hatti
- `0001G` for Mycenae
- `WILUS` for Troy/Wilusa
- `ASYRI` for Assyria
- `KASSI` for Kassite Babylonia
- `SIDON` and `ARWAD` for Phoenician coastal city states
- `KNOSS`, `KYDON`, `PHAIS`, `MALIA`, `ZAKRO` for Minoan Cretan centers
- `LUKKA` for Lukka
- `ELAM` for Elam
- `URATU` for Urartu
- `ACHAE` for the Ahhiyawa/Achaean theme

## How To Test

1. Launch the game with the mod enabled.
2. Start a campaign.
3. Open the country selection screen or diplomacy panel for one of the covered tags.
4. Check that the country shield no longer uses a random/default flag.
5. Check `error.log` after launch.

## Common Error Causes

- The country uses a different tag than the one defined in `00_bronze_age_flags.txt`.
- A color name is not defined in `main_menu/common/named_colors/`.
- A DDS texture name is misspelled.
- A custom DDS is placed in the wrong folder.
- The CoA key in `flag_definitions` does not match the key in `coat_of_arms`.
- The file path is under `in_game` instead of `main_menu`.

## What To Check In `error.log`

Search for:

- `coat_of_arms`
- `flag_definition`
- `Unknown texture`
- `Unknown color`
- `Invalid CoA`
- the specific tag, such as `HATTI`, `0001G`, or `WILUS`

If the game loads but the flag does not change, the most likely cause is a tag mismatch.
