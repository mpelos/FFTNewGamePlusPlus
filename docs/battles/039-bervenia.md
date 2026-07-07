# 039 - Free City of Bervenia

Status: ✅ implemented (v3 adjusted, entry 443)
Chapter: 4 — "In the Name of Love"
Battle order: Battle 34 (after Dugeura Pass)
Target version: Enhanced v1.5.0
ENTD: global entry **443** (local entry 59, `battle_entd4_ent.bin`)
File: `battle_entd4_ent.bin` (embedded NG+ swap)

> **NG++ rewards applied:** Save the Queen + Jade Armlet + Remedy through guaranteed Spoils of War
> (`0x1e`), NG+ only, within the 3-item cap, no stealing required. Steal Weapon remains a tactical
> disarm answer, not the only reward path.

Implemented composition (entry 443, vanilla-dump verified):

- s0 **Meliadoul** (job 47 Divine Knight, boss, dies) — L104, JobLevel 8, Mighty Sword break kit,
  Save the Queen (34) as equipped threat/steal-bait, win-on-death scripting preserved.
- s1,s4 Summoner — L102.
- s2,s3 Archer — L102.
- s5 Monk — L102.

The v2 redesign keeps the exact six-body boss-duel shape, but upgrades the whole support screen to
complete Chapter 4 setups while preserving the key fairness point: only Meliadoul breaks equipment,
and she must remain stealable/disarmable.

The v3 redesign starts from the v2 composition baseline below and has been adjusted after playtest:
the Dancer soft-clock was removed, the second lane-pressure Archer restored, Meliadoul's Faith was
raised to make magic answers matter, and the Monk was softened from Shirahadori wall to Counter.

## Original Battle

Objective:

```text
Defeat Meliadoul! The mission ends the instant she falls, regardless of remaining enemies.
```

Player deployment:

```text
Up to 5 units, including Ramza. No guests.
```

Original enemy composition:

```text
1x Meliadoul Tengille  (boss; Divine Knight / Knights Templar equipment-break)
2x Archer             (ranged elevation chip)
2x Summoner           (AoE charge pressure)
1x Ninja              (fast dual-wield / Throw flanker)
```

Public walkthrough details:

```text
Recommended level: ~41. Difficulty: 3/5. Urban elevation. Meliadoul's Unyielding Blade/Mighty Sword
breaks equipment; Safeguard and Steal Weapon are the named answers. Defeating Meliadoul ends the map.
```

Design reading:

Bervenia is the first true Chapter 4 boss duel. It is not about clearing a city; it is about crossing
a support screen fast enough to stop a Templar from shredding your loadout. The original designers
made Meliadoul the objective because the tactical lesson is focus: protect or disarm your gear, reach
the boss, and end the fight before the support pieces make the approach too expensive.

For v2 the identity is: **a complete-but-fair Templar break puzzle where Meliadoul is the only break
source, the support team amplifies her by blocking the steal/burst route, and the player still has
clear answers: Safeguard/Maintenance, Steal Weapon, magic pressure, mobility, and focused burst.**

## Local Data Confirmed

```text
Entry 443 / local entry 59 / battle_entd4_ent.bin:
  s0 Meliadoul     job 47 Divine Knight   L104   boss; defeat ends battle
  s1 Summoner      L102                   active enemy
  s2 Archer        L102                   active enemy
  s3 Archer        L101                   active enemy
  s4 Summoner      L102                   active enemy
  s5 Ninja         L102                   active enemy

Preserve: defeat-Meliadoul win condition, urban/elevation geometry, Meliadoul's Mighty Sword identity,
six-enemy roster, no guests, no chain.
```

Known / carried IDs:

```text
Archer job id: 77
Meliadoul job id: 47
Save the Queen item id: 34
Other job/equipment IDs: verify against loader tables before implementation.
```

## Enemy Party Escalation (Chapter 4 redesign)

```text
Headline engine: stealable Templar equipment-break race.
Supporting roles:
  - Meliadoul threatens gear and carries the objective.
  - Summoners punish clumping and slow static Safeguard setups.
  - Two Archers cover approach lanes and force route commitment.
  - Monk replaces the vanilla Ninja as a fast physical flanker without adding a rare-weapon leak.
```

