# City Prestige System

This document describes the optimized City Prestige system used by the Bronze Era total conversion.

## Purpose

City Prestige ranks important urban centers without running expensive monthly world scans.

Prestige represents the international importance of a location through:

- population;
- prosperity;
- capital status;
- maritime and commercial activity;
- palatial or monumental construction;
- historical importance;
- military reputation.

The system is intentionally lightweight. It does not add laws, privileges,
buildings, or technologies. A small yearly event pool gives prestigious cities
positive opportunities and exposes them to decline when food, trade, or
prosperity fail.

## Eligible Locations

Only locations with one of these exact EU5 settlement ranks participate:

- `location_rank:city`;
- `location_rank:megalopolis`.

Capitals, ports, market centers, historic locations, and highly populated
locations do not qualify while they remain towns, villages, rural settlements,
or tribal settlements. Every five yearly pulses, countries register newly
upgraded cities and remove locations that have fallen below city rank.

## Variables

The following variables are stored on location scopes:

| Variable | Purpose |
| --- | --- |
| `bronze_city_prestige_enabled` | Marks a location as participating in the system. |
| `bronze_city_prestige_score` | Stores the current calculated prestige score. |
| `bronze_city_prestige_rank` | Stores the current rank from `1` to `5`. |
| `bronze_city_prestige_global_rank` | Stores the city's current position in the global ranking. |
| `bronze_city_prestige_rank_percentile` | Stores the city's percentile position and supplies the placement requirement for its influence category. |
| `bronze_city_prestige_foreign_migration_cooldown` | Prevents repeated prestige migration routes for four years. |
| `bronze_historic_city` | Optional historical prestige value added to the score. |
| `bronze_city_monument_score` | Optional prestige supplied by another monument system. |
| `bronze_city_prestige_military_score` | Optional military prestige supplied by future events or mechanics. |

Countries use:

| Variable | Purpose |
| --- | --- |
| `bronze_city_prestige_bronze_country` | Marks countries that started with a Bronze template. |
| `bronze_city_prestige_eligibility_years` | Controls the five-year eligibility scan. |
| `bronze_city_prestige_cities` | Compact variable list containing the country's tracked cities. |
| `bronze_city_prestige_ledger_cities` | Global GUI list containing every ranked city shown in the ledger. |
| `bronze_city_prestige_influence_score` | Combined influence from cities owned in the global top fifteen. |

## Score Calculation

The score is recalculated once per year.

Immediately before the global sort, every registered city score is recalculated
again. This prevents country yearly-pulse order from ranking one country with
new values and another with values from the previous year.

Population values in EU5 location triggers are expressed in thousands.

### Settlement Rank

| Settlement | Points |
| --- | ---: |
| City | +25 |
| Megalopolis | +100 |

The larger initial score makes a megalopolis structurally more prestigious
without guaranteeing it a permanent high rank.

### Population

Population thresholds are cumulative:

| Population | Points |
| --- | ---: |
| At least 10,000 | +10 |
| At least 50,000 | +25 |
| At least 100,000 | +50 |
| At least 250,000 | +100 |
| At least 500,000 | +200 |

Example: a city with 100,000 inhabitants receives `10 + 25 + 50 = 85` population prestige.

### Prosperity

Prosperity contributes one non-cumulative award:

| Prosperity | Points |
| --- | ---: |
| At least -25% | +5 |
| At least 0% | +10 |
| At least 25% | +20 |
| At least 50% | +35 |
| At least 75% | +50 |

Only the highest matching bracket is applied. A prosperous city therefore
gains international importance, while prosperity never outweighs the main
population, building, political, and historical sources by itself.

### Political Status

| Condition | Points |
| --- | ---: |
| Country capital | +50 |

### Trade And Maritime Status

A city receives this award only once, even if it satisfies several conditions.

| Condition | Points |
| --- | ---: |
| Market center or port | +50 |

### Building Prestige

Building points are cumulative and configured in one dedicated file:

`in_game/common/scripted_effects/01_bronze_city_prestige_building_points.txt`

| Building | Points |
| --- | ---: |
| `market_village` | +10 |
| `marketplace` | +20 |
| `entrepot` | +30 |
| `trading_hub` | +40 |
| `stock_exchange` | +50 |
| `bronze_age_palatial_complex` | +100 |

To add another building, copy one `if` block in that file and change only:

1. `building_type:your_building_id`;
2. the number after `add =`.

No other City Prestige script needs to be edited for an urban building.

### Monumental Status

The value of `bronze_city_monument_score` is added directly to the score.

### Historical Status

The value of `bronze_historic_city` is added directly to the final score.

Recommended values:

