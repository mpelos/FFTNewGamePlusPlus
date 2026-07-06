# 040 - Finnath Creek (Finath River)

Status: 📝 redesign v3 planned (docs-only) — v1 implementation remains pool-curation only; level-scaling needs in-game verify
Chapter: 4 — "In the Name of Love"
Battle order: Battle 35 (after Bervenia)
Target version: Enhanced v1.5.0
ENTD: global entry **444** (local entry 60, `battle_entd4_ent.bin`)
File: `battle_entd4_ent.bin` (embedded NG+ swap) — `tools/battle_patch.py finath`

Current implementation (entry 444, vanilla-dump verified) — a 12-slot RANDOM POOL (all level 0xFE, runtime-driven):
vanilla = 6 yellow Chocobo (94, s0-5) + 4 Red Chocobo (96, s6-9) + 1 Black Chocobo (95, s10) + 1 Pig (121, s11).
- Converted **s4,s5 yellow → Black Chocobo (95), jl8** — the vanilla pool had only ONE black, so a
  random draw often lacked the Choco-Meteor threat; biasing the pool guarantees ranged-nuke pressure.
  Safe under either reading of the 0xFE slots (changes what a slot becomes, not the spawn count; no level edit).
- Pig (s11) + Entice-recruit/poach flag preserved; yellow healers + red chip untouched. No boss/no rare.

Planned v3 redesign (docs-only in this pass): replace the random outcome with a **fixed six-body flock**
when implemented: **2 Red Chocobo + 2 yellow Chocobo + 1 Black Chocobo + 1 Wild Boar**. The goal is a
learnable Chapter-4 monster-tempo puzzle, not a random roll that can become trivial or spike unfairly.

> ⚠️ Verify in-game: this randomized battle's LEVEL scaling is runtime/OverrideEntryData-driven, so the
> .bin level edits used for fixed battles likely don't apply. If the flock spawns under-levelled, move
> the Ch4 levels (Red 102 / yellow+Black 101 / Wild Boar 100) to the OverrideEntryData layer.

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `037-chapter-4-overview.md`.

## Design Goal

```text
Make Finnath Creek a light-but-real Chapter-4 valley: a de-randomized wild chocobo field where the
player reads the flock, kills or disables Choco Cure sustain, spaces around Choco Meteor, and can still
choose to recruit the Wild Boar without being punished by guest AI, hard status, or boss-level pressure.
```

No active guests appear here. No guest-control implementation is needed for this battle.

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
from range) plus a **tempting side-objective** (Entice the rare boar instead of killing it). After the
Bervenia break-duel, it deliberately switches register to a faster, lighter, positional fight against
a mobile pack. Its lesson: *focus-kill the healer-chocobos and respect the ranged Choco Meteor while
optionally charming the boar.*

The one weakness of the vanilla version is that the flock is **randomized** — it can roll a trivial
all-yellow pack or a nasty all-black one. The faithful New Game++ improvement is to **curate the flock
toward its threatening identity** (guarantee the Choco-Cure sustain and the Choco-Meteor nukes) so the
tempo puzzle reliably has teeth, while keeping it a lighter change-of-pace, not a boss fight.

For New Game++ the identity must stay: **a wild chocobo-menagerie field — fast, self-healing, ranged-
nuking monsters and the optional rare-boar recruit — kept a lighter change-of-pace, but de-randomized
to Chapter-4 strength so the mobility/tempo lesson always lands.**

## Local Data Confirmed / Data Still Needed

```text
CONFIRMED:
- Entry 444 is the Finnath Creek ENTD entry.
- Vanilla uses a 12-slot randomized monster pool:
  6 yellow Chocobo + 4 Red Chocobo + 1 Black Chocobo + 1 Pig.
- Current v1 implementation biased the pool by converting two yellow slots into Black Chocobo.
- Pig slot and Entice/poach hook are part of vanilla identity and must remain.
- No boss, no named rare, no active guest.

STILL NEEDED FOR V3 IMPLEMENTATION:
- Confirm whether the implementation layer can force a fixed six-body output from the random pool.
- If fixed output is not available, define the closest deterministic/weighted substitute and test rolls.
- Confirm whether OverrideEntryData carries Level for this battle or leaves levels at 0xFE runtime scale.
- If the flock spawns under-levelled, move the intended levels to the OverrideEntryData layer.
- Preserve buried map treasure as-is.
```

