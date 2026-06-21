# 040 - Finnath Creek (Finath River)

Status: ✅ implemented (v1, entry 444) — pool-curation only; level-scaling needs in-game verify
Chapter: 4 — "In the Name of Love"
Battle order: Battle 35 (after Bervenia)
Target version: Enhanced v1.5.0
ENTD: global entry **444** (local entry 60, `battle_entd4_ent.bin`)
File: `battle_entd4_ent.bin` (embedded NG+ swap) — `tools/battle_patch.py finath`

Implemented (entry 444, vanilla-dump verified) — a 12-slot RANDOM POOL (all level 0xFE, runtime-driven):
vanilla = 6 yellow Chocobo (94, s0-5) + 4 Red Chocobo (96, s6-9) + 1 Black Chocobo (95, s10) + 1 Pig (121, s11).
- Converted **s4,s5 yellow → Black Chocobo (95), jl8** — the vanilla pool had only ONE black, so a
  random draw often lacked the Choco-Meteor threat; biasing the pool guarantees ranged-nuke pressure.
  Safe under either reading of the 0xFE slots (changes what a slot becomes, not the spawn count; no level edit).
- Pig (s11) + Entice-recruit/poach flag preserved; yellow healers + red chip untouched. No boss/no rare.

> ⚠️ Verify in-game: this randomized battle's LEVEL scaling is runtime/OverrideEntryData-driven, so the
> .bin level edits used for fixed battles likely don't apply. If the flock spawns under-levelled, move
> the Ch4 levels (Black 102 / yellow+red 101 / Pig 100) to the OverrideEntryData layer.

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

Original enemy composition (verified via Game8, Battle 35):

```text
RANDOMIZED monster flock (no fixed counts), drawn from:
  Chocobo        (yellow — Choco Cure: heals the pack)
  Red Chocobo    (Choco Pellets / Choco Esuna — ranged chip / cleanse)
  Black Chocobo  (Choco Meteor — ranged AoE nuke; the real threat)
  Pig            (x1 — OPTIONAL recruit via Entice; a rare monster)
```

Public walkthrough details:

```text
Recommended level: ~41.  Difficulty: 3/5 stars.  Deploy up to 5.  Win: defeat all enemies.
Open river/field map (Finath) — a wild MONSTER field, a change of pace from human-job fights.
THE FLOCK: yellow Chocobos CHOCO CURE the pack (sustain), Black Chocobos CHOCO METEOR (ranged AoE),
  Red Chocobos chip/cleanse. Chocobos are FAST (high Move) — a mobility/tempo puzzle.
THE PIG: one rare Pig — do NOT kill it; recruit it with ENTICE (needs Speechcraft + Beast Tongue).
  It poaches into high-tier accessories (e.g. Ribbon) and lays eggs to farm — an EXISTING vanilla
  monster-recruit/poach mechanic.
Rewards: 28,200 Gil + four buried-treasure locations.
```

Design reading:

Finnath Creek is **the Chapter-4 monster-menagerie change-of-pace**: no human boss, no rare boss item
— just a wild flock whose identity is **mobile monster tempo** (fast chocobos that self-heal and nuke
from range) plus a **tempting side-objective** (Entice the rare Pig instead of killing it). After the
Bervenia break-duel, it deliberately switches register to a faster, lighter, positional fight against
a mobile pack. Its lesson: *focus-kill the healer-chocobos and respect the ranged Choco Meteor while
optionally charming the Pig.*

The one weakness of the vanilla version is that the flock is **randomized** — it can roll a trivial
all-yellow pack or a nasty all-black one. The faithful New Game++ improvement is to **curate the flock
toward its threatening identity** (guarantee the Choco-Cure sustain and the Choco-Meteor nukes) so the
tempo puzzle reliably has teeth, while keeping it a lighter change-of-pace, not a boss fight.

For New Game++ the identity must stay: **a wild chocobo-menagerie field — fast, self-healing, ranged-
nuking monsters and the optional rare-Pig recruit — kept a lighter change-of-pace, but de-randomized
to Chapter-4 strength so the mobility/tempo lesson always lands.**

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm the randomized monster slots; REPLACE the random roll with a CURATED Ch4 flock (below) so the
  fight reliably tests the tempo/sustain/ranged-nuke puzzle (no trivial all-yellow roll).
