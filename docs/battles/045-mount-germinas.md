# 045 - Mount Germinas (Germinas Peak)

Status: 🧪 v3 implemented — direct in-game playtest pending
Chapter: 4 — "In the Name of Love"
Battle order: Battle 40 (after Bethla Sluice)
Target version: Enhanced v1.5.0
ENTD: global entry **452** (local entry 68, `battle_entd4_ent.bin`)
File: `battle_entd4_ent.bin` (embedded NG+ swap) — `tools/battle_patch.py germinas`

> **NG++ reward applied (2026-06-27):** the ninja arsenal - Ninja Gear (s0, Ninja) + Koga Blade (s1, Ninja)
> + Iga Blade (s2, Thief). The two prior minor spoils (s1 item212, s2 Germinas Boots) were overwritten so
> the three ninja items are the awarded 3. Guaranteed Spoils of War (ENTD 0x1e), NG+ only, within the
> 3-cap, no steal needed. Canonical map: `chapter-4-rewards-implementation.md`.

Current v3 implementation (entry 452, statically verified):
- s0 Apex Ninja L102; s1 Barehand Ninja L101; s2 Martial Thief L101.
- s3 Yoichi Archer L102; s4 Throw Thief L100; s5 Yoichi Archer L100.
- Roster is 2 Ninjas + 2 Thieves + 2 Archers; the three Martial Arts users are s0/s1/s2.
- No boss; in-band levels (terrain rates it 4/5★). Ninja arsenal rewards remain guaranteed spoils.
  Plateau geometry, positions, event data, and buried Invisibility Cloak layer are untouched.

The v3 redesign keeps the vertical bandit identity but hardens the fight against all-party Shihadori.
The anti-Shihadori answer is
not magic or Geomancy; it is Martial Arts on fast cliff-runners, using Aurablast/Shockwave while the
Yoichi Archers and Throw Thief maintain high-ground and flank pressure. Rewards remain guaranteed
spoils, not Steal- or equipment-dependent. The cloak route must be buffered by placement: one anti-
Shihadori unit can threaten it, but the whole team must not collapse on it immediately.

> Data-layer fields and slot offsets were confirmed against the real entry 452. The embedded ENTD is
> installed in the Reloaded-II mod; see `037-chapter-4-overview.md` for chapter context.

## Design Goal

```text
Make Mount Germinas a hard vertical mobility skirmish: two Ninjas and two Thieves race over the plateau,
three Martial Arts users stop all-party Shihadori from trivializing the fight, Archers own the height
with Yoichi Bow pressure, and the optional Invisibility Cloak dig remains viable. The fight should feel
like speed, Jump, terrain, and target priority, not status, magic, or raw level inflation.
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
- Planned v3 roster is 2 Ninjas + 2 Thieves + 2 Archers.
- No active guest, no boss.
- Reward ledger maps this battle to Ninja Gear + Koga Blade + Iga Blade guaranteed spoils.
- The buried Invisibility Cloak is a protected vanilla map-treasure side objective.

V3 IMPLEMENTATION CONFIRMED:
- Exact active slot order and positions were preserved from entry 452.
- Koga/Iga/Ninja Gear are equipped legally on the Apex Ninja and remain guaranteed spoils.
- OverrideEntryData leaves the relevant unit build fields to the embedded ENTD.
- Multi-level plateau geometry, unit positions, event data, and map treasure were not edited.

STILL NEEDED IN GAME:
- Confirm Martial Arts commands, especially Aurablast/Shockwave, bypass Shihadori as expected in TIC.
- Confirm the optional Invisibility Cloak route remains practical with the v3 pressure lanes.
```

Confirmed job IDs from the installed tables:

```text
77 = Archer
78 = Monk
83 = Thief
88 = Samurai
89 = Ninja
93 = Mime              (91 is Bard)
```

## Enemy Party Escalation (Chapter 4 rule)