Job IDs (monsters — verify all in-game):

```text
Chocobo (yellow) id        (TBD - verify)
Red Chocobo id             (TBD - verify)
Black Chocobo id           (TBD - verify)
Wild Boar / Pig-family id  (TBD - verify; optional Entice recruit — keep the recruit flag)
```

## Enemy Party Escalation (Chapter 4 rule)

```text
CHANGE: DE-RANDOMIZE the flock into a fixed Ch4 menagerie that guarantees the threatening variants —
  the Choco-Cure healers AND the Choco-Meteor nukers — at Chapter-4 levels. No human job is swapped;
  this is a monster field. The escalation is making the tempo puzzle reliable instead of a dice roll.
WHY: the fight's identity is "mobile pack that self-heals and nukes from range." Vanilla randomization
  can erase that with a trivial all-yellow roll or over-spike it with too many nukers. Fixing the flock
  toward its own design intent is the faithful Ch4 escalation: it raises the floor without adding a
  second engine, and keeps Finnath a lighter change-of-pace.
REJECTED DEFAULTS: no Bull Demon / Minotaur bruiser, no Cockatrice/Petrify beast, no instant-death
  monster, no all-Black-Chocobo nuke stack. Those variants add a second demand or make the valley too
  spiky.
WHAT IS NOT CHANGED: the chocobo-menagerie identity, the open field, the high monster Move, and the
  optional rare-boar Entice recruit all remain. No brand-new caste, no boss, no rare boss item.
```

## Sanctioned exceptions (carried precedents)

```text
MONSTER PACK SELF-HEAL (yellow Choco Cure) — allowed; the answer is to focus-kill the healers first.
  Pack sustain, not a lock; race-able.
RANGED MONSTER AoE (Black Choco Meteor) — allowed; telegraphed ranged nuke, spaceable; race-able by
  killing the Black Chocobos. No status.
NO HARD STATUS — explicitly NO Petrify/instant-death monsters here (no Cockatrice, etc.). Keeps the
  carried no-hard-lock rule; this is a tempo fight, not a status trap.
WILD BOAR ENTICE RECRUIT / POACH — preserved exactly as vanilla (Speechcraft + Beast Tongue to Entice;
  rare poach). We are NOT adding, upgrading, or promising any equipment reward through Finnath; the
  boar hook is a preserved monster-system side objective, not the Chapter 4 spoils channel.
```

## Rare/reward handling

```text
None. Per `chapter-4-rewards-implementation.md`, Finnath Creek has no guaranteed equipment spoils.
No named boss appears here, no boss rare is assigned, and no non-buyable gear is introduced.
Monster drops/poach tables and buried map treasure remain vanilla behavior, not NG++ reward placement.
```

## Proposed Composition (New Game++ Finnath Creek v3)

Replace the random outcome with a fixed flock of six that reliably poses the tempo puzzle; keep the
optional recruitable boar. Modest Chapter-4 levels — this is a change-of-pace, not a spike. Red
Chocobos `102` become the headline ranged pressure; yellow and Black Chocobos sit at `101`; Wild Boar
stays `100`.

Vanilla composition:

```text
RANDOMIZED monster pool:
  6x Chocobo (yellow)
  4x Red Chocobo
  1x Black Chocobo
  1x Pig / boar-family recruit target
```

v3 composition:

| Slot | Role | Monster | Level | Br/Fa | Purpose |
| ------ | ------ | --------- | ------- | --- | --------- |
| n | Ranged pressure | Red Chocobo | `102` | `90/30` | High-tempo ranged chip; primary pressure piece. |
| n | Ranged pressure | Red Chocobo | `102` | `90/30` | Second red keeps the flock aggressive without making Meteor the whole fight. |
| n | Sustain | Chocobo (yellow) | `101` | `90/30` | Choco Cure — keeps the flock alive; first kill if the party is using chip damage. |
| n | Sustain | Chocobo (yellow) | `101` | `90/30` | Second healer — makes the pack feel like a pack, not six isolated monsters. |
| n | Meteor threat | Black Chocobo | `101` | `90/30` | Choco Meteor remains present, but as a single answerable spike. |
| n | Optional recruit | Wild Boar | `100` | `60/40` | Rare Entice target — keep recruitable; do not force-kill. |

Current difference from vanilla:

```text
- Enemy count is fixed at 6 active monsters instead of being selected from the 12-slot random pool.
- Vanilla can roll many yellow/red chocobos with only one Black in the pool; v3 guarantees exactly
  2 Red, 2 yellow, 1 Black, and 1 Wild Boar.
- The optional recruit/poach side objective is preserved through the Wild Boar slot.
- The fight remains a monster-tempo valley: no boss, no human kits, no rare equipment reward,
  and no hard-status beast.
```

Reasoning:

The faithful move is to **lock in the menagerie's intended threats and keep it light**. Two Red
Chocobos make the flock more active turn-to-turn, two yellow Chocobos preserve the Choco-Cure sustain
read, and a single Black Chocobo keeps Choco Meteor in the fight without making the whole map a Meteor
stack. The optional Wild Boar stays as the side-objective (Entice, don't kill). Levels stay at the
bottom of the band (`100`-`102`) to keep it a change-of-pace dip in the curve between Bervenia and the
Zalmo rematch.

Rejected variants:

```text
- Pool-only v1: better than vanilla, but still lets the puzzle disappear or spike by random draw.
- Two Black Chocobos at `102`: too much Choco Meteor emphasis for this v3 direction.
- Bull Demon / Minotaur bruiser: adds a second melee-bruiser engine instead of sharpening the flock.
- Cockatrice / status beast: violates Finnath's no-hard-status tempo identity.
- Mostly yellow Chocobos: too low-pressure for Chapter 4 and loses the Meteor lesson.
```

## Builds (monster field — no human kit to spec)

```text
Monsters have fixed innate skillsets; there is no equipment, secondary, reaction, support, or movement
slot to assign. The Chapter 4 "complete setup" rule applies to active humans, not monster bodies.
Confirm each monster's innate ability set in-game and set only LEVEL + fixed roster:
  Black Chocobo — Choco Meteor (ranged AoE), Choco Ball; high Move/Fly.
  Chocobo (yellow) — Choco Cure (pack heal), Choco Attack; high Move.
  Red Chocobo — Choco Pellets / Choco Esuna; high Move.
  Wild Boar — pig-family innate set; keep its Entice-recruit flag — do NOT script it hostile-only.
    (Poach reward is vanilla; untouched.)
No human equipment or ability-completeness checklist exists here.
```

## Positioning Plan

```text
Open river/field: scatter the flock so the chocobos' high Move turns the map into a mobility puzzle —
  the Red Chocobos start with open lanes for ranged pressure, the yellow healers central (so they can
  reach any wounded chocobo), the Black Chocobo at range with Meteor sightlines, and the Wild Boar off
  to one side (so the player can choose to reach and Entice it rather than being forced to kill it).
Preserve the open geometry and high Move (the tempo identity). Do NOT box the flock into a corner —
  the point is chasing/cornering a mobile, self-healing pack.
Keep it light: bottom-of-band levels, no status beasts, no boss.
```

The creek should say: "a wild river crossing — run down the healer-birds, dodge the meteor-bird, and
if you're patient, charm the lucky boar instead of cooking it."

## Simulation Plan and Results

Simulation artifact:

```text
tmp/fft-level-design-040-finnath-creek/
  assumptions.md
  simulate.py
  iteration-results.json
  iteration-results.md
```

Model scope:

```text
Coarse deterministic opening-pressure model over the first four rounds.
It scores pressure, target clarity, Choco Meteor answerability, recruit safety, breather role,
and hard-status risk. It does not claim to simulate exact FFT damage formulas.
```

Result summary:

| Candidate | Pressure | Clarity | Meteor answer | Recruit safety | Breather | Status risk | Verdict |
|---|---:|---:|---:|---:|---:|---:|---|
| v1 biased random pool | 167 | 79 | 66 | 71.3 | 57.7 | 0 | Rejected: too spiky / still random |
| v2 fixed chocobo tempo flock | 129 | 97 | 90 | 88.0 | 83.6 | 0 | **Accepted** |
| all black meteor spike | 181 | 57 | 46 | 65.0 | 61.8 | 0 | Rejected: too spiky |
| bull demon bruiser variant | 153 | 77 | 82 | 69.7 | 57.5 | 0 | Rejected: second engine / too spiky |
| status beast variant | 180 | 62 | 65 | 45.5 | 27.2 | 40 | Rejected: hard-status violation |
| soft yellow pasture | 101 | 49 | 82 | 88.0 | 95.4 | 0 | Rejected: unclear / too soft |

Iteration decision:

```text
V3 target flock: 2 Red Chocobo + 2 yellow Chocobo + 1 Black Chocobo + 1 Wild Boar.
The prior v2 simulation accepted a fixed flock approach; v3 keeps the same de-randomized valley role
but shifts headline pressure from double Black Choco Meteor to double Red Chocobo tempo.
Do not add a bruiser/status beast unless future playtests prove the fixed flock cannot threaten tuned
NG++ parties even at the documented level band; if that happens, redesign and resimulate first.
```

## Implementation Checklist

- [ ] Confirm the current v1 implementation and original randomized pool still match entry 444.
- [ ] Determine whether the v3 implementation can force a fixed flock output instead of a weighted random pool.
- [ ] Replace the random outcome with the fixed flock (2 Red + 2 yellow + 1 Black Chocobo + 1 Wild Boar).
- [ ] Preserve the Wild Boar's Entice-recruit flag (do NOT make it hostile-only); leave poach untouched.
- [ ] Set levels: Red Chocobos `102`; yellow + Black `101`; Wild Boar `100`.
- [ ] Confirm NO status beasts are present (no Cockatrice/Petrify); keep it a tempo fight.
- [ ] Keep the open field + high monster Move; do not over-scale (change-of-pace).
- [ ] Patch via the correct layer; keep the diff inside the Finnath Creek window only.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify recruit flag intact.
- [ ] Install mod, test from a New Game+ save; confirm it plays as a light monster-tempo field + Wild Boar.

## Test Questions

- Does the curated flock reliably pose the tempo puzzle (focus-kill the Choco-Cure healers, manage the
  Red Chocobo tempo, and respect the single Choco-Meteor threat) — never a trivial all-yellow roll?
- Is it clearly a LIGHTER change-of-pace (3/5★ feel, no boss, bottom-of-band levels) after Bervenia?
- Is the optional Wild Boar still recruitable via Entice (recruit flag intact), not forced-kill?
- Are there NO hard-status beasts (no Petrify/instant-death) — keeping the no-hard-lock rule?
- Does the high monster Move still make the open field a mobility/positioning puzzle?
- Does it read as a wild river menagerie, not a designed arena?
- Does the fight stay below Bervenia/Outlying Church pressure while still forcing target priority?

## Sources

- Game8, "Finnath Creek Walkthrough (Battle 35)": randomized chocobo flock (yellow Choco Cure, Red/
  Black Choco Pellets/Choco Meteor) + optional Pig recruit via Entice, objective "Defeat all enemies!",
  recommended level ~41, 3/5 stars, deploy 5, rewards (28,200 Gil + buried treasure).
  https://game8.co/games/Final-Fantasy-Tactics/archives/553195
- Final Fantasy Wiki, "Finath River": story/terrain context.
  https://finalfantasy.fandom.com/wiki/Finath_River
- Local: `037-chapter-4-overview.md` (job-escalation + rare-loot rules), `015`/`027` (Chocobo/Dragoon
  monster precedents), `032-yuguewood.md` (monster-field handling).
