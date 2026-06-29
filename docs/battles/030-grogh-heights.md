# 030 - Grogh Heights (Grog Hill)

Status: ✅ implemented (v1, entry 426) — NG+ only; pending playtest. **v2 redesign documented only** (implementation pending).
Chapter: 3 — "The Valiant"
Battle order: Battle 27 (after the Monastery Vaults chain)
Target version: Enhanced v1.5.0
ENTD: global entry **426** (local entry 42, `battle_entd4_ent.bin`)
File: `battle_entd4_ent.bin` (embedded NG+ swap) — `tools/battle_patch.py grogh`

Implemented composition (entry 426, vanilla-dump verified) — kept LIGHT (breather):
- s0 Squire→**Black Mage** L101 (NEW rain-Thunder caster) — Mage Hat/shop Robe/Featherweave/shop Rod; Reflexes/Atk Boost/Mv+1.
- s2 Squire L100 — Headband/Power Garb/Bracers/Icebrand; Counter/Atk Boost/Mv+1.
- s1,s3 Chemist L101/L100 — Mage Hat/Black Garb/Bracers/Mythril Gun (two-hand); Auto-Potion/Throw Items/Mv+1.
- s4 Archer L101 — Thief's Cap/Black Garb/Bracers/Windslash (two-hand); Reflexes/Concentration/Mv+1.
- s5 Thief L100 — Thief's Cap/Black Garb/Germinas/Air Knife; First Strike/Atk Boost/Mv+2 (Steal innate).
- s6 (Orran placeholder), s7, s8 = inactive (level 0xFE) — left untouched. No boss → no rare. Modest levels preserve the curve dip.

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `024-chapter-3-overview.md`.

## Original Battle

Objective:

```text
Defeat all enemies!
```

Player deployment:

```text
Up to 5 units, including Ramza. No guests.
```

Original enemy composition:

```text
2x Squire    (weak generic bodies)
2x Chemist   (minor sustain)
1x Archer    (ranged)
1x Thief     (steal / charm harass)
```

Public walkthrough details:

```text
Recommended level: ~31.  Difficulty: 2/5 stars.
TIGHT, RAINY map: space is cramped, the enemies are many and weak, and the rain BOOSTS Thunder.
The enemies CLUSTER in rows because the map is tight — perfect for LIGHTNING magic and LINE attacks
  (Divine Ruination, Shockwave) that catch several foes at once.
A deliberately light fight — a tactical breather, won by exploiting weather + clustering.
```

Design reading:

Grogh Heights is **the rainy breather** — a low-lethality, high-tempo fight whose whole identity is
**weather + clustering**: a tight map forces a weak, numerous band into rows, the rain amplifies
Thunder, and the player is rewarded for **line/AoE and lightning** that sweep the cluster. After the
heavy Orbonne Vault chain, it deliberately lowers intensity (weak Squires/Chemists, 2/5★) and asks
a single clean question: *can you punish a clump?* It reprises the rain-Thunder motif from Brigands'
Den (`006`) and Balias Swale (`019`), but here as a light, satisfying AoE playground rather than a
boss fight.

For New Game++ the identity must stay: **a tight rainy skirmish where a weak, numerous band clumps
into rows and the rain rewards Thunder/line-AoE — a deliberate breather, kept light, with the only
new twist being that the weather now cuts both ways.**

## Local Data Confirmed

```text
ENTD entry 426 confirmed in `024-chapter-3-overview.md` and v1 implementation.
Original roster: 2 Squire + 2 Chemist + 1 Archer + 1 Thief, plus the player slots.
v1/v2 active roster: 1 Squire is swapped to Black Mage; keep 1 Squire + 2 Chemist + 1 Archer +
  1 Thief. s6 Orran placeholder and s7/s8 inactive placeholders stay inactive.
Keep the RAIN weather flag (Thunder boost) and the tight-map clustering geometry — these ARE the fight.
This is a BREATHER: do not over-scale it (no boss, modest levels), to preserve the curve after the
  Vault chain.
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
```

Job IDs (carry over known, verify the rest in-game):

```text
74 = Squire            (confirmed)
75 = Chemist           (confirmed)
77 = Archer            (confirmed)
83 = Thief             (confirmed)
Black Mage job id      (TBD - verify; one Squire slot is swapped to this rain-Thunder caster)
```

## Enemy Party Escalation (Chapter 3 redesign)

```text
VANILLA SPIRIT: a rainy, cramped breather where weak enemies clump into rows and the player is
  rewarded for Thunder/line-AoE.
CHAPTER-3 UPGRADE: keep the six-enemy light band and the one-Squire -> Black Mage swap, but complete
  every active human setup with secondary/reaction/support/movement. The party becomes a soft
  weather cell: one Black Mage punishes player clumps, Chemists add light sustain, Archer/Thief chip
  and harass, and the remaining Squire keeps the "weak bodies in rows" feel.
WHY: the single fitting escalation is to make the weather cut both ways. A second Black Mage,
  elite job, or heavy charm package would erase the deliberate post-Vaults curve dip.
WHAT IS NOT CHANGED: the enemies still clump, Thunder/line-AoE is still the player's satisfying
  answer, and the battle remains a 2/5★ breather.
```

