# 032 - The Yuguewood (Yuguo Woods)

Status: designed (not yet implemented)
Chapter: 3 — "The Valiant"
Battle order: Battle 29 (after Walled City of Yardrow)
Target version: Enhanced v1.5.0
ENTD: global entry **TBD** — confirm on Windows game data
File: `battle_entd*_ent.bin` (TBD) / `OverrideEntryData` rows (TBD)

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `024-chapter-3-overview.md`.

## Original Battle

Objective:

```text
Defeat all enemies!
```

Player deployment:

```text
Up to 5 units, including Ramza. No guests.
```

Original enemy composition:

```text
1x Ghoul     (undead — reraises; status touch)
1x Ghast     (undead — reraises; status touch)
1x Revenant  (undead — reraises; tougher body)
2x Black Mage (ranged elemental magic)
2x Time Mage  (Haste the undead / Slow the player)
```

Public walkthrough details:

```text
Recommended level: ~33.  Difficulty: 2/5 stars.
Swamp woods with mobility challenges (soft/awkward terrain).
The undead RERAISE and revive unless permakilled; HEALING magic DAMAGES them, and a Chemist's
  Phoenix Down / Hi-Potion INSTAKILLS them. Mustadio's SEAL EVIL petrifies them out of the fight,
  and an Orator's ENTICE can flip an undead to your side (Traitor).
The Black Mages add ranged elemental damage; the Time Mages HASTE the undead (more attacks) and
  SLOW the player.
```

Design reading:

The Yuguewood is **the second undead fight — now with a living caster backline**. Where Tchigolith
(`017`) was a pure-monster undead bog, Yuguo pairs reraising undead with **Black Mage magic and
Time-Mage tempo**: the undead won't stay dead (permakill with Phoenix Down / Holy / Seal Evil),
while the casters shell you from range and **Haste the undead** so they swing more often and **Slow**
your cleanup. The swamp hampers movement, making the attrition bite. The lesson builds on Tchigolith
— *weaponize healing against the undead, permakill them* — but adds **tempo and ranged pressure**,
so the player must close the kill faster before the Hasted dead and the mages grind them down. The
player's own anti-undead tools (Phoenix Down, Holy, Seal Evil, even Entice) are richly rewarded.

For New Game++ the identity must stay: **a swampy undead attrition fight where reraising dead must be
permakilled with healing/Holy/Seal Evil, now Hasted by Time Mages and shelled by Black Mages —
won by closing the permakill faster under tempo and ranged pressure.**

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm slots: 1 Ghoul + 1 Ghast + 1 Revenant + 2 Black Mage + 2 Time Mage, plus the player slots.
CRITICAL: preserve the UNDEAD flags (reraise/revive + heal-damages-undead + Phoenix-Down-instakill +
  Seal-Evil-petrify + Entice-able) on the Ghoul/Ghast/Revenant. These ARE the fight.
Keep the swamp terrain / mobility flags (the bog is part of the attrition).
Keep Time Mage to Haste/Slow only; keep Black Mage cast cadence normal.
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
```

Job/monster IDs (verify all in-game):

```text
Ghoul / Ghast / Revenant monster ids (TBD - verify; undead, reraise)
Black Mage job id   (TBD - verify)
Time Mage job id    (TBD - verify; from Ch1 Lenalian / Ch2 Goug & Gallows / Vaults 027)
```

## Job Escalation (Chapter 3 rule)

```text
THE WRINKLE IS THE CASTER BACKLINE ON THE UNDEAD: unlike Tchigolith (017, pure monsters), the Yuguo
undead are supported by 2 Black Mages (ranged magic) and 2 Time Mages (Haste the dead / Slow you).
The living caster support IS this fight's escalation — it adds tempo + ranged pressure to the
permakill puzzle. Per "one new wrinkle per fight," NO brand-new caste is introduced (the enemy
Orator/Mediator already debuted at Gollund 025; Oracle is NOT in this roster). Keep the
3-undead / 2 Black Mage / 2 Time Mage shape.
WHY: reraising undead under Haste + magic is a meaningfully harder version of the Tchigolith puzzle;
  stacking a new caste on top would overload a 2/5★ fight. (Note: the OVERVIEW initially guessed an
  "Oracle" here — the real roster has Black/Time Mages instead; corrected.)
