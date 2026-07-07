# 043a - Fort Besselat: South Wall (Bethla Garrison)

Status: 📝 redesign v2 planned (docs-only) — v1 implementation exists for entry 448
Chapter: 4 — "In the Name of Love"
Battle order: Battle 38A (South Wall — mutually exclusive with `043b`)
Target version: Enhanced v1.5.0
ENTD: global entry **448** (South) — `battle_entd4_ent.bin` local 64
File: `battle_entd4_ent.bin` (embedded NG+ swap) — `tools/battle_patch.py besselat_wall`

> **NG++ reward applied (2026-06-27):** Yoichi Bow + Perseus Bow on the Archer slots of BOTH path entries
> (448 s3/s4, 449 s0/s3), so either route awards them. Guaranteed Spoils of War (ENTD 0x1e), NG+ only,
> within the 3-cap, no steal needed. Canonical map: `chapter-4-rewards-implementation.md`.

Current implementation (entry 448, vanilla-dump verified):
- s0,s1 Knight L102 + s2 Knight L101 — Heavy gear/Runeblade/Shield, Rend innate.
- s3 Archer L102, s4 Archer L101 — Windslash bow pressure.
- s5 Ninja L102 — dual Longblade.
- s6 Thief L101 — Air Knife.
- No boss / no named boss rare; low Ch4 band (101-102). Map treasure (other layer) untouched.

Planned v2 redesign (docs-only in this pass): keep the South melee/stealth roster, but make every
active human a complete Chapter-4 unit. Yoichi/Perseus may be visible on the Archer roles here because
the reward pair is duplicated in `043b` for route parity.

## Design Goal

```text
Make South Wall the melee/stealth branch of Fort Besselat: the player cracks a Knight wall on narrow
vertical terrain while a Ninja and Thief pressure exposed flanks. The route should feel distinct from
North's ranged/AoE branch and clearly below the Sluice spike.
```

No active guests appear here. No guest-control implementation is needed.

## Original Battle

Objective:

```text
Defeat all enemies!
```

Player deployment:

```text
Up to 5 units, including Ramza. No guests.
```

Original South composition (verified via Game8, Battle 38A):

```text
3x Knight    (front-line wall of bodies)
2x Archer    (ranged chip from the parapets)
1x Thief     (steal / fast flank)
1x Ninja     (dual-wield wall-climber / Throw)
```

Vanilla comparison:

```text
- Enemy count and jobs are unchanged from vanilla South: 3 Knights + 2 Archers + 1 Thief + 1 Ninja.
- Objective is unchanged: defeat all enemies.
- The difference is completeness: all active humans get Chapter-4-level gear and full ability slots.
- Knight Rend is capped at two of the three Knights; the third Knight remains a bodyguard without Rend.
- Yoichi Bow + Perseus Bow remain guaranteed route-parity rewards; visible Archer bows are optional
  pressure, never steal-gated rewards.
```

## Local Data Confirmed / Data Still Needed

```text
CONFIRMED:
- Entry 448 is the Fort Besselat South Wall ENTD entry.
- South roster: 3 Knight + 2 Archer + 1 Ninja + 1 Thief.
- The player fights either this branch or North (`043b`), never both.
- No active guest, no boss.
- Reward ledger duplicates Yoichi Bow + Perseus Bow across both entries so either route pays the same
  guaranteed spoils.

STILL NEEDED FOR V2 IMPLEMENTATION:
- Confirm exact slot order before patching complete v2 kits.
- Confirm objective remains "Defeat all enemies".
- Confirm whether OverrideEntryData carries level for this battle or leaves levels at runtime scale.
- Preserve vertical wall / narrow-path geometry and branch scripting.
- Preserve map treasure as vanilla map loot.
```

Job IDs (carry over known, verify the rest in-game):

```text
77 = Archer            (confirmed)
83 = Thief             (confirmed)
Knight job id          (TBD - verify)
Ninja job id           (TBD - verify; Ch3 debut, 031)
```

## Enemy Party Escalation (Chapter 4 rule)

```text
CHANGE: no new caste added. South becomes a complete melee/stealth wall team: Knights hold the ramp,
  Archers tax the parapet lanes, and Ninja/Thief exploit the vertical edges.
WHY: South's identity is "crack the wall while covering your flanks." The faithful Ch4 move is to make
  the same defenders fully built and let the wall matter more, not to add a boss or a second engine.
CONSTRAINTS: Ninja Throw = ranged damage, not a lock; Thief steal/charm = minor harass, no hard lock;
  Knight Rend <=2 sources (South has 3 Knights, so at most 2 learn/use Rend).
REJECTED DEFAULTS: no third Rend Knight, no hard-status flankers, no 103+ overlevel spike, no one-sided
  rewards. Branch parity matters because the player chooses only one path.
WHAT IS NOT CHANGED: South's roster, the "defeat all" objective, and wall/chokepoint geometry remain.
```

## Rare/reward handling

```text
Guaranteed spoils for entry 448: YOICHI BOW + PERSEUS BOW.
These are duplicated on North entry 449 because the player fights only one path.
The player must never be forced to pick a route or Steal to receive the reward pair.
PRESERVE: South map treasure (Circlet, Platinum Sword) remains existing map loot, not the NG++ reward
channel.
```

## Proposed Composition (New Game++ South Wall v2)

Keep the local roster and the boss-less wall-skirmish feel. No `103`+ spike.