| Historical importance | Suggested value |
| --- | ---: |
| Important regional center | 25 |
| Major Bronze Age city | 50 |
| Great royal or sacred center | 100 |
| Exceptional world-historical center | 150-200 |

### Military Prestige

The value of `bronze_city_prestige_military_score` is added directly to the final score.

This is an extension hook. The base system does not currently create battle or siege events.

Future systems may use it for:

- successful city defenses;
- victories near the city;
- royal triumphs;
- famous garrisons;
- temporary wartime prestige.

## World Position And Influence Rank

Only one rank modifier is active and visible on a location at a time. The
location effects panel therefore displays a single entry such as
`City Prestige: Great City`, containing all gameplay effects for that rank.

The system tracks two different values:

- **World Position** is the exact numerical place in the annual prestige
  table. The highest-prestige city is rank 1, the next is rank 2, and so on.
- **Influence Rank** is the city's gameplay category: World, Imperial, Great,
  Regional, or Local City.

Influence Rank combines the city's exact placement with its raw prestige:

| Influence rank | Placement | Minimum prestige | Political requirement |
| --- | --- | ---: | --- |
| World City | Exact world rank 1 | None | None |
| Imperial City | Top 20% | 100 | Located in an empire, or the capital of a kingdom |
| Great City | Top 45% | 75 | None |
| Regional City | Top 75% | 45 | None |
| Local City | Remaining cities | None | None |

There can therefore be only one World City. An important non-capital city in a
kingdom may be a Great City, but cannot be called Imperial without belonging
to an empire. A kingdom receives the Imperial title only for its capital.

World Position never uses zero after a completed sort. A newly registered city
shows `-` while waiting for the next complete sort; it is never given a false
provisional position. The ranking manager rebuilds a pool directly from every
urban location, sorts it, and assigns unique consecutive positions from 1.

Cities are sorted by:

1. prestige score, descending;
2. population, descending, when prestige values are equal;
3. the persistent global location-list order as the deterministic final fallback.

The final fallback is deterministic because world locations enter the
persistent list in map iteration order.

## Rank Effects

Effects are deliberately limited to avoid making prestige the dominant economic system.

| Rank | Migration attraction | Local trade center power |
| ---: | ---: | ---: |
| World City | +15% | +10% |
| Imperial City | +10% | +7.5% |
| Great City | +5% | +5% |
| Regional City | +2.5% | None |
| Local City | +1% | None |

No research modifier is currently applied because EU5 does not expose a reliable location-scoped research-speed modifier. A fake or country-wide substitute was intentionally avoided.

## Performance Model

The system avoids:

- monthly world scans;
- population loops during normal ranking updates;
- repeated exact comparisons between every city.

The famine and exodus event options may iterate the affected city's pops once
to apply proportional losses. These loops run only when the rare event fires,
not during the yearly ranking calculation.

At game start, one world scan initializes existing cities and megalopolises.
When an older save does not contain the initialization marker, the first
monthly country pulse performs the same scan once and reconstructs every city
list, rank modifier, owner reward, and player ledger cache.

After initialization:

- each country stores its eligible locations in `bronze_city_prestige_cities`;
- every eligible location is also registered once in the persistent global
  `bronze_city_prestige_world_cities` list;
- country updates iterate their compact owner lists, while the single ranking
  manager rebuilds and sorts the world pool once per yearly ranking pass;
- stale entries created by ownership changes are ignored by an owner check;
- a broader owned-location eligibility scan runs once every five years.

One human country is selected as the ranking manager at game start. Only this
country sorts the global city list, assigns exact global positions, and applies
top-fifteen rewards. After the sort, a separate global display list is rebuilt
for the ledger. This uses EU5's native `GetGlobalList` GUI path and cannot alter
the rank variables produced by the ranking system.

## Prestigious City Events

The yearly country pulse samples at most one rare event and then applies a
three-year country cooldown.

Positive opportunities:

- **Scholars Gather**, for Great Cities or higher;
- **Famous Craftsmen**, for Great Cities or higher with artisan industry;
- **Merchant Caravan**, for Regional Cities or higher with trade infrastructure;
- **Foreign Envoys**, for Imperial Cities or the World City.

Urban decline:

- **Urban Famine**, when a populous prestigious city has critically low food;
- **Trade Collapse**, when a prestigious city has poor market access;
- **Population Exodus**, after severe prosperity loss or recent raid damage.

Each temporary location modifier changes the next annual City Prestige score,
so a crisis can lower a city's rank and a successful urban opportunity can
raise it.

## Royal Capitals

When a country's capital is a Regional City or higher, the country receives one
consolidated legitimacy modifier:

| Capital influence rank | Monthly legitimacy |
| --- | ---: |
| Regional City | +0.02 |
| Great City | +0.05 |
| Imperial City | +0.10 |
| World City | +0.15 |

The modifier is recalculated after every world ranking and is removed
automatically if the capital changes or loses its qualifying influence rank.

The location window contains a compact City Prestige badge above the normal
condition icons. It displays the city's world position; its tooltip displays
the raw score and exact effects. This keeps the information accessible even
when the generic timed-modifier stack contains many unrelated modifiers.

Influence categories use global percentile thresholds and minimum raw scores
after sorting every eligible city. This keeps the number of prestigious cities
proportional to the living world while preventing weak cities from receiving a
high title solely because few cities currently exist.

## Great Cities Ledger

The standard ledger contains a `Great Cities` tab. It lists every ranked city in
descending score order and displays:

- exact world rank;
- city and owner;
- prestige score;
- population;
- dominant culture.

The ledger reads one global list created during the ordered world-ranking pass.
It does not filter by discovery, ownership, or Influence Rank. Every `city` and
`megalopolis`, including Local Cities, appears in the table. A versioned player
bootstrap repairs converted saves, while a cheap monthly guard rebuilds the
ranking only if the global GUI list is absent or empty.

## Urban Influence

The global top fifteen cities contribute Urban Influence to their owners:

| Global position | Influence points |
| ---: | ---: |
| 1 | 8 |
| 2-3 | 5 each |
| 4-5 | 3 each |
| 6-10 | 2 each |
| 11-15 | 1 each |

Influence is converted into one consolidated national modifier:

| Influence | Power Projection | Monthly Prestige |
| ---: | ---: | ---: |
| 1-2 | +1 | +0.005 |
| 3-4 | +3 | +0.01 |
| 5-7 | +5 | +0.02 |
| 8-12 | +8 | +0.03 |
| 13 or more | +10 | +0.05 |

## Foreign Urban Migration

Cities in the global top thirty can occasionally attract a small migration
route from a neighboring country or a country known by their owner.

The route:

- moves real source-country peasants;
- preserves their culture and religion;
- lasts 24 months;
- moves approximately 24-72 people depending on global rank;
- has a four-year per-city cooldown.

This creates limited cosmopolitan minorities without replacing the local
population majority or generating population from nothing.

## Adding A Historic City

Use a known location ID in a scripted effect or an on-game-start extension:

```txt
location:athens = {
	set_variable = {
		name = bronze_historic_city
		value = 100
	}
	bronze_city_prestige_initialize_city = yes
	bronze_city_prestige_recalculate_city = yes
}
```

Do not add a historical city until its exact EU5 location ID has been verified.

Recommended candidates include:

- Babylon;
- Nineveh;
- Memphis;
- Egyptian Thebes;
- Athens;
- Mycenae;
- Troy;
- Susa;
- Tyre;
- Sidon;
- Ur.

The examples are not hardcoded because several archaeological sites use different EU5 location names.

## Adding Monument Prestige

Another system may assign prestige without modifying the City Prestige calculation:

```txt
location:example_location = {
	set_variable = {
		name = bronze_city_monument_score
		value = 100
	}
	bronze_city_prestige_initialize_city = yes
	bronze_city_prestige_recalculate_city = yes
}
```

## Adding Military Prestige

Permanent military prestige:

```txt
location:example_location = {
	set_variable = {
		name = bronze_city_prestige_military_score
		value = 50
	}
	bronze_city_prestige_initialize_city = yes
	bronze_city_prestige_recalculate_city = yes
}
```

Increasing an existing score:

```txt
location:example_location = {
	if = {
		limit = {
			NOT = { has_variable = bronze_city_prestige_military_score }
		}
		set_variable = {
			name = bronze_city_prestige_military_score
			value = 0
		}
	}
	change_variable = {
		name = bronze_city_prestige_military_score
		add = 25
	}
}
```

The normal yearly update will include the new military value. Call `bronze_city_prestige_recalculate_city = yes` immediately only when the result must be visible without waiting for the next yearly pulse.

## Bronze Template Maintenance

EU5 setup templates cannot be queried dynamically after game start.

For that reason, `bronze_city_prestige_is_bronze_country` contains the tags that currently use:

- `Bronze`;
- `Bronze_coast`;
- `bronze_balkan`;
- `bronze_china_korea`;
- `bronze_city_state`;
- `bronze_empire`;
- `bronze_india`;
- `bronze_italy`;
- `bronze_japan`;
- `bronze_maritime`;
- `bronze_mesoamerica`;
- `bronze_north_africa`;
- `bronze_palatial_kingdom`;
- `bronze_southeast_asia`.

