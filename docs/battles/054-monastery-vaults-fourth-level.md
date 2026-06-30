# 054 - Monastery Vaults, Fourth Level (Endgame Gauntlet 1/5)

Status: redesigned (documentation only; not implemented in game data by this task)
Chapter: 4 - "In the Name of Love"
Battle order: Battle 49 (ENDGAME GAUNTLET 1 of 5 - no resupply across 054 -> 055 -> 056 -> 057 -> 058)
Target version: Enhanced v1.5.0
ENTD: `entd4` global entry `435`
Local slot: `051`
Simulation artifact: `tmp/fft-level-design-054-monastery-vaults-fourth-level/`

> Docs-only redesign note: this document is the intended NG++ level design. It does not change the
> embedded ENTD, scripts, binaries, or patch code. Implementation must later patch entry `435` and
> preserve the event behavior verified below.

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
Can you preserve weapons/armor under capped Rend pressure while a fast flanker punishes loose formation,
without spending too much HP/MP/items before the first real boss at 055?
```

The headline engine is **gear preservation under capped Rend**. The Ninja is support tempo, not a
second puzzle. Monks add Chakra-first sustain, not a revive engine. No hard status, no boss, no reward.

## Enemy Party Escalation

Accepted redesign: **v2 capped-Rend tempo opener**.

| Slot | Role | Job | Level | Purpose |
|---:|---|---|---:|---|
| 0 | Cutscene | Loffrey / Divine Knight | 1 | Exits by script. Do not activate as a combatant. |
| 1 | Rend carrier | Knight | 103 | Equipment-break source #1; telegraphed gear-preservation test. |
| 2 | Rend carrier | Knight | 103 | Equipment-break source #2; the last allowed break source. |
| 3 | Guard body | Knight | 102 | Armored wall without meaningful Rend pressure. |
| 4 | Sustain body | Monk | 102 | Chakra-first melee sustain; no dedicated revive loop. |
| 5 | Sustain body | Monk | 102 | Second martial body; pressure and emergency sustain. |
| 6 | Tempo flanker | Ninja | 103 | Replaces Archer; melee flank tempo with tempered Throw/no high-tier payload. |

Why this works:

```text
- Two Rend sources keep the vanilla gear-loss lesson and remain answerable by Safeguard/Maintenance,
  Steal Weapon, disabling the carriers, or quick focus fire.
- The third Knight preserves the front wall but must not become a third effective break source.
- The Archer becomes a Ninja because a late-game Archer is too passive against NG++ builds; the Ninja
  forces formation discipline without adding hard control.
- Monk sustain is useful but bounded. This fight must not become a revive-loop slog before the gauntlet
  bosses start.
- The fight stays all-generic, defeat-all, and clearly lighter than 055-058.
```

## Builds

### Loffrey (slot 0) - cutscene unit

```text
Preserve event behavior: enters/exits by script and does not fight.
Do not turn him into a boss, target, reward carrier, or meaningful source of pressure.
```

### Knight x2 - capped Rend carriers

```text
Level: 103
JobLevel: 8
Primary: Knight / Battle Skill with Rend Weapon and Rend Armor as the visible threat
Secondary: Item or another low-impact utility, intentionally set
Reaction: Counter or Reflexes-tier defensive reaction
Support: Attack Boost / Defense Boost-tier role fit
Movement: Move +1
Gear: complete late-Chapter-4 heavy gear, shop-tier or non-reward role gear only
Reward: none
```

Guardrail: only these two may act as real break sources.

### Knight x1 - front guard without break pressure

```text
Level: 102
JobLevel: 8
Primary: Knight body, but implementation must suppress meaningful Rend use through ability selection,
AI priority, command setup, or a nearby equivalent job if the engine cannot cap Knight skills directly.
Secondary: Item or Basic Skill-style utility, intentionally set
Reaction/Support/Movement: complete defensive kit
Gear: complete heavy gear
Reward: none
```

Guardrail: if all three Knights can reliably Rend, the design fails. The cap of two break sources is
more important than preserving the third unit's exact command list.

### Monk x2 - Chakra-first sustain

```text
Level: 102
JobLevel: 8
Primary: Martial Arts; emphasize Chakra and melee pressure
Secondary: low-impact utility, no Phoenix Down spam engine
Reaction: Counter
Support: Attack Boost
Movement: Move +1
Gear: complete martial gear
Reward: none
```

Guardrail: Monks may keep the skirmish from collapsing instantly, but they should not produce a long
revive-loop cleanup before 055.

### Ninja x1 - tempered tempo flanker

```text
Level: 103
JobLevel: 8
Primary: Ninja/Throw, but no high-tier Throw payload
Secondary: Steal, Item, or another utility that does not add status lock
Reaction: Reflexes
Support: Attack Boost / Concentration-tier offense, not a second engine
Movement: Move +2
Gear: complete shop-tier ninja gear; dual-wield melee pressure
Reward: none
```

Guardrail: the Ninja exists to punish loose formation and speed up the opener. It should not become a
burst-delete unit or hidden reward carrier.

## Positioning Plan

```text
Use the cramped vault corridors. Put the two Rend Knights forward enough that the player sees the gear
threat immediately. The third Knight anchors the wall. Monks sit behind/adjacent as Chakra-first sustain.
The Ninja starts on a side route or flank so the party cannot simply turtle behind one frontliner.
```

The intended player read is: protect the loadout, isolate one break Knight, keep the Ninja from slipping
onto casters, and end the guard fight with resources intact.

## Simulation Plan and Results

Artifact:

```text
tmp/fft-level-design-054-monastery-vaults-fourth-level/
```

Accepted candidate:

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
- Confirm only two Knights can meaningfully use Rend/break pressure.
- Confirm the Ninja adds tempo without causing unrecoverable losses before 055.
- Test 054 immediately into 055; this opener should cost attention, not consume the run.
```

## Implementation Checklist

- [ ] Preserve entry `435`, slot `0` Loffrey as cutscene exit / non-combat unit.
- [ ] Keep active enemy count at 6.
- [ ] Convert the Archer slot (`s6`) to a tempered Ninja, level `103`, complete kit.
- [ ] Keep two Knight Rend carriers at level `103`.
- [ ] Keep the third Knight at level `102` and prevent it from becoming a third effective break source.
- [ ] Keep both Monks level `102`, complete kits, Chakra-first sustain, no revive-loop engine.
- [ ] Ensure every active human has complete equipment plus intentional secondary/reaction/support/move.
- [ ] Add no usable rewards, no Tier-A/Tier-S payloads, and no steal-dependent reward hooks.
- [ ] Re-dump entry `435` after implementation and verify only the intended slot/kit changes.
- [ ] Playtest `054 -> 055` back-to-back from the point-of-no-return save.

## Test Questions

- Does the fight still read as the gauntlet's light all-generic opener?
- Is gear preservation the felt lesson, with Rend capped at two answerable sources?
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
