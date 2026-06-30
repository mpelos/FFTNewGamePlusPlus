# 001 - Magick City of Gariland

Status: final-shop v1 implemented  
Chapter: 1  
Battle order: Battle 2, first Chapter 1 battle after Orbonne prologue  
Target version: Enhanced v1.5.0  
ENTD: global entry `388`  
File: `battle_entd4_ent.bin`  
Local entry in file: `4`

## Original Battle

Objective:

```text
Defeat all enemies.
```

Player deployment:

```text
Up to 5 units, including Ramza.
Delita participates as a guest/allied story unit.
```

Original enemy composition:

```text
4x Squire
1x Chemist
```

Public walkthrough details:

```text
Recommended level: 1
Difficulty: 1 star
No treasure chest rewards
Listed spoils include gil, Phoenix Down, Potion, and Mythril Knife
```

NG++ spoils applied:

```text
Air Knife (9)
Phoenix Down (253)
X-Potion (242)
```

This preserves the original reward categories: Mythril Knife -> Air Knife, Phoenix Down stays
Phoenix Down, Potion -> X-Potion.

Design reading:

Gariland is not supposed to be a boss fight. It is a street fight against low-grade thieves
inside a city. The original battle teaches basic formation, melee pressure, chemist healing,
and how quickly Delita can collapse weak enemies.

For New Game++, the fight should say: "story battles scale now", but it should not become a
hard wall before the player has even reached Mandalia Plain.

## Local Data Confirmed

Entry `388` unit dump from the original v1.5.0 Enhanced data:

| Slot | Role read | Level | MainJob | Notes |
|------|-----------|-------|---------|-------|
| 0 | special/player-side | `1` | `4` | Leave untouched. Looks like Ramza/special formation slot. |
| 1 | enemy | `1` | `74` | Squire. |
| 2 | enemy | `1` | `74` | Squire. |
| 3 | enemy | `1` | `74` | Squire. |
| 4 | enemy | `1` | `75` | Chemist. |
| 5 | enemy | `1` | `74` | Squire. |

Confirmed job IDs:

```text
74 = generic enemy Squire
75 = generic enemy Chemist
```

Likely job IDs to verify before implementation:

```text
77 = Archer, inferred from classic job order and nearby ENTD usage
83 = Thief, inferred from classic job order and nearby ENTD usage
```

Existing successful validation patch:

| Slot | File offset | Old level | New level |
|------|-------------|-----------|-----------|
| 1 | `0x00A2B` | `1` | `100` |
| 2 | `0x00A53` | `1` | `100` |
| 3 | `0x00A7B` | `1` | `100` |
| 4 | `0x00AA3` | `1` | `100` |
| 5 | `0x00ACB` | `1` | `100` |

Result: tested in-game and confirmed story enemy scaling works.

Guest join note:

```text
Delita is not the entry 388 slot 0 unit. He is cached into the save when he joins the party
before Gariland, using the confirmed fingerprint record at entry 392 slot 1.

Entry 392 slot 1:
- Level already scales at 100.
- Squire Job Level test now keeps `JobUnlock` on Squire (`0x01430` / slot byte `0x08 = 1`)
  and raises the seeded JobLevel (`0x01431` / slot byte `0x09 = 8`).
- Prior test with `0x08 = 7, 0x09 = 8` gave Delita Time Mage Job Level 8, proving `0x08`
  is a job/JP target index, not a visible rank.

As with the level fix, this only applies when testing from a save before Delita joins or from a
fresh New Game+ start. Saves where Delita already joined keep the old cached JobLevel.

Autosave repair for the bad cached test:
- Delita's cached job levels are packed nibbles at `br_fa + 0x56`; job JP u16s start at
  `br_fa + 0x62`.
- Bad cached state: Squire Lv1 JP28, Time Mage Lv8 JP1172.
- Repaired state: Squire Lv8 JP1172, Time Mage Lv1 JP28.
- Use `tools/fft_save_patch_delita.py <autoenhanced.png> --in-place`; it creates a backup first.
```

## New Game++ Design Goal

Keep the battle's identity:

```text
Academy cadets vs. local thieves in a city street.
```

Increase difficulty by adding:

```text
One ranged threat
One more deliberate frontline shape
One support unit that keeps enemies alive
Light role variety without advanced jobs
```

Avoid for this battle:

```text
Black Mage burst damage
Time Mage control
Knight equipment breaking
Monk burst damage
Heavy status effects
Multiple archers on high ground
Boss-tier level offsets
```

## Implemented Version: Final-Shop v1

The first harder variant worked, but the enemy equipment was too weak for a New Game+
endgame-style battle. This version keeps the 6-enemy composition, but upgrades the group to
late-shop/endgame purchasable equipment and explicit reaction/support/movement skills.

The design rule is:

```text
Use strong final-shop gear, not unique/steal-only superboss gear.
```

So this version avoids items like Genji gear, Chaos Blade, Excalibur, Ragnarok, Save the
Queen, and other unique treasure/steal rewards. It uses equipment that appears in shops or
in the mod loader's shop table.

