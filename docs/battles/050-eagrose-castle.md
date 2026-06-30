# 050 - Eagrose Castle (Igros Castle)

Status: 📝 redesign v2 planned (docs-only) — v1 implementation exists for entry 459
Chapter: 4 — "In the Name of Love"
Battle order: Battle 45 (after the Limberry chain)
Target version: Enhanced v1.5.0
ENTD: global entry **459** (local 75, entd4)
File: `battle_entd4_ent.bin`

> **NG++ rewards applied (2026-06-27):** Maximillian + Grand Helm + Venetian Shield through guaranteed
> Spoils of War (`0x1e`), NG+ only, within the 3-item cap, no stealing required. Canonical map:
> `chapter-4-rewards-implementation.md`.

## Current Implementation / Data Reality

```text
DATA REALITY (verified from current embedded entd4 dump, entry 459):
  slot 0 = allied story guest record
           name/job 8, level 103, JobLevel 8, full gear (Runeblade/Crystal Shield-class loadout).
           Must be player-controlled in NG++ if active. Do not use guest AI as difficulty.

  slot 1 = Dycedarg
           name/job 9, level 104, JobLevel 8, complete setup:
           secondary 71, reaction 450, support 479, movement 486.
           gear includes Grand Helm (156), Maximillian-tier body (181), Defender (33), Aegis Shield (136).
           Spoils payload = 0xB9 (Maximillian).

  slots 2-6 = five Knight stair-wall bodies
              job 76, level 103, JobLevel 8, full equipment and R/S/M setup:
              Counter (442), Attack Boost (465), Movement +1 (486), heavy gear + Bracers.
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

Planned v2 redesign (docs-only in this pass): keep the two-phase brother fight, but make the fairness
requirements explicit. The active guest must be controlled. The stair wall may contain five bodies, but
no more than two can be **effective break sources**. Phase 2 must remain a sequential transform into a
spaceable Lucavi AoE puzzle, not simultaneous pressure layered on top of the full Knight wall.

> Data-layer fields are known for entry 459, but final implementation still needs a fresh dump/diff and
> in-game verification of guest control, transform behavior, and the hard break-source cap. This pass
> updates documentation only.

## Design Goal

```text
Make Eagrose the second major Chapter 4 Lucavi spike: Phase 1 is a controlled high-stair gear-pressure
wall around Dycedarg, Phase 2 is Adramelk's spread-or-die summon pressure. The player must protect key
gear, crack the stair wall, then spread and burst the Lucavi. The fight must never become a five-Rend
gear deletion wall, an AI-guest failure, or a non-spaceable AoE/status lock.
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
demands must remain sequential and readable. If all five Knights are effective Rend users, the first
phase becomes a gear-destruction tax. If Adramelk's AoE is non-spaceable, the second phase becomes a
wipe check. If the guest is AI-controlled, the fight asks the player to babysit a bad decision engine.

For New Game++ the identity must stay: **controlled guest, capped break wall, then space against the
Lucavi.**

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

STILL NEEDED FOR V2 IMPLEMENTATION:
- Verify slot 0 is active and player-controllable; if not, set the guest-control bit.
- Verify the transform from Dycedarg to Adramelk fires correctly.
- Enforce the two-effective-breaker cap. If Knight primary command makes all five job-76 bodies real
  break sources, implementation must change three bodies' job/command/AI/ability layer to non-break
  heavy guards. Leaving a five-Rend wall is not acceptable v2 behavior.
- Confirm Adramelk's AoE/status cadence is telegraphed, spaceable, resistable, and non-locking.
- Confirm all three spoils land in the first three awarded `0x1e` items.
- Preserve buried map treasure as vanilla map loot.
```

## Enemy Party Escalation (Chapter 4 rule)

```text
Headline engine: two-phase brother-to-Lucavi fight.
Phase 1 support structure:
  - Dycedarg anchors the upper stairs.
  - Two effective breakers threaten gear and force Safeguard/Maintenance/Steal/disarm decisions.
  - Three non-break heavy guards preserve the Knight-wall feeling without creating a five-source break
    lock.

Phase 2 support structure:
  - Adramelk is the single Lucavi engine.
  - Summon-AoE punishes clumping.
  - Confuse/Stone-style status is resistable and non-locking.

WHY: the original battle is already a strong puzzle: elevation wall -> demon reveal. Chapter 4 v2 makes
both halves matter while keeping them sequential and answerable.
```

## Sanctioned Exceptions

```text
KNIGHT REND / BREAK:
  Allowed because Phase 1 is a gear-preservation wall. Guardrail: hard cap of two effective break
  sources. Five coordinated breakers are banned.

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
  - Dycedarg may visibly carry defensive lord gear as threat identity.
  - The armor set is still guaranteed through spoils, not dependent on stealing from him.

PRESERVE:
  - Buried map treasure remains vanilla map loot.
  - No Excalibur. Excalibur stays Orlandeau's.