```text
CHANGE: swap one Archer into a second NINJA, so the band reads 2 Ninja + 2 Thief + 2 Archer.
WHY: the fight's identity is "fast wall-climbing flankers on a vertical plateau," but a pure physical
  Throw/bow plan loses too hard to all-party Shihadori. The faithful Ch4 escalation is to keep the
  speed/Jump/thief-ninja fantasy while adding 3 Martial Arts users as real Shihadori answers: Apex
  Ninja, Second Ninja, and Martial Thief. They use Aurablast/Shockwave to punish parry-stacking without
  turning the fight into a caster or Geomancy map.
CONSTRAINT: the anti-Shihadori plan must stay physical-mobility flavored. No Geomancy low-MA chip, no
  caster secondary, no hard status. Yoichi Archers remain high-ground pressure but are not treated as
  Shihadori counters. Keep most enemies at `100`–`101`, with only two anchors at `102`.
REJECTED DEFAULTS: no single anti-Shihadori unit, no third Ninja, no hard-status ledges, no magic/MA
  package, no overlevelled peak. The optional dig must remain possible without sacrificing a unit.
WHAT IS NOT CHANGED: the multi-level plateau, fast climbers, thief/ninja pressure, Archer ledge chip,
  high mobility, and optional Invisibility-Cloak dig remain. No boss. Still a skirmish.
```

## Sanctioned exceptions (carried precedents)

```text
MARTIAL ARTS ANTI-SHIHADORI — Aurablast/Shockwave on fast bodies are the battle's sanctioned parry
  answer. This is damage pressure, not hard control, and it stays inside the mountain-assassin fantasy.
NINJA THROW / WALL-CLIMB — ranged damage + mobility; pin/intercept counters (031). Not a lock.
THIEF THROW / DUAL WIELD — fast physical pressure and cleanup; useful against non-parry targets, but
  not counted as a Shihadori bypass.
YOICHI BOW LEDGE CHIP — strong high-ground physical pressure. Item/Throw Items support the role, but
  bows are not treated as Shihadori counters.
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
COMBAT ROLE: the Apex Ninja may use Ninja Gear/Koga/Iga as the visible apex reward kit where job
equipment rules allow it. Do not force Koga/Iga onto non-legal users just to make rewards visible.
PRESERVE: buried Invisibility Cloak and other map treasure remain vanilla map loot and are not the NG++
reward channel.
```

## Proposed Composition (New Game++ Mount Germinas v3)

Keep the count (6) and the 4/5★ vertical-skirmish feel; relative to the existing v1 implementation, one
Archer becomes the second Thief so the roster reaches the documented 2/2/2 shape. Every active
human has a complete kit and a JobLevel 8 bucket. Band `100`–`102`, with four of six enemies at
`100`–`101`; terrain and kits carry the difficulty.
The headline is fast Martial Arts on vertical bodies; Archers and Throw Thief punish everything that is
not protected by Shihadori.

| Slot | Role | Job | Job bucket | Level | Br/Fa | Purpose |
| ------ | ------ | ----- | ----- | ------- | --- | --------- |
| s0 `(4,6)` | Apex Ninja | Ninja | Samurai `JL8` | `102` | `90/35` | Reward-kit assassin; Shihadori + Martial Arts answer. |
| s1 `(1,4)` | Barehand Ninja | Ninja | Monk `JL8` | `101` | `90/38` | Brawler cliff-runner; barehand Martial Arts pressure. |
| s2 `(5,0)` | Martial Thief | Thief | Monk `JL8` | `101` | `88/38` | Fast barehand thief; third Aurablast/Shockwave line. |
| s4 `(4,4)` | Throw Thief | Thief | Ninja `JL8` | `100` | `88/38` | Central dual-wield/Throw flanker; cleans up non-parry targets. |
| s3 `(9,0)` | Archer | Archer | Mime `JL8` | `102` | `82/45` | Yoichi Bow high-ground pressure; Item utility. |
| s5 `(7,4)` | Archer | Archer | Mime `JL8` | `100` | `82/45` | Second Yoichi angle; Item utility from another ledge. |

Reasoning:

The faithful move is to **lean into verticality + speed while making Shihadori a checked strategy, not a
win button**. Three enemies can threaten Shihadori builds with Martial Arts: the apex Ninja, a barehand
Monk-bucket Ninja, and a barehand Monk-bucket Thief. The Throw Thief and Yoichi Archers keep the original
bandit crossfire and punish parties that do not bring parry, but they are not counted as parry answers.
The optional Invisibility-Cloak dig stays as the multitasking side-objective. Levels stay in-band
(`100`–`102`, only the Apex Ninja and primary Archer at `102`) because the difficulty must come from speed,
positioning, and target priority — not a number spike — keeping it a skirmish, not a boss fight, right
before Limberry.

Rejected variants:

```text
- v1 partial setup: correct two-Ninja shape, but incomplete for Chapter 4 humans.
- v2 two-Ninja cliff band: too easy if the player stacks Shihadori across the party.
- Single anti-Shihadori Ninja: too fragile as the only answer; kill/control it and the map collapses.
- Geomancy/caster secondary: solves parry, but shifts the map away from speed/Jump/PA into MA logic.
- Third Ninja: makes the Invisibility Cloak dig too punitive and overstates the Ninja escalation.
- Hard-status / Charm thief band: wrong for a mobility skirmish.
- Archer rare-bow crossfire without Martial Arts: adds pressure but still folds to all-party Shihadori.
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

### Apex Ninja (Lv 102) — reward-kit anti-Shihadori assassin

```text
Job: Ninja (89)   JobLevel: 8
Job bucket: Samurai   JobLevel: 8
Secondary: Martial Arts
Reaction: Shihadori
Support: Brawler
Movement: Jump +3
Right hand: Koga Blade   Left hand: Iga Blade
Head: Thief's Cap   Body: Ninja Gear   Accessory: Bracers
```

Role: primary apex threat. Koga/Iga + Ninja Gear make the reward kit visible, while Martial Arts gives
Aurablast/Shockwave pressure into Shihadori-heavy parties.

### Barehand Ninja (Lv 101) — Monk-bucket cliff-runner

```text
Job: Ninja (89)   JobLevel: 8
Job bucket: Monk   JobLevel: 8
Secondary: Martial Arts
Reaction: First Strike
Support: Brawler
Movement: Movement +3
Right hand: none   Left hand: none
Head: Headband   Body: Power Garb   Accessory: Bracers
```

Role: fast barehand attacker. Brawler + Headband + Power Garb turns Martial Arts into the second real
anti-Shihadori line without adding magic.

### Martial Thief (Lv 101) — Monk-bucket pressure thief

```text
Job: Thief (83)   JobLevel: 8
Job bucket: Monk   JobLevel: 8
Secondary: Martial Arts
Reaction: Reflexes
Support: Brawler
Movement: Movement +3
Right hand: none   Left hand: none
Head: Headband   Body: Power Garb   Accessory: Bracers
```

Role: third anti-Shihadori threat. It is weaker than the Ninjas, but fast enough to stop the player from
solving the entire map by killing one Martial Arts unit.

### Throw Thief (Lv 100) — Ninja-bucket flanker

```text
Job: Thief (83)   JobLevel: 8
Job bucket: Ninja   JobLevel: 8
Secondary: Throw
Reaction: Speed Surge
Support: Dual Wield
Movement: Jump +3
Right hand: Zwill Straightblade   Left hand: Assassin's Dagger
Head: Thief's Cap   Body: Power Garb   Accessory: Bracers
```

Role: preserves the thief/throw flavor and punishes non-parry targets. Not counted as a Shihadori
bypass.

### Archer x2 (Lv 102 / 100) — Yoichi ledge crossfire

```text
Job: Archer (77)   JobLevel: 8
Job bucket: Mime   JobLevel: 8
Secondary: Item
Reaction: Reflexes (449)
Support: Throw Items
Movement: Jump +3
Right hand: Yoichi Bow
Head: Thief's Cap   Body: Power Garb   Accessory: Bracers
```

Role: high-ground pressure and emergency Item utility. They do not use Aim as secondary because Aim is
already their primary command, and they are not treated as Shihadori counters.

## Positioning Plan

```text
Multi-level plateau: stack the enemy across the TIERS — the Apex Ninja and Barehand Ninja start on
  separate upper-ledges, the Martial Thief starts near the cloak-side pressure lane, the Throw Thief
  roves the opposite flank, and the two Yoichi Archers spread across two elevation bands for crossfire.
  The buried Invisibility-Cloak tile sits out on the map so the optional dig pulls a fragile Chemist
  into contested ground, but only one anti-Shihadori unit should threaten that lane immediately; the
  other two must take at least a little movement/time to collapse on it.
Preserve the verticality + high Move/Jump (the mobility puzzle) — do NOT flatten the plateau.
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

Current v3 validation note:

```text
No new simulation was requested for this implementation; validation is intentionally deferred to the
user's direct in-game test. Static validation covers roster, jobs, buckets, complete kits, positions,
unit IDs, and preserved spoils. The playtest must confirm Martial Arts behavior and cloak-route fairness.
```