```

## Sanctioned exceptions (carried precedents)

```text
UNDEAD reraise + heal-weakness — allowed and intended (Tchigolith 017 precedent): preserved as
  mechanic AND counterplay (Phoenix Down / Hi-Potion / Holy permakill; Seal Evil petrify; Entice flip).
TIME MAGE control — allowed (Lenalian 007 / Goug 018 / Gallows 020 / Vaults 027 precedent): the TWO
  Time Mages are Haste (on the undead) / Slow (on the player) / Float ONLY. NO Stop, Immobilize,
  Don't Move, Don't Act. They amplify the undead (the headline), not lock the player.
ONE-DISRUPTOR mass-status cap (017): the undead's status is single-target touch only; there is NO
  mass-status monster here (no Malboro), so the cap is respected — do NOT add one.
```

## Boss rare loot

```text
None. No named boss here — no rare boss item (per the Chapter 3 overview). The undead/casters stay
shop-tier (monsters carry no gear). The map's rare TREASURE (Bestiary / Mythril Spear / Iron Fan /
Damask Cloth) is existing map treasure, not boss loot; leave it as-is.
```

## Proposed Composition (New Game++ Yuguewood v1)

Keep the exact roster; scale and preserve the undead + tempo mechanics. The Revenant and one Time
Mage anchor at `101`–`102`; the rest at `100`–`101`. Moderate (2/5★).

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Revenant (undead) | Revenant | `101` | Tougher reraising body; attrition anchor. |
| n | Ghoul (undead) | Ghoul | `100` | Reraises; status touch; bog melee. |
| n | Ghast (undead) | Ghast | `100` | Reraises; status touch; second dead body. |
| n | Time Mage | Time Mage | `101` | Hastes the undead (more swings) / Slows the player. |
| n | Time Mage | Time Mage | `101` | Second tempo caster; reinforces the Hasted-dead clock. |
| n | Black Mage | Black Mage | `101` | Ranged elemental damage on the player's cleanup line. |
| n | Black Mage | Black Mage | `100` | Second mage; punishes a clumped permakill. |

Reasoning:

The faithful move is to **preserve the undead mechanics and add tempo + ranged pressure**. The three
undead reraise unless permakilled, so a player who doesn't exploit Phoenix Down / Holy / Seal Evil
faces endless attrition — exactly Tchigolith's lesson — but now the Time Mages Haste the dead (faster
swings) and Slow the cleanup, while the Black Mages shell from range and punish clumping. The swamp
hampers repositioning, so the player must permakill efficiently under pressure. Modest levels keep it
a fair 2/5★ — a tempo'd undead attrition puzzle, harder than Tchigolith but not a wall, sitting
between Yardow and the Riovanes finale.

## Builds / Monster Tuning Notes

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Undead x3 — Ghoul / Ghast / Revenant (Lv 100–101)

```text
Set JobLevel 8; keep aggressive Brave so they press onto the player's line.
PRESERVE undead flags: reraise/revive timers, heal-damages-undead, Phoenix-Down/Hi-Potion-instakill,
  Seal-Evil-petrify, Entice-able. Keep their single-target status touch (poison/zombie/etc.).
No equipment (monsters); levers are Level, JobLevel, Brave, innate skill tier.
```

Role: the reraising attrition core — must be permakilled, not just dropped.

### Time Mage x2 (Lv 101) — Haste/Slow only

```text
Job: Time Mage (id TBD)   JobLevel: 8   Secondary: none
Skillset limit: Haste (on the undead) / Slow (on the player) / Float-tier ONLY.
  NO Stop, Immobilize, Don't Move, Don't Act.
