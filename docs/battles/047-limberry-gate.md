# 047 - Limberry Castle Gate

Status: 📝 redesign v2 planned (docs-only) — v1 implementation exists for entry 454
Chapter: 4 — "In the Name of Love"
Battle order: Battle 42 (Limberry chain 1 of 3 — NO resupply between 42→43→44)
Target version: Enhanced v1.5.0
ENTD: global entry **454** (local 70, entd4)
File: `battle_entd4_ent.bin`

## Current Implementation (v1, entry 454)

```text
DATA (verified from entd4 dump):
  slot 0 = Celia  (job 45 Assassin, name_id 45)  eq=254 (fixed boss gear, no editable equip slots)
  slot 1 = Lettie (job 46 Assassin, name_id 46)  eq=254
  slots 2-5 = Reaver (job 150 monster, lvl 254 runtime, eq=255) -- the 4 demon escort

CHANGE (faithful, minimal):
  Celia/Lettie = 104 (boss-tier chain opener)
  4 Reavers = 103
  flee-on-critical trigger, teleport mobility, status kit, Ultima behavior, and scripting tail preserved.
```

Planned v2 redesign (docs-only in this pass): keep the fixed Assassin boss kits and the 4-Reaver
escort. Do not plan normal equipment/secondary setup for Celia/Lettie because their slots are fixed.
The design target is the flee race and chain tax, not gear editing.

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `037-chapter-4-overview.md`. LIMBERRY CHAIN: 42 (`047`) → 43 (`048`) → 44 (`049`), one loadout.

## Design Goal

```text
Make Limberry Gate a dangerous but bounded chain opener: burst one teleporting Assassin to critical
before status and Ultima drain too many resources, while Reavers create body pressure. Preserve the
status-immunity vs Ultima tradeoff and flee trigger; do not add drops, extra bodies, or hard locks.
```

No active guests appear here. No guest-control implementation is needed for this battle.

## Original Battle

Objective:

```text
Defeat all enemies!   (but the battle ENDS when ONE Assassin is reduced to CRITICAL — they flee)
```

Player deployment:

```text
Up to 5 units, including Ramza. No guests. NO outfitter access (chain 1/3).
```

Original enemy composition:

```text
Celia     (Assassin — fixed boss kit; teleport, status, Ultima; flees on critical)
Lettie    (Assassin — fixed boss kit; teleport, status, Ultima; flees on critical)
4x Reaver (demon monster bodies)
```

Design reading:

Limberry Gate is **the assassin flee-race**, now placed at the front of a three-battle no-resupply
chain. It reprises the Ch3 Roof logic: the player does not need to kill both assassins, only push one
to critical. The pressure is the tradeoff between status protection and Ultima. Full status immunity is
not a free answer if it biases the assassins toward Ultima; no immunity is dangerous because Charm,
Stop, Stone, Toad, and death-style effects can break tempo. The intended answer is a balanced chain
loadout: enough resistance and cleanse to keep acting, enough burst to force one flee, and enough
resource discipline to enter the Keep.

## Local Data Confirmed / Data Still Needed

```text
CONFIRMED:
- Entry 454 is Limberry Gate.
- Celia and Lettie are fixed-kit Assassin boss slots with eq=254.
- Slots 2-5 are Reaver monsters.
- Flee-on-critical scripting is the fight shape.
- No active guest.
- Reward ledger maps Limberry Gate to no equipment reward because the assassins flee.

STILL NEEDED FOR V2 IMPLEMENTATION:
- Confirm exact Reaver display/innate behavior in installed data.
- Confirm flee-on-critical transition into Keep remains untouched.
- Confirm Ultima/status targeting bias still works after any future tuning.
- Preserve buried map treasure as vanilla map loot.
```

## Enemy Party Escalation (Chapter 4 rule)

```text
CHANGE: NO new caste and no editable gear plan. The escalation is fixed-kit Celia/Lettie at 104 with
  the status-vs-Ultima tradeoff intact, plus four Reavers at 103.
WHY: the fight's identity is "burst one teleporting assassin to critical before the chain opener taxes
  too many resources." Extra enemies, overleveling, or hard-status spam would turn a race into a slog.
CONSTRAINTS:
  - Flee-on-critical must remain.
  - Gate has no equipment reward.
  - Status must be resistable/cleansable and not spammed into a lock.
  - Ultima must be telegraphed/spaceable and chain-budgeted.
  - Reavers pressure the front but must not become cleanup tax.
WHAT IS NOT CHANGED: teleport mobility, Assassin fixed kits, Reaver escort, no-resupply chain context.
```

## Sanctioned Exceptions (carried precedents)

```text
ASSASSIN STATUS / INSTANT-DEATH PRESSURE — allowed as identity, but resistable + non-spam + telegraphed.
ULTIMA TRADEOFF — allowed because it is the build puzzle; status immunity should not trivialize the map.
FLEE-ON-CRITICAL — preserved; retreat means no equipment drop here.
FIXED BOSS KITS — active human completeness is constrained by eq=254 slots; do not invent normal gear.
REAVER DEMON ADDS — monster bodies; set level/position only unless future data proves safe edits.
```

## Rare/reward handling

```text
None. Limberry Gate carries no equipment reward by design.
Celia and Lettie flee on critical, so rewards are deferred to later Limberry outcomes.
Masamune/Genji/Chirijiraden belong to Elmdor at the Keep (`048`), not here.
Buried map treasure stays vanilla map loot.
```

## Proposed Composition (New Game++ Limberry Gate v2)

