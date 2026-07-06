# 038 - Dugeura Pass (Doguola Pass)

Status: ✅ implemented (v1, entry 442) — redesign plan v3 docs-only
Chapter: 4 — "In the Name of Love"
Battle order: Battle 33 (Chapter 4 opener)
Target version: Enhanced v1.5.0
ENTD: global entry **442** (local entry 58, `battle_entd4_ent.bin`)
File: `battle_entd4_ent.bin` (embedded NG+ swap)

> **NG++ reward applied (2026-06-27):** Rod of Faith on s1 through guaranteed Spoils of War
> (`0x1e`), NG+ only, within the 3-item cap, no stealing required. This is reward pressure, not
> combat gear that must be equipped.

Implemented v1 composition (entry 442, vanilla-dump verified):

- s0 Knight L101.
- s1 Black Mage L102.
- s2 Archer -> **Time Mage** L102, JobLevel 4 cap / command-filtered to Haste/Slow/Float.
- s3 Black Mage L102.
- s4 Dragoon L102.
- s5 Dragoon L101.

The v2 redesign kept this verified six-body shape, but upgraded it from "good v1 idea with some
incomplete slots" to a complete Chapter 4 opener: every active human gets secondary/reaction/support/
movement and legal gear, while the single headline engine remains Haste-Jump plus Black Mage AoE.

The v3 redesign keeps the same opener identity but replaces the Knight screen with a Samurai screen
and the Time Mage connector with a Geomancer bruiser. Shirahadori makes blind physical rushing worse,
while two Geomancy users give the front line terrain pressure instead of turning the opener into a
Rend or hard-CT-control tax.

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
1x Knight       (front-line bruiser)
1x Archer       (ranged chip)
2x Black Mage   (high-level AoE; the priority threat)
2x Dragoon      (Jump; untargetable while airborne, lands on marked panels)
```

Public walkthrough details:

```text
Recommended level: ~41. Difficulty: 3/5. Open field. Kill the Black Mages first and move units off
Dragoon landing panels. Buried map treasure and normal spoils exist, but there is no named boss.
```

Design reading:

Dugeura is Chapter 4's first handshake: no Lucavi, no named boss, just proof that ordinary enemies now
operate like endgame pieces. Vanilla asks for two reads: rush the Black Mages before AoE compounds,
and dodge Dragoon Jump by respecting the landing marks. New Game++ should sharpen that lesson, not
replace it with a spike.

For v2 the identity was: **an open-field Chapter 4 opener where a complete Time Mage links the two
vanilla threats by Hasting the Dragoons while two Black Mages punish clumping. The answer is still
kill casters, read Jump panels, and do not overcommit into the Knight screen.**

For v3 the identity is: **an open-field Black Mage AoE / Jump opener, now with a Samurai frontliner
and a Geomancer bruiser that punish careless weapon attacks and bad terrain approaches without making
equipment break or hard CT control the battle's headline.**

## Local Data Confirmed

```text
Entry 442 / local entry 58 / battle_entd4_ent.bin:
  s0 Knight       L101   active enemy
  s1 Black Mage   L102   active enemy; Rod of Faith spoils carrier
  s2 Time Mage    L102   v1 swap from Archer; Haste/Slow/Float only
  s3 Black Mage   L102   active enemy
  s4 Dragoon      L102   active enemy
  s5 Dragoon      L101   active enemy

Preserve: open-field geometry, two Black Mage AoE priority, two Dragoon Jump threats, no boss, no
guest, no no-resupply chain.

v3 target change:
  s0 Knight -> Samurai L101 with Shirahadori, Doublehand, Movement +2 (487), and Geomancy secondary.
  s2 Time Mage -> Geomancer L102 with Martial Arts secondary, Nature's Wrath, Attack Boost,
     Movement +2 (487), and PA/MA hybrid gear.