| Slot | New role | Job | Level | Purpose |
|------|----------|-----|-------|---------|
| 1 | Leader | Squire | `102` | High-damage veteran; central pressure. |
| 2 | Bruiser | Squire | `100` | Physical striker with PA gear. |
| 3 | Bodyguard | Squire | `100` | Durable/evasive frontliner. |
| 4 | Support | Chemist | `100` | Gun user, healing/revive pressure. |
| 5 | Ranged | Archer | `101` | Reliable ranged threat. |
| 6 | Skirmisher | Thief | `101` | Fast backline pressure and disruption. |

Reasoning:

This keeps the original 4 Squire + 1 Chemist spirit, but replaces one Squire with an Archer
so the map matters more, then adds a Thief as the extra pressure point. The leader is `102`,
not `103+`, because this is still the first real battle of Chapter 1.

## Final-Shop v1 Builds

Item IDs come from:

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
```

Skill IDs come from:

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Slot 1 - Squire Leader

```text
Job: Squire (74)
Level: 102
JobLevel: 8
Secondary: none
Reaction: Counter (442)
Support: Attack Boost (465)
Movement: Movement +2 (487)

Head: Thief's Cap (168)
Body: Black Garb (198)
Accessory: Bracers (218)
Right hand: Runeblade (30)
Left hand: none (255)
```

Role:

```text
Main melee danger. Fast, hard-hitting, but still a Squire.
```

### Slot 2 - Squire Bruiser

```text
Job: Squire (74)
Level: 100
JobLevel: 8
Secondary: none
Reaction: Counter (442)
Support: Attack Boost (465)
Movement: Movement +1 (486)

Head: Headband (163)
Body: Power Garb (195)
Accessory: Bracers (218)
Right hand: Icebrand (29)
Left hand: none (255)
```

Role:

```text
Pure physical pressure. Uses PA-focused gear instead of maximum HP/evasion.
```

### Slot 3 - Squire Bodyguard

```text
Job: Squire (74)
Level: 100
JobLevel: 8
Secondary: none
Reaction: Counter (442)
Support: Attack Boost (465)
Movement: Movement +1 (486)

Head: Thief's Cap (168)
Body: Black Garb (198)
Accessory: Featherweave Cloak (234)
Right hand: Runeblade (30)
Left hand: none (255)
```

Role:

```text
Tougher frontliner; protects the Chemist/Archer lane.
```

### Slot 4 - Chemist Support

```text
Job: Chemist (75)
Level: 100
JobLevel: 8
Secondary: Fundaments (5)
Reaction: Auto-Potion (441)
Support: Throw Items (474)
Movement: Movement +1 (486)

Head: Thief's Cap (168)
Body: Black Garb (198)
Accessory: Featherweave Cloak (234)
Right hand: Mythril Gun (72)
Left hand: none/two-hand marker (254)
```

Role:

```text
Backline stabilizer. Mythril Gun makes it relevant even when not healing.
```

### Slot 5 - Archer

```text
Job: Archer (77)
Level: 101
JobLevel: 8
Secondary: Fundaments (5)
Reaction: Reflexes (449)
Support: Concentration (469)
Movement: Movement +1 (486)

Head: Thief's Cap (168)
Body: Black Garb (198)
Accessory: Bracers (218)
Right hand: Windslash Bow (87)
Left hand: none/two-hand marker (254)
```

Role:

```text
Reliable ranged pressure. Concentration makes the Archer matter against evasive NG+ units.
```

### Slot 6 - Thief Skirmisher

```text
Job: Thief (83)
Level: 101
JobLevel: 8
Secondary: Fundaments (5)
Reaction: First Strike (453)
Support: Attack Boost (465)
Movement: Movement +2 (487)

