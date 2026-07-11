# 054 - Monastery Vaults, Fourth Level (Endgame Gauntlet 1/5)

Status: v3 implemented/deployed - direct playtest pending
Chapter: 4 - "In the Name of Love"
Battle order: Battle 49 (ENDGAME GAUNTLET 1 of 5 - no resupply across 054 -> 055 -> 056 -> 057 -> 058)
Target version: Enhanced v1.5.0
ENTD: `entd4` global entry `435`
Local slot: `051`
Simulation artifact: `tmp/fft-level-design-054-monastery-vaults-fourth-level/`

> **V3 implementation (2026-07-11):** entry 435 patched in the embedded ENTD and deployed through a
> successful Release build. Loffrey's cutscene record, objective, positions, enemy count and no-reward
> rule are preserved. Sprite-sheet count remains unchanged at four.

## V3 Locked Decisions

```text
s1/s2 = Eagrose Knight Martial Artists (slots 2/3), copied respectively.
s3    = Eagrose Knight Samurai (slot 4).
s4/s5 = two exact copies of Fort Besselat South Wall Monk (slot 6).
s6    = exact copy of Fort Besselat South Wall Ninja (slot 5; replaces vanilla Archer).

PRESERVE:
  s0 Loffrey exits by script and remains non-combatant.
  Defeat-all objective, six active generics and all vanilla positions.
  No usable rewards or rare payloads.
```

## Gate Answers / Constraints

```text
Scope: redesign battle doc 054 only; no game data or code changes.
Allowed changes in design: active enemy job/kit/level/gear/ability plan, placement, and test criteria.
Chapter target: Chapter 4 broken-but-readable puzzle, but this specific map is the light opener.
Must preserve: all-generic vault guard feeling, defeat-all objective, Rend/gear-preservation lesson,
  Loffrey's cutscene exit, cramped vault terrain, and no-resupply gauntlet context.
Guests: no active guest. If future testing discovers any active guest/NPC, it must be player-controlled
  in NG+ and never used as a skill check.
Reward rule: no usable rewards inside 054-058. This fight has no boss rare and no designed spoil.
```

## Original Battle

Objective:

```text
Defeat all enemies!
```

Player deployment:

```text
Up to 5 units, including Ramza. No outfitter: this is the first fight after the point of no return.
```

Original enemy composition:

```text
Loffrey appears as a scripted cutscene unit and exits before the fight.
3x Knight
2x Monk
1x Archer
```

The vanilla role is not a boss test. It is the gauntlet's first breath: an all-generic guard skirmish
whose real danger is context. The Knights threaten equipment breaks at the exact moment the player is
locked into five consecutive battles with no shop, no outfitter, and no chance to repair a stripped
loadout. The lesson is simple and important: preserve your gear before the real bosses begin.

## Local Data Confirmed

Dump command:

```bash
python tools/entd_tool.py dump-entry --input src/fftivc.battles.ngplus/entd/battle_entd4_ent.bin --entry 435 --include-empty
```

Confirmed active data:

| Slot | Status | Job | Level | JL | Secondary | Reaction | Support | Move | Equipment ids | Notes |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| 0 | Cutscene / exits | 37 | 1 | 4 | 61 | 447 | 466 | 492 | 153,181,211,33,136 | Loffrey. Preserve as non-combat event unit. |
| 1 | Active | 76 | 102 | 8 | 254 | 442 | 465 | 486 | 154,182,218,254,139 | Knight body. |
| 2 | Active | 76 | 102 | 8 | 254 | 442 | 465 | 486 | 154,182,218,254,139 | Knight body. |
| 3 | Active | 76 | 102 | 8 | 254 | 442 | 465 | 486 | 154,182,218,254,139 | Knight body. |
| 4 | Active | 78 | 102 | 8 | 0 | 442 | 465 | 486 | 163,195,218,254,254 | Monk body. |
| 5 | Active | 78 | 102 | 8 | 0 | 442 | 465 | 486 | 163,195,218,254,254 | Monk body. |
| 6 | Active | 77 | 102 | 8 | 5 | 449 | 469 | 486 | 168,198,218,87,254 | Archer body. |

Data implications:

```text
- Entry 435 is confirmed moddable through ENTD direct edits.
- Slot 0 must not become an active boss. Loffrey's real fight is 055.
- The active roster is exactly 6 generics. Preserve the count and all-generic opener identity.
- Current active humans have full equipment and reaction/support/movement, but secondaries are not yet
  intentionally designed for the Chapter 4 rule. The redesign requires complete intentional kits.
- Current data still has the Archer; the proposed redesign swaps only that active slot to Ninja.
```

## Design Goal

Turn the old 1/5 warm-up into a readable NG++ opener: still the lightest fight of the final stretch,
but no longer free for a tuned party. The fight should ask:

```text
Can you preserve weapons/armor against three distinct Knight styles while an unarmed Ninja flanker
punishes loose formation,
without spending too much HP/MP/items before the first real boss at 055?
```

The headline engine is **gear preservation against the imported Eagrose Knight trio**. The Ninja and
Monks reproduce the South Wall martial package without adding a second puzzle. No hard status, boss,
or reward is added.

## Enemy Party Escalation

Accepted redesign: **v3 imported-build gauntlet opener**.

| Slot | Role | Job | Level | Br/Fa | Purpose |
| ---: | --- | --- | ---: | --- | --- |
| 0 | Cutscene | Loffrey / Divine Knight | 1 | `90/55` | Exits by script. Do not activate as a combatant. |
| 1 | Knight Martial Artist | Eagrose s2 copy | 100 | `88/42` | Shielded Arts of War + Martial Arts bruiser. |
| 2 | Knight Martial Artist | Eagrose s3 copy | 100 | `86/44` | Second shielded Arts of War + Martial Arts bruiser. |
| 3 | Knight Samurai | Eagrose s4 copy | 101 | `88/58` | Arts of War + Iaido, Shirahadori and Doublehand. |
| 4 | Monk | South Wall s6 copy | 101 | `88/38` | Counter/Dual Wield martial body with Jump +3. |
| 5 | Monk | South Wall s6 copy | 101 | `88/38` | Exact second copy of the same Monk build. |
| 6 | Ninja | South Wall s5 copy | 102 | `90/35` | Unarmed Martial Arts/Brawler flanker with Jump +3. |

Why this works:

```text
- All three Knights retain primary Arts of War because their main job remains Knight. Their Martial
  Arts/Iaido split makes the visible gear threat readable through three imported Eagrose builds.
- The Archer becomes the South Wall Ninja, forcing formation discipline through unarmed Brawler pressure.
- The two South Wall Monks reproduce the Counter/Dual Wield/Jump +3 build without adding hard control.
- The fight stays all-generic, defeat-all, and clearly lighter than 055-058.
```

## Builds

### Loffrey (slot 0) - cutscene unit

```text
Preserve event behavior: enters/exits by script and does not fight.
Do not turn him into a boss, target, reward carrier, or meaningful source of pressure.
```

### Knight x2 - Eagrose Knight Martial Artists

```text
Levels: s1 100; s2 100
JobLevel: 8
Main job: Knight
Primary: Arts of War
Job bucket: Monk, Job Level 8
Secondary: Martial Arts
Brave/Faith: s1 88/42; s2 86/44
Reaction: Counter
Support: Attack Boost
Movement: Movement +3
Right hand: Runeblade
Left hand: Crystal Shield
Head: Crystal Helm
Body: Crystal Mail
Accessory: Bracers
Reward: none
```

### Knight x1 - Eagrose Knight Samurai

```text
Level: 101
JobLevel: 8
Main job: Knight
Primary: Arts of War
Job bucket: Samurai, Job Level 8
Secondary: Iaido
Brave/Faith: 88/58
Reaction: Shirahadori
Support: Doublehand
Movement: Movement +3
Right hand: Runeblade
Left hand: None
Head: Crystal Helm
Body: Crystal Mail
Accessory: Magepower Glove
Reward: none
```

### Monk x2 - Fort Besselat South Wall copies

```text
Level: 101
JobLevel: 8
Main job: Monk
Primary: Martial Arts
Secondary: None
Brave/Faith: 88/38
Reaction: Counter
Support: Dual Wield
Movement: Jump +3
Right hand: None
Left hand: None
Head: Barrette
Body: Power Garb
Accessory: Bracers
Reward: none
```

Both Monks use the exact same build.