```

Known / carried IDs:

```text
Archer job id: 77 (vanilla slot, swapped out)
Rod of Faith reward item: see chapter-4-rewards-implementation.md
Other job IDs and exact equipment IDs: verify against loader tables before implementation.
```

## Enemy Party Escalation (Chapter 4 redesign)

```text
Headline engine: Black Mage AoE / Jump pressure with Geomancy terrain control.
Supporting roles:
  - Black Mages force immediate caster priority.
  - Geomancer bruiser pressures terrain lines and threatens Martial Arts sustain/burst.
  - Dragoons create panel-dodge pressure.
  - Samurai screens the casters, punishes careless weapon rushes, and adds terrain chip through Geomancy.
```

This is a broken-but-readable Chapter 4 opener only in miniature: the enemy side has a real engine,
but no extra bodies, no Stop, no boss loot, and no unrelated puzzle. The Rod of Faith is guaranteed
spoils and should not be treated as mandatory combat equipment.

## Sanctioned Exceptions

```text
GEOMANCY PRESSURE:
  Terrain attacks are allowed as instant chip/status pressure, including Nature's Wrath counters.
  Do not turn terrain status into hard-lock spam or a second invisible failure condition.

DRAGOON JUMP:
  Preserved as a telegraphed landing-panel threat. Counterplay is still visible movement and killing
  grounded Dragoons.

BLACK MAGE AoE:
  Strong elemental AoE is allowed because the walkthrough already names Black Mages as the priority.
  Keep charge/cast cadence readable and do not add a third AoE engine.
```

## Reward Handling

```text
No boss rare. Rod of Faith is the designed guaranteed Spoils of War reward for the battle, authored
through ENTD 0x1e on s1 and documented in chapter-4-rewards-implementation.md. Do not make stealing
required. Do not add more than three spoils.
```

Map treasure remains the map's own reward layer and should not be conflated with the battle puzzle.

## Proposed Composition (New Game++ Dugeura Pass v2)

Keep six active enemies. Bottom-of-band levels preserve opener pacing.

| Slot | Role | Job | Level | Br/Fa | Purpose |
| ------ | ------ | ----- | ------- | --- | --------- |
| s0 | Screen | Knight | `101` | `88/42` | Blocks the direct caster rush; one break source at most. |
| s1 | AoE priority | Black Mage | `102` | `60/84` | Main damage engine; Rod of Faith spoils carrier. |
| s2 | Tempo support | Time Mage | `101` or `102` | `62/80` | Haste Dragoons / Slow players; no hard lock. |
| s3 | AoE priority | Black Mage | `102` | `60/84` | Second AoE caster; makes clumping costly. |
| s4 | Jump threat | Dragoon | `102` | `86/40` | Hasted Jump pressure; panel-dodge check. |
| s5 | Jump threat | Dragoon | `101` | `86/40` | Staggered Jump pressure without spiking the opener. |

Reasoning:

The v1 swap was the right idea, but v2 needs Cap 4 completeness and cleaner guardrails. Complete
setups make the party credible, while slightly reducing the average offset keeps the opener from
feeling like Bervenia or Limberry. The player has at least two fair answers: blitz the Time/Black
Mage cluster before Haste compounds, or spread defensively and punish Dragoons as they land.

Simulation result (`tmp/fft-level-design-038-dugeura-pass/iteration-results.md`):

```text
v2 complete readable Haste-Jump opener: Accepted.
Pressure 165.0; caster priority 86.0; Jump counterplay 72.0; spike risk 20.5; answerability 93.1.

