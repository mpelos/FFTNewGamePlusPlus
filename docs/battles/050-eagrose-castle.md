# 050 - Eagrose Castle (Igros Castle)

Status: 🧪 v3 implemented and deployed — in-game playtest pending
Chapter: 4 — "In the Name of Love"
Battle order: Battle 45 (after the Limberry chain)
Target version: Enhanced v1.5.0
ENTD: global entry **459** (local 75, entd4)
File: `battle_entd4_ent.bin`

> **NG++ rewards applied (2026-06-27):** Maximillian + Grand Helm + Venetian Shield through guaranteed
> Spoils of War (`0x1e`), NG+ only, within the 3-item cap, no stealing required. Canonical map:
> `chapter-4-rewards-implementation.md`.

> **V3 implementation (2026-07-11):** entry 459 patched in the embedded ENTD and deployed through a
> successful Release build. All 358 Chapter-4 validation checks pass. `event436.e` was not modified;
> its SHA-256 remains `132FE1DB670F85079BF31BF881B5B48BD79CC1540BC92B564346CC0436998318`.

> **Dragoon revision (2026-07-11):** s5/s6 converted from Ninja-bucket Knights to true Dragoons with
> Dragoon bucket JL8, no secondary, Reflexes, Doublehand, Ignore Elevation and Javelin "II". The Release
> build was deployed to Reloaded-II and the installed DLL was read back successfully. Sprite-sheet count
> rises from 5 to 6; direct playtest must confirm both Dragoon sprites and event choreography.

## Current Implementation / Data Reality

```text
DATA REALITY (verified from current embedded entd4 dump, entry 459):
  slot 0 = allied story guest record
           name/job 8, level 103, JobLevel 8, Ragnarok, Venetian Shield, Grand Helm,
           Lordly Robe, and Bracers.
           Must be player-controlled in NG++ if active. Do not use guest AI as difficulty.

  slot 1 = Dycedarg
           name/job 9, level 103, JobLevel 8, complete setup:
           secondary 71, reaction 450, support 479, movement 486.
           gear includes Defender (33), Venetian Shield (142), Grand Helm (156), Maximillian (185),
           and Bracers (218).
           Spoils payload = 0xB9 (Maximillian).

  slots 2-4 = three Knight stair-wall bodies (two Martial Artists + one Samurai).
  slots 5-6 = two Dragoon stair-wall bodies with Javelin "II" and Doublehand.
              slot 2 spoils payload = 0x9C (Grand Helm).
              slot 3 spoils payload = 0x8E (Venetian Shield).

  slot 7 = Adramelk / Adrammelech Lucavi transform
           job 69, level 105, no normal equipment, secondary 120.

  slots 8,9 = job-8 scripting placeholders, level 254, no normal battle role; preserve untouched.

Current v1 implementation:
  Guest slot = 103 by direct ENTD scaling.
  Dycedarg = 104.
  Five Knight bodies = 103 with complete gear/R/S/M.
  Adramelk = 105.
  Two-phase transform and buried map treasure are preserved.
```

Historical v2 baseline: keep the two-phase brother fight, control the active guest, cap effective break
sources, and preserve a sequential transform into a spaceable Lucavi AoE puzzle.

V3 planning is complete. This pass locks s0 Zalbaag, s1 Dycedarg, Adrammelech's level, and the
complete levels, Brave/Faith targets, builds, and event-script positions for all five stair-wall bodies.

> V3 is implemented in the ENTD patch path and deployed to Reloaded-II. Runtime transform behavior,
> secondary-skill availability, and battle feel remain pending direct in-game validation.

## V3 Locked Decisions

