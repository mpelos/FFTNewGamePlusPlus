# 058 - Airship Graveyard (Final Battle: Hashmal -> Ultima)

Status: redesigned (documentation only; not implemented in game data by this task)
Chapter: 4 - "In the Name of Love"
Battle order: Battle 53 (ENDGAME GAUNTLET 5 of 5 - final campaign battle)
Target version: Enhanced v1.5.0
ENTD phase 1: `entd4` global entry `440`
ENTD phase 2: `entd4` global entry `441`
Local slots: `056` and `057`
Simulation artifact: `tmp/fft-level-design-058-airship-graveyard/`

> Docs-only redesign note: this document is the intended NG++ finale design. It does not change the
> embedded ENTD, scripts, binaries, or patch code. Implementation must later patch entries `440` and
> `441` only after verifying which records are active combatants, transform records, dormant script
> records, targetable, and stealable.

## Gate Answers / Constraints

```text
Scope: redesign battle doc 058 only; no game data or code changes.
Allowed changes in design: active boss/support level plan, slot-risk notes, reward policy, positioning,
  and finale test criteria.
Chapter target: Chapter 4 final capstone, broken-but-readable and fair.
Must preserve: two-phase Hashmal -> Ultima structure, full HP/MP restore between phases, Ultima's
  Dispelja/Almagest identity, demon surround, low-HP transformation, and final win script.
Guests: no active guest. If future testing discovers any active guest/NPC, it must be player-controlled
  in NG+ and never used as a skill check.
Reward rule: no usable rewards inside 054-058. Ragnarok already pays at 053 and must not be awarded here.
```

## Original Battle

Objective:

```text
Defeat Hashmal!
Full HP/MP restore.
Defeat Ultima, including her transformed final form.
```

Player deployment:

```text
Up to 5 units, including Ramza. No outfitter: this is the final fight after the point of no return.
```

Original tactical identity:

```text
Phase 1: Hashmal / Lucavi wide-area pressure.
Interphase: scripted full HP/MP restore.
Phase 2: Ultima with demon surround, Dispelja, Almagest, and final transformation.
Campaign ends after Ultima's final form falls.
```

The finale is not the 5-star raw attrition peak; `057` owns that role. Airship Graveyard is the
adaptation capstone: survive Hashmal, use the restore, break Ultima's circle, rebuff after Dispelja,
heal through telegraphed Almagest, and burst the final form.

## Local Data Confirmed

Phase 1 dump:

```bash
python tools/entd_tool.py dump-entry --input src/fftivc.battles.ngplus/entd/battle_entd4_ent.bin --entry 440 --include-empty
```

Entry `440` confirmed active/scripted data:

| Slot | Status | Job | Level | JL | Secondary | Reaction | Support | Move | Equipment ids | Notes |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| 0 | Scripted/active record | 36 | 105 | 8 | 65 | 510 | 510 | 510 | 154,182,213,34,141 | Folmarv/Hashmal script record. Item `34` is Save the Queen; verify steal/target behavior. |
| 1 | Scripted/active record | 44 | 105 | 8 | 254 | 0 | 0 | 0 | 171,206,234,61,255 | Named demon/support record. |
| 2 | Scripted/active record | 64 | 105 | 0 | 112 | 0 | 0 | 0 | 255,255,255,255,255 | Hashmal/Lucavi record. |
| 3 | Scripted/active record | 44 | 104 | 0 | 0 | 0 | 0 | 0 | 255,255,255,255,255 | Support/form record. |
| 4 | Scripted/active record | 44 | 104 | 0 | 0 | 0 | 0 | 0 | 255,255,255,255,255 | Support/form record. |
| 5 | Scripted/active record | 44 | 104 | 0 | 0 | 0 | 0 | 0 | 255,255,255,255,255 | Support/form record. |

Phase 2 dump:

```bash
python tools/entd_tool.py dump-entry --input src/fftivc.battles.ngplus/entd/battle_entd4_ent.bin --entry 441 --include-empty
```

Entry `441` confirmed active/scripted data:

| Slot | Status | Job | Level | JL | Secondary | Reaction | Support | Move | Equipment ids | Notes |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| 0 | Scripted/form record | 49 | 105 | 0 | 0 | 0 | 0 | 0 | 255,255,255,255,255 | Lucavi/form record. |
| 1 | Scripted/form record | 49 | 105 | 0 | 0 | 0 | 0 | 0 | 255,255,255,255,255 | Lucavi/form record. |
| 2 | Active boss record | 20 | 105 | 8 | 0 | 430 | 0 | 0 | 171,206,234,61,255 | Ultima-related record; v2 target active final boss to level 106 after script verification. |
| 3 | Active monster | 154 | 105 | 0 | 0 | 0 | 0 | 0 | 255,255,255,255,255 | Ultima Demon. |
| 4 | Active monster | 154 | 105 | 0 | 0 | 0 | 0 | 0 | 255,255,255,255,255 | Ultima Demon. |
| 5 | Active monster | 154 | 105 | 0 | 0 | 0 | 0 | 0 | 255,255,255,255,255 | Ultima Demon. |
| 6 | Active monster | 154 | 105 | 0 | 0 | 0 | 0 | 0 | 255,255,255,255,255 | Ultima Demon. |
| 7 | Scripted/form record | 65 | 105 | 0 | 124 | 438 | 0 | 0 | 255,255,255,255,255 | Lucavi/form record. |
| 8 | Scripted/form record | 73 | 105 | 0 | 126 | 0 | 0 | 0 | 255,255,255,255,255 | Lucavi/form record. |

Data implications:

```text
- The finale is definitely two ENTD entries: 440 then 441.
- Current dump has all major finale records at 105. v2 design raises the active Ultima/final-form boss
  record(s) to 106 only after confirming which records drive the real boss/transform.
- Support records stay capped at 105. Do not overlevel supports above the final boss cap.
- Entry 440 slot 0 carries Save the Queen `34` and shield `141`. If that slot is targetable/stealable,
  implementation must swap those to non-reward gear or prove the items cannot leak.
- Entry 440 may also contain dormant reward/script data. Do not turn dormant rewards into awarded loot.
- No Ragnarok, no Save the Queen, no Excalibur, and no other unique steal/reward payload inside 058.
```

## Design Goal

Make the finale a grand but fair adaptation exam:

```text
Phase 1 asks the party to spread and handle Hashmal/Lucavi pressure.
The scripted restore resets HP/MP and makes Phase 2 fair after the 057 peak.
Phase 2 asks the party to break the demon surround, rebuff after Dispelja, survive telegraphed
sublethal Almagest, and burst Ultima through the transformation.
```

The headline engine is **two-phase adaptation under scripted Lucavi pressure**. Raw attrition already
peaked at `057`; this fight earns its climax by changing demands without deleting counterplay.

## Enemy Party Escalation

Accepted redesign: **v2 no-reward two-phase Ultima capstone**.

### Phase 1 - Hashmal / Lucavi entry 440

| Slot group | Role | Level target | Purpose |
|---|---|---:|---|
| Hashmal/Folmarv/Lucavi active record(s) | Phase boss | 105 | Wide-area pressure; defeat triggers phase transition. |
| Demon/support records | Screen / script support | 104-105 | Pressure and positioning, not hard lock. |

### Phase 2 - Ultima entry 441

| Slot group | Role | Level target | Purpose |
|---|---|---:|---|
| Active Ultima / final-form record(s) | Final boss | 106 | Single highest active boss in the mod. |
| Ultima Demon x4 | Surround | 105 | Positional/status pressure with Ribbon/spacing answers. |
| Lucavi/form records | Scripted transform/support records | 105 | Preserve transformation and win sequence. |

Why this works:

```text
- Ultima at 106 gives the finale the single-highest-boss identity.
- Supports stay 105 so the fight does not become raw level inflation.
- The full restore between phases is mandatory fairness after 057.
- Almagest is allowed only if telegraphed and sublethal.
- Dispelja is a soft reset answered by rebuffing.
- Demon surround is positional pressure answered by Ribbon/status prep, spacing, and burst.
- No usable reward appears here; Ragnarok already pays before the point of no return.
```

## Builds / Implementation Intent

### Phase 1 active boss/support records

```text
Level: 105 cap for active Hashmal/Folmarv/Lucavi records.
Primary: wide-area Lucavi pressure and scripted transition behavior.
Gear: verify all equipped unique-looking items. Save the Queen `34` must not be stealable/rewarded here.
Reward: none.
```

Guardrail: do not simplify or rewrite the phase. Preserve the scripts that transform/transition into
the second ENTD entry.

### Ultima / final form

```text
Level: 106 for the verified active final boss / final-form record(s).
Primary: Dispelja + Almagest + final Lucavi magic.
Almagest: telegraphed, sublethal, healable.
Dispelja: buff strip, answered by rebuffing.
Gear: no Ragnarok, no Excalibur, no unique reward payload.
Reward: none.
```

Guardrail: raising the wrong dormant/form record can break scripting. Identify active final boss records
before implementation.

### Ultima Demon surround and Lucavi/form support