### Ninja x1 - Fort Besselat South Wall copy

```text
Level: 102
JobLevel: 8
Main job: Ninja
Primary: Throw
Secondary: Martial Arts
Brave/Faith: 90/35
Reaction: Counter
Support: Brawler
Movement: Jump +3
Right hand: None
Left hand: None
Head: Thief's Cap
Body: Power Garb
Accessory: Bracers
Reward: none
```

Guardrail: the Ninja exists to punish loose formation and speed up the opener. It should not become a
burst-delete unit or hidden reward carrier.

## Positioning Plan

```text
Use the existing cramped-vault positions. The two Martial Artist Knights and Knight Samurai form the
visible Arts-of-War wall. The Monks occupy their vanilla lanes, while the Ninja retains the old Archer
position as a distant approach threat.
The Ninja starts on a side route or flank so the party cannot simply turtle behind one frontliner.
```

The intended player read is: protect the loadout, isolate one break Knight, keep the Ninja from slipping
onto casters, and end the guard fight with resources intact.

## Historical v2 Simulation / v3 Test Plan

Artifact:

```text
tmp/fft-level-design-054-monastery-vaults-fourth-level/
```

Historical accepted candidate, superseded by the locked v3 imported builds:

```text
v2 capped-rend tempo opener
Pressure: 306
Gear risk: 54
Opener lightness: 90.1
Answerability: 100
Chain tax: 38
Roster fidelity: 100
Reward correctness: 100
```

Iteration notes:

```text
- Vanilla Archer screen was rejected as too low-tempo for NG++ endgame.
- A raw Ninja swap was initially too heavy for an opener, so v2 tempers the Ninja: melee flank pressure,
  no high-tier Throw payload.
- Three Rend sources were rejected because they create a gear-loss spiral across the no-resupply chain.
- Activating Loffrey was rejected because it steals the role of 055 and breaks the all-generic opener.
- Hard status, extra engines, overleveling, revive-loop sustain, and usable rewards were rejected as
  unfair chain tax.
```

Residual risks:

```text
- Confirm Loffrey exits before combat and cannot be targeted or rewarded.
- Confirm the three Arts-of-War Knights remain answerable through Safeguard, disarm, range or focus fire.
- Confirm the Ninja adds tempo without causing unrecoverable losses before 055.
- Test 054 immediately into 055; this opener should cost attention, not consume the run.
```

## Implementation Checklist

- [x] Preserve entry `435`, slot `0` Loffrey as cutscene exit / non-combat unit.
- [x] Keep active enemy count at 6.
- [x] Set s1/s2 as exact copies of Eagrose Knight Martial Artists s2/s3.
- [x] Set s3 as an exact copy of Eagrose Knight Samurai s4.
- [x] Set s4/s5 as exact copies of Fort Besselat South Wall Monk s6.
- [x] Convert the Archer slot s6 into an exact copy of Fort Besselat South Wall Ninja s5.
- [x] Ensure every active human has complete equipment plus intentional secondary/reaction/support/move.
- [x] Add no usable rewards, no Tier-A/Tier-S payloads, and no steal-dependent reward hooks.
- [x] Re-dump entry `435` after implementation and verify only the intended slot/kit changes.
- [ ] Playtest `054 -> 055` back-to-back from the point-of-no-return save.

## Test Questions

- Does the fight still read as the gauntlet's light all-generic opener?
- Is gear preservation still the felt lesson with the three imported Eagrose Knight styles?
- Does the Ninja punish loose formation without turning the opener into a burst wall?
- Do the Monks add limited sustain without causing a cleanup slog?
- Is there zero usable reward or rare leak inside the no-resupply gauntlet?
- Does the party enter `055` strained but not drained?

## Sources

- Local: `docs/battles/ENDGAME-BLOCKER.md` for entry mapping and Loffrey cutscene behavior.
- Local: `docs/battles/037-chapter-4-overview.md` for Chapter 4 puzzle-party principles and gauntlet curve.
- Local: `docs/battles/chapter-4-rewards-implementation.md` for the no-usable-reward rule in `054-058`.
- Local: `tmp/fft-level-design-054-monastery-vaults-fourth-level/` simulation artifact.
- Local dump: `tools/entd_tool.py dump-entry --entry 435`.
