# Runtime raw stat formulas

This document records the FFT/IVC raw-stat formula and the runtime fields used to inspect or correct
specific edge cases. It is not a standard implementation requirement for Chapter 3+ battles.
Validated Gollund/Orran tests showed that Ivalice Chronicles already recalculates ordinary human
battle stats correctly from the expanded ENTD level, job growth, and job multipliers.

Default rule:

```text
Use ENTD level encoding (`100+` relative levels) as the normal scaling mechanism.
Do not apply runtime stat correction unless a specific unit is proven undergrown in-game.
```

Scope:

```text
Included:
- diagnostic calculations for generic human enemies in jobs 74-93;
- battle-specific runtime exceptions for active allied guests only when a test proves the guest is
  undergrown after normal ENTD scaling.

Excluded:
- inactive story actors, story bosses, Lucavi, monsters, transform forms, and Chapter 1/2 units
- normally scaled humans, unless a separate battle-specific runtime rule explicitly opts them in.
```

## Confidence

```text
HIGH   = confirmed in Ivalice Chronicles data/runtime or local reverse engineering.
MEDIUM = classic FFT stat model carried forward; good enough to implement, then validate in-game.
```

## Level-1 generic raw seeds

Classic FFT stores level-1 generic stats as hidden fixed-point raw values. One visible stat point is
`16384` raw units. Generic units are normally generated inside a small range; for this mod's
deterministic runtime correction, use the lower bound of each range as the seed.

| Gender | HP seed | MP seed | Speed seed | PA seed | MA seed | Fixed-point raw values | Confidence |
|---|---:|---:|---:|---:|---:|---|---|
| Male | 30 | 14 | 6 | 5 | 4 | HP `491520`, MP `229376`, Speed `98304`, PA `81920`, MA `65536` | MEDIUM |
| Female | 28 | 15 | 6 | 4 | 5 | HP `458752`, MP `245760`, Speed `98304`, PA `65536`, MA `81920` | MEDIUM |

Use male/female only for ordinary generic humans and active human guests. If a unit is a monster,
Lucavi, inactive story actor, or story boss, do not use this table unless a separate runtime rule
explicitly says so.

Do not use the old simplified visible bases (`Male HP30/MP15/Spd6/PA4/MA3`,
`Female HP28/MP16/Spd6/PA3/MA4`). Those are Squire-like visible approximations and understate
high-level PA/MA after recalculation.

## Growth model

Job growth constants are inverse: lower growth is better.

Working model for a unit treated as if it leveled entirely in its current job:

```text
RAW_SCALE = 16384
raw = level_1_gender_seed * RAW_SCALE
for currentLevel = 1 to targetLevel - 1:
  raw += raw / (growth + currentLevel)

displayStat = floor(raw * multiplier / (RAW_SCALE * 100))
```

Preserve fractions while looping. If this is implemented with only visible integer stats, Speed/PA/MA
growth will be undercounted because many level-up increments are fractional. Runtime code should use a
scaled integer or equivalent fixed-point representation, then floor only for the final display stat.
The current runtime uses the classic `16384` scale directly.

For a diagnostic/edge-case runtime patch, `displayStat` is the target battle stat:

```text
HP     -> Max HP / Current HP, with no mid-fight healing
MP     -> Max MP / Current MP, with no mid-fight refill
Speed  -> Raw Speed, then Effective Speed adjusted by the same equipment delta
PA     -> Raw PA, then Effective PA adjusted by the same equipment delta
MA     -> Raw MA, then Effective MA adjusted by the same equipment delta
```

If an exception patch is enabled, apply the recalculated value only when it is not lower than the
unit's current live stat. This pass is a correction for proven undergrown battle units, not a nerf
pass. For PA/MA/Speed, compare the final effective stat after preserving the equipment delta; if that
final stat would be lower, keep both the old raw and old effective bytes. For HP/MP visible pools,
never reduce Max HP/MP.

The HP/MP path does not currently have a separate confirmed raw-vs-equipment pair like PA/MA/Speed.
`+0x30/+0x32/+0x34/+0x36` are visible pools, not the hidden fixed-point raw stats. Until the real
raw HP/MP storage is mapped, treat the calculated value as the intended start-of-battle max stat and
only sync current HP/MP when the unit is still full. Never use this runtime pass as a mid-fight
heal/refill.

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
unit's actual loaded job data, including Ivalice Chronicles job-table changes and this mod's future
job edits. Some IVC rows differ from classic internet tables; the live bytes win.

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

## Diagnostic / exception implementation rules

Do not run this globally for every active unit. The current mod keeps the generic runtime-stat pass
disabled by default because the game already calculates normal human stats from level.

For each generic human enemy opted into an exception patch:

```text
1. Arm the runtime scan only for the current NG+ battle entry.
2. Patch only configured enemy unit ids for that entry.
3. Confirm the actor entry is active: state != 0xFF.
4. Confirm it is enemy-side. Player-side units and guests are never eligible.
5. Confirm job id is 74-93.
6. Read gender flags from +0x06; choose male or female base; skip monsters/unknown flags.
7. Read the already-expanded live level from +0x29.
8. Read current-job growth/multiplier from +0x8A..+0x93.
9. Recalculate HP, MP, Speed, PA, and MA from the `16384` raw seeds as if the unit leveled entirely
   in its current job.
10. Write Max HP/MP only if the current build intentionally enables visible-pool HP/MP writes, and
   only upward; preserve current HP/MP without healing/refilling if the unit is no longer full.
11. Write Raw PA/MA/Speed and preserve the old effective-minus-raw deltas, but never lower the final
   effective stat.
12. Mark that unit id patched so a repeated scan cannot apply late HP/MP healing.
```

For each active allied guest opted into an exception patch:

```text
1. Arm the runtime scan only for the current NG+ battle entry.
2. Patch only the configured guest unit id for that entry.
3. Confirm the actor entry is active: state != 0xFF.
4. Confirm the expected allied/guest side and expected story unit id.
5. Do not require job id 74-93; named guest jobs can sit outside the generic range.
6. Read gender flags, live expanded level, and the live job growth/multiplier bytes from +0x8A..+0x93.
7. Recalculate HP, MP, Speed, PA, and MA from the `16384` raw seeds using those live
   growth/multiplier bytes.
8. Preserve HP/MP current/full relationship and effective-stat equipment deltas.
9. Mark the guest patched so repeated scans cannot keep refreshing HP/MP.
10. Preserve the guest's scripted identity, control behavior, objective status, and special commands.
```

Every exception must name the battle, unit id, observed wrong stat, expected stat, and playtest proof.

## Sources

- Local Ivalice Chronicles job constants:
  `D:\Projects\FFTGenericChronicle\work\external\fftivc.utility.modloader\fftivc.utility.modloader\TableData\JobData.xml`
- Upstream Ivalice Chronicles job constants:
  <https://github.com/Nenkai/fftivc.utility.modloader/blob/master/fftivc.utility.modloader/TableData/JobData.xml>
- FFHacktics level-up simulator reference:
  <https://ffhacktics.com/wiki/Level_Up_Simulator>
- Community summary of the classic Battle Mechanics Guide formula:
  <https://steamcommunity.com/app/1004640/discussions/0/595162650440186676/>