```text
LEVELS:
  s0 Zalbaag: 103.
  s1 Dycedarg: 103.
  s2 Knight Martial Artist: 100.
  s3 Knight Martial Artist: 100.
  s4 Knight Samurai: 101.
  s5 Dragoon: 101.
  s6 Dragoon: 100.
  s7 Adrammelech: 105.

s0 ZALBAAG — complete equipment locked:
  Right hand: Ragnarok
  Left hand: Venetian Shield
  Head: Grand Helm
  Body: Lordly Robe
  Accessory: Bracers

s1 DYCEDARG — complete equipment locked:
  Right hand: Defender
  Left hand: Venetian Shield
  Head: Grand Helm
  Body: Maximillian
  Accessory: Bracers

BRAVE/FAITH:
  s0 Zalbaag: 70/65.
  s1 Dycedarg: 88/60.
  s2: 88/42.  s3: 86/44.  s4: 88/58.  s5: 88/52.  s6: 86/56.

PRESERVE:
  Zalbaag and Dycedarg keep their existing ability setup except for the equipment changes above.
  The reward ledger remains Maximillian + Grand Helm + Venetian Shield.
```

## Design Goal

```text
Make Eagrose the second major Chapter 4 Lucavi spike: Phase 1 is a controlled high-stair physical wall
around Dycedarg, built from Martial Arts/Iaido Knights and Javelin "II" Dragoons; Phase 2 is Adramelk's
spread-or-die summon pressure. The player must read and crack three distinct physical styles, then
spread and burst the Lucavi. The fight must never become an unreadable damage pile-up, an AI-guest
failure, or a non-spaceable AoE/status lock.
```

Slot 0 is an active-guest concern. If present in battle, this unit must be player-controlled in NG++.

## Original Battle

Objective:

```text
Defeat Dycedarg, Ramza's elder brother!   (two-phase: Dycedarg -> Adramelk)
```

Player deployment:

```text
Up to 5 units, including Ramza, plus an allied story guest record in local data.
```

Original enemy composition:

```text
PHASE 1:
  Dycedarg + 5x Knight on the upper stairs.

PHASE 2:
  Dycedarg transforms into Adramelk / Adrammelech, a Lucavi with summon-AoE and status pressure.
```

Public walkthrough details:

```text
Recommended level: ~60. Difficulty: 4/5 stars. Multi-level Eagrose keep with upper stairs.
Phase 1 asks the player to crack a Knight wall from below. Phase 2 punishes grouped units with large
summon-AoE and resistable status such as Confuse/Stone. Buried map treasure includes Blood Sword,
Healing Staff, Featherweave Cloak, and Thief's Cap.
```

Design reading:

Eagrose is **the brother fight**. Its shape is not just "another Lucavi": the human phase forces Ramza
through the institutional Beoulve wall first, then reveals the monster underneath. That means the two
demands must remain sequential and readable. Three v3 bodies remain main-job Knights and retain Arts
of War as their primary command. The former Ninja-bucket Knights become true Dragoons with Jump primary,
no secondary, Doublehand, and Javelin "II". If Adramelk's AoE is non-spaceable, the second phase
becomes a wipe check. If the guest is
AI-controlled, the fight asks the player to babysit a bad decision engine.

For New Game++ the identity must stay: **controlled guest, Knight/Dragoon physical wall, then space
against the Lucavi.**

## Local Data Confirmed / Data Still Needed

```text
CONFIRMED:
- Entry 459 is Eagrose Castle / Igros Castle.
- Slot 0 is an allied guest/story unit at level 103 with full gear.
- Slot 1 is Dycedarg at level 104 with complete setup.
- Slots 2-6 are five level-103 Knight bodies with complete gear/R/S/M.
- Slot 7 is Adramelk/Adrammelech at level 105.
- Slots 8/9 are job-8 placeholders and should be preserved.
- Rewards are already mapped to Maximillian + Grand Helm + Venetian Shield guaranteed spoils.

STILL NEEDED FOR V3 IMPLEMENTATION:
- Verify slot 0 is active and player-controllable; if not, set the guest-control bit.
- Verify the transform from Dycedarg to Adramelk fires correctly.
- Confirm Adramelk's AoE/status cadence is telegraphed, spaceable, resistable, and non-locking.
- Confirm all three spoils land in the first three awarded `0x1e` items.
- Preserve buried map treasure as vanilla map loot.
```

