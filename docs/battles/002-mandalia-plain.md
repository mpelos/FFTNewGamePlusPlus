# 002 - Mandalia Plain

Status: ✅ implemented (v1) — NG+ only, awaiting playtest
Chapter: 1
Battle order: Battle 3 (after Gariland)
Target version: Enhanced v1.5.0
ENTD: global entry **389**
File: `battle_entd4_ent.bin` (local entry `5`)
Patcher: `tools/battle_patch.py mandalia`

## Original Battle

Objective (player makes a story choice on entry):

```text
"Our duty is to destroy the Corpse Brigade" -> Defeat all enemies (+10 Brave to the party).
"We must help the man"                      -> Save Argath (he must survive).
```

Player deployment:

```text
Up to 5 units, including Ramza.
Guests: Delita and Argath both join as allied story units.
```

Original enemy composition:

```text
3x Squire (Corpse Brigade)
1x Thief
1x Red Panther (monster)
```

Public walkthrough details:

```text
Recommended level: ~2-3
Difficulty: low, but the first fight with a monster.
Open grassland map with gentle elevation and a few ramps.
Red Panther can inflict Poison; the Thief is the fastest human threat.
The Squires are weak filler; the danger is Argath's reckless AI running into the beast.
```

Design reading:

Mandalia is the game's **first monster fight and first soft escort**. It teaches three things:
monsters behave differently from human jobs (the Red Panther is fast and poisons), guests can
get themselves killed (Argath charges in), and the open field offers no walls to hide behind.

The original is trivially easy now, but its *identity* is "an open-plains skirmish against
Corpse Brigade rabble and a wild beast, while a reckless ally throws himself forward." New
Game++ must keep that — a fast, readable field fight with one real beast and genuine pressure
on the fragile guest line — without turning the on-ramp into a wall.

## Local Data Confirmed

Entry `389` identified by: 2 guests present (Delita 0x04 + Argath 0x07 — Mandalia is where
Argath joins; Gariland had only Delita), enemy composition Thief + 4 Squire + 1 monster at
real low levels, sitting immediately after Gariland (388). Vanilla dump:

| Slot | Role | charId | Level | MainJob | Notes |
|------|------|--------|-------|---------|-------|
| 0,1 | guests | 0x04 / 0x07 | — | — | Delita + Argath. Left untouched (runtime guest layer scales them). |
| 2 | enemy | 0x80 | `2` | `83` | Thief. |
| 3 | enemy | 0x80 | `1` | `74` | Squire. |
| 4 | enemy | 0x80 | `1` | `74` | Squire. |
| 5 | enemy | 0x80 | `1` | `74` | Squire. |
| 6 | enemy | 0x80 | `1` | `74` | Squire (→ converted to Archer). |
| 7 | enemy | 0x82 | `1` | `103` (monster) | Red Panther. |

Vanilla had **4** Squire (not 3 as some walkthroughs list); one becomes the Archer, leaving
3 Squire + Thief + Archer + Red Panther = the designed composition with no slot added.

Job IDs:

```text
74 = Squire           (confirmed)
83 = Thief            (confirmed)
77 = Archer           (confirmed)
103 = Red Panther     (confirmed — monster slot 7, flags 0x20, no equipment)
```

## New Game++ Design Goal

Keep the identity:

```text
Open-field clash with Corpse Brigade deserters and a plains beast, while a reckless
guest (Argath) charges the front. No walls, no roof — positioning is the whole puzzle.
```

Raise the challenge by:

```text
Keeping the monster (the beast is the soul of this fight) and giving it teeth at scale.
Adding ONE ranged threat so the open field punishes a clumped party and a charging guest.
Giving the Corpse Brigade humans coherent deserter gear instead of paper.
Leaving the player room to win fast if they position well.
```

Avoid for this battle (see overview rules):

```text
Any mage (no Black/Time Mage yet — Dorter introduces magic pressure).
Status spam beyond the monster's natural Poison.
A second monster that turns the escort into chaos.
Boss-tier level offsets.
```

## Proposed Composition (New Game++ Mandalia v1)

