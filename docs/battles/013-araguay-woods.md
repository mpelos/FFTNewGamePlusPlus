# 013 - Araguay Woods

Status: v2 implemented (entry 404, revised 2026-07-01) - Boco direct-scaled/controllable; vanilla monster tiers promoted with safer elite placement.
Chapter: 2 - "The Manipulator and the Subservient"
Battle order: Battle 12 (after Merchant City of Dorter)
Target version: Enhanced v1.5.0
ENTD: global entry **404** (battle_entd4, local entry 20)
File: `entd/battle_entd4_ent.bin` (embedded; swapped only in NG+ by the code mod)

Implemented with:

```powershell
python tools/battle_patch.py araguay
python tools/validate_ch2_v2.py
```

## Original Battle

Objective:

```text
Defeat all enemies!  - OR -  Save Chocobo!
```

Player deployment:

```text
Up to 4 units, including Ramza.
Rescuable unit: Boco. If the rescue route is chosen, Boco death is Game Over.
```

Vanilla enemy composition:

```text
5x Goblin
1x Black Goblin
```

## Design Goal

Araguay must remain a monster-pack rescue fight, not a human-style tactics squad. The first v2 pass
was too easy because normal Goblins still folded at NG++ scale. The revised v2 keeps the vanilla
shape but promotes each monster by one family tier:

```text
Vanilla Goblin       -> Black Goblin
Vanilla Black Goblin -> Gobbledygook
Added Red Panther    -> Coeurl
```

Boco remains the player-controlled rescue piece. Difficulty should come from stronger monster
tiers, the woods, and route pressure, not from helpless guest AI.

## Local Data Confirmed

```text
s0  Boco         Chocobo 94       rescue ally; direct-scaled/control
s1  vanilla elite Black Goblin    kept as Black Goblin 98 because it starts too close to Boco
s2  vanilla Goblin                promoted to Black Goblin 98
s3  distant vanilla Goblin        promoted to Gobbledygook 99
s4  vanilla Goblin                promoted to Gobbledygook 99 as the second elite body
s5  vanilla Goblin                promoted to Black Goblin 98
s6  vanilla Goblin                promoted to Black Goblin 98
s7  story unit                    leave lvl 254
s8  story unit                    leave lvl 254
s9  added flank monster           Coeurl 104, UnitID 0x87
```

Monster job IDs used by this implementation:

```text
94  Chocobo
97  Goblin
98  Black Goblin
99  Gobbledygook
103 Red Panther
104 Coeurl
105 Vampire Cat
```

## Proposed Composition (New Game++ Araguay v2)

| Slot | Monster | Level | Br/Fa | Purpose |
|---|---|---:|---|---|
| s0 | Boco | 100 | 72/40 | Controlled rescue target; level parity with party. |
| s1 | Black Goblin | 100 | 78/35 | Close to Boco; kept below Gobbledygook speed/threat so Boco gets a fair first move. |
| s2 | Black Goblin | 100 | 78/35 | Promoted vanilla Goblin; sturdy swarm body. |
| s3 | Gobbledygook | 101 | 78/35 | Distant promoted elite; replaces the too-close s1 Gobbledygook. |
| s4 | Gobbledygook | 102 | 78/35 | Second elite body; anchors the pack. |
| s5 | Black Goblin | 100 | 78/35 | Promoted vanilla Goblin; route pressure. |
| s6 | Black Goblin | 100 | 78/35 | Promoted vanilla Goblin; route pressure. |
| s9 | Coeurl | 101 | 78/35 | Added flanker; toned down from Vampire Cat after playtest showed Boco could be outrun too hard. |

No equipment, reaction, support, or movement bytes are used for monster tuning. The relevant levers
are monster job, level, JobLevel, Brave/Faith, position, and Boco control.

## Guest Handling

Boco uses generic monster charId `0x82`, so it cannot safely use the named-guest runtime scaler
without risking enemy monster matches. It is handled directly in ENTD:

```text
Level 100
JobLevel 8
Brave/Faith 72/40
player-control bit enabled
```

This preserves the rescue route while removing the old NG+ failure case where low-level AI Boco died
before the player had a fair answer.

## Positioning Plan

Keep the v2 slot layout:

- Gobbledygooks anchor the center/far lane and force the player to spend real actions on the pack.
- Black Goblins fill the vanilla lanes and stop the rescue route from being solved by one fast unit.
- Coeurl uses the added flank slot (`s9`, UnitID `0x87`) as the hunter without jumping all the way to Vampire Cat pressure.

The player should still be rewarded for routing Boco intelligently and preparing Ice, but the pack
should no longer collapse like a Chapter 1 monster group.

## Implementation Checklist

- [x] Replace all vanilla Goblin slots with Black Goblin (`98`).
- [x] Keep the close original Black-Goblin-tier slot as Black Goblin (`98`) so Boco has a fair first move.
- [x] Promote a farther Goblin slot (`s3`) and central slot (`s4`) to Gobbledygook (`99`).
- [x] Replace added Vampire Cat with Coeurl (`104`) in slot `s9`, UnitID `0x87`.
- [x] Preserve Boco level/control fix.
- [x] Keep story slots `s7/s8` untouched.
- [x] Validate with `python tools/validate_ch2_v2.py`.
- [x] Build/deploy to Reloaded-II.

## Test Questions

- Does the promoted pack feel meaningfully harder without turning the rescue into an unavoidable
  turn-one Boco failure?
- Does Coeurl create flank pressure without making the fight feel like a random battle
  monster spike?
- Do Gobbledygooks make the center sturdy enough that the fight no longer feels trivial?
- Is Ice preparation still rewarded?

## Sources

- Local Chapter 2 overview: `docs/battles/011-chapter-2-overview.md`
- Local monster family notes: `docs/battles/000-chapter-1-overview.md`
- Local implementation: `tools/battle_patch.py`
