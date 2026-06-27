# 043 - Fort Besselat: South / North Wall (Bethla Garrison)

Status: ✅ implemented (v1, entries 448 South / 449 North)
Chapter: 4 — "In the Name of Love"
Battle order: Battle 38 (A = South Wall / B = North Wall — the player picks ONE)
Target version: Enhanced v1.5.0
ENTD: global entries **448** (South) / **449** (North) — `battle_entd4_ent.bin` (local 64/65)

> **NG++ reward applied (2026-06-27):** Yoichi Bow + Perseus Bow on the Archer slots of BOTH path entries
> (448 s3/s4, 449 s0/s3), so either route awards them. Guaranteed Spoils of War (ENTD 0x1e), NG+ only,
> within the 3-cap, no steal needed. Canonical map: `chapter-4-rewards-implementation.md`.
File: `battle_entd4_ent.bin` (embedded NG+ swap) — `tools/battle_patch.py besselat_wall`

Implemented (both entries, vanilla-dump verified):
- **South 448** (melee/stealth): s0,s1 Knight L102 + s2 Knight L101 (Heavy gear/Runeblade/Shield, Rend
  innate); s3 Archer L102, s4 Archer L101 (Windslash); s5 Ninja L102 (dual Longblade); s6 Thief L101 (Air Knife).
- **North 449** (ranged/AoE): s0 Archer L102, s3 Archer L101; s1 Dragoon L102, s2 Dragoon L101
  (Partisan/heavy, Jump innate — TIC has 2 Dragoons vs walkthrough's 1); s4 Summoner L102 (priority,
  charge intact); s5 Monk L102 (bare-fist, Power Garb/Bracers).
- No boss / no rare; low Ch4 band (101-102). Map treasure (other layer) untouched.

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `037-chapter-4-overview.md`. This is a BRANCHING battle: South and North are mutually
> exclusive (the player attacks one wall); BOTH lead to the same next battle, the Sluice Gate (`044`).

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

## Local Data Confirmed

```text
TBD — dump BOTH entries (South and North) on Windows and fill the slot tables here, like 001-gariland.
Confirm South slots: 3 Knight + 2 Archer + 1 Thief + 1 Ninja; North slots: 2 Archer + 1 Monk +
  1 Dragoon + 1 Summoner; plus the player slots in each.
Keep both as "Defeat all enemies" with the VERTICAL WALL + NARROW-PATH geometry (the chokepoint puzzle
  IS the fight). Keep the Dragoon Jump (North) and the Ninja wall-climb/Throw (South).
This is a no-boss, no-rare wall skirmish (one of two): modest Ch4 levels (100-103), NOT a spike.
Confirm whether OverrideEntryData carries Level for these battles or leaves them at -1.
Leave the map treasure (Circlet / Platinum Sword / Carabineer Mail / etc.) as-is — map loot, not boss loot.
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

## Job Escalation (Chapter 4 rule)

```text
CHANGE: NO new caste added. The escalation is the TERRAIN sharpening each path's existing signature —
  South's Ninja/Thief exploit the ramparts to flank a Knight wall; North's Summoner wide-AoE + Dragoon
  Jump punish clumping on narrow ledges. Levels rise to the Ch4 band (45-equivalent).
WHY: the fight's identity is "vertical chokepoint warfare, two flavors." Each path already carries one
  clean demand (South = crack the wall while covering your flanks; North = kill the Summoner / dodge
  the Jump). Bolting a new mechanic onto either would break the one-new-demand rule and blur the
  South/North contrast. The faithful Ch4 move is to make the verticality MATTER more (tighter
  chokepoints, accurate high-ground placement), not to add castes.
CONSTRAINTS (carried): Ninja Throw = ranged DAMAGE, not a lock (031); Dragoon Jump = telegraphed panel
  (027/038); Summoner = INTACT charge times, race-able (028); Thief steal/charm = minor harass, no
  hard lock; Knight Rend ≤2 sources (South has 3 Knights → give Rend to at most 2).
