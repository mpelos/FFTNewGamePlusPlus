# 046 - Lake Poescas (Poeskas Lake)

Status: 📝 redesign v2 planned (docs-only) — v1 implementation exists for entry 453
Chapter: 4 — "In the Name of Love"
Battle order: Battle 41 (after Mount Germinas)
Target version: Enhanced v1.5.0
ENTD: global entry **453** (local 69, entd4)
File: `battle_entd4_ent.bin`

> **NG++ reward applied (2026-06-27):** Cursed Ring (s0), thematic to the undead battle; the two existing
> Phoenix Down spoils are kept. Guaranteed Spoils of War (ENTD 0x1e), NG+ only, within the 3-cap, no
> steal needed. Canonical map: `chapter-4-rewards-implementation.md`.

## Current Implementation / Data Reality

```text
DATA REALITY (verified from entd4 dump + JobData.xml):
  Entry 453 sits exactly between Germinas (452) and the Limberry assassin chain (454/455).
  Every enemy slot is a MONSTER undead (eq=254, no equipment slots), not a human Archer/Mystic/Summoner.
    slots 0,3 = job 70/71  "Float, Undead" floaters
    slots 1,2 = job 63     "Float, Undead" floaters
    slots 4,5 = job 114    Revenant family (InnateStatus: Undead)
  All six are innately UNDEAD, so the reraise/permakill war is intact at the data level.

Current v1 implementation:
  slot 4 Revenant = 103 (anchor)   slot 5 Revenant = 102
  slots 0,3 floaters = 102          slots 1,2 floaters = 101
  Monsters: LEVEL only set; job / undead innates / equipment-empty monster structure / scripting untouched.
```

Planned v2 redesign (docs-only in this pass): keep the data-faithful all-monster undead roster. Do not
force the older public-guide human-job plan onto the ENTD. The redesign is a deliberate **permakill
resource war**: spread the six undead so Phoenix Down/Holy/Seal Evil answers stay decisive, but the
player must spend real actions to end the dead for good. Cursed Ring is reward payload only because
monsters cannot equip accessories.

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from the real
> game files. This doc is the design; the byte patch is applied on the Windows box. See
> `037-chapter-4-overview.md`.

## Design Goal

```text
Make Poeskas Lake the hard all-undead skirmish: every enemy returns unless properly finished, the lake
spread taxes Phoenix Down/Holy/Seal Evil usage, and the fight never becomes a hard-status trap or an
unkillable sustain loop. The puzzle is permakill discipline, not human-job synergy.
```

No active guests appear here. No guest-control implementation is needed for this battle.

## Original Battle

Objective:

```text
Defeat all enemies!   (and make them STAY dead — every foe is undead and can return)
```

Player deployment:

```text
Up to 5 units, including Ramza. No guests.
```

Public-guide composition (useful for player-facing identity, but superseded by local ENTD data):

```text
2x Revenant   (undead melee / reraise)
2x Archer     (undead ranged chip)
1x Mystic     (undead soft status)
1x Summoner   (undead AoE)
ALL six enemies are UNDEAD.
```

Public walkthrough details:

```text
Recommended level: ~59. Difficulty: 5/5 stars. Deploy up to 5.
Win: defeat all enemies, but every enemy is undead and may return instead of crystallizing.
Answers: Phoenix Down, Holy damage, Seal Evil, and finishing undead bodies for good.
Rewards: 30,400 Gil, Phoenix Down x2, buried treasure.
```

Design reading:

Lake Poescas is **the all-undead permakill war**. The public guide describes a mixed undead band, but
the local data expresses that same identity through monster-undead slots rather than human jobs. The
faithful NG++ design therefore preserves the real ENTD: six undead monsters, two Revenant-family
anchors, four floating undead, all vulnerable to the player's permakill tools. Chipping them down is
not enough; the player must spend the right actions and finish them for good.

For New Game++ the identity must stay: **a hard all-undead lake fight whose whole demand is reraise
management and decisive permakill tools (Phoenix Down / Holy / Seal Evil), kept boss-less, data-faithful,
and free of artificial hard lockdown.**

## Local Data Confirmed / Data Still Needed

```text
CONFIRMED:
- Entry 453 is the Poeskas Lake ENTD entry.
- All six enemies are monster undead.
- Slots 4/5 are Revenant-family undead anchors.
- Slots 0-3 are floating undead monster jobs.
- Monsters have no equipment slots; human complete-kit rules do not apply.
- No active guest, no boss.
- Reward ledger maps this battle to Cursed Ring + two Phoenix Downs guaranteed spoils.

STILL NEEDED FOR V2 IMPLEMENTATION:
- Confirm exact monster job names/ability sets for job 70/71, job 63, and job 114.
- Confirm undead/reraise behavior and Phoenix Down/Holy/Seal Evil answers in game.
- Confirm whether OverrideEntryData carries level for this battle or leaves it at runtime scale.
- Preserve lake terrain and spread positioning.
- Preserve buried map treasure as vanilla map loot.
```

