# 056 - Necrohol of Mullonde (Endgame Gauntlet 3/5)

Status: v3 implemented/deployed - direct playtest pending
Chapter: 4 - "In the Name of Love"
Battle order: Battle 51 (ENDGAME GAUNTLET 3 of 5 - no resupply across 054 -> 055 -> 056 -> 057 -> 058)
Target version: Enhanced v1.5.0
ENTD: `entd4` global entry `438`
Local slot: `054`
Simulation artifact: `tmp/fft-level-design-056-necrohol-of-mullonde/`

> V3 docs-only revision: preserve entry 438, positions and win-on-Cletienne behavior. Copy Cletienne
> from Mullonde Nave, Time Mages from Vaults Fifth Level, and the nearest true-job Samurai build from
> Fort Besselat Sluice. Generic levels are capped at 102-103.

> **V3 implementation (2026-07-11):** entry 438 patched in the embedded ENTD and deployed through a
> successful Release build. The installed DLL resource matches the source binary byte-for-byte; levels,
> genders, jobs, complete kits, positions and zero-spoil bytes were mechanically verified.

## V3 Locked Decisions

```text
s0 CLETIENNE - copy Mullonde Nave s2:
  Level 104; JobLevel 8; Brave/Faith 65/88.
  Sorcerer primary; secondary None; Magick Counter; Magick Defense Boost; Ignore Elevation.
  Dragon Rod / None / Lambent Hat / Black Robe / Featherweave Cloak.

s1/s2 TIME MAGE FEMALE - copy Vaults Fifth Level s5:
  Level 102; Time Mage bucket JL8; Brave/Faith 62/80; secondary None.
  Mana Shield / Swiftness / Teleport.
  Zeus Mace / None / Ribbon / Luminous Robe / Featherweave Cloak.

s3/s4 NINJA:
  Level 103; Ninja bucket JL8; Brave/Faith 90/35; secondary Martial Arts.
  Reflexes / Concentration / Movement +3.
  Koga's Blade / Iga's Blade / Thief's Cap / Ninja Gear / Hermes Shoes.

s5/s6 SAMURAI - copy Fort Besselat Sluice battle Samurai build:
  Level 102; main job Samurai; Samurai bucket JL8; Brave/Faith 88/42; secondary None.
  Dragon's Heart / Magick Attack Boost / Movement +3.
  Masamune / Crystal Shield / Crystal Helm / Crystal Mail / Bracers.

PRESERVE:
  All vanilla positions, Defeat Cletienne objective and zero special-spoil bytes.
```

## Gate Answers / Constraints

```text
Scope: redesign battle doc 056 only; no game data or code changes.
Allowed changes in design: active enemy kit/level/gear/ability plan, positioning, reward policy, and tests.
Chapter target: Chapter 4 broken-but-readable puzzle; gauntlet 3/5 should be harder than 055 but not
  the 057 peak.
Must preserve: Cletienne boss, Samurai/Ninja/Time Mage elite
  screen, ruined Necrohol terrain, and "Defeat Cletienne" objective.
Guests: no active guest. If future testing discovers any active guest/NPC, it must be player-controlled
  in NG+ and never used as a skill check.
Reward rule: no special spoils inside 054-058. V3 deliberately copies active Zeus Mace/Ribbon gear
  from 055 onto both Time Mages; Lordly Robe already pays at 052.
```

## Original Battle

Objective:

```text
Defeat Cletienne!
```

Player deployment:

```text
Up to 5 units, including Ramza. No outfitter: this is the third fight after the point of no return.
```

Original enemy composition:

```text
Cletienne Duroi   (Sorcerer; Magick Surge comeback mechanic)
2x Samurai         (Draw Out / Iaido pressure)
2x Ninja           (fast flankers)
2x Time Mage       (Slow / tempo pressure)
```

The vanilla tactical read is a tempo race. Cletienne becomes more dangerous if the player chips him
slowly, so the correct answer is to Silence and burst the boss while the elite screen tries to stall that
kill. The fight ends when Cletienne falls; full cleanup is intentionally optional.

## Local Data Confirmed

Dump command:

```bash
python tools/entd_tool.py dump-entry --input src/fftivc.battles.ngplus/entd/battle_entd4_ent.bin --entry 438 --include-empty
```

Confirmed active data:

| Slot | Status | Job | Level | JL | Secondary | Reaction | Support | Move | Equipment ids | Notes |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| 0 | Active boss | 39 | 105 | 8 | 0 | 423 | 468 | 507 | 167,198,234,65,254 | Cletienne. Black Garb-class body; no Lordly Robe reward. |
| 1 | Active | 81 | 104 | 8 | 0 | 449 | 510 | 486 | 167,206,234,56,255 | Time Mage; support currently empty. |
| 2 | Active | 81 | 104 | 8 | 0 | 449 | 510 | 486 | 167,206,234,56,255 | Time Mage; support currently empty. |
| 3 | Active | 89 | 104 | 8 | 254 | 453 | 465 | 487 | 168,198,210,14,14 | Ninja. |
| 4 | Active | 89 | 104 | 8 | 254 | 453 | 465 | 487 | 168,198,210,14,14 | Ninja. |
| 5 | Active | 88 | 104 | 8 | 254 | 442 | 465 | 486 | 154,182,218,254,254 | Samurai. |
| 6 | Active | 88 | 104 | 8 | 254 | 442 | 465 | 486 | 154,182,218,254,254 | Samurai. |

Data implications:

```text
- Entry 438 is confirmed moddable through ENTD direct edits.
- The current active roster already matches the intended identity: Cletienne + 2 Time Mage + 2 Ninja +
  2 Samurai.
- Current screen levels are 104. The redesign keeps that because 103 tested too soft for gauntlet 3/5.
- Current Time Mage support slots are empty (`510`); v2 must give every active human a complete,
  intentional Chapter 4 kit.
- Cletienne's body is `198`, not Lordly Robe. Preserve no usable reward in this gauntlet battle.
```

## Design Goal

Make Necrohol a true gauntlet 3/5 focus puzzle:

```text
Burst Cletienne through Magick Counter pressure while a level-102/103 elite screen threatens space,
tempo, and flanks without forcing full cleanup before the 057 dragon pit.
```

The headline engine is **Cletienne's copied Nave build and Magick Counter race**. Samurai/Ninja/Time Mage units exist to delay or
complicate the boss kill, not to become separate hard-lock engines.

## Enemy Party Escalation

Accepted redesign: **v3 copied-build Magick Counter boss race**.

| Slot | Role | Job | Level | Br/Fa | Purpose |
| ---: | --- | --- | ---: | --- | --- |
| 0 | Boss objective | Cletienne / Sorcerer | 104 | `65/88` | Mullonde Nave copy; Magick Counter caster target. |
| 1 | Soft tempo | Time Mage female | 102 | `62/80` | Fifth Level Mana Shield/Swiftness copy. |
| 2 | Soft tempo | Time Mage female | 102 | `62/80` | Second identical Time Mage. |
| 3 | Flanker | Ninja | 103 | `90/35` | Martial Arts/Concentration dual-blade flanker. |
| 4 | Flanker | Ninja | 103 | `90/35` | Second identical Ninja. |
| 5 | AoE pressure | Samurai | 102 | `88/42` | True-job Sluice Samurai build with Masamune. |
| 6 | AoE pressure | Samurai | 102 | `88/42` | Second identical true-job Samurai. |

Why this works:

```text
- The level-102/103 screen makes 056 meaningfully harder than 055 through builds rather than raw levels.
- The boss-focus lane is mandatory: the player must be able to reach and burst Cletienne
  without clearing all six support units.
- The two Time Mages exactly copy the accepted 055 build.
- The Samurai debut stays prominent and canonical, but Draw Out is spaceable/raceable.
- No reward appears here; Lordly Robe already pays before the point of no return at 052.
```

## Builds

### Cletienne Duroi - Nave-copy boss

```text
Level: 104
JobLevel: 8
Primary: Sorcerer
Secondary: None
Reaction: Magick Counter
Support: Magick Defense Boost
Movement: Ignore Elevation
Gear: Dragon Rod / None / Lambent Hat / Black Robe / Featherweave Cloak
Brave/Faith: 65/88
Reward: none
```

Guardrail: Magick Counter must pressure magic without making physical or ranged burst nonviable.

### Time Mage x2 - Fifth Level copies

```text
Female; Level: 102
JobLevel: 8
Primary: Time Magicks
Secondary: None
Reaction: Mana Shield
Support: Swiftness
Movement: Teleport
Gear: Zeus Mace / None / Ribbon / Luminous Robe / Featherweave Cloak
Brave/Faith: 62/80
Reward: none
```

Guardrail: validate the exact copied build in-game, especially Mana Shield sustain and Teleport routing.

### Ninja x2 - flank tempo

```text
Level: 103
JobLevel: 8
Primary: Throw
Secondary: Martial Arts
Reaction: Reflexes
Support: Concentration
Movement: Movement +3
Gear: Koga's Blade / Iga's Blade / Thief's Cap / Ninja Gear / Hermes Shoes
Brave/Faith: 90/35
Reward: none
```

Guardrail: Ninjas punish stalled play and exposed casters; they should not become instant-delete units
that decide the fight before Cletienne matters.

### Samurai x2 - Draw Out pressure

```text
Level: 102
JobLevel: 8
Main job: Samurai
Primary: Iaido
Secondary: None
Reaction: Dragon's Heart
Support: Magick Attack Boost
Movement: Movement +3
Gear: Masamune / Crystal Shield / Crystal Helm / Crystal Mail / Bracers
Brave/Faith: 88/42
Reward: none
```

