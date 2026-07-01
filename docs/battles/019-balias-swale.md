# 019 - Balias Swale (Bariaus Valley)

Status: v2 implemented (entry 413, 2026-07-01) — Agrias runtime guest handling retained; Geomancer storm-cell slot-add applied.
Chapter: 2 — "The Manipulator and the Subservient"
Battle order: Battle 18 (after Goug Lowtown)
Target version: Enhanced v1.5.0

## V2 Implementation Update (2026-07-01)

Implemented with `python tools/battle_patch.py balias_swale`.

- Agrias remains handled by the runtime guest scaler/control path (`cid 0x1e`), with ENTD Brave/Faith support only.
- Enemy roster is 2 Knights, 2 Archers, 2 Black Mages, and a new Geomancer.
- The Geomancer is a plain static ENTD slot-add in `s7` with UnitID `0x86`, First Strike, Attack Boost, Move +1, Runeblade, and Chapter-2 shop-tier armor.
ENTD: global entry **413** (battle_entd4, local entry 29) — confirmed by composition + Agrias guest
File: `entd/battle_entd4_ent.bin` (embedded; swapped only in NG+ by the code mod)

> Implemented via `tools/battle_patch.py balias_swale`, plus a Program.cs change adding Agrias (cid
> 0x1e) to the runtime guest-scaler. NG+-only enemy edits. See `011-chapter-2-overview.md`.

## Original Battle

Objective:

```text
Save Agrias!  (she must survive — losing her fails the battle and the recruit)
```

Player deployment:

```text
Up to 5 units, including Ramza — across a SPLIT-team deployment.
Ally: Agrias is the protected guest. She can hold her own but starts OUTNUMBERED and isolated;
  she becomes a permanent party member after this battle.
```

Original enemy composition:

```text
1x Knight
2x Archer
2x Black Mage   (Thunder — amplified by the rain)
```

Public walkthrough details:

```text
Recommended level: ~20 (2/5 stars on paper).
Rainy valley/swale; RAIN BOOSTS THUNDER damage (both sides).
The Black Mages are the primary threat — rain-boosted Thunder hurts.
Enemies start on the FAR END; the player needs ranged units or Movement 4+ to reach them and
  to relieve the isolated, outnumbered Agrias quickly.
Split your forces: mix mages and physical attackers across the two teams.
```

Design reading:

Balias Swale is a **split-team race to relieve an outnumbered VIP in the rain**. It braids three
earlier ideas — Sand Rat's split deployment, Zeirchele's protect-the-guest, and the rain-Thunder
gimmick — into one: Agrias is stranded and outgunned on the far side, and the player must split
their force and **close distance fast** before the rain-boosted Black Mages and Archers wear her
down. It teaches split-team coordination, mobility (Move 4+), and respecting weather (Thunder
cuts both ways).

For New Game++ the identity must stay: **a rainy split-team rush to save an isolated, outnumbered
Agrias from a ranged firing line whose Thunder the weather amplifies — distance and tempo are the
whole fight.**

## Local Data Confirmed (entry 413)

```text
slot  cid    flags  job        role                       action
s0    0x1e   0x50   30 (==cid) Agrias (Save-Agrias VIP)   SCALE L100 + equip survival/offense kit
s1    0x80   0x80   76 Knight  frontline body             SCALE -> L101
s2    0x81   0x40   77 Archer  far-end ranged             SCALE -> L101
s3    0x81   0x40   77 Archer  far-end ranged             SCALE -> L100
s4    0x80   0x80   76 Knight  frontline body             SCALE -> L100
s5    0x80   0x80   80 BMage   rain-Thunder (primary)     SCALE -> L101
s6    0x80   0x80   80 BMage   rain-Thunder (primary)     SCALE -> L101
```

Job IDs: Knight 76, Archer 77, Black Mage 80, Agrias's Holy-Knight job 30. (TIC has 2 Knights vs the
walkthrough's 1.) The Knights run job 76 at jl8, so they carry Battle Skill (Rend) innately — a minor
extra over this doc's "no break" preference, not suppressible without changing the job; non-blocking.