## Enemy Party Escalation (Chapter 4 rule)

```text
CHANGE: no human job swap. Keep the local all-monster undead roster and tune it through level band,
  spread positioning, and protected counterplay.
WHY: the fight's identity is already the reraise/permakill puzzle. The public-guide plan to add an
  undead Dark-heal Mystic assumed human slots that the data does not have. Forcing that plan would
  break the actual ENTD shape and risk an unkillable sustain slog. The faithful Chapter-4 escalation is
  to make the existing monster undead band demand real resource discipline.
CONSTRAINT: every enemy remains undead; PD/Holy/Seal Evil must remain decisive; no hard-status trap;
  no dark-heal loop; no non-undead variety.
WHAT IS NOT CHANGED: lake terrain, monster undead identity, reraise/permakill behavior, no boss.
```

## Sanctioned Exceptions

```text
UNDEAD RERAISE — preserved as the core mechanic and counterplay test. The player answers with Phoenix
  Down, Holy, Seal Evil, or finishing the enemy while it is down.
ALL-MONSTER ENTD — sanctioned here because the local data proves every active enemy is a monster. No
  equipment/secondary/reaction/support/movement setup exists for monster slots.
PHOENIX DOWN SPOILS — kept as thematic minor spoils and practical undead answers.
NO DARK-HEAL LOOP — rejected; sustain layered over reraise risks cleanup slog.
NO HARD STATUS — rejected; this battle tests permakill discipline, not turn deletion.
```

## Rare/reward handling

```text
Guaranteed spoils for entry 453: CURSED RING + PHOENIX DOWN + PHOENIX DOWN.
These are delivered by the Spoils of War reward channel; the player must never be required to Steal.
COMBAT ROLE: Cursed Ring is reward payload only because monsters cannot equip accessories.
PRESERVE: buried map treasure remains vanilla map loot, not the NG++ reward channel.
```

## Proposed Composition (New Game++ Poeskas Lake v2)

Keep the local six-monster roster. Band `101`-`103`; the Revenant anchor carries the top level, and the
floaters create the spread/resource tax.

| Slot | Role | Unit type | Level | Br/Fa | Purpose |
| ------ | ------ | ----------- | ------- | --- | --------- |
| s4 | Revenant anchor | Revenant-family monster undead | `103` | `86/35` | Main reraising melee body; forces decisive permakill. |
| s5 | Revenant anchor | Revenant-family monster undead | `102` | `86/35` | Second melee/reraise body; prevents one-action cleanup. |
| s0 | Floating undead | Monster undead floater | `102` | `86/35` | Mobile undead pressure; spreads Phoenix Down/Holy decisions. |
| s3 | Floating undead | Monster undead floater | `102` | `86/35` | Second upper-band floater; keeps the lake from collapsing into one side. |
| s1 | Floating undead | Monster undead floater | `101` | `86/35` | Lower-band body; resource tax without spike. |
| s2 | Floating undead | Monster undead floater | `101` | `86/35` | Lower-band body; resource tax without spike. |

Reasoning:

The faithful move is to **treat the verified monster data as the design surface**. Two Revenants anchor
the reraise war, and four floaters spread the lake so the player cannot erase the whole field with one
clustered answer. Levels are high enough to make the undead tax real, but the fight's true difficulty is
still action economy: which enemy gets Phoenix Down, which one gets Holy, which body can be safely left
down, and whether the player can finish all six before the lake resets.

Rejected variants:

```text
- Humanized Dark-heal plan: ignores local all-monster ENTD reality.
- Monster Dark-heal loop: risks sustain + reraise cleanup slog.
- Hard-status drowned trap: wrong engine; Poeskas is not a lockdown map.
- Overlevelled dead: replaces permakill puzzle with raw stats.
- Clustered AoE cleanup: makes the fight trivial or tedious, not tactical.
- Non-undead monster mix: breaks the all-undead identity.
```

## Builds (monster field — no human kit to spec)

```text
Monsters have innate kits and no equipment, secondary, reaction, support, or movement slots.
The Chapter 4 complete-human setup rule does not apply here.

Revenant-family monsters:
  - Preserve Undead innate.
  - Preserve reraise/permakill behavior.
  - Set levels only: 103 / 102.

Floating undead monsters:
  - Preserve Float + Undead innate.
  - Preserve innate monster ability sets.
  - Set levels only: 102 / 102 / 101 / 101.

Rewards:
  - Cursed Ring and Phoenix Downs are spoils payloads only.
  - Do not attempt to equip monster slots with accessories/items.
```

