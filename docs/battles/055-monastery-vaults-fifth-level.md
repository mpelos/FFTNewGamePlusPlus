# 055 - Monastery Vaults, Fifth Level (Orbonne descent / Murond Death City)

Status: redesign v2 planned (documentation only; v1 implementation exists for entry 436)
Chapter: 4 - "In the Name of Love"
Battle order: Battle 50 (ENDGAME GAUNTLET 2 of 5 - no resupply across 054 -> 055 -> 056 -> 057 -> 058)
Target version: Enhanced v1.5.0
ENTD: global entry **436** (entd4)
File: `battle_entd4_ent.bin`

> Final-gauntlet reward rule: no usable NG++ reward is added inside battles `054`-`058`. Escutcheon was
> moved to the Nave reward set (`052`) before the point of no return. This battle keeps standard/vanilla
> rewards and buried Elixirs only. See `chapter-4-rewards-implementation.md`.

## Current Implementation (v1, entry 436)

```text
DATA (resolved in-game; see ENDGAME-BLOCKER.md):
  slot 0 = Loffrey (job 37)
           -> active Divine Knight boss; fights and dies here.
  active support = 2 Black Mage + 2 Summoner + 1 Time Mage.

CHANGE (v1 already implemented):
  Loffrey and the caster screen scaled as final-gauntlet battle 2/5.
  Defeat-Loffrey objective and caster crossfire preserved.
  Standard loot / buried Elixirs only under current reward policy.
```

Current dump:

| Slot | Status | Job | Level | JL | Secondary | Reaction | Support | Move | Equipment ids | Notes |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| 0 | Active boss | 37 | 105 | 8 | 61 | 447 | 466 | 492 | 154,182,210,34,139 | Loffrey. Item `34` is Save the Queen and must be swapped/avoided in v2. |
| 1 | Active | 80 | 104 | 8 | 0 | 449 | 465 | 486 | 167,206,234,56,255 | Black Mage; v2 target level `103`. |
| 2 | Active | 80 | 104 | 8 | 0 | 449 | 465 | 486 | 167,206,234,56,255 | Black Mage; v2 target level `103`. |
| 3 | Active | 82 | 104 | 8 | 0 | 449 | 465 | 486 | 167,206,234,56,255 | Summoner; v2 target level `103`. |
| 4 | Active | 81 | 104 | 8 | 0 | 449 | 510 | 486 | 167,206,234,56,255 | Time Mage; v2 needs intentional support. |
| 5 | Active | 82 | 104 | 8 | 0 | 449 | 465 | 486 | 167,206,234,56,255 | Summoner; v2 target level `103`. |

Planned v2 redesign (docs-only in this pass): keep the caster-crossfire boss race, but remove outdated
reward assumptions. Loffrey is still the objective and still dies here; he just no longer pays Escutcheon
inside the no-resupply gauntlet.

## Design Goal

```text
Make Vaults 5th a disperse-disarm-burst test: cross a wide caster killzone, answer Slow, disarm or
endure Loffrey's one equipment-break source, and defeat him before the caster screen drains the gauntlet.
No usable reward is added here.
```

No active guests appear here. No guest-control implementation is needed for this battle.

## Original Battle

Objective:

```text
Defeat Loffrey!   (the battle ends when Loffrey falls; casters are optional)
```

Player deployment:

```text
Up to 5 units, including Ramza. No outfitter access (gauntlet 2/5).
```

Original enemy composition:

```text
Loffrey Wodring   (Divine Knight; equipment-break boss)
2x Black Mage      (heavy AoE magic)
2x Summoner        (summon AoE)
1x Time Mage       (Slow / tempo pressure)
```

Design reading:

Vaults 5th is **the wide-field caster crossfire**. Unlike the light opener, this fight should force
real resource decisions: spread against AoE, decide whether to pressure casters or rush Loffrey, and
avoid losing gear to one Divine Knight break source. The battle ends on Loffrey, so full cleanup is the
wrong read.

What must stay recognizable:

```text
- Loffrey is active and is the objective.
- One equipment-break boss source.
- 2 Black Mages + 2 Summoners + 1 Time Mage create the crossfire.
- Charge times and spacing are counterplay.
- Slow is soft tempo pressure, not hard lock.
- No usable NG++ reward inside the gauntlet.
```

## Local Data Confirmed / Data Still Needed

