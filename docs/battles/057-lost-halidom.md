# 057 - Lost Halidom (Endgame Gauntlet 4/5)

Status: v3 implemented/deployed - direct playtest pending
Chapter: 4 - "In the Name of Love"
Battle order: Battle 52 (ENDGAME GAUNTLET 4 of 5 - no resupply across 054 -> 055 -> 056 -> 057 -> 058)
Target version: Enhanced v1.5.0
ENTD: `entd4` global entry `439`
Local slot: `055`
Simulation artifact: `tmp/fft-level-design-057-lost-halidom/`

> V3 docs-only revision: preserve entry 439, positions and win-on-Barich behavior. Copy Barich's first
> battle build, replace the Chemist with a Monk, replace Hydra with King Behemoth, and lower every
> monster into the 102-103 band.

> **V3 implementation (2026-07-11):** entry 439 patched in the embedded ENTD and deployed through a
> successful Release build. The installed DLL resource matches the source binary byte-for-byte; jobs,
> levels, complete human kits, positions, monster shells and zero-spoil bytes were mechanically verified.

## V3 Locked Decisions

```text
s0 BARICH - copy Beddha Sandwaste s0:
  Level 104; JobLevel 8; Brave/Faith 84/55.
  Machinist primary; secondary None; Reflexes; Defense Boost; Jump +3.
  Stoneshooter / two-hand marker / Thief's Cap / Black Garb / Featherweave Cloak.

s1 MONK - replaces Chemist:
  Level 102; main job Monk; Mime bucket JL8; Brave/Faith 88/38.
  Primary Martial Arts; secondary Items; Counter; Dual Wield; Movement +3.
  Both hands empty / Barrette / Power Garb / Bracers.

s2 KING BEHEMOTH - replaces Hydra: level 103.
s3 GREATER HYDRA: level 102.
s4 TIAMAT: level 103.
s5 DARK BEHEMOTH: level 102.
All monsters retain Brave/Faith 90/30 and their innate fixed-body kits.

PRESERVE:
  Defeat-Barich objective, all positions and zero special-spoil bytes.
```

## Gate Answers / Constraints

```text
Scope: redesign battle doc 057 only; no game data or code changes.
Allowed changes in design: active enemy kit/level/gear/ability plan, positioning, reward policy, and tests.
Chapter target: Chapter 4 broken-but-readable puzzle; this is the 5-star peak before the finale.
Must preserve: Barich rematch, ranged gunner identity, apex monster pit, holy-ground
  terrain, and "Defeat Barich" objective.
Guests: no active guest. If future testing discovers any active guest/NPC, it must be player-controlled
  in NG+ and never used as a skill check.
Reward rule: no special spoils inside 054-058. Materia Blade is not awarded here; Stoneshooter is an
  intentional active-equipment Steal exposure copied from Barich's first battle.
```

## Original Battle

Objective:

```text
Defeat Barich!
```

Player deployment:

```text
Up to 5 units, including Ramza. No outfitter: this is the fourth fight after the point of no return.
```

Original enemy composition, corrected by local data:

```text
Barich Fendsor    (Machinist/gunner control boss)
1x Chemist         (sustain)
4x apex monsters   (local jobs 139/140/141/135; ENDGAME-BLOCKER identifies these as dragons)
```

Public guides often describe the monster pit as Hydras/Tiamat/Dark Behemoth. The local ENTD entry is
authoritative for implementation: Barich + Chemist + four monster jobs. The preserved feeling is still
the same: a brutal breath/monster pit under Barich's Disable/Immobilize control.

## Local Data Confirmed

Dump command:

```bash
python tools/entd_tool.py dump-entry --input src/fftivc.battles.ngplus/entd/battle_entd4_ent.bin --entry 439 --include-empty
```

Confirmed active data:

| Slot | Status | Job | Level | JL | Secondary | Reaction | Support | Move | Equipment ids | Notes |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| 0 | Active boss | 43 | 105 | 8 | 0 | 442 | 472 | 493 | 168,206,234,76,254 | Barich. Verify item `76`; swap if it duplicates the 042 gun rewards. |
| 1 | Active | 75 | 104 | 8 | 254 | 510 | 510 | 510 | 254,254,254,75,254 | Chemist; needs complete R/S/M kit in v2. |
| 2 | Active monster | 139 | 105 | 8 | 0 | 510 | 510 | 510 | 0,0,0,0,0 | Apex monster / dragon caste. |
| 3 | Active monster | 140 | 105 | 8 | 0 | 510 | 510 | 510 | 0,0,0,0,0 | Apex monster / dragon caste. |
| 4 | Active monster | 141 | 105 | 8 | 0 | 510 | 510 | 510 | 0,0,0,0,0 | Apex monster / dragon caste. |
| 5 | Active monster | 135 | 105 | 8 | 0 | 510 | 510 | 510 | 0,0,0,0,0 | Apex monster / dragon caste. |

