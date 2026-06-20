# 002 - Mandalia Plain

Status: designed (not yet implemented)
Chapter: 1
Battle order: Battle 3 (after Gariland)
Target version: Enhanced v1.5.0
ENTD: global entry **TBD** — confirm on Windows game data
File: `battle_entd*_ent.bin` (TBD) / `OverrideEntryData` rows (TBD)

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `000-chapter-1-overview.md`.

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

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm: which slots are the 3 Squires / Thief / Red Panther, and which are guest/player.
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
```

Job IDs (carry over known, verify the rest in-game):

```text
74 = Squire           (confirmed)
83 = Thief            (confirmed)
77 = Archer           (confirmed)
Red Panther job id    (TBD — verify; monster slot, no equipment)
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

## Implementation Checklist

- [ ] Identify Mandalia `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify 3 Squire + 1 Thief + 1 Red Panther + guest/player slots.
- [ ] Confirm Red Panther job id and a legal monster build.
- [ ] Verify Archer/Thief/Squire item IDs against `ItemData.xml`.
- [ ] Set levels: leader `102`, Squires `100`, Thief/Archer/Panther `101`.
- [ ] Set JobLevel `8` on all active enemy slots.
- [ ] Add the Archer slot (clone a human template like Gariland's slot-6 method, then re-job).
- [ ] Apply gear + R/S/M per builds above.
- [ ] Set positions per the placement plan.
- [ ] Patch via the correct layer; keep the diff inside the Mandalia window only.
- [ ] Re-dump and diff; confirm changes are small and intentional.
- [ ] Install mod, test from a New Game+ save with both objective choices.

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