```text
Level: 105 cap.
Ultima Demon jobs: 154 x4 in the dump.
Lucavi/form records: jobs 49/65/73 plus any script form records.
Pressure: positional surround, status/demon pressure, and support magic.
Reward: none.
```

Guardrail: surround must be answerable. No hard status pile-up, instant collapse, or support overleveling.

## Positioning Plan

```text
Phase 1: keep enough space for spread-vs-wide-area play.
Interphase: preserve the full HP/MP restore and any scripted repositioning.
Phase 2: place Ultima as the center of the final objective and use the four Ultima Demons as a circle
or partial surround. The surround should force immediate decisions without trapping all units.
```

The player read should be: spend enough to beat Hashmal, accept the restore, rebuff after Dispelja,
break the demon circle, heal through Almagest, and end Ultima's final form.

## Simulation Plan and Results

Artifact:

```text
tmp/fft-level-design-058-airship-graveyard/
```

Accepted candidate:

```text
v2 no-reward two-phase Ultima capstone
Phase 1 pressure: 140
Phase 2 pressure: 142
Adaptation score: 100
Finale identity: 100
Chain fairness: 100
Reward correctness: 100
Scripting fidelity: 100
```

Iteration notes:

```text
- Ultima must be the single highest active boss at 106; support records stay 105.
- The full restore between Hashmal and Ultima is mandatory fairness, not optional flavor.
- Almagest must remain telegraphed/sublethal; Dispelja must keep rebuff counterplay.
- Demon surround must be positional pressure with Ribbon/spacing answers, not a hard lock.
- Ragnarok, Save the Queen, and any unique steal payloads inside the finale were rejected by the reward
  ledger.
- Scripted support/form records are preserved; do not simplify the finale into solo Ultima.
```

Residual risks:

```text
- Confirm exactly which 440/441 slots are active, targetable, stealable, transform records, or dormant
  script records.
- Confirm the full HP/MP restore fires between phase 1 and phase 2.
- Confirm raising Ultima/form records to 106 does not break the low-HP transform or final win trigger.
- Confirm any equipped unique-looking items on scripted slots cannot leak as steals; otherwise swap them out.
```

## Rare / Reward Handling

```text
None. No usable NG++ reward is added inside the final gauntlet.
Ragnarok already pays at `053` through guaranteed Spoils of War and must not be awarded here.
Hashmal/Ultima/demon records must not leak dead post-game rewards or steal-only uniques.
Excalibur stays with Orlandeau and never appears on an enemy.
```

## Implementation Checklist

- [ ] Preserve the two-entry script: `440` phase 1 -> restore -> `441` phase 2.
- [ ] Verify which records are active combatants, targetable, stealable, dormant, or transform-only.
- [ ] Raise only the verified active Ultima/final-form boss record(s) to `106`.
- [ ] Keep active support records capped at `105`; do not overlevel support above Ultima.
- [ ] Preserve full HP/MP restore between phases.
- [ ] Preserve low-HP transformation and final win trigger.
- [ ] Keep Almagest telegraphed/sublethal and Dispelja rebuff-answerable.
- [ ] Keep demon surround answerable with Ribbon/status prep, spacing, and burst.
- [ ] Remove or prove non-leaking any unique-looking active/stealable equipment, especially Save the
      Queen `34` on entry `440` slot `0`.
- [ ] Add no usable reward, no Ragnarok, and no steal-dependent rare.
- [ ] Re-dump entries `440` and `441` after implementation and verify only intended level/gear/kit changes.
- [ ] Playtest `057 -> 058` and the full `054 -> 058` gauntlet.

## Test Questions

- Does the final still play as Hashmal -> restore -> Ultima -> final form?
- Is Ultima the only active level-106 enemy?
- Does the restore fire and make Phase 2 fair after the 057 peak?
- Are Almagest, Dispelja, and the demon surround scary but answerable?
- Are no usable NG++ rewards or unique steal payloads present?
- Does the finale feel climactic without becoming a scripted wipe?

## Sources

- Local: `docs/battles/ENDGAME-BLOCKER.md` for entry mapping and two-phase data.
- Local: `docs/battles/037-chapter-4-overview.md` for Chapter 4 finale principles and gauntlet curve.
- Local: `docs/battles/chapter-4-rewards-implementation.md` for the no-usable-reward rule in `054-058`.
- Local: `tmp/fft-level-design-058-airship-graveyard/` simulation artifact.
- Local dumps: `tools/entd_tool.py dump-entry --entry 440` and `--entry 441`.
- Game8, "Airship Graveyard Walkthrough (Battle 53 - Final Battle)": original phase structure and
  public finale framing.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553229