Keep the OPTIONAL PIG slot and its Entice-recruit flag intact (do NOT remove the recruit/poach hook —
  it is vanilla; we are not adding or buffing the Ribbon poach, just preserving it).
Keep the open river/field geometry and the chocobos' high Move (the mobility puzzle).
This is a no-boss, no-rare CHANGE-OF-PACE: modest Ch4 levels (100-102), NOT a spike.
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
Leave the buried map treasure as-is (existing map loot).
```

Job IDs (monsters — verify all in-game):

```text
Chocobo (yellow) id        (TBD - verify)
Red Chocobo id             (TBD - verify)
Black Chocobo id           (TBD - verify)
Pig id                     (TBD - verify; optional Entice recruit — keep the recruit flag)
(Bull Demon id, optional)  (TBD - verify; only if the optional bruiser variant is used — see below)
```

## Job Escalation (Chapter 4 rule)

```text
CHANGE: DE-RANDOMIZE the flock into a curated Ch4 menagerie that guarantees the threatening variants —
  the Choco-Cure healers AND the Choco-Meteor nukers — at Chapter-4 levels. (No human job is swapped;
  this is a monster field. The "escalation" is making the tempo puzzle reliable instead of a dice roll.)
WHY: the fight's identity is "mobile pack that self-heals and nukes from range." Vanilla randomization
  can erase that (a trivial all-yellow roll). Curating the flock toward its own design intent IS the
  faithful Ch4 escalation — it raises the floor without changing the plan, and keeps it a lighter
  change-of-pace.
OPTIONAL (one-new-demand budget): a single non-chocobo BRUISER (Bull Demon / Minotaur-type) MAY be
  added for variety if the curated flock plays too soft in testing — a melee vector to complement the
  ranged chocobos. Add AT MOST one, and only a NON-status beast (NO Cockatrice/Petrify, NO instant-
  death monsters — keep the no-hard-lock rule). Default is the pure chocobo flock + Pig.
WHAT IS NOT CHANGED: the chocobo-menagerie identity, the open field, the high monster Move, and the
  optional rare-Pig Entice recruit all remain. No brand-new caste, no boss, no rare boss item.
```

## Sanctioned exceptions (carried precedents)

```text
MONSTER PACK SELF-HEAL (yellow Choco Cure) — allowed; the answer is to focus-kill the healers first.
  Pack sustain, not a lock; race-able.
RANGED MONSTER AoE (Black Choco Meteor) — allowed; telegraphed ranged nuke, spaceable; race-able by
  killing the Black Chocobos. No status.
NO HARD STATUS — explicitly NO Petrify/instant-death monsters here (no Cockatrice, etc.). Keeps the
  carried no-hard-lock rule; this is a tempo fight, not a status trap.
PIG ENTICE RECRUIT / POACH — preserved exactly as vanilla (Speechcraft + Beast Tongue to Entice; rare
  poach). We are NOT adding or upgrading the Ribbon poach — it is existing game behavior; the "best of
  best" reservation concerns BOSS loot we place, not pre-existing monster-poach tables.
```

## Boss rare loot

```text
None. No named boss here — no rare boss item (per the Chapter 4 overview tiering). Monster drops and
the optional Pig's poach are EXISTING vanilla behavior, left untouched. Buried map treasure stays as-is.
```

## Proposed Composition (New Game++ Finnath Creek v1)

Replace the random roll with a curated flock (6) that reliably poses the tempo puzzle; keep the
optional Pig. Modest Chapter-4 levels — this is a change-of-pace, not a spike. Black Chocobos `102`
(the threats); yellow/red `101`; Pig `100`.

| Slot | Role | Monster | Level | Purpose |
|------|------|---------|-------|---------|
| n | Black Chocobo | Black Chocobo | `102` | Choco Meteor — ranged AoE nuke; the real threat. |
| n | Black Chocobo | Black Chocobo | `102` | Second nuker — two Meteors force spacing/focus. |
| n | Chocobo (yellow) | Chocobo | `101` | Choco Cure — sustains the pack; focus-kill priority. |
| n | Chocobo (yellow) | Chocobo | `101` | Second healer — pack won't fold to chip damage. |
| n | Red Chocobo | Red Chocobo | `101` | Choco Pellets / cleanse — mobile chip + Esuna. |
| n | Pig (OPTIONAL recruit) | Pig | `100` | Rare Entice target — do NOT force-kill; vanilla recruit/poach. |

Reasoning:

The faithful move is to **lock in the menagerie's intended threats and keep it light**. Two Black
Chocobos guarantee the Choco-Meteor ranged pressure; two yellow Chocobos guarantee the Choco-Cure
sustain (so the player must focus-kill healers, not just chip); a Red Chocobo adds mobile cleanse.
That makes the tempo/positioning puzzle reliable at Chapter-4 strength without making it a boss fight.
The optional Pig stays as the side-objective (Entice, don't kill). Levels stay at the bottom of the
band (`100`–`102`) to keep it a change-of-pace dip in the curve between Bervenia and the Zalmo
rematch. (If testing finds it too soft, add one Bull Demon per the optional note — no status beasts.)

## Builds (monster field — no human kit to spec)

```text
Monsters have fixed innate skillsets; there is no equipment to assign. Confirm each monster's ability
set in-game and set only LEVEL + the curated roster:
  Black Chocobo — Choco Meteor (ranged AoE), Choco Ball; high Move/Fly.
  Chocobo (yellow) — Choco Cure (pack heal), Choco Attack; high Move.
  Red Chocobo — Choco Pellets / Choco Esuna; high Move.
  Pig — Oink / Toot / Straighten (harmless); keep its Entice-recruit flag — do NOT script it hostile-
    only. (Poach reward is vanilla; untouched.)
