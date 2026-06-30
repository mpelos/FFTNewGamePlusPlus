# 013 - Araguay Woods

Status: ✅ implemented (v1, entry 404); Boco scaled to party level (2026-06-27, playtest-confirmed) + **v2 redesign documented only** (implementation pending)
Chapter: 2 — "The Manipulator and the Subservient"
Battle order: Battle 12 (after Merchant City of Dorter)
Target version: Enhanced v1.5.0
ENTD: global entry **404** (battle_entd4, local entry 20) — confirmed by composition matching
File: `entd/battle_entd4_ent.bin` (embedded; swapped only in NG+ by the code mod)

> Implemented via `tools/battle_patch.py araguay`. NG+-only by construction (whole ENTD swapped
> only in NG+). See `011-chapter-2-overview.md`.

## Original Battle

Objective:

```text
Defeat all enemies!  — OR —  Save Chocobo!
(The player chooses: simply clear the pack, or rescue the wounded Chocobo, Boco.)
```

Player deployment:

```text
Up to 4 units, including Ramza.
Rescuable unit: Boco (a wounded Chocobo). If you choose to rescue it, it joins as an ally for
  the fight and its death is a GAME OVER. Protecting it through the battle recruits it after.
```

Original enemy composition (all monsters):

```text
5x Goblin
1x Black Goblin
```

Public walkthrough details:

```text
Recommended level: ~11.
Woods terrain: trees and brush restrict movement and break up sightlines.
Goblins are weak to Ice (an Ice Bow / ice magic is the recommended answer).
If rescuing Boco, the fight becomes an escort: the pack beelines for the wounded Chocobo and
  the player must intercept. Losing Boco ends the run.
```

Design reading:

Araguay is a **monster-pack woodland fight wrapped around a rescue choice**. On its surface it
echoes Siedge Weald (a goblin swarm in the trees, weak to Ice), but the soul of *this* fight is the
choice to save **Boco**. In vanilla, that creates a protect mission. In New Game++, the challenge
must not be "Boco's AI did something stupid." Boco should be party-level and player-controlled; the
enemy pressure should come from the woods, pack routes, and a fast hunter, not from a helpless NPC.

For New Game++ the identity must stay: **a goblin swarm in the woods around a rescue target —
Ice rewards preparation, the trees deny easy kiting, and Boco is a controlled ally the player can
route intelligently, not an AI liability.**

## Local Data Confirmed (entry 404)

```text
slot  cid    name  flags  job             role                       action
s0    0x82   118   0x30   94 Chocobo      Boco — rescuable ally      SCALE -> 100 (party level)
s1    0x82   255   0x20   98 Gobbledeguck Black-Goblin-tier melee    SCALE -> L101
s2    0x82   255   0x20   97 Goblin       swarm body                 SCALE -> L100
s3    0x82   255   0x20   97 Goblin       swarm body                 SCALE -> L100
s4    0x82   255   0x20   97 Goblin       swarm body                 SCALE -> L100
s5    0x82   255   0x20   97 Goblin       swarm body                 SCALE -> L100
s6    0x82   255   0x20   97 Goblin       swarm body                 SCALE -> L100
s7    0x17   23    0x89   (named)         story unit                 LEAVE (lvl 254)
s8    0x34   52    0x49   (named)         story unit                 LEAVE (lvl 254)
```

Monster job IDs: Goblin 97, Gobbledeguck (Black-Goblin tier) 98, Chocobo 94 (shared with Siedge
Weald / Mandalia). All-monster fight — Level + JobLevel are the only levers (no gear, no R-S-M),
exactly like Ch1 Siedge Weald. Boco is distinguished by name_id 118 + flags 0x30 (the goblins are
flags 0x20).

### Boco note (playtest item #1) — RESOLVED 2026-06-27

**Playtest confirmed the bug.** Player report: "Boco still comes LV10... I'm LV65 so the Goblins
hit-kill Boco", which made the optional **"Save Chocobo!"** path impossible (he was gibbed before the
player could intercept). The mandatory **"Defeat all enemies!"** path was unaffected.

**Fix applied:** Boco's level byte (s0, offset 0x03) set from 10 to **100 (= party level)** in the
modded ENTD, the same dynamic-level lever the goblins use (100 = party, 101 = party+1). Boco now
matches the party and the swarm exactly as he did in vanilla, where he sat at roughly goblin level.
NG+-only by construction (whole-file swap). Only the level byte changed; his job (94 Chocobo), flags
(0x30), name_id, and ability bytes are untouched, so his team and Game-Over scripting are unaffected.

**Why not the runtime guest-scaler:** Boco's charId is **0x82**, a *generic* monster id shared with
all the goblins, and his job (94) is not equal to his charId, so the `ScaleGuestsAlways` `job == charId`
guard in Program.cs can never target him without also hitting the goblins. A monster guest like Boco
must be scaled by a **direct ENTD level edit**, not the runtime charId scaler.

