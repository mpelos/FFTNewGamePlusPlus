# 052 - Mullonde Cathedral Nave (Murond Holy Place)

Status: 📝 redesign v2 planned (docs-only) — v1 implementation exists for entry 461
Chapter: 4 — "In the Name of Love"
Battle order: Battle 47 (Mullonde chain 2 of 3 — NO resupply across 46→47→48)
Target version: Enhanced v1.5.0
ENTD: global entry **461** (local 77, entd4)
File: `battle_entd4_ent.bin`

> **NG++ rewards applied (2026-06-27):** Chaos Blade + Escutcheon + Lordly Robe through guaranteed
> Spoils of War (`0x1e`), NG+ only, within the 3-item cap, no stealing required. These are paid here so
> the player has the best pre-gauntlet gear before the point of no return. Canonical map:
> `chapter-4-rewards-implementation.md`.

## Current Implementation / Data Reality

```text
DATA REALITY (verified from current embedded entd4 dump, entry 461):
  slot 0 = Folmarv
           job 36, level 105, JobLevel 8, complete gear/setup, Chaos Blade in right hand.
           Reaction 442, support 466, movement 486. Spoils payload = 0x25 (Chaos Blade).

  slot 1 = Loffrey
           job 37, level 104, JobLevel 8, complete gear/setup.
           Reaction 437, support 466, movement 489. Spoils payload = 0x8F (Escutcheon).

  slot 2 = Cletienne
           job 39, level 104, JobLevel 8, complete caster gear/setup.
           Reaction 435, support 468, movement 492. Spoils payload = 0xCF (Lordly Robe).

  slot 3 = job-39 clone/script placeholder
           level 65, no normal battle role; preserve until playtest proves active.

Current v1 implementation:
  Folmarv = 105, Loffrey/Cletienne = 104.
  Three named bosses are complete.
  Chaos Blade is active on Folmarv.
  Escutcheon + Lordly Robe are reward payloads on the other boss records.
  Win-on-one-falls and retreat behavior must be preserved.
```

Planned v2 redesign (docs-only in this pass): keep the pure triple-boss Nave, preserve the win-on-one
focus race, and align the reward language with the current ledger. Loffrey and Cletienne may retreat,
but their best-in-slot items are still paid as guaranteed battle spoils here by project rule.

> MULLONDE CHAIN: 46 (`051`) → 47 (`052`) → 48 (`053`), one loadout.

## Design Goal

```text
Make Mullonde Nave the chain's focus-and-commit boss rush: Folmarv and Loffrey threaten gear with two
effective break sources, Cletienne denies turtling with caster pressure, and the player wins by choosing
one boss and ending the fight before attrition strips the party. Rewards are Chaos Blade + Escutcheon +
Lordly Robe via guaranteed spoils, not a Steal or clear-all requirement.
```

No active guests appear here. No guest-control implementation is needed for this battle.

## Original Battle

Objective:

```text
Defeat Folmarv!   (the fight ends when one of the three bosses falls; the others retreat)
```

Player deployment:

```text
Up to 5 units, including Ramza. No outfitter (chain 2/3).
```

Original enemy composition:

```text
Folmarv Tengille   (Divine Knight leader; equipment-break pressure)
Loffrey Wodring    (Divine Knight; second equipment-break source)
Cletienne Duroi    (Sorcerer; ranged magic pressure)
```

Public walkthrough details:

```text
Recommended level: ~60. Difficulty: 4/5 stars. Three named bosses, no generics.
The encounter ends when any one boss is defeated or pushed to the retreat condition. Folmarv is the
named/intended target. The tactical advice is to disarm/break the Templars and commit to a target while
Cletienne pressures the party from range.
```

Design reading:

The Nave is **the triple-Templar focus race**. It escalates Bervenia's single break boss into three
named enemies acting at once, but it stays readable because the player does not need to clear all three.
The skill test is target discipline under gear pressure: identify the break sources, control or disarm
them, then burst one boss before the chain tax gets out of hand.

For New Game++ the identity must stay: **three named bosses, no generics, win when one falls.**

## Local Data Confirmed / Data Still Needed

```text
CONFIRMED:
- Entry 461 is Mullonde Nave.
- Slots 0-2 are Folmarv, Loffrey, and Cletienne.
- Slot 3 is a job-39 script placeholder and should not be treated as a normal enemy unless proven active.
- Folmarv is level 105; Loffrey/Cletienne are level 104.
- All three named bosses have complete gear/setup.
- Folmarv carries Chaos Blade actively.
- Rewards are Chaos Blade + Escutcheon + Lordly Robe guaranteed spoils.
- No active guests.

STILL NEEDED FOR V2 IMPLEMENTATION:
- Verify the fight ends when any one boss falls and the others retreat.
- Verify all three authored spoils are awarded despite the retreat behavior.
- Confirm Folmarv and Loffrey are the only effective break sources.
- Confirm Cletienne's magic has answerable timing and does not become hard status/instant wipe.
- Preserve buried map treasure as vanilla map loot.
```

