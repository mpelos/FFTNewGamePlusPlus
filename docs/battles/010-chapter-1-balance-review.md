# 010 - Chapter 1 Balance Review

A cross-battle audit of all **10** Chapter 1 New Game++ designs (`001`–`009`). It checks the
difficulty curve, verifies consistency of level bands / gear / job-skill IDs, logs the
deliberate design exceptions, flags the open risks, and gives a recommended playtest order.
This is a paper review — every finding must be re-validated in-game once each battle is patched
on the Windows data.

## The central balancing insight

Because every enemy is scaled with `Level = 100 + offset` (party level + offset), **the level
offset is NOT the main difficulty lever**. A level-100 unit and a level-102 unit are both
"around the player's level." Difficulty comes from four things instead:

```text
1. Enemy count and action economy (how many threats act per round).
2. Composition complexity (melee -> + ranged -> + magic -> + control -> + boss/break).
3. Terrain (open field -> woods -> rooftops -> corridors -> fortress).
4. Special mechanics (escort, Self-Destruct, elevation, chokepoints, healers, control, break, boss kill).
```

So the curve is carried by **composition + terrain + mechanics**, with level offsets (100–103)
as fine tuning only — and the three named bosses (Milleuda, Wiegraf, Argath) as the spikes.

## Difficulty curve (all 10 battles, as designed)

| # | Battle | Doc | Enemies | New demand introduced | Terrain | Tier |
|---|--------|-----|---------|-----------------------|---------|------|
| 1 | Orbonne | — | (tutorial) | — | monastery | (out of scope) |
| 2 | Gariland | `001` | 6 (4 Squire-line + Archer + Thief) | baseline melee + 1 ranged | street | ▁ warm-up |
| 3 | Mandalia | `002` | 6 (3 Squire + Thief + Archer + Red Panther) | escort + first beast | open plain | ▂ light |
| 4 | Siedge Weald | `003` | 7 monsters | all-monster swarm + Self-Destruct + elements | woods | ▃ moderate |
| 5 | Dorter | `004` | 6 (Knight + 3 Archer + 2 Black Mage) | **spike**: elevation + ranged + magic | rooftops | ▅ hard |
| 6 | Sand Rat | `005` | 6 (3 Knight + Archer + 2 Monk) | split party + melee chokepoint attrition | corridors | ▅ hard |
| 7 | Brigands' Den | `006` | 7 (Milleuda boss + Knight + 2 White Mage + 3 Thief) | **first named boss** + healers + rain | rainy den | ▅+ hard |
| 8 | Lenalian | `007` | 7 (Milleuda boss + 3 Knight + 2 Black Mage + Time Mage) | boss rematch + stacked magic + **first control** | field | ▆ harder |
| 9 | Fovoham | `008` | 5 (Wiegraf boss + Knight + 2 Monk + Chocobo) | **sword-skill boss spike** + bruisers | windflats | ▇ very hard |
| 10 | Ziekden | `009` | 6 (Argath boss + 3 Knight + 2 Black Mage) | **finale**: boss + gear-break + magic + split | fortress | ▇ finale |

Reading: the front half (2–6) teaches one tactic at a time (ranged → beast+escort → swarm →
the rooftop spike → split attrition). The back half (7–10) is a **four-boss escalation** that
never repeats the same boss archetype:

```text
Brigands' Den : a brawler boss kept alive by HEALERS        (kill the healers / reach her)
Lenalian      : a boss behind STACKED MAGIC + tempo control (spacing + manage Slow)
Fovoham       : a ranged SWORD-SKILL boss + bruisers        (break the blade / clear Monks)
Ziekden       : a durable boss + GEAR-BREAK + magic + split (Safeguard / two-front assault)
```

### Curve verdict

```text
PASS (on paper). Monotonic in "number of distinct demands," the right axis for a scale-to-party
mod. Dorter and Sand Rat sit intentionally close (both "hard", different flavors). The back-half
bosses each pose a different problem, so the four-in-a-row does not feel repetitive on paper.
Watch-item: confirm in play that the boss back half doesn't cause fatigue (see risks).
```

## Level bands & boss policy

```text
Generic enemies: 100-102 (most 100-101; captains/anchors 102).
Bosses:  Milleuda 102 (+2, both appearances)  |  Wiegraf 103 (+3)  |  Argath 103 (+3).
No generic exceeds +2; only Wiegraf and Argath reach +3 (the two pre-finale/finale spikes).

Boss-loot policy (Chapter 1): ALL three bosses use STRONG but NON-UNIQUE shop-tier gear.
Rare, non-buyable boss items begin in CHAPTER 2 by campaign design; the best gear is reserved
for the final chapter. This keeps Chapter 1's reward curve flat and makes the Ch2 rare drops
land harder.
```

## Design-exception log

Two chapter-wide rules are deliberately broken in specific fights, because the original battles
are built around those mechanics. Both are constrained to stay fair at NG+ scale:

| Exception | Where | Why | Guardrail |
|-----------|-------|-----|-----------|
| Time Mage control | Lenalian (`007`) | The original fight contains a Time Mage; tempo control is the point | Haste/Slow/Float only — **no** Stop/Immobilize/Don't Move/Don't Act; one Time Mage only |
| Equipment break | Fovoham (`008`), Ziekden (`009`) | Wiegraf's power is his (breakable) sword skill; Ziekden's Knights have canonical Rend + telegraphed Safeguard | Fovoham: keep Wiegraf's blade breakable (Rend-Weapon = the counter). Ziekden: Rend on only 2/3 Knights; shop-tier gear only; boss does not spam break |

Break is banned in every other Chapter 1 fight; control (Stop-tier) is banned everywhere.

## Consistency audit

### Job IDs

```text
Confirmed & reused identically: Squire 74, Chemist 75, Archer 77, Thief 83.
TBD (verify on Windows, used by name): Knight, Monk, White Mage, Black Mage, Time Mage,
  the monster jobs (Red Panther, Goblin, Black Goblin, Bomb, Chocobo), and the three named
  boss jobs (Milleuda, Wiegraf, Argath).
New jobs introduced during Chapter 1 (first appearances — verify carefully):
  White Mage (Brigands' Den), Time Mage (Lenalian), Chocobo (Fovoham).
```

### Equipment & skill IDs

```text
Reused without conflict across all docs: Thief's Cap 168, Black Garb 198, Power Garb 195,
  Headband 163, Bracers 218, Germinas Boots 210, Featherweave Cloak 234, Runeblade 30,
  Icebrand 29, Windslash Bow 87, Air Knife 9, Mythril Gun 72.
Skills reused: Counter 442, Attack Boost 465, Movement +1 486, Movement +2 487,
  Concentration 469, Reflexes 449, First Strike 453, Auto-Potion 441, Throw Items 474,
  Fundaments 5 (standardized — the id-5 Squire skillset is called "Fundaments" everywhere,
  fix originally applied to the Ziekden doc).
Knight/mage shop gear (heavy helm/armor/shield, robe, rod, staff) is referenced by tier and
  left TBD until mapped in ItemData.xml — consistent across 004-009. No conflicts.
```

### Level bands & boss kits

```text
Consistent. Milleuda's Lenalian kit is intentionally a touch stronger than her Brigands' Den
kit (harder rematch) but both stay +2 / non-unique. Wiegraf and Argath both +3 / non-unique,
each with a focus-fire reaction and a signature threat (Judgment Blade / presence + break).
```

## Open risks / watch-items for playtest

1. **Gariland may be over-tuned for a "warm-up"** (`001`). Established, in-game-tested baseline;
   if the opening feels punishing, soften it first (drop a skill, not a level).
2. **Scale-to-party compresses the curve.** Confirm Gariland/Mandalia still feel clearly easier
   than the Dorter spike and the boss back half in practice, not just on paper.
3. **Monster fights are hard to fine-tune** (Siedge Weald `003`; the Chocobo in Fovoham `008`).
   Use the docs' softer/harder notes rather than adding archetypes.
4. **Dorter ≈ Sand Rat** — confirm the *type* of hard differs (ranged/vertical vs melee/attrition).
5. **Boss back-half fatigue** (`006`–`009`, four boss fights in a row). Each is a distinct
   archetype by design; verify in play they don't blur together or overstay.
6. **Time Mage Slow on an endgame party** (`007`) — verify it's annoying, not oppressive (no
   hard lock per the exception log).
7. **Wiegraf's Judgment Blade scaling** (`008`) — verify it's scary but Rend-Weapon truly
   neutralizes it and it doesn't one-shot.
8. **Ziekden break exception** (`009`) — verify Safeguard makes it fair; if cheap, drop to 1
   Render-Knight.
9. **Boss-scripting integrity for all three named bosses** — Milleuda's death cutscene
   (`007`), Wiegraf's auto-retreat at low HP (`008`), Argath + the Tietra hostage sequence
   (`009`). Highest-risk patches; diff-check and test objective/retreat triggers.

## Recommended implementation & playtest order

Implement in story order so the curve can be felt as a player would:

```text
002 Mandalia -> 003 Siedge Weald -> 004 Dorter -> 005 Sand Rat ->
006 Brigands' Den -> 007 Lenalian -> 008 Fovoham -> 009 Ziekden
```

(`001` Gariland is already implemented/tested and serves as the baseline reference.)

For each: dump the real entry, fill the doc's "Local Data Confirmed", patch, diff-check inside
the battle window only, then test from a New Game+ save and record results back in the doc.

## Status

```text
Design phase: COMPLETE for all 10 Chapter 1 battles (001 implemented; 002-009 designed).
Consistency: audited; one skill-name fix (Fundaments) carried; exceptions logged.
Curve: passes on paper; risk items above to confirm in-game.
Boss-loot: all Ch1 bosses non-unique — sets up the Chapter 2 rare-item escalation.
Next: data-layer patching + playtest in order; then Chapter 2 (see Chapter 2 overview).
```

## Sources

- Local design docs: `000-chapter-1-overview.md`, `001-gariland.md` … `009-ziekden-fortress.md`.
- Original-battle rosters cross-referenced from Game8 Chapter 1 battle walkthroughs
  (see each battle doc's Sources section).
</content>