Chapter 3 requirements applied:

```text
- Every active human enemy has full equipment.
- Every active human enemy has secondary, reaction, support, and movement.
- The party has light synergy: rain-Thunder caster + modest sustain + ranged/charm harass.
- No guests are present.
- No extra caster, no elite job, no heavy charm/status stack.
```

## Sanctioned exceptions (carried precedents)

```text
CHARM/STEAL (Thief) — allowed, minor (Ch2/Gollund precedent): the one Thief may Steal/charm; it is a
  light harass, counterable, not run-ending. No hard lock anywhere.
RAIN-THUNDER — a weather mechanic, not a status; allowed on the added Black Mage as the two-way
  escalation (Brigands' Den 006 / Balias Swale 019 motif). Keep cast cadence normal (race-able).
```

## Boss rare loot

```text
None. No named boss here — no rare boss item (per the Chapter 3 overview). Generics stay shop-tier.
(The map's rare TREASURE — Kunai / Main Gauche / Ame-no-Murakumo / Sleep Blade — is existing map
treasure, not boss loot; leave it as-is.)
```

## Proposed Composition (New Game++ Grogh Heights v2)

Keep the count (6) and the LIGHT feel; swap one Squire for a rain-Thunder Black Mage. Modest
levels — this is a breather. Black Mage `101`; everyone else `100`–`101`. The v2 change is kit
completeness, not new lethality.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Black Mage (NEW) | Black Mage | `101` | Rain-boosted Thunder — the weather now threatens the player too. |
| n | Squire | Squire | `100` | Weak body; clumps in the rows. |
| n | Chemist | Chemist | `101` | Minor heal sustain. |
| n | Chemist | Chemist | `100` | Second medic; light sustain. |
| n | Archer | Archer | `101` | Ranged chip; part of the cluster. |
| n | Thief | Thief | `100` | Fast steal/charm harass. |

Reasoning:

The faithful move is to **keep it light and lean entirely into the weather-and-cluster puzzle**.
The band stays weak and numerous so it clumps into rows the player can sweep with Thunder/line-AoE —
the original's whole appeal. The single escalation, a rain-Thunder Black Mage, makes the rain a
two-way street: the player still wants to lightning the cluster, but must now avoid clumping into
the enemy's boosted Thunder. Complete setups make the units behave like Chapter 3 enemies without
turning them into a real wall. Modest levels (mostly `100`–`101`, no `102` anchor) keep it a genuine
2/5★ breather — a deliberate dip in the curve between the Vault chain and the Yardow/Riovanes climb.

## Builds (final-shop quality; hill deserter band flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Black Mage (Lv 101) — NEW (rain-Thunder)

```text
Job: Black Mage (id TBD)   JobLevel: 8   Primary: Black Magic
Secondary: Item or low-tier White Magic if legal; no Time Magic / no hard control
Lean into THUNDER (rain-boosted). Keep normal cast cadence (race-able).
Reaction: Reflexes (449)   Support: MA/Magick-boost (id TBD)   Movement: Movement +1 (486)
Head: cloth/mage hat (id TBD)   Body: shop robe (id TBD)
Accessory: Featherweave Cloak (234)   Right hand: shop magic-boost rod (id TBD)   Left: none (255)
```

Role: the two-way weather threat — punishes the player for clumping, as the player punishes the band.

### Squire (Lv 100)

```text
Job: Squire (74)   JobLevel: 8   Primary: Fundaments (5)
Secondary: Item or basic support equivalent; no status package
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head: shop hat (id TBD)   Body: shop clothes (id TBD)   Accessory: Bracers (218)
Right hand: shop sword (id TBD)   Left: shop shield (id TBD)
```

Role: a weak body that fills out the cluster.

### Chemist x2 (Lv 101 / 100) — sustain

```text
Job: Chemist (75)   JobLevel: 8   Primary: Item (Potion / Hi-Potion / Antidote)
Secondary: Fundaments / Steal-lite equivalent if legal; no status package
Reaction: Auto-Potion (441)   Support: Throw Items (474)   Movement: Movement +1 (486)
Head: shop hat (id TBD)   Body: shop clothes (id TBD)   Accessory: Bracers (218)
Right hand: shop gun/knife (id TBD)   Left: none
```

Role: light heal sustain — not enough to make the fight a grind.

### Archer (Lv 101)

```text
Job: Archer (77)   JobLevel: 8   Primary: Aim/Charge
Secondary: Item or Fundaments equivalent; no hard status
Reaction: Reflexes (449)   Support: Concentration (469)   Movement: Movement +1 (486)
Head: Thief's Cap (168)   Body: Black Garb (198)   Accessory: Bracers (218)
Right hand: Windslash Bow (87)   Left: none / two-hand marker (254)
```

Role: ranged chip; clusters with the band.

### Thief (Lv 100) — harass

