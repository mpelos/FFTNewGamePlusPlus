# 046 - Lake Poescas (Poeskas Lake)

Status: 📝 redesign v3 planned (docs-only) — v1 implementation exists for entry 453
Chapter: 4 — "In the Name of Love"
Battle order: Battle 41 (after Mount Germinas)
Target version: Enhanced v1.5.0
ENTD: global entry **453** (local 69, `battle_entd4_ent.bin`)
File: `battle_entd4_ent.bin` (embedded NG+ swap) — `tools/battle_patch.py poeskas`

> **NG++ reward applied (2026-06-27):** Cursed Ring (s0), thematic to the undead battle; the two existing
> Phoenix Down spoils are kept. Guaranteed Spoils of War (ENTD `0x1e`), NG+ only, within the 3-item cap,
> no stealing required. Canonical map: `chapter-4-rewards-implementation.md`.

Current v1 implementation scales levels only:

```text
s0 undead Mystic (job 70)   L102
s1 undead Archer (job 63)   L101
s2 undead Archer (job 63)   L101
s3 undead Summoner (job 71) L102
s4 Revenant (job 114)       L103
s5 Revenant (job 114)       L102
```

Planned v3 redesign (docs-only in this pass): preserve the exact vanilla roster, but recognize the
four floating records correctly as **special human undead jobs**, not monsters. Give those four humans
complete Chapter-4 setups: a Mana-Shield Mystic with Geomancy, a Swiftspell Summoner with Black Magicks,
and two undead Archers with Items/Throw Items. The two Revenants remain equipment-less monsters and keep
their innate kits. The whole enemy side remains undead.

## Gate Answers / Constraints

```text
Scope: redesign battle doc 046 only; no ENTD, binary, table, script, or runtime implementation.
Allowed changes: job buckets, secondary commands, R/S/M, gear, Brave/Faith targets, levels, and
  positioning plan. Preserve the exact six-unit count and the original main-job identities except
  for assigning the agreed setup to the second undead Archer.
Chapter target: Chapter 4 broken-but-readable puzzle against tuned NG++ parties.
Vanilla identity: all-undead salt-lake permakill war; defeat all; no boss; no guest.
Success bar: complete v3 document setup, simulation rationale, implementation checklist, and playtest
  questions.
```

No active guests appear here. No guest-control implementation is needed.

## Critical ENTD Limitation: Learned Skills Are Random

ENTD can set the main job, secondary command, equipped reaction/support/movement, and the job bucket
whose level seeds the character. It **cannot allowlist the individual skills learned by an enemy**.

For this v3 design:

```text
- "Mime bucket L8", "Chemist bucket L8", and "Summoner bucket L8" are generation targets.
- Job Level 8 should produce a strong pool, but the exact learned skills remain random.
- The document specifies intended roles and legal complete setups; it does not promise that a specific
  generated unit will know one exact spell, summon, Aim tier, or Item.
- Simulation and playtest must evaluate the generated distribution, not a hand-picked skill list that
  ENTD cannot enforce.
```

## Design Goal

```text
Make Poeskas Lake the Chapter-4 all-undead 5-star field: six enemies return unless permanently finished,
the Mystic and Summoner supply reliable non-physical pressure into Shihadori-heavy parties, the two
Archers sustain the formation through ranged Items while maintaining crossfire, and the Revenants hunt
the player's backline. Phoenix Down, Holy, fire weakness, and Seal Evil must remain decisive answers.
The challenge is simultaneous threat control plus permakill discipline, not hard lockdown or raw levels.
```

## Original Battle

Objective:

```text
Defeat all enemies!
```

Player deployment:

```text
Up to 5 units, including Ramza. No guests.
```

Original/local composition:

```text
2x undead Archer
1x undead Mystic
1x undead Summoner
2x Revenant
ALL six enemies are undead.
```

Local ENTD interpretation:

```text
s0 job 70 = special undead Mystic; human record; innate Float + Undead.
s1 job 63 = special undead Archer; human record; innate Float + Undead.
s2 job 63 = special undead Archer; human record; innate Float + Undead.
s3 job 71 = special undead Summoner; human record; innate Float + Undead.
s4 job 114 = Revenant monster; innate Undead.
s5 job 114 = Revenant monster; innate Undead.
```