Data implications:

```text
- Entry 439 is confirmed moddable through ENTD direct edits.
- The current data already makes this the peak: Barich 105, Chemist 104, four monster bodies at 105.
- Current Chemist R/S/M slots are empty (`510`); v2 must make this an intentional complete Chapter 4 kit.
- Barich currently uses item `76`; verify against the item table. If it is Blaze Gun, Blaster, or another
  reward from 042, replace it with a standard/non-reward gun.
- No Materia Blade, no special relic reward, and no usable gauntlet payout.
```

## Design Goal

Make Lost Halidom the final gauntlet's 5-star tactical peak:

```text
Break through overlapping monster lanes, blunt the apex bodies with resistance or disable effects,
answer Barich's Stoneshooter pressure, and defeat Barich without being baited into a full
monster-pit cleanup.
```

The headline engine is **apex monster pressure under a copied ranged boss**. This is allowed to be the
hardest fight before Ultima, but every pressure point must be visible and answerable.

## Enemy Party Escalation

Accepted redesign: **v3 Behemoth/Hydra apex pit**.

| Slot | Role | Job / Unit | Level | Br/Fa | Purpose |
| ---: | --- | --- | ---: | --- | --- |
| 0 | Boss objective | Barich / Machinist | 104 | `84/55` | Exact first-battle Stoneshooter build; defeat ends fight. |
| 1 | Martial body | Monk, Mime bucket Lv8 | 102 | `88/38` | Items utility plus Counter/Dual Wield martial pressure. |
| 2 | Apex body | King Behemoth, job 134 | 103 | `90/30` | Replaces Hydra at `(7,2)`. |
| 3 | Breath lane | Greater Hydra, job 140 | 102 | `90/30` | Hydra-family lane at `(5,1)`. |
| 4 | Breath lane | Tiamat, job 141 | 103 | `90/30` | Strongest breath lane at `(3,1)`. |
| 5 | Apex body | Dark Behemoth, job 135 | 102 | `90/30` | Behemoth lane at `(1,1)`. |

Why this works:

```text
- Four distinct level-102/103 apex monsters make this the true peak through composition over raw levels.
- Overlapping breath lanes create the 5-star pressure, but elemental resistance/absorb and monster
  disable/break must remain valid answers.
- Barich reproduces his answerable first-battle Stoneshooter package.
- The Monk adds martial pressure, but the player can bypass it by focusing Barich.
- The boss-focus lane is mandatory: defeating Barich must be a real plan before full cleanup.
- No usable reward appears here; Materia Blade stays outside this gauntlet battle.
```

## Builds

### Barich Fendsor - copied Stoneshooter boss

```text
Level: 104
JobLevel: 8
Primary: Machinist
Secondary: None
Reaction: Reflexes
Support: Defense Boost
Movement: Jump +3
Brave/Faith: 84/55
Gear: Stoneshooter / two-hand marker / Thief's Cap / Black Garb / Featherweave Cloak
Reward: none
```

Guardrail: Barich may pressure movement and actions, but he must remain one source of resistable or
cleansable control. No party-wide chain-lock.

### Monk - Mime-bucket martial body

```text
Level: 102
JobLevel: 8
Main job: Monk
Job bucket: Mime, JobLevel 8
Primary: Martial Arts
Secondary: Items
Reaction: Counter
Support: Dual Wield
Movement: Movement +3
Brave/Faith: 88/38
Gear: empty hands / Barrette / Power Garb / Bracers
Reward: none
```

Guardrail: sustain must be raceable. It should force priority decisions, not create a monster revive slog.

### Apex monsters x4

```text
Levels: King Behemoth 103; Greater Hydra 102; Tiamat 103; Dark Behemoth 102
Jobs: 134, 140, 141, 135
Primary: monster breath / apex physical pressure
Gear: none
Reward: none
```

Guardrails:

```text
- Breath pressure must be elemental/resistable or otherwise mitigable.
- Monsters must be disableable, breakable, or bluntable by established player answers.
- Positioning creates overlapping lanes but must not seal Barich behind mandatory cleanup.
```

## Positioning Plan

