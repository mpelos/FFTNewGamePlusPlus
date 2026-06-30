# 045 - Mount Germinas (Germinas Peak)

Status: 📝 redesign v2 planned (docs-only) — v1 implementation exists for entry 452
Chapter: 4 — "In the Name of Love"
Battle order: Battle 40 (after Bethla Sluice)
Target version: Enhanced v1.5.0
ENTD: global entry **452** (local entry 68, `battle_entd4_ent.bin`)
File: `battle_entd4_ent.bin` (embedded NG+ swap) — `tools/battle_patch.py germinas`

> **NG++ reward applied (2026-06-27):** the ninja arsenal - Ninja Gear (s0, Ninja) + Koga Blade (s1, Ninja)
> + Iga Blade (s2, Thief). The two prior minor spoils (s1 item212, s2 Germinas Boots) were overwritten so
> the three ninja items are the awarded 3. Guaranteed Spoils of War (ENTD 0x1e), NG+ only, within the
> 3-cap, no steal needed. Canonical map: `chapter-4-rewards-implementation.md`.

Current implementation (entry 452, vanilla-dump verified) — slots: s0 Ninja, s1,s2 Thief, s3,s4,s5 Archer:
- s0 Ninja L103 (apex) + s1 Thief→**Ninja** L102 — dual Ninja Longblades; Thief's Cap/Black Garb/Germinas; First Strike/Atk Boost/Mv+2.
- s2 Thief L101 — Air Knife; Steal harass; First Strike/Atk Boost/Mv+2.
- s3 Archer L102, s4,s5 Archer L101 — Thief's Cap/Black Garb/Bracers/Windslash (two-hand); Reflexes/Concentration/Mv+1.
- No boss; in-band levels (terrain rates it 4/5★). Ninja arsenal rewards are applied through spoils.
  Plateau geometry + buried Invisibility Cloak (other layer) untouched.

Planned v2 redesign (docs-only in this pass): keep the two-Ninja shape, make every active human a
complete Chapter-4 unit, and let Ninja Gear/Koga/Iga be visible only where job-equipment legality
supports it. Rewards remain guaranteed spoils, not Steal- or equipment-dependent. The cloak route must
be buffered by placement: one Ninja can threaten it, but both Ninjas must not collapse on it immediately.

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `037-chapter-4-overview.md`.

## Design Goal

```text
Make Mount Germinas a moderate+ vertical mobility skirmish: two Ninjas are the apex ledge threat,
the Thief preserves steal pressure, Archers own the height, and the optional Invisibility Cloak dig
remains viable. The fight should feel like terrain and movement, not status or raw level inflation.
```

No active guests appear here. No guest-control implementation is needed for this battle.

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

## Local Data Confirmed / Data Still Needed

```text
CONFIRMED:
- Entry 452 is the Mount Germinas ENTD entry.
- Current v1 roster is 2 Ninjas + 1 Thief + 3 Archers.
- No active guest, no boss.
- Reward ledger maps this battle to Ninja Gear + Koga Blade + Iga Blade guaranteed spoils.
- The buried Invisibility Cloak is a protected vanilla map-treasure side objective.

STILL NEEDED FOR V2 IMPLEMENTATION:
- Confirm exact slot order before patching complete v2 kits.
- Confirm Koga/Iga/Ninja Gear active equipment only where job legality supports it.
- Confirm whether OverrideEntryData carries level for this battle or leaves it at runtime scale.
- Preserve multi-level plateau geometry, high Move/Jump, and the Invisibility Cloak dig tile.
- Preserve other map treasure behavior as vanilla map loot.
```

Job IDs (carry over known, verify the rest in-game):

```text
77 = Archer            (confirmed)
83 = Thief             (confirmed)
Ninja job id           (TBD - verify; Ch3 debut, 031)
```

## Enemy Party Escalation (Chapter 4 rule)

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
REJECTED DEFAULTS: no third Ninja, no hard-status ledges, no illegal visible reward equipment, and no
  overlevelled peak. The optional dig must remain possible without sacrificing a unit.
WHAT IS NOT CHANGED: the multi-level plateau, the 3 Archers' ledge chip, the high mobility, and the
  optional Invisibility-Cloak dig remain. No boss. Still a skirmish.