## Enemy Party Escalation (Chapter 4 rule)

```text
Headline engine: two-phase brother-to-Lucavi fight.
Phase 1 support structure:
  - Dycedarg anchors the upper stairs.
  - s2/s3 are Monk-bucket Knight Martial Artists with shielded counter-pressure.
  - s4 is a Samurai-bucket Knight whose Doublehand/Iaido build is the central melee threat.
  - s5/s6 are true Dragoons with Javelin "II", Doublehand, no secondary, and vertical freedom.
  - s2-s4 retain primary Arts of War because their main job is Knight. The Dragoons use Jump primary.

Phase 2 support structure:
  - Adramelk is the single Lucavi engine.
  - Summon-AoE punishes clumping.
  - Confuse/Stone-style status is resistable and non-locking.

WHY: the original battle is already a strong puzzle: elevation wall -> demon reveal. Chapter 4 v2 makes
both halves matter while keeping them sequential and answerable.
```

## Sanctioned Exceptions

```text
KNIGHT JOB-BUCKET CASTES:
  s2/s3 remain main-job Knights with Monk buckets and s4 remains a main-job Knight with Samurai bucket.
  Arts of War is primary for those three. s5/s6 are true Dragoons with Jump primary and no secondary.

THREE ARTS-OF-WAR SOURCES:
  Eagrose retains three main-job Knights and therefore three visible Arts-of-War sources. The pressure
  is explicit and visible;
  Safeguard, disarm, status, range, and focusing individual Knights remain the intended answers.

TWO-PHASE TRANSFORM:
  Preserved as the emotional and tactical beat. Phase pressure is sequential, not simultaneous.

LUCAVI SUMMON-AoE:
  Allowed as Adramelk's identity. Guardrail: telegraphed, spaceable, and survivable through spread,
  Shell/mitigation, burst, and boss focus.

LUCAVI STATUS:
  Confuse/Stone-style effects may exist as support pressure, but must be resistable and non-locking.

ACTIVE GUEST:
  Slot 0 must be controllable if active. Guest AI is not a skill check.
```

## Rare/reward handling

```text
Guaranteed spoils for entry 459: MAXIMILLIAN + GRAND HELM + VENETIAN SHIELD.
These are delivered by the Spoils of War reward channel; the player must never be required to Steal.

COMBAT ROLE:
  - V3 Zalbaag visibly carries Ragnarok, Venetian Shield, Grand Helm, Lordly Robe, and Bracers.
  - V3 Dycedarg visibly carries Defender, Venetian Shield, Grand Helm, Maximillian, and Bracers.
  - The armor set is still guaranteed through spoils, not dependent on stealing from him.
  - These active equipment decisions do not change the guaranteed-spoils ledger.

PRESERVE:
  - Buried map treasure remains vanilla map loot.
  - No Excalibur. Excalibur stays Orlandeau's.
```

## Proposed Composition (New Game++ Eagrose Castle v3)

Keep the local two-phase roster. Named-unit builds and all five stair-wall levels, Brave/Faith targets,
jobs/buckets, abilities, equipment, and final combat positions below are locked.

### Phase 1 - Dycedarg + High-Stair Wall

| Slot | Role | Unit type | Level | Br/Fa | Purpose |
| ------ | ------ | ----------- | ------- | --- | --------- |
| s0 | Allied guest/story unit | Zalbaag | `103` | `70/65` | Player-controlled; Ragnarok/Lordly Robe build locked. |
| s1 | Boss / phase trigger | Dycedarg | `103` | `88/60` | Defender/Maximillian build locked; defeat triggers Lucavi phase. |
| s2 | Knight Martial Artist / reward payload | Knight body; Monk bucket Lv8 | `100` | `88/42` | Shielded Counter bruiser at final event tile `(8,4)`; Grand Helm spoil remains current baseline. |
| s3 | Knight Martial Artist / reward payload | Knight body; Monk bucket Lv8 | `100` | `86/44` | Shielded Counter bruiser at final event tile `(9,5)`; Venetian Shield spoil remains current baseline. |
| s4 | Knight Samurai | Knight body; Samurai bucket Lv8 | `101` | `88/58` | Doublehand/Iaido central threat at final event tile `(7,7)`. |
| s5 | Dragoon | Dragoon bucket Lv8 | `101` | `88/52` | Doublehand Javelin "II" flank threat at final event tile `(1,5)`. |
| s6 | Dragoon | Dragoon bucket Lv8 | `100` | `86/56` | Doublehand Javelin "II" flank threat at final event tile `(1,3)`. |