The four special jobs (`63`, `70`, `71`) use fixed/default equipment sentinels in vanilla, but they are
human-style jobs with legal equipment categories. Only the Revenants are true equipment-less monsters.

Public walkthrough details:

```text
Recommended level: ~59. Difficulty: 5/5 stars. Deploy up to 5.
All enemies are undead and may return instead of crystallizing.
Core answers: Phoenix Down, Holy damage, Seal Evil, and finishing undead bodies permanently.
Rewards: 30,400 Gil, Phoenix Down x2, buried treasure.
Terrain: dried salt lake with outcroppings, bridge/wooden sections, sand, and salt flats.
```

Design reading:

Poeskas is the campaign's dedicated **all-undead permakill battle**. Its six-body vanilla roster already
contains the correct tactical roles: ranged physical pressure, a Mystic disruptor, a Summoner AoE clock,
and two fast Revenant hunters. The v3 escalation is therefore not a roster replacement. It completes
the four human undead builds and lets their original jobs work together at Chapter-4 intensity while
keeping all six vulnerable to the intended anti-undead tools.

## Local Data Confirmed / Data Still Needed

```text
CONFIRMED:
- Entry 453 is Poeskas Lake.
- Exact active roster: job 70, job 63 x2, job 71, job 114 x2.
- Jobs 63/70/71 are unique human undead jobs with Float + Undead, not monsters.
- Job 63 legally equips bows, crossbows, shields, hats, clothes, and robes.
- Job 70 legally equips poles/books/staves/rods plus caster armor.
- Job 71 legally equips staves/rods plus caster armor.
- Revenant 114 is an equipment-less monster with its innate kit.
- No active guest and no boss.
- Reward ledger maps Cursed Ring + two Phoenix Downs to guaranteed spoils.

STILL NEEDED FOR V3 IMPLEMENTATION:
- Confirm that explicit ENTD gear and R/S/M fields are honored by special jobs 63/70/71 in battle.
- Confirm job-bucket encoding for Mime, Chemist, and Summoner on these special records.
- Confirm the generated Job Level 8 skill distributions are sufficiently threatening across test loads.
- Confirm Items + Throw Items AI behaves sensibly on an all-undead team and does not self-sabotage.
- Confirm Rubber Suit is legal and active on job 63 in TIC.
- Preserve Float + Undead on all four special human jobs.
- Preserve lake terrain, enemy placements, objective, and buried map treasure.
```

## Enemy Party Escalation (Chapter 4 Rule)

```text
CHANGE: no enemy-count increase and no removal of the vanilla castes. The four special human undead
  receive full v3 builds. Mystic becomes the durable Geomancy caster, Summoner becomes the main magical
  AoE clock, and both Archers gain ranged Item utility around their bow pressure.
WHY: a level-only six-undead band does not sufficiently pressure a tuned Chapter-4 party with Shihadori,
  Mana Shield, rare gear, mobility, and burst. The complete shell forces target priority while the
  reraise/permakill rule taxes actions.
CONSTRAINT: exact learned skills remain random from Job Level 8 buckets. Do not write or validate the
  design as though ENTD can guarantee a particular learned spell or Item.
REJECTED DEFAULTS: no third Revenant, no non-undead body, no hard-status engine, no dark-heal loop,
  no four-unit Mana Shield wall, and no 104+ overlevel spike.
WHAT IS NOT CHANGED: six enemies, all-undead identity, no boss, defeat-all objective, salt-lake terrain,
  and decisive Phoenix Down/Holy/Seal Evil counterplay.
```

## Sanctioned Exceptions

```text
UNDEAD RERAISE — the core mechanic. Every enemy demands a permanent finish.
SPECIAL HUMAN UNDEAD JOBS — jobs 63/70/71 retain Float + Undead while accepting full human gear/RSM.
ONE MANA SHIELD — allowed on the Mystic to resist opening burst. It is not paired with Manafont.
SUMMONER MANAFONT — allowed to sustain the offensive caster; its reaction is Reflexes, not Mana Shield,
  so there is no shield/font loop.
ITEMS + THROW ITEMS x2 — allowed as the Archer support identity. Exact available Items depend on the
  generated Chemist/Mime bucket skills and must be tested.
NO HARD-LOCK EXCEPTION — Petrify/Stop/Don't Act/Charm are not authored as the battle engine.
```