## Enemy Pack Escalation (Chapter 2 redesign)

```text
VANILLA SPIRIT: rescue Boco in a goblin-infested wood; trees break clean movement and Ice is the
  clean answer to the pack.
CHAPTER-2 UPGRADE: keep the all-monster identity, but make the pack less slow and less easy to
  wall off: 4 Goblins, 2 Black Goblins, and 1 Red Panther.
WHY: the second Black Goblin gives the pack a durable center, while exactly one Red Panther creates
  a fast flank/poison threat. This pressures route control without making Boco's AI the test.
WHAT IS NOT CHANGED: Goblins remain the majority, Ice remains rewarded, monsters still carry no
  equipment, and this is still a wild pack rather than a designed human squad.
```

Chapter 2 requirements applied:

```text
- No human enemies, so equipment/R/S/M rules do not apply here.
- Every active monster is tuned through Level, JobLevel, Brave/Faith where relevant, and placement.
- Red Panther count is capped at one; two were rejected as too much fast poison pressure.
- No hard-lock status is added.
```

## Boss rare loot

```text
None. Not a boss battle — no rare item (per the Chapter 2 overview). Monsters carry no gear.
```

## Guest handling

```text
Boco is an active rescue ally. In NG+ he must be party-level and player-controlled. His death can
remain the rescue-route fail condition, but the loss should come from the player ignoring the board
or misrouting him, not from low level or uncontrolled AI.

Current v1 already fixes Boco's level to 100. The v2 implementation pass must also verify/apply
player control for Boco without broad charId rules, because his generic monster id overlaps the
enemy monster ids.
```


Fixed encounter Brave/Faith targets:

| Unit | Br/Fa | Rationale |
|------|-------|-----------|
| Boco | `72/40` | Controlled monster guest; enough Brave to act aggressively, low Faith because chocobo value is physical/support, not magic scaling. |

## Proposed Composition (New Game++ Araguay v2)

Use seven monsters: 4 Goblins, 2 Black Goblins, 1 Red Panther. The fight remains a goblin rescue,
but the pack now has a durable center and a single fast hunter.

| Slot | Monster | Level | Br/Fa | Purpose |
| ------ | --------- | ------- | --- | --------- |
| n | Goblin | `100` | `78/35` | Basic swarm body; Ice-weak teaching target. |
| n | Goblin | `100` | `78/35` | Swarm body; pressures the front. |
| n | Goblin | `100` | `78/35` | Swarm body; flanks toward Boco. |
| n | Goblin | `100` | `78/35` | Swarm body; second flank. |
| n | Black Goblin | `101` | `78/35` | Tougher goblin; the durable melee of the pack. |
| n | Black Goblin | `102` | `78/35` | Second durable body; keeps the center from folding instantly. |
| n | Red Panther (NEW) | `101` | `78/35` | Fast poison beast; threatens flanks and retreat lanes. |

Reasoning:

The faithful move for a monster fight is to **scale the pack logic, not turn it into a human
tactics squad**. The v2 pack keeps Goblins as the majority, preserves Ice counterplay, and adds
only two pressure upgrades: one additional Black-Goblin-tier body and one Red Panther. Boco is a
controlled ally, so the enemy plan must challenge routing and interception rather than punish
guest AI. If the player declines the rescue, this is a tougher monster swarm; if they accept, Boco
becomes a controllable piece in the route-control problem.

## Monster Tuning Notes

```text
Set JobLevel 8 on all monsters; keep monster-typical high Brave (aggressive, presses routes).
Goblins keep Ice weakness — a prepared, ice-equipped party is rewarded exactly as the original.
Red Panther keeps Poison on hit + high Move/Jump; position it with a clear lane toward the
  player/Boco side, but not an unavoidable turn-1 kill line.
Second Black Goblin should be the central bodyguard, not a second flanker.
Keep the pack SPREAD across the tree line so the player cannot AoE it all at once and must
  fight through the woods while routing Boco deliberately.
```

## Positioning Plan

```text
The goblin pack starts spread across the far side of the woods, between the player and the
  natural approach, so they funnel through the trees toward Boco.
The two Black Goblins anchor separate tree gaps, creating a center that cannot be erased by one
  action.
The Red Panther starts on a flank with an open movement lane toward the player/Boco side — the
  first threat to intercept, not an automatic loss.
Preserve Boco's start position and the player deployment zone unless playtest proves Boco can be
  hit before any player-controlled answer.
```

If the player rescues Boco, every approach lane should feel like a routing choice; if not, it's a
harder but still readable swarm. The woods plus a spread pack keep the player from trivially kiting.

## Simulation Plan and Results

Simulation artifact:

```text
tmp/fft-level-design-013-araguay-woods/
```

Model scope:

```text
First four rounds only; compares monster action economy and weighted pack pressure. It checks the
guest-control rule explicitly: a candidate that leaves Boco AI-framed fails regardless of pressure.
```

Iteration results:

| Candidate | Monsters | Enemy actions | Action ratio | Pressure | Delta vs v1 | Result |
|-----------|----------|---------------|--------------|----------|-------------|--------|
| v1 current: 5 Goblin, 1 Black Goblin | 6 | 22.6 | 1.13 | 38.0 | 0.0% | Baseline |
| Add Red Panther but leave Boco AI-framed | 7 | 27.4 | 1.37 | 49.5 | +30.3% | Rejected: guest-AI framing |
| 4 Goblin, 1 Black Goblin, 2 Red Panthers | 7 | 28.4 | 1.42 | 54.9 | +44.5% | Rejected: too much poison/flank |
| 4 Goblin, 2 Black Goblin, 1 Red Panther | 7 | 27.2 | 1.36 | 51.0 | +34.2% | Accepted |

Decision:

```text
Use 4 Goblins, 2 Black Goblins, and 1 Red Panther. Boco must be party-level and player-controlled.
The fight tests route control and Ice preparation, not guest AI.
```

## Current Implementation (v1, entry 404 — superseded by v2 design)

Applied with `python tools/battle_patch.py araguay`; diff contained to local entry 20 (global 404),
12 bytes. Black-Goblin tier (s1) → L101; five Goblins (s2–s6) → L100; JobLevel 8 on all six.
Story units (s7/s8) untouched.

**Boco level fix (2026-06-27):** Boco (s0) level byte set 10 -> 100 (party level) via a direct 1-byte
ENTD edit straight into the tracked `.bin` (battle_patch.py is no longer present locally; the embedded
`.bin` is now the source of truth). Verified surgical (only offset 0x03 changed) and confirmed in the
deployed DLL.

This implementation remains the shipped v1 data. The v2 redesign above is **documentation only** in
this pass; it requires a later ENTD implementation pass to add the second Black Goblin, add the Red
Panther, verify/apply Boco player control, and keep all changes contained to entry 404.

## Future Implementation Checklist (v2)

- [x] Identify Araguay ENTD entry (404) on Windows data; fill "Local Data Confirmed".
- [x] Dump original entry; verify 5 Goblin + 1 Black-Goblin tier + Boco + story slots.
- [x] Confirm Goblin / Black-Goblin / Chocobo monster job IDs.
- [ ] Convert one Goblin into a second Black-Goblin-tier body or add the second Black Goblin in a
  verified central slot.
- [ ] Add one Red Panther in a verified flank slot; do not add a second Panther.
- [ ] Set levels: Goblins `100`, first Black Goblin `101`, second Black Goblin `102`,
  Red Panther `101`, Boco `100`.
- [ ] Set JobLevel `8` on all active monsters; no equipment.
- [ ] Verify/apply Boco player control in NG+ without broad monster-charId rules.
- [ ] Patch the embedded ENTD in a later implementation pass; no binary/data change in this doc pass.
- [ ] Re-dump and diff; confirm changes are contained to entry 404 plus deliberate Boco-control bytes.
- [x] Resolve the Boco-level question: playtest confirmed LV10 Boco was unviable; fixed to party level (100).
- [ ] Re-playtest the rescue path from a NG+ save to confirm controlled, party-level Boco can be routed
  safely with good play.

## Test Questions

- With the rescue chosen, does controlled Boco create a routing decision rather than an AI survival
  check?
- Does the Red Panther create a real flank/poison problem without causing an instant Game Over?
- Do two Black Goblins make the center sturdy without turning the fight into cleanup?
- Without the rescue, is it a fair, slightly-tougher swarm — not trivial, not a wall?
- Is the Ice-weakness lesson still rewarded at scale (does a prepared party clear faster)?
- Do the woods meaningfully restrict the player, keeping them from kiting the whole pack?
- Does it still read as a wild goblin ambush in the woods, not a designed squad?
- Is it a reasonable Chapter 2 rescue-route fight — harder than Ch1 monster fights, but not a spike?

## Sources

- Game8, "Araguay Woods Walkthrough (Battle 12)": roster (5 Goblin, 1 Black Goblin), objective
  "Defeat all enemies! / Save Chocobo!", deploy 4, recommended level ~11, woods terrain, Goblin
  Ice weakness, Boco rescue = escort with Game-Over-on-death and post-battle recruitment.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553173
- Final Fantasy Wiki, "Araguay Woods" / "Boco": story context (the wounded chocobo rescue).
  https://finalfantasy.fandom.com/wiki/Boco_(Tactics)
- Local: `docs/battles/011-chapter-2-overview.md` (enemy-party escalation rule), `003-siedge-weald.md`
  (Chapter 1 monster-pack handling), `002-mandalia-plain.md` (Red Panther tuning).
</content>
