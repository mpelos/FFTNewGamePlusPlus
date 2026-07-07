# 043b - Fort Besselat: North Wall (Bethla Garrison)

Status: 📝 redesign v2 planned (docs-only) — v1 implementation exists for entry 449
Chapter: 4 — "In the Name of Love"
Battle order: Battle 38B (North Wall — mutually exclusive with `043a`)
Target version: Enhanced v1.5.0
ENTD: global entry **449** (North) — `battle_entd4_ent.bin` local 65
File: `battle_entd4_ent.bin` (embedded NG+ swap) — `tools/battle_patch.py besselat_wall`

> **NG++ reward applied (2026-06-27):** Yoichi Bow + Perseus Bow on the Archer slots of BOTH path entries
> (448 s3/s4, 449 s0/s3), so either route awards them. Guaranteed Spoils of War (ENTD 0x1e), NG+ only,
> within the 3-cap, no steal needed. Canonical map: `chapter-4-rewards-implementation.md`.

Current implementation (entry 449, vanilla-dump verified):
- s0 Archer L102, s3 Archer L101.
- s1 Dragoon L102, s2 Dragoon L101 — Partisan/heavy, Jump innate. TIC has 2 Dragoons vs the public
  walkthrough's 1.
- s4 Summoner L102 — priority caster, charge intact.
- s5 Monk L102 — bare-fist, Power Garb/Bracers.
- No boss / no named boss rare; low Ch4 band (101-102). Map treasure (other layer) untouched.

Planned v2 redesign (docs-only in this pass): keep the confirmed two-Dragoon North roster, but make
every active human a complete Chapter-4 unit. Yoichi/Perseus may be visible on the Archer roles here
because the reward pair is duplicated in `043a` for route parity.

## Design Goal

```text
Make North Wall the ranged/AoE branch of Fort Besselat: the player rushes a Summoner while reading two
Dragoon Jump threats on narrow vertical terrain. The route should feel distinct from South's
melee/stealth branch and clearly below the Sluice spike.
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

Original North composition (verified via Game8, Battle 38B):

```text
2x Archer    (ranged chip)
1x Monk      (melee bruiser; Chakra/Wave Fist)
1x Dragoon   (Jump — vertical pressure)
1x Summoner  (wide-area summon — the priority threat)
```

Local data correction:

```text
TIC / current local data has 2x Dragoon, not 1x Dragoon. The NG++ North doc follows the local roster:
2 Archer + 2 Dragoon + 1 Monk + 1 Summoner.
```

Vanilla comparison:

```text
- The route keeps the vanilla North identity: ranged/AoE pressure on vertical wall terrain.
- Objective is unchanged: defeat all enemies.
- Compared to public vanilla walkthroughs, the local entry has a second Dragoon; this is preserved.
- The difference is completeness: all active humans get Chapter-4-level gear and full ability slots.
- Yoichi Bow + Perseus Bow remain guaranteed route-parity rewards; visible Archer bows are optional
  pressure, never steal-gated rewards.
```

## Local Data Confirmed / Data Still Needed

```text
CONFIRMED:
- Entry 449 is the Fort Besselat North Wall ENTD entry.
- North local roster: 2 Archer + 2 Dragoon + 1 Summoner + 1 Monk.
- The player fights either this branch or South (`043a`), never both.
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
Monk job id            (TBD - verify)
Dragoon / Lancer id    (TBD - verify; enemy Dragoon, 027/038)
Summoner job id        (TBD - verify)
```

## Enemy Party Escalation (Chapter 4 rule)

```text
CHANGE: no new caste added. North becomes a complete ranged/AoE wall team: Summoner wide-AoE and two
  Dragoon Jump threats punish clumping on narrow ledges while Archers and Monk hold the route.
WHY: North's identity is "rush the Summoner / dodge the Jump." The faithful Ch4 move is to make every
  defender fully built and let the wall matter more, not to add a boss or a second engine.
CONSTRAINTS: Dragoon Jump = telegraphed panel; Summoner keeps intact charge times and remains race-able;
  Archers are pressure/reward carriers, not a separate gun engine.
REJECTED DEFAULTS: no accelerated Summoner, no hard-status support, no 103+ overlevel spike, no one-sided
  rewards. Branch parity matters because the player chooses only one path.