## Rare / Reward Handling

```text
Guaranteed spoils for entry 453: CURSED RING + PHOENIX DOWN + PHOENIX DOWN.
These are delivered through Spoils of War; no Steal is required.
Cursed Ring remains reward payload, not required active equipment.
Yoichi Bow already pays at Fort Besselat, so its active use here does not introduce a new reward tier.
Preserve all buried map treasure as vanilla map loot.
```

## Proposed Composition (New Game++ Poeskas Lake v3)

Keep the exact six-unit roster. Mystic, Summoner, and the stronger Archer sit at `102-103`; the second
Archer remains `101`; Revenants stay `103/102`. Difficulty comes from complete roles plus undead action
tax, not a boss band.

| Slot | Role | Main job | Job bucket | Level | Br/Fa | Purpose |
|---|---|---|---|---:|---:|---|
| `s0` | Undead Mystic | Undead Mystic `70` | Mime `L8` | `103` | `72/84` | Durable non-physical pressure; Geomancy + Mana Shield anchor. |
| `s1` | Undead Archer 1 | Undead Archer `63` | Mime `L8` | `102` | `88/70` | Mount-Germinas-style Yoichi crossfire plus ranged Items. |
| `s2` | Undead Archer 2 | Undead Archer `63` | Chemist `L8` | `101` | `88/70` | Durable Yoichi item-support Archer; Rubber Suit + cloak. |
| `s3` | Undead Summoner | Undead Summoner `71` | Summoner `L8` | `103` | `72/84` | Primary AoE clock; Summon + Black Magicks with Swiftspell. |
| `s4` | Revenant apex | Revenant `114` | innate monster kit | `103` | `90/55` | Mobile drain/flank anchor; top permakill body. |
| `s5` | Revenant hunter | Revenant `114` | innate monster kit | `102` | `88/55` | Second fast hunter on the opposite approach. |

## Builds

### s0 — Undead Mystic (Lv 103)

```text
Job: Undead Mystic (70)   Main JobLevel: 8
Job bucket: Mime   Bucket JobLevel: 8
Primary: Mystic Arts
Secondary: Geomancy
Reaction: Mana Shield
Support: Magick Boost / Magic Attack Boost
Movement: Movement +2

Right hand: Wizard's Rod
Left hand: none
Head: Lambent Hat
Body: Wizard's Robe
Accessory: Magepower Glove
```

Intuit: the durable magical anchor. Mystic Arts and Geomancy give the enemy side non-physical pressure,
while Mana Shield prevents a single opening finisher from deleting the role. It deliberately has no
Manafont: once its MP is exhausted, its burst protection is gone. Wizard's Robe + Magepower Glove makes
the build MA-focused rather than a high-HP stall body.

Random-skill note: Mime bucket `L8` seeds a strong generated ability pool; it does not guarantee one
specific learned Mystic/Geomancy action beyond what the generated character actually receives.

### s1 — Undead Archer 1 (Lv 102), copied from Mount Germinas

```text
Job: Undead Archer (63)   Main JobLevel: 8
Job bucket: Mime   Bucket JobLevel: 8
Primary: Aim
Secondary: Items
Reaction: Reflexes
Support: Throw Items
Movement: Jump +3

Right hand: Yoichi Bow
Left hand: none / two-handed marker
Head: Thief's Cap
Body: Power Garb
Accessory: Bracers
```

Intuit: copy the proven Mount Germinas Archer package into the undead roster. It maintains strong
high-ground Yoichi pressure while Items + Throw Items let it support fallen/damaged allies from range.
Float is innate to job 63; Jump +3 still preserves strong vertical reach if Float behavior differs on
specific lake tiles.

Random-skill note: the exact Items available depend on generated job knowledge. Throw Items is always
role-correct, but its practical value must be sampled across Job Level 8 generations.

### s2 — Undead Archer 2 (Lv 101), Chemist-bucket support Archer

```text
Job: Undead Archer (63)   Main JobLevel: 8
Job bucket: Chemist   Bucket JobLevel: 8
Primary: Aim
Secondary: Items
Reaction: Reflexes
Support: Throw Items
Movement: Movement +3

Right hand: Yoichi Bow
Left hand: none / two-handed marker
Head: Thief's Cap
Body: Rubber Suit
Accessory: Featherweave Cloak
```

