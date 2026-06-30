# 043 - Fort Besselat: South / North Wall (Bethla Garrison)

Status: 📝 redesign v2 planned (docs-only) — v1 implementation exists for entries 448 South / 449 North
Chapter: 4 — "In the Name of Love"
Battle order: Battle 38 (A = South Wall / B = North Wall — the player picks ONE)
Target version: Enhanced v1.5.0
ENTD: global entries **448** (South) / **449** (North) — `battle_entd4_ent.bin` (local 64/65)

> **NG++ reward applied (2026-06-27):** Yoichi Bow + Perseus Bow on the Archer slots of BOTH path entries
> (448 s3/s4, 449 s0/s3), so either route awards them. Guaranteed Spoils of War (ENTD 0x1e), NG+ only,
> within the 3-cap, no steal needed. Canonical map: `chapter-4-rewards-implementation.md`.
File: `battle_entd4_ent.bin` (embedded NG+ swap) — `tools/battle_patch.py besselat_wall`

Current implementation (both entries, vanilla-dump verified):
- **South 448** (melee/stealth): s0,s1 Knight L102 + s2 Knight L101 (Heavy gear/Runeblade/Shield, Rend
  innate); s3 Archer L102, s4 Archer L101 (Windslash); s5 Ninja L102 (dual Longblade); s6 Thief L101 (Air Knife).
- **North 449** (ranged/AoE): s0 Archer L102, s3 Archer L101; s1 Dragoon L102, s2 Dragoon L101
  (Partisan/heavy, Jump innate — TIC has 2 Dragoons vs walkthrough's 1); s4 Summoner L102 (priority,
  charge intact); s5 Monk L102 (bare-fist, Power Garb/Bracers).
- No boss / no named boss rare; low Ch4 band (101-102). Map treasure (other layer) untouched.

Planned v2 redesign (docs-only in this pass): keep the local South/North rosters, including the
confirmed **two-Dragoon North** entry, but make every active human a complete Chapter-4 unit. The
Yoichi/Perseus Bow reward pair may be visible on the Archer roles in BOTH entries because the gear is
role-fitting, branch-parity safe, and still moderate under the wall model.

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `037-chapter-4-overview.md`. This is a BRANCHING battle: South and North are mutually
> exclusive (the player attacks one wall); BOTH lead to the same next battle, the Sluice Gate (`044`).

## Design Goal

```text
Make Fort Besselat Wall a fair branching breather with teeth: South tests cracking a Knight wall while
Ninja/Thief pressure the flanks; North tests rushing a Summoner and reading two Dragoon Jump threats.
Both routes must feel distinct, complete, reward-equivalent, and clearly below the Sluice spike.
```

No active guests appear here. No guest-control implementation is needed for either branch.

## Original Battle

Objective (both paths):

```text
Defeat all enemies!
```

Player deployment:

```text
Up to 5 units, including Ramza. No guests.
```

Original enemy composition (verified via Game8, Battle 38 A & B):

```text
SOUTH WALL (A) — melee / stealth gauntlet:
  3x Knight    (front-line wall of bodies)
  2x Archer    (ranged chip from the parapets)
  1x Thief     (steal / fast flank)
  1x Ninja     (dual-wield wall-climber / Throw)

NORTH WALL (B) — ranged / AoE gauntlet:
  2x Archer    (ranged chip)
  1x Monk      (melee bruiser; Chakra/Wave Fist)
  1x Dragoon   (Jump — vertical pressure)
  1x Summoner  (wide-area summon — the priority threat)
```

Public walkthrough details:

```text
Recommended level: ~45.  Difficulty: 3/5 stars (both).  Deploy up to 5.  Win: defeat all enemies.
FORTRESS WALLS — vertical ramparts and NARROW paths; height and chokepoints define both fights.
SOUTH is a heavier melee/stealth press (Knight wall + Ninja/Thief flankers using the walls);
NORTH is a ranged/AoE press (Summoner wide-area + Dragoon Jump + Monk + Archers) — the walkthrough
  says PRIORITIZE THE SUMMONER, whose wide spells reach you from her start.
Both paths converge on the Sluice Gate next (044).
Rewards: South — 30,700 Gil, Circlet, Platinum Sword (treasure). North — 27,200 Gil, Carabineer Mail,
  Angel Ring / Runeblade / Kiku-Ichimonji (treasure).
```

