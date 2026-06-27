# 045 - Mount Germinas (Germinas Peak)

Status: ✅ implemented (v1, entry 452)
Chapter: 4 — "In the Name of Love"
Battle order: Battle 40 (after Bethla Sluice)
Target version: Enhanced v1.5.0
ENTD: global entry **452** (local entry 68, `battle_entd4_ent.bin`)
File: `battle_entd4_ent.bin` (embedded NG+ swap) — `tools/battle_patch.py germinas`

> **NG++ reward applied (2026-06-27):** the ninja arsenal - Ninja Gear (s0, Ninja) + Koga Blade (s1, Ninja)
> + Iga Blade (s2, Thief). The two prior minor spoils (s1 item212, s2 Germinas Boots) were overwritten so
> the three ninja items are the awarded 3. Guaranteed Spoils of War (ENTD 0x1e), NG+ only, within the
> 3-cap, no steal needed. Canonical map: `chapter-4-rewards-implementation.md`.

Implemented (entry 452, vanilla-dump verified) — slots: s0 Ninja, s1,s2 Thief, s3,s4,s5 Archer:
- s0 Ninja L103 (apex) + s1 Thief→**Ninja** L102 — dual Ninja Longblades; Thief's Cap/Black Garb/Germinas; First Strike/Atk Boost/Mv+2.
- s2 Thief L101 — Air Knife; Steal harass; First Strike/Atk Boost/Mv+2.
- s3 Archer L102, s4,s5 Archer L101 — Thief's Cap/Black Garb/Bracers/Windslash (two-hand); Reflexes/Concentration/Mv+1.
- No boss/no rare; in-band levels (terrain rates it 4/5★). Plateau geometry + buried Invisibility Cloak (other layer) untouched.

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `037-chapter-4-overview.md`.

## Original Battle

Objective:

```text
Defeat all enemies!   (with an optional buried-treasure side-objective — see below)
```

Player deployment:

```text
Up to 5 units, including Ramza. No guests.
```

Original enemy composition (verified via Game8, Battle 40):

```text
3x Archer    (ranged chip from the ledges)
2x Thief     (fast climbers; Steal harass)
1x Ninja     (dual-wield wall-climber / Throw — the apex mobility threat)
```

Public walkthrough details:

```text
Recommended level: ~59.  Difficulty: 4/5 stars.  Deploy up to 5.  Win: defeat all enemies.
MOUNTAIN PLATEAU — multiple elevation levels; verticality and ledges define the fight. Fast, mobile
  enemies (Ninja/Thieves) climb and flank; Archers chip from the high ledges.
OPTIONAL SIDE-OBJECTIVE — a buried INVISIBILITY CLOAK: secure it with a LOW-BRAVERY Chemist running
  Treasure Hunter parked on the right dig tile (a multitasking/positioning layer atop the skirmish).
Rewards: 36,200 Gil, Germinas Boots, Winged Boots (treasure).
```

Design reading:

Mount Germinas is **the hard vertical skirmish** (4/5★, a clear step up from the chapter's 3/5★
fields): no boss, but a **fast, gear-stealing, ledge-hopping band on a multi-level plateau**, plus the
**optional Invisibility-Cloak dig** that pulls a fragile Chemist out onto the map. Its identity is
**verticality + mobility + theft + a treasure-race**: the player must control the high ground, pin the
climbers before they Steal and scatter, and optionally protect a digging Chemist — all on terrain that
punishes a flat-footed formation. It's the last "pure skirmish" before the Limberry boss chain, and it
earns its higher star rating through movement and multitasking, not a boss.

For New Game++ the identity must stay: **a 4/5★ vertical mobility/steal skirmish on the plateau — pin
the wall-climbing flankers and hold the ledges while optionally racing the buried Invisibility Cloak —
sharpened by making the Ninja(s) the apex ledge threat, but kept boss-less and rare-less.**

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm slots: 3 Archer + 2 Thief + 1 Ninja (pre-swap), plus the player slots, AND the buried
  Invisibility-Cloak treasure tile.
Keep the MULTI-LEVEL PLATEAU geometry + high enemy Move/Jump (the verticality/mobility IS the fight)
  and the buried Invisibility-Cloak dig tile (the optional side-objective — vanilla; do not remove).