When a country changes to or from a Bronze template in `main_menu/setup/start/10_countries.txt`, update:

`in_game/common/scripted_triggers/00_bronze_city_prestige_triggers.txt`

This list affects automatic eligibility for rural Bronze capitals. Ordinary towns, cities, ports, markets, historic sites, and large population centers remain dynamically eligible regardless of template.

## Main Scripted Effects

| Effect | Scope | Purpose |
| --- | --- | --- |
| `bronze_city_prestige_initialize_city` | Location | Enables a city and registers it in the owner list. |
| `bronze_city_prestige_recalculate_city` | Location | Rebuilds the score from all current sources. |
| `bronze_city_prestige_apply_rank` | Location | Removes old rank modifiers and applies the correct rank. |
| `bronze_city_prestige_yearly_update` | Country | Recalculates cities in the compact country list. |
| `bronze_city_prestige_update_world_ranking` | Country | Performs the single yearly world sort and rebuilds player ledgers. |
| `bronze_city_prestige_apply_owner_reward` | Country | Applies one consolidated Urban Influence modifier. |
| `bronze_city_prestige_try_foreign_migration` | Location | Rolls a controlled foreign migration route for high-ranked cities. |
| `bronze_city_prestige_five_year_eligibility_update` | Country | Finds newly eligible locations and repairs ownership lists. |
| `bronze_city_prestige_initialize_world` | Global | Initializes the system at campaign start. |

## Files

- Triggers: `in_game/common/scripted_triggers/00_bronze_city_prestige_triggers.txt`
- Building points: `in_game/common/scripted_effects/01_bronze_city_prestige_building_points.txt`
- Effects: `in_game/common/scripted_effects/02_bronze_city_prestige_effects.txt`
- On-action logic: `in_game/common/on_action/00_bronze_city_prestige_on_action.txt`
- Yearly pulse hook: `in_game/common/on_action/country_yearly.txt`
- Game-start hook: `in_game/common/on_action/_hardcoded.txt`
- Static modifiers: `main_menu/common/static_modifiers/00_bronze_city_prestige_modifiers.txt`
- Ledger page: `in_game/gui/bronze_city_prestige_ledger.gui`
- Ledger tab registration: `in_game/gui/pops_overview.gui`
- English localization: `localization/english/Bronze_static_modifiers_l_english.yml`
- French localization: `localization/french/Bronze_static_modifiers_l_french.yml`

Localization files must remain encoded as UTF-8 with BOM.

## UI

The population ledger contains a `Great Cities` tab implemented in:

`in_game/gui/bronze_city_prestige_ledger.gui`

The tab displays every city and megalopolis in the world. It shows exact global
rank, city, owner, score, population, dominant culture,
Urban Influence, and the country's current Power Projection.

## Testing Checklist

Start a new campaign after changing game-start setup.

Verify:

1. Existing towns and cities receive a City Prestige rank.
2. Bronze-template capitals are ranked even when their initial rank is rural.
3. A capital receives 50 score.
4. A port or market receives the commercial 50 score only once.
5. A Palatial Complex adds 100 score.
6. Rank modifiers change when the score crosses a threshold.
7. Newly urbanized or sufficiently populated locations join within five years.
8. Conquered cities are registered by their new owner during the five-year repair pass.
9. English and French modifier names display correctly.
10. The `Great Cities` tab opens and lists all cities and megalopolises.
11. Clicking a ledger row moves the camera to that city.
12. No City Prestige errors appear in `error.log`.

## Troubleshooting

### A city is not ranked

Check:

- the location is a town, city, capital, major port, market, historic city, monumental city, or has at least 50,000 inhabitants;
- `bronze_city_prestige_enabled` exists;
- the campaign was started after the initialization hook was added;
- five yearly pulses have passed for dynamically eligible locations.

### A city keeps an old rank

Run:

```txt
bronze_city_prestige_recalculate_city = yes
```

from that location's scope, or wait for the next yearly pulse.

### A conquered city stops updating

The five-year eligibility pass repairs the new owner's city list. The location remains enabled and is not deleted from the system.

### Localization is missing

Confirm:

- the localization file is in the correct language folder;
- the first line is `l_english:` or `l_french:`;
- the file uses UTF-8 with BOM;
- modifier localization uses the `STATIC_MODIFIER_NAME_` prefix.

### Script errors occur at load

Inspect:

- `Documents/Paradox Interactive/Europa Universalis V/logs/error.log`;
- missing country tags in the Bronze country trigger;
- misspelled building IDs;
- duplicate scripted effect, trigger, modifier, or localization IDs.