Design reading:

Fort Besselat's walls are **the branching fortress assault**: the player storms one of two ramparts,
and the two paths are deliberately *different fights on the same vertical terrain*. **South** is a
**melee/stealth** problem — a Knight wall you must crack while a Ninja and Thief use the ramparts to
flank and harass. **North** is a **ranged/AoE** problem — a Summoner's wide spells and a Dragoon's
Jump punish you on the narrow ledges, so you rush the Summoner and read the Jump panels. The shared
identity is **vertical chokepoint warfare**: height, narrow paths, and a "defeat all" clear that
rewards controlling the ramp.

For New Game++ the identity must stay: **a branching fortress-wall assault on vertical, narrow terrain
— South a melee/stealth press, North a ranged/AoE press — both kept boss-less skirmishes whose one
demand is mastering the wall's verticality and chokepoints; each path's signature threat (South's
Ninja flank / North's Summoner AoE + Dragoon Jump) is sharpened by the terrain, not replaced.**

## Local Data Confirmed / Data Still Needed

```text
CONFIRMED:
- Entries 448 South / 449 North are the Fort Besselat Wall branch entries.
- South roster: 3 Knight + 2 Archer + 1 Ninja + 1 Thief.
- North local roster: 2 Archer + 2 Dragoon + 1 Summoner + 1 Monk.
- The player fights exactly one branch; both lead to the Sluice (`044`).
- No active guest, no boss.
- Reward ledger duplicates Yoichi Bow + Perseus Bow across BOTH entries so either route pays the same
  guaranteed spoils.

STILL NEEDED FOR V2 IMPLEMENTATION:
- Confirm exact slot order before patching complete v2 kits on both entries.
- Confirm both objectives remain "Defeat all enemies".
- Confirm whether OverrideEntryData carries level for these battles or leaves levels at runtime scale.
- Preserve vertical wall / narrow-path geometry and all branch scripting.
- Preserve map treasure as vanilla map loot.
```

Job IDs (carry over known, verify the rest in-game):

```text
77 = Archer            (confirmed)
83 = Thief             (confirmed)
Knight job id          (TBD - verify)
Monk job id            (TBD - verify)
Ninja job id           (TBD - verify; Ch3 debut, 031)
Dragoon / Lancer id    (TBD - verify; enemy Dragoon, 027/038)
Summoner job id        (TBD - verify)
```

## Enemy Party Escalation (Chapter 4 rule)

```text
CHANGE: NO new caste added. The escalation is complete branch-specific wall teams plus visible
  role-fitting bow pressure. South's Ninja/Thief exploit the ramparts to flank a Knight wall; North's
  Summoner wide-AoE + two Dragoon Jump threats punish clumping on narrow ledges.
WHY: the fight's identity is "vertical chokepoint warfare, two flavors." Each path already carries one
  clean demand (South = crack the wall while covering your flanks; North = kill the Summoner / dodge
  the Jump). The faithful Ch4 move is to make every defender fully built and let the wall matter more,
  not to add castes or a boss.
CONSTRAINTS (carried): Ninja Throw = ranged DAMAGE, not a lock (031); Dragoon Jump = telegraphed panel
  (027/038); Summoner = INTACT charge times, race-able (028); Thief steal/charm = minor harass, no
  hard lock; Knight Rend ≤2 sources (South has 3 Knights → give Rend to at most 2).
REJECTED DEFAULTS: no third Rend Knight, no accelerated Summoner, no hard-status flankers, no 103+
  overlevel spike, no one-sided rewards. Branch parity matters because the player chooses only one path.
WHAT IS NOT CHANGED: both rosters, the "defeat all" objective, and the wall/chokepoint geometry remain.
  No boss. Each path stays its own distinct skirmish.
```

## Sanctioned exceptions (carried precedents)

```text
NINJA THROW / WALL-CLIMB (South) — ranged damage + mobility; pin/intercept counters (031). Not a lock.
DRAGOON JUMP (North) — telegraphed landing panel, untargetable airborne; step off / kill grounded (027/038).
SUMMONER WIDE-AoE (North) — mid-tier summons, INTACT charge times; race-able by rushing the Summoner (028).
THIEF STEAL/CHARM (South) — minor harass, counterable, no hard lock (Ch2/Ch3 precedent).
KNIGHT REND (South) — at most 2 of the 3 Knights (≤2-break-source cap); telegraphed, Safeguard/Steal.
No hard-control exception introduced — this is established castes plus role-fitting bow rewards on
vertical terrain.
```

## Rare/reward handling

```text
Guaranteed spoils for BOTH entries: YOICHI BOW + PERSEUS BOW.
These are duplicated across entries 448 and 449 because the player fights only one path.
The player must never be forced to pick a route or Steal to receive the reward pair.
COMBAT ROLE: the bows may be visible on Archer slots because they are role-fitting non-buyable gear
and reinforce the wall-rampart puzzle. If playtest shows they spike either route, move them to spoils
payload only and resimulate.
PRESERVE: map treasure (South: Circlet, Platinum Sword; North: Carabineer Mail, Angel Ring, Runeblade,
Kiku-Ichimonji) remains existing map loot, not the NG++ reward channel.
```

## Proposed Composition (New Game++ Fort Besselat Wall v2)

Keep both local rosters and the boss-less wall-skirmish feel; make every active human complete and let
the terrain do the work. No `103`+ spike — this is one of two converging paths before the harder Sluice.

### South Wall (A) — melee / stealth (7)

| Slot | Role | Job | Level | Br/Fa | Purpose |
| ------ | ------ | ----- | ------- | --- | --------- |
| n | Knight | Knight | `102` | `88/42` | Wall of bodies; Rend (break source 1). |
| n | Knight | Knight | `102` | `88/42` | Second body; Rend (break source 2 — cap). |
| n | Knight | Knight | `101` | `88/42` | Third body; NO Rend (cap kept). |
| n | Bow Archer | Archer | `102` | `82/45` | Yoichi/Perseus visible bow pressure from the parapet. |
| n | Bow Archer | Archer | `101` | `82/45` | Second bow reward carrier; covers the ramp. |
| n | Thief Flanker | Thief | `101` | `88/38` | Fast flank / steal harass using the walls; no hard status. |
| n | Ninja Flanker | Ninja | `102` | `90/35` | Wall-climbing dual-wield / Throw — the South signature. |

### North Wall (B) — ranged / AoE (6)

| Slot | Role | Job | Level | Br/Fa | Purpose |
| ------ | ------ | ----- | ------- | --- | --------- |
| n | Summoner | Summoner | `102` | `60/84` | Wide-area summon — PRIORITY kill; reaches you from start. |
| n | Dragoon | Dragoon | `102` | `86/40` | Jump — vertical pressure on the ledges. |
| n | Dragoon | Dragoon | `101` | `86/40` | Second Jump body from local data; keeps panels readable. |
| n | Monk | Monk | `102` | `88/40` | Melee bruiser (Chakra self-sustain / Wave Fist). |
| n | Bow Archer | Archer | `102` | `82/45` | Yoichi/Perseus visible bow pressure from the rampart. |
| n | Bow Archer | Archer | `101` | `82/45` | Second bow reward carrier; covers the approach. |

Reasoning:

The faithful move is to **keep both paths distinct and let the wall carry the difficulty**. South
stays a melee/stealth crack-the-wall problem (Knight wall with Rend capped, plus a wall-climbing Ninja
and a Thief to punish exposed flanks). North stays a ranged/AoE problem (rush the Summoner, dodge two
readable Dragoon Jump bodies, grind the Monk). The Yoichi/Perseus bow pair is duplicated across both
routes and may sit on the Archers as visible, role-fitting pressure. Levels sit in the low Ch4 band
(`101`–`102`, no `103`) because this is a converging skirmish, not a boss spike — and the player only
fights ONE side, so neither path should feel like a wall-of-numbers.

Rejected variants:

```text
- v1 partial setup: correct branch shape, but incomplete for Chapter 4 humans.
- Spoils-only bows: acceptable fallback, but less expressive if active bows test fair.
- South triple-Rend wall: violates the two-break-source cap.
- North accelerated Summoner: turns a wall assault into a speed-caster puzzle.
- Hard-status flankers: not appropriate for a breather branch.
- Overlevelled walls: creates a spike immediately before Sluice.
- One-sided rewards: fails branch parity.
```

## Builds (Chapter-4 shop quality; fortress-garrison flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Knight x3 (South — Lv 102/102/101)

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

### Ninja (South — Lv 102) / Thief (South — Lv 101)

```text
Ninja: (id TBD)   JobLevel: 8   Secondary: Throw   Reaction: First Strike (453)   Support: Attack Boost (465)
  Movement: Movement +2 (487)   Head: Thief's Cap (168)   Body: Black Garb (198)
  Accessory: Germinas Boots (210)   Hands: shop ninja blade x2 (dual-wield)
Thief (83): JobLevel: 8   Secondary: Steal   Reaction: First Strike (453)   Support: Attack Boost (465)
  Movement: Movement +2 (487)   Head: Thief's Cap (168)   Body: Black Garb (198)
  Accessory: Germinas Boots (210)   Right: Air Knife (9)
```

### Summoner (North — Lv 102) / Dragoon (North — Lv 102) / Monk (North — Lv 102)

```text
Summoner: (id TBD)   JobLevel: 8   Mid-tier summons, INTACT charge times. Secondary: White Magic,
  limited to defensive/light support; no Short Charge/Quick-like acceleration.
  Reaction: Reflexes (449)
  Support: MA-boost (id TBD)   Movement: Movement +1 (486)   Body: shop robe (id TBD)
  Accessory: Featherweave Cloak (234)   Right: magic-boost rod (id TBD)
Dragoon x2: (id TBD)   JobLevel: 8   Primary: Jump   Secondary: Item, limited utility only.
  Reaction: Reflexes (449)   Support: Attack Boost (465)
  Movement: Movement +1 (486)   Body: shop heavy armor (id TBD)   Right: shop spear   Left: shield
Monk: (id TBD)   JobLevel: 8   Primary: Martial Arts (Chakra / Wave Fist)   Secondary: Item,
  limited utility only. Reaction: Counter (442)
  Support: Attack Boost (465)   Movement: Movement +1 (486)   Body: Power Garb (195)   Accessory: Bracers (218)
```

### Archer x2 (both paths — Lv 102/101)

```text
Job: Archer (77)   JobLevel: 8   Secondary: Item, limited to Potion/Remedy style utility.
Reaction: Reflexes (449)   Support: Concentration (469)
  Movement: Movement +1 (486)   Head: Thief's Cap (168)   Body: Black Garb (198)
  Accessory: Bracers (218)   Right: Yoichi/Perseus or shop high-tier bow per slot/reward plan
```

Role: visible bow pressure from the wall. Rewards still pay via guaranteed spoils; Steal is optional.

## Positioning Plan

```text
Both paths: place the enemy to OWN the verticality — defenders on the high rampart, chokepoints on the
  narrow ramp the player must climb.
SOUTH: the 3 Knights hold the ramp (the wall of bodies), the 2 Archers on the parapet above, the Ninja
  and Thief start wide to use the wall edges and flank — the player must crack the wall without being
  enveloped.
NORTH: the Summoner starts high/back with wide-AoE sightlines onto the climb (rush her), the 2 Dragoons
  on staggered elevation for readable Jump arcs, the Monk forward as the bruiser, the 2 Archers on the
  rampart.
Preserve the narrow paths + height; do NOT flatten or widen the wall (the chokepoint IS the fight).
Modest levels — one of two converging skirmishes, not a spike.
```

The walls should say: "two ways up the garrison — fight through steel on the south stair or magic and
spears on the north; either way, the wall is the real enemy."

## Simulation Plan and Results

Simulation artifact:

```text
tmp/fft-level-design-043-fort-besselat-wall/
  assumptions.md
  simulate.py
  iteration-results.json
  iteration-results.md
```

Model scope:

```text
Coarse deterministic branch-balance model over the first five rounds.
It scores South pressure, North pressure, branch delta, identity clarity, answerability, reward parity,
and hard-lock risk. It does not simulate exact FFT formulas.
```

Result summary:

| Candidate | South pressure | North pressure | Delta | Identity | Answer | Reward parity | Hard lock | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| v1 partial branch | 148 | 141 | 7 | 93 | 84 | 100 | 0 | Rejected: incomplete setup |
| v2 complete visible-bow branches | 156 | 149 | 7 | 93 | 84 | 100 | 0 | **Accepted** |
| spoils-only bow branches | 140 | 133 | 7 | 83 | 84 | 90 | 0 | Rejected: weaker expression / parity risk |
| south triple-rend wall | 168 | 149 | 19 | 93 | 60 | 100 | 0 | Rejected: break cap violation |
| north accelerated summoner | 156 | 173 | 17 | 75 | 66 | 100 | 0 | Rejected: second speed engine |
| hard-status flankers | 191 | 184 | 7 | 69 | 54 | 100 | 45 | Rejected: hard status |
| overlevelled walls | 178 | 171 | 7 | 93 | 76 | 100 | 0 | Rejected: too spiky before Sluice |
| one-sided rewards | 156 | 149 | 7 | 93 | 84 | 40 | 0 | Rejected: route parity failure |

Iteration decision:

```text
ACCEPT v2 complete visible-bow branches.
Both routes remain moderate, distinct, reward-equivalent, and readable. Use active bow pressure on the
Archer slots if playtest confirms it stays below the Sluice; otherwise move the bows to spoils payload
only and resimulate.
```

## Implementation Checklist

- [ ] Confirm current entries 448 South / 449 North slot order before patching complete kits.
- [ ] Verify South (3 Knight + 2 Archer + 1 Thief + 1 Ninja) and North local roster (2 Archer + 2
      Dragoon + 1 Monk + 1 Summoner) + player slots.
- [ ] Keep both objectives "Defeat all enemies" + the vertical wall / narrow-path geometry.
- [ ] South: Rend on ≤2 Knights; third Knight has no Rend; keep Ninja Throw/wall-climb + Thief steal.
- [ ] North: keep Summoner charge times intact (rushable) + two readable Dragoon Jump panels.
- [ ] Give every active human complete equipment plus secondary/reaction/support/movement.
- [ ] Keep secondaries constrained to utility/support; no Phoenix Down loops, hard status, or Summoner speed engine.
- [ ] Preserve guaranteed spoils: Yoichi Bow + Perseus Bow on BOTH branch entries.
- [ ] Set levels in the low Ch4 band (`101`-`102`, no `103`); JobLevel `8` on all active slots.
- [ ] Patch both entries via the correct layer; keep each diff inside its own battle window.
- [ ] Re-dump and diff both; confirm changes are small, distinct per path, and intentional.
- [ ] Install mod, test BOTH paths from a New Game+ save; confirm South=melee/stealth, North=ranged/AoE.

## Test Questions

- Do South and North still feel DISTINCT (melee/stealth vs ranged/AoE) on the same wall?
- Does the verticality/chokepoint carry the difficulty (no boss, modest levels)?
- South: can the player crack the Knight wall without being enveloped by the Ninja/Thief flank?
- North: is the Summoner still the clear priority, and are both Dragoon Jump panels dodge-able?
- Are all carried caste constraints honored (Throw/Jump/Summon/Steal/Rend caps — no hard lock)?
- Do all active humans have complete equipment plus secondary/reaction/support/movement?
- Do both branch entries pay Yoichi Bow + Perseus Bow equivalently?
- Are active bow carriers strong but still below Sluice pressure?
- Are levels kept low Ch4 band so this converging skirmish isn't a spike before the Sluice/Limberry?
- Does each path read as one face of a fortress assault, not a designed arena?

## Sources

- Game8, "Fort Besselat: South Wall (Battle 38A)": roster (3 Knight + 2 Archer + 1 Thief + 1 Ninja),
  "Defeat all enemies!", rec ~45, 3/5 stars, deploy 5, fortress vertical walls, rewards (Circlet,
  Platinum Sword). https://game8.co/games/Final-Fantasy-Tactics/archives/553198
- Game8, "Fort Besselat: North Wall (Battle 38B)": roster (2 Archer + 1 Monk + 1 Dragoon + 1 Summoner),
  prioritize the Summoner, rewards (Carabineer Mail, Angel Ring, Runeblade, Kiku-Ichimonji).
  https://game8.co/games/Final-Fantasy-Tactics/archives/553199
- Final Fantasy Wiki, "Bethla Garrison": story/terrain context.
  https://finalfantasy.fandom.com/wiki/Bethla_Garrison
- Local: `037-chapter-4-overview.md` (rules), `031-walled-city-yardrow.md` (Ninja), `027`/`038`
  (Dragoon Jump), `028-monastery-vaults-3rd.md` (Summoner), `044-fort-besselat-sluice.md` (the next,
  converging battle — to be designed), `chapter-4-rewards-implementation.md` (Yoichi/Perseus duplicate
  reward parity across both branch entries).