Intuit: the defensive ranged support body. It remains the real undead Archer job, preserving Float +
Undead, but its Chemist bucket reinforces the Items secondary. Rubber Suit and Featherweave Cloak make
it harder to remove through common elemental/ranged pressure, while Movement +3 lets it reposition to
deliver Items or secure a new firing lane. It is intentionally the lower-level Archer (`101`).

Random-skill note: Chemist `L8` raises the quality/breadth of the generated Item knowledge; it cannot
guarantee an exact consumable list through ENTD.

### s3 — Undead Summoner (Lv 103)

```text
Job: Undead Summoner (71)   Main JobLevel: 8
Job bucket: Summoner   Bucket JobLevel: 8
Primary: Summon
Secondary: Black Magicks
Reaction: Reflexes
Support: Swiftspell
Movement: Manafont

Right hand: Wizard's Rod
Left hand: none
Head: Lambent Hat
Body: Black Robe
Accessory: Magepower Glove
```

Intuit: the priority AoE clock. Swiftspell accelerates whatever Summon/Black Magicks the generated unit
knows; Black Robe and Magepower Glove turn elemental casts into real Chapter-4 damage. Manafont sustains
the offensive MP budget, but Reflexes replaces Mana Shield so movement never creates an indefinite
defensive loop. The player can still rush, Silence, drain, or permanently finish this unit.

Random-skill note: Summoner bucket `L8` improves the generated Summon knowledge but cannot guarantee an
exact summon list. Test several generation seeds rather than validating only one favorable load.

### s4/s5 — Revenants (Lv 103 / 102)

```text
Job: Revenant (114)
Equipment: none
Secondary / R/S/M: innate monster behavior only
Preserve: Undead, Ectoplasm, Drain Touch, Counter, Teleport, Move 5 / Jump 4, Dark absorption,
  Holy and Fire weakness.
```

Intuit: fast hunters and permakill anchors. The `103` Revenant pressures the more direct lane; the `102`
Revenant takes the opposite approach so one choke or AoE does not solve both. Their percentage-based
Drain Touch and high mobility remain relevant against optimized high-HP builds without adding equipment
or a second authored engine.

## Positioning Plan

```text
- Place s4/s5 Revenants on different forward approaches. They should threaten the backline without both
  reaching the same player unit before a reasonable first response.
- Place s0 Mystic and s3 Summoner on opposite mid/back lanes. A single dive or AoE must not remove both.
- Put s1 Archer on the stronger elevated Yoichi firing lane.
- Put s2 support Archer on the alternate flank, close enough to throw Items across the formation but not
  adjacent to the Summoner.
- Spread downed-body locations so permanent finishing requires real movement/target priority.
- Do not create unreachable Float pockets or force cleanup after the tactical battle is already won.
- Preserve every original map tile, buried treasure tile, and the defeat-all objective.
```

The lake should say: "the dead have formed a complete firing line — silence the summoner, break the
support network, and finish every corpse before the salt flats fill with them again."

## Simulation Plan and Results

Simulation artifact:

```text
tmp/fft-level-design-046-poeskas-lake-v3/
  assumptions.md
  simulate.py
  iteration-results.md
```

Model scope:

```text
Coarse deterministic role-pressure model for a tuned NG++ party. It scores pressure, anti-meta coverage,
identity, answerability, opening-burst resilience, cleanup risk, and hard-lock risk. It does not model
exact FFT formulas or guarantee randomly learned job-bucket skills.
```

Result summary:

| Candidate | Pressure | Anti-meta | Identity | Answer | Burst resilience | Cleanup | Hard lock | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| v2 level-only reading | 218 | 28 | 100 | 92 | 50 | 18 | 0 | Rejected: too weak for optimized builds |
| Mana Shield on all four humans | 280 | 96 | 100 | 48 | 102 | 70 | 0 | Rejected: reraise/shield slog |
| **Agreed v3 mixed undead shell** | **271** | **81** | **100** | **87** | **72** | **24** | **0** | **Accepted** |
| Agreed shell without Mystic Mana Shield | 264 | 76 | 100 | 92 | 62 | 18 | 0 | Rejected: opening burst too effective |
| Third Revenant attrition | 286 | 81 | 82 | 87 | 72 | 36 | 0 | Rejected: wrong roster/cleanup |
| Hard-status graveyard | 271 | 81 | 75 | 59 | 72 | 24 | 55 | Rejected: wrong engine |