```text
Use the Lost Halidom as a desecrated holy arena. Put Barich at range with a real but contested lane to
him. Spread the four monsters so their threat lanes overlap across obvious rush paths. Keep the Monk
on the former Chemist tile, where killing it is not mandatory before any boss
pressure is possible.
```

The player read should be: prepare elemental/status answers, disable or blunt one monster lane, push a
route to Barich, and end the control source before the breath pit drains the run.

## Historical v2 Simulation / v3 Test Plan

The simulation below is historical v2 context. It does not validate the lower monster levels, the
King Behemoth substitution, copied Barich build, or new Monk; those require direct playtest.

Artifact:

```text
tmp/fft-level-design-057-lost-halidom/
```

Accepted candidate:

```text
v2 no-reward apex monster pit
Monster pressure: 192
Control risk: 16
Answerability: 100
Focus clarity: 96
Peak identity: 100
Chain tax: 64.2
Reward correctness: 100
Human kit score: 100
```

Iteration notes:

```text
- Current local data has four level-105 monster bodies; this is kept because 057 is the gauntlet's
  5-star peak.
- First pass had enough monster pressure but too little chain-tax separation from 056; v2 requires
  overlapping breath lanes.
- The old lower-level / three-breath plan was rejected as too soft for this slot.
- The peak passes only with all answers present: elemental counterplay, monster disable/break, one Barich
  control source, raceable Chemist, and a boss-focus lane.
- The Materia Blade campaign-reward variant was rejected by the current reward ledger.
- Full-clear requirements, sealed monster walls, unanswerable breath, hard status locks, and overleveling
  were rejected.
```

Residual risks:

```text
- Confirm Barich defeat ends the battle even if monsters remain.
- Confirm monster breath is elemental/resistable and monsters can be disabled or otherwise blunted.
- Confirm Barich control is one answerable source and does not chain-lock the party.
- Test 056 -> 057 -> 058 as a unit; 057 should be the peak but still leave a viable path into the finale.
```

## Rare / Reward Handling

```text
No special NG++ spoil is added inside the final gauntlet.
Materia Blade is not awarded here and is not relocated into this fight.
Barich deliberately copies the first-battle Stoneshooter as active equipment. It is not a spoil payload,
but its Steal/Break exposure is an intentional v3 exception.
No monster or Monk carries a hidden rare payload.
Keep standard/vanilla loot and buried Elixirs only.
```

## Implementation Checklist

- [x] Preserve entry `439` and the "Defeat Barich" objective data.
- [x] Copy first-battle Barich exactly at level `104`.
- [x] Replace Chemist with the locked level-102 Monk/Mime-bucket build.
- [x] Replace Hydra job `139` with King Behemoth job `134`.
- [x] Set monster levels to `103/102/103/102` for s2-s5.
- [ ] Create overlapping breath lanes through placement without sealing Barich behind mandatory cleanup.
- [ ] Ensure monster breath has real elemental/disable/break counterplay.
- [ ] Preserve Barich's copied Stoneshooter/Reflexes/Defense Boost/Jump +3 package.
- [x] Verify the Monk's complete secondary/reaction/support/move and empty hands.
- [x] Equip Barich with Stoneshooter and document its active Steal exposure.
- [x] Add no special spoil or Materia Blade; Stoneshooter exposure is intentional active equipment.
- [x] Re-dump entry `439` after implementation and verify only intended kit/ability/positioning changes.
- [ ] Playtest `056 -> 057 -> 058` as a no-resupply unit.

## Test Questions

- Does this clearly feel like the 5-star peak before the finale?
- Are monster breath lanes scary because they overlap, not because they are unanswerable?
- Can players blunt the monster pit with elemental resist/absorb, Disable, breaks, or equivalent tools?
- Is copied Stoneshooter Barich dangerous but answerable?
- Can the player focus Barich and end the fight without full monster cleanup?
- Are zero special spoils preserved, with Stoneshooter exposure limited to the intended active equipment?
- Does the 102-103 monster band remain a 5-star peak through composition rather than raw levels?

## Sources

- Local: `docs/battles/ENDGAME-BLOCKER.md` for entry mapping and corrected roster.
- Local: `docs/battles/037-chapter-4-overview.md` for Chapter 4 puzzle-party principles and gauntlet curve.
- Local: `docs/battles/chapter-4-rewards-implementation.md` for the no-usable-reward rule in `054-058`.
- Local: `tmp/fft-level-design-057-lost-halidom/` simulation artifact.
- Local dump: `tools/entd_tool.py dump-entry --entry 439`.
- Game8, "Lost Halidom Walkthrough (Battle 52)": original objective and public monster-pit framing.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553228
