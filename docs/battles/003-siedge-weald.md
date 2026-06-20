# 003 - Siedge Weald (Sweegy Woods)

Status: designed (not yet implemented)
Chapter: 1
Battle order: Battle 4 (after Mandalia Plain)
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
Up to 4 units, including Ramza.
Guests: Delita and Argath travel with the party (best minimized so the core party fights).
```

Original enemy composition (all monsters — no humans):

```text
1x Red Panther
2x Goblin
2x Black Goblin
2x Bomb
```

Public walkthrough details:

```text
Recommended level: ~2
Dense woodland map: trees, brush, and uneven elevation that break up movement and sightlines.
Goblins are weak to Ice; Bombs are weak to Thunder.
The signature danger is Bomb Self-Destruct when a Bomb's HP gets low.
Otherwise the original is easy — it is a teaching fight about monsters and elements.
```

Design reading:

Siedge Weald is **the all-monster fight**. It is the first time the player faces a pack with
no human jobs at all, and it exists to teach three things: monster archetypes behave
differently from classes, **elements matter** (Ice on Goblins, Thunder on Bombs), and a
cornered Bomb will **Self-Destruct** for a huge hit. The woods themselves are the second
opponent — trees and elevation restrict movement, so the player cannot freely kite the swarm.

For New Game++ the identity is sacred: **a wild monster swarm ambushing the party in thick
woods, where the real danger is a scaled Self-Destruct and getting surrounded.** No humans,
no gear — the scaling itself, plus the terrain and the explosions, is the difficulty.

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm the 7 monster slots and which (if any) slots are guest/player.
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
Monsters use NO equipment slots; the levers are Level, JobLevel, Brave/Faith, and the
  monster's innate skill tier. Verify how the data encodes monster abilities before patching.
```

Job/monster IDs (verify all monster IDs in-game — none confirmed yet):

```text
Red Panther job id     (TBD - verify)
Goblin job id          (TBD - verify)
Black Goblin job id    (TBD - verify)
Bomb job id            (TBD - verify)
```

## New Game++ Design Goal

Keep the identity:

```text
An all-monster pack ambush in dense woods. Elements still matter; a low-HP Bomb still
threatens to erase a unit; the trees still deny easy escape.
```

Raise the challenge by:

```text
Scaling every monster to party level so HP pools are real and Self-Destruct actually hurts.
Keeping the full 7-monster pack so the party (4 + guests) is outnumbered in bad terrain.
Leaning into the Bombs as the headline threat: scaled Self-Destruct is the spike of this fight.
Preserving the elemental-weakness puzzle so a prepared player is rewarded for bringing magic.
```

Avoid for this battle (see overview rules):

```text
Adding any human job (it must stay a pure monster fight).
Adding a caster / a mage monster that introduces status control this early.
A third+ Bomb in v1 (the basic version keeps 2; see "Harder v2" note below).
Boss-tier level offsets — the swarm's danger is numbers + explosions, not a single elite.
```

## Proposed Composition (New Game++ Siedge Weald v1)

Keep the exact original roster of 7 monsters; only the levels change. The two tougher
families (Red Panther, Black Goblins) and the Bombs sit one point above the rabble Goblins.

| Slot | Monster | Level | Purpose |
|------|---------|-------|---------|
| n | Red Panther | `101` | Pack alpha; fast, poisons, picks off exposed units. |
| n | Goblin | `100` | Basic body; swarms the front. Ice-weak teaching target. |
| n | Goblin | `100` | Second body; flanks. |
| n | Black Goblin | `101` | Tougher goblin; the durable melee of the pack. |
| n | Black Goblin | `101` | Pairs with the first to pin the frontline. |
| n | Bomb | `101` | The headline threat. Scaled Self-Destruct can delete a unit. |
| n | Bomb | `101` | Second explosive; forces the player to split focus-fire. |

Reasoning:

The roster is already perfect for this fight's purpose, so the faithful move is to **scale,
not redesign**. Bombs and the tougher monsters at `101` make the pack bite without any unit
crossing into boss tier. The whole difficulty comes from three honest sources: real HP pools,
two scaled Bombs that punish slow/cornered play, and the woods restricting movement. A player
who brings Thunder for the Bombs and Ice for the Goblins is rewarded exactly as the original
intended — now it actually matters.

### Optional "Harder v2" (tune after playtest)

If v1 plays too soft once HP is scaled, the faithful escalation is **more explosions, not new
archetypes**:

```text
Promote one Goblin -> a third Bomb (3 Bombs total), OR
Bump both Bombs to level 102 so Self-Destruct is a true panic button.
```

Do not add humans or status-effect monsters — that would break the fight's identity.

## Monster Tuning Notes

```text
Set JobLevel 8 on all monsters so their innate skills/HP land at full tier for the level.
Brave: keep monster-typical high Brave (aggressive AI) so the pack presses, as in the original.
Self-Destruct scales off the Bomb's max HP — at party level this is the single biggest hit in
  the fight. Position Bombs so the player must choose between killing them fast (risking the
  blast radius) or zoning around them (losing tempo to the rest of the pack).
Red Panther keeps Poison on hit; at scale, poison chip + pack focus is what punishes a
  clumped party.
```

## Positioning Plan

```text
The pack starts spread across the far tree line, not bunched — so the player cannot AoE the
  whole swarm on turn 1 and must fight through the woods.
Bombs start slightly behind the goblin frontline: reachable, but the player has to commit
  into the trees to kill them before they Self-Destruct.
Red Panther starts on a flank with a clear movement lane, free to lunge at the backline.
Black Goblins anchor the center chokepoints between trees, forcing the party to funnel.
```

The woods plus a spread pack means the player can't kite freely and can't nuke at once —
exactly the original's lesson, now with stakes.

## Implementation Checklist

- [ ] Identify Siedge Weald `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify Red Panther x1 + Goblin x2 + Black Goblin x2 + Bomb x2.
- [ ] Confirm all four monster job IDs and how monster skills are encoded.
- [ ] Set levels: Goblins `100`; Red Panther / Black Goblins / Bombs `101`.
- [ ] Set JobLevel `8` on all monster slots; keep aggressive Brave.
- [ ] Do NOT touch equipment slots (monsters carry none).
- [ ] Patch via the correct layer; keep the diff inside the Siedge Weald window only.
- [ ] Re-dump and diff; confirm changes are small and intentional.
- [ ] Install mod, test from a New Game+ save; watch a scaled Self-Destruct land.

## Test Questions

- Does a scaled Bomb's Self-Destruct feel like a genuine panic moment (not an instant party wipe)?
- Is the pure-monster identity intact — does it still read as a wild ambush, not a designed squad?
- Do the woods meaningfully restrict the player, or can they trivially kite the whole pack?
- Is bringing Thunder/Ice rewarded the way the original taught, now that it actually matters?
- Outnumbered 7-vs-4(+guests), is the fight tense but winnable without grinding?
- Does v1 need the "Harder v2" extra Bomb, or is scaled HP + 2 Bombs already enough?

## Sources

- Game8, "Siedge Weald Walkthrough (Battle 4)": exact roster (Red Panther x1, Goblin x2,
  Black Goblin x2, Bomb x2), objective "Defeat all enemies!", deploy 4, recommended level ~2,
  Bomb Self-Destruct warning, Goblins weak to Ice / Bombs weak to Thunder.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553165
- Final Fantasy Wiki, "Siedge Weald": story context (Ramza/Delita/Argath en route to Dorter,
  monster pack barring the way).
  https://finalfantasy.fandom.com/wiki/Siedge_Weald
- StrategyWiki, "Final Fantasy Tactics/Sweegy Woods": original battle behavior, terrain.
  https://strategywiki.org/wiki/Final_Fantasy_Tactics/Sweegy_Woods
- Local: `docs/battles/000-chapter-1-overview.md` (design rules), `001-gariland.md`.
</content>
