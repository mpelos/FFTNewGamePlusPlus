# 043a - Fort Besselat: South Wall (Bethla Garrison)

Status: 📝 redesign v3 planned (docs-only) — v1 implementation exists for entry 448
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

Planned v3 redesign (docs-only in this pass): keep the South melee/stealth wall identity, but turn the
front line into a stronger Chapter-4 assault: a Holy-Knight-style leader anchors the chokepoint while
two Samurai-bucket wall units cover the ramp with elite crossbow pressure. The two vanilla Archer slots
become Black Mage gun-casters, adding long-range magical-gunner punishment from the parapets.

## Design Goal

```text
Make South Wall the melee/stealth branch of Fort Besselat: the player cracks a Knight wall on narrow
vertical terrain while a Ninja and Monk pressure exposed flanks. The route should feel distinct from
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
- Enemy count is unchanged from vanilla South: 3 former Knight slots + 2 former Archer slots + 1 Thief
  + 1 Ninja.
- Jobs are upgraded from vanilla: one Knight becomes a Holy-Knight-style leader if the data layer allows
  it, the two wall Knights become Samurai-bucket units, and the two Archers become Black Mages with guns.
- The vanilla Thief slot becomes a Monk flanker; the vanilla Ninja slot remains Ninja but changes into a
  Martial-Arts burst unit.
- Objective is unchanged: defeat all enemies.
- The difference is completeness: all active humans get Chapter-4-level gear and full ability slots.
- Rend is removed from the wall plan; the new pressure is a leader + two defensive Samurai-bucket shooters
  plus two Black Mage gun-casters.
- Yoichi Bow + Perseus Bow remain guaranteed route-parity rewards through spoils, not active Archer gear
  in this v3 setup.
```

## Local Data Confirmed / Data Still Needed

```text
CONFIRMED:
- Entry 448 is the Fort Besselat South Wall ENTD entry.
- Original South roster: 3 Knight + 2 Archer + 1 Ninja + 1 Thief.
- Planned v3 roster: Knight Leader + 2 Samurai-bucket walls + 2 Black Mage gun-casters + Monk + Ninja.
- The player fights either this branch or North (`043b`), never both.
- No active guest, no boss.
- Reward ledger duplicates Yoichi Bow + Perseus Bow across both entries so either route pays the same
  guaranteed spoils.

STILL NEEDED FOR V3 IMPLEMENTATION:
- Confirm exact slot order before patching complete v3 kits.
- Confirm objective remains "Defeat all enemies".
- Confirm whether OverrideEntryData carries level for this battle or leaves levels at runtime scale.
- Preserve vertical wall / narrow-path geometry and branch scripting.
- Preserve map treasure as vanilla map loot.
```

Job IDs (carry over known, verify the rest in-game):

```text
77 = Archer            (confirmed)
83 = Thief             (confirmed)
Monk job id            (TBD - verify)
Knight job id          (TBD - verify)
Ninja job id           (TBD - verify; Ch3 debut, 031)
```

## Enemy Party Escalation (Chapter 4 rule)

```text
CHANGE: South becomes a complete melee/stealth wall team with a stronger command unit: the Knight Leader
  holds the chokepoint, two Samurai-bucket wall units tax the ramp, Black Mage gun-casters punish exposed
  lanes from the parapets, and Ninja/Monk exploit the vertical edges.
WHY: South's identity is "crack the wall while covering your flanks." The faithful Ch4 move is to make
  the same defenders fully built and let the wall matter more, not to add a boss or a second engine.
CONSTRAINTS: Holy Knight bucket/secondary is "if possible" until implementation proves the data supports it;
  Samurai and Black Mage JobLevel 8 are mod-side job-bucket notes, not secondary JobLevel fields; Black
  Mage guns add range without adding a second spell-control engine; Monk/Ninja flanks are physical burst
  threats, not hard control.
REJECTED DEFAULTS: no Rend wall, no hard-status flankers, no 103+ overlevel spike, no one-sided
  rewards. Branch parity matters because the player chooses only one path.
WHAT IS NOT CHANGED: enemy count, the "defeat all" objective, and wall/chokepoint geometry remain.
```

## Rare/reward handling

```text
Guaranteed spoils for entry 448: YOICHI BOW + PERSEUS BOW.
These are duplicated on North entry 449 because the player fights only one path.
The player must never be forced to pick a route or Steal to receive the reward pair.
PRESERVE: South map treasure (Circlet, Platinum Sword) remains existing map loot, not the NG++ reward
channel.
```

## Proposed Composition (New Game++ South Wall v3)

Keep the local enemy count and the boss-less wall-skirmish feel. No `103`+ spike.

| Slot | Role | Job | Level | Br/Fa | Purpose |
| ------ | ------ | ----- | ------- | --- | --------- |
| n | Knight Leader | Holy Knight bucket, if possible | `101` | `88/42` | Chokepoint commander; Defender + Crystal Shield anchor. |
| n | Wall Samurai | Samurai bucket | `102` | `88/42` | Defensive crossbow wall; Dragon's Heart pressure sink. |
| n | Wall Samurai | Samurai bucket | `102` | `88/42` | Second defensive crossbow wall; mirrors the first. |
| n | Gun Black Mage | Black Mage bucket | `102` | `62/84` | Glacial Gun caster-gunner; long-range parapet pressure. |
| n | Gun Black Mage | Black Mage bucket | `101` | `62/84` | Blaster caster-gunner; second ranged pressure angle. |
| n | Monk Flanker | Monk bucket | `101` | `88/38` | Jump +3 physical flanker; Dual Wield burst threat. |
| n | Ninja Flanker | Ninja bucket | `102` | `90/35` | Jump +3 Martial Arts burst unit; keeps the South mobility signature. |

