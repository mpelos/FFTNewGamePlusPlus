# Runtime raw stats for Chapter 3+ humans

This document is the starting reference for Chapter 3+ runtime stat recalculation.

Scope:

```text
Included:
- generic human enemies in jobs 74-93;
- active allied guests when a battle doc explicitly requires them, using the guest's live
  job-growth/multiplier bytes instead of a hardcoded generic-job assumption.

Excluded:
- inactive story actors, story bosses, Lucavi, monsters, transform forms, and Chapter 1/2 units
  unless a separate battle-specific runtime rule explicitly opts them in.
```

## Confidence

```text
HIGH   = confirmed in Ivalice Chronicles data/runtime or local reverse engineering.
MEDIUM = classic FFT stat model carried forward; good enough to implement, then validate in-game.
```

## Level-1 generic bases

Working classic FFT base seeds:

| Gender | HP | MP | Speed | PA | MA | Confidence |
|---|---:|---:|---:|---:|---:|---|
| Male | 30 | 15 | 6 | 4 | 3 | MEDIUM |
| Female | 28 | 16 | 6 | 3 | 4 | MEDIUM |

Use male/female only for ordinary generic humans and active human guests. If a unit is a monster,
Lucavi, inactive story actor, or story boss, do not use this table unless a separate runtime rule
explicitly says so.

## Growth model

Job growth constants are inverse: lower growth is better.

Working model for a unit treated as if it leveled entirely in its current job:

```text
raw = level_1_gender_base
for currentLevel = 1 to targetLevel - 1:
  raw += raw / (growth + currentLevel)

displayStat = floor(raw * multiplier / 100)
```

Preserve fractions while looping. If this is implemented with only visible integer stats, Speed/PA/MA
growth will be undercounted because many level-up increments are fractional. Runtime code should use a
scaled integer or equivalent fixed-point representation, then floor only for the final display stat.

For our runtime patch, `displayStat` is the target battle stat:

```text
HP     -> Max HP / Current HP, with no mid-fight healing
MP     -> Max MP / Current MP, with no mid-fight refill
Speed  -> Raw Speed, then Effective Speed adjusted by the same equipment delta
PA     -> Raw PA, then Effective PA adjusted by the same equipment delta
MA     -> Raw MA, then Effective MA adjusted by the same equipment delta
```

The HP/MP path does not currently have a separate confirmed raw-vs-equipment pair like PA/MA/Speed.
Until equipment HP/MP bonuses are mapped, treat the calculated value as the intended start-of-battle
max stat and only sync current HP/MP when the unit is still full. Never use this runtime pass as a
mid-fight heal/refill.

## Runtime fields

Actor table base and stride are documented in [02-battle-actor-table.md](02-battle-actor-table.md).

Fields needed for runtime stat scaling:

| Offset | Field | Use |
|---:|---|---|
| `+0x01` | State | Must not be `0xFF`; ignore inactive/preloaded entries. |
| `+0x03` | JobId | Must be a generic human job `74-93`. |
| `+0x04`/`+0x05` | Team/control bytes | Use with battle-specific guards; player-side units must never be patched. |
| `+0x06` | Gender flags | `0x80` male, `0x40` female, `0x20` monster. Skip monsters. |
| `+0x29` | Level | Already-expanded live level, not ENTD `100+` syntax. |
| `+0x30` | Current HP | Write only when preserving the current/full relationship. |
| `+0x32` | Max HP | Write recalculated HP. |
| `+0x34` | Current MP | Write only when preserving the current/full relationship. |
| `+0x36` | Max MP | Write recalculated MP. |
| `+0x38` | Raw PA | Write recalculated PA. |
| `+0x39` | Raw MA | Write recalculated MA. |
| `+0x3A` | Raw Speed | Write recalculated Speed. |
| `+0x3E` | Effective PA | Preserve equipment delta: `newRaw + (oldEffective - oldRaw)`. |
| `+0x3F` | Effective MA | Same. |
| `+0x40` | Effective Speed | Same. |
| `+0x8A` | HP Growth | Cached current-job value. |
| `+0x8B` | HP Multiplier | Cached current-job value. |
| `+0x8C` | MP Growth | Cached current-job value. |
| `+0x8D` | MP Multiplier | Cached current-job value. |
| `+0x8E` | Speed Growth | Cached current-job value. |
| `+0x8F` | Speed Multiplier | Cached current-job value. |
| `+0x90` | PA Growth | Cached current-job value. |
| `+0x91` | PA Multiplier | Cached current-job value. |
| `+0x92` | MA Growth | Cached current-job value. |
| `+0x93` | MA Multiplier | Cached current-job value. |

Prefer the cached growth/multiplier block over a hardcoded job table when possible. It reflects the
unit's actual loaded job data, including modded job-table values.

Gender flags are cross-checked from the neighboring `FFTGenericChronicle` runtime map:
`Male=0x80`, `Female=0x40`, `Monster=0x20` at actor-table offset `+0x06`.

## Generic job constants

Source of truth:

```text
D:\Projects\FFTGenericChronicle\work\external\fftivc.utility.modloader\fftivc.utility.modloader\TableData\JobData.xml
```

Upstream reference:

```text
https://github.com/Nenkai/fftivc.utility.modloader/blob/master/fftivc.utility.modloader/TableData/JobData.xml
```

Only the generic human rows are copied here.