## Enemy Party Escalation (Chapter 4 rule)

```text
Headline engine: triple-Templar focus race.
Supporting roles:
  - Folmarv is the leader, intended target, Chaos Blade carrier, and first break source.
  - Loffrey is the second break source and pincer threat.
  - Cletienne is caster pressure that prevents turtling behind break protection.

WHY: adding generics would dilute the original's clean boss rush. The Chapter 4 escalation is not more
units; it is three boss-quality kits forcing the player to commit under pressure.

CONSTRAINTS:
  - Win-on-one-falls remains.
  - No generic adds.
  - No more than two effective break sources.
  - Cletienne stays a caster, not a hard-lock engine or third breaker.
  - Rewards are guaranteed spoils and do not require killing all three.
```

## Sanctioned Exceptions

```text
TWO EQUIPMENT-BREAK BOSSES:
  Allowed because this is the Templar center of the campaign. Guardrail: exactly two effective break
  sources; disarm, break-resist, Safeguard/Maintenance, and focused burst remain fair answers.

WIN-ON-ONE-FALLS:
  Preserved as the main tactical rule. It reduces cleanup and keeps the battle about commitment.

RETREAT REWARD BEND:
  Normally retreating bosses do not pay drops. This battle intentionally bends that convention through
  guaranteed Spoils of War because the reward ledger moves Escutcheon + Lordly Robe pre-gauntlet.

PURE THREE-BOSS FIGHT:
  No generics. The pressure is concentration, not enemy count.
```

## Rare/reward handling

```text
Guaranteed spoils for entry 461: CHAOS BLADE + ESCUTCHEON + LORDLY ROBE.
These are delivered by the Spoils of War reward channel; the player must never be required to Steal.

COMBAT ROLE:
  - Chaos Blade is active on Folmarv and is both threat identity and reward payload.
  - Escutcheon and Lordly Robe are reward payloads here, not a demand to kill Loffrey/Cletienne.

PRESERVE:
  - The other bosses can retreat when one falls.
  - Buried map treasure remains vanilla map loot.
  - No Excalibur. Excalibur stays Orlandeau's.
```

## Proposed Composition (New Game++ Mullonde Nave v2)

Keep the local three-boss roster. Folmarv is `105`; Loffrey and Cletienne are `104`.

| Slot | Role | Unit type | Level | Purpose |
|------|------|-----------|-------|---------|
| s0 | Leader / intended target / reward payload | Folmarv, Divine Knight | `105` | Break source 1; active Chaos Blade; focus target. |
| s1 | Pincer breaker / reward payload | Loffrey, Divine Knight | `104` | Break source 2; pressures gear and positioning; Escutcheon spoil. |
| s2 | Caster / reward payload | Cletienne, Sorcerer | `104` | Ranged magic pressure; no break; Lordly Robe spoil. |
| s3 | Script placeholder | Job-39 clone | `65` | Preserve unless proven active. |

Reasoning:

The accepted design is **v2 triple-Templar focus race**. The simulation rejects every attempt to add
generics, require clearing all three, add a third breaker, or keep the old one-reward logic. The fight
is hard because three boss-quality kits pressure one party of five on no resupply, but the win condition
keeps it fair: choose one, solve the break/caster screen, and end the battle.

Rejected variants:

```text
- Clear-all triple boss: breaks the focus race and overtaxes the chain.
- Templars plus generics: dilutes the pure boss identity.
- Three-breaker pile-up: violates break-source cap.
- Hard-lock Sorcerer: turns Cletienne into a second headline engine.
- Old one-reward ledger: contradicts current reward map.
- Steal-required Chaos Blade: contradicts guaranteed spoils.
- Overlevelled Nave: replaces target discipline with raw stats.
```

## Builds (three boss-quality kits)

```text
Folmarv:
  - Level 105, JobLevel 8.
  - Primary: Divine Knight / equipment-break package.
  - Reaction/Support/Move: complete boss setup already present.
  - Active gear: Chaos Blade as threat and story reward.
  - Role: intended kill target and first break source.

Loffrey:
  - Level 104, JobLevel 8.
  - Primary: Divine Knight / equipment-break package.
  - Reaction/Support/Move: complete boss setup already present.
  - Role: second break source; pincer pressure.

Cletienne:
  - Level 104, JobLevel 8.
  - Primary: Sorcerer/caster pressure.
  - Reaction/Support/Move: complete caster setup already present.
  - Guardrail: no hard-lock status engine, no third break source, no instant wipe magic.
```