This is a Chapter 4 puzzle party, but a narrow one. The support screen is complete and synergistic;
it does not add a second hard engine. No extra break source, no boss Safeguard, no hard status, and no
seventh body.

## Sanctioned Exceptions

```text
MIGHTY SWORD / EQUIPMENT BREAK:
  Allowed as Meliadoul's identity. Telegraphed, countered by Safeguard/Maintenance, disarmable by
  Steal Weapon/Rend Weapon, and capped at one break source.

SUMMONER AoE:
  Allowed with intact charge times. It supports the route puzzle; it is not an instant damage wall.

MONK FLANK:
  Allowed as damage, counter-pressure, and positional pressure. No hard status, no turn deletion.

DOUBLE ARCHER SCREEN:
  Restored after the Dancer variant. This keeps Bervenia closer to vanilla and avoids adding a global
  performer clock on top of the Templar break race.
```

## Reward Handling

```text
Guaranteed spoils: Save the Queen + Jade Armlet + Remedy, per chapter-4-rewards-implementation.md.
Save the Queen may also be represented as Meliadoul's equipped threat/steal-bait if implementation
accepts the duplicate/steal semantics; the canonical reward path is guaranteed spoils, not stealing.
```

No other named boss rare. Map treasure remains map treasure.

## Proposed Composition (New Game++ Bervenia v2)

Keep six active enemies. Meliadoul is the only boss-band unit.

| Slot | Role | Job | Level | Br/Fa | Purpose |
| ------ | ------ | ----- | ------- | --- | --------- |
| s0 | Boss / objective | Divine Knight (47) | `104` | `88/42` | Gear-break race; steal/disarm target; guaranteed Save the Queen reward. |
| s1 | AoE screen | Summoner | `102` | `60/84` | Charge-time AoE that punishes clumping on the approach. |
| s2 | High-ground chip | Archer (77) | `102` | `88/55` | Covers one route to Meliadoul. |
| s3 | High-ground chip | Archer (77) | `101` | `82/45` | Covers the alternate route. |
| s4 | AoE screen | Summoner | `102` | `60/84` | Second charge-time AoE; forces movement. |
| s5 | Flanker | Ninja | `102` | `90/35` | Fast Throw/dual-wield pressure on backline or steal attempts. |

Reasoning:

The v1 concept already had the right center: Meliadoul as the first Chapter 4 break boss. The v2 pass
makes the whole side complete and more puzzle-like, while protecting the fight's fair answers. If
Meliadoul has Safeguard, the disarm line dies. If supports add Rend or hard status, the map becomes a
gear tax instead of a Templar duel. The accepted version keeps one break source and turns the support
screen into route pressure.

Simulation result (`tmp/fft-level-design-039-bervenia/iteration-results.md`):

```text
v2 complete stealable Templar puzzle: Accepted.
Pressure 195.1; focus clarity 89.0; steal access 77.6; break fairness 71.0; hard-wall risk 3.4;
answerability 100.0.

Rejected: Safeguarded Meliadoul, dual-break support grinder, hard-status support screen, and seventh
body city lock.
```

## Proposed Composition (New Game++ Bervenia v3)

Current v3 changes: both vanilla Archer bodies remain Archers with complete lane-pressure kits, and
the vanilla Ninja becomes a Monk flanker.

Vanilla composition:

```text
1x Meliadoul Tengille  (boss; Divine Knight / Knights Templar equipment-break)
2x Archer             (ranged elevation chip)
2x Summoner           (AoE charge pressure)
1x Ninja              (fast dual-wield / Throw flanker)
```

v3 composition:

| Slot | Role | Job | Level | Br/Fa | Purpose |
| ------ | ------ | ----- | ------- | --- | --------- |
| s0 | Boss / objective | Divine Knight (47) | `104` | `88/78` | Gear-break race; steal/disarm target; guaranteed Save the Queen reward; magic answer stays live. |
| s1 | AoE screen | Summoner | `102` | `60/84` | Charge-time AoE that punishes clumping on the approach. |
| s2 | High-ground chip | Archer (77) | `102` | `88/55` | Covers one route to Meliadoul. |
| s3 | High-ground chip | Archer (77) | `102` | `88/55` | Second Archer matching s2; restores vanilla lane pressure. |
| s4 | AoE screen | Summoner | `102` | `60/84` | Second charge-time AoE; forces movement. |
| s5 | Flanker | Monk | `102` | `90/35` | Fast brawler pressure on backline or steal attempts. |

Current difference from vanilla:

```text
- Enemy count is unchanged: 6 enemies.
- Job count changes one slot: vanilla has 2 Archers + 1 Ninja; v3 has 2 Archers + 1 Monk.
- Objective is unchanged: defeat Meliadoul.
- The intended NG++ difference is kit completeness, higher level bands, Brave/Faith tuning,
  guaranteed Save the Queen reward, stricter guardrails around the single equipment-break source,
  two complete Archer lane-pressure units, and a Monk flanker replacing the vanilla Ninja.
```

## Builds (complete setups; Templar-duel puzzle)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Meliadoul — Divine Knight Boss (Lv 104)

```text
Job: Divine Knight / Knights Templar (47)   JobLevel: 8
Primary: Mighty Sword / equipment-break kit
Secondary: Fundaments, Squire JobLevel 8
Reaction: Counter (442)
Support: Magic Defense Boost (468); NOT Safeguard/Maintenance
Movement: Movement +2 (487)
Head: Crystal Helm (154)
Body: Reflect Mail (184)
Accessory: preserve Meliadoul's vanilla/default perfume; do not overwrite it
Right hand: Save the Queen (34) if using equipped-threat version; otherwise strong non-duplicate sword
Left hand: Crystal Shield (139)

Guardrails: one break source only; no boss Safeguard; Save the Queen reward is guaranteed spoils.
```

Role: the whole point of the fight. Disarm her or burst her before gear loss snowballs.

### Summoner x2 (Lv 102)

```text
JobLevel: 8
Primary: Summon Magic with intact charge times
Reaction: Soulbind
Support: Swiftspell
Movement: Movement +2 (487)
Gear: Wizard's Rod + Lambent Hat + Wizard's Robe + Featherweave Cloak (234)
Forbidden: instant summons, Stop/Don't Act engines, unrelated hard status.
```

Secondary split:

```text
s1 Summoner: White Magic, White Mage JobLevel 8
s4 Summoner: Time Magic, Time Mage JobLevel 8
```

Role: make standing still against Meliadoul expensive. Swiftspell shortens the summon clock, Soulbind
punishes careless burst, and the split secondaries let one Summoner stabilize while the other adds
tempo pressure.

### Archer x2 (Lv 102)

```text
Job: Archer (77)   JobLevel: 8
Primary: Aim / bow pressure
Secondary: Item, Chemist JobLevel 8
Reaction: Reflexes (449)
Support: Throw Items (474)
Movement: Ignore Elevation (Ignore Height legacy name)
Gear: Thief's Cap (168), Black Garb (198), Bracers (218), high-tier bow
Forbidden: Rend support; they are lane pressure, not extra break sources.
```

Role: force both approach lanes to cost turns and HP while keeping the roster closer to vanilla than
the Dancer variant.

### Monk (Lv 102, v3 replacement for vanilla Ninja)

```text
Job: Monk   JobLevel: 8
Primary: Martial Arts
Secondary: Throw, Ninja JobLevel 8, or Item, Chemist JobLevel 8, depending on legal slot behavior
Reaction: Counter
Support: Dual Wield
Movement: Movement +2 (487)
Gear: Black Garb (198), Bracers (218)
Forbidden: hard status; no rare Koga/Iga here because Germinas owns that reward beat.
```

Role: punish a tunnel-vision rush without changing the objective. The Monk keeps the vanilla Ninja's
fast physical flank pressure, but shifts it into body-blocking, counterplay, and melee threat instead
of dual ninja-blade burst.

## Positioning Plan