### Agrias (VIP): scaled + equipped; v2 requires player control

Agrias (**cid 0x1e, job 30 == cid**) is the "Save Agrias!" objective unit: isolated, outnumbered,
and her death FAILS the battle. She is in `GuestCharIds`, so the runtime guest-scaler already keeps
her at party level; here her ENTD level byte is ALSO set to 100 (party level) so the scaling is
explicit in the modded data (the scaler then no-ops on it).

**Player report:** at NG+ party level she "dies way too easy"; enemies not killed before their turn
focus Agrias and kill her. **Root cause:** scaled level but Ch2-tier gear (Golden Helm/Armor, Mythril
Shield, Coral Sword) on an outnumbered VIP. **Fix:** equip an endgame, job-legal Holy-Knight kit
(job 30 equips Helmet/Armor/Shield/KnightSword plus Armguard/Cloak/etc.). Only the level and the 5
gear bytes changed; job, cid, flags, and scripting are untouched. NG+-only (modded ENTD swap).

- Weapon: **Save the Queen (34)**, Power 18, +30 evasion, her signature blade (user-requested)
- Head: **Crystal Helm (154)**, +120 HP. Body: **Crystal Mail (182)**, +110 HP (no magic-reflect, so she stays healable)
- Shield: **Crystal Shield (139)**, 40% phys / 15% magic evasion
- Accessory: **Bracers (218, Armguard)**, +3 PA (user-requested; she hits harder and clears her own attackers)

Net at party level: stacked physical evasion (25% class + 40% shield + 30% weapon) so she dodges most
of the melee focus, plus ~230 bonus HP (HPMult 140 job) and Save the Queen offense boosted by Bracers.
She trades a cloak's magic evasion for PA, so her magic dodge is the shield's 15% only, offset by her
high HP vs the rain-Thunder. Reserved player rewards (Maximillian/Grand Helm/Genji/Escutcheon) were
avoided; Save the Queen is the user-chosen exception (it is also the Bervenia spoil 443, with no economy
conflict since this 413 slot is the battle-only guest instance).

The RAIN flag and split-team zones are map/terrain data (not in the ENTD slots), so they are untouched.

For v2, scaling/equipment is still not enough: Agrias is an active guest and must be
player-controlled in NG+. The challenge should come from coordinating the split deployment and
relieving her under a rain-boosted firing line, not from watching guest AI choose bad actions.

## Enemy Party Escalation (Chapter 2 redesign)

```text
VANILLA SPIRIT: split-team rescue in a rainy valley, where distance and weather make the ranged
  firing line dangerous.
CHAPTER-2 UPGRADE: keep the local-data roster of 2 Knights, 2 Archers, and 2 rain-Thunder Black
  Mages, then add 1 Geomancer as the terrain-pressure debut. Optimize the full party with complete
  equipment and intentional reaction/support/movement.
WHY: the Geomancer fits the swale and makes the crossing itself dangerous. The accepted v2 version
  must bias pressure onto the route and the split teams, not simply focus Agrias before the player
  can meaningfully control the board.
WHAT IS NOT CHANGED: the strategy is still "split, rush, relieve Agrias, and manage rain-Thunder."
  This is not a Time Mage or hard-control fight.
```

Chapter 2 requirements applied:

```text
- Every active human enemy has full equipment.
- Every active human enemy has intentional reaction, support, and movement.
- Secondary is optional; the jobs' primary commands already express their roles.
- Agrias must be scaled, geared, and player-controlled in NG+.
- No Time Mage, no third Black Mage, and no hard-lock control package.
```

## Boss rare loot

```text
None. No named boss here — no rare item (per the Chapter 2 overview). Generics stay shop-tier.
```

## Map reward note

```text
No enemy carries rare loot here. The Chapter 2 reward ledger may still treat Balias Swale as a
signature map-treasure battle because Agrias joins after it; that reward is not part of the enemy
loadout and should not make a normal enemy a rare-gear carrier in Chapter 2.
```

## Guest handling

