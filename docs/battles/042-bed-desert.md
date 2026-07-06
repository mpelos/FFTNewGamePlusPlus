# 042 - Beddha Sandwaste (Bed Desert)

Status: 📝 redesign v3 planned (docs-only) — v1 implementation exists for entry 447
Chapter: 4 — "In the Name of Love"
Battle order: Battle 37 (after Outlying Church)
Target version: Enhanced v1.5.0
ENTD: global entry **447** (local entry 63, `battle_entd4_ent.bin`)
File: `battle_entd4_ent.bin` (embedded NG+ swap) — `tools/battle_patch.py bed_desert`

> **NG++ reward applied (2026-06-27):** the full gun trio - Glacial Gun (s0, kept) + Blaze Gun (s1) +
> Blaster (s2), thematic to Barich the machinist. Guaranteed Spoils of War (ENTD 0x1e), NG+ only, within
> the 3-cap, no steal needed. Canonical map: `chapter-4-rewards-implementation.md`.

Current implementation (entry 447, vanilla-dump verified):
- s0 **Barich** (job 43 Machinist, BOSS, dies → reward pays) — L104/jl8; **Glacial Gun (74)**,
  already his equipped weapon (visible steal-bait = tactical disarm); job/secondary/head/body/acc/win-on-death preserved.
- s1,s2 Knight L102 — Heavy gear/Runeblade/shop Shield; Rend innate (cap 2); Counter/Atk Boost/Mv+1.
- s3 Black Mage L102 — Mage Hat/shop Robe/Featherweave/shop Rod; Reflexes/Atk Boost/Mv+1.
- s4,s5 Archer L102/L101 — Thief's Cap/Black Garb/Bracers/Windslash (two-hand); Reflexes/Concentration/Mv+1.
- s6,s7 = job-43 Barich-clone scripting placeholders (jl0) — left untouched. NO Hydra. Only Barich at band 104.
- Barich recurs at Lost Halidom (057) as a Tier-S dragon fight — no double-best (gun paid here only).

Planned v3 redesign (docs-only in this pass): keep the vanilla six-body gun-duel roster, but make every
active human a complete Chapter-4 unit. Barich shifts from the v2 Glacial Gun engine into a more
mobile/evasive Stoneshooter boss package, while the vanilla Knights become Samurai parry screens and
the vanilla Archers become Geomancer terrain bruisers. **Glacial Gun**, **Blaze Gun**, and **Blaster**
stay guaranteed Spoils of War rewards, not extra enemy gun pressure.

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `037-chapter-4-overview.md`.

## Design Goal

```text
Make Bed Desert a clean open-lane gun duel: the player must cross exposed sand, respect Stoneshooter,
disarm Barich if desired, and burst him through a complete ranged screen. The pressure is range,
evasion, terrain, and approach geometry, not dragons, hard control, or a three-gunner pileup.
```

No active guests appear here. No guest-control implementation is needed for this battle.

## Original Battle

Objective:

```text
Defeat Barich!   (the battle ends the instant he falls — he is defeated here)
```

Player deployment:

```text
Up to 5 units, including Ramza. No guests.
```

Original enemy composition (verified via Game8, Battle 37):

```text
Barich Fendsor (Desert)   (BOSS — Knights Templar machinist; GLACIAL GUN — ranged ice nukes)
2x Knight                 (front-line; Rend/break)
2x Archer                 (ranged chip — desert sightlines)
1x Black Mage             (AoE caster)
```

> Correction to the overview's tentative note: there is **NO Hydra** at Bed Desert. The Hydra (and
> Tiamat) appear later, at **Lost Halidom (`052`)**, in the endgame. Bed Desert is Barich's
> long-range **gun-sniper** fight.

Public walkthrough details:

