# 028 - Monastery Vaults, 3rd Level — Izlude (Orbonne Monastery)

Status: designed (not yet implemented)
Chapter: 3 — "The Valiant"
Battle order: Battle 25 (after Vaults 2nd Level) — **Vaults chain 2 of 3**
Target version: Enhanced v1.5.0
ENTD: global entry **TBD** — confirm on Windows game data
File: `battle_entd*_ent.bin` (TBD) / `OverrideEntryData` rows (TBD)

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
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm slots: Izlude + 2 Knight + 2 Archer + 1 Summoner, plus the player slots.
DO NOT touch the "defeat Izlude ends the battle" objective scripting or the chain link into the 1st
  Level (Wiegraf).
Keep the tall-shelf high-ground geometry (the Jump-4+/climb-to-the-boss puzzle depends on it).
Keep Summoner charge times intact (race-the-cast counter).
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
```

Job IDs (carry over known, verify the rest in-game):

```text
77 = Archer            (confirmed)
Knight job id          (TBD - verify)
Summoner job id        (TBD - verify; from Balias Tor 016)
Knights Templar job id (TBD - verify; Izlude — dual-wield + Mighty Sword; FIRST Templar in the mod)
Reflect Mail item id   (TBD - verify; Izlude's rare — auto-Reflect armor)
```

## Job Escalation (Chapter 3 rule)

```text
THE NEW CASTE IS BUILT IN: Izlude debuts the KNIGHTS TEMPLAR — dual-wield + "Mighty Sword" ranged
equipment/stat breaks (an elevated Rend). The Templar boss IS this fight's escalation; per "one new
wrinkle per fight," NO additional generic job is swapped in. Keep the 2 Knight / 2 Archer / 1
Summoner screen.
WHY: a dual-wielding break-from-range boss on high ground is a dense new problem (your gear isn't
  safe even at distance, and he's hard to reach). Stacking another new caste would muddy it; Ninja,
  Oracle, and Velius debut in their own fights.
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
  Izlude). It is a real in-fight wrinkle AND a tempting steal/drop, clearly above Chapter 2's tier
  (Ancient Sword / 108 Gems) yet well below the Ch4-reserved best (Genji armor, best robes). First
  Chapter 3 rare drop.
STORY NUANCE: Izlude is decisively DEFEATED here (the fight ends on his fall), so the reward is paid
  out HERE. His later Riovanes Roof appearance (035) is a scripted cutscene death — NOT a second
  player-lootable kill — so there is no double-dip; do not also assign him a rare at 035.
DIFFERENTIATION: the marquee Templar KNIGHT SWORD rare (Defender) is reserved for Wiegraf (029), so
  Izlude's highlight is defensive (Reflect Mail), not a sword.
```

## Proposed Composition (New Game++ Vaults 3rd v1)

Keep the exact roster; Izlude is the elevated sub-boss spike. Izlude `103`; Knights `101`;
Summoner `101`; Archers `100`–`101`.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Izlude (SUB-BOSS, NEW caste) | Knights Templar | `103` | Dual-wield + Mighty-Sword breaks from the shelves; defeating him ENDS the fight. Reflect Mail. |
| n | Knight (Rend) | Knight | `101` | Screens the climb to Izlude; break-wall. |
| n | Knight | Knight | `101` | Second body; contests the vertical lane. |
| n | Archer | Archer | `101` | Ranged punishment on the climbers. |
| n | Archer | Archer | `100` | Second bow; covers the other shelf lane. |
| n | Summoner | Summoner | `101` | Mid-tier AoE shelling the approach; raises the cost of clumping. |

Reasoning:

The faithful move is to **make Izlude an elevated decapitation target and keep the break + summon
pressure**. At `103` on the shelves with dual-wield and Mighty-Sword breaks, he punishes a slow
approach and strips gear from range, while Reflect Mail forces the player to finish him physically;
the Knights/Archers screen the climb and the Summoner shells the lane. The intended solution holds:
build for verticality (Jump/climb), defend gear (Safeguard/Maintenance), and race a lane to Izlude
to end the fight before attrition wins — on the chain's one loadout. A 3/5★ sub-boss step, harder
than the 2nd Level, setting up the Wiegraf boss.

## Builds (final-shop quality; Knights Templar flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Izlude — Knights Templar SUB-BOSS (Lv 103) — rare: Reflect Mail

```text
Job: Knights Templar (id TBD)   JobLevel: 8   Primary: Mighty Sword (ranged equip/stat break)
Support: Dual Wield (id TBD — innate/equipped; two blades)
Reaction: Counter (442) or a parry reaction (id TBD)   Movement: Jump +? / Ignore Height (id TBD)
Head: shop helm (id TBD)   Body: REFLECT MAIL (id TBD — his rare; auto-Reflect)
Accessory: Bracers (218)   Right/Left hand: two shop-tier-best swords (ids TBD; not a reserved best)
Defeating him ENDS the battle. Reflect Mail = his drop/steal.
```

Role: the elevated Templar — breaks gear from range, reflects magic, ends the fight when he falls.

### Knight x2 (Lv 101) — 1x Rend

```text
Job: Knight (id TBD)   JobLevel: 8   Secondary: Rend (break) on ONE of the two (id TBD)
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head/Body: shop heavy helm + heavy armor (ids TBD)
Accessory: Bracers (218)   Right hand: Runeblade (30) / Icebrand (29)   Left: shop shield (id TBD)
```

Role: screens the vertical approach to Izlude; one carries Rend (Safeguard stays relevant).

### Archer x2 (Lv 101 / 100)

```text
Job: Archer (77)   JobLevel: 8   Secondary: none
Reaction: Reflexes (449)   Support: Concentration (469)   Movement: Movement +1 (486)
Head: Thief's Cap (168)   Body: Black Garb (198)   Accessory: Bracers (218)
Right hand: Windslash Bow (87)   Left hand: none / two-hand marker (254)
```

Role: ranged punishment on the player's climb to the shelves.

### Summoner (Lv 101) — mid-tier summons

```text
Job: Summoner (id TBD)   JobLevel: 8   Secondary: none
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
The 2 Knights start on the lower lane between the player and the shelves; the 2 Archers cover the
  climb; the Summoner starts back with a sightline onto the approach cluster.
Preserve the tall-shelf high ground and the Jump-4+/climb requirement.
Preserve the "defeat Izlude ends the fight" objective and the chain link into the 1st Level.
```

The vault should say: "the Templar fights from the high shelves and breaks your blades from afar —
climb to him, keep your gear, and end it with steel, not spells."

## Implementation Checklist

- [ ] Identify Vaults 3rd `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify Izlude + 2 Knight + 2 Archer + 1 Summoner + player slots.
- [ ] Confirm Knights Templar / Summoner job ids; keep Izlude's dual-wield + Mighty-Sword breaks.
- [ ] Assign REFLECT MAIL as Izlude's body armor AND rare drop/steal (mid-high verify).
- [ ] Constrain Mighty Sword (telegraphed breaks, no hard lock); Rend on ONE Knight; summons mid-tier.
- [ ] Set levels: Izlude `103`; Knights + Summoner + one Archer `101`; second Archer `100`.
- [ ] Set JobLevel `8` on all active enemy slots.
- [ ] PRESERVE the shelf high ground, the "defeat Izlude ends fight" objective, and the chain link.
- [ ] Patch via the correct layer; keep the diff inside the Vaults 3rd window only.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify objective + Reflect Mail.
- [ ] Install mod, test from a New Game+ save; confirm reaching/killing Izlude ends the fight fairly.

## Test Questions

- Is reaching the elevated Izlude a real verticality puzzle (Jump/climb) under screen + summon fire?
- Do his Mighty-Sword breaks threaten gear from range while staying counterable (Safeguard/race)?
- Does Reflect Mail meaningfully push the player to PHYSICAL damage on Izlude (magic bounces)?
- Does defeating Izlude end the fight, rewarding a decapitation race on the one-loadout chain?
- Is Reflect Mail clearly mid-high (above Ch2's tier, below Genji/best armor)?
- Does the Knights Templar read as a distinct new caste (break-from-range elite)?
- Is it a 3/5★ sub-boss step above the 2nd Level but below the Wiegraf boss?
- Does it still read as a Templar holding a vault, not a designed arena?

## Sources

- Game8, "Monastery Vaults: Third Level Walkthrough (Battle 25)": roster (Izlude/Isilud + 2 Knight,
  2 Archer, 1 Summoner), objective "Defeat Isilud!", recommended level ~28, 3/5 stars, deploy 5,
  Izlude on shelf high ground + dual-wield, defeating him ends the fight, tall-shelf terrain (Jump
  4+), no-resupply chain into the 1st Level, rewards.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553185
- Final Fantasy Wiki, "Izlude Tingel" / "Knights Templar": story + Mighty Sword context.
  https://finalfantasy.fandom.com/wiki/Izlude_Tingel
- Local: `docs/battles/024-chapter-3-overview.md` (job-escalation + rare-loot rules),
  `027-monastery-vaults-2nd.md` (chain 1/3), `016-balias-tor.md` & `021-lionel-castle-gate.md`
  (Rend/break + Summoner precedents), `020-golgollada-gallows.md` (disarm/break boss pattern).
</content>
