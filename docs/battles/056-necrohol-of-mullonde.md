# 056 - Necrohol of Mullonde (Endgame Gauntlet 3/5)

Status: redesigned (documentation only; not implemented in game data by this task)
Chapter: 4 - "In the Name of Love"
Battle order: Battle 51 (ENDGAME GAUNTLET 3 of 5 - no resupply across 054 -> 055 -> 056 -> 057 -> 058)
Target version: Enhanced v1.5.0
ENTD: `entd4` global entry `438`
Local slot: `054`
Simulation artifact: `tmp/fft-level-design-056-necrohol-of-mullonde/`

> Docs-only redesign note: this document is the intended NG++ level design. It does not change the
> embedded ENTD, scripts, binaries, or patch code. Implementation must later patch entry `438` and
> preserve the win-on-Cletienne behavior.

## Gate Answers / Constraints

```text
Scope: redesign battle doc 056 only; no game data or code changes.
Allowed changes in design: active enemy kit/level/gear/ability plan, positioning, reward policy, and tests.
Chapter target: Chapter 4 broken-but-readable puzzle; gauntlet 3/5 should be harder than 055 but not
  the 057 peak.
Must preserve: Cletienne boss, Magick Surge / punish-slow-chip identity, Samurai/Ninja/Time Mage elite
  screen, ruined Necrohol terrain, and "Defeat Cletienne" objective.
Guests: no active guest. If future testing discovers any active guest/NPC, it must be player-controlled
  in NG+ and never used as a skill check.
Reward rule: no usable rewards inside 054-058. Lordly Robe already pays at 052.
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

Make Necrohol a true gauntlet 3/5 tempo puzzle:

```text
Silence or burst Cletienne before Magick Surge punishes slow chip, while a level-104 elite screen
threatens space, tempo, and flanks without forcing full cleanup before the 057 dragon pit.
```

The headline engine is **Cletienne's surge race**. Samurai/Ninja/Time Mage units exist to delay or
complicate the boss kill, not to become separate hard-lock engines.

## Enemy Party Escalation

Accepted redesign: **v2 no-reward surge race elite screen**.

| Slot | Role | Job | Level | Purpose |
|---:|---|---|---:|---|
| 0 | Boss objective | Cletienne / Sorcerer | 105 | Magick Surge comeback mage; Silence/burst target. |
| 1 | Soft tempo | Time Mage | 104 | Slow/Haste lane, but not hard control. |
| 2 | Soft tempo | Time Mage | 104 | Secondary tempo caster; together they create one effective Slow lane. |
| 3 | Flanker | Ninja | 104 | Fast pressure on exposed casters and stalled boss rushes. |
| 4 | Flanker | Ninja | 104 | Second flank route; punishes slow formation. |
| 5 | AoE pressure | Samurai | 104 | Draw Out/Iaido space pressure; no hard lock. |
| 6 | AoE pressure | Samurai | 104 | Second Samurai; makes the screen real. |

Why this works:

```text
- The level-104 screen makes 056 meaningfully harder than 055.
- The boss-focus lane is mandatory: the player must be able to reach, Silence, and burst Cletienne
  without clearing all six support units.
- Time Mage pressure is capped to one effective Slow lane. No Stop, Don't Act, Death, or repeated hard
  turn denial.