```text
Recommended level: ~43.  Difficulty: 3/5 stars.  Deploy up to 5.  Win: defeat Barich (ends fight).
DESERT open field — long, open sightlines suit ranged play (gun, bows, AoE).
THE THREAT — BARICH'S GLACIAL GUN: fires ICE spells (Blizzard up to Blizzaga) at GUN RANGE — a
  long-range elemental nuke that ignores the usual caster charge time. The walkthrough's tip: equip an
  ICE SHIELD to ABSORB his shots (turn his damage into healing), and/or close the distance.
SUPPORT: two Knights screen, two Archers snipe the open lanes, one Black Mage adds AoE.
Rewards: 30,600 Gil, buried rare Yagyu Darkrood (ninja sword).
```

Design reading:

Bed Desert is **the long-range gun-duel**: Barich is a Knights Templar **machinist** whose **Glacial
Gun** snipes high-tier ice from across the open desert — a ranged nuke with no charge tell. Its
identity is **a distance/elemental puzzle**: the player must **close on the gunner, absorb his element
(Ice Shield), or disarm him**, all while crossing open sand under a ranged screen (Archers + Black
Mage AoE). Because the fight ends when Barich falls, it rewards reaching and bursting the gunner over
trading shots across the dunes.

The v3 New Game++ move is to give him **Stoneshooter as visible steal-bait** — so the disarm line
(Steal Weapon) removes his active gun threat, exactly like disarming Wiegraf's Holy Sword in Ch3,
while the actual Glacial/Blaze/Blaster rewards remain guaranteed through Spoils of War.

For New Game++ the identity must stay: **an open-desert gun-duel — close on / bypass / disarm a
long-range Templar gunner and burst him through a ranged screen — with his active gun as the tempting,
threat-removing steal; the boss is the escalation, the screen stays familiar, and the extra guns are
payout rather than extra combat engines.**

## Local Data Confirmed / Data Still Needed

```text
CONFIRMED:
- Entry 447 is the Bed Desert ENTD entry.
- Current roster is Barich + 2 Knights + 2 Archers + 1 Black Mage.
- Current v1 implementation already sets Barich to L104/JL8 and preserves win-on-Barich-fall scripting.
- No active guest.
- No Hydra here; the dragon-pit Barich rematch belongs to Lost Halidom (`057`).
- Reward ledger currently maps this battle to Glacial Gun + Blaze Gun + Blaster guaranteed spoils.

STILL NEEDED FOR V3 IMPLEMENTATION:
- Confirm exact enemy slot order before patching complete v3 kits.
- Confirm the win condition remains "Defeat Barich" and Barich clone placeholders remain untouched.
- Confirm whether OverrideEntryData carries level for this battle or leaves it at runtime scale.
- Preserve open desert geometry and long sightlines; the distance puzzle is the fight.
- Preserve buried Yagyu Darkrood map treasure as vanilla map loot.
```

Job IDs (carry over known, verify the rest in-game):

```text
Samurai job id         (TBD - verify)
Geomancer job id       (TBD - verify)
Black Mage job id      (TBD - verify)
Knights Templar / Machinist id (TBD - verify; Barich's boss job)
```

## Enemy Party Escalation (Chapter 4 rule)

```text
CHANGE: light generic-slot swap. The escalation is a complete open-desert firing lane around the BOSS —
  Barich is a Knights Templar machinist whose Stoneshooter package creates a mobile/evasive gunner
  threat, while the vanilla Knights become Samurai parry screens instead of break tanks and the
  vanilla Archers become Geomancer terrain bruisers instead of pure bow chip.
WHY: the fight's identity is already "cross open ground and neutralize a long-range gunner."
  The faithful Ch4 escalation is to give the existing screen complete kits while keeping the gun-boss
  as the single headline. The Samurai pin the approach, Geomancers tax terrain lanes, and the Black
  Mage punishes clumps; all of that amplifies crossing the gun lane.
CONSTRAINT: the gun is answerable — closing distance removes the range advantage, Reflexes/Featherweave
  are bypassed by non-evadable pressure, and STEAL WEAPON disarms it. Rewards are guaranteed spoils,
  not steal-gated.
REJECTED DEFAULTS: no Hydra/dragon preview, no active three-gun enemy team, no heavy Disable/
  Immobilize control, no Time Mage crossfire. Those are either the 057 rematch identity or a second
  engine.
WHAT IS NOT CHANGED: the open desert, the 2 front-line screeners + 2 lane punishers + 1 Black Mage
  ranged screen, and the "reach and burst the boss" win line remain. No brand-new caste debuts here.
```

