# 047 - Limberry Castle Gate

Status: 🧪 v3 implemented — deploy and direct in-game playtest pending
Chapter: 4 — "In the Name of Love"
Battle order: Battle 42 (Limberry chain 1 of 3 — NO resupply between 42→43→44)
Target version: Enhanced v1.5.0
ENTD: global entry **454** (local 70, entd4)
File: `battle_entd4_ent.bin`

## Current Implementation (v3, entry 454)

```text
DATA (verified from entd4 dump):
  slot 0 = Celia  (job 45 Assassin, name_id 45)  L102; dual Masamune
  slot 1 = Lettie (job 46 Assassin, name_id 46)  L102; Koga Blade + Iga Blade
  slots 2-5 = Reaver (job 150 monster, lvl 254 runtime, eq=255) -- the 4 demon escort

CHANGE (faithful, minimal):
  Celia/Lettie = 102 (the only +2 anchors)
  4 Reavers = 101/101/100/100
  flee-on-critical trigger, teleport mobility, status kit, Ultima behavior, and scripting tail preserved.
```

Implemented v3 redesign: keep the v2 Assassin flee race and 4-Reaver escort, but explicitly write only
the two weapon fields. Celia's Assassin job legally equips Katanas and has innate Dual Wield; Lettie's
legally equips Ninja Blades and has innate Dual Wield. Fixed armor/accessory and all scripted behavior
remain untouched.

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
- Celia and Lettie are fixed-kit Assassin boss slots, but their RH/LH fields accept explicit legal weapons.
- Slots 2-5 are Reaver monsters.
- Flee-on-critical scripting is the fight shape.
- No active guest.
- Reward ledger maps Limberry Gate to no equipment reward because the assassins flee.

V3 IMPLEMENTATION CONFIRMED:
- JobData confirms Celia job 45 equips Katana and Lettie job 46 equips NinjaBlade.
- Both Assassin jobs have innate Dual Wield (`477`).
- OverrideEntryData leaves RH/LH and Level unset, so entry 454 is authoritative.
- Only levels and the two Assassin hand fields were changed; flags, positions, job kits and scripting remain.

STILL NEEDED IN GAME:
- Confirm exact Reaver display/innate behavior in installed data.
- Confirm flee-on-critical transition into Keep remains untouched.
- Confirm Ultima/status targeting bias still works after any future tuning.
- Preserve buried map treasure as vanilla map loot.
```

## Enemy Party Escalation (Chapter 4 rule)

```text
CHANGE: keep the v2 race, give Celia dual Masamune and Lettie Koga + Iga, and use the low level band:
  Assassins `102`, Reavers `101/101/100/100`.
WHY: the fight's identity is "burst one teleporting assassin to critical before the chain opener taxes
  too many resources." Extra enemies, overleveling, or hard-status spam would turn a race into a slog.
CONSTRAINTS:
  - Flee-on-critical must remain.
  - Gate has no equipment reward.
  - Status must be resistable/cleansable and not spammed into a lock.
  - Ultima must be telegraphed/spaceable and chain-budgeted.
  - Reavers pressure the front but must not become cleanup tax.
WHAT IS NOT CHANGED: teleport mobility, Assassin abilities/fixed armor, Reaver escort, no-resupply chain context.
```

## Sanctioned Exceptions (carried precedents)

```text
ASSASSIN STATUS / INSTANT-DEATH PRESSURE — allowed as identity, but resistable + non-spam + telegraphed.
ULTIMA TRADEOFF — allowed because it is the build puzzle; status immunity should not trivialize the map.
FLEE-ON-CRITICAL — preserved; retreat means no equipment drop here.
FIXED BOSS KITS — preserve fixed armor/accessory and abilities; v3 explicitly overrides only RH/LH.
REAVER DEMON ADDS — monster bodies; set level/position only unless future data proves safe edits.
```

## Rare/reward handling

```text
None. Limberry Gate carries no equipment reward by design.
Celia and Lettie flee on critical, so rewards are deferred to later Limberry outcomes.
The Gate weapons are active threat gear on fleeing units, not guaranteed spoils and not required rewards.
Elmdor's guaranteed Masamune/Genji/Chirijiraden payout remains at the Keep (`048`).
Buried map treasure stays vanilla map loot.
```

## Proposed Composition (New Game++ Limberry Gate v3)

Keep the count (6) and the fixed-kit flee-race shape. Assassins `102`; Reavers `101/101/100/100`.

| Slot | Role | Unit type | Level | Br/Fa | Purpose |
| ------ | ------ | ----------- | ------- | --- | --------- |
| 0 | Celia | Assassin fixed kit; dual Masamune | `102` | `92/90` | Teleport status/Ultima threat; flee target. |
| 1 | Lettie | Assassin fixed kit; Koga + Iga | `102` | `92/90` | Second teleport status/Ultima threat; flee target. |
| 2 | Reaver | Demon monster | `101` | `88/76` | Front pressure while assassins teleport. |
| 3 | Reaver | Demon monster | `101` | `88/76` | Second front pressure body. |
| 4 | Reaver | Demon monster | `100` | `88/76` | Flank/body pressure. |
| 5 | Reaver | Demon monster | `100` | `88/76` | Screen and chain-tax body. |

Rejected variants:

```text
- Full editable gear assassins: rejected; v3 changes weapons only and preserves fixed armor/accessory.
- Hard-status assassin lock: turns the race into lost turns.
- Extra Reaver escort: creates cleanup/chain tax before Keep.
- Overlevelled opener: spends the chain's spike budget too early.
- No Ultima tradeoff: removes the build puzzle.
- Rewarded Gate: contradicts flee/no-drop policy and reward ledger.
```

## Builds

```text
Celia:
- Fixed Assassin boss kit with innate Dual Wield.
- Right hand: Masamune. Left hand: Masamune.

Lettie:
- Fixed Assassin boss kit with innate Dual Wield.
- Right hand: Koga Blade. Left hand: Iga Blade.

Both:
- Preserve fixed head/body/accessory.
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
Keep the accepted v2 flee race and apply only the documented v3 weapon overrides plus the low-band level
rule. No new simulation was requested; direct playtest must confirm the explicit weapons appear and the
race remains bounded.
```

## Implementation Checklist

- [x] Confirm entry 454 slot order: Celia, Lettie, four Reavers.
- [x] Preserve flee-on-critical trigger and transition to Keep by leaving scripts and control data untouched.
- [x] Set Celia/Lettie to `102`; Reavers to `101/101/100/100`.
- [x] Give Celia Masamune + Masamune; preserve fixed head/body/accessory.
- [x] Give Lettie Koga Blade + Iga Blade; preserve fixed head/body/accessory.
- [ ] Keep status resistable/cleansable/non-spam; keep Ultima telegraphed/spaceable.
- [ ] Preserve status-immunity vs Ultima tradeoff.
- [x] Preserve no equipment reward; preserve buried map treasure.
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