Keep the count (6) and the fixed-kit flee-race shape. Assassins `104`; Reavers `103`.

| Slot | Role | Unit type | Level | Br/Fa | Purpose |
| ------ | ------ | ----------- | ------- | --- | --------- |
| 0 | Celia | Assassin fixed boss kit | `104` | `92/90` | Teleport status/Ultima threat; flee target. |
| 1 | Lettie | Assassin fixed boss kit | `104` | `92/90` | Second teleport status/Ultima threat; flee target. |
| 2 | Reaver | Demon monster | `103` | `88/76` | Front pressure while assassins teleport. |
| 3 | Reaver | Demon monster | `103` | `88/76` | Second front pressure body. |
| 4 | Reaver | Demon monster | `103` | `88/76` | Flank/body pressure. |
| 5 | Reaver | Demon monster | `103` | `88/76` | Screen and chain-tax body. |

Rejected variants:

```text
- Editable gear assassins: eq=254 fixed boss kits make normal gear/secondary planning invalid.
- Hard-status assassin lock: turns the race into lost turns.
- Extra Reaver escort: creates cleanup/chain tax before Keep.
- Overlevelled opener: spends the chain's spike budget too early.
- No Ultima tradeoff: removes the build puzzle.
- Rewarded Gate: contradicts flee/no-drop policy and reward ledger.
```

## Builds

```text
Celia/Lettie:
- Fixed Assassin boss kits; do not assign normal equipment.
- Preserve teleport mobility, status kit, Ultima behavior, and flee-on-critical scripting.
- Keep ability behavior resistable/cleansable/telegraphed; no unavoidable lock.

Reavers:
- Monster bodies; no normal equipment.
- Set level/position only unless future data work proves safe monster edits.
```

## Positioning Plan

```text
Castle gate: Reavers begin forward to create body pressure. Celia and Lettie begin spread so teleport
angles threaten the back line, but Ultima remains telegraphed and spaceable.

The player should see the answer quickly:
  1. Pick one Assassin.
  2. Commit burst until critical.
  3. Spend enough cleanse/resist to keep acting, but conserve resources for Keep and Undercroft.
```

The gate should say: "two knives open Limberry's chain — push one to the brink fast, or pay for every
turn you spend here."

## Simulation Plan and Results

Simulation artifact:

```text
tmp/fft-level-design-047-limberry-gate/
  assumptions.md
  simulate.py
  iteration-results.json
  iteration-results.md
```

Model scope:

```text
Coarse deterministic flee-race and chain-tax model over the first five rounds.
It scores pressure, race clarity, answerability, chain tax, status-lock risk, reward correctness, and
scripting fidelity. It does not simulate exact FFT formulas.
```

Result summary:

| Candidate | Pressure | Race clarity | Answer | Chain tax | Status lock | Reward | Scripting | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| v2 fixed-kit flee race | 204 | 96 | 90 | 48 | 12 | 100 | 100 | **Accepted** |
| editable gear assassins | 214 | 96 | 90 | 48 | 12 | 100 | 50 | Rejected: fixed-kit violation |
| hard-status assassin lock | 266 | 78 | 60 | 76 | 67 | 100 | 100 | Rejected: hard lock |
| extra reaver escort | 218 | 74 | 76 | 66 | 12 | 100 | 100 | Rejected: chain-tax cleanup |
| overlevelled opener | 228 | 96 | 80 | 60 | 12 | 100 | 100 | Rejected: overlevel |
| no ultima tradeoff | 186 | 96 | 76 | 36 | 20 | 100 | 100 | Rejected: loses build puzzle |
| rewarded gate | 204 | 96 | 90 | 48 | 12 | 30 | 100 | Rejected: no-drop violation |

Iteration decision:

```text
ACCEPT v2 fixed-kit flee race.
Keep the fixed boss kits and race scripting. The fight should tax the chain through status/Ultima
pressure, not through extra cleanup, fake gear setup, or unavoidable lockdown.
```

## Implementation Checklist

- [ ] Confirm entry 454 slot order: Celia, Lettie, four Reavers.
- [ ] Preserve flee-on-critical trigger and transition to Keep.
- [ ] Keep Celia/Lettie at `104`; Reavers at `103`.
- [ ] Preserve Assassin fixed kits (`eq=254`) and do not assign normal gear.
- [ ] Keep status resistable/cleansable/non-spam; keep Ultima telegraphed/spaceable.
- [ ] Preserve status-immunity vs Ultima tradeoff.
- [ ] Preserve no equipment reward; preserve buried map treasure.
- [ ] Test as Limberry chain 1/3 with resources carried into `048` and `049`.

## Test Questions

- Does one Assassin reaching critical end the fight reliably?
- Can a prepared party win without blanket immunity and without being hard-locked?
- Does blanket status immunity increase Ultima pressure enough to remain a real tradeoff?
- Do Reavers pressure without forcing a cleanup slog before Keep?
- Does the fight award no equipment and transition cleanly to `048`?
- Is chain tax meaningful but not crippling before the Elmdor and Zalera fights?

## Sources

- Game8, "Limberry Castle Gate Walkthrough (Battle 42)": roster, flee-on-critical, status/Ultima
  behavior, chain context, and map treasure.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553202
- Final Fantasy Wiki, "Celia and Lettie" / "Limberry Castle": story/terrain context.
  https://finalfantasy.fandom.com/wiki/Celia_and_Lettie
- Local: `037-chapter-4-overview.md`, `035-riovanes-castle-roof.md`,
  `048-limberry-keep.md`, `049-limberry-undercroft.md`, `chapter-4-rewards-implementation.md`.