## Sanctioned exceptions (carried precedents)

```text
RANGED BOSS GUN (Barich's Stoneshooter) — allowed as the boss's identity: long-range pressure from the
  named machinist. Counters: close the distance, use non-evadable pressure against Reflexes/
  Featherweave, or Steal Weapon (disarm = the tactical answer). Not a status; race-able; no hard lock.
SAMURAI PARRY SCREEN — the former Knight slots become Samurai with Shirahadori. Counters: magic,
  non-evadable skills, disarm/steal pressure, or ignoring them to reach Barich. This replaces Rend;
  do not also add Knight break pressure here.
BLACK MAGE AoE — boosted elemental, race-able by rushing it (Ch4 opener precedent, 038). Not new.
GEOMANCER TERRAIN BRUISERS — the former Archer slots become Geomancers with Nature's Wrath. Counters:
  range, magic, disabling the bruisers, or forcing them off ideal terrain. This preserves lane pressure
  without adding a second ranged-gun engine.
```

## Rare/reward handling

```text
Guaranteed spoils for entry 447: GLACIAL GUN + BLAZE GUN + BLASTER.
These are delivered by the Spoils of War reward channel; the player must never be required to Steal.
COMBAT ROLE: in v3 Barich equips Stoneshooter as visible steal-bait and as the fight's active gun.
Glacial Gun, Blaze Gun, and Blaster remain reward payloads, not active extra enemy gun engines, unless
the fight is redesigned and resimulated.
WHY IT FITS: Barich is the machinist Templar; the gun trio is his thematic payout.
TIER: mid-Chapter-4 gun reward. The later Lost Halidom Barich rematch is dragon/control-themed and
does not re-pay the gun identity.
```

## Proposed Composition (New Game++ Bed Desert v3)

Keep the count (6) and the open-desert gun-duel shape; make every active human a complete Chapter-4
unit. Boss `104`; Samurai `102`; Geomancers `102`/`101`; Black Mage `102`.

| Slot | Role | Job | Level | Br/Fa | Purpose |
| ------ | ------ | ----- | ------- | --- | --------- |
| n | Barich (BOSS) | Knights Templar (machinist) | `104` | `84/55` | Stoneshooter gun pressure; evasive/mobile boss; objective. |
| n | Parry Samurai | Samurai | `102` | `88/60` | Front-line parry screen; Martial Arts utility; Kiku-Ichimonji pressure. |
| n | Parry Samurai | Samurai | `102` | `88/60` | Second parry screen; blocks the approach without adding Rend pressure. |
| n | Terrain Geomancer | Geomancer | `102` | `84/60` | Terrain bruiser; Runeblade + Nature's Wrath punishes the approach. |
| n | Terrain Geomancer | Geomancer | `101` | `84/60` | Second terrain bruiser; covers the alternate lane with Item utility. |
| n | Black Mage | Black Mage | `102` | `60/84` | AoE caster; punishes clumping while crossing; no Time Magic engine. |

Current difference from vanilla:

```text
- Enemy count is unchanged, but the vanilla Knight and Archer slots are upgraded: Barich + 2 Samurai +
  2 Geomancers + 1 Black Mage.
- The objective is unchanged: defeat Barich.
- Barich's v3 setup replaces the active Glacial Gun plan with Stoneshooter, no secondary, Reflexes,
  Defense Boost, Jump +3, Thief's Cap, Black Garb, and Featherweave Cloak.
- The former Knights lose Rend entirely and become Samurai parry screens: Martial Arts secondary,
  Shirahadori, Doublehand, Movement +3, Kiku-Ichimonji, Crystal Helm, Crystal Mail, and Magic Gauntlet.
- The former Archers become Geomancers: Item secondary at JobLevel 8, Nature's Wrath, Attack Boost,
  Movement +2, Runeblade, Lambent Hat, Power Garb, and Magepower Glove.
- Glacial Gun, Blaze Gun, and Blaster remain guaranteed rewards only; they are not extra active enemy
  gun engines.
- The two Samurai and two Geomancers now have full v3 kits; the Black Mage keeps the vanilla caster
  pressure shape until its v3 individual kit is assigned.
```