### Phase 2 - Adramelk / Adrammelech

| Slot | Role | Unit type | Level | Br/Fa | Purpose |
| ------ | ------ | ----------- | ------- | --- | --------- |
| s7 | Lucavi boss | Adramelk / Adrammelech | `105` | `92/86` | Sequential transform spike; spaceable summon-AoE + resistable status. |

Script placeholders to preserve:

| Slot | Record | Handling |
|------|--------|----------|
| s8 | job-8 placeholder | Preserve untouched unless implementation proves active. |
| s9 | job-8 placeholder | Preserve untouched unless implementation proves active. |

Reasoning:

The v3 design is a **Knight/Dragoon physical wall followed by the Lucavi duel**. The human phase uses
two shielded Martial Artists, one Doublehand Samurai, and two Javelin "II" Dragoons. The three Knights
retain primary Arts of War; the Dragoons use Jump primary and no secondary. The transform remains
sequential, the guest remains controlled, and the
reward ledger is the full armor/shield set rather than the old single-Grand-Helm plan.

Rejected variants:

```text
- Five identical Knight builds: rejected in favor of Martial Arts/Iaido Knights plus Dragoons.
- AI guest hostage: guest AI becomes a failure condition.
- Unavoidable summon lock: Phase 2 loses spacing counterplay.
- Extra caster support: adds a second engine to an already two-phase fight.
- Single-phase Dycedarg: removes the Lucavi reveal.
- One-rare old ledger: contradicts Maximillian + Grand Helm + Venetian Shield reward map.
- Steal-required armor set: contradicts guaranteed spoils.
- Overlevelled brother spike: replaces puzzle pressure with raw stats.
- Simultaneous pressure pile-up: makes phase 1 and phase 2 feel like one overloaded fight.
```

## Builds (v3 — named units and Knight kits locked)

```text
Zalbaag — guest ally slot 0:
  - Level: 103.
  - Right hand: Ragnarok.
  - Left hand: Venetian Shield.
  - Head: Grand Helm.
  - Body: Lordly Robe.
  - Accessory: Bracers.
  - Must be player-controlled if active.

Dycedarg:
  - Level: 103.
  - Right hand: Defender.
  - Left hand: Venetian Shield.
  - Head: Grand Helm.
  - Body: Maximillian.
  - Accessory: Bracers.
  - Preserve the transform trigger.

Knights s2-s3 — Knight Martial Artists:
  - Levels: s2 100; s3 100.
  - Brave/Faith: s2 88/42; s3 86/44.
  - Main job/body: Knight.
  - Primary: Arts of War.
  - Job bucket: Monk; JobLevel: 8.
  - Secondary: Martial Arts.
  - Reaction: Counter.
  - Support: Attack Boost.
  - Movement: Movement +3.
  - Right hand: Runeblade.
  - Left hand: Crystal Shield.
  - Head: Crystal Helm.
  - Body: Crystal Mail.
  - Accessory: Bracers.

Knight s4 — Knight Samurai:
  - Level: 101.
  - Brave/Faith: 88/58.
  - Main job/body: Knight.
  - Primary: Arts of War.
  - Job bucket: Samurai; JobLevel: 8.
  - Secondary: Iaido.
  - Reaction: Shirahadori.
  - Support: Doublehand.
  - Movement: Movement +3.
  - Right hand: Runeblade.
  - Left hand: None.
  - Head: Crystal Helm.
  - Body: Crystal Mail.
  - Accessory: Magepower Glove.

Dragoons s5-s6:
  - Levels: s5 101; s6 100.
  - Brave/Faith: s5 88/52; s6 86/56.
  - Main job/body: Dragoon.
  - Job bucket: Dragoon; JobLevel: 8.
  - Primary: Jump.
  - Secondary: None.
  - Reaction: Reflexes.
  - Support: Doublehand.
  - Movement: Ignore Elevation.
  - Right hand: Javelin "II".
  - Left hand: None.
  - Head: Crystal Helm.
  - Body: Crystal Mail.
  - Accessory: Hermes Shoes.

Adramelk / Adrammelech:
  - Level 105 Lucavi transform, no normal equipment.
  - One summon-AoE engine, telegraphed and spaceable.
  - Status pressure is support only: resistable, cleansable, non-locking.
```

