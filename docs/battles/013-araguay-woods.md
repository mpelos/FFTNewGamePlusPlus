# 013 - Araguay Woods

Status: designed (not yet implemented)
Chapter: 2 — "The Manipulator and the Subservient"
Battle order: Battle 12 (after Merchant City of Dorter)
Target version: Enhanced v1.5.0
ENTD: global entry **TBD** — confirm on Windows game data
File: `battle_entd*_ent.bin` (TBD) / `OverrideEntryData` rows (TBD)

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `011-chapter-2-overview.md`.

## Original Battle

Objective:

```text
Defeat all enemies!  — OR —  Save Chocobo!
(The player chooses: simply clear the pack, or rescue the wounded Chocobo, Boco.)
```

Player deployment:

```text
Up to 4 units, including Ramza.
Rescuable unit: Boco (a wounded Chocobo). If you choose to rescue it, it joins as an ally for
  the fight and its death is a GAME OVER. Protecting it through the battle recruits it after.
```

Original enemy composition (all monsters):

```text
5x Goblin
1x Black Goblin
```

Public walkthrough details:

```text
Recommended level: ~11.
Woods terrain: trees and brush restrict movement and break up sightlines.
Goblins are weak to Ice (an Ice Bow / ice magic is the recommended answer).
If rescuing Boco, the fight becomes an escort: the pack beelines for the wounded Chocobo and
  the player must intercept. Losing Boco ends the run.
```

Design reading:

Araguay is a **monster-pack woodland fight wrapped around an escort**. On its surface it echoes
Siedge Weald (a goblin swarm in the trees, weak to Ice), but the soul of *this* fight is the
choice to save **Boco**: the moment the player opts in, a light battle becomes a tense protect
mission where one mistake is a Game Over. It teaches escort positioning under a swarm in
movement-restricting terrain — and rewards a prepared, ice-equipped party.