```

## Sanctioned exceptions (carried precedents)

```text
NINJA THROW / WALL-CLIMB — ranged damage + mobility; pin/intercept counters (031). Not a lock.
THIEF STEAL/CHARM — minor harass on the remaining Thief; counterable, no hard lock (Ch2/Ch3 precedent).
HIGH MOVE/JUMP — a stat/terrain feature, not a status; preserved as the mobility identity.
BURIED-TREASURE DIG (Invisibility Cloak) — vanilla optional side-objective (low-Brave Chemist +
  Treasure Hunter); preserved untouched. We do NOT add/buff it; it is existing map behavior.
ROLE-FITTING NINJA ARSENAL — Ninja Gear/Koga/Iga may appear as visible combat gear only where legal;
  otherwise they remain guaranteed spoils payloads.
No hard-control exception introduced.
```

## Rare/reward handling

```text
Guaranteed spoils for entry 452: NINJA GEAR + KOGA BLADE + IGA BLADE.
These are delivered by the Spoils of War reward channel; the player must never be required to Steal.
COMBAT ROLE: the two Ninjas may use Ninja Gear/Koga/Iga only where job equipment rules allow it. Do not
force Iga/Koga onto non-legal users just to make rewards visible.
PRESERVE: buried Invisibility Cloak and other map treasure remain vanilla map loot and are not the NG++
reward channel.
```

## Proposed Composition (New Game++ Mount Germinas v2)

Keep the count (6) and the 4/5★ vertical-skirmish feel; one Thief remains swapped into a second Ninja.
Every active human has a complete kit. Band `101`–`103` (terrain carries the difficulty). Ninjas are
the threats; Archers chip; Thief harasses.

| Slot | Role | Job | Level | Br/Fa | Purpose |
| ------ | ------ | ----- | ------- | --- | --------- |
| n | Apex Ninja | Ninja | `103` | `90/35` | Apex wall-climber / Throw; legal Ninja Gear/Koga/Iga pressure if available. |
| n | Ninja | Ninja | `102` | `90/35` | Second climber; legal ninja arsenal pressure if available. |
| n | Thief | Thief | `101` | `88/38` | Fast Steal harass using the ledges. |
| n | Archer | Archer | `102` | `82/45` | Ranged chip from the high plateau. |
| n | Archer | Archer | `101` | `82/45` | Second archer; covers a second tier. |
| n | Archer | Archer | `101` | `82/45` | Third archer; crossfire over the climb. |

Reasoning:

The faithful move is to **lean into verticality + mobility and let the terrain rate the fight**. Two
Ninjas make the wall-climbing, Throw-capable assassin pressure the defining demand (the 4/5★ identity),
while a Thief keeps the gear-theft harass and three Archers own the ledges with crossfire. The optional
Invisibility-Cloak dig stays as the multitasking side-objective. Levels stay in-band (`101`–`103`, one
`103` anchor on the apex Ninja) because the difficulty must come from movement, theft, and elevation —
not a number spike — keeping it a skirmish, not a boss fight, right before Limberry.

Rejected variants:

```text
- v1 partial setup: correct two-Ninja shape, but incomplete for Chapter 4 humans.
- Spoils-only ninja arsenal: acceptable fallback if active reward gear overperforms, but too soft in the model.
- Third Ninja: makes the Invisibility Cloak dig too punitive.
- Hard-status / Charm thief band: wrong for a mobility skirmish.
- Archer rare-bow crossfire: adds unrelated reward pressure.
- Overlevelled peak: makes numbers, not terrain, carry the fight.
- Mandatory cloak dig: violates the optional side-objective.
```

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
Right hand/Left hand: Koga/Iga/other legal ninja blade only where legal; otherwise shop ninja blades.
Body: Ninja Gear on a Ninja only if legal and playtest-safe; otherwise reward payload only.
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
Job: Archer (77)   JobLevel: 8   Secondary: Item, limited to Potion/Remedy utility; no Phoenix Down loop.
Reaction: Reflexes (449)   Support: Concentration (469)   Movement: Movement +1 (486)
Head: Thief's Cap (168)   Body: Black Garb (198)   Accessory: Bracers (218)
Right hand: shop high-tier bow (id TBD)   Left: none / two-hand marker (254)
```

Role: tiered ranged chip from the plateau; punishes a slow, clumped climb.

## Positioning Plan

```text
Multi-level plateau: stack the enemy across the TIERS — the two Ninjas on separate upper ledges
  (wall-climb arcs onto different player lanes), the three Archers spread across two elevation bands
  for crossfire, the Thief roving a flank. The buried Invisibility-Cloak tile sits out on the map so
  the optional dig pulls a fragile Chemist into contested ground, but only one Ninja should threaten
  that lane immediately; the other starts on a separate flank so the dig stays optional and viable.
Preserve the verticality + high Move (the mobility puzzle) — do NOT flatten the plateau.
Keep it a skirmish: in-band levels, no boss; rewards pay through spoils while terrain + climbers rate
it 4/5★.
```