WHAT IS NOT CHANGED: North's roster, the "defeat all" objective, and wall/chokepoint geometry remain.
```

## Rare/reward handling

```text
Guaranteed spoils for entry 449: YOICHI BOW + PERSEUS BOW.
These are duplicated on South entry 448 because the player fights only one path.
The player must never be forced to pick a route or Steal to receive the reward pair.
PRESERVE: North map treasure (Carabineer Mail, Angel Ring, Runeblade, Kiku-Ichimonji) remains existing
map loot, not the NG++ reward channel.
```

## Proposed Composition (New Game++ North Wall v2)

Keep the local roster and the boss-less wall-skirmish feel. No `103`+ spike.

| Slot | Role | Job | Level | Br/Fa | Purpose |
| ------ | ------ | ----- | ------- | --- | --------- |
| n | Summoner | Summoner | `102` | `60/84` | Wide-area summon — priority kill; reaches you from start. |
| n | Dragoon | Dragoon | `102` | `86/40` | Jump — vertical pressure on the ledges. |
| n | Dragoon | Dragoon | `101` | `86/40` | Second Jump body from local data; keeps panels readable. |
| n | Monk | Monk | `102` | `88/40` | Melee bruiser with Chakra/Wave Fist pressure. |
| n | Bow Archer | Archer | `102` | `82/45` | Yoichi/Perseus visible bow pressure from the rampart. |
| n | Bow Archer | Archer | `101` | `82/45` | Second bow reward carrier; covers the approach. |

Reasoning:

North remains a ranged/AoE wall problem. The player must prioritize the Summoner, read two Dragoon
Jump panels, and handle Archer lane pressure while climbing narrow terrain. The second Dragoon is a
local-data correction, not an added spike.

## Builds

### Summoner (Lv 102)

```text
Summoner: (id TBD)   JobLevel: 8   Mid-tier summons, INTACT charge times.
Secondary: White Magic, limited to defensive/light support; no Short Charge/Quick-like acceleration.
Reaction: Reflexes (449)
Support: MA-boost (id TBD)   Movement: Movement +1 (486)   Body: shop robe (id TBD)
Accessory: Featherweave Cloak (234)   Right: magic-boost rod (id TBD)
```

### Dragoon x2 (Lv 102/101)

```text
Dragoon x2: (id TBD)   JobLevel: 8   Primary: Jump   Secondary: Item, limited utility only.
Reaction: Reflexes (449)   Support: Attack Boost (465)
Movement: Movement +1 (486)   Body: shop heavy armor (id TBD)   Right: shop spear   Left: shield
```

### Monk (Lv 102)

```text
Monk: (id TBD)   JobLevel: 8   Primary: Martial Arts (Chakra / Wave Fist)
Secondary: Item, limited utility only. Reaction: Counter (442)
Support: Attack Boost (465)   Movement: Movement +1 (486)   Body: Power Garb (195)   Accessory: Bracers (218)
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
North: the Summoner starts high/back with wide-AoE sightlines onto the climb, the 2 Dragoons start on
  staggered elevation for readable Jump arcs, the Monk starts forward as bruiser, and the 2 Archers sit
  on the rampart.
Preserve the narrow paths + height; do NOT flatten or widen the wall.
Modest levels — one of two converging skirmishes, not a spike.
```

## Simulation Plan and Results

Simulation artifact:

```text
tmp/fft-level-design-043b-fort-besselat-north-wall/
  assumptions.md
  simulate.py
  iteration-results.json
  iteration-results.md
```

Current result source: inherited from the former combined 043 branch-balance simulation. North accepted
as part of `v2 complete visible-bow branches`, with moderate pressure and route parity.

## Implementation Checklist

- [ ] Confirm entry 449 North slot order before patching complete kits.
- [ ] Keep objective = "Defeat all enemies" + the vertical wall / narrow-path geometry.
- [ ] Keep Summoner charge times intact and rushable.
- [ ] Keep two readable Dragoon Jump panels.
- [ ] Give every active human complete equipment plus secondary/reaction/support/movement.
- [ ] Preserve guaranteed spoils: Yoichi Bow + Perseus Bow on this branch.
- [ ] Set levels in the low Ch4 band (`101`-`102`, no `103`); JobLevel `8` on all active slots.
- [ ] Patch entry 449 via the correct layer; keep the diff inside the North Wall window.
- [ ] Test this path from a New Game+ save and confirm North = ranged/AoE wall assault.

## Test Questions

- Does North still feel like the ranged/AoE branch, distinct from South?
- Is the Summoner still the clear priority and race-able with intact charge times?
- Are both Dragoon Jump panels readable and dodge-able?
- Are active bow carriers strong but still below Sluice pressure?
- Does the route pay Yoichi Bow + Perseus Bow equivalently to South?

## Sources

- Game8, "Fort Besselat: North Wall (Battle 38B)": roster, objective, Summoner priority, terrain, rewards.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553199
- Local: `037-chapter-4-overview.md`, `043a-fort-besselat-south-wall.md`, `027`/`038`
  (Dragoon Jump), `028-monastery-vaults-3rd.md`, `044-fort-besselat-sluice.md`,
  `chapter-4-rewards-implementation.md`, and `tmp/fft-level-design-043b-fort-besselat-north-wall/`.