Head: Thief's Cap (168)
Body: Black Garb (198)
Accessory: Germinas Boots (210)
Right hand: Air Knife (9)
Left hand: none/two-hand marker (254)
```

Role:

```text
Fast flanker. Pressures weak units and forces the player to protect the backline.
```

## Implementation Notes

```text
Slot 5 Squire -> Archer, MainJob 74 -> 77
Slot 6 empty -> Thief, MainJob 83
All active enemy slots now have JobLevel 8
All active enemy slots now have explicit reaction/support/movement skills
Slot 6 was cloned from slot 5's human template, then changed to male generic Thief
Slot 6 position bytes set to X=4, Y=2
Slot 6 unit/slot id byte set to 0x85
```

Patch output:

```text
work\battle_entd4_ent.gariland-finalshop-v1.bin
mod\fftivc.battles.rescale\FFTIVC\data\enhanced\fftpack\battle_entd4_ent.bin
work\entd_388_gariland_finalshop_v1.csv
```

Diff summary:

```text
74 bytes changed, all inside Gariland entry 388.
No bytes changed outside the local Gariland window.
```

## Skill Plan

Squire leader:

```text
Primary: Basic Skill
Secondary: Item if easy to encode safely, otherwise none
Reaction: none/random default
Support: none/random default
Movement: none/random default
Notes: Should feel like the most confident thief, not a boss.
```

Squire frontliners:

```text
Primary: Basic Skill
Secondary: none or Item on only one unit
Reaction: none/random default
Support: none/random default
Movement: none/random default
Notes: Keep them simple. Their danger comes from scaling and formation.
```

Chemist:

```text
Primary: Item
Secondary: none
Reaction: avoid Auto-Potion for first implementation
Support: avoid Throw Item for first implementation unless range is too weak
Movement: none/random default
Notes: Potion/Phoenix Down pressure is enough for Battle 2.
```

Archer:

```text
Primary: Aim/Charge
Secondary: none or Basic Skill
Reaction: none/random default
Support: none/random default
Movement: none/random default
Notes: One Archer is enough. The goal is positional pressure, not a firing squad.
```

Thief, optional later:

```text
Primary: Steal
Secondary: Basic Skill
Reaction: none/random default
Support: none/random default
Movement: none/random default
Notes: Avoid Steal Heart in the first pass; charm this early may feel cheap.
```

## Equipment Notes

The earlier low-gear version has been superseded. Exact item IDs are now mapped through the
mod loader's `ItemData.xml`, and the implemented equipment is listed in the Final-Shop v1
builds above.

Important compatibility note:

```text
Generic enemy Squire (job 74) does not equip shields or heavy armor.
```

Therefore the Squires use sword + hat + clothing + accessory, not Crystal Shield/Crystal
Mail. This keeps the fight coherent with the actual job equipment rules.

## Positioning Plan

Keep the encounter readable:

```text
Squire leader starts near the central/front pressure lane.
Two Squires start split enough to threaten both Ramza and Delita paths.
Chemist starts behind the frontliners, reachable but not exposed on turn 1.
Archer starts on or near elevation, but not so high/far that melee cannot contest.
```

The Archer should force the player to respect rooftops without making the first fight a
slow chase.

## Implementation Checklist

- Verify Archer job ID in-game. Done in harder v1.
- Verify Thief job ID in-game. Done in harder v1.
- Map final-shop item IDs. Done.
- Map relevant command/ability IDs. Done.
- Patch slot levels:
  - Slot 1: `102`
  - Slots 2-4: `100`
  - Slot 5: `101`
  - Slot 6: `101`
- Set active enemy JobLevel to `8`. Done.
- Change slot 5 from Squire to Archer. Done.
- Add slot 6 as Thief. Done.
- Upgrade all active enemy equipment to final-shop v1. Done.
- Add explicit reaction/support/movement skills. Done.
- Keep slot 4 as Chemist.
- Slot 0 Delita: keep level `100`; for Squire Job Level testing, keep `0x08=1` and set `0x09=8`.
- Set Delita's pre-Gariland join record (`entry 392`, slot `1`) to `0x08=1`, `0x09=8`.
  Needs in-game confirmation from a save before Delita joins.
- Upgrade Gariland spoils from vanilla to Air Knife + Phoenix Down + X-Potion. Done.
- Re-dump entry `388` after patch. Done.
- Compare binary diff; expected changes should be small and intentional. Done.
- Install updated `New Game++` mod into `C:\Reloaded-II\Mods`. Done.
- Test in-game from a New Game+ file.

## Test Questions

- Do enemies scale correctly with slots 1/5/6 above party level?
- Does the Archer's Windslash Bow + Concentration dominate too much?
- Does the Chemist's Mythril Gun + Auto-Potion + Throw Items prolong the battle too much?
- Do the Squires hit too hard with Bracers/Attack Boost?
- Does First Strike on the Thief feel fair?
- Does Delita still make the fight too easy?
- Is the first battle challenging but still fast?
- Does the battle still feel like Gariland?

## Sources

- Game8, "Magick City of Gariland Walkthrough (Battle 2)": confirms Chapter 1 Battle 2,
  recommended level 1, objective, party size, original enemies, and rewards.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553163
- StrategyWiki, "Final Fantasy Tactics/Gariland Magic City": confirms practical original
  battle behavior, enemy Chemist healing loop, early-party expectations, and post-battle shop
  context.
  https://strategywiki.org/wiki/Final_Fantasy_Tactics/Gariland_Magic_City
- GameFAQs, SMaxson's Shop Guide: confirms shop availability timing. Key point for this
  design: all equipment/items are available after story battle 39 except Thief Hat/Thief's
  Cap after battle 44; lists final shop equipment such as Rune Blade, Crystal Shield,
  Crystal Mail, Black Costume/Black Garb, Light Robe/Luminous Robe, Thief Hat/Thief's Cap,
  and Bracer/Bracers.
  https://gamefaqs.gamespot.com/ps/197339-final-fantasy-tactics/faqs/30462
- Local data:
  - `extracted\enhanced_0002_selected\fftpack\battle_entd4_ent.bin`
  - `work\enhanced_0004.sqlite`
  - `work\entd_388_gariland_candidate.csv`
  - `work\entd_388_gariland_finalshop_v1.csv`
  - `C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml`
  - `C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml`
  - `C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobData.xml`
