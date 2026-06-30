# 028 - Monastery Vaults, 3rd Level — Izlude (Orbonne Monastery)

Status: ✅ implemented (v1, entry 423) — NG+ only; pending playtest. **v2 redesign documented only** (implementation pending).
Chapter: 3 — "The Valiant"
Battle order: Battle 25 (after Vaults 2nd Level) — **Vaults chain 2 of 3**
Target version: Enhanced v1.5.0
ENTD: global entry **423** (local entry 39, `battle_entd4_ent.bin`)
File: `battle_entd4_ent.bin` (embedded NG+ swap) — `tools/battle_patch.py vaults_3rd`

Implemented composition (entry 423, vanilla-dump verified):
- s0 Izlude (job 38 Knights-Templar special, sec 52 Mighty Sword) — L103/jl8; rare **Mirror Mail
  (184 = TIC's "Reflect Mail", auto-Reflect)** as body; Bracers + Runeblade; job/sec/kit/shield/head
  preserved (decapitation-target identity + the "defeat Izlude ends fight" scripting untouched).
- s1,s2 Knight L101 — Heavy Helm/Heavy Armor/Bracers/Runeblade/shop Shield; Rend innate; Counter/Atk Boost/Mv+1.
- s3 Summoner L101 — Mage Hat/shop Robe/Featherweave/shop Rod (Rod is job-82-legal); Reflexes/Atk Boost/Mv+1.
- s4,s5 Archer L101/L100 — Thief's Cap/Black Garb/Bracers/Windslash Bow (two-hand); Reflexes/Concentration/Mv+1.

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `024-chapter-3-overview.md`.

## Original Battle

Objective:

```text
Defeat Isilud!  (the fight ENDS the moment Izlude falls — he is the only target that matters, and
  his defeat throws you straight into the Vaults 1st Level / Wiegraf with NO resupply.)
```

Player deployment:

```text
Up to 5 units, including Ramza. No guests.
CHAIN: mid-link of the three Vault battles (2nd -> 3rd -> 1st), NO resupply or gear change between.
```

Original enemy composition:

```text
1x Izlude (Isilud)  (Knights Templar BOSS — dual-wield; "Mighty Sword" ranged equipment/stat breaks)
2x Knight
2x Archer
1x Summoner         (AoE pressure from the back)
ALL on a vault of TALL shelves / walls — high ground everywhere; Jump 4+ to navigate.
```

Public walkthrough details:

```text
Recommended level: ~28.  Difficulty: 3/5 stars.
Izlude perches on the SHELVES (high ground) and DUAL-WIELDS; reaching him needs Jump 4+ / climbing.
Defeating Izlude ENDS the battle immediately (he is the objective), so a decisive strike on him
  short-circuits the fight — but he is elevated and screened.
A Summoner threatens AoE from the back; 2 Knights + 2 Archers screen the approach.
No resupply afterward — you go straight into Wiegraf.
```

Design reading:

The 3rd Level is **the Knights Templar debut and a reach-the-elevated-boss puzzle**. Izlude is the
chapter's first Templar: he dual-wields and wields **Mighty Sword** — ranged strikes that break the
player's weapon/armor/shield/accessory or sap stats (an elevated cousin of the Knight's Rend). He
fights from the **shelf high ground**, so the player must climb/Jump to him through a Knight/Archer
screen while a Summoner shells the approach. Because **defeating Izlude ends the fight**, the puzzle
is a *decapitation race* — punch a lane to the elevated boss and drop him before the breaks and the
summon grind you down — all on the chain's single loadout. It teaches verticality (Jump/climb),
priority (the objective is one unit), and break-defense (Safeguard/Maintenance).

For New Game++ the identity must stay: **a vertical decapitation race to a dual-wielding Templar on
the shelves who breaks your gear from range, screened by knights/archers and a summoner — reach him
and end it before attrition and breaks win, on one loadout.**

## Local Data Confirmed

```text
ENTD entry 423 confirmed in `024-chapter-3-overview.md` and v1 implementation.
Roster: Izlude + 2 Knight + 2 Archer + 1 Summoner, plus the player slots.
DO NOT touch the "defeat Izlude ends the battle" objective scripting or the chain link into the 1st
  Level (Wiegraf).
Keep the tall-shelf high-ground geometry (the Jump-4+/climb-to-the-boss puzzle depends on it).
Keep Summoner charge times intact (race-the-cast counter).
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
```

Job / item IDs (carry over known, verify any remaining table ids before implementation):

```text
38 = Knights Templar special (Izlude; confirmed in v1 implementation)
52 = Mighty Sword secondary (confirmed on Izlude in v1 implementation)
76 = Knight (confirmed generic Knight id in local docs)
77 = Archer (confirmed)
82 = Summoner (confirmed from Balias Tor 016 and v1 implementation)
184 = Mirror Mail / TIC "Reflect Mail" (auto-Reflect armor; confirmed in v1 implementation)
```

