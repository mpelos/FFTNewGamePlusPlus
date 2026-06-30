# 038 - Dugeura Pass (Doguola Pass)

Status: ✅ implemented (v1, entry 442) — redesign plan v2 docs-only
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

The v2 redesign keeps this verified six-body shape, but upgrades it from "good v1 idea with some
incomplete slots" to a complete Chapter 4 opener: every active human gets secondary/reaction/support/
movement and legal gear, while the single headline engine remains Haste-Jump plus Black Mage AoE.

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

For v2 the identity is: **an open-field Chapter 4 opener where a complete Time Mage links the two
vanilla threats by Hasting the Dragoons while two Black Mages punish clumping. The answer is still
kill casters, read Jump panels, and do not overcommit into the Knight screen.**

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
```

Known / carried IDs:

```text
Archer job id: 77 (vanilla slot, swapped out)
Rod of Faith reward item: see chapter-4-rewards-implementation.md
Other job IDs and exact equipment IDs: verify against loader tables before implementation.
```

## Enemy Party Escalation (Chapter 4 redesign)

```text
Headline engine: Haste-Jump / AoE tempo.
Supporting roles:
  - Black Mages force immediate caster priority.
  - Time Mage accelerates Dragoons and can Slow, but cannot hard-lock.
  - Dragoons create panel-dodge pressure.
  - Knight screens the casters and punishes careless rushes.
```

This is a broken-but-readable Chapter 4 opener only in miniature: the enemy side has a real engine,
but no extra bodies, no Stop, no boss loot, and no unrelated puzzle. The Rod of Faith is guaranteed
spoils and should not be treated as mandatory combat equipment.

## Sanctioned Exceptions

```text
TIME MAGE CONTROL:
  Haste/Slow/Float only. No Stop, Don't Act, Immobilize, Petrify, or hard turn-deletion.

DRAGOON JUMP:
  Preserved as a telegraphed landing-panel threat. Haste may speed the cadence, but counterplay is
  still visible movement and killing grounded Dragoons.

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
Secondary: Item or low White Magic utility, if legal
Reaction: Reflexes (449) or Auto-Potion (441)
Support: Arcane Strength / magic boost if legal
Movement: Movement +1 (486) or Move-MP Up equivalent
Gear: final-shop mage hat + elemental/MA robe + Featherweave Cloak (234) + shop rod
Spoils note: s1 carries Rod of Faith in 0x1e; it does not need to be equipped.
```

Role: the named priority. If ignored, the fight snowballs.

### Time Mage (Lv 101-102)

```text
JobLevel: 8 or command-filtered equivalent
Primary: Time Magic limited to Haste, Slow, Float
Secondary: Item or low Black Magic utility, if legal
Reaction: Reflexes (449)
Support: Arcane Strength / Swiftness if legal and not instant-locking
Movement: Movement +1 (486)
Gear: final-shop mage hat + robe + Featherweave Cloak (234) + shop staff
Forbidden: Stop, Don't Act, Immobilize, Petrify, instant spell engines.
```

Role: the engine connector. Haste Dragoons, then Slow exposed targets.

### Dragoon x2 (Lv 102 / 101)

```text
JobLevel: 8
Primary: Jump
Secondary: Item / Fundaments / light utility, if legal
Reaction: Reflexes (449) or Counter (442)
Support: Attack Boost (465)
Movement: Movement +1 (486) or Jump-enhancing legal movement
Gear: final-shop helm + heavy armor + Germinas Boots (210) + shop spear + shield if legal
```

Role: visible panel pressure. They should punish ignored positioning, not erase the party before a
turn.

### Knight (Lv 101)

```text
JobLevel: 8
Primary: Knight skillset; at most one Rend/Mighty Sword source
Secondary: Item / Fundaments / light utility, if legal
Reaction: Counter (442)
Support: Attack Boost (465) or Safeguard if used defensively
Movement: Movement +1 (486)
Gear: final-shop helm + heavy armor + Bracers (218) + shop knight sword + shield
```

Role: the screen. One break source is enough; do not make gear destruction the opener's headline.

## Positioning Plan

```text
Open field. Keep the two Black Mages and Time Mage behind or offset from the Knight screen so the
player must choose a route instead of deleting all casters in one AoE. Put Dragoons where Haste gives
them credible Jump access, but preserve readable landing panels and enough room to step away.
```

The map should say: "Chapter 4 has begun; even generics have a plan. Kill the mages, watch the floor,
and do not chase blindly through the Knight."

## Implementation Checklist

- [x] Record entry 442 roster and current v1 swap in the doc.
- [ ] Preserve six active enemies and open-field geometry.
- [ ] Keep Archer slot as Time Mage, but complete its setup and command-filter to Haste/Slow/Float.
- [ ] Complete both Black Mage setups; keep s1 as Rod of Faith spoils carrier.
- [ ] Complete both Dragoon setups; preserve Jump and landing-panel counterplay.
- [ ] Complete Knight setup; cap break pressure at one source.
- [ ] Tune levels as opener: Black Mages/one Dragoon `102`; Knight/one Dragoon `101`; Time Mage `101`
      or `102` depending on playtest pressure.
- [ ] Confirm no boss rare and no steal-dependent reward.
- [ ] Patch only through the correct future implementation layer; keep this redesign docs-only for now.
- [ ] Re-dump and diff after implementation; verify spoils, Time Magic filtering, Jump, and no hard lock.

## Test Questions

- Are Black Mages still the obvious first priority?
- Does Haste make Jump more urgent without making it unreadable?
- Can the player dodge marked Jump panels after Haste?
- Does Slow add pressure without becoming a turn-deletion lock?
- Does the Knight screen matter without turning the fight into a gear-break tax?
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