Six enemies: the original five re-tuned + one Archer for open-field pressure. Corpse Brigade
human core stays Squire/Thief; the beast stays a Red Panther.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Brigade leader | Squire | `102` | Front pressure; the most confident deserter. |
| n | Brigade soldier | Squire | `100` | Physical body; pushes toward the guests. |
| n | Brigade soldier | Squire | `100` | Second body; pincers from the flank. |
| n | Skirmisher | Thief | `101` | Fast flanker; harasses the backline / steals. |
| n | Marksman | Archer | `101` | Open-field ranged pressure; punishes clumping and the guest line. |
| n | Beast | Red Panther | `101` | Fast poison threat; the identity of the fight. Keep it. |

Reasoning:

This is the original 3 Squire + 1 Thief + 1 Red Panther, kept intact, plus a single Archer.
The Archer is the one new "meaningful threat" the budget allows: on an open plain with no
cover, a marksman makes the player respect spacing and forces them to actually shield Argath
instead of letting him solo the field. The leader at `102` and two skirmishers at `101` keep
the fight a touch above party level without crossing into boss territory.

## Builds (final-shop quality, deserter flavor)

Item/skill IDs come from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

Gear flavor rule for Mandalia: **worn military / leather, not academy polish.** Corpse Brigade
are army deserters — leather, hats, knives, swords, a bow — at final-shop power, but grittier
than Gariland's cadets. Reuse Gariland's confirmed item IDs where they fit; new picks marked
TBD until checked against `ItemData.xml`.

### Brigade Leader - Squire (Lv 102)

```text
Job: Squire (74)   JobLevel: 8   Secondary: none
Reaction: Counter (442)
Support: Attack Boost (465)
Movement: Movement +1 (486)

Head: Headband (163)        - PA flavor, fits a brawler deserter
Body: Power Garb (195)      - PA body, leather feel
Accessory: Bracers (218)
Right hand: Icebrand (29)    or Runeblade (30)
Left hand: none (255)
```

Role: the deserter who thinks he's still a soldier. Main melee danger, but still a Squire.

### Brigade Soldier x2 - Squire (Lv 100)

```text
Job: Squire (74)   JobLevel: 8   Secondary: none
Reaction: Counter (442)
Support: Attack Boost (465)
Movement: Movement +1 (486)

Head: Headband (163)
Body: Power Garb (195)
Accessory: Bracers (218)
Right hand: Icebrand (29)
Left hand: none (255)
```

Role: bodies that push the line toward Ramza and the guests. Identical pair, simple by design.

### Skirmisher - Thief (Lv 101)

```text
Job: Thief (83)   JobLevel: 8   Secondary: Steal (or none for v1)
Reaction: First Strike (453)
Support: Attack Boost (465)
Movement: Movement +2 (487)

Head: Thief's Cap (168)
Body: Black Garb (198)
Accessory: Germinas Boots (210)
Right hand: Air Knife (9)
Left hand: none / two-hand marker (254)
```

Role: fast flanker. Pressures the backline and the guests; Movement +2 makes the open field
small. Keep Steal mild (no Steal Heart this early — see overview).

### Marksman - Archer (Lv 101)

```text
Job: Archer (77)   JobLevel: 8   Secondary: none (or Fundaments 5)
Reaction: Reflexes (449)
Support: Concentration (469)
Movement: Movement +1 (486)

Head: Thief's Cap (168)
Body: Black Garb (198)
Accessory: Bracers (218)
Right hand: Windslash Bow (87)
Left hand: none / two-hand marker (254)
```

Role: the new open-field threat. Concentration makes the Archer matter against evasive NG+
units. Should pressure the guest line from range, not delete the party — one bow only.

### Beast - Red Panther (Lv 101)

```text
Job: Red Panther (monster, id TBD)   JobLevel: 8
Equipment: none (monster)
Reaction / Support / Movement: monster defaults (verify the slot encodes legal monster skills)
```

Role: the soul of the fight. Fast, poisons on hit, beelines for whoever is exposed — usually
the charging guest. Keep it a single Red Panther; do not add a second monster.

## Positioning Plan

```text
Brigade leader + one Squire start center, on or near the gentle rise, facing the player's
  deployment so they contest the middle immediately.
Second Squire starts on a flank to pincer toward Argath's charge lane.
Thief starts wide, positioned to loop around to the backline within 1-2 turns.
Archer starts on the highest available tile (a rise/ramp), with line of sight over the field
  but reachable — not an unassailable perch (Mandalia has only gentle elevation, keep it fair).
Red Panther starts forward and central, free to lunge at the most exposed unit.
```