```text
Meliadoul starts reachable but screened, close enough to threaten early break. Summoners sit behind
or above the route so charge AoE punishes clumping. The two Archers cover opposite high-ground lanes
and tax the approach without adding another puzzle engine. Monk starts wide enough to punish
backline/steal routes but not so close that the player loses before acting.
```

The city should say: "protect your kit, open a route through the bow lanes, and take the sword out of
her hand before the support screen makes the approach too expensive."

## Implementation Checklist

- [x] Record entry 443 active roster in the doc.
- [ ] Preserve defeat-Meliadoul win condition.
- [ ] Keep Meliadoul as the only break source.
- [ ] Keep Save the Queen guaranteed in spoils; decide whether equipped Save the Queen duplicate/steal
      semantics are acceptable or use a non-duplicate equipped sword.
- [ ] Do not give Meliadoul Safeguard/Maintenance.
- [ ] Complete Meliadoul setup: Fundaments at JobLevel 8, Counter, Magic Defense Boost (468),
      Movement +2 (487), Crystal Helm, Reflect Mail, Crystal Shield, and her vanilla/default perfume.
- [ ] Complete both Summoner setups: s1 with White Magic at JobLevel 8, s4 with Time Magic at
      JobLevel 8, Soulbind, Swiftspell, Movement +2 (487), Wizard's Rod, Lambent Hat, Wizard's Robe,
      and Featherweave Cloak.
- [ ] Complete both Archer setups: Item at JobLevel 8, Reflexes, Throw Items,
      Ignore Elevation, Thief's Cap, Black Garb, Bracers, and a high-tier bow.
- [ ] Replace the vanilla Ninja with Monk: Throw or Item secondary, Counter, Dual Wield,
      Movement +2, Black Garb, and Bracers.
- [ ] Set/verify levels: Meliadoul `104`; supports `101`-`102`.
- [ ] Patch only through the correct future implementation layer; keep this redesign docs-only for now.
- [ ] Re-dump and diff after implementation; verify win condition, spoils, break behavior, and steal/disarm.

## Test Questions

- Is Meliadoul clearly the objective and best focus target?
- Can the player still answer the break engine with Safeguard/Maintenance, Steal Weapon, magic, or burst?
- Does the support screen make the route hard without adding a second puzzle?
- Do Swiftspell Summoners remain raceable, or do they make the approach too compressed?
- Do White Magic and Time Magic support Meliadoul without creating a second hard engine?
- Does the Monk preserve the vanilla Ninja's flank pressure without turning into an unfair physical wall?
- Do the two Archers create lane pressure without burying the Templar break-duel identity?
- Is Save the Queen guaranteed through spoils and not steal-dependent?
- If Save the Queen is equipped, is duplicate/steal behavior acceptable?
- Does the fight feel like the first Chapter 4 boss, not a Lucavi-tier spike?

## Sources

- Game8, "Free City of Bervenia Walkthrough (Battle 34)": roster, objective, level, Unyielding Blade
  gear-break, Safeguard/Steal tips, spoils and treasure.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553194
- Game8 ability/item pages: Soulbind, Swiftspell, Wizard's Rod, Wizard's Robe, and robe stat table.
  https://game8.co/games/Final-Fantasy-Tactics/archives/554315
  https://game8.co/games/Final-Fantasy-Tactics/archives/554342
  https://game8.co/games/Final-Fantasy-Tactics/archives/544613
  https://game8.co/games/Final-Fantasy-Tactics/archives/544780
  https://game8.co/games/Final-Fantasy-Tactics/archives/542019
- Final Fantasy Wiki, "Lambent Hat (Tactics)": hat name and magic-focused stat role.
  https://finalfantasy.fandom.com/wiki/Lambent_Hat_(Tactics)
- Local: `037-chapter-4-overview.md`, `059-chapter-4-balance-review.md`,
  `chapter-4-rewards-implementation.md`, `028-monastery-vaults-3rd.md`,
  `033-riovanes-castle-gate.md`, `031-walled-city-yardrow.md`, and
  `tmp/fft-level-design-039-bervenia/` (simulation and rejected variants).