Previous v2 result:

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
REPLACE v2 complete ninja cliff band with v3 Shihadori-checked cliff band.
Iteration 1 rejected the same roster because both Ninjas collapsing on the cloak route made the optional
dig too unsafe. v3 keeps the same positioning lesson: only one anti-Shihadori unit can threaten the
cloak lane immediately.
```

## Implementation Checklist

- [x] Confirm current entry 452 slot order and map each v3 role to the intended enemy slots.
- [x] Confirm Invisibility-Cloak tile and map treasure behavior remain untouched by the ENTD patch.
- [x] Apply v3 roster: 2 Ninja + 2 Thief + 2 Archer.
- [x] Keep the multi-level plateau geometry + high Move/Jump; keep the buried Invisibility-Cloak dig.
- [x] Preserve the existing positions; s4 becomes the Throw Thief while s3/s5 retain separate bow angles.
- [x] Set levels: Apex Ninja and primary Archer `102`; Barehand Ninja and Martial Thief `101`; Throw
  Thief and second Archer `100`.
- [x] Set JobLevel `8` on every main job and every requested job bucket: Samurai, Monk, Ninja, Mime.
- [x] Give Apex Ninja Samurai bucket, Martial Arts secondary, Shihadori, Brawler, Jump +3, Koga Blade,
  Iga Blade, Thief's Cap, Ninja Gear, and Bracers.
- [x] Give Barehand Ninja Monk bucket, Martial Arts secondary, First Strike, Brawler, Movement +3,
  bare hands, Headband, Power Garb, and Bracers.
- [x] Give Martial Thief Monk bucket, Martial Arts secondary, Reflexes, Brawler, Movement +3, bare hands,
  Headband, Power Garb, and Bracers.
- [x] Give Throw Thief Ninja bucket, Throw secondary, Speed Surge, Dual Wield, Jump +3, dual daggers,
  Thief's Cap, Power Garb, and Bracers.
- [x] Give both Archers Mime bucket, Item secondary, Reflexes, Throw Items, Jump +3, Yoichi Bow,
  Thief's Cap, Power Garb, and Bracers.
- [ ] Confirm Martial Arts Aurablast/Shockwave bypass Shihadori in-game.
- [x] Give every active human complete equipment plus secondary/reaction/support/movement.
- [x] Preserve guaranteed spoils: Ninja Gear + Koga Blade + Iga Blade.
- [x] Equip reward gear only where job legality supports it; otherwise keep reward as spoils payload.
- [x] Patch via the embedded ENTD; keep the binary diff inside entry 452 (plus requested Sluice retune).
- [x] Re-dump and statically validate; positions, flags, unit IDs, and spoils remain intact.
- [x] Install the rebuilt mod in Reloaded-II.
- [ ] Test from a New Game+ save; confirm it plays as a 4/5★ vertical mobility/steal skirmish.

## Test Questions

- Does the verticality + high mobility still define the fight (pin the climbers, hold the ledges)?
- Do the three Martial Arts users create enough anti-Shihadori pressure without turning the map into a
  cleanup slog?
- Does killing one anti-Shihadori unit still leave at least one meaningful parry answer alive?
- Do the two Yoichi Archers pressure non-parry targets without pretending to bypass Shihadori?
- Does the Throw Thief preserve thief/ninja flavor without becoming the real headline?
- Is the optional Invisibility-Cloak dig still viable (the multitasking side-objective preserved)?
- Do the anti-Shihadori units start on separate lanes so the cloak dig is contested, not immediately
  collapsed?
- Do all active humans have complete equipment plus secondary/reaction/support/movement?
- Do Ninja Gear/Koga/Iga pay through guaranteed spoils, without requiring Steal or illegal equipment?
- Are levels kept in-band (`100`–`102`) so terrain — not a number spike — carries the 4/5★ difficulty?
- Does it read as a cliff-running ambush, a clear step up from the chapter's 3/5★ fields, before Limberry?

## Sources

- Game8, "Mount Germinas Walkthrough (Battle 40)": roster (3 Archer + 2 Thief + 1 Ninja), "Defeat all
  enemies!", rec ~59, 4/5 stars, deploy 5, mountain-plateau multi-elevation terrain, buried Invisibility
  Cloak (low-Brave Chemist + Treasure Hunter), rewards (36,200 Gil, Germinas Boots, Winged Boots).
  https://game8.co/games/Final-Fantasy-Tactics/archives/553200
- Final Fantasy Wiki, "Germinas Peak": story/terrain context.
  https://finalfantasy.fandom.com/wiki/Germinas_Peak
- Local: `037-chapter-4-overview.md` (rules), `031-walled-city-yardrow.md` (Ninja debut),
  `043a-fort-besselat-south-wall.md` / `043b-fort-besselat-north-wall.md` (vertical-skirmish handling),
  `chapter-4-rewards-implementation.md` (Ninja Gear + Koga + Iga guaranteed spoils).