```text
Agrias is the protected guest and recruit. In NG+ she must be player-controlled from the start.
Her strong guest kit keeps the objective from failing instantly, but enemy pressure must be placed
so the player still has to coordinate the split deployment instead of relying on Agrias AI.
```


Fixed encounter Brave/Faith targets:

| Unit | Br/Fa | Rationale |
|------|-------|-----------|
| Agrias | `76/65` | Protected Holy Knight ally; physical pressure with moderate Faith so healing/support remain meaningful. |

## Proposed Composition (New Game++ Balias Swale v2)

Use seven enemies: 2 Knights, 2 Archers, 2 Black Mages, and 1 Geomancer. This is one extra active
enemy over the shipped v1 data and keeps the fight below the boss-heavy back third.

| Slot | Role | Job | Level | Br/Fa | Purpose |
| ------ | ------ | ----- | ------- | --- | --------- |
| n | Route Anchor | Knight | `101` | `76/48` | Holds the main crossing lane; Battle Skill is incidental, not the headline. |
| n | Backstop Knight | Knight | `100` | `76/48` | Protects the firing line and slows a straight rush. |
| n | Lead Archer | Archer | `101` | `74/50` | Lane cover; pressures split units that overextend. |
| n | Flank Archer | Archer | `100` | `74/50` | Covers the second approach and keeps both player teams relevant. |
| n | Fast Storm Mage | Black Mage | `102` | `55/76` | Faster rain-Thunder cast; priority target. |
| n | Power Storm Mage | Black Mage | `101` | `55/76` | Harder rain-Thunder cast; punishes clumping. |
| n | Swale Geomancer | Geomancer | `101` | `62/68` | Delayed terrain pressure on the crossing; Geomancer debut. |

Reasoning:

The faithful move is to **scale the firing line, keep rain-Thunder as the headline, and make the
crossing more dangerous through terrain pressure**. The two Black Mages remain the priority kills,
but the accepted v2 plan does not let every ranged unit freely focus Agrias on turn 1. The Geomancer
and at least one caster line should pressure the player's route, forcing split-team coordination.
Agrias being controlled by the player turns the objective into an active rescue problem instead of
a guest-AI survival roll.

## Builds (final-shop quality; valley garrison flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Knight x2 (Lv 101 / 100)

```text
Job: Knight (76)   JobLevel: 8   Secondary: none
Primary: Battle Skill exists because this is the Knight job, but do not add break-enhancing setup.
Reaction: Counter (442)   Support: Defense Boost / Attack Boost (id TBD / 465)
Movement: Movement +1 (486)
Head/Body: shop heavy helm + heavy armor (ids TBD)
Accessory: Bracers (218)   Right hand: Runeblade (30)   Left hand: shop shield (id TBD)
```

Role: route anchors. They slow the crossing and protect the firing line, but Balias Swale should
not become a Rend puzzle; no Dual Wield, no Concentration break, and no rare gear.

### Archer x2 (Lv 101 / 100)

```text
Job: Archer (77)   JobLevel: 8   Secondary: none
Reaction: Reflexes (449)   Support: Concentration (469)   Movement: Movement +1 (486)
Head: Thief's Cap (168)   Body: Black Garb (198)   Accessory: Bracers (218)
Right hand: Windslash Bow (87) or a verified shop-tier lightning bow if the weather interaction works
Left hand: none / two-hand marker (254)
```

Role: lane cover. They punish overextended split units and soften Agrias only if the player ignores
the far side; they should not be positioned as an unavoidable turn-1 Agrias execution squad.

### Black Mage x2 (Lv 102 / 101) — rain-Thunder

