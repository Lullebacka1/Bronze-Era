# Bronze Era Positive Chronology

EU5's vanilla systems are safest when the internal calendar uses positive years.
Negative start dates can confuse systems that compare dates, schedule monthly or yearly pulses, store cooldowns, progress ages, trigger situations, and serialize saves.

The mod therefore uses a stable positive engine chronology:

- Internal engine date `1.1.1` = historical display date `1209 BC`
- Internal engine date `15.1.1` = historical display date `1195 BC`
- Internal engine date `1329.12.31` = historical display date `120 AD`

For the BC portion of the campaign, the approximate visual conversion is:

```text
Displayed BC year = 1210 - internal engine year
```

Age start mapping:

- Bronze: internal year `1` = `1209 BC`
- Iron: internal year `160` = `1050 BC`
- Archaic: internal year `410` = `800 BC`
- Classic: internal year `710` = `500 BC`
- Hellenistic: internal year `887` = `323 BC`
- Roman: internal year `1063` = `147 BC`

This keeps vanilla gameplay systems stable while presenting the mod as a Late Bronze Age and antique chronology through names, descriptions, situations, and documentation.

In-game topbar display:

- The vanilla engine date is preserved internally and remains visible as a small secondary line.
- The primary topbar date is driven by Bronze Era country variables initialized on game start.
- `bronze_display_year` counts down through the BC campaign.
- `bronze_display_ad_year` takes over once the internal chronology reaches the AD portion.