```

## Proposed Composition (New Game++ Eagrose Castle v2)

Keep the local two-phase roster and levels. The required redesign is not more bodies; it is hard
fairness around break count, guest control, reward handling, and phase separation.

### Phase 1 - Dycedarg + High-Stair Wall

| Slot | Role | Unit type | Level | Br/Fa | Purpose |
| ------ | ------ | ----------- | ------- | --- | --------- |
| s0 | Allied guest/story unit | Guest record | `103` | `70/65` | Player-controlled ally if active; not a failure condition engine. |
| s1 | Boss / phase trigger | Dycedarg | `104` | `88/60` | High-stair anchor; defeat triggers Lucavi phase; reward payload. |
| s2 | Breaker 1 / reward payload | Knight body | `103` | `88/42` | Effective break source 1; Grand Helm spoil. |
| s3 | Breaker 2 / reward payload | Knight body | `103` | `88/42` | Effective break source 2; Venetian Shield spoil. |
| s4 | Heavy guard | Non-break effective stair guard | `103` | `84/55` | Body pressure without break-lock. |
| s5 | Heavy guard | Non-break effective stair guard | `103` | `84/55` | Second guard; preserves wall. |
| s6 | Heavy guard | Non-break effective stair guard | `103` | `84/55` | Third guard; blocks route without extra Rend pressure. |

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

The accepted design is **v2 hard-capped brother duel**. The first simulation overcounted pressure by
treating both phases as simultaneous; iteration 2 correctly models the transform as sequential. Under
that model, the fight is a valid Chapter 4 spike only if the five-body stair wall has no more than two
effective breakers and the guest is controlled. The reward ledger is the full armor/shield set, not the
old single-Grand-Helm plan.

Rejected variants:

```text
- Five-Rend stair wall: gear deletion tax, violates break-source cap.
- AI guest hostage: guest AI becomes a failure condition.
- Unavoidable summon lock: Phase 2 loses spacing counterplay.
- Extra caster support: adds a second engine to an already two-phase fight.
- Single-phase Dycedarg: removes the Lucavi reveal.
- One-rare old ledger: contradicts Maximillian + Grand Helm + Venetian Shield reward map.
- Steal-required armor set: contradicts guaranteed spoils.
- Overlevelled brother spike: replaces puzzle pressure with raw stats.
- No-break stair wall: loses Phase 1's gear-preservation lesson.
- Simultaneous pressure pile-up: makes phase 1 and phase 2 feel like one overloaded fight.
```

## Builds (two-phase boss fight)

```text
Guest/story ally slot 0:
  - Keep level 103 and current gear unless implementation data says otherwise.
  - Must be player-controlled if active.
  - Do not tune the battle around this unit's AI survival.

Dycedarg:
  - Level 104, JobLevel 8, complete setup already present.
  - Preserve lord/defender identity and transform trigger.
  - Defensive gear is allowed as visible identity; rewards are spoils.

Breaker Knights x2:
  - Level 103, JobLevel 8, full gear/R/S/M.
  - These are the only effective break sources.
  - Their purpose is to force gear protection/disarm routing.

Heavy guards x3:
  - Level 103, full gear/R/S/M.
  - Must not function as additional effective break sources.
  - If job 76 primary makes Rend unavoidable, implementation must solve it by job/command/AI/ability
    layer changes rather than accepting five breakers.

Adramelk / Adrammelech:
  - Level 105 Lucavi transform, no normal equipment.
  - One summon-AoE engine, telegraphed and spaceable.
  - Status pressure is support only: resistable, cleansable, non-locking.
```

## Positioning Plan

```text
Phase 1: Dycedarg and the stair wall hold the upper level. The two breakers cover the most direct
approach; the three heavy guards block lanes and bodyguard without adding more break pressure. Slot 0
guest starts controllable and must not be exposed to unavoidable failure.

Phase 2: After the transform, Adramelk's threat becomes spacing. The player should have room to spread,
re-buff, and focus the Lucavi instead of being pinned in the stair-wall geometry by leftover break spam.
```

The keep should say: "your brother hides behind the house's steel; break through the stair wall, then
scatter when the demon rises."

## Simulation Plan and Results

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

Iteration decision:

```text
ACCEPT v2 hard-capped brother duel.
Iteration 2 treats the fight as sequential phases. The stair wall is allowed only with two effective
breakers, slot 0 must be controllable if active, and Phase 2 must remain spaceable.
```

## Implementation Checklist

- [ ] Re-dump entry 459 and verify slot order, rewards, placeholder behavior, and transform.
- [ ] Verify slot 0 is active and controllable; if active but not controllable, set player control.
- [ ] Preserve win condition and Dycedarg -> Adramelk transform.
- [ ] Keep Dycedarg at `104`; Knight bodies at `103`; Adramelk at `105`; guest at `103`.
- [ ] Enforce hard cap: no more than two effective break sources in Phase 1.
- [ ] Preserve complete gear/R/S/M on active human enemies, but do not let all five Knights be breakers.
- [ ] Keep Phase 2 AoE/status telegraphed, spaceable, resistable, and non-locking.
- [ ] Author/verify spoils: Maximillian + Grand Helm + Venetian Shield, guaranteed and within the 3-item cap.
- [ ] Preserve buried map treasure as map treasure.

## Test Questions

- Is slot 0 player-controlled if active, and does the battle avoid guest-AI failure?
- Are only two enemies functioning as effective break sources in Phase 1?
- Does the stair wall still feel like Eagrose without becoming a gear deletion lock?
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