```text
Job: Thief (83)   JobLevel: 8   Primary: Steal (incl. Steal Heart)
Secondary: Item or Fundaments equivalent; no second charm/status source
Reaction: First Strike (453)   Support: Attack Boost (465)   Movement: Movement +2 (487)
Head: Thief's Cap (168)   Body: Black Garb (198)   Accessory: Germinas Boots (210)
Right hand: Air Knife (9)   Left: none / two-hand marker (254)
```

Role: light steal/charm harass; fast but fragile.

## Positioning Plan

```text
The band starts grouped on the tight rainy heights, naturally forming ROWS the player can sweep
  with Thunder / line-AoE — preserve that clustering geometry.
The Black Mage starts mid/back with a sightline onto the player's likely cluster (the two-way rain
  threat); the Chemists support from behind; the Archer/Thief flank.
Preserve the RAIN flag and the tight-map layout.
```

The heights should say: "a soggy little ambush — sweep their rows with lightning, but mind you
don't bunch up under theirs."

## Simulation Plan and Results

Simulation artifact:

```text
tmp/fft-level-design-030-grogh-heights/
```

Model scope:

```text
First four rounds only; compares two-way weather pressure, clump reward, answerability, and whether
the fight still functions as a deliberate breather after the Vaults chain.
```

Iteration results:

| Candidate | Enemies | Action ratio | Weather pressure | Total pressure | Clump reward | Answerability | Breather score | Result |
|-----------|---------|--------------|------------------|----------------|--------------|---------------|----------------|--------|
| v1 light rain shell | 6 | 0.79 | 21.6 | 53.4 | 79.5 | 87.2 | 94.2 | Baseline |
| v2 complete rainy breather | 6 | 0.83 | 24.5 | 65.7 | 79.5 | 84.5 | 90.3 | Accepted |
| Second Black Mage storm | 7 | 0.96 | 51.8 | 93.1 | 73.0 | 77.8 | 78.3 | Rejected: extra rain caster |
| Double-Thief charm rain | 7 | 0.96 | 24.5 | 96.7 | 70.5 | 58.8 | 60.7 | Rejected: charm/status stack |
| Dragoon weather flanker | 6 | 0.83 | 24.5 | 86.0 | 59.5 | 66.0 | 66.2 | Rejected: elite job / diluted AoE reward |

Decision:

```text
Use the complete six-enemy rainy breather. Keep one Black Mage as the two-way rain-Thunder threat,
complete the setups with soft secondaries, and reject extra casters, charm stacking, or elite jobs
so the post-Vaults curve dip stays intact.
```

## Current Implementation (v1, entry 426 — superseded by v2 design)

The shipped v1 already establishes the rain-Thunder Black Mage swap while keeping Grogh light.
The v2 redesign above is **documentation only** in this pass; it requires a later implementation
pass to add mandatory secondary setups and verify the fight still plays as a breather.

## Future Implementation Checklist (v2)

- [x] Identify Grogh Heights ENTD entry 426; fill "Local Data Confirmed".
- [x] Dump original entry; verify 2 Squire + 2 Chemist + 1 Archer + 1 Thief + player slots.
- [ ] Swap ONE Squire -> Black Mage; lean it into Thunder (rain-boosted), normal cast cadence.
- [ ] Keep the RAIN flag + tight clustering geometry; do NOT over-scale (breather).
- [ ] Set levels: Black Mage + a Chemist + Archer `101`; Squire + second Chemist + Thief `100`.
- [ ] Set JobLevel `8` on all active enemy slots; keep Steal/charm on the one Thief.
- [ ] Give every active human enemy full equipment plus secondary/reaction/support/movement.
- [ ] Preserve breather calibration: no extra Black Mage, no elite job, no second charm/status source.
- [ ] Patch via the correct layer in a later implementation pass; no binary/data change in this doc pass.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify rain + clustering intact.
- [ ] Install mod, test from a New Game+ save; confirm it plays as a light Thunder/AoE breather.

## Test Questions

- Do the enemies still clump into rows that reward Thunder / line-AoE (the original's appeal)?
- Does the rain-Thunder Black Mage make the weather a two-way threat without raising lethality much?
- Do the complete setups still feel like a light enemy band rather than a serious wall?
- Is it clearly a LIGHTER fight (2/5★) — a deliberate breather after the Vault chain?
- Is the one Thief's steal/charm a minor harass, not a swing factor?
- Are levels kept modest so the curve dips here before Yardow/Riovanes?
- Does it still read as a soggy hillside ambush, not a designed arena?

## Sources

- Game8, "Grogh Heights Walkthrough (Battle 27)": roster (2 Squire, 2 Chemist, 1 Archer, 1 Thief),
  objective "Defeat all enemies!", recommended level ~31, 2/5 stars, deploy 5, tight rainy map with
  enemies clustering in rows, rain-boosted Thunder + line attacks recommended, rewards/treasure.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553187
- Final Fantasy Wiki, "Grog Hill": story/terrain context.
  https://finalfantasy.fandom.com/wiki/Grog_Hill
- Local: `docs/battles/024-chapter-3-overview.md` (Chapter 3 complete-party + rare-loot rules),
  `006-brigands-den.md` & `019-balias-swale.md` (rain-Thunder motif), `004-dorter-slums.md`
  (Black Mage build).
