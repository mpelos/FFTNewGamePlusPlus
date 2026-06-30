# 039 - Free City of Bervenia

Status: ✅ implemented (v1, entry 443) — redesign plan v2 docs-only
Chapter: 4 — "In the Name of Love"
Battle order: Battle 34 (after Dugeura Pass)
Target version: Enhanced v1.5.0
ENTD: global entry **443** (local entry 59, `battle_entd4_ent.bin`)
File: `battle_entd4_ent.bin` (embedded NG+ swap)

> **NG++ rewards applied:** Save the Queen + Jade Armlet + Remedy through guaranteed Spoils of War
> (`0x1e`), NG+ only, within the 3-item cap, no stealing required. Steal Weapon remains a tactical
> disarm answer, not the only reward path.

Implemented v1 composition (entry 443, vanilla-dump verified):

- s0 **Meliadoul** (job 47 Divine Knight, boss, dies) — L104, JobLevel 8, Mighty Sword break kit,
  Save the Queen (34) as equipped threat/steal-bait, win-on-death scripting preserved.
- s1,s4 Summoner — L102.
- s2,s3 Archer — L102/L101.
- s5 Ninja — L102.

The v2 redesign keeps the exact six-body boss-duel shape, but upgrades the whole support screen to
complete Chapter 4 setups while preserving the key fairness point: only Meliadoul breaks equipment,
and she must remain stealable/disarmable.

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
  - Archers cover approach lanes and force route commitment.
  - Ninja pressures the flank/backline and punishes a pure rush.
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

NINJA FLANK / THROW:
  Allowed as damage and positional pressure. No hard status, no turn deletion.
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
Secondary: Item / Fundaments-style light command, if legal
Reaction: Counter or defensive reaction that does not block Steal Weapon
Support: Attack Boost (465) or offensive support; NOT Safeguard/Maintenance
Movement: Movement +1 (486) or legal mobility
Head/Body/Accessory: Tier-A-appropriate heavy gear, not Genji/best Tier-S
Right hand: Save the Queen (34) if using equipped-threat version; otherwise strong non-duplicate sword
Left hand: legal shield, not Escutcheon/Genji Shield

Guardrails: one break source only; no boss Safeguard; Save the Queen reward is guaranteed spoils.
```

Role: the whole point of the fight. Disarm her or burst her before gear loss snowballs.

### Summoner x2 (Lv 102)

```text
JobLevel: 8
Primary: Summon Magic with intact charge times
Secondary: Item / low White Magic utility, if legal
Reaction: Reflexes (449) or Auto-Potion (441)
Support: Arcane Strength / magic boost if legal
Movement: Movement +1 (486)
Gear: final-shop mage hat + robe + Featherweave Cloak (234) + shop rod/staff
Forbidden: instant summons, Stop/Don't Act engines, unrelated hard status.
```

Role: make standing still against Meliadoul expensive.

### Archer x2 (Lv 102 / 101)

```text
Job: Archer (77)   JobLevel: 8
Primary: Aim / bow pressure
Secondary: Item / Fundaments / light utility, if legal
Reaction: Reflexes (449)
Support: Concentration (469)
Movement: Movement +1 (486) or Ignore Height if legal and not overused
Gear: Thief's Cap (168), Black Garb (198), Bracers (218), high-tier bow
Forbidden: Rend support; they are lane pressure, not extra break sources.
```

Role: force the approach to cost turns and HP.

### Ninja (Lv 102)

```text
JobLevel: 8
Primary: Ninja skillset / dual-wield attack
Secondary: Throw or Item, depending on legal slot behavior
Reaction: First Strike (453) or Reflexes (449)
Support: Attack Boost (465) or Dual Wield innate support if needed
Movement: Movement +2 (487)
Gear: Thief's Cap (168), Black Garb (198), Germinas Boots (210), shop ninja blades
Forbidden: hard status; no rare Koga/Iga here because Germinas owns that reward beat.
```

Role: punish a tunnel-vision rush without changing the objective.

## Positioning Plan

```text
Meliadoul starts reachable but screened, close enough to threaten early break. Summoners sit behind
or above the route so charge AoE punishes clumping. Archers split high-ground lanes. Ninja starts wide
enough to punish backline/steal routes but not so close that the player loses before acting.
```

The city should say: "protect your kit, open a route, and take the sword out of her hand before the
support screen makes the approach too expensive."

## Implementation Checklist

- [x] Record entry 443 active roster in the doc.
- [ ] Preserve defeat-Meliadoul win condition.
- [ ] Keep Meliadoul as the only break source.
- [ ] Keep Save the Queen guaranteed in spoils; decide whether equipped Save the Queen duplicate/steal
      semantics are acceptable or use a non-duplicate equipped sword.
- [ ] Do not give Meliadoul Safeguard/Maintenance.
- [ ] Complete both Summoner setups with intact charge times.
- [ ] Complete both Archer setups without Rend/break support.
- [ ] Complete Ninja setup without hard status or Koga/Iga reward leakage.
- [ ] Set/verify levels: Meliadoul `104`; supports `101`-`102`.
- [ ] Patch only through the correct future implementation layer; keep this redesign docs-only for now.
- [ ] Re-dump and diff after implementation; verify win condition, spoils, break behavior, and steal/disarm.

## Test Questions

- Is Meliadoul clearly the objective and best focus target?
- Can the player still answer the break engine with Safeguard/Maintenance, Steal Weapon, magic, or burst?
- Does the support screen make the route hard without adding a second puzzle?
- Is Save the Queen guaranteed through spoils and not steal-dependent?
- If Save the Queen is equipped, is duplicate/steal behavior acceptable?
- Does the fight feel like the first Chapter 4 boss, not a Lucavi-tier spike?

## Sources

- Game8, "Free City of Bervenia Walkthrough (Battle 34)": roster, objective, level, Unyielding Blade
  gear-break, Safeguard/Steal tips, spoils and treasure.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553194
- Local: `037-chapter-4-overview.md`, `059-chapter-4-balance-review.md`,
  `chapter-4-rewards-implementation.md`, `028-monastery-vaults-3rd.md`,
  `033-riovanes-castle-gate.md`, `031-walled-city-yardrow.md`, and
  `tmp/fft-level-design-039-bervenia/` (simulation and rejected variants).