## Positioning Plan

```text
Phase 1: Dycedarg and the stair wall hold the upper level. The event script `event436.e` overrides the
provisional ENTD coordinates. Final combat tiles are s2 `(8,4)`, s3 `(9,5)`, s4 `(7,7)`, s5 `(1,5)`,
and s6 `(1,3)`. The two Martial Artists hold the central approach, the Samurai supplies the central
Doublehand/Iaido threat, and the two Dragoons exploit the left side and elevation. Slot 0
guest starts controllable and must not be exposed to unavoidable failure.

Phase 2: After the transform, Adramelk's threat becomes spacing. The player should have room to spread,
re-buff, and focus the Lucavi instead of being pinned in the stair-wall geometry by leftover enemies.
```

The keep should say: "your brother hides behind the house's steel; break through the stair wall, then
scatter when the demon rises."

## Historical v2 Simulation / v3 Test Plan

The table below is historical v2 analysis. It does not validate the new v3 named builds or the locked
Martial Artist/Samurai/Dragoon redesign. No new simulation is requested; direct in-game validation
will follow implementation.

Simulation artifact:

```text
tmp/fft-level-design-050-eagrose-castle/
  assumptions.md
  simulate.py
  iteration-results.json
  iteration-results.md
```

Model scope:

```text
Coarse deterministic two-phase stair-wall and Lucavi-AoE model.
It scores pressure, phase clarity, break fairness, AoE fairness, answerability, guest safety, reward
correctness, and scripting fidelity. It does not simulate exact FFT formulas.
```

Result summary:

| Candidate | Pressure | Phase clarity | Break fair | AoE fair | Answer | Guest | Reward | Scripting | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| v2 hard-capped brother duel | 338 | 94 | 92 | 88 | 96 | 100 | 100 | 100 | **Accepted** |
| five-rend stair wall | 395 | 94 | 38 | 88 | 73 | 100 | 100 | 100 | Rejected: too many breaks |
| AI guest hostage | 338 | 94 | 92 | 88 | 96 | 30 | 100 | 100 | Rejected: guest AI |
| unavoidable summon lock | 398 | 94 | 92 | 22 | 47 | 100 | 100 | 100 | Rejected: AoE/status lock |
| extra caster support | 368 | 74 | 92 | 88 | 84 | 100 | 100 | 100 | Rejected: second engine |
| single-phase Dycedarg | 364 | 45 | 92 | 88 | 80 | 100 | 100 | 55 | Rejected: breaks transform |
| one-rare old ledger | 338 | 94 | 92 | 88 | 96 | 100 | 75 | 100 | Rejected: reward ledger |
| steal-required armor set | 338 | 94 | 80 | 88 | 96 | 100 | 35 | 100 | Rejected: reward policy |
| overlevelled brother spike | 366 | 94 | 92 | 76 | 86 | 100 | 100 | 100 | Rejected: raw levels |
| no-break stair wall | 282 | 94 | 78 | 88 | 96 | 100 | 100 | 100 | Rejected: loses gear lesson |
| simultaneous pressure pile-up | 420 | 94 | 92 | 88 | 96 | 100 | 100 | 100 | Rejected: phase pile-up |