Reasoning:

The faithful move is to **make the gun-boss the whole focus while the desert screen becomes fully built
Chapter 4 support**. Barich at `104` with Stoneshooter, Reflexes, Defense Boost, Jump +3, Thief's Cap,
Black Garb, and Featherweave Cloak delivers the "cross the sand and neutralize the gunner" duel at full
Ch4 strength, but now the boss is a harder-to-pin evasive target instead of a pure Glacial Gun elemental
check. The two former Knights become Samurai: they trade Rend pressure for Shirahadori/Doublehand
front-line threat, making careless physical rushes worse without turning the fight into a gear-break
tax. The former Archers become Geomancers, trading passive bow chip for terrain-driven hybrid pressure
and Nature's Wrath counter-chip. The Black Mage still punishes clumps without adding another puzzle
engine. Only Barich sits at the boss band (`104`); the screen is `101`-`102`.

Rejected variants:

```text
- v1 partial setup: correct gun-duel shape, but incomplete for Chapter 4 humans.
- Active gun trio: gives the screen Blaze/Blaster pressure and blurs the disarm target.
- Hard-control machinist: Disable/Immobilize belongs to the 057 rematch, not the first gun duel.
- Hydra preview: steals Lost Halidom's dragon-pit identity.
- Time Magic crossfire: adds a second tempo engine to a fight that should be about crossing the gun lane.
- Overlevelled screen: makes the guards the fight instead of Barich.
```

## Builds (Chapter-4 quality; desert machinist-Templar flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Barich (Lv 104) — BOSS (machinist Templar)

```text
Job: Knights Templar / Machinist (id TBD)   JobLevel: 8   Primary: machinist/gun skills at JobLevel 8.
No Disable/Immobilize control in this first Barich fight.
Secondary: none
Reaction: Reflexes (449)
Support: Defense Boost (466)
Movement: Jump +3
Head: Thief's Cap (168)
Body: Black Garb (198)
Accessory: Featherweave Cloak (234)
Right hand: Stoneshooter   Left: none / two-hand (254)
```

Role: the long-range threat and objective — close, bypass evasion, disarm (Steal Weapon), or burst him.
Keep the gun stealable as tactical disarm; rewards still pay through spoils.

### Samurai x2 (Lv 102) — desert parry screen

```text
Job: Samurai (id TBD)   JobLevel: 8
Secondary: Martial Arts, Monk JobLevel 8
Reaction: Shirahadori
Support: Doublehand
Movement: Movement +3
Head: Crystal Helm (154)
Body: Crystal Mail (182)
Accessory: Magic Gauntlet
Right hand: Kiku-Ichimonji   Left: none / two-hand (254)
```

Role: front-line parry screen slowing the player's approach across the sand; no Rend/break pressure.

### Geomancer x2 (Lv 102 / 101) — open-lane terrain bruisers

```text
Job: Geomancer (id TBD)   JobLevel: 8
Secondary: Item, Item JobLevel 8
Reaction: Nature's Wrath
Support: Attack Boost (465)
Movement: Movement +2 (487)
Head: Lambent Hat
Body: Power Garb (195)
Accessory: Magepower Glove
Right hand: Runeblade (30)   Left: none (255)
```

Role: terrain bruiser exploiting the open desert lanes; punishes a slow approach and melee contact.

### Black Mage (Lv 102) — AoE