## Positioning Plan

```text
Lake terrain: spread the undead so the player cannot solve the fight with one AoE or one compact PD
chain. The two Revenants pressure different approaches from the water's edge; floaters split across the
lake to tax target priority and movement.
Preserve every undead flag and reraise behavior. The player answers must stay decisive: PD, Holy, Seal
Evil, or finish-while-down.
Avoid clustered cleanup and avoid unreachable undead pockets. Hard, not tedious.
```

The lake should say: "the drowned dead won't lie still — bring tools that end them for good, or spend
the whole battle watching them rise from the water again."

## Simulation Plan and Results

Simulation artifact:

```text
tmp/fft-level-design-046-poeskas-lake/
  assumptions.md
  simulate.py
  iteration-results.json
  iteration-results.md
```

Model scope:

```text
Coarse deterministic all-undead permakill model over the first six rounds.
It scores pressure, permakill demand, answerability, resource tax, cleanup risk, reward safety, and
hard-lock risk. It does not simulate exact FFT formulas or undead heart-counter odds.
```

Result summary:

| Candidate | Pressure | Permakill | Answer | Resource tax | Cleanup risk | Reward safe | Hard lock | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| v2 data-faithful monster band | 230 | 100 | 92 | 90 | 20 | 100 | 0 | **Accepted** |
| humanized dark-heal plan | 248 | 100 | 72 | 90 | 20 | 80 | 0 | Rejected: ignores local data |
| monster dark-heal loop | 265 | 100 | 64 | 100 | 40 | 100 | 0 | Rejected: cleanup slog |
| hard-status drowned trap | 290 | 100 | 56 | 90 | 20 | 100 | 55 | Rejected: hard status |
| overlevelled dead | 256 | 100 | 80 | 100 | 34 | 100 | 0 | Rejected: raw level pressure |
| clustered aoe cleanup | 208 | 90 | 92 | 74 | 46 | 100 | 0 | Rejected: cleanup risk |
| non-undead monster mix | 188 | 51 | 92 | 66 | 20 | 100 | 0 | Rejected: breaks all-undead identity |

Iteration decision:

```text
ACCEPT v2 data-faithful monster band.
Local ENTD reality overrides the public-guide human-job roster. Preserve monster jobs, undead flags,
reraise, PD/Holy answers, and spread positioning. Do not add a Dark-heal loop or hard status.
```

## Implementation Checklist

- [ ] Confirm entry 453 slot order and monster job names for all six enemies.
- [ ] Preserve every enemy as undead; preserve reraise/permakill behavior.
- [ ] Keep monster jobs; do not convert to human Archer/Mystic/Summoner slots.
- [ ] Set levels: Revenants `103`/`102`, floaters `102`/`102`/`101`/`101`.
- [ ] Spread positioning to create resource tax without cleanup slog.
- [ ] Preserve guaranteed spoils: Cursed Ring + two Phoenix Downs.
- [ ] Do not equip Cursed Ring or accessories on monster slots.
- [ ] Preserve buried map treasure.
- [ ] Re-dump and diff; confirm undead flags + reraise behavior are intact.
- [ ] Install mod, test from a New Game+ save; confirm PD/Holy/Seal Evil are decisive and no loop occurs.

## Test Questions

- Does the reraise mechanic define the fight while PD/Holy/Seal Evil remain decisive?
- Is the fight hard because of resource/action tax, not because enemies are unkillable?
- Is cleanup risk low enough once the player understands the permakill puzzle?
- Do all six enemies remain undead monsters in the real entry?
- Does Cursed Ring + Phoenix Down x2 pay through guaranteed spoils without touching monster equipment?
- Does it read as a drowned-dead lake that will not stay dead, not a human caster arena?

## Sources

- Game8, "Lake Poescas Walkthrough (Battle 41)": public-facing all-undead identity, reraise,
  Phoenix Down/Holy counterplay, 5/5 star rating, rewards.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553201
- Final Fantasy Wiki, "Poeskas Lake": story/terrain context.
  https://finalfantasy.fandom.com/wiki/Poeskas_Lake
- Local: `037-chapter-4-overview.md` (rules), `032-yuguewood.md` (Ch3 undead precedent),
  `chapter-4-rewards-implementation.md` (Cursed Ring + Phoenix Down spoils), local entd4 dump notes
  recorded above.