No Reaction/Support/Movement equipment slots for monsters — leave innate.
```

## Positioning Plan

```text
Open river/field: scatter the flock so the chocobos' high Move turns the map into a mobility puzzle —
  the Black Chocobos start at range (Meteor sightlines), the yellow healers central (so they can reach
  any wounded chocobo), the Red Chocobo roving, the Pig off to one side (so the player can choose to
  reach and Entice it rather than being forced to kill it).
Preserve the open geometry and high Move (the tempo identity). Do NOT box the flock into a corner —
  the point is chasing/cornering a mobile, self-healing pack.
Keep it light: bottom-of-band levels, no status beasts, no boss.
```

The creek should say: "a wild river crossing — run down the healer-birds, dodge the meteor-birds, and
if you're patient, charm the lucky pig instead of cooking it."

## Implementation Checklist

- [ ] Identify Finnath Creek `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; confirm the randomized monster slots + the Pig slot.
- [ ] Replace the random roll with the curated flock (2 Black + 2 yellow + 1 Red Chocobo + 1 Pig).
- [ ] Preserve the Pig's Entice-recruit flag (do NOT make it hostile-only); leave poach untouched.
- [ ] Set levels: Black Chocobos `102`; yellow + Red `101`; Pig `100`.
- [ ] Confirm NO status beasts are present (no Cockatrice/Petrify); keep it a tempo fight.
- [ ] Keep the open field + high monster Move; do not over-scale (change-of-pace).
- [ ] Patch via the correct layer; keep the diff inside the Finnath Creek window only.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify recruit flag intact.
- [ ] Install mod, test from a New Game+ save; confirm it plays as a light monster-tempo field + Pig.

## Test Questions

- Does the curated flock reliably pose the tempo puzzle (focus-kill the Choco-Cure healers, dodge the
  Choco-Meteor nukers) — never a trivial all-yellow roll?
- Is it clearly a LIGHTER change-of-pace (3/5★ feel, no boss, bottom-of-band levels) after Bervenia?
- Is the optional Pig still recruitable via Entice (recruit flag intact), not forced-kill?
- Are there NO hard-status beasts (no Petrify/instant-death) — keeping the no-hard-lock rule?
- Does the high monster Move still make the open field a mobility/positioning puzzle?
- Does it read as a wild river menagerie, not a designed arena?

## Sources

- Game8, "Finnath Creek Walkthrough (Battle 35)": randomized chocobo flock (yellow Choco Cure, Red/
  Black Choco Pellets/Choco Meteor) + optional Pig recruit via Entice, objective "Defeat all enemies!",
  recommended level ~41, 3/5 stars, deploy 5, rewards (28,200 Gil + buried treasure).
  https://game8.co/games/Final-Fantasy-Tactics/archives/553195
- Final Fantasy Wiki, "Finath River": story/terrain context.
  https://finalfantasy.fandom.com/wiki/Finath_River
- Local: `037-chapter-4-overview.md` (job-escalation + rare-loot rules), `015`/`027` (Chocobo/Dragoon
  monster precedents), `032-yuguewood.md` (monster-field handling).
```
</content>