The peak should say: "a nest of cliff-running cutthroats — pin the climbers and hold the ledges, and
if you're bold, send a digger for the cloak while the knives are flying."

## Simulation Plan and Results

Simulation artifact:

```text
tmp/fft-level-design-045-mount-germinas/
  assumptions.md
  simulate.py
  iteration-1-results.json
  iteration-1-results.md
  iteration-2-results.json
  iteration-2-results.md
  iteration-results.json
  iteration-results.md
```

Model scope:

```text
Coarse deterministic vertical-skirmish model over the first five rounds.
It scores pressure, vertical identity, answerability, dig safety, reward safety, and hard-lock risk.
It does not simulate exact FFT formulas.
```

Final iteration result:

| Candidate | Pressure | Vertical identity | Answer | Dig safety | Reward safe | Hard lock | Verdict |
|---|---:|---:|---:|---:|---:|---:|---|
| v1 partial cliff band | 172 | 100 | 70 | 57 | 100 | 0 | Rejected: incomplete setup |
| v2 complete ninja cliff band | 180 | 100 | 70 | 65 | 100 | 0 | **Accepted** |
| spoils-only ninja arsenal | 162 | 96 | 82 | 57 | 90 | 0 | Rejected: too soft |
| third ninja cliff trap | 194 | 64 | 52 | 52 | 100 | 0 | Rejected: third Ninja |
| hard-status thief band | 235 | 72 | 45 | 39 | 100 | 50 | Rejected: hard status |
| archer rare-bow crossfire | 200 | 84 | 60 | 57 | 80 | 0 | Rejected: unrelated reward pressure |
| overlevelled peak | 202 | 100 | 62 | 45 | 100 | 0 | Rejected: overlevel |
| mandatory cloak dig | 192 | 100 | 70 | 39 | 75 | 0 | Rejected: mandatory side objective |

Iteration decision:

```text
ACCEPT v2 complete ninja cliff band.
Iteration 1 rejected the same roster because both Ninjas collapsing on the cloak route made the optional
dig too unsafe. Iteration 2 keeps the roster and adds a positioning rule: one Ninja can threaten the
cloak lane, while the other starts on a separate flank.
```

## Implementation Checklist

- [ ] Confirm current entry 452 slot order: 2 Ninja + 1 Thief + 3 Archer + player slots.
- [ ] Confirm Invisibility-Cloak tile and map treasure behavior remain untouched.
- [ ] Preserve the one-Thief -> Ninja swap (2 Ninja + 1 Thief + 3 Archer); keep Throw as ranged damage.
- [ ] Keep the multi-level plateau geometry + high Move/Jump; keep the buried Invisibility-Cloak dig.
- [ ] Position Ninjas on separate threat lanes; only one can immediately pressure the cloak dig route.
- [ ] Set levels: apex Ninja `103`, second Ninja + one Archer `102`; Thief + two Archers `101`.
- [ ] Keep Steal on the Thief (minor harass); no hard lock anywhere.
- [ ] Give every active human complete equipment plus secondary/reaction/support/movement.
- [ ] Preserve guaranteed spoils: Ninja Gear + Koga Blade + Iga Blade.
- [ ] Equip reward gear only where job legality supports it; otherwise keep reward as spoils payload.
- [ ] Set JobLevel `8` on all active enemy slots.
- [ ] Patch via the correct layer; keep the diff inside the Mount Germinas window only.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify verticality + dig intact.
- [ ] Install mod, test from a New Game+ save; confirm it plays as a 4/5★ vertical mobility/steal skirmish.

## Test Questions

- Does the verticality + high mobility still define the fight (pin the climbers, hold the ledges)?
- Do the two Ninjas read as the apex threat without a hard lock (Throw = damage, not status)?
- Is the Thief's Steal a minor harass, not a swing factor?
- Is the optional Invisibility-Cloak dig still viable (the multitasking side-objective preserved)?
- Do the Ninjas start on separate lanes so the cloak dig is contested, not immediately collapsed?
- Do all active humans have complete equipment plus secondary/reaction/support/movement?
- Do Ninja Gear/Koga/Iga pay through guaranteed spoils, without requiring Steal or illegal equipment?
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
  `043-fort-besselat-wall.md` (vertical-skirmish handling),
  `chapter-4-rewards-implementation.md` (Ninja Gear + Koga + Iga guaranteed spoils).
