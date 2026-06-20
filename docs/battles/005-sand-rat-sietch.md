# 005 - Sand Rat Sietch (Sand Rat Cellar)

Status: designed (not yet implemented)
Chapter: 1
Battle order: Battle 6 (after Dorter Slums)
Target version: Enhanced v1.5.0
ENTD: global entry **TBD** — confirm on Windows game data
File: `battle_entd*_ent.bin` (TBD) / `OverrideEntryData` rows (TBD)

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `000-chapter-1-overview.md`.

## Original Battle

Objective:

```text
Defeat all enemies!
```

Player deployment:

```text
Up to 4 units, including Ramza — but split into TWO teams that start at opposite entrances.
Guests: Delita and Argath, one assigned to each split team.
```

Original enemy composition:

```text
3x Knight
1x Archer
2x Monk
```

Public walkthrough details:

```text
Recommended level: ~4
Indoor cellar/sietch: cramped rooms and corridors with a left-entrance chokepoint where
  most enemies funnel through. The interior naturally channels units into passages.
The fight is melee-heavy: tanky Knights anchor, Monks hit hard (high PA, Chakra self-heal,
  ranged Earth Slash / Wave Fist), one Archer pokes from range.
Standard read: hold the left chokepoint with a Knight + Chemist, circle the right with
  Ramza + a Black Mage to AoE the clustered enemies.
```

Design reading:

Sand Rat is **the meat grinder and the split-force puzzle**. It is the first fight where the
player's own deployment is divided — you defend two doorways at once with half a team (plus a
guest) on each side. The enemy is deliberately melee-dense: three durable Knights and two
high-damage Monks, fronted through narrow corridors, with a lone Archer for ranged poke. Where
Dorter tested verticality and ranged/magic, Sand Rat tests **chokepoint discipline and
attrition** while you're stretched thin.

