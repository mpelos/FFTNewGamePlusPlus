# 030 - Grogh Heights (Grog Hill)

Status: designed (not yet implemented)
Chapter: 3 — "The Valiant"
Battle order: Battle 27 (after the Monastery Vaults chain)
Target version: Enhanced v1.5.0
ENTD: global entry **TBD** — confirm on Windows game data
File: `battle_entd*_ent.bin` (TBD) / `OverrideEntryData` rows (TBD)

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
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm slots: 2 Squire + 2 Chemist + 1 Archer + 1 Thief, plus the player slots.
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
Black Mage job id      (TBD - verify; one added below — rain-Thunder caster)
```

## Job Escalation (Chapter 3 rule)

```text
CHANGE: swap ONE Squire -> a Black Mage that casts rain-boosted THUNDER (and clusters with the band).
WHY: the original's lesson is "the PLAYER punishes the cluster with Thunder/line-AoE." The single,
  fitting escalation is to make the WEATHER CUT BOTH WAYS — an enemy rain-Thunder caster means the
  player must also respect the rain (don't clump into enemy Thunder) while still wanting to lightning
  the enemy rows. It RAISES the existing puzzle (weather + clustering) without changing it, and it is
  NOT a brand-new caste (Black Mage is long-established), so the fight stays a light breather.
WHAT IS NOT CHANGED: the weak, numerous, clumping band and the rain/cluster/Thunder identity remain.
  No brand-new Ch3 caste here — Ninja, Oracle, and Velius debut in their own fights.
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

## Proposed Composition (New Game++ Grogh Heights v1)

Keep the count (6) and the LIGHT feel; swap one Squire for a rain-Thunder Black Mage. Modest
levels — this is a breather. Black Mage `101`; everyone else `100`–`101`.

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
the enemy's boosted Thunder. Modest levels (mostly `100`–`101`, no `102` anchor) keep it a genuine
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
Job: Black Mage (id TBD)   JobLevel: 8   Secondary: none
Lean into THUNDER (rain-boosted). Keep normal cast cadence (race-able).
Reaction: Reflexes (449)   Support: MA/Magick-boost (id TBD)   Movement: Movement +1 (486)
Head: cloth/mage hat (id TBD)   Body: shop robe (id TBD)
Accessory: Featherweave Cloak (234)   Right hand: shop magic-boost rod (id TBD)   Left: none (255)
```

Role: the two-way weather threat — punishes the player for clumping, as the player punishes the band.

### Squire (Lv 100)

```text
Job: Squire (74)   JobLevel: 8   Primary: Fundaments (5)
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head: shop hat (id TBD)   Body: shop clothes (id TBD)   Accessory: Bracers (218)
Right hand: shop sword (id TBD)   Left: shop shield (id TBD)
```

Role: a weak body that fills out the cluster.

### Chemist x2 (Lv 101 / 100) — sustain

```text
Job: Chemist (75)   JobLevel: 8   Primary: Item (Potion / Hi-Potion / Antidote)
Reaction: Auto-Potion (441)   Support: Throw Items (474)   Movement: Movement +1 (486)
Head: shop hat (id TBD)   Body: shop clothes (id TBD)   Accessory: Bracers (218)
Right hand: shop gun/knife (id TBD)   Left: none
```

Role: light heal sustain — not enough to make the fight a grind.

### Archer (Lv 101)

```text
Job: Archer (77)   JobLevel: 8   Secondary: none
Reaction: Reflexes (449)   Support: Concentration (469)   Movement: Movement +1 (486)
Head: Thief's Cap (168)   Body: Black Garb (198)   Accessory: Bracers (218)
Right hand: Windslash Bow (87)   Left: none / two-hand marker (254)
```

Role: ranged chip; clusters with the band.

### Thief (Lv 100) — harass

```text
Job: Thief (83)   JobLevel: 8   Secondary: Steal (incl. Steal Heart)
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

## Implementation Checklist

- [ ] Identify Grogh Heights `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify 2 Squire + 2 Chemist + 1 Archer + 1 Thief + player slots.
- [ ] Swap ONE Squire -> Black Mage; lean it into Thunder (rain-boosted), normal cast cadence.
- [ ] Keep the RAIN flag + tight clustering geometry; do NOT over-scale (breather).
- [ ] Set levels: Black Mage + a Chemist + Archer `101`; Squire + second Chemist + Thief `100`.
- [ ] Set JobLevel `8` on all active enemy slots; keep Steal/charm on the one Thief.
- [ ] Patch via the correct layer; keep the diff inside the Grogh Heights window only.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify rain + clustering intact.
- [ ] Install mod, test from a New Game+ save; confirm it plays as a light Thunder/AoE breather.

## Test Questions

- Do the enemies still clump into rows that reward Thunder / line-AoE (the original's appeal)?
- Does the rain-Thunder Black Mage make the weather a two-way threat without raising lethality much?
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
- Local: `docs/battles/024-chapter-3-overview.md` (job-escalation + rare-loot rules),
  `006-brigands-den.md` & `019-balias-swale.md` (rain-Thunder motif), `004-dorter-slums.md`
  (Black Mage build).
</content>