```text
CONFIRMED:
- Entry 436 is Vaults 5th.
- Loffrey fights and dies here.
- Active support roster is 2 Black Mage, 2 Summoner, 1 Time Mage.
- Win condition is "Defeat Loffrey".
- Escutcheon is no longer awarded here under the current reward ledger.
- Current v1 caster levels are `104`; v2 intentionally documents `103` to keep chain tax below the
  gauntlet 3/5 threshold.
- Current v1 Loffrey still carries item `34` (Save the Queen), which duplicates Bervenia and must be
  removed/avoided during v2 implementation.
- Current v1 Time Mage support is `510`; v2 needs an intentional complete support slot.

STILL NEEDED FOR V2 IMPLEMENTATION:
- Confirm Loffrey has exactly one functional equipment-break source.
- Confirm caster charge times remain intact.
- Confirm Time Mage pressure is Slow/Haste-style soft tempo, not Stop/Don't Act.
- Preserve standard loot and buried Elixirs only.
```

## Enemy Party Escalation (Chapter 4 rule)

```text
CHANGE: Keep Loffrey + the exact caster screen:
  - Loffrey 105 as the one break boss and objective.
  - 2 Black Mages 103.
  - 2 Summoners 103.
  - 1 Time Mage 103.
WHY: the fight's identity is crossing a wide AoE field to reach a disarmable boss. Extra bodies, extra
  break sources, or instant-cast magic turn it into tax instead of a readable crossfire puzzle.
CONSTRAINTS:
  - Equipment break is one source.
  - Caster AoE keeps charge-time counterplay.
  - Slow is soft and cleansable/resistable.
  - Defeating Loffrey ends the battle.
  - No usable rewards in 054-058.
WHAT IS NOT CHANGED: wide-field layout, caster-crossfire identity, Loffrey objective, and no-resupply
  gauntlet context.
```

## Sanctioned Exceptions (carried precedents)

```text
UNYIELDING BLADE / EQUIPMENT BREAK — allowed on Loffrey only. Steal/disarm, Rend/Crush, Safeguard, and
  burst answer it.
CASTER CROSSFIRE — allowed as the fight's core. Charge times and spacing remain the counterplay.
TIME MAGIC SLOW — allowed as one soft disruptor. No Stop, Don't Act, or hard turn deletion.
NO-REWARD GAUNTLET RULE — enforced even though Loffrey dies here.
```

## Rare/reward handling

```text
None. No usable NG++ reward is added inside the final gauntlet.
Escutcheon is already paid at `052`.
Do not duplicate Save the Queen or place Tier-S gear here.
Keep standard/vanilla loot and buried Elixirs only.
```

## Proposed Composition (New Game++ Vaults Fifth Level v2)

Keep six active enemies. Loffrey `105`; casters `103`.

| Slot | Role | Unit type | Level | Br/Fa | Purpose |
| ------ | ------ | ----------- | ------- | --- | --------- |
| 0 | Boss objective | Loffrey, Divine Knight | `105` | `90/55` | One break source; disarm/burst target. |
| 1 | AoE caster | Black Mage | `103` | `60/84` | Heavy magic from one flank. |
| 2 | AoE caster | Black Mage | `103` | `60/84` | Second Black Mage; crossfire pressure. |
| 3 | AoE caster | Summoner | `103` | `60/84` | Summon AoE with charge-time counterplay. |
| 4 | AoE caster | Summoner | `103` | `60/84` | Second summon line; widens killzone. |
| 5 | Tempo caster | Time Mage | `103` | `62/80` | Slow/Haste-style tempo pressure; no hard lock. |

Rejected variants:

```text
- Usable Escutcheon gauntlet reward: outdated and violates current policy.
- Save the Queen duplicate: duplicates Bervenia's story reward.
- Double-break Loffrey wall: too much gear loss pressure.
- Hard Time lock: turns Slow into turn denial.
- Instant-cast AoE crossfire: removes charge-time counterplay.
- Kill-all caster cleanup: contradicts objective and adds tax.
- Underpowered caster screen: fails to make the wide field matter.
- Overlevelled caster gauntlet: too high for battle 2/5.
```

## Builds

