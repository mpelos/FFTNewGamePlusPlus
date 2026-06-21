# 038 - Dugeura Pass (Doguola Pass)

Status: ✅ implemented (v1, entry 442)
Chapter: 4 — "In the Name of Love"
Battle order: Battle 33 (Chapter 4 opener)
Target version: Enhanced v1.5.0
ENTD: global entry **442** (local entry 58, `battle_entd4_ent.bin`)
File: `battle_entd4_ent.bin` (embedded NG+ swap) — `tools/battle_patch.py dugeura`

Implemented composition (entry 442, vanilla-dump verified) — roster matched [76,77,80,80,87,87]:
- s0 Knight L101 — Heavy Helm/Heavy Armor/Bracers/Runeblade/shop Shield; Counter/Atk Boost/Mv+1.
- s1,s3 Black Mage L102 — Mage Hat/shop Robe/Featherweave/shop Rod; Reflexes/Atk Boost/Mv+1 (AoE priority).
- s2 Archer→**Time Mage** L102 — Mage Hat/shop Robe/Featherweave/shop Staff; **jl4** (Haste/Slow/Float only); Reflexes/Mv+1.
- s4,s5 Dragoon L102/L101 — Heavy Helm/Heavy Armor/Germinas/Partisan/shop Shield; Jump innate; Reflexes/Atk Boost/Mv+1.
- No boss → no rare; bottom-of-band levels (opener, not a spike).

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `037-chapter-4-overview.md`.

## Original Battle

Objective:

```text
Defeat all enemies!
```

Player deployment:

```text
Up to 5 units, including Ramza. No guests.
```

Original enemy composition (verified via Game8, Battle 33):

```text
1x Knight       (front-line bruiser)
1x Archer       (ranged chip)
2x Black Mage   (high-level AoE — the priority threat)
2x Dragoon      (Jump — vanish off-screen, untargetable until they land)
```

Public walkthrough details:

```text
Recommended level: ~41.  Difficulty: 3/5 stars.  Deploy up to 5.  Win: defeat all enemies.
Open field map (standard layout — no scripted pincer).
THREAT 1 — BLACK MAGES: two of them, in Black Robes (boosted elemental), throwing high-level AoE that
  can catch several of your units at once. The walkthrough's #1 tip: KILL THE BLACK MAGES FIRST.
THREAT 2 — DRAGOONS: two of them Jump, vanishing off-screen and untargetable until they land on a
  marked panel — step your units OFF the marked panels to dodge.
Map (buried) treasure: Ether/Diamond Sword, Remedy/Wizard's Rod, Maiden's Kiss/Golden Staff,
  Phoenix Down/Windslash Bow. Spoils: 27,200 Gil, Diamond Armor.
```

Design reading:

Dugeura Pass is **the Chapter 4 "welcome to the endgame" fight**: no boss, but the generics have
levelled hard (rec ~41) and the map teaches the two threats that define the chapter's open-field
battles — **AoE casters you must rush down, and Jump units you must dodge by reading the floor.** Its
identity is a clean two-axis priority puzzle: *burst the Black Mages before their AoE compounds, while
keeping your formation off the Dragoons' landing panels.* It is the first time both pressures appear
together at full strength.

For New Game++ the identity must stay: **an open-field skirmish whose whole lesson is "kill the AoE
casters fast and dance off the Jump panels," now sharpened by one tempo escalation — without turning
the chapter opener into a boss fight.**

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm slots: 1 Knight + 1 Archer + 2 Black Mage + 2 Dragoon, plus the player slots.
Keep the open-field geometry and the Dragoon Jump behavior (untargetable-while-airborne) — these ARE
  the fight. Keep the two Black Mages in Black-Robe-equivalent (boosted elemental AoE).
This is the chapter OPENER: no boss, no rare; modest Ch4 levels (100-102), not a spike.
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
Leave the buried map treasure as-is (existing map loot, not boss loot).
```

Job IDs (carry over known, verify the rest in-game):

```text
77 = Archer            (confirmed)  — note: SWAPPED OUT below
Knight job id          (TBD - verify)
Black Mage job id      (TBD - verify)
Dragoon / Lancer id    (TBD - verify; enemy Dragoon caste, debuted as enemy at the Vaults, 027)
Time Mage job id       (TBD - verify; the single swapped-in escalation slot)
```

## Job Escalation (Chapter 4 rule)

```text
CHANGE: swap the lone ARCHER -> a TIME MAGE that HASTES the Dragoons (and may Slow the player).
WHY: the fight's two-axis identity is "burst the AoE casters / dodge the Jumps." The single, fitting
  escalation is to TIE THE TWO AXES TOGETHER: a Time Mage that Hastes the Dragoons makes the Jump
  cadence faster (sharper panel-dodging) AND adds a third must-kill caster — so "kill the casters
  first" becomes more urgent without changing the plan. It INTENSIFIES the existing puzzle; it does
  not replace it.
