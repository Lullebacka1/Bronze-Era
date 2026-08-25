# Building and Advance Report

- Building definitions found: `150`
- Buildings unlocked by at least one advance: `77`
- Buildings with no matching `unlock_building` entry: `73`
- Advance/building unlock rows written: `151`

## Buildings Unlocked By Advances

| building | unlock_advance | explicit_level | effective_level | level_source | rural | town | city | megalopolis | advance_requires |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| beer_iron_age | independent_craftsmen |  |  |  | no | yes | yes | yes | dispersion_of_authority_advance |
| beer_palace | royal_production_advance |  | 3 | inferred_from_prerequisite_workforce_specialization_advance | no | yes | yes | yes | workforce_specialization_advance |
| bog_iron_smelter | bog_iron_smelting_advance | 4 | 4 | explicit | yes | yes | yes | yes | bloomery_smelting_advance |
| bronze_age_aristocratic_mounds | aristocratic_burial_advance | 3 | 3 | explicit | yes | yes | no | no | aristocratic_recognition_advance |
| bronze_age_bronze_forge | bronze_forge_advance | 2 | 2 | explicit | no | yes | no | no | mining_advance |
| bronze_age_bronze_foundry | bronze_foundry_advance |  | 3 | inferred_from_prerequisite_workforce_specialization_advance | no | yes | yes | yes | workforce_specialization_advance |
| bronze_age_burial_pits | ceremonial_burial_advance | 1 | 1 | explicit | yes | yes | yes | no | settlements_advance |
| bronze_age_collective_tombs | ceremonial_burial_advance | 1 | 1 | explicit | yes | yes | yes | no | settlements_advance |
| bronze_age_palatial_complex | palace_economy_advance | 3 | 3 | explicit | no | no | yes | yes |  |
| bronze_age_trade_office | bronze_age_trade_posts_advance | 3 | 3 | explicit | no | yes | yes | yes | intercultural_relations_advance |
| bronze_age_triumphal_monument | triumphal_monuments_advance |  | 3 | inferred_from_prerequisite_royal_reliefs_advance | yes | yes | yes | yes | royal_reliefs_advance |
| bronze_age_urnfield_burial_site | urnfield_advance |  | 1 | inferred_from_prerequisite_ceremonial_burial_advance | yes | yes | yes | yes | ceremonial_burial_advance |
| bronze_age_victory_stelae | triumphal_monuments_advance |  | 3 | inferred_from_prerequisite_royal_reliefs_advance | yes | yes | yes | yes | royal_reliefs_advance |
| bronze_city_walls | bronze_city_walls_advance | 3 | 3 | explicit | no | setup_only | yes | yes | city_building_advance |
| bronze_dock | sailing_advance | 3 | 3 | explicit | no | yes | yes | yes | long_distance_trade_advance |
| bronze_monumental_gates | monumental_gates_advance | 4 | 4 | explicit | no | no | yes | yes | bronze_city_walls_advance |
| charcoal_maker | charcoal_maker_advance | 1 | 1 | explicit | yes | no | no | no | bronze_forge_advance |
| cyclopean_walls | cyclopean_walls_advance |  | 3 | inferred_from_prerequisite_bronze_city_walls_advance | no | setup_only | yes | yes | bronze_city_walls_advance |
| farming_village | agriculture_advance | 1 | 1 | explicit | yes | no | no | no |  |
| fine_cloth_iron_age | independent_craftsmen |  |  |  | no | yes | yes | yes | dispersion_of_authority_advance |
| fine_cloth_palace | royal_production_advance |  | 3 | inferred_from_prerequisite_workforce_specialization_advance | no | yes | yes | yes | workforce_specialization_advance |
| frontier_post | frontier_post_advance | 3 | 3 | explicit | yes | no | no | no | trade_caravans |
| gate_court | delegated_judicial_authority |  |  |  | no | yes | yes | yes | provincial_governors |
| hill_fort | hill_forts_advance | 4 | 4 | explicit | yes | yes | no | no | warrior_lodges_advance |
| house_of_remedies | house_of_remedies_advance | 1 | 1 | explicit | yes | no | no | no | settlements_advance |
| iron_citadel | iron_citadel_advance |  |  |  | yes | yes | no | no | provincial_governors |
| iron_city_walls | iron_city_walls_advance |  |  |  | no | setup_only | yes | yes | stone_dressing |
| irrigation_systems | irrigation_systems_advance | 1 | 1 | explicit | yes | yes | yes | yes | settlements_advance |
| jewelry_iron_age | independent_craftsmen |  |  |  | no | yes | yes | yes | dispersion_of_authority_advance |
| jewelry_palace | royal_production_advance |  | 3 | inferred_from_prerequisite_workforce_specialization_advance | no | yes | yes | yes | workforce_specialization_advance |
| market_village | standard_measurements_advance | 2 | 2 | explicit | yes | no | no | no | long_distance_trade_advance |
| mason | masonry_advance |  | 1 | inferred_from_prerequisite_agriculture_advance | yes | yes | yes | yes | mining_advance |
| megalithic_religious_monument | megalithic_monument_advance | 4 | 4 | explicit | yes | no | no | no | ritual_sites_advance |
| megaron | megarons_advance |  | 3 | inferred_from_prerequisite_palace_economy_advance | no | no | yes | yes | palace_economy_advance |
| merchants_quarters | merchants_quarters_unlock_advance |  | 3 | inferred_from_prerequisite_merchant_script_advance | no | yes | yes | yes | scribe_alphabetic_maintenance |
| naval_supplies_iron_age | independent_craftsmen |  |  |  | no | yes | yes | yes | dispersion_of_authority_advance |
| naval_supplies_palace | royal_navy_supply_advance |  | 3 | inferred_from_prerequisite_workforce_specialization_advance | no | yes | yes | yes | royal_weapon_workshop_advance |
| neolithic_feast_court | ritual_sites_advance |  | 1 | inferred_from_prerequisite_agriculture_advance | yes | yes | yes | yes | agriculture_advance |
| neolithic_granary | agriculture_advance | 1 | 1 | explicit | yes | yes | no | no |  |
| neolithic_leather_maker | animal_husbandry_advance |  | 1 | inferred_from_prerequisite_agriculture_advance | yes | yes | no | no | agriculture_advance |