| JobId | Job | HP C | HP M | MP C | MP M | Sp C | Sp M | PA C | PA M | MA C | MA M | Move | Jump | C-Ev |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 74 | Squire | 11 | 100 | 15 | 75 | 100 | 100 | 60 | 90 | 50 | 80 | 4 | 3 | 5 |
| 75 | Chemist | 12 | 80 | 16 | 75 | 100 | 100 | 75 | 75 | 50 | 80 | 3 | 3 | 5 |
| 76 | Knight | 10 | 120 | 15 | 80 | 100 | 100 | 40 | 120 | 50 | 80 | 3 | 3 | 10 |
| 77 | Archer | 11 | 100 | 16 | 65 | 100 | 100 | 45 | 110 | 50 | 80 | 3 | 3 | 10 |
| 78 | Monk | 9 | 135 | 13 | 80 | 100 | 110 | 48 | 129 | 50 | 80 | 3 | 4 | 20 |
| 79 | White Mage | 10 | 80 | 10 | 120 | 100 | 110 | 50 | 90 | 50 | 110 | 3 | 3 | 5 |
| 80 | Black Mage | 12 | 75 | 9 | 120 | 100 | 100 | 60 | 60 | 50 | 150 | 3 | 3 | 5 |
| 81 | Time Mage | 12 | 75 | 10 | 120 | 100 | 100 | 65 | 50 | 50 | 130 | 3 | 3 | 5 |
| 82 | Summoner | 13 | 70 | 8 | 125 | 100 | 90 | 70 | 50 | 50 | 125 | 3 | 3 | 5 |
| 83 | Thief | 11 | 90 | 16 | 50 | 90 | 110 | 50 | 100 | 50 | 60 | 4 | 4 | 25 |
| 84 | Orator | 11 | 80 | 18 | 70 | 100 | 100 | 55 | 75 | 50 | 75 | 3 | 3 | 5 |
| 85 | Mystic | 12 | 75 | 10 | 110 | 100 | 100 | 60 | 50 | 50 | 120 | 3 | 3 | 5 |
| 86 | Geomancer | 10 | 110 | 11 | 95 | 100 | 100 | 45 | 110 | 50 | 105 | 4 | 3 | 10 |
| 87 | Dragoon | 10 | 120 | 15 | 50 | 100 | 100 | 40 | 120 | 50 | 50 | 3 | 4 | 15 |
| 88 | Samurai | 12 | 75 | 14 | 90 | 100 | 100 | 45 | 128 | 50 | 90 | 3 | 3 | 20 |
| 89 | Ninja | 12 | 70 | 13 | 50 | 80 | 120 | 43 | 122 | 50 | 75 | 4 | 4 | 30 |
| 90 | Arithmetician | 14 | 65 | 10 | 80 | 100 | 50 | 70 | 50 | 50 | 70 | 3 | 3 | 5 |
| 91 | Bard | 20 | 55 | 20 | 50 | 100 | 100 | 80 | 30 | 50 | 115 | 3 | 3 | 5 |
| 92 | Dancer | 20 | 60 | 20 | 50 | 100 | 100 | 50 | 110 | 50 | 95 | 3 | 3 | 5 |
| 93 | Mime | 6 | 140 | 30 | 50 | 100 | 120 | 35 | 120 | 40 | 115 | 4 | 4 | 5 |

## Implementation rules

For each generic human enemy:

```text
1. Arm the runtime scan only for the current NG+ battle entry.
2. Patch only configured enemy unit ids for that entry.
3. Confirm the actor entry is active: state != 0xFF.
4. Confirm it is enemy-side. Player-side units and guests are never eligible.
5. Confirm job id is 74-93.
6. Read gender flags from +0x06; choose male or female base; skip monsters/unknown flags.
7. Read the already-expanded live level from +0x29.
8. Read current-job growth/multiplier from +0x8A..+0x93.
9. Recalculate HP, MP, Speed, PA, and MA as if the unit leveled entirely in its current job.
10. Write Max HP/MP and preserve current HP/MP without healing/refilling if the unit is no longer full.
11. Write Raw PA/MA/Speed and preserve the old effective-minus-raw deltas.
12. Mark that unit id patched so a repeated scan cannot apply late HP/MP healing.
```

For each active allied guest opted into the pass:

```text
1. Arm the runtime scan only for the current NG+ battle entry.
2. Patch only the configured guest unit id for that entry.
3. Confirm the actor entry is active: state != 0xFF.
4. Confirm the expected allied/guest side and expected story unit id.
5. Do not require job id 74-93; named guest jobs can sit outside the generic range.
6. Read gender flags, live expanded level, and the live job growth/multiplier bytes from +0x8A..+0x93.
7. Recalculate HP, MP, Speed, PA, and MA using those live growth/multiplier bytes.
8. Preserve HP/MP current/full relationship and effective-stat equipment deltas.
9. Mark the guest patched so repeated scans cannot keep refreshing HP/MP.
10. Preserve the guest's scripted identity, control behavior, objective status, and special commands.
```

Do not run this globally for every active unit. It is a Chapter 3+ battle-start correction and should
be enabled entry-by-entry or unit-by-unit from the runtime plan.

## Sources

- Local Ivalice Chronicles job constants:
  `D:\Projects\FFTGenericChronicle\work\external\fftivc.utility.modloader\fftivc.utility.modloader\TableData\JobData.xml`
- Upstream Ivalice Chronicles job constants:
  <https://github.com/Nenkai/fftivc.utility.modloader/blob/master/fftivc.utility.modloader/TableData/JobData.xml>
- FFHacktics level-up simulator reference:
  <https://ffhacktics.com/wiki/Level_Up_Simulator>
- Community summary of the classic Battle Mechanics Guide formula:
  <https://steamcommunity.com/app/1004640/discussions/0/595162650440186676/>