CONSTRAINT: Time Mage uses Haste/Slow/Float ONLY (no Stop/Immobilize/Don't Act) — amplify the
  headline, never hard-lock the endgame party (carried Ch2/Ch3 Time-Mage precedent).
WHAT IS NOT CHANGED: the two Black Mages (AoE priority), the two Dragoons (Jump), and the lone Knight
  front-line all remain. No brand-new caste debuts here — Samurai/Lucavi/Ultima-Demons debut in their
  own fights. The opener stays an open-field skirmish, not a boss fight.
NOTE: this corrects the overview's tentative "pincer" guess — the verified map is an open field with
  no scripted two-sided ambush; the wrinkle is tempo (Haste), not geometry.
```

## Sanctioned exceptions (carried precedents)

```text
TIME MAGE CONTROL — Haste/Slow/Float only, normal cast cadence; no hard lock (Ch2/Ch3 precedent).
DRAGOON JUMP — preserved as designed: telegraphed landing panel, untargetable while airborne; the
  counter is to step OFF the marked panel / kill the Dragoon while grounded (Ch3 Vaults precedent, 027).
BLACK MAGE AoE — boosted elemental (Black-Robe-equivalent); strong but race-able by rushing the casters.
  No new exception introduced.
```

## Boss rare loot

```text
None. No named boss here — no rare boss item (per the Chapter 4 overview tiering). Generics stay
Chapter-4 shop-tier. The map's buried treasure (Diamond Sword / Wizard's Rod / Golden Staff /
Windslash Bow) is existing map treasure, not boss loot — leave it as-is.
```

## Proposed Composition (New Game++ Dugeura Pass v1)

Keep the count (6) and the open-field feel; swap the Archer for a Haste Time Mage. Modest Chapter-4
levels — this is the opener, not a spike. Casters anchor at `102`; the rest `101`.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Black Mage | Black Mage | `102` | High-level AoE (boosted elemental) — priority kill #1. |
| n | Black Mage | Black Mage | `102` | Second AoE caster — compounds damage if ignored. |
| n | Dragoon | Dragoon | `102` | Jump — untargetable while airborne; lands on a marked panel. |
| n | Dragoon | Dragoon | `101` | Second Jumper — staggered leaps pressure the back-line. |
| n | Time Mage (NEW) | Time Mage | `102` | Hastes the Dragoons / Slows the player — the tempo escalation. |
| n | Knight | Knight | `101` | Lone front-line bruiser; screens the casters. |

Reasoning:

The faithful move is to **keep the two-axis open-field puzzle and add exactly one tempo wrinkle**. The
two Black Mages stay as the AoE priority the walkthrough is built around; the two Dragoons stay as the
Jump-dodging threat; the lone Knight stays as the body that screens them. Swapping the Archer for a
Haste Time Mage **welds the axes together** — the casters are now even more urgent to kill because one
of them is accelerating the Jumps. Levels sit at the bottom of the Chapter-4 band (`101`–`102`, no
`103`) so the opener establishes "enemies are stronger now" without spiking before Bervenia.

## Builds (Chapter-4 shop quality; conspirators'-ambush flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Black Mage x2 (Lv 102) — AoE priority

```text
Job: Black Mage (id TBD)   JobLevel: 8   Secondary: none
Lean into high-level AoE (Fire/Bolt/Ice 3-tier). Black-Robe-equivalent body (boosted elemental).
Reaction: Reflexes (449)   Support: MA/Magick-boost (id TBD)   Movement: Movement +1 (486)
Head: mage hat (id TBD)   Body: Black Robe / boosted-elemental robe (id TBD)
Accessory: Featherweave Cloak (234)   Right hand: magic-boost rod (id TBD)   Left: none (255)
```

Role: the priority kill — two of them, AoE that compounds if the player doesn't rush them.

### Dragoon x2 (Lv 102 / 101) — Jump

```text
Job: Dragoon / Lancer (id TBD)   JobLevel: 8   Primary: Jump
Reaction: Reflexes (449)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head: shop helm (id TBD)   Body: shop heavy armor (id TBD)   Accessory: Germinas Boots (210)
Right hand: shop spear (id TBD)   Left: shop shield (id TBD)
```

Role: vertical pressure — Jump from range/elevation onto the back-line; dodge by leaving the panel.

### Time Mage (Lv 102) — NEW (tempo)

```text
Job: Time Mage (id TBD)   JobLevel: 8   Secondary: none
Cast HASTE on the Dragoons (and Slow on the player). Haste/Slow/Float ONLY — no Stop/Don't Act.
Reaction: Reflexes (449)   Support: MA/Magick-boost (id TBD)   Movement: Movement +1 (486)
Head: mage hat (id TBD)   Body: shop robe (id TBD)
Accessory: Featherweave Cloak (234)   Right hand: magic-boost rod (id TBD)   Left: none (255)
```

Role: the single escalation — speeds the Jumps and adds a third must-kill caster.

### Knight (Lv 101) — front-line

```text
Job: Knight (id TBD)   JobLevel: 8   Primary: (basic) Mighty Sword / Rend (limited — see note)
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head: shop helm (id TBD)   Body: shop heavy armor (id TBD)   Accessory: Bracers (218)
Right hand: shop knight sword (id TBD)   Left: shop shield (id TBD)
```

Role: the lone body that screens the casters; keep Rend limited (carried ≤2-break-source cap — here
just one Knight, well within it).

## Positioning Plan

```text
Open field: the two Black Mages start mid/back with clear sightlines, the two Dragoons on or near the
  high ground (good Jump arcs onto the player back-line), the Time Mage tucked behind the casters, the
  Knight forward as the screen.