```text
Loffrey:
- Level 105, JobLevel 8.
- One equipment-break source only.
- Use a strong non-unique sword/shield setup; do not duplicate Save the Queen or add Tier-S gear.
- Defensive reaction, Defense Boost/Attack Boost, Move +1/+2.

Black Mages:
- Level 103, JobLevel 8.
- Heavy Black Magic with intact charge times.
- Complete caster gear, defensive reaction, MA support, Move +1.

Summoners:
- Level 103, JobLevel 8.
- Summon AoE with intact charge times.
- Complete caster gear, defensive reaction, MA support, Move +1.

Time Mage:
- Level 103, JobLevel 8.
- Haste/Slow/Float style tempo only.
- No Stop, Don't Act, Death, or hard control.
- Complete caster gear, defensive reaction, MA support, Move +1.
```

## Positioning Plan

```text
Wide vault floor: Loffrey starts forward/center as the visible objective. Black Mages and Summoners
spread to flanks/back so clumping is punished. Time Mage sits mid-back to slow an overcommitted rush.
The player should spread, choose a lane, disarm or burst Loffrey, and avoid full caster cleanup.
```

The vault floor should say: "the casters own the open ground; scatter through the fire, strip Loffrey's
blade if needed, and end the fight before the crossfire drains the run."

## Simulation Plan and Results

Simulation artifact:

```text
tmp/fft-level-design-055-vaults-fifth/
  assumptions.md
  simulate.py
  iteration-results.json
  iteration-results.md
```

Model scope:

```text
Coarse deterministic no-reward caster-crossfire boss-race model. It scores crossfire pressure, disarm
answerability, control risk, focus clarity, chain tax, reward legality, and identity fidelity.
```

Result summary:

| Candidate | Crossfire | Disarm answer | Control | Focus | Chain tax | Reward | Identity | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| v2 no-reward caster crossfire boss race | 114 | 100 | 18 | 94 | 51.6 | 100 | 100 | **Accepted** |
| usable Escutcheon gauntlet reward | 114 | 94 | 18 | 94 | 51.6 | 30 | 100 | Rejected |
| Save the Queen duplicate | 114 | 94 | 18 | 94 | 51.6 | 75 | 100 | Rejected |
| double-break Loffrey wall | 114 | 44 | 18 | 94 | 61.6 | 100 | 100 | Rejected |
| hard Time lock | 114 | 86 | 80 | 82 | 67.1 | 100 | 82 | Rejected |
| instant-cast AoE crossfire | 142 | 86 | 18 | 94 | 55.8 | 100 | 100 | Rejected |
| kill-all caster cleanup | 114 | 86 | 18 | 56 | 66.6 | 100 | 75 | Rejected |
| underpowered caster screen | 80 | 78 | 14 | 94 | 45.5 | 100 | 82 | Rejected |
| overlevelled caster gauntlet | 122 | 94 | 22 | 94 | 53.8 | 100 | 100 | Rejected |

Iteration decision:

```text
ACCEPT v2 no-reward caster crossfire boss race.
The fight is hard because of spacing, charge-time pressure, Slow, and one disarmable boss source, not
because it deletes turns or gives unusable late rewards.
```

## Implementation Checklist

- [ ] Confirm entry 436 slot order.
- [ ] Preserve win condition: `Defeat Loffrey`.
- [ ] Keep Loffrey at `105`; casters at `103`.
- [ ] Keep exactly one functional equipment-break source.
- [ ] Remove/avoid Save the Queen duplication.
- [ ] Keep caster charge times intact.
- [ ] Keep Time Mage to Haste/Slow/Float only; no hard control.
- [ ] Preserve standard loot and buried Elixirs only; no usable NG++ reward.
- [ ] Test as gauntlet 2/5 with resources carried into 056-058.

## Test Questions

- Does defeating Loffrey end the battle immediately?
- Is Loffrey one disarmable break source, not a gear-lock wall?
- Does the caster screen force spreading while preserving charge-time counterplay?
- Is Slow soft and recoverable?
- Are no usable NG++ rewards added?
- Is the party taxed but still ready for Necrohol, Lost Halidom, and Airship?

## Sources

- Local: `ENDGAME-BLOCKER.md` (authoritative entry 436), `037-chapter-4-overview.md`,
  `059-chapter-4-balance-review.md`, `chapter-4-rewards-implementation.md`.
- Game8, "Monastery Vaults: Fifth Level Walkthrough (Battle 50)": roster, objective, wide field,
  caster crossfire, Slow/disarm advice, and buried Elixirs.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553226