Historical iteration decision (superseded for the v3 Knight kits):

```text
ACCEPT v2 hard-capped brother duel as the historical baseline.
Iteration 2 treats the fight as sequential phases. The stair wall is allowed only with two effective
breakers, slot 0 must be controllable if active, and Phase 2 must remain spaceable.
V3 intentionally uses three main-job Knights retaining primary Arts of War plus two true Dragoons.
This historical simulation is retained only for phase/guest/AoE context and does not validate the
three-source Rend pressure or Javelin "II" Dragoon damage.
```

## Implementation Checklist

- [x] Re-dump entry 459 and verify slot order, rewards, and placeholder bytes.
- [x] Set slot 0 player-control bit (`0x18 = 0x8C`); verify actual control in game.
- [ ] Preserve win condition and Dycedarg -> Adramelk transform.
- [x] Set Zalbaag and Dycedarg to `103`; s2/s3/s6 to `100`; s4/s5 to `101`; Adrammelech to `105`.
- [x] Set Br/Fa: s0 `70/65`, s1 `88/60`, s2 `88/42`, s3 `86/44`, s4 `88/58`,
      s5 `88/52`, and s6 `86/56`.
- [x] Equip Zalbaag with Ragnarok, Venetian Shield, Grand Helm, Lordly Robe, and Bracers.
- [x] Equip Dycedarg with Defender, Venetian Shield, Grand Helm, Maximillian, and Bracers.
- [x] Define s2/s3 Monk-bucket Knight Martial Artists and s4 Samurai-bucket Knight.
- [x] Convert s5/s6 to Dragoon bucket Lv8 with no secondary, Reflexes, Doublehand, Ignore Elevation,
      and Javelin "II".
- [x] Preserve unmodified `event436.e` final combat positions: s2 `(8,4)`, s3 `(9,5)`, s4 `(7,7)`,
      s5 `(1,5)`, s6 `(1,3)`.
- [ ] Keep Phase 2 AoE/status telegraphed, spaceable, resistable, and non-locking.
- [x] Verify spoils: Maximillian + Grand Helm + Venetian Shield, guaranteed and within the 3-item cap.
- [x] Preserve buried map treasure by leaving the event/map layers untouched.

## Test Questions

- Is slot 0 player-controlled if active, and does the battle avoid guest-AI failure?
- Does Zalbaag appear at level 103 with Ragnarok, Venetian Shield, Grand Helm, Lordly Robe, and Bracers?
- Does Dycedarg appear at level 103 with Defender, Venetian Shield, Grand Helm, Maximillian, and Bracers?
- Do s5/s6 appear as Dragoons with Dragoon bucket Lv8, no secondary, and the exact Javelin "II" build?
- Do both Dragoon sprites load correctly without corrupting named-unit or Lucavi sprites?
- Does the three-source Arts of War wall remain answerable through Safeguard, disarm, status, range,
  or focus fire?
- Does each Knight begin combat on the event-script tile documented above, especially s2 after its
  scripted walk from `(8,8)` to `(8,4)`?
- Does the transform fire cleanly and make Phase 2 sequential rather than simultaneous with Phase 1?
- Is Adramelk's summon/status pressure spaceable and resistable?
- Do Maximillian + Grand Helm + Venetian Shield appear as guaranteed spoils?

## Sources

- Game8, "Eagrose Castle Walkthrough (Battle 45)": public roster, two-phase boss shape, stair terrain,
  Adramelk summon/status pressure, and buried treasure.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553205
- Final Fantasy Wiki, "Dycedarg Beoulve" / "Adramelk": story/terrain context.
  https://finalfantasy.fandom.com/wiki/Dycedarg_Beoulve
- Local: `037-chapter-4-overview.md`, `034-riovanes-castle-keep.md`,
  `049-limberry-undercroft.md`, `chapter-4-rewards-implementation.md`,
  `spoils-of-war-reward-system.md`.
