# 013 - Araguay Woods

Status: ✅ implemented (v1, entry 404); Boco scaled to party level (2026-06-27, playtest-confirmed); Red Panther add still deferred (see below)
Chapter: 2 — "The Manipulator and the Subservient"
Battle order: Battle 12 (after Merchant City of Dorter)
Target version: Enhanced v1.5.0
ENTD: global entry **404** (battle_entd4, local entry 20) — confirmed by composition matching
File: `entd/battle_entd4_ent.bin` (embedded; swapped only in NG+ by the code mod)

> Implemented via `tools/battle_patch.py araguay`. NG+-only by construction (whole ENTD swapped
> only in NG+). See `011-chapter-2-overview.md`.

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

## Local Data Confirmed (entry 404)

```text
slot  cid    name  flags  job             role                       action
s0    0x82   118   0x30   94 Chocobo      Boco — rescuable ally      SCALE -> 100 (party level)
s1    0x82   255   0x20   98 Gobbledeguck Black-Goblin-tier melee    SCALE -> L101
s2    0x82   255   0x20   97 Goblin       swarm body                 SCALE -> L100
s3    0x82   255   0x20   97 Goblin       swarm body                 SCALE -> L100
s4    0x82   255   0x20   97 Goblin       swarm body                 SCALE -> L100
s5    0x82   255   0x20   97 Goblin       swarm body                 SCALE -> L100
s6    0x82   255   0x20   97 Goblin       swarm body                 SCALE -> L100
s7    0x17   23    0x89   (named)         story unit                 LEAVE (lvl 254)
s8    0x34   52    0x49   (named)         story unit                 LEAVE (lvl 254)
```

Monster job IDs: Goblin 97, Gobbledeguck (Black-Goblin tier) 98, Chocobo 94 (shared with Siedge
Weald / Mandalia). All-monster fight — Level + JobLevel are the only levers (no gear, no R-S-M),
exactly like Ch1 Siedge Weald. Boco is distinguished by name_id 118 + flags 0x30 (the goblins are
flags 0x20).

### Boco note (playtest item #1) — RESOLVED 2026-06-27

**Playtest confirmed the bug.** Player report: "Boco still comes LV10... I'm LV65 so the Goblins
hit-kill Boco", which made the optional **"Save Chocobo!"** path impossible (he was gibbed before the
player could intercept). The mandatory **"Defeat all enemies!"** path was unaffected.

**Fix applied:** Boco's level byte (s0, offset 0x03) set from 10 to **100 (= party level)** in the
modded ENTD, the same dynamic-level lever the goblins use (100 = party, 101 = party+1). Boco now
matches the party and the swarm exactly as he did in vanilla, where he sat at roughly goblin level.
NG+-only by construction (whole-file swap). Only the level byte changed; his job (94 Chocobo), flags
(0x30), name_id, and ability bytes are untouched, so his team and Game-Over scripting are unaffected.

**Why not the runtime guest-scaler:** Boco's charId is **0x82**, a *generic* monster id shared with
all the goblins, and his job (94) is not equal to his charId, so the `ScaleGuestsAlways` `job == charId`
guard in Program.cs can never target him without also hitting the goblins. A monster guest like Boco
must be scaled by a **direct ENTD level edit**, not the runtime charId scaler.

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

## Implemented (v1, entry 404)

Applied with `python tools/battle_patch.py araguay`; diff contained to local entry 20 (global 404),
12 bytes. Black-Goblin tier (s1) → L101; five Goblins (s2–s6) → L100; JobLevel 8 on all six.
Story units (s7/s8) untouched.

**Boco level fix (2026-06-27):** Boco (s0) level byte set 10 -> 100 (party level) via a direct 1-byte
ENTD edit straight into the tracked `.bin` (battle_patch.py is no longer present locally; the embedded
`.bin` is now the source of truth). Verified surgical (only offset 0x03 changed) and confirmed in the
deployed DLL.

**Deferred — Red Panther escalation (slot-add):** the doc's single wrinkle adds a 7th monster (a
fast poison beast with a lane to Boco). That requires inserting a unit at a verified map position,
batched for the playtest pass (same policy as the Merchant Dorter Knight add).

## Implementation Checklist

- [x] Identify Araguay ENTD entry (404) on Windows data; fill "Local Data Confirmed".
- [x] Dump original entry; verify 5 Goblin + 1 Black-Goblin tier + Boco + story slots.
- [x] Confirm Goblin / Black-Goblin / Chocobo monster job IDs.
- [ ] Add the Red Panther slot (deferred — needs a verified map position; do during playtest).
- [x] Set levels: Goblins `100`; Black-Goblin tier `101`.
- [x] Set JobLevel `8` on all scaled monsters; no equipment.
- [x] Patch the embedded ENTD (NG+-only by construction); diff inside entry 404 only.
- [x] Re-dump and diff; confirm changes are small and intentional; Boco slot untouched.
- [x] Resolve the Boco-level question: playtest confirmed LV10 Boco was unviable; fixed to party level (100).
- [ ] Re-playtest the rescue path from a NG+ save to confirm a party-level Boco survives the escort.

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