## Buildings Without Matching Advance Unlock

| building | source_file | rural | town | city | megalopolis |
| --- | --- | --- | --- | --- | --- |
| black_market | in_game/common/building_types/pirate_buildings.txt | no | yes | yes | yes |
| bridge_infrastructure | in_game/common/building_types/common_buildings.txt | yes | yes | yes | yes |
| bronze_age_palace_house | in_game/common/building_types/00_bronze_age_palatial_complex.txt | yes | yes | yes | yes |
| bronze_monument_abu_simbel | in_game/common/building_types/01_bronze_historical_monuments.txt | yes | yes | yes | yes |
| bronze_monument_assur_complex | in_game/common/building_types/01_bronze_historical_monuments.txt | yes | yes | yes | yes |
| bronze_monument_avebury | in_game/common/building_types/01_bronze_historical_monuments.txt | yes | yes | yes | yes |
| bronze_monument_bru_na_boinne | in_game/common/building_types/01_bronze_historical_monuments.txt | yes | yes | yes | yes |
| bronze_monument_chogha_zanbil | in_game/common/building_types/01_bronze_historical_monuments.txt | yes | yes | yes | yes |
| bronze_monument_giza_pyramid_complex | in_game/common/building_types/01_bronze_historical_monuments.txt | yes | yes | yes | yes |
| bronze_monument_great_pyramid_new | in_game/common/building_types/01_bronze_historical_monuments.txt | no | no | yes | yes |
| bronze_monument_great_pyramid_unfinished | in_game/common/building_types/01_bronze_historical_monuments.txt | no | no | yes | yes |
| bronze_monument_hattusa_complex | in_game/common/building_types/01_bronze_historical_monuments.txt | yes | yes | yes | yes |
| bronze_monument_karnak_complex | in_game/common/building_types/01_bronze_historical_monuments.txt | yes | yes | yes | yes |
| bronze_monument_knossos_complex | in_game/common/building_types/01_bronze_historical_monuments.txt | yes | yes | yes | yes |
| bronze_monument_luxor_temple | in_game/common/building_types/01_bronze_historical_monuments.txt | yes | yes | yes | yes |
| bronze_monument_madau_giants_tombs | in_game/common/building_types/01_bronze_historical_monuments.txt | yes | yes | yes | yes |
| bronze_monument_mycenae_citadel | in_game/common/building_types/01_bronze_historical_monuments.txt | yes | yes | yes | yes |
| bronze_monument_nuraghe_arrubiu | in_game/common/building_types/01_bronze_historical_monuments.txt | yes | yes | yes | yes |
| bronze_monument_pylos_palace | in_game/common/building_types/01_bronze_historical_monuments.txt | yes | yes | yes | yes |
| bronze_monument_romanzesu | in_game/common/building_types/01_bronze_historical_monuments.txt | yes | yes | yes | yes |
| bronze_monument_santu_antine | in_game/common/building_types/01_bronze_historical_monuments.txt | yes | yes | yes | yes |
| bronze_monument_serra_orrios | in_game/common/building_types/01_bronze_historical_monuments.txt | yes | yes | yes | yes |
| bronze_monument_stonehenge | in_game/common/building_types/01_bronze_historical_monuments.txt | yes | yes | yes | yes |
| bronze_monument_su_nuraxi | in_game/common/building_types/01_bronze_historical_monuments.txt | yes | yes | yes | yes |
| bronze_monument_theban_necropolis | in_game/common/building_types/01_bronze_historical_monuments.txt | yes | yes | yes | yes |
| bronze_monument_tiryns_cyclopean | in_game/common/building_types/01_bronze_historical_monuments.txt | yes | yes | yes | yes |
| bronze_monument_troy_citadel | in_game/common/building_types/01_bronze_historical_monuments.txt | yes | yes | yes | yes |
| bronze_monument_ugarit_complex | in_game/common/building_types/01_bronze_historical_monuments.txt | yes | yes | yes | yes |
| bronze_monument_ur_ziggurat | in_game/common/building_types/01_bronze_historical_monuments.txt | yes | yes | yes | yes |
| bronze_monument_yin_xu | in_game/common/building_types/01_bronze_historical_monuments.txt | yes | yes | yes | yes |
| brothel | in_game/common/building_types/pirate_buildings.txt | no | yes | yes | yes |
| clay_pit | in_game/common/building_types/common_buildings.txt | yes | yes | yes | yes |
| construction_center | in_game/common/building_types/town_buildings.txt | no | yes | yes | yes |
| egyptian_canaanite_garrison | in_game/common/building_types/02_bronze_egyptian_canaanite_garrison.txt | yes | yes | yes | yes |
| elephant_hunting_grounds | in_game/common/building_types/rural_buildings.txt | yes | no | no | no |
| fiber_crops_farm | in_game/common/building_types/common_buildings.txt | yes | yes | yes | yes |
| fishing_village | in_game/common/building_types/rural_buildings.txt | yes | no | no | no |
| forest_village | in_game/common/building_types/rural_buildings.txt | yes | no | no | no |
| fruit_orchard | in_game/common/building_types/common_buildings.txt | yes | yes | yes | yes |
| horse_breeders | in_game/common/building_types/common_buildings.txt | yes | yes | yes | yes |

Full data is available in the CSV file written beside this report.
