# 057 - Lost Halidom (Endgame Gauntlet 4/5)

Status: redesigned (documentation only; not implemented in game data by this task)
Chapter: 4 - "In the Name of Love"
Battle order: Battle 52 (ENDGAME GAUNTLET 4 of 5 - no resupply across 054 -> 055 -> 056 -> 057 -> 058)
Target version: Enhanced v1.5.0
ENTD: `entd4` global entry `439`
Local slot: `055`
Simulation artifact: `tmp/fft-level-design-057-lost-halidom/`

> Docs-only redesign note: this document is the intended NG++ level design. It does not change the
> embedded ENTD, scripts, binaries, or patch code. Implementation must later patch entry `439` and
> preserve the win-on-Barich behavior.

## Gate Answers / Constraints

```text
Scope: redesign battle doc 057 only; no game data or code changes.
Allowed changes in design: active enemy kit/level/gear/ability plan, positioning, reward policy, and tests.
Chapter target: Chapter 4 broken-but-readable puzzle; this is the 5-star peak before the finale.
Must preserve: Barich rematch, control boss identity, apex monster pit, Chemist sustain, holy-ground
  terrain, and "Defeat Barich" objective.
Guests: no active guest. If future testing discovers any active guest/NPC, it must be player-controlled
  in NG+ and never used as a skill check.
Reward rule: no usable rewards inside 054-058. Materia Blade is not awarded here.
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
Break through overlapping monster breath lanes, blunt the dragons with elemental resistance or disable
effects, answer Barich's single control source, and defeat Barich without being baited into a full
monster-pit cleanup.
```

The headline engine is **apex monster pressure under one control boss**. This is allowed to be the
hardest fight before Ultima, but every pressure point must be visible and answerable.

## Enemy Party Escalation

Accepted redesign: **v2 no-reward apex monster pit**.

| Slot | Role | Job / Unit | Level | Br/Fa | Purpose |
| ---: | --- | --- | ---: | --- | --- |
| 0 | Boss objective | Barich / Machinist | 105 | `84/55` | One Disable/Immobilize control source; defeat ends the fight. |
| 1 | Sustain | Chemist | 104 | `72/68` | Heals/revives or stabilizes the monster line, but must be raceable. |
| 2 | Breath lane | Monster job 139 | 105 | `90/30` | Apex monster body; overlapping breath/space pressure. |
| 3 | Breath lane | Monster job 140 | 105 | `90/30` | Second monster lane; pressures a different approach. |
| 4 | Breath lane | Monster job 141 | 105 | `90/30` | Third monster lane; reinforces the 5-star peak. |
| 5 | Breath lane | Monster job 135 | 105 | `90/30` | Fourth monster body; closes the pit without sealing Barich. |

Why this works:

```text
- Four level-105 monsters make this the true peak over 055/056.
- Overlapping breath lanes create the 5-star pressure, but elemental resistance/absorb and monster
  disable/break must remain valid answers.
- Barich is one answerable control source, not a permanent status lock.
- The Chemist sustains the pit, but the player can race it or bypass it by focusing Barich.
- The boss-focus lane is mandatory: defeating Barich must be a real plan before full cleanup.
- No usable reward appears here; Materia Blade stays outside this gauntlet battle.
```

## Builds

### Barich Fendsor - control boss

```text
Level: 105
JobLevel: 8
Primary: gun pressure plus Disable/Immobilize-style control
Secondary: intentional utility that does not create a second lock
Reaction: Counter or defensive reaction
Support: gun/control role support
Movement: boss mobility
Gear: complete gunner/caster gear; do not duplicate Glacial Gun, Blaze Gun, or Blaster from 042
Reward: none
```

Guardrail: Barich may pressure movement and actions, but he must remain one source of resistable or
cleansable control. No party-wide chain-lock.

### Chemist - sustain

```text
Level: 104
JobLevel: 8
Primary: Item sustain
Secondary: utility only
Reaction: intentional defensive reaction; current `510` empty reaction must be fixed
Support: intentional defensive/support ability; current `510` empty support must be fixed
Movement: Move +1 or equivalent; current `510` empty movement must be fixed
Gear: complete Chemist gear
Reward: none
```

Guardrail: sustain must be raceable. It should force priority decisions, not create a monster revive slog.

### Apex monsters x4 - breath lanes

```text
Level: 105
JobLevel: 8
Jobs: 139, 140, 141, 135
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
him. Spread the four monsters so their breath lanes overlap across obvious rush paths. Put Chemist behind
or between monsters where it can sustain, but not where killing it becomes mandatory before any boss
pressure is possible.
```

The player read should be: prepare elemental/status answers, disable or blunt one monster lane, push a
route to Barich, and end the control source before the breath pit drains the run.

## Simulation Plan and Results

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
None. No usable NG++ reward is added inside the final gauntlet.
Materia Blade is not awarded here and is not relocated into this fight.
Barich should not duplicate the gun trio from 042: Glacial Gun, Blaze Gun, or Blaster.
No monster or Chemist carries a hidden rare payload.
Keep standard/vanilla loot and buried Elixirs only.
```

## Implementation Checklist

- [ ] Preserve entry `439` and the "Defeat Barich" objective.
- [ ] Keep Barich level `105`, Chemist level `104`, and four monster bodies level `105`.
- [ ] Verify monster job identities for `139`, `140`, `141`, and `135`; preserve the apex monster pit.
- [ ] Create overlapping breath lanes through placement without sealing Barich behind mandatory cleanup.
- [ ] Ensure monster breath has real elemental/disable/break counterplay.
- [ ] Keep Barich to one answerable control source; no hard status lock.
- [ ] Fill Chemist R/S/M slots and verify every active human has complete equipment plus intentional
      secondary/reaction/support/move.
- [ ] Verify Barich item `76`; replace it if it duplicates a 042 gun reward.
- [ ] Add no usable reward, no Materia Blade, and no steal-dependent rare.
- [ ] Re-dump entry `439` after implementation and verify only intended kit/ability/positioning changes.
- [ ] Playtest `056 -> 057 -> 058` as a no-resupply unit.

## Test Questions

- Does this clearly feel like the 5-star peak before the finale?
- Are monster breath lanes scary because they overlap, not because they are unanswerable?
- Can players blunt the monster pit with elemental resist/absorb, Disable, breaks, or equivalent tools?
- Is Barich a single control source, not a chain-lock?
- Can the player focus Barich and end the fight without full monster cleanup?
- Are no usable NG++ rewards or unique steal payloads present?

## Sources

- Local: `docs/battles/ENDGAME-BLOCKER.md` for entry mapping and corrected roster.
- Local: `docs/battles/037-chapter-4-overview.md` for Chapter 4 puzzle-party principles and gauntlet curve.
- Local: `docs/battles/chapter-4-rewards-implementation.md` for the no-usable-reward rule in `054-058`.
- Local: `tmp/fft-level-design-057-lost-halidom/` simulation artifact.
- Local dump: `tools/entd_tool.py dump-entry --entry 439`.
- Game8, "Lost Halidom Walkthrough (Battle 52)": original objective and public monster-pit framing.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553228