## Positioning Plan

```text
Nave interior: Folmarv and Loffrey pressure from forward/central lanes so their break threat is visible.
Cletienne uses altar/backline sightlines to punish turtling and force movement. Pillars and elevation
should give the player cover, approach choices, and a reason to commit to one target.

The player should see the intended line:
  1. Pick the target, usually Folmarv because of objective/read/reward.
  2. Disarm, protect against, or burst through the two break sources.
  3. Keep moving under Cletienne's magic.
  4. End the fight when one boss falls.
```

The nave should say: "three Templars bar the altar; choose one throat, protect your steel, and end the
stand before the chain bleeds you dry."

## Simulation Plan and Results

Simulation artifact:

```text
tmp/fft-level-design-052-mullonde-nave/
  assumptions.md
  simulate.py
  iteration-results.json
  iteration-results.md
```

Model scope:

```text
Coarse deterministic triple-Templar focus-race model over the first six rounds.
It scores pressure, focus clarity, break fairness, caster fairness, answerability, reward correctness,
scripting fidelity, and chain tax. It does not simulate exact FFT formulas.
```

Result summary:

| Candidate | Pressure | Focus clarity | Break fair | Caster fair | Answer | Reward | Scripting | Chain tax | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| v2 triple-Templar focus race | 338 | 96 | 92 | 88 | 98 | 100 | 100 | 52 | **Accepted** |
| clear-all triple boss | 420 | 38 | 92 | 88 | 57 | 100 | 55 | 66 | Rejected: breaks focus |
| templars plus generics | 374 | 76 | 92 | 88 | 84 | 100 | 80 | 64 | Rejected: generic dilution |
| three-breaker pile-up | 387 | 96 | 68 | 58 | 75 | 100 | 100 | 52 | Rejected: too many breaks |
| hard-lock sorcerer | 405 | 96 | 92 | 18 | 64 | 100 | 100 | 74 | Rejected: hard caster |
| old one-reward ledger | 338 | 82 | 92 | 88 | 98 | 56 | 100 | 52 | Rejected: reward ledger |
| steal-required chaos blade | 338 | 96 | 82 | 88 | 98 | 40 | 100 | 52 | Rejected: reward policy |
| overlevelled nave | 366 | 96 | 92 | 80 | 88 | 100 | 100 | 62 | Rejected: raw levels |

Iteration decision:

```text
ACCEPT v2 triple-Templar focus race.
The battle stays pure: three bosses, two break sources, one caster, win when one falls, and all three
rewards delivered through guaranteed spoils.
```

## Implementation Checklist

- [ ] Re-dump entry 461 and verify slots 0-3.
- [ ] Preserve win-on-one-falls and retreat behavior.
- [ ] Preserve no-generic roster.
- [ ] Keep levels: Folmarv `105`; Loffrey/Cletienne `104`.
- [ ] Keep no more than two effective break sources: Folmarv + Loffrey only.
- [ ] Keep Cletienne caster pressure answerable, not hard-lock or instant wipe.
- [ ] Author/verify spoils: Chaos Blade + Escutcheon + Lordly Robe, guaranteed and within the 3-item cap.
- [ ] Preserve buried map treasure as map treasure.
- [ ] Test as Mullonde chain 2/3 with resources from `051` and into `053`.

## Test Questions

- Does the fight end when any one boss falls, with the other two retreating?
- Are all three rewards awarded even when only one boss dies?
- Are Folmarv/Loffrey's break threats strong but answerable?
- Does Cletienne pressure turtling without becoming a hard-lock engine?
- Does the fight remain a pure boss rush, not a mob fight?
- Does the party enter Sanctuary taxed but still functional?

## Sources

- Game8, "Mullonde Cathedral Nave Walkthrough (Battle 47)": public roster, win-on-one-falls behavior,
  three named bosses, Templar break pressure, caster pressure, and buried treasure.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553207
- Final Fantasy Wiki, "Folmarv Tengille" / "Loffrey Wodring" / "Cletienne Duroi": story context.
  https://finalfantasy.fandom.com/wiki/Folmarv_Tengille
- Local: `037-chapter-4-overview.md`, `051-mullonde-exterior.md`, `053-mullonde-sanctuary.md`,
  `chapter-4-rewards-implementation.md`, `spoils-of-war-reward-system.md`.