Reasoning:

South remains a melee/stealth crack-the-wall problem. The player must break through a named wall leader
and two defensive Samurai-bucket shooters while not letting the Ninja and Monk wrap the backline. The
former Archer slots now become Black Mage gun-casters, so parapet pressure is more dangerous without
changing the route's enemy count. Yoichi/Perseus still pay through spoils for route parity.

## Builds

### Knight Leader (Lv 101)

```text
Job bucket: Holy Knight, if possible   JobLevel: 8
Secondary: Holy Knight, if possible
Reaction: Counter (442)
Support: Attack Boost (465)
Movement: Movement +3
Right hand: Defender   Left hand: Crystal Shield
Head: Crystal Helm   Body: Crystal Mail   Accessory: Bracers
```

Implementation note:

```text
If Holy Knight cannot be assigned cleanly for this generic slot, preserve the role as a Knight Leader:
Defender + Crystal Shield anchor, Counter, Attack Boost, Movement +3, and no Rend wall plan.
```

### Wall Samurai x2 (Lv 102/102)

```text
Job bucket: Samurai   JobLevel: 8
Note: this JobLevel is mod-side bucket data; secondary JobLevel is not separately definable.
Secondary: Aim
Reaction: Dragon's Heart
Support: Defense Boost
Movement: Movement +3
Right hand: Gastrophetes   Left hand: Crystal Shield
Head: Crystal Helm   Body: Reflect Mail   Accessory: Bracers
```

### Monk (Lv 101)

```text
Job bucket: Monk   JobLevel: 8
Secondary: None
Reaction: First Strike (453)
Support: Dual Wield
Movement: Jump +3
Head: Barrette   Body: Power Garb   Accessory: Bracers
```

### Ninja (Lv 102)

```text
Job bucket: Ninja   JobLevel: 8
Secondary: Martial Arts
Reaction: First Strike (453)
Support: Brawler
Movement: Jump +3
Head: Thief's Cap   Body: Power Garb   Accessory: Bracers
```

### Black Mage x2 (Lv 102/101)

```text
Job bucket: Black Mage   JobLevel: 8
Secondary: None
Reaction: Reflexes (449)
Support: Equip Guns
Movement: Teleport
Right hand: Glacial Gun / Blaster (one each)
Head: Lambent Hat   Body: Wizard's Robe   Accessory: Magepower Glove
```

Role: long-range parapet pressure from the former Archer slots. Rewards still pay via guaranteed spoils;
Steal is optional and not required for Yoichi Bow + Perseus Bow.

## Positioning Plan

```text
South: the Knight Leader and 2 Samurai-bucket wall units hold the ramp, the 2 Black Mage gun-casters sit
  on the parapet above, and the Ninja/Monk start wide to use the wall edges and flank.
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

Current result source: inherited from the former combined 043 branch-balance simulation. The v3 redesign
needs a refreshed simulation pass because the old visible-bow branch has become Black Mage gun pressure
plus Monk/Ninja burst flanks.

## Implementation Checklist

- [ ] Confirm entry 448 South slot order before patching complete kits.
- [ ] Keep objective = "Defeat all enemies" + the vertical wall / narrow-path geometry.
- [ ] Knight Leader uses Holy Knight bucket/secondary if implementation supports it; otherwise preserve the documented leader role.
- [ ] Wall Knights become Samurai-bucket JobLevel 8 units with Aim, Dragon's Heart, Defense Boost, Movement +3.
- [ ] Former Archer slots become Black Mage JobLevel 8 units with no secondary, Reflexes, Equip Guns, Teleport.
- [ ] Former Thief slot becomes Monk JobLevel 8 with no secondary, First Strike, Dual Wield, Jump +3.
- [ ] Ninja keeps Ninja JobLevel 8 with Martial Arts, First Strike, Brawler, Jump +3.
- [ ] Give every active human complete equipment plus secondary/reaction/support/movement.
- [ ] Preserve guaranteed spoils: Yoichi Bow + Perseus Bow on this branch.
- [ ] Set levels in the low Ch4 band (`101`-`102`, no `103`); JobLevel `8` on all active slots.
- [ ] Patch entry 448 via the correct layer; keep the diff inside the South Wall window.
- [ ] Test this path from a New Game+ save and confirm South = melee/stealth wall assault.

## Test Questions

- Does South still feel like the melee/stealth branch, distinct from North?
- Can the player crack the Knight wall without being enveloped by the Ninja/Monk flank?
- Is the no-Rend wall still threatening through positioning, gear, and Black Mage gun pressure?
- Are the Black Mage gun-casters strong but still below Sluice pressure?
- Does the route pay Yoichi Bow + Perseus Bow equivalently to North?

## Sources

- Game8, "Fort Besselat: South Wall (Battle 38A)": roster, objective, terrain, rewards.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553198
- Local: `037-chapter-4-overview.md`, `043b-fort-besselat-north-wall.md`,
  `031-walled-city-yardrow.md`, `044-fort-besselat-sluice.md`,
  `chapter-4-rewards-implementation.md`, and `tmp/fft-level-design-043a-fort-besselat-south-wall/`.