```text
Fast Storm Mage:
Job: Black Mage (80)   JobLevel: 8   Secondary: none
Primary: Thunder/Thundara priority; avoid unrelated status/control.
Reaction: Reflexes (449)   Support: Swiftness/Short Charge (id TBD)   Movement: Movement +1 (486)
Head: cloth/mage hat (id TBD)   Body: shop robe (id TBD)
Accessory: Featherweave Cloak (234)   Right hand: shop magic-boost rod (id TBD)   Left: none (255)

Power Storm Mage:
Job: Black Mage (80)   JobLevel: 8   Secondary: none
Primary: Thunder/Thundara priority; rain is the damage amplifier.
Reaction: Reflexes (449)   Support: Arcane Strength / MA boost (id TBD)
Movement: Movement +1 (486)
Head: cloth/mage hat (id TBD)   Body: shop robe (id TBD)
Accessory: Featherweave Cloak (234)   Right hand: shop magic-boost rod (id TBD)   Left: none (255)
```

Role: the primary danger. One caster makes the clock real; the other punishes clumping. They should
create urgent target priority without turning the first two rounds into unavoidable Agrias focus.

### Geomancer (Lv 101) — NEW terrain pressure

```text
Job: Geomancer (id TBD)   JobLevel: 8   Secondary: none (innate Geomancy)
Reaction: Counter (442) or First Strike (453)
Support: Attack Boost (465)   Movement: Movement +1 (486)
Head: shop hat (id TBD)   Body: shop light armor / robe-tier the job allows (id TBD)
Accessory: Bracers (218)   Right hand: a shop sword/rod the job allows (id TBD)   Left: none/shield
```

Role: delayed mid-range terrain pressure on the crossing. The Geomancer exists to make the route
dangerous, not to add another direct VIP-focus gun.

## Positioning Plan

```text
The firing line (2 Archers + 2 Black Mages) starts on the FAR END, but not every unit has a clean
  turn-1 line on Agrias.
One Black Mage may threaten Agrias early; the other should have a stronger line on the crossing or
  the player split, so the storm pressure is shared.
The Geomancer starts at mid-range on a wet/valley route tile, aimed at the crossing rather than the
  protected guest.
The two Knights start forward and staggered: one contests the main route, one protects the firing
  line. Leave at least two readable routes open.
Agrias starts isolated/outnumbered and must be player-controlled in NG+.
Preserve the split-team zones, Agrias's protected slot, and the RAIN flag.
```

The valley should say: "your VIP is stranded under a rain-charged firing line — split up, close
fast, and use the weather before it's used on you."

## Simulation Plan and Results

Simulation artifact:

```text
tmp/fft-level-design-019-balias-swale/
```

Model scope:

```text
First four rounds only; compares route pressure, enemy action economy, and rain-Thunder pressure
before the split teams can stabilize. It assumes Agrias is player-controlled in v2 and rejects
variants where survival depends on guest AI luck, dense terrain/status pressure, or a Time Mage
identity shift.
```

Iteration results:

| Candidate | Enemies | Enemy actions | Action ratio | Rain Thunder | Terrain | Pressure | Delta vs v1 | Result |
|-----------|---------|---------------|--------------|--------------|---------|----------|-------------|--------|
| v1 current: 2 Knight, 2 Archer, 2 Black Mage | 6 | 20.0 | 1.14 | 6.4 | 0.0 | 150.3 | +0.0% | Baseline |
| Guest remains AI-framed | 7 | 23.4 | 1.73 | 6.4 | 3.4 | 190.8 | +26.9% | Rejected: guest rule |
| Two Geomancers | 8 | 26.8 | 1.57 | 6.4 | 6.8 | 214.4 | +42.6% | Rejected: too dense |
| Add Time Mage storm tempo | 8 | 26.8 | 1.57 | 6.4 | 3.4 | 208.8 | +38.9% | Rejected: wrong identity |
| v2 storm crossing: 2 Knight, 2 Archer, 2 Black Mage, 1 Geomancer | 7 | 23.2 | 1.28 | 6.4 | 3.2 | 175.6 | +16.8% | Accepted |

Decision:

```text
Use the seven-enemy storm-crossing cell: 2 Knights, 2 Archers, 2 rain-Thunder Black Mages, and 1
delayed route-pressure Geomancer. Agrias control reduces the split tax because the player can
stabilize her side actively; the added difficulty comes from route pressure and caster priority,
not guest AI.
```

## Current Implementation (v1, entry 413 — superseded by v2 design)

