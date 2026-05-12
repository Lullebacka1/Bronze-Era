# The Sea Peoples Crisis

This module is a country-scoped dynamic disaster for the Bronze Era total conversion.

## Design

- Phase 1: climate pressure and famine.
- Phase 2: migration pressure and coastal raiding.
- Phase 3: trade crash, palace economy collapse, and internal breakdown.
- Phase 4: settlement pressure and political fragmentation.
- Phase 5: assimilation, Phoenician recovery, and Iron Age transition.

## Scope

The crisis targets countries tied to the eastern Mediterranean world: Greece, Cyprus, Anatolia, the Levant, coastal Egypt, Sicily, southern Italy, and related maritime cultures.

## Implementation

- Events live in `in_game/events/bronze_sea_peoples_crisis_events.txt`.
- Country variables are managed in `in_game/common/scripted_effects/00_bronze_sea_peoples_crisis_effects.txt`.
- Region/culture eligibility lives in `in_game/common/scripted_triggers/00_bronze_sea_peoples_crisis_triggers.txt`.
- Effects are applied through auto modifiers in `in_game/common/auto_modifiers/00_bronze_sea_peoples_crisis_modifiers.txt`.
- Yearly pulse hooks live in `in_game/common/on_action/00_bronze_sea_peoples_crisis_on_action.txt`.
- The vanilla `yearly_country_pulse` is preserved locally in `in_game/common/on_action/country_yearly.txt` and calls `sea_peoples_crisis_yearly_pulse`.

The Sea Peoples are intentionally not a normal permanent country. The system treats them as raiders, refugees, mercenaries, migrants, and temporary settlement pressure.