Preserve the open-field geometry and the Dragoons' Jump panels (untargetable-while-airborne).
Spread the enemy so the player can't AoE the whole band at once — forcing the "rush the casters while
  dodging Jumps" read the fight is about.
Do NOT over-scale: bottom-of-band levels keep this the chapter opener, not a spike.
```

The pass should say: "the conspiracy's hunters open Chapter 4 — burn down their mages before the AoE
piles up, and keep your feet off the dragoons' landing marks."

## Implementation Checklist

- [ ] Identify Dugeura Pass `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify 1 Knight + 1 Archer + 2 Black Mage + 2 Dragoon + player slots.
- [ ] Swap the Archer -> Time Mage; restrict it to Haste/Slow/Float (no hard lock).
- [ ] Keep the open-field geometry + Dragoon Jump panels (untargetable while airborne).
- [ ] Keep both Black Mages on boosted-elemental AoE (Black-Robe-equivalent).
- [ ] Set levels: both Black Mage, one Dragoon, Time Mage `102`; other Dragoon + Knight `101`.
- [ ] Set JobLevel `8` on all active enemy slots; keep Jump on the Dragoons.
- [ ] Patch via the correct layer; keep the diff inside the Dugeura Pass window only.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify Jump + AoE intact.
- [ ] Install mod, test from a New Game+ save; confirm it plays as an open-field AoE/Jump opener.

## Test Questions

- Are the two Black Mages still the clear priority (AoE that compounds if ignored)?
- Do the Dragoons still Jump (untargetable while airborne) so the player must read the landing panels?
- Does the swapped-in Time Mage sharpen the tempo (faster Jumps / urgency to kill casters) WITHOUT
  hard-locking the player (Haste/Slow only)?
- Is it clearly the chapter OPENER (3/5★ feel, no boss, bottom-of-band levels) — establishing Ch4
  power without spiking before Bervenia?
- Does it still read as an open-field ambush by mages and dragoons, not a designed arena?
- Is the lone Knight a fair screen (one Rend source at most), not a break-lock?

## Sources

- Game8, "Dugeura Pass Walkthrough (Battle 33)": roster (1 Knight, 1 Archer, 2 Black Mage, 2 Dragoon),
  objective "Defeat all enemies!", recommended level ~41, 3/5 stars, deploy 5, Black-Mage-priority +
  Dragoon-Jump tips, buried treasure + spoils (27,200 Gil, Diamond Armor).
  https://game8.co/games/Final-Fantasy-Tactics/archives/553193
- Final Fantasy Wiki, "Doguola Pass": story/terrain context.
  https://finalfantasy.fandom.com/wiki/Doguola_Pass
- Local: `037-chapter-4-overview.md` (job-escalation + best-tier rare-loot rules),
  `027-monastery-vaults-2nd.md` (enemy Dragoon Jump precedent), `030-grogh-heights.md` (open-field
  skirmish + Black Mage build template).
```
</content>