- The Samurai debut stays prominent and canonical, but Draw Out is spaceable/raceable.
- No reward appears here; Lordly Robe already pays before the point of no return at 052.
```

## Builds

### Cletienne Duroi - surge boss

```text
Level: 105
JobLevel: 8
Primary: Sorcerer magic plus Magick Surge identity
Secondary: intentional utility that does not remove Silence/burst counterplay
Reaction: existing boss reaction or defensive reaction
Support: magic/offense support
Movement: boss mobility
Gear: complete caster gear; keep Black Garb-class body or equivalent standard gear
Reward: none
```

Guardrail: the dangerous magic must remain meaningfully answerable by Silence and decisive burst. An
unsilenceable surge build fails the battle.

### Time Mage x2 - one effective Slow lane

```text
Level: 104
JobLevel: 8
Primary: Time Magic with Haste/Slow/Float style tempo
Secondary: low-impact caster utility
Reaction: Reflexes
Support: intentional MA/defense support; current `510` empty support must be fixed
Movement: Move +1
Gear: complete caster gear
Reward: none
```

Guardrail: two Time Mages are allowed, but only one effective Slow/disruptor lane. No Stop, Don't Act,
Death, or hard turn deletion.

### Ninja x2 - flank tempo

```text
Level: 104
JobLevel: 8
Primary: Ninja / Throw / dual-wield pressure
Secondary: utility, not status lock
Reaction: existing evasion/counter reaction
Support: Attack Boost or equivalent offense support
Movement: Move +2
Gear: complete ninja gear, no reward payload
Reward: none
```

Guardrail: Ninjas punish stalled play and exposed casters; they should not become instant-delete units
that decide the fight before Cletienne's surge matters.

### Samurai x2 - Draw Out pressure

```text
Level: 104
JobLevel: 8
Primary: Draw Out / Iaido pressure
Secondary: utility, not hard status
Reaction: Counter or defensive reaction
Support: Attack/MA support
Movement: Move +1
Gear: complete heavy/samurai gear
Reward: none
```

Guardrail: Draw Out is the screen's space pressure, not an unavoidable wipe. Keep it raceable and
positionally readable.

## Positioning Plan

```text
Use the ruined Necrohol tiers. Cletienne starts protected but reachable: there must be a real lane for
Silence/burst. Samurai hold mid-field lanes, Ninjas start wide/flanking, and Time Mages sit back enough
to slow a reckless rush without sealing the map.
```

The player read should be: pick a lane, blunt tempo, Silence Cletienne, and finish him before surge and
screen pressure turn the fight into a resource bleed.

## Simulation Plan and Results

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
None. No usable NG++ reward is added inside the final gauntlet.
Lordly Robe already pays at `052` through guaranteed Spoils of War.
Cletienne should not carry Lordly Robe, and no support unit should carry a hidden rare payload.
Keep standard/vanilla loot and buried Elixirs only.
```

## Implementation Checklist

- [ ] Preserve entry `438` and the "Defeat Cletienne" objective.
- [ ] Keep Cletienne level `105`; keep the elite screen level `104`.
- [ ] Keep roster identity: 2 Time Mage, 2 Ninja, 2 Samurai.
- [ ] Ensure Cletienne remains Silence/burst-answerable.
- [ ] Cap Time Mage pressure to one effective Slow lane; no Stop/Don't Act/hard control.
- [ ] Fill Time Mage support slots and verify every active human has complete equipment plus intentional
      secondary/reaction/support/move.
- [ ] Preserve a playable boss-focus lane; do not force full cleanup.
- [ ] Add no usable reward, no Lordly Robe, and no steal-dependent rare.
- [ ] Re-dump entry `438` after implementation and verify only intended kit/ability changes.
- [ ] Playtest `055 -> 056 -> 057` as a no-resupply unit.

## Test Questions

- Does Silence/burst Cletienne feel like the correct plan?
- Does Magick Surge punish slow chip without becoming unavoidable?
- Does the level-104 elite screen feel stronger than `055` but below the `057` peak?
- Do the two Time Mages create soft tempo rather than hard control?
- Can the player reach Cletienne without clearing all six support units?
- Are no usable NG++ rewards or unique steal payloads present?

## Sources

- Local: `docs/battles/ENDGAME-BLOCKER.md` for entry mapping.
- Local: `docs/battles/037-chapter-4-overview.md` for Chapter 4 puzzle-party principles and gauntlet curve.
- Local: `docs/battles/chapter-4-rewards-implementation.md` for the no-usable-reward rule in `054-058`.
- Local: `tmp/fft-level-design-056-necrohol-of-mullonde/` simulation artifact.
- Local dump: `tools/entd_tool.py dump-entry --entry 438`.
- Game8, "Necrohol of Mullonde Walkthrough (Battle 51)": original roster and objective.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553227