WHAT IS NOT CHANGED: both rosters, the "defeat all" objective, and the wall/chokepoint geometry remain.
  No boss, no rare. Each path stays its own distinct skirmish.
```

## Sanctioned exceptions (carried precedents)

```text
NINJA THROW / WALL-CLIMB (South) — ranged damage + mobility; pin/intercept counters (031). Not a lock.
DRAGOON JUMP (North) — telegraphed landing panel, untargetable airborne; step off / kill grounded (027/038).
SUMMONER WIDE-AoE (North) — mid-tier summons, INTACT charge times; race-able by rushing the Summoner (028).
THIEF STEAL/CHARM (South) — minor harass, counterable, no hard lock (Ch2/Ch3 precedent).
KNIGHT REND (South) — at most 2 of the 3 Knights (≤2-break-source cap); telegraphed, Safeguard/Steal.
No NEW exception introduced — this is established castes on vertical terrain.
```

## Boss rare loot

```text
None. No named boss on either path — no rare boss item (per the Chapter 4 overview tiering). Generics
stay Chapter-4 shop-tier. The map treasure (South: Circlet, Platinum Sword; North: Carabineer Mail,
Angel Ring, Runeblade, Kiku-Ichimonji) is EXISTING map loot — leave it as-is.
```

## Proposed Composition (New Game++ Fort Besselat Wall v1)

Keep both rosters and the boss-less wall-skirmish feel; raise to the Ch4 band and let the terrain do
the work. No `103`+ spike — this is one of two converging paths.

### South Wall (A) — melee / stealth (7)

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Knight | Knight | `102` | Wall of bodies; Rend (break source 1). |
| n | Knight | Knight | `102` | Second body; Rend (break source 2 — cap). |
| n | Knight | Knight | `101` | Third body; NO Rend (cap kept). |
| n | Archer | Archer | `102` | Parapet chip down the narrow path. |
| n | Archer | Archer | `101` | Second archer; covers the ramp. |
| n | Thief | Thief | `101` | Fast flank / steal harass using the walls. |
| n | Ninja | Ninja | `102` | Wall-climbing dual-wield / Throw — the South signature. |

### North Wall (B) — ranged / AoE (5)

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Summoner | Summoner | `102` | Wide-area summon — PRIORITY kill; reaches you from start. |
| n | Dragoon | Dragoon | `102` | Jump — vertical pressure on the ledges. |
| n | Monk | Monk | `102` | Melee bruiser (Chakra self-sustain / Wave Fist). |
| n | Archer | Archer | `102` | Ranged chip from the rampart. |
| n | Archer | Archer | `101` | Second archer; covers the approach. |

Reasoning:

The faithful move is to **keep both paths distinct and let the wall carry the difficulty**. South
stays a melee/stealth crack-the-wall problem (Knight wall with Rend capped, plus a wall-climbing Ninja
and a Thief to punish exposed flanks). North stays a ranged/AoE problem (rush the Summoner, dodge the
Dragoon's Jump, grind the Monk). Levels sit in the low Ch4 band (`101`–`102`, no `103`) because this
is a converging skirmish, not a boss spike — and the player only fights ONE side, so neither path
should feel like a wall-of-numbers.

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
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head: shop helm (id TBD)   Body: shop heavy armor (id TBD)   Accessory: Bracers (218)
Right hand: shop knight sword (id TBD)   Left: shop shield (id TBD)
```

### Ninja (South — Lv 102) / Thief (South — Lv 101)

```text
Ninja: (id TBD)   Secondary: Throw   Reaction: First Strike (453)   Support: Attack Boost (465)
  Movement: Movement +2 (487)   Head: Thief's Cap (168)   Body: Black Garb (198)
  Accessory: Germinas Boots (210)   Hands: shop ninja blade x2 (dual-wield)
Thief (83): Secondary: Steal   Reaction: First Strike (453)   Support: Attack Boost (465)
  Movement: Movement +2 (487)   Head: Thief's Cap (168)   Body: Black Garb (198)
  Accessory: Germinas Boots (210)   Right: Air Knife (9)
```