```text
Job: Black Mage (id TBD)   JobLevel: 8
High-tier AoE (Fire/Bolt/Ice 3-tier). Black-Robe-equivalent body.
Secondary: Item, limited to Ether/Remedy/self-care; no Time Magic, no Stop/Don't Act.
Reaction: Reflexes (449)   Support: MA/Magick-boost (id TBD)   Movement: Movement +1 (486)
Head: mage hat (id TBD)   Body: Black Robe-equivalent (id TBD)
Accessory: Featherweave Cloak (234)   Right hand: magic-boost rod (id TBD)   Left: none (255)
```

Role: punishes the player for clumping while crossing the open ground toward Barich.

## Positioning Plan

```text
Open desert: Barich starts at MAX distance with clear Stoneshooter sightlines (the long-range duel),
  the two Samurai forward as the screen, the two Geomancers on flanking dunes/lanes, the Black Mage
  mid-back.
Preserve the open geometry and long sightlines (the distance puzzle IS the fight) — do not box Barich
  in a corner where he can be reached trivially turn one.
Keep the gun stealable; the player should have multiple valid answers (close, non-evadable pressure,
  disarm), none mandatory.
Only the boss at `104`; do not over-scale the screen.
```

The desert should say: "a Templar gunner rules the open sand — sprint the dunes, ignore his evasive
shell, or snatch his gun, then put him down before the desert wears you thin."

## Simulation Plan and Results

Simulation artifact:

```text
tmp/fft-level-design-042-bed-desert/
  assumptions.md
  simulate.py
  iteration-results.json
  iteration-results.md
```

Model scope:

```text
Coarse deterministic opening-pressure model over the first five rounds.
It scores local pressure, gun clarity, approach answerability, disarm clarity, break fairness, repeat-
foe differentiation, and hard-control risk. It does not simulate exact FFT formulas.
```

Result summary:

> Current note: these results are the v2 baseline simulation. The v3 Stoneshooter/Reflexes/
> Featherweave Barich package is the active design direction and still needs a refreshed simulation
> pass before implementation.

| Candidate | Pressure | Gun clarity | Approach answer | Disarm clarity | Break fairness | Repeat diff | Hard control | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| v1 partial firing line | 168 | 94 | 84 | 90 | 74 | 95 | 0 | Rejected: incomplete setup |
| v2 complete firing lane | 176 | 94 | 84 | 90 | 74 | 95 | 0 | **Accepted** |
| active gun trio | 232 | 62 | 48 | 46 | 74 | 77 | 0 | Rejected: unclear / reward risk |
| hard control machinist | 231 | 94 | 59 | 90 | 74 | 70 | 50 | Rejected: hard control |
| hydra preview | 256 | 64 | 49 | 65 | 74 | 45 | 0 | Rejected: wrong identity |
| time magic crossfire | 194 | 76 | 84 | 78 | 74 | 95 | 0 | Rejected: second engine |
| overlevelled screen | 194 | 94 | 75 | 90 | 66 | 95 | 0 | Rejected: unclear / screen too strong |

Iteration decision:

```text
ACCEPT v2 complete firing lane as the baseline structure.
For v3, keep the vanilla count and complete every human setup, but replace Barich's active Glacial
Gun engine with the Stoneshooter/Reflexes/Defense Boost/Jump +3 evasive boss package, and replace the
two vanilla Knights with Samurai parry screens and the two vanilla Archers with Geomancer terrain
bruisers. Do not activate Glacial Gun/Blaze Gun/Blaster as extra enemy guns; do not bring forward
057's dragons or Disable/Immobilize control. The answer remains: close distance, non-evadable
pressure, Steal Weapon, or burst Barich.
```

## Implementation Checklist

- [ ] Confirm current entry 447 slot order: Barich + 2 Knight + 2 Archer + 1 Black Mage + player slots (NO Hydra).
- [ ] Keep win condition = "Defeat Barich" (ends on his fall); keep the open desert geometry.
- [ ] Set Barich `104` with complete v3 kit: primary JobLevel 8, no secondary, Reflexes, Defense Boost,
      Jump +3, Stoneshooter, Thief's Cap, Black Garb, and Featherweave Cloak.
