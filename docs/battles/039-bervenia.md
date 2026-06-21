# 039 - Free City of Bervenia

Status: ✅ implemented (v1, entry 443)
Chapter: 4 — "In the Name of Love"
Battle order: Battle 34 (after Dugeura Pass)
Target version: Enhanced v1.5.0
ENTD: global entry **443** (local entry 59, `battle_entd4_ent.bin`)
File: `battle_entd4_ent.bin` (embedded NG+ swap) — `tools/battle_patch.py bervenia`

Implemented composition (entry 443, vanilla-dump verified):
- s0 **Meliadoul** (job 47 Divine Knight, BOSS, dies → rare pays) — L104/jl8 (full Mighty Sword break);
  **Save the Queen (34)** as her equipped KnightSword (Tier-A rare/steal-bait, upgrades her vanilla
  Defender 33); job/secondary/helm/armor/acc/shield/win-on-death scripting preserved. No hard lock added.
- s1,s4 Summoner L102 — Mage Hat/shop Robe/Featherweave/shop Rod; intact charge times; Reflexes/Atk Boost/Mv+1.
- s2,s3 Archer L102/L101 — Thief's Cap/Black Garb/Bracers/Windslash (two-hand); Reflexes/Concentration/Mv+1.
- s5 Ninja L102 — dual-wield Ninja Longblades; Thief's Cap/Black Garb/Germinas; First Strike/Atk Boost/Mv+2.
- Only Meliadoul at the boss band (104); adds 101-102.

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `037-chapter-4-overview.md`.

## Original Battle

Objective:

```text
Defeat Meliadoul!   (the mission ends the instant she falls, regardless of remaining enemies)
```

Player deployment:

```text
Up to 5 units, including Ramza. No guests.
```

Original enemy composition (verified via Game8, Battle 34):

```text
Meliadoul Tengille   (BOSS — Knights Templar; Mighty Sword equipment-breaks)
2x Archer            (ranged chip / elevation)
2x Summoner          (AoE summon support)
1x Ninja             (fast dual-wield flanker / Throw)
```

Public walkthrough details:

```text
Recommended level: ~41.  Difficulty: 3/5 stars.  Deploy up to 5.  Win: defeat Meliadoul (ends fight).
Urban map (Free City of Bervenia) — streets and elevation; ranged support holds high ground.
THE THREAT — MELIADOUL: her "Unyielding Blade" (Mighty Sword) SHREDS your weapons and armor. The
  walkthrough's tips: equip SAFEGUARD to protect gear, and use STEAL WEAPON / STEAL ACCESSORY on her.
SUPPORT: two Summoners throw AoE; two Archers chip from elevation; one Ninja flanks fast.
Because the fight ENDS when Meliadoul falls, the optimal line is to rush/burst HER — the adds are a
  screen, not the objective.
Spoils: 25,100 Gil, 2x Remedy, 1x Jade Armlet. Buried (rare): Bloodstring Harp, Papyrus Codex,
  Partisan, Gokuu's Pole.
```

Design reading:

Bervenia is **the first true Chapter-4 boss duel**: Meliadoul is a full **Knights Templar** — the
caste Izlude debuted in Ch3 (`028`) — now at boss strength, and her **equipment-break** kit is the
whole identity. The fight is a race against attrition: her Mighty Sword can strip your weapons/armor,
so the player must answer with **Safeguard / Maintenance**, disarm her (Steal Weapon), and **burst the
boss** before the breaks pile up — all while a ranged screen (Summoners + Archers + a Ninja) tries to
keep the party off her. Because the win condition is *defeat Meliadoul*, it rewards focus over
mop-up.