### Summoner (North — Lv 102) / Dragoon (North — Lv 102) / Monk (North — Lv 102)

```text
Summoner: (id TBD)   Mid-tier summons, INTACT charge times.   Reaction: Reflexes (449)
  Support: MA-boost (id TBD)   Movement: Movement +1 (486)   Body: shop robe (id TBD)
  Accessory: Featherweave Cloak (234)   Right: magic-boost rod (id TBD)
Dragoon: (id TBD)   Primary: Jump   Reaction: Reflexes (449)   Support: Attack Boost (465)
  Movement: Movement +1 (486)   Body: shop heavy armor (id TBD)   Right: shop spear   Left: shield
Monk: (id TBD)   Primary: Martial Arts (Chakra / Wave Fist)   Reaction: Counter (442)
  Support: Attack Boost (465)   Movement: Movement +1 (486)   Body: Power Garb (195)   Accessory: Bracers (218)
```

### Archer x2 (both paths — Lv 102/101)

```text
Job: Archer (77)   Secondary: none   Reaction: Reflexes (449)   Support: Concentration (469)
  Movement: Movement +1 (486)   Head: Thief's Cap (168)   Body: Black Garb (198)
  Accessory: Bracers (218)   Right: shop high-tier bow (id TBD)
```

## Positioning Plan

```text
Both paths: place the enemy to OWN the verticality — defenders on the high rampart, chokepoints on the
  narrow ramp the player must climb.
SOUTH: the 3 Knights hold the ramp (the wall of bodies), the 2 Archers on the parapet above, the Ninja
  and Thief start wide to use the wall edges and flank — the player must crack the wall without being
  enveloped.
NORTH: the Summoner starts high/back with wide-AoE sightlines onto the climb (rush her), the Dragoon on
  elevation for Jump arcs, the Monk forward as the bruiser, the 2 Archers on the rampart.
Preserve the narrow paths + height; do NOT flatten or widen the wall (the chokepoint IS the fight).
Modest levels — one of two converging skirmishes, not a spike.
```

The walls should say: "two ways up the garrison — fight through steel on the south stair or magic and
spears on the north; either way, the wall is the real enemy."

## Implementation Checklist

- [ ] Identify BOTH Fort Besselat wall `BattleId` / ENTD entries (South + North); fill "Local Data".
- [ ] Dump both entries; verify South (3 Knight+2 Archer+1 Thief+1 Ninja) and North (2 Archer+1 Monk+
      1 Dragoon+1 Summoner) + player slots.
- [ ] Keep both objectives "Defeat all enemies" + the vertical wall / narrow-path geometry.
- [ ] South: Rend on ≤2 Knights; keep Ninja Throw/wall-climb + Thief steal (minor harass).
- [ ] North: keep Summoner charge times intact (rushable) + Dragoon Jump panels.
- [ ] Set levels in the low Ch4 band (`101`-`102`, no `103`); JobLevel `8` on all active slots.
- [ ] Patch both entries via the correct layer; keep each diff inside its own battle window.
- [ ] Re-dump and diff both; confirm changes are small, distinct per path, and intentional.
- [ ] Install mod, test BOTH paths from a New Game+ save; confirm South=melee/stealth, North=ranged/AoE.

## Test Questions

- Do South and North still feel DISTINCT (melee/stealth vs ranged/AoE) on the same wall?
- Does the verticality/chokepoint carry the difficulty (no boss, modest levels)?
- South: can the player crack the Knight wall without being enveloped by the Ninja/Thief flank?
- North: is the Summoner still the clear priority, and is the Dragoon Jump dodge-able?
- Are all carried caste constraints honored (Throw/Jump/Summon/Steal/Rend caps — no hard lock)?
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
  converging battle — to be designed).
```
</content>