Reaction: Reflexes (449)   Support: MA/Magick-boost (id TBD)   Movement: Movement +1 (486)
Head: cloth/mage hat (id TBD)   Body: shop robe (id TBD)
Accessory: Featherweave Cloak (234)   Right hand: shop magic-boost rod (id TBD)   Left: none (255)
```

Role: the tempo amplifier — Hasted undead swing more; Slow drags the player's permakill.

### Black Mage x2 (Lv 101 / 100)

```text
Job: Black Mage (id TBD)   JobLevel: 8   Secondary: none
Reaction: Reflexes (449)   Support: MA/Magick-boost (id TBD)   Movement: Movement +1 (486)
Head: cloth/mage hat (id TBD)   Body: shop robe (id TBD)
Accessory: Featherweave Cloak (234)   Right hand: shop magic-boost rod (id TBD)   Left: none (255)
```

Role: ranged elemental punishment on the cleanup line; forces the player to spread.

## Positioning Plan

```text
The three undead start spread across the bog between the player and dry ground, pressing melee.
The 2 Time Mages start back so they can Haste the undead turn 1; the 2 Black Mages flank with lines
  onto the player's likely cleanup cluster.
Preserve the swamp terrain / mobility flags so the attrition is felt.
Keep the undead reraise + all anti-undead counters intact.
```

The woods should say: "the dead won't lie down — burn them out with light and elixirs — but their
chronomancers keep them swinging and their mages keep you honest."

## Implementation Checklist

- [ ] Identify Yuguewood `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify 1 Ghoul + 1 Ghast + 1 Revenant + 2 Black Mage + 2 Time Mage.
- [ ] Confirm undead monster ids AND that undead flags (reraise + heal-weakness + PD-kill + Seal-Evil
      + Entice) persist; confirm Black/Time Mage ids.
- [ ] Constrain BOTH Time Mages to Haste/Slow (no hard lock); keep Black Mage cadence normal.
- [ ] Keep the undead's status touch single-target (no mass-status; one-disruptor cap respected).
- [ ] Set levels: Revenant + both Time Mages + one Black Mage `101`; Ghoul/Ghast + second Black Mage `100`.
- [ ] Set JobLevel `8`; aggressive Brave on the undead; no equipment on monsters.
- [ ] Preserve the swamp terrain / mobility flags.
- [ ] Patch via the correct layer; keep the diff inside the Yuguewood window only.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify undead + Haste fairness.
- [ ] Install mod, test from a New Game+ save; verify permakill (PD/Holy/Seal Evil) works under Haste.

## Test Questions

- Do the undead genuinely reraise, forcing permakill (Phoenix Down / Holy / Seal Evil)?
- Is "weaponize healing against the undead" rewarded, now under Time-Mage Haste pressure?
- Do the Black Mages + Slow make the player close the permakill faster (tempo matters)?
- Does the swamp terrain make the attrition bite without being unfair?
- Is the one-disruptor cap respected (single-target status only; no mass-status added)?
- Does it read as a HARDER Tchigolith (undead + casters) rather than a repeat?
- Is it a fair 2/5★ — above Tchigolith, below the Riovanes finale?

## Sources

- Game8, "The Yuguewood Walkthrough (Battle 29)": roster (1 Ghoul, 1 Ghast, 1 Revenant, 2 Black
  Mage, 2 Time Mage), objective "Defeat all enemies!", recommended level ~33, 2/5 stars, deploy 5,
  swamp terrain, undead heal-weakness + Phoenix-Down-instakill + Seal Evil petrify + Orator Entice,
  rewards/treasure.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553188
- Final Fantasy Wiki, "Yuguo Woods" + undead mechanics.
  https://finalfantasy.fandom.com/wiki/Yuguo_Woods
- Local: `docs/battles/024-chapter-3-overview.md` (job-escalation + rare-loot rules),
  `017-tchigolith-fenlands.md` (undead handling + one-disruptor cap), `018-goug-lowtown.md`
  (Time Mage Haste/Slow limit), `025-mining-town-gollund.md` (enemy Orator already debuted).
</content>