| Slot | Role | Job | Level | Br/Fa | Purpose |
| ------ | ------ | ----- | ------- | --- | --------- |
| n | Knight | Knight | `102` | `88/42` | Wall of bodies; Rend source 1. |
| n | Knight | Knight | `102` | `88/42` | Second body; Rend source 2 — cap reached. |
| n | Knight | Knight | `101` | `88/42` | Third body; no Rend, holds the chokepoint. |
| n | Bow Archer | Archer | `102` | `82/45` | Yoichi/Perseus visible bow pressure from the parapet. |
| n | Bow Archer | Archer | `101` | `82/45` | Second bow reward carrier; covers the ramp. |
| n | Thief Flanker | Thief | `101` | `88/38` | Fast flank / steal harass using the walls; no hard status. |
| n | Ninja Flanker | Ninja | `102` | `90/35` | Wall-climbing dual-wield / Throw — the South signature. |

Reasoning:

South remains a melee/stealth crack-the-wall problem. The player must break through three front-line
bodies while not letting the Ninja and Thief wrap the backline. Archer pressure is visible and
route-parity-safe, but the reward still pays through spoils.

## Builds

### Knight x3 (Lv 102/102/101)

```text
Job: Knight (id TBD)   JobLevel: 8   Primary: basic + Rend (ONLY 2 of 3 — cap)
Secondary: Item, limited to Potion/Hi-Potion/Remedy style stabilization; no Phoenix Down/Elixir.
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head: shop helm (id TBD)   Body: shop heavy armor (id TBD)   Accessory: Bracers (218)
Right hand: shop knight sword (id TBD)   Left: shop shield (id TBD)
```

Third Knight rule:

```text
The Lv101 bodyguard Knight has complete equipment/reaction/support/movement but NO Rend enabled.
His job is body-blocking, Item cleanup, and holding the chokepoint.
```

### Ninja (Lv 102) / Thief (Lv 101)

```text
Ninja: (id TBD)   JobLevel: 8   Secondary: Throw   Reaction: First Strike (453)   Support: Attack Boost (465)
  Movement: Movement +2 (487)   Head: Thief's Cap (168)   Body: Black Garb (198)
  Accessory: Germinas Boots (210)   Hands: shop ninja blade x2 (dual-wield)
Thief (83): JobLevel: 8   Secondary: Steal   Reaction: First Strike (453)   Support: Attack Boost (465)
  Movement: Movement +2 (487)   Head: Thief's Cap (168)   Body: Black Garb (198)
  Accessory: Germinas Boots (210)   Right: Air Knife (9)
```

### Archer x2 (Lv 102/101)

```text
Job: Archer (77)   JobLevel: 8   Secondary: Item, limited to Potion/Remedy style utility.
Reaction: Reflexes (449)   Support: Concentration (469)
  Movement: Movement +1 (486)   Head: Thief's Cap (168)   Body: Black Garb (198)
  Accessory: Bracers (218)   Right: Yoichi/Perseus or shop high-tier bow per slot/reward plan
```

Role: visible bow pressure from the wall. Rewards still pay via guaranteed spoils; Steal is optional.

## Positioning Plan

```text
South: the 3 Knights hold the ramp, the 2 Archers sit on the parapet above, and the Ninja/Thief start
  wide to use the wall edges and flank.
Preserve the narrow paths + height; do NOT flatten or widen the wall.
Modest levels — one of two converging skirmishes, not a spike.
```

## Simulation Plan and Results

Simulation artifact:

```text
tmp/fft-level-design-043a-fort-besselat-south-wall/
  assumptions.md
  simulate.py
  iteration-results.json
  iteration-results.md
```

Current result source: inherited from the former combined 043 branch-balance simulation. South accepted
as part of `v2 complete visible-bow branches`, with moderate pressure and route parity.

## Implementation Checklist

- [ ] Confirm entry 448 South slot order before patching complete kits.
- [ ] Keep objective = "Defeat all enemies" + the vertical wall / narrow-path geometry.
- [ ] Rend on <=2 Knights; third Knight has no Rend.
- [ ] Keep Ninja Throw/wall-climb + Thief steal as harassment, not hard control.
- [ ] Give every active human complete equipment plus secondary/reaction/support/movement.
- [ ] Preserve guaranteed spoils: Yoichi Bow + Perseus Bow on this branch.
- [ ] Set levels in the low Ch4 band (`101`-`102`, no `103`); JobLevel `8` on all active slots.
- [ ] Patch entry 448 via the correct layer; keep the diff inside the South Wall window.
- [ ] Test this path from a New Game+ save and confirm South = melee/stealth wall assault.

## Test Questions

- Does South still feel like the melee/stealth branch, distinct from North?
- Can the player crack the Knight wall without being enveloped by the Ninja/Thief flank?
- Is Rend capped at two sources and answerable with Safeguard/Steal/burst?
- Are active bow carriers strong but still below Sluice pressure?
- Does the route pay Yoichi Bow + Perseus Bow equivalently to North?

## Sources

- Game8, "Fort Besselat: South Wall (Battle 38A)": roster, objective, terrain, rewards.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553198
- Local: `037-chapter-4-overview.md`, `043b-fort-besselat-north-wall.md`,
  `031-walled-city-yardrow.md`, `044-fort-besselat-sluice.md`,
  `chapter-4-rewards-implementation.md`, and `tmp/fft-level-design-043a-fort-besselat-south-wall/`.