Iteration decision:

```text
ACCEPT the agreed v3 mixed undead shell for documentation.
The first draft overused Mana Shield and created an undead cleanup slog. The final v3 keeps exactly one
Mana Shield on the Mystic, places Manafont only on the non-shielded Summoner, and uses two Items/Throw
Items Archers to make the enemy formation resilient through action economy rather than invulnerability.
```

## Implementation Checklist

- [ ] Confirm entry 453 active slot order: `70,63,63,71,114,114`.
- [ ] Preserve Float + Undead on jobs 63/70/71 and Undead on both Revenants.
- [ ] Set levels: Mystic `103`, Archer 1 `102`, Archer 2 `101`, Summoner `103`, Revenants `103/102`.
- [ ] Set main JobLevel `8` for all four human undead; preserve monster-job handling on Revenants.
- [ ] Seed buckets: Mystic→Mime `L8`, Archer 1→Mime `L8`, Archer 2→Chemist `L8`, Summoner→Summoner `L8`.
- [ ] Apply the exact secondary/R/S/M and equipment packages documented above.
- [ ] Confirm special jobs 63/70/71 honor explicit ENTD gear and R/S/M fields.
- [ ] Do not implement a per-unit learned-skill allowlist; ENTD cannot provide it.
- [ ] Sample multiple generated enemies/saves to validate the random Job Level 8 skill distribution.
- [ ] Confirm Items + Throw Items AI helps the team and does not misuse Phoenix Down or restorative
      items against undead allies.
- [ ] Preserve both Revenant innate kits; do not assign human gear or job buckets to them.
- [ ] Preserve guaranteed spoils: Cursed Ring + Phoenix Down + Phoenix Down.
- [ ] Preserve buried map treasure and all original terrain/objective behavior.
- [ ] Re-dump and diff; keep all data changes inside entry 453 or the narrowly required special-job layer.
- [ ] Run the sprite-budget audit if any visual/main-job change becomes necessary during implementation.
- [ ] Test from a New Game+ save against physical/Shihadori, Mana Shield, magic, Holy/PD, and burst teams.

## Test Questions

- Do all six enemies remain undead and reraising until permanently finished?
- Are Phoenix Down, Holy, fire weakness, and Seal Evil still decisive rather than invalidated by gear?
- Does the Mystic survive one opening burst through Mana Shield without becoming a Manafont loop?
- Does the Summoner create a real Swiftspell AoE clock while remaining rushable/Silenceable?
- Do Geomancy, Summon, and Black Magicks provide enough non-physical pressure into Shihadori-heavy teams?
- Do both Archers actually receive useful Item knowledge often enough from their level-8 generation?
- Does Items + Throw Items AI behave correctly with undead allies?
- Does the Rubber Suit/Featherweave Archer feel durable without becoming the real boss?
- Are the two Yoichi Archers threatening while still answerable by magic, positioning, and focused burst?
- Do the Revenants reach separate lanes and remain meaningful against high-HP endgame units?
- Does the spread create permakill discipline without an unreachable-body cleanup slog?
- Does Cursed Ring + two Phoenix Downs pay through guaranteed spoils?
- Does the battle still read as Poeskas Lake: a 5-star all-undead field immediately before Limberry?

## Sources

- Final Fantasy Wiki, "Lake Poescas": original roster (2 Archer, Mystic, Summoner, 2 Revenant), all-undead
  rule, objective, terrain, and the unusual robe-equipped undead Archers.
  https://finalfantasy.fandom.com/wiki/Lake_Poescas
- Final Fantasy Wiki, "Ghost (Tactics)": Revenant movement/evasion, Ectoplasm, Drain Touch, Counter,
  Teleport, weaknesses, and innate monster behavior.
  https://finalfantasy.fandom.com/wiki/Ghost_(Tactics)
- Local: `037-chapter-4-overview.md`, `045-mount-germinas.md`,
  `chapter-4-rewards-implementation.md`, `docs/modding/01-entd-binary-format.md`, current entry-453 dump,
  upstream modloader `JobData.xml`, and `tmp/fft-level-design-046-poeskas-lake-v3/`.