The point: the open plain plus one archer plus a charging beast should force the player to
actually escort Argath, not ignore him. No tile should be a safe corner.

## Implemented Mapping (v1)

Applied to the embedded NG+ ENTD (`tools/battle_patch.py mandalia`), entry 389. 52 bytes
changed, all inside entry 389. Existing slots re-tuned in place (no slot added — Mandalia
already had 6 enemy slots), so positions are kept vanilla.

| Slot | Role | Job | Level | R / S / M | Gear (head/body/acc/RH/LH) |
|------|------|-----|-------|-----------|----------------------------|
| 3 | Leader | Squire (74) | 102 | Counter / Attack Boost / Move +1 | Headband / Power Garb / Bracers / Runeblade / — |
| 4 | Soldier | Squire (74) | 100 | Counter / Attack Boost / Move +1 | Headband / Power Garb / Bracers / Icebrand / — |
| 5 | Soldier | Squire (74) | 100 | Counter / Attack Boost / Move +1 | Headband / Power Garb / Bracers / Icebrand / — |
| 2 | Skirmisher | Thief (83) | 101 | First Strike / Attack Boost / Move +2 | Thief's Cap / Black Garb / Germinas Boots / Air Knife / 2h |
| 6 | Marksman | Archer (77) | 101 | Reflexes / Concentration / Move +1 | Thief's Cap / Black Garb / Bracers / Windslash Bow / 2h |
| 7 | Beast | Red Panther (103) | 101 | monster defaults (untouched) | none (monster) |

Notes / known risks:
- Job conversion (s6 Squire→Archer) changed only `mainJob` (0x0A); `x08` left as vanilla
  (it varies independently of job and is duplicated across slots, so it is not job/sprite/id
  critical). If the Archer renders or behaves wrong in-game, set `x08`=3 as Gariland did.
- Thief secondary left as none (v1, per design). Archer secondary = Fundaments (matches the
  verified Gariland archer).
- Positions kept vanilla; the open-field placement plan above is a future-tuning option.

## Implementation Checklist

- [x] Identify Mandalia ENTD entry → **389** (local 5, `battle_entd4_ent.bin`).
- [x] Dump original entry; verified Thief + 4 Squire + Red Panther + 2 guests.
- [x] Confirm Red Panther job id → **103** (monster, no equipment).
- [x] Verify Archer/Thief/Squire item IDs (reused Gariland's in-game-validated IDs).
- [x] Set levels: leader `102`, Squires `100`, Thief/Archer/Panther `101`.
- [x] Set JobLevel `8` on all active enemy slots.
- [x] Convert one Squire (s6) → Archer in place (no slot added; 6 already present).
- [x] Apply gear + R/S/M per builds above.
- [ ] Positions: kept vanilla (placement plan deferred to a tuning pass).
- [x] Patch via the NG+ embedded ENTD; diff confirmed inside entry 389 only (52 bytes).
- [x] Rebuild + deploy mod.
- [ ] Test in-game from a New Game+ save with both objective choices.

## Test Questions

- Does the Red Panther still feel like the standout threat, or did the Archer overshadow it?
- With "Save Argath" chosen, is protecting him tense but achievable (not a guaranteed loss)?
- Does the open field punish clumping the way Dorter's roofs will later — but more gently?
- Is one Archer the right amount of ranged pressure, or does it stall the fight into a chase?
- Does the fight still resolve quickly if the player positions well? (It should.)
- Does it still read as "Corpse Brigade rabble + a beast on the plains," not a designed squad?

## Sources

- Game8, "Mandalia Plain Walkthrough (Battle 3)": objective choice (+10 Brave), guests
  Delita + Argath, enemies Thief / Squire x3 / Red Panther, Red Panther poison threat.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553164
- StrategyWiki, "Final Fantasy Tactics/Mandalia Plains": original battle behavior, escort
  pressure, recommend-a-Chemist-in-throw-range tip.
  https://strategywiki.org/wiki/Final_Fantasy_Tactics/Mandalia_Plains
- Caves of Narshe FFT walkthrough (battle 3): roster cross-check.
  https://www.cavesofnarshe.com/fft/walkthrough.php?battle=3
- Local: `docs/battles/001-gariland.md` (confirmed item/skill IDs, slot-add method),
  `docs/battles/000-chapter-1-overview.md` (design rules).
</content>