- [ ] Confirm STEAL WEAPON works against Stoneshooter; rewards must still be guaranteed spoils.
- [ ] Do not activate Glacial Gun/Blaze Gun/Blaster as extra enemy gun engines unless redesigned and
      resimulated.
- [ ] Replace both vanilla Knights with Samurai `102`: Martial Arts secondary at Monk JobLevel 8,
      Shirahadori, Doublehand, Movement +3, Kiku-Ichimonji, Crystal Helm, Crystal Mail, and
      Magic Gauntlet.
- [ ] Replace both vanilla Archers with Geomancers: Item secondary at Item JobLevel 8, Nature's Wrath,
      Attack Boost, Movement +2, Runeblade, Lambent Hat, Power Garb, and Magepower Glove.
- [ ] Remove Knight Rend/break pressure from these two slots; keep Black Mage AoE + Geomancer lane
      pressure.
- [ ] Give every active human complete equipment plus secondary/reaction/support/movement.
- [ ] Keep remaining secondaries constrained to role utility; no Phoenix Down loops, Time Magic, or hard control.
- [ ] Set add levels: 2 Samurai + 1 Geomancer + Black Mage `102`; second Geomancer `101`.
- [ ] Set JobLevel `8` on all active enemy slots.
- [ ] Preserve guaranteed spoils: Glacial Gun + Blaze Gun + Blaster; preserve buried Yagyu Darkrood.
- [ ] Patch via the correct layer; keep the diff inside the Bed Desert window only.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify gun + steal + win-cond.
- [ ] Install mod, test from a New Game+ save; confirm it plays as an open-desert gun-duel.

## Test Questions

- Is Barich's Stoneshooter a real long-range threat with multiple FAIR answers (close distance,
  non-evadable pressure, Steal Weapon disarm) — never a hard lock?
- Does stealing the Stoneshooter remove his gun threat while rewards still pay through guaranteed spoils?
- Does "Defeat Barich ends the fight" keep it a reach-and-burst race, not a cross-desert trade war?
- Is the open desert geometry preserved (long sightlines — the distance puzzle)?
- Do the Samurai parry screens pressure physical rushes without turning Shirahadori into a fake wall?
- Do the Geomancers preserve lane pressure without becoming a second headline engine?
- Is the AoE Black Mage race-able while the Samurai and Geomancers occupy the approach lanes?
- Do all active humans have complete equipment plus secondary/reaction/support/movement?
- Are Glacial Gun, Blaze Gun, and Blaster rewards only, not extra active enemy gun engines?
- Is only Barich at the boss band (`104`), screen `101`-`102` — a Tier-A boss, not a spike?
- Does the loot stay consistent with his later Lost Halidom (`052`) appearance (no double-best)?

## Sources

- Game8, "Beddha Sandwaste Walkthrough (Battle 37)": roster (Barich boss + 2 Knight + 2 Archer +
  1 Black Mage; NO Hydra), objective "Defeat Barich!", recommended level ~43, 3/5 stars, deploy 5,
  desert terrain, Glacial-Gun ice + Ice-Shield-absorb tip, rewards (30,600 Gil, buried Yagyu Darkrood).
  https://game8.co/games/Final-Fantasy-Tactics/archives/553197
- Final Fantasy Wiki, "Balk Fendsor" / "Bed Desert": story/terrain context.
  https://finalfantasy.fandom.com/wiki/Balk_Fendsor
- Local: `037-chapter-4-overview.md` (job-escalation + Chapter 4 reward rules),
  `029-monastery-vaults-1st.md`/`034` (disarm-the-boss-weapon precedent), `038-dugeura-pass.md`
  (Black Mage AoE build), and `057-lost-halidom.md` (Barich's later Tier-S endgame appearance — to be
  designed; keep loot consistent), `chapter-4-rewards-implementation.md` (gun trio guaranteed spoils).