For New Game++ the identity must stay: **a cramped indoor holding action against a tanky,
hard-hitting melee squad, with your force split between two entrances.** It should feel like
grinding through a fortified cellar — distinct from Dorter's rooftop gauntlet.

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm the 6 enemy slots: 3 Knight / 1 Archer / 2 Monk, plus the split player/guest slots.
Confirm the two player deployment zones (left + right entrances) are preserved.
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
```

Job IDs (carry over known, verify the rest in-game):

```text
77 = Archer            (confirmed)
Knight job id          (TBD - verify; shares with Dorter's Knight)
Monk job id            (TBD - verify)
```

## New Game++ Design Goal

Keep the identity:

```text
An indoor attrition fight at two chokepoints with a split party. Tanky Knights stall the
doors; Monks bring the burst and self-sustain; an Archer pokes. The corridors are the puzzle.
```

Raise the challenge by:

```text
Scaling the melee squad so the Knights are real time-sinks and the Monks' PA actually threatens.
Keeping Monk self-sustain (Chakra) and ranged Earth Slash so a holding player can't just turtle.
Giving the Knights coherent shop heavy gear so the chokepoints genuinely hold.
Preserving the split-team start so the player must win two holds at once, not one.
```

Avoid for this battle (see overview rules):

```text
Knight equipment-break skillsets (breaking endgame gear is unfun — keep them as anchors).
Any mage on the enemy side — Sand Rat is a MELEE fight; magic pressure belongs to Dorter.
Time Mage control / heavy status — attrition is the theme, not lockdown.
Boss-tier offsets (a Knight captain may hit +2, no further).
```

## Proposed Composition (New Game++ Sand Rat v1)

Keep the exact original 3/1/2 shape; scale and gear it. One Knight reads as the captain at
`102`; the Monks sit at `101` for burst; the Archer pokes at `100`.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Knight captain | Knight | `102` | Anchors the main (left) chokepoint; the hardest single unit to remove. |
| n | Knight | Knight | `101` | Holds the second doorway; splits the player's focus. |
| n | Knight | Knight | `100` | Roving body; reinforces whichever door is breaking. |
| n | Monk | Monk | `101` | Burst + Chakra self-heal; punishes a stalled hold. |
| n | Monk | Monk | `101` | Second Monk; Earth Slash / Wave Fist reaches over the frontline. |
| n | Archer | Archer | `100` | Ranged poke down a corridor; chips whoever holds the door. |

Reasoning:

The roster is already the perfect "fortified cellar squad," so the faithful move is to **scale
and equip**, not redesign. Three Knights mean both chokepoints are genuinely defended and the
player can't collapse one door for free; the captain at `102` is the immovable object at the
main entrance. Two Monks supply the burst and the Chakra sustain that stop a turtling player
from winning by attrition alone — they must push. The Archer keeps the lone ranged identity
the original had. With the party split, answering all of this at two doors at once is the
challenge, exactly as designed.

## Builds (final-shop quality, fortified-Brigade flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

Gear flavor for Sand Rat: a dug-in Corpse Brigade holdout — Knights in real shop heavy gear
(shield + mail), Monks bare-handed with PA/HP clothing, the Archer with a strong bow. All
non-unique / shop-tier.

### Knight Captain (Lv 102) + 2 Knights (Lv 101 / 100)

```text
Job: Knight (id TBD)   JobLevel: 8   Secondary: none (NO Break skillset — see avoid list)
Reaction: Counter (442)
Support: Attack Boost (465)
Movement: Movement +1 (486)

Head: shop heavy helm (e.g. Crystal Helm-tier, id TBD)
Body: shop heavy armor (e.g. Crystal Mail-tier, id TBD)   - Knights CAN wear heavy armor
Accessory: Bracers (218)
Right hand: Runeblade (30) or Icebrand (29)
Left hand: shop shield (e.g. Crystal Shield-tier, id TBD) - high block; anchors the door
```

Role: the chokepoint walls. Shield + heavy armor make each door a real time-sink; the captain
is the centerpiece of the main entrance.

### Monk x2 (Lv 101)

```text
Job: Monk (id TBD)   JobLevel: 8   Secondary: none (innate Martial Arts command)
Reaction: Counter (442)        (Monks punishing melee fits the bruiser identity)
Support: Attack Boost (465)
Movement: Movement +1 (486)

Head: Headband (163)          - PA boost, fits the bare-handed bruiser
Body: Power Garb (195) or Earth Clothes-tier (id TBD)  - Monks wear clothing, NOT heavy armor
Accessory: Bracers (218)
Right hand: none (bare-handed — Martial Arts; do NOT equip a weapon)
Left hand: none (255)
```

Role: the burst and the sustain. Chakra keeps them in the fight; Earth Slash / Wave Fist reach
over the Knights to hit a holding party. They are the reason the player can't just turtle.

### Archer (Lv 100)

```text
Job: Archer (77)   JobLevel: 8   Secondary: none
Reaction: Reflexes (449)
Support: Concentration (469)
Movement: Movement +1 (486)

Head: Thief's Cap (168)
Body: Black Garb (198)
Accessory: Bracers (218)
Right hand: Windslash Bow (87)
Left hand: none / two-hand marker (254)
```

Role: corridor poke. Sits behind the melee line and chips whoever holds the door — a little
extra pressure that keeps the holds honest.

## Positioning Plan

```text
Knight Captain starts at the main (left) chokepoint, blocking the primary corridor.
Second Knight holds the right doorway so BOTH player teams face a wall on turn 1.
Third Knight starts central/deep, free to reinforce whichever door the player breaks first.
Both Monks start just behind the Knights — close enough to Earth Slash / Wave Fist over them,
  and to rush a door the moment its Knight falls.
Archer starts deep down a corridor with a long sightline to one of the entrances.
```

Preserve the two player deployment zones. The fight should force the player to win two holds
at once, never letting them mass their whole force at a single door.

## Implementation Checklist

- [ ] Identify Sand Rat `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify 3 Knight + 1 Archer + 2 Monk + the split player/guest slots.
- [ ] Confirm Knight and Monk job IDs and their legal equipment (Monks: no weapon, clothing only).
- [ ] Map shop-tier heavy armor / shield / PA-clothing item IDs in `ItemData.xml`.
- [ ] Set levels: captain `102`; 2nd Knight + both Monks `101`; 3rd Knight + Archer `100`.
- [ ] Set JobLevel `8` on all active enemy slots.
- [ ] Equip per builds; ensure Knights have NO Break skillset and Monks carry NO weapon.
- [ ] Preserve the two enemy-facing chokepoint positions; keep both player zones intact.
- [ ] Patch via the correct layer; keep the diff inside the Sand Rat window only.
- [ ] Re-dump and diff; confirm changes are small and intentional.
- [ ] Install mod, test from a New Game+ save; verify both holds are genuinely contested.

## Test Questions

- Does the split-team start still create two simultaneous holds, or can the player merge and steamroll?
- Are the Knights real time-sinks at the doors without being unkillable?
- Do the Monks' Chakra + Earth Slash stop a pure turtle, forcing the player to push?
- Does it feel like melee attrition in a cellar — clearly different from Dorter's rooftop fight?
- Is it a notch below Dorter and Ziekden in difficulty (attrition, not spike), per the curve?
- Does it still read as a dug-in Corpse Brigade holdout, not a designed arena?

## Sources

- Game8, "Sand Rat Sietch Walkthrough (Battle 6)": roster (3 Knight, 1 Archer, 2 Monk),
  objective "Defeat all enemies!", deploy 4 split into two teams, recommended level ~4,
  left-entrance chokepoint, guests Argath + Delita one per team, hold-and-circle strategy.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553167
- StrategyWiki, "Final Fantasy Tactics/Sand Rat Cellar": indoor chokepoint terrain and the
  split-deployment holding action.
  https://strategywiki.org/wiki/Final_Fantasy_Tactics
- Local: `docs/battles/000-chapter-1-overview.md` (design rules), `004-dorter-slums.md`
  (Knight anchor build), `001-gariland.md` (confirmed item/skill IDs).
</content>