This is a no-boss, no-rare 4/5-star skirmish: keep enemy band scale-to-party (101-103); terrain +
  composition carry the difficulty, NOT a raw level spike (rec ~59 is the player's curve, not an offset).
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
Leave the buried treasure (Invisibility Cloak) + spoils (Germinas Boots, Winged Boots) as-is — map loot.
```

Job IDs (carry over known, verify the rest in-game):

```text
77 = Archer            (confirmed)
83 = Thief             (confirmed)
Ninja job id           (TBD - verify; Ch3 debut, 031)
```

## Job Escalation (Chapter 4 rule)

```text
CHANGE: swap ONE Thief -> a second NINJA, so the band reads 2 Ninja + 1 Thief + 3 Archer.
WHY: the fight's identity is "fast wall-climbing flankers on a vertical plateau." The single, fitting
  escalation for a 4/5★ mountain fight is to make the NINJA the apex demand — two dual-wielding,
  wall-climbing, Throw-capable ledge-assassins turn the verticality into the real threat, exactly the
  movement-pressure the high star rating implies. The remaining Thief keeps the Steal harass, so the
  "pin the climbers before they rob you and scatter" read survives. It INTENSIFIES the existing puzzle
  (mobility + theft + ledges) without adding a brand-new mechanic.
CONSTRAINT: Ninja Throw = ranged DAMAGE, not a status lock (031); Thief Steal/charm = minor harass, no
  hard lock. Keep enemy Move/Jump high (the mobility) but levels in-band (101-103).
WHAT IS NOT CHANGED: the multi-level plateau, the 3 Archers' ledge chip, the high mobility, and the
  optional Invisibility-Cloak dig remain. No boss, no rare. Still a skirmish.
```

## Sanctioned exceptions (carried precedents)

```text
NINJA THROW / WALL-CLIMB — ranged damage + mobility; pin/intercept counters (031). Not a lock.
THIEF STEAL/CHARM — minor harass on the remaining Thief; counterable, no hard lock (Ch2/Ch3 precedent).
HIGH MOVE/JUMP — a stat/terrain feature, not a status; preserved as the mobility identity.
BURIED-TREASURE DIG (Invisibility Cloak) — vanilla optional side-objective (low-Brave Chemist +
  Treasure Hunter); preserved untouched. We do NOT add/buff it; it is existing map behavior.
No NEW exception introduced.
```

## Boss rare loot

```text
None. No named boss here — no rare boss item (per the Chapter 4 overview tiering). Generics stay
Chapter-4 shop-tier. The buried Invisibility Cloak + Germinas Boots / Winged Boots are EXISTING map
loot — leave as-is.
```

## Proposed Composition (New Game++ Mount Germinas v1)

Keep the count (6) and the 4/5★ vertical-skirmish feel; swap one Thief for a second Ninja. Band
`101`–`103` (terrain carries the difficulty). Ninjas are the threats; Archers chip; Thief harasses.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Ninja | Ninja | `103` | Apex wall-climber / Throw — the ledge-assassin threat. |
| n | Ninja (NEW) | Ninja | `102` | Second climber — pins the back-line; the escalation. |
| n | Thief | Thief | `101` | Fast Steal harass using the ledges. |
| n | Archer | Archer | `102` | Ranged chip from the high plateau. |
| n | Archer | Archer | `101` | Second archer; covers a second tier. |
| n | Archer | Archer | `101` | Third archer; crossfire over the climb. |

Reasoning:

The faithful move is to **lean into verticality + mobility and let the terrain rate the fight**. Two
Ninjas make the wall-climbing, Throw-capable assassin pressure the defining demand (the 4/5★ identity),
while a Thief keeps the gear-theft harass and three Archers own the ledges with crossfire. The optional
Invisibility-Cloak dig stays as the multitasking side-objective. Levels stay in-band (`101`–`103`, one
`103` anchor on the apex Ninja) because the difficulty must come from movement, theft, and elevation —
not a number spike — keeping it a skirmish, not a boss fight, right before Limberry.

## Builds (Chapter-4 quality; mountain-bandit/assassin flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Ninja x2 (Lv 103 / 102) — apex climbers

```text
Job: Ninja (id TBD)   JobLevel: 8   Secondary: Throw
Reaction: First Strike (453)   Support: Attack Boost (465)   Movement: Movement +2 (487)
Head: Thief's Cap (168)   Body: Black Garb (198)   Accessory: Germinas Boots (210)
Right hand: shop ninja blade (id TBD)   Left: shop ninja blade (id TBD) / dual-wield
```

Role: wall-climbing dual-wield flankers; Throw as ranged damage — pin/intercept to answer.

### Thief (Lv 101) — harass

```text
Job: Thief (83)   JobLevel: 8   Secondary: Steal
Reaction: First Strike (453)   Support: Attack Boost (465)   Movement: Movement +2 (487)
Head: Thief's Cap (168)   Body: Black Garb (198)   Accessory: Germinas Boots (210)
Right hand: Air Knife (9)   Left: none / two-hand marker (254)
```

Role: fast Steal harass using the ledges; minor, counterable.

### Archer x3 (Lv 102 / 101 / 101) — ledge crossfire

```text
Job: Archer (77)   JobLevel: 8   Secondary: none
Reaction: Reflexes (449)   Support: Concentration (469)   Movement: Movement +1 (486)
Head: Thief's Cap (168)   Body: Black Garb (198)   Accessory: Bracers (218)
Right hand: shop high-tier bow (id TBD)   Left: none / two-hand marker (254)
```

Role: tiered ranged chip from the plateau; punishes a slow, clumped climb.

## Positioning Plan

```text
Multi-level plateau: stack the enemy across the TIERS — the two Ninjas on the upper ledges (wall-climb
  arcs onto the player back-line), the three Archers spread across two elevation bands for crossfire,
  the Thief roving a flank. The buried Invisibility-Cloak tile sits out on the map so the optional dig
  pulls a fragile Chemist into contested ground (the multitasking layer).
Preserve the verticality + high Move (the mobility puzzle) — do NOT flatten the plateau.
Keep it a skirmish: in-band levels, no boss, no rare; the terrain + climbers rate it 4/5★.
```

The peak should say: "a nest of cliff-running cutthroats — pin the climbers and hold the ledges, and
if you're bold, send a digger for the cloak while the knives are flying."

## Implementation Checklist

- [ ] Identify Mount Germinas `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify 3 Archer + 2 Thief + 1 Ninja + the Invisibility-Cloak tile + player slots.
- [ ] Swap ONE Thief -> Ninja (2 Ninja + 1 Thief + 3 Archer); keep Throw as ranged damage.
- [ ] Keep the multi-level plateau geometry + high Move/Jump; keep the buried Invisibility-Cloak dig.
- [ ] Set levels: apex Ninja `103`, second Ninja + one Archer `102`; Thief + two Archers `101`.
- [ ] Keep Steal on the Thief (minor harass); no hard lock anywhere.
- [ ] Set JobLevel `8` on all active enemy slots.
- [ ] Patch via the correct layer; keep the diff inside the Mount Germinas window only.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify verticality + dig intact.
- [ ] Install mod, test from a New Game+ save; confirm it plays as a 4/5★ vertical mobility/steal skirmish.

## Test Questions

- Does the verticality + high mobility still define the fight (pin the climbers, hold the ledges)?
- Do the two Ninjas read as the apex threat without a hard lock (Throw = damage, not status)?
- Is the Thief's Steal a minor harass, not a swing factor?
- Is the optional Invisibility-Cloak dig still viable (the multitasking side-objective preserved)?
- Are levels kept in-band (101-103) so terrain — not a number spike — carries the 4/5★ difficulty?
- Does it read as a cliff-running ambush, a clear step up from the chapter's 3/5★ fields, before Limberry?

## Sources

- Game8, "Mount Germinas Walkthrough (Battle 40)": roster (3 Archer + 2 Thief + 1 Ninja), "Defeat all
  enemies!", rec ~59, 4/5 stars, deploy 5, mountain-plateau multi-elevation terrain, buried Invisibility
  Cloak (low-Brave Chemist + Treasure Hunter), rewards (36,200 Gil, Germinas Boots, Winged Boots).
  https://game8.co/games/Final-Fantasy-Tactics/archives/553200
- Final Fantasy Wiki, "Germinas Peak": story/terrain context.
  https://finalfantasy.fandom.com/wiki/Germinas_Peak
- Local: `037-chapter-4-overview.md` (rules), `031-walled-city-yardrow.md` (Ninja debut),
  `043-fort-besselat-wall.md` (vertical-skirmish handling).
```
</content>