For New Game++ the identity must stay: **a goblin swarm in the woods that the player fights
while shielding a fragile, mandatory-survival ally — Ice rewards preparation, the trees deny
easy kiting, and Boco's safety is the real objective.**

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm slots: 5 Goblin + 1 Black Goblin, plus the player slots and BOCO's ally slot.
DO NOT touch Boco's slot or the rescue/Game-Over scripting — only the enemy pack is edited.
Monsters use NO equipment; levers are Level, JobLevel, Brave/Faith, innate skill tier.
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
```

Job/monster IDs (verify all in-game):

```text
Goblin job id          (TBD - verify; shares with Siedge Weald)
Black Goblin job id    (TBD - verify; shares with Siedge Weald)
Red Panther job id     (TBD - verify; added below; shares with Mandalia)
```

## Job Escalation (Chapter 2 rule)

```text
CHANGE: add ONE Red Panther to the pack (a fast, poison-on-hit beast).
WHY: the original 5+1 goblin pack is slow and easy to wall off; a Red Panther can LUNGE at
  Boco from range, which directly raises the escort stakes — the single new wrinkle. It keeps
  the all-monster woodland identity (it's still a wild pack, no humans) while making "protect
  the Chocobo" genuinely tense at NG+ scale.
WHAT IS NOT CHANGED: the goblin core and the Ice-weakness lesson stay intact; the strategy is
  still "shield Boco, fight the swarm, exploit Ice."
```

## Boss rare loot

```text
None. Not a boss battle — no rare item (per the Chapter 2 overview). Monsters carry no gear.
```

## Proposed Composition (New Game++ Araguay v1)

Keep the original goblin pack and add one Red Panther (7 monsters). Goblins at `100`, the
Black Goblin and Red Panther at `101`.

| Slot | Monster | Level | Purpose |
|------|---------|-------|---------|
| n | Goblin | `100` | Basic swarm body; Ice-weak teaching target. |
| n | Goblin | `100` | Swarm body; pressures the front. |
| n | Goblin | `100` | Swarm body; flanks toward Boco. |
| n | Goblin | `100` | Swarm body; second flank. |
| n | Goblin | `100` | Swarm body; numbers pressure. |
| n | Black Goblin | `101` | Tougher goblin; the durable melee of the pack. |
| n | Red Panther (NEW) | `101` | Fast poison beast; can lunge at Boco — the escort threat. |

Reasoning:

The faithful move for a monster fight is to **scale, not redesign** — so the five Goblins and
the Black Goblin keep their roles and their Ice weakness. The one escalation is the Red Panther:
its speed turns "wall off the slow goblins" into "and also stop the thing that's sprinting at
your Chocobo." That single addition makes the rescue objective bite at party level without
breaking the wild-woods identity. If the player declines the rescue, it's simply a slightly
tougher swarm; if they accept, the Panther is the unit they must respect first.

## Monster Tuning Notes

```text
Set JobLevel 8 on all monsters; keep monster-typical high Brave (aggressive, presses the escort).
Goblins keep Ice weakness — a prepared, ice-equipped party is rewarded exactly as the original.
Red Panther keeps Poison on hit + high Move/Jump; position it with a clear lane toward Boco's
  start so it threatens the escort from turn 1.
Keep the pack SPREAD across the tree line so the player cannot AoE it all at once and must
  fight through the woods while covering Boco.
```

## Positioning Plan

```text
The goblin pack starts spread across the far side of the woods, between the player and the
  natural approach, so they funnel through the trees toward Boco.
The Black Goblin anchors a central chokepoint between trees.
The Red Panther starts on a flank with an open movement lane toward Boco — the first threat the
  player must intercept if they chose the rescue.
Preserve Boco's start position and the player deployment zone; do NOT alter the escort scripting.
```

If the player rescues Boco, every approach lane should feel like a race to intercept; if not,
it's a manageable swarm. The woods plus a spread pack keep the player from trivially kiting.

## Implementation Checklist

- [ ] Identify Araguay `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify 5 Goblin + 1 Black Goblin + player + Boco slots.
- [ ] Confirm Goblin / Black Goblin / Red Panther monster job IDs.
- [ ] Add the Red Panther slot (clone a monster template, then re-type); do NOT touch Boco.
- [ ] Set levels: Goblins `100`; Black Goblin + Red Panther `101`.
- [ ] Set JobLevel `8` and aggressive Brave on all monsters; no equipment.
- [ ] Keep the pack spread; give the Red Panther a lane toward Boco.
- [ ] Patch via the correct layer; keep the diff inside the Araguay window only.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify Boco scripting intact.
- [ ] Install mod, test BOTH objective choices (clear vs rescue) from a New Game+ save.

## Test Questions

- With the rescue chosen, does the Red Panther make protecting Boco genuinely tense (not an
  instant Game Over, but a real threat to intercept)?
- Without the rescue, is it a fair, slightly-tougher swarm — not trivial, not a wall?
- Is the Ice-weakness lesson still rewarded at scale (does a prepared party clear faster)?
- Do the woods meaningfully restrict the player, keeping them from kiting the whole pack?
- Does it still read as a wild goblin ambush in the woods, not a designed squad?
- Is it a reasonable Chapter 2 escort fight — harder than Ch1 monster fights, but not a spike?

## Sources

- Game8, "Araguay Woods Walkthrough (Battle 12)": roster (5 Goblin, 1 Black Goblin), objective
  "Defeat all enemies! / Save Chocobo!", deploy 4, recommended level ~11, woods terrain, Goblin
  Ice weakness, Boco rescue = escort with Game-Over-on-death and post-battle recruitment.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553173
- Final Fantasy Wiki, "Araguay Woods" / "Boco": story context (the wounded chocobo rescue).
  https://finalfantasy.fandom.com/wiki/Boco_(Tactics)
- Local: `docs/battles/011-chapter-2-overview.md` (job-escalation rule), `003-siedge-weald.md`
  (Chapter 1 monster-pack handling), `002-mandalia-plain.md` (Red Panther tuning).
</content>