Guardrail: Draw Out is the screen's space pressure, not an unavoidable wipe. Keep it raceable and
positionally readable.

## Positioning Plan

```text
Use the ruined Necrohol tiers. Cletienne starts protected but reachable: there must be a real lane for
boss burst. Samurai hold mid-field lanes, Ninjas start wide/flanking, and Time Mages sit back enough
to slow a reckless rush without sealing the map.
```

The player read should be: pick a lane, blunt tempo, and finish Cletienne before counter pressure and
screen pressure turn the fight into a resource bleed.

## Historical v2 Simulation / v3 Test Plan

The simulation below is historical v2 context. It does not validate the v3 removal of Magick Surge,
the lower generic levels, or the copied equipment packages; those require direct playtest.

Artifact:

```text
tmp/fft-level-design-056-necrohol-of-mullonde/
```

Accepted candidate:

```text
v2 no-reward surge race elite screen
Surge pressure: 66
Screen pressure: 144
Control risk: 23
Focus clarity: 100
Answerability: 100
Chain tax: 62
Reward correctness: 100
Kit completeness: 100
Identity fidelity: 100
```

Iteration notes:

```text
- Older level-103 screen plan was rejected as too soft for gauntlet 3/5.
- First level-104 pass was rejected by chain tax until the design required a real boss-focus lane.
- Double-Slow / Stop-style Time Mage pressure was rejected as a hard tempo lock.
- Unsilenceable Cletienne was rejected because Magick Surge must keep the Silence/burst answer.
- The Lordly Robe reward variant was rejected by the no-reward gauntlet rule.
- Current underbuilt support slots were rejected; all active humans need complete intentional kits.
```

Residual risks:

```text
- Confirm defeating Cletienne ends the battle before screen cleanup.
- Confirm Silence meaningfully shuts down the dangerous part of Cletienne's surge plan.
- Confirm Time Mage AI/abilities create soft tempo, not repeated hard control.
- Test 055 -> 056 -> 057 as a unit; 056 should tax tempo but not consume the resources needed for the
  5-star dragon pit.
```

## Rare / Reward Handling

```text
No special NG++ spoil is added inside the final gauntlet.
Lordly Robe already pays at `052` through guaranteed Spoils of War.
Cletienne does not carry Lordly Robe. Both Time Mages visibly carry Zeus Mace and Ribbon as an
intentional active-equipment exception; these are not spoil payloads.
Keep standard/vanilla loot and buried Elixirs only.
```

## Implementation Checklist

- [x] Preserve entry `438` and the "Defeat Cletienne" objective data.
- [x] Copy Cletienne's Mullonde Nave build at level `104`.
- [x] Keep every generic within level `102-103`.
- [x] Copy both female Time Mages from Vaults Fifth Level at `102`.
- [x] Apply both level-103 Ninja builds exactly as locked.
- [x] Copy the true-job Sluice Samurai build twice at level `102`, using Crystal Mail.
- [x] Keep roster identity: 2 Time Mage, 2 Ninja, 2 Samurai.
- [x] Apply Cletienne's Magick Counter setup.
- [x] Apply the exact copied Time Mage builds, including Mana Shield and Teleport.
- [x] Fill Time Mage support slots and verify every active human has complete equipment plus intentional
      secondary/reaction/support/move.
- [x] Preserve all positions and the existing boss-focus lane data.
- [x] Preserve zero special-spoil bytes and document active Zeus Mace/Ribbon Steal exposure.
- [x] Re-dump entry `438` after implementation and verify only intended kit/ability changes.
- [ ] Playtest `055 -> 056 -> 057` as a no-resupply unit.

## Test Questions

- Does focused burst against Cletienne feel like the correct plan?
- Does Magick Counter punish careless casting without shutting down the fight?
- Does the level-102/103 elite screen feel stronger than `055` but below the `057` peak?
- Do the two Time Mages create soft tempo rather than hard control?
- Can the player reach Cletienne without clearing all six support units?
- Are zero special spoils preserved, with Zeus Mace/Ribbon exposure limited to the intended equipment?
- Do both Time Mages appear female while Ninjas and Samurais retain their existing gender?

## Sources

- Local: `docs/battles/ENDGAME-BLOCKER.md` for entry mapping.
- Local: `docs/battles/037-chapter-4-overview.md` for Chapter 4 puzzle-party principles and gauntlet curve.
- Local: `docs/battles/chapter-4-rewards-implementation.md` for the no-usable-reward rule in `054-058`.
- Local: `tmp/fft-level-design-056-necrohol-of-mullonde/` simulation artifact.
- Local dump: `tools/entd_tool.py dump-entry --entry 438`.
- Game8, "Necrohol of Mullonde Walkthrough (Battle 51)": original roster and objective.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553227