Applied with `python tools/battle_patch.py balias_swale`; diff contained to local entry 29 (global
413), 62 bytes. Knights L101/L100, Archers L101/L100, Black Mages L101; JobLevel 8 on all.

```text
s1  Knight   L101 jl8  R Counter  S Atk-Boost  M +1  heavy shop kit + Runeblade + Shield
s4  Knight   L100 jl8  (same kit)
s2  Archer   L101 jl8  R Reflexes  S Concentration  M +1  Thief's Cap / Black Garb / Bracers + Windslash Bow
s3  Archer   L100 jl8  (same kit)
s5  BMage    L101 jl8  R Reflexes  M +1  Mage Hat / shop Robe / Featherweave + shop Rod  (rain-Thunder)
s6  BMage    L101 jl8  (same kit)
```

**Deferred — Geomancer escalation (slot-add).** The doc's wrinkle adds a Geomancer (first use of the
job), which needs a verified map position; batched for the playtest pass.

This implementation remains the shipped v1 data. The v2 redesign above is **documentation only** in
this pass; it requires a later implementation pass to add the Geomancer, tune caster/route
placement, complete final ability/equipment mapping, and confirm Agrias player control.

## Original V2 Implementation Checklist (historical)

- [x] Identify Balias Swale ENTD entry (413); fill "Local Data Confirmed".
- [x] Dump original entry; verify Knights + Archers + Black Mages + Agrias.
- [x] Confirm Knight / Black Mage / Archer job IDs and legal equipment.
- [ ] Add the Geomancer slot at a verified route-pressure position.
- [ ] Set v2 levels: Fast Storm Mage `102`; Route Anchor + Lead Archer + Power Storm Mage +
  Geomancer `101`; Backstop Knight + Flank Archer `100`.
- [ ] Set JobLevel `8` on all active enemies.
- [ ] Give every active human enemy complete equipment plus intentional reaction/support/movement.
- [ ] Tune Black Mage spell access toward Thunder/Thundara; avoid unrelated control.
- [ ] Confirm Agrias is player-controlled in NG+ in addition to being scaled/equipped.
- [ ] Preserve Agrias's protected slot, split deployment zones, and RAIN flag.
- [x] Patch the embedded ENTD via `tools/battle_patch.py balias_swale`.
- [ ] Re-dump and diff; changes small and intentional.
- [ ] Playtest from a NG+ save; confirm Save-Agrias + split work; verify Agrias survives because
  the player can act, not because enemy focus is toothless.
- [ ] Confirm whether her equipped gear carries over when she joins (Save the Queen overlaps the Bervenia 443 spoil).

## Test Questions

- With Agrias player-controlled, is relieving her tense because of route pressure rather than guest AI?
- Are the rain-boosted Black Mages the clear primary threat (and can the player exploit Thunder too)?
- Does the added Geomancer make the crossing deadlier without becoming another direct VIP-focus unit?
- Does the split-team deployment still force genuine two-front coordination?
- Does route-biased placement leave at least two readable approaches instead of a single kill lane?
- Are Time Mage tempo, hard-lock control, and third-Black-Mage burst still absent?
- Does it read as a distinct fight (rainy VIP-rescue) vs the other split/escort battles?
- Is it a fair step (later in the chapter) but below the Gaffgarion/Cúchulainn bosses?

## Sources

- Game8, "Balias Swale Walkthrough (Battle 18)": objective "Save Agrias!", roster (1 Knight,
  2 Archer, 2 Black Mage), recommended level ~20, rain boosts Thunder, enemies on the far end,
  split-team deploy 5, Agrias outnumbered guest who becomes permanent after.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553178
- Final Fantasy Wiki, "Bariaus Valley" / "Agrias Oaks": story/terrain context.
  https://finalfantasy.fandom.com/wiki/Bariaus_Valley
- Local: `docs/battles/011-chapter-2-overview.md` (enemy-party escalation rule), `005-sand-rat-sietch.md`
  (split-team handling), `006-brigands-den.md` (rain-Thunder gimmick), `014-zeirchele-falls.md`
  (protect-the-guest).
</content>