For New Game++ the identity must stay: **an elite Templar boss-duel where the headline is her
gear-shredding Mighty Sword — answered by Safeguard and disarm — fought through a ranged support
screen, won by bursting the boss; the boss herself is the escalation, so the support cast stays
familiar.**

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm slots: Meliadoul (boss) + 2 Archer + 2 Summoner + 1 Ninja, plus the player slots.
Keep the win condition = "Defeat Meliadoul" (ends on her death) and the urban/elevation geometry.
Keep Meliadoul's Mighty Sword break kit + her steal-bait gear (Steal Weapon/Accessory must work).
This is a Tier-A BOSS fight: boss spike at 104, adds in the 100-103 band; ONE Tier-A rare on Meliadoul.
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
Leave the buried map treasure (Partisan / Gokuu's Pole / etc.) as-is — map loot, not boss loot.
```

Job IDs (carry over known, verify the rest in-game):

```text
77 = Archer            (confirmed)
Summoner job id        (TBD - verify; established caste)
Ninja job id           (TBD - verify; Ch3 debut, Yardow 031)
Knights Templar id     (TBD - verify; Meliadoul's boss job — Izlude precedent, 028)
```

## Job Escalation (Chapter 4 rule)

```text
CHANGE: NO generic-slot swap. The escalation is the BOSS — Meliadoul is a full Knights Templar with a
  boss-strength Mighty Sword break kit (the Ch3 Templar caste, Izlude/028, raised to boss tier).
WHY: the fight's identity is already "survive and disarm a gear-shredding Templar." The single, fitting
  escalation for Chapter 4 is to deliver that Templar at FULL boss power (more break range, higher
  level, steal-bait gear) — NOT to bolt a second new mechanic onto a roster that already has Summoners
  (AoE), Archers, and a Ninja. Adding another wrinkle would violate the one-new-demand rule; the boss
  IS the demand.
CONSTRAINT (carry Ch3 Templar precedent, 028/033): the break is TELEGRAPHED; Safeguard/Maintenance
  counter it; LIMIT/RANDOMIZE which slot she breaks (don't deterministically strip everything); no hard
  lock. She must remain a tempting, viable STEAL target (Steal Weapon/Accessory).
WHAT IS NOT CHANGED: the 2 Archer + 2 Summoner + 1 Ninja support screen and the "rush the boss to end
  it" win condition remain. No brand-new caste debuts here.
```

## Sanctioned exceptions (carried precedents)

```text
MIGHTY SWORD / EQUIPMENT BREAK (Meliadoul) — allowed as the boss's identity (Ch3 Templar precedent,
  Izlude 028 / Riovanes Gate 033): telegraphed, Safeguard/Maintenance counter, limited/randomized
  targeting, no hard lock. She is disarmable (Steal Weapon) — the intended answer.
SUMMONER AoE — mid-tier summons with INTACT charge times (race-able), as in Ch3 (028). Not new.
NINJA THROW / FLANK — ranged DAMAGE (not a status lock); pin/intercept counters (Ch3 Ninja, 031). Not new.
BREAK-SOURCE CAP — only Meliadoul breaks here (1 source), well within the carried ≤2-break-source cap.
```

## Boss rare loot

```text
MELIADOUL (boss) drops/carries ONE Tier-A rare: SAVE THE QUEEN (knight sword).
WHY IT FITS: she is a sword-wielding Knights Templar; a top-tier knight sword is her natural weapon and
  a genuine in-fight threat (she hits harder) AND a tempting STEAL (the walkthrough already says to
  Steal Weapon from her). Save the Queen is the best knight sword BELOW the Tier-S pair, so it is a
  clear upgrade over Ch3's Defender (Wiegraf, 034) without being best-in-slot.
TIER: A (mid-Chapter-4 best non-ultimate). NOT Ragnarok / Chaos Blade — those are Tier-S, reserved for
  the endgame sequence (47-53). Excalibur is excluded (iconic to Orlandeau, a player unit).
She DIES here (win = defeat Meliadoul), so the rare pays out — consistent with "retreat/flee = no drop."
```

## Proposed Composition (New Game++ Bervenia v1)

Keep the count (6) and the boss-duel shape; elevate Meliadoul to a full Templar boss, keep the support
screen. Boss `104`; Summoners `102`; Archers `101`–`102`; Ninja `102`.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Meliadoul (BOSS) | Knights Templar | `104` | Mighty Sword gear-break; the objective; Save the Queen steal-bait. |
| n | Summoner | Summoner | `102` | AoE summon support (charge times intact). |
| n | Summoner | Summoner | `102` | Second summoner — pins the party while Meliadoul presses. |
| n | Archer | Archer | `102` | Ranged chip from elevation. |
| n | Archer | Archer | `101` | Second archer; covers the approach lanes. |
| n | Ninja | Ninja | `102` | Fast flanker / Throw — harasses the player's now-fragile gear. |

Reasoning:

The faithful move is to **make the boss the whole escalation and leave the screen recognizable**.
Meliadoul at `104` with a telegraphed, Safeguard-counterable break kit and Save-the-Queen steal-bait
delivers the "survive + disarm + burst the Templar" duel at full Chapter-4 strength. The two Summoners,
two Archers, and Ninja stay as the ranged screen that makes reaching her a problem — no new mechanic
added, honoring the one-new-demand rule. The win condition (ends on her death) keeps the fight a focus
race, not a mop-up. Levels put only Meliadoul at the boss band (`104`); the adds sit at `101`–`102`.

## Builds (Chapter-4 quality; Knights-Templar duel flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Meliadoul (Lv 104) — BOSS (Knights Templar)

```text
Job: Knights Templar (id TBD)   JobLevel: 8   Primary: Mighty Sword (Crush Weapon/Armor/Helm/Shield/
  Accessory — LIMIT/RANDOMIZE the targeted slot; telegraphed)   Secondary: (light) basic
Reaction: Safeguard / Maintenance-equivalent or Counter (id TBD)   Support: Attack Boost (465)
  Movement: Movement +1 (486)
Head: Tier-A helm (Grand Helm-tier, id TBD)   Body: Tier-A heavy armor (id TBD)
Accessory: Tier-A accessory (id TBD)
Right hand: SAVE THE QUEEN (Tier-A knight sword, id TBD)   Left: Tier-A shield (Aegis-tier, id TBD)
```

Role: the objective and the threat — gear-shredding Templar; disarm her (Steal Weapon) and burst her.
Keep her steal-bait gear actually stealable; keep the break telegraphed and randomized (no hard lock).

### Summoner x2 (Lv 102) — AoE screen

```text
Job: Summoner (id TBD)   JobLevel: 8   Secondary: none
Mid-tier summons (Ifrit/Shiva/Ramuh-tier) with INTACT charge times (race-able).
Reaction: Reflexes (449)   Support: MA/Magick-boost (id TBD)   Movement: Movement +1 (486)
Head: mage hat (id TBD)   Body: shop robe (id TBD)
Accessory: Featherweave Cloak (234)   Right hand: magic-boost rod (id TBD)   Left: none (255)
```

Role: AoE pressure that pins the party while Meliadoul closes; race-able by killing the boss.

### Archer x2 (Lv 102 / 101) — elevation chip

```text
Job: Archer (77)   JobLevel: 8   Secondary: none
Reaction: Reflexes (449)   Support: Concentration (469)   Movement: Movement +1 (486)
Head: Thief's Cap (168)   Body: Black Garb (198)   Accessory: Bracers (218)
Right hand: shop high-tier bow (id TBD)   Left: none / two-hand marker (254)
```

Role: ranged chip from the rooftops; covers the lanes to the boss.

### Ninja (Lv 102) — flanker

```text
Job: Ninja (id TBD)   JobLevel: 8   Secondary: Throw
Reaction: First Strike (453)   Support: Attack Boost (465)   Movement: Movement +2 (487)
Head: Thief's Cap (168)   Body: Black Garb (198)   Accessory: Germinas Boots (210)
Right hand: shop ninja blade (id TBD)   Left: shop ninja blade (id TBD) / dual-wield
```

Role: fast flanker — Throw harasses the player's now-fragile gear; pin/intercept to answer.

## Positioning Plan

```text
Urban map: Meliadoul starts mid, on or near the player's approach so she can press the break early;
  the two Summoners hold back/elevation with AoE sightlines; the two Archers take the rooftops; the
  Ninja starts wide to flank.
Preserve the elevation geometry (ranged support on high ground) and the "rush the boss" line —
  Meliadoul should be reachable but screened, so the duel is a fight THROUGH the support, not around it.
Keep Meliadoul's break telegraphed and her gear stealable; do not surround the player so tightly that
  Safeguard becomes mandatory rather than a smart answer.
```

The city should say: "a Templar holds the free city — protect your gear, disarm her blade, and cut
her down before her sword unmakes your party."

## Implementation Checklist

- [ ] Identify Bervenia `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify Meliadoul + 2 Archer + 2 Summoner + 1 Ninja + player slots.
- [ ] Keep win condition = "Defeat Meliadoul" (ends on her death).
- [ ] Set Meliadoul `104` with Mighty Sword break — LIMIT/RANDOMIZE the slot, telegraphed, no hard lock.
- [ ] Equip Meliadoul with Save the Queen (Tier-A) + Tier-A armor/shield; confirm STEAL WEAPON works.
- [ ] Keep Summoner charge times intact; keep Ninja Throw as ranged damage (not a lock).
- [ ] Set add levels: Summoners + one Archer + Ninja `102`; second Archer `101`.
- [ ] Set JobLevel `8` on all active enemy slots.
- [ ] Patch via the correct layer; keep the diff inside the Bervenia window only.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify break + steal + win-cond.
- [ ] Install mod, test from a New Game+ save; confirm it plays as a Templar break-duel.

## Test Questions

- Is Meliadoul's Mighty Sword break a real but FAIR threat (telegraphed, randomized slot, Safeguard /
  Steal Weapon answer it) — never a hard lock?
- Is she a tempting, viable STEAL (Save the Queen) — rewarding the disarm line?
- Does "Defeat Meliadoul ends the fight" still make it a focus-burst race, not a mop-up?
- Do the Summoners (intact charge times) + Archers + Ninja form a fair screen, not an AoE wall?
- Is only Meliadoul at the boss band (`104`), adds `101`-`102` — a Tier-A boss, not a spike?
- Does it read as an elite Templar holding an urban city, a clear step up from Izlude (`028`)?

## Sources

- Game8, "Free City of Bervenia Walkthrough (Battle 34)": roster (Meliadoul boss + 2 Archer +
  2 Summoner + 1 Ninja), objective "Defeat Meliadoul!", recommended level ~41, 3/5 stars, deploy 5,
  Unyielding-Blade gear-break + Safeguard/Steal-Weapon tips, spoils (25,100 Gil, Jade Armlet) + buried
  treasure (Partisan, Gokuu's Pole, etc.).
  https://game8.co/games/Final-Fantasy-Tactics/archives/553194
- Final Fantasy Wiki, "Bervenia Free City" / "Meliadoul Tengille": story/terrain context.
  https://finalfantasy.fandom.com/wiki/Meliadoul_Tengille
- Local: `037-chapter-4-overview.md` (job-escalation + Tier-A rare-loot rules),
  `028-monastery-vaults-3rd.md` (Izlude — Knights Templar / Mighty Sword precedent),
  `033-riovanes-castle-gate.md` (Templar break + Safeguard precedent), `031-walled-city-yardrow.md`
  (Ninja precedent).
```
</content>