Rejected: Stop-Time opener trap, seven-body pincer, and over-spiking pressure. Third Black Mage
artillery was considered but rejected as the main plan because it turns the fight into raw AoE instead
of linking the vanilla Dragoon lesson to the caster priority lesson.
```

## Proposed Composition (New Game++ Dugeura Pass v3)

Keep six active enemies and preserve the Black Mage AoE / Dragoon Jump lesson. The v3 change is
focused: replace the old Knight screen with a Samurai who is harder to brute-force physically, and
replace the Time Mage with a Geomancer bruiser who pressures terrain lanes without hard CT control.
Both remain answerable through magic, status, flanking, caster blitz, or killing the support pieces
first.

| Slot | Role | Job | Level | Br/Fa | Purpose |
| ------ | ------ | ----- | ------- | --- | --------- |
| s0 | Parry screen | Samurai | `101` | `88/60` | Screens the caster cluster with Shirahadori; Geomancy adds terrain chip without becoming the main engine. |
| s1 | AoE priority | Black Mage | `102` | `60/84` | Main damage engine; Rod of Faith spoils carrier. |
| s2 | Terrain bruiser | Geomancer | `102` | `84/60` | Runeblade hybrid pressure; Martial Arts utility; Nature's Wrath punishes adjacent weapon attacks. |
| s3 | AoE priority | Black Mage | `102` | `60/84` | Second AoE caster; makes clumping costly. |
| s4 | Jump threat | Dragoon | `102` | `86/40` | Jump pressure; panel-dodge check. |
| s5 | Jump threat | Dragoon | `101` | `86/40` | Staggered Jump pressure without spiking the opener. |

Reasoning:

The Samurai is a better Chapter 4 opener screen than the v2 Knight. Knight break pressure risks
turning the first map into a gear-tax lesson; Samurai pressure instead asks the player to respect
physical evasion and terrain while still prioritizing the real threats. The Geomancer replaces
Haste/Slow tempo with visible terrain pressure and Monk utility, so the battle stops relying on hard
CT control while still feeling more complete than v1. This keeps the answer pattern clear: do not
brute-force the frontliners, remove the Black Mage core, and keep moving around Jump markers.

## Builds (complete setups; opener-tier gear)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Black Mage x2 (Lv 102)

```text
JobLevel: 8
Primary: Black Magic, high elemental AoE with normal charge/cast cadence
Reaction: Mana Shield (445)
Support: Swiftness
Movement: Manafont (494)
Gear: Wizard's Rod + Lambent Hat + Black Robe + Barrette
Spoils note: s1 carries Rod of Faith in 0x1e; it does not need to be equipped.
```

Secondary split:

```text
s1 Black Mage: White Magic, White Mage JobLevel 8
s3 Black Mage: Time Magic, Time Mage JobLevel 8
```

Role: the named priority. If ignored, the fight snowballs. Mana Shield plus Manafont lets the mages
survive one careless burst line, while Swiftness makes their cast windows more urgent without changing
the answer: spread, Silence, burst after MP pressure, or reach them through the front screen. White
Magic gives one caster recovery/revive utility, while Time Magic gives the other tempo pressure without
returning the whole encounter to the old Time Mage connector plan.

### Geomancer (Lv 102, v3 replacement for Time Mage)

```text
JobLevel: 8
Primary: Geomancy
Secondary: Martial Arts, Monk JobLevel 8
Reaction: Nature's Wrath (Counter Flood legacy name)
Support: Attack Boost (465)
Movement: Movement +2 (487)
Gear: Runeblade (30) + Thief's Cap (168) + Power Garb (195) + Red Shoes (214)
```

Role: the terrain bruiser. Runeblade and mixed PA/MA gear make Geomancy credible, Martial Arts gives
no-MP utility, and Nature's Wrath punishes melee contact without adding hard turn deletion.

### Dragoon x2 (Lv 102 / 101)

```text
JobLevel: 8
Primary: Jump
Secondary: Martial Arts, Monk JobLevel 8
Reaction: Dragonheart (Dragon Heart legacy name)
Support: Attack Boost (465)
Movement: Ignore Elevation (Ignore Height legacy name)
Gear: Obelisk + Crystal Helm + Crystal Mail + Hermes Shoes (213)
```

Role: visible panel pressure. Hermes Shoes improves their tempo, while Dragonheart can create a
limited Reraise tax if the player clips them early. Martial Arts gives no-MP utility when grounded,
and Ignore Elevation lets them keep the open-field vertical pressure. They should punish ignored
positioning, not erase the party before a turn.

### Samurai (Lv 101, v3 replacement for Knight)

```text
JobLevel: 8
Primary: Samurai / Iaido
Secondary: Geomancy, JobLevel 8
Reaction: Shirahadori
Support: Doublehand
Movement: Movement +2 (487)
Gear: Kiku-Ichimonji + Crystal Helm + Crystal Mail + Magic Gauntlet
```

Role: the parry screen. It should punish careless weapon attacks and add terrain chip, but not become
the battle's objective by itself. Magic, status, flanks, and ignoring it long enough to kill the caster
core must remain valid answers.

## Positioning Plan

```text
Open field. Keep the two Black Mages behind or offset from the Samurai and Geomancer screen so the
player must choose a route instead of deleting all casters in one AoE. Put Dragoons where they have
credible Jump access, but preserve readable landing panels and enough room to step away.
```

The map should say: "Chapter 4 has begun; even generics have a plan. Kill the mages, watch the floor,
and do not chase blindly through the Samurai."

## Implementation Checklist

- [x] Record entry 442 roster and current v1 swap in the doc.
- [ ] Preserve six active enemies and open-field geometry.
- [ ] Replace s2 Time Mage with Geomancer setup: Martial Arts secondary, Nature's Wrath,
      Attack Boost, Movement +2 (487).
- [ ] Set Geomancer and Monk job levels to `8`.
- [ ] Equip Geomancer with Runeblade, Thief's Cap, Power Garb, and Red Shoes.
- [ ] Complete both Black Mage setups with Mana Shield, Swiftness, Manafont, and Barrette; set s1
      secondary to White Magic at JobLevel 8, s3 secondary to Time Magic at JobLevel 8, and keep s1 as
      Rod of Faith spoils carrier. Equip both with Wizard's Rod, Lambent Hat, and Black Robe.
- [ ] Complete both Dragoon setups with Martial Arts secondary at Monk JobLevel 8, Dragonheart,
      Attack Boost, Ignore Elevation, Obelisk, Crystal Helm, Crystal Mail, and Hermes Shoes; preserve
      Jump and landing-panel counterplay.
- [ ] Replace s0 Knight with Samurai setup: Shirahadori, Doublehand, Movement +2 (487), Geomancy secondary.
- [ ] Set Samurai and Geomancy job levels to `8`.
- [ ] Equip Samurai with Kiku-Ichimonji, Crystal Helm, Crystal Mail, and Magic Gauntlet.
- [ ] Tune levels as opener: Black Mages/Geomancer/one Dragoon `102`; Samurai/one Dragoon `101`.
- [ ] Confirm no boss rare and no steal-dependent reward.
- [ ] Patch only through the correct future implementation layer; keep this redesign docs-only for now.
- [ ] Re-dump and diff after implementation; verify spoils, Geomancy/Nature's Wrath, Jump, and no hard lock.

## Test Questions

- Are Black Mages still the obvious first priority?
- Do Mana Shield and Manafont make the Black Mages resilient without invalidating focused MP pressure
  or Silence?
- Does Swiftness create urgency without making the first cast unavoidable?
- Do White Magic and Time Magic add support pressure without making the Black Mages too self-sufficient?
- Can the player dodge marked Jump panels while managing Geomancy terrain pressure?
- Do Hermes Shoes make Dragoon Jump tempo urgent without making landing panels unreadable?
- Does Dragonheart create only a small Reraise tax instead of a cleanup slog?
- Does Ignore Elevation improve Dragoon reach without making the opening formation unavoidable?
- Does Martial Arts add utility without turning the Geomancer into the main objective?
- Does the Samurai screen matter without turning Shirahadori into a fake wall?
- Does Geomancy add pressure without becoming a second headline engine?
- Does the fight feel like a Chapter 4 opener rather than a boss spike?
- Does Rod of Faith arrive through guaranteed spoils, within the 3-item cap?

## Sources

- Game8, "Dugeura Pass Walkthrough (Battle 33)": roster, objective, level, Black Mage priority,
  Dragoon Jump counterplay, treasure/spoils.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553193
- Local: `037-chapter-4-overview.md`, `059-chapter-4-balance-review.md`,
  `chapter-4-rewards-implementation.md`, `docs/spoils-of-war-reward-system.md`,
  `027-monastery-vaults-2nd.md` (Dragoon precedent), and
  `tmp/fft-level-design-038-dugeura-pass/` (simulation and rejected variants).