## Enemy Party Escalation (Chapter 3 redesign)

```text
VANILLA SPIRIT: a vertical decapitation race against Izlude, the first Templar, who breaks gear from
  shelf high ground while Knights, Archers, and a Summoner screen the climb.
CHAPTER-3 UPGRADE: keep the exact six-enemy roster, but complete every active human setup with
  secondary/reaction/support/movement. The party becomes a coordinated Templar cell: Izlude breaks
  from range, one Knight adds limited Rend pressure, Archers punish the climb, and the Summoner
  shells clumped approaches.
WHY: the Templar debut is already the new caste. Adding another job, another archer, or a Time Mage
  would overtax the no-resupply chain before Wiegraf and blur the "reach the elevated boss" lesson.
WHAT IS NOT CHANGED: defeating Izlude still ends the battle; shelf geometry still matters; the
  Summoner remains raceable/interruption-friendly; break pressure stays capped at Izlude + one Knight.
```

Chapter 3 requirements applied:

```text
- Every active human enemy has full equipment.
- Every active human enemy has secondary, reaction, support, and movement.
- The party has real synergy: elevated Templar break + one Rend bodyguard + ranged climb punishment
  + mid-tier AoE.
- No guests are present.
- No extra body, no Time Mage tempo, no hard-lock status, no second Rend Knight.
```

## Sanctioned exceptions (carried + extended precedent)

```text
TEMPLAR "MIGHTY SWORD" breaks — allowed, constrained (extends the Knight-Rend exception, 016/021):
  ALLOWED: ranged equipment/stat breaks on Izlude (his signature threat).
  GUARDRAILS: it is telegraphed and counterable — Safeguard / Maintenance defend gear; the player
    can also race him (his defeat ends the fight). He does NOT break every slot every turn, and the
    generics use only shop-tier breakable gear. NO hard lock (no Stop/Don't Act). Treated like
    Gaffgarion's Drain: strong, but with a clear answer.
SUMMONER — allowed (Balias Tor 016): MID-TIER summons, charge times intact; it shells the approach,
  not the boss, so it doesn't double up on Izlude's threat.
```

## Boss rare loot

```text
Izlude -> REFLECT MAIL (armor; non-buyable; auto-Reflect). Ch3 MID-HIGH tier.
WHY IT FITS: an elite Templar in reflective mail — magic BOUNCES off him, so the player must kill
  him with PHYSICAL damage (the Summoner becomes the player's risky magic option, not a tool against
  Izlude). It is a real in-fight wrinkle AND a tempting steal/drop, clearly above Chapter 2's rare
  baseline (Blood Sword / 108 Gems) yet well below the Ch4-reserved best (Genji armor, best robes). First
  Chapter 3 rare drop.
STORY NUANCE: Izlude is decisively DEFEATED here (the fight ends on his fall), so the reward is paid
  out HERE. His later Riovanes Roof appearance (035) is a scripted cutscene death — NOT a second
  player-lootable kill — so there is no double-dip; do not also assign him a rare at 035.
DIFFERENTIATION: the marquee Templar KNIGHT SWORD rare (Defender) is reserved for Wiegraf (029), so
  Izlude's highlight is defensive (Reflect Mail), not a sword.
```

## Proposed Composition (New Game++ Vaults 3rd v2)

Keep the exact roster; Izlude is the elevated sub-boss spike. Izlude `103`; Knights `101`;
Summoner `101`; Archers `100`–`101`. The v2 increase is **completeness and coordination**, not
body count.

| Slot | Role | Job | Level | Br/Fa | Purpose |
| ------ | ------ | ----- | ------- | --- | --------- |
| n | Izlude (SUB-BOSS, NEW caste) | Knights Templar | `103` | `86/55` | Dual-wield + Mighty-Sword breaks from the shelves; defeating him ENDS the fight. Reflect Mail. |
| n | Knight (Rend) | Knight | `101` | `86/55` | Screens the climb to Izlude; the only generic break source. |
| n | Knight (bodyguard) | Knight | `101` | `84/45` | Second body; contests the vertical lane without Rend. |
| n | Archer (shelf cover) | Archer | `101` | `80/45` | Ranged punishment on the climbers. |
| n | Archer (lane cover) | Archer | `100` | `80/45` | Covers the other shelf lane without creating a hard ranged lock. |
| n | Summoner | Summoner | `101` | `58/78` | Mid-tier AoE shelling the approach; raises the cost of clumping but stays raceable. |

Reasoning:

The faithful move is to **make Izlude an elevated decapitation target and keep the break + summon
pressure**, then tune the escort so it sharpens the climb instead of draining the chain dry. At
`103` on the shelves with dual-wield and Mighty-Sword breaks, he punishes a slow approach and strips
gear from range, while Reflect Mail forces the player to finish him physically. One Knight carries
Rend so Safeguard/Maintenance matter; the second Knight only bodies the lane; the Archers and
Summoner punish clumping and slow climbing without adding an unavoidable crossfire wall. The
intended solution holds: build for verticality (Jump/climb), defend gear, and race a lane to Izlude
to end the fight before attrition wins — while still having enough resources for Wiegraf.

## Builds (final-shop quality; Knights Templar flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Izlude — Knights Templar SUB-BOSS (Lv 103) — rare: Reflect Mail

```text
Job: Knights Templar special (38)   JobLevel: 8   Primary: Templar/basic command
Secondary: Mighty Sword (52 — ranged equip/stat break)
Reaction: Counter (442) or a parry reaction (id TBD)   Movement: Jump +? / Ignore Height (id TBD)
Support: Dual Wield (id TBD — innate/equipped; two blades)
Head: shop helm (id TBD)   Body: REFLECT MAIL (id TBD — his rare; auto-Reflect)
Accessory: Bracers (218)   Right/Left hand: two shop-tier-best swords (ids TBD; not a reserved best)
Defeating him ENDS the battle. Reflect Mail = his drop/steal.
```

Role: the elevated Templar — breaks gear from range, reflects magic, ends the fight when he falls.

### Knight x2 (Lv 101) — 1x Rend

```text
Job: Knight (76)   JobLevel: 8
Secondary: Knight A = Rend (break) / Knight B = Item or Fundaments equivalent (NO Rend)
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head/Body: shop heavy helm + heavy armor (ids TBD)
Accessory: Bracers (218)   Right hand: Runeblade (30) / Icebrand (29)   Left: shop shield (id TBD)
```

Role: screens the vertical approach to Izlude; only one carries Rend so the break-source cap holds.

### Archer x2 (Lv 101 / 100)

```text
Job: Archer (77)   JobLevel: 8   Primary: Aim/Charge
Secondary: Item or Fundaments equivalent; no hard status
Reaction: Reflexes (449)   Support: Concentration (469)   Movement: Movement +1 (486)
Head: Thief's Cap (168)   Body: Black Garb (198)   Accessory: Bracers (218)
Right hand: Windslash Bow (87)   Left hand: none / two-hand marker (254)
```

Role: ranged punishment on the player's climb to the shelves; they punish bad routes, not every tile.

### Summoner (Lv 101) — mid-tier summons

```text
Job: Summoner (82)   JobLevel: 8
Secondary: Item or low-tier White Magic if legal; no Time Magic / no hard control
Primary: Summon (mid-tier: Ifrit / Shiva / Ramuh / Titan — NOT best summons; reserved later)
Reaction: Reflexes (449)   Support: MA/Magick-boost (id TBD)   Movement: Movement +1 (486)
Head: cloth/mage hat (id TBD)   Body: shop robe (id TBD)
Accessory: Featherweave Cloak (234)   Right hand: shop magic-boost rod (id TBD)   Left: none (255)
```

Role: shells the approach lane; charge times intact so it can be raced/interrupted.

## Positioning Plan

```text
Izlude starts ELEVATED on the shelves, screened, with Mighty-Sword reach over the approach — the
  player must climb/Jump to him while their gear is at risk from range.
The 2 Knights start on the lower lane between the player and the shelves; the Rend Knight should
  guard the most direct route, while the non-Rend Knight blocks without multiplying break pressure.
The 2 Archers cover the climb from different angles, but their lines should not overlap into a
  total shelf lock; the Summoner starts back with a sightline onto the approach cluster and remains
  reachable/interruption-friendly.
Preserve the tall-shelf high ground and the Jump-4+/climb requirement.
Preserve the "defeat Izlude ends the fight" objective and the chain link into the 1st Level.
```

The vault should say: "the Templar fights from the high shelves and breaks your blades from afar —
climb to him, keep your gear, and end it with steel, not spells."

## Simulation Plan and Results

Simulation artifact:

```text
tmp/fft-level-design-028-monastery-vaults-3rd/
```

Model scope:

```text
First four rounds only; compares break pressure, vertical delay, ranged/summon pressure, and chain
tax into Wiegraf. It rejects extra bodies, a second Rend Knight, and hard-control support.
```

Iteration results:

| Candidate | Enemies | Action ratio | Break pressure | Vertical delay | Ranged pressure | Total pressure | Chain tax | Answerability | Result |
|-----------|---------|--------------|----------------|----------------|-----------------|----------------|-----------|---------------|--------|
| v1 elevated Templar shell | 6 | 0.86 | 50.0 | 41.6 | 49.2 | 148.8 | 22.3 | 52.6 | Baseline |
| v2 chain-safe complete Templar cell | 6 | 0.91 | 51.0 | 42.3 | 51.0 | 161.3 | 23.2 | 57.9 | Accepted |
| Dual-Rend bodyguard stack | 6 | 0.91 | 67.0 | 45.3 | 55.8 | 185.1 | 27.8 | 47.5 | Rejected: too many break sources / chain tax |
| Extra Archer shelf lock | 7 | 1.06 | 53.0 | 48.5 | 68.3 | 200.8 | 32.4 | 45.5 | Rejected: extra body / chain tax |
| Time Mage support trap | 6 | 0.91 | 53.0 | 44.1 | 59.1 | 189.2 | 35.1 | 34.0 | Rejected: hard-lock / chain tax |

Decision:

```text
Keep the six-enemy vanilla roster and complete every setup. Izlude plus one Rend Knight is enough
break pressure for a fair Chapter 3 chain fight. Reject the second Rend Knight, extra ranged body,
and hard-control support because they overtax the no-resupply path into Wiegraf.
```

## Current Implementation (v1, entry 423 — superseded by v2 design)

The shipped v1 already establishes Izlude, Reflect Mail, and the canonical escort on entry 423.
The v2 redesign above is **documentation only** in this pass; it requires a later implementation
pass to add mandatory secondary setups, cap Rend to one Knight, and validate the Vaults chain.

## Future Implementation Checklist (v2)

- [x] Identify Vaults 3rd ENTD entry 423; fill "Local Data Confirmed".
- [x] Dump original entry; verify Izlude + 2 Knight + 2 Archer + 1 Summoner + player slots.
- [ ] Confirm Knights Templar / Summoner job ids; keep Izlude's dual-wield + Mighty-Sword breaks.
- [ ] Assign REFLECT MAIL as Izlude's body armor AND rare drop/steal (mid-high verify).
- [ ] Constrain Mighty Sword (telegraphed breaks, no hard lock); Rend on ONE Knight only; summons mid-tier.
- [ ] Set levels: Izlude `103`; Knights + Summoner + one Archer `101`; second Archer `100`.
- [ ] Set JobLevel `8` on all active enemy slots.
- [ ] Give every active human enemy full equipment plus secondary/reaction/support/movement.
- [ ] Preserve no-resupply chain balance into Wiegraf; no extra body, no Time Mage, no second Rend Knight.
- [ ] PRESERVE the shelf high ground, the "defeat Izlude ends fight" objective, and the chain link.
- [ ] Patch via the correct layer in a later implementation pass; no binary/data change in this doc pass.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify objective + Reflect Mail.
- [ ] Install mod, test from a New Game+ save; confirm reaching/killing Izlude ends the fight fairly.

## Test Questions

- Is reaching the elevated Izlude a real verticality puzzle (Jump/climb) under screen + summon fire?
- Do his Mighty-Sword breaks threaten gear from range while staying counterable (Safeguard/race)?
- Does the one-Rend cap keep break pressure scary without draining the Wiegraf chain?
- Does Reflect Mail meaningfully push the player to PHYSICAL damage on Izlude (magic bounces)?
- Does defeating Izlude end the fight, rewarding a decapitation race on the one-loadout chain?
- Is Reflect Mail clearly mid-high (above Ch2's rare baseline, below Genji/best armor)?
- Does the Knights Templar read as a distinct new caste (break-from-range elite)?
- Is it a 3/5★ sub-boss step above the 2nd Level but below the Wiegraf boss, without burning the
  inventory needed for the 1st Level?
- Does it still read as a Templar holding a vault, not a designed arena?

## Sources

- Game8, "Monastery Vaults: Third Level Walkthrough (Battle 25)": roster (Izlude/Isilud + 2 Knight,
  2 Archer, 1 Summoner), objective "Defeat Isilud!", recommended level ~28, 3/5 stars, deploy 5,
  Izlude on shelf high ground + dual-wield, defeating him ends the fight, tall-shelf terrain (Jump
  4+), no-resupply chain into the 1st Level, rewards.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553185
- Final Fantasy Wiki, "Izlude Tingel" / "Knights Templar": story + Mighty Sword context.
  https://finalfantasy.fandom.com/wiki/Izlude_Tingel
- Local: `docs/battles/024-chapter-3-overview.md` (Chapter 3 complete-party + rare-loot rules),
  `027-monastery-vaults-2nd.md` (chain 1/3), `029-monastery-vaults-1st.md` (chain 3/3),
  `016-balias-tor.md` & `021-lionel-castle-gate.md` (Rend/break + Summoner precedents),
  `020-golgollada-gallows.md` (disarm/break boss pattern).
