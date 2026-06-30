# 017 - Tchigolith Fenlands

Status: ✅ implemented (v1, entry 410) — undead/status is the built-in escalation. **v2 redesign documented only** (implementation pending).
Chapter: 2 — "The Manipulator and the Subservient"
Battle order: Battle 16 (after Balias Tor)
Target version: Enhanced v1.5.0
ENTD: global entry **410** (battle_entd4, local entry 26) — confirmed by sequence + composition
File: `entd/battle_entd4_ent.bin` (embedded; swapped only in NG+ by the code mod)

> Implemented via `tools/battle_patch.py tchigolith`. NG+-only by construction. See
> `011-chapter-2-overview.md`.

## Original Battle

Objective:

```text
Defeat all enemies!
```

Player deployment:

```text
Up to 5 units, including Ramza. No guests.
```

Original enemy composition (fixed, all monsters):

```text
2x Ghoul        (undead)
2x Skeleton     (undead)
1x Bonesnatch   (undead — tougher skeleton)
1x Malboro      (mass status — Bad Breath)
1x Floating Eye (status / gaze)
```

Public walkthrough details:

```text
Recommended level: ~17 (2/5 stars on paper, but the terrain does the work).
Swamp map: bog tiles inflict POISON, and a poisoned/standing unit is then vulnerable to SLEEP.
Enemies can teleport across the field; safe elevated terrain is critical.
Undead / dark-aligned: HEALING magic DAMAGES them, and a Chemist's Phoenix Down INSTAKILLS them.
Malboro's Bad Breath can land a spread of bad statuses; the Floating Eye adds gaze status.
Recommended: an ALL-RANGED team (Archers, White Mages, Chemists) to fight from dry, safe tiles.
```

Design reading:

Tchigolith is **the undead-swamp horror** — the chapter's monster fight where the *terrain and
the status game* are the real enemy. It is the player's first encounter with **undead** (which
reraise/revive unless permakilled, and take damage from healing) layered on a **poison bog** that
softens you up for **sleep**, with a **Malboro** spreading mass status and **teleporting** foes
denying safe spacing. It teaches the player to fight ranged from dry ground, to **weaponize
healing/Phoenix Down against the undead**, and to respect status. The original is "easy" only if
you bring the right tools — which is the whole lesson.

For New Game++ the identity must stay: **a fetid bog where undead that won't stay dead, a
status-spewing Malboro, and poison/sleep terrain punish melee and reward a prepared ranged team
that turns healing into a weapon.**

## Local Data Confirmed (entry 410)

```text
slot  cid    job          monster              action
s0    0x22   34           Mustadio (disabled)  LEAVE (lvl 254)
s1    0x82   110          Bonesnatch (undead)  SCALE -> L101
s2    0x82   109          Skeleton (undead)    SCALE -> L100
s3    0x82   109          Skeleton (undead)    SCALE -> L101 (tougher of the pair)
s4    0x82   112          Ghoul (undead)       SCALE -> L100
s5    0x82   112          Ghoul (undead)       SCALE -> L100
s6    0x82   115          Floating Eye         SCALE -> L100
s7    0x82   130          Malboro              SCALE -> L101
s8    0x82   121          (disabled)           LEAVE (lvl 254)
```

Monster job IDs: Skeleton 109, Bonesnatch 110, Ghoul 112, Floating Eye 115, Malboro 130. Scaling is
**Level + JobLevel only** (no gear, no R-S-M, no job change), so the undead flags (reraise /
heal-damages-undead / Phoenix-Down-instakill — intrinsic to the job id + the flag byte we never
touch) and the swamp poison terrain are preserved. Only one mass-status disruptor (the Malboro);
none added.

## Enemy Pack Escalation (Chapter 2 redesign)

```text
VANILLA SPIRIT: undead in a poison bog, with one Malboro and one Floating Eye making status scary.
CHAPTER-2 UPGRADE: keep the status budget fixed and add one more elite undead body: a second
  Bonesnatch.
WHY: adding another Malboro or Floating Eye turns the fight into status spam. Adding a Bonesnatch
  increases undead attrition while preserving the clean counterplay: Phoenix Down, healing, Holy,
  and ranged dry-ground play.
WHAT IS NOT CHANGED: no humans, no gear, no extra status engine, no map flattening, no removal of
  undead flags.
```

Chapter 2 requirements applied:

```text
- No human enemies, so equipment/R/S/M rules do not apply.
- Every active monster is tuned through Level, JobLevel, Brave/Faith where relevant, and placement.
- Malboro count remains exactly one.
- Floating Eye count remains exactly one.
- Undead counterplay must remain intact.
```

## Boss rare loot

```text
None. No named boss here — no rare item (per the Chapter 2 overview). Monsters carry no gear.
```

## Proposed Composition (New Game++ Tchigolith v2)

Use eight monsters: the original roster plus one additional Bonesnatch. The pressure increase comes
from undead attrition, not more status.

| Slot | Monster | Level | Br/Fa | Purpose |
| ------ | --------- | ------- | --- | --------- |
| n | Ghoul (undead) | `100` | `80/35` | Undead body; reraises. Melee + status touch. |
| n | Ghoul (undead) | `100` | `80/35` | Second undead body; attrition. |
| n | Skeleton (undead) | `100` | `80/35` | Undead striker; reraises unless permakilled. |
| n | Skeleton (undead) | `101` | `80/35` | Tougher of the pair; pressures dry ground. |
| n | Bonesnatch (undead) | `102` | `80/35` | Elite undead anchor; the durable attrition threat. |
| n | Bonesnatch (undead) | `101` | `80/35` | Second elite undead; makes permakill tools matter. |
| n | Malboro | `102` | `78/35` | Bad Breath mass status — the single headline disruptor. |
| n | Floating Eye | `100` | `78/35` | Gaze status; chips and disables from range. |

Reasoning:

The faithful move is to **scale while preserving the mechanics**. The difficulty here is not a new
job engine; it is undead that revive, terrain that poisons, and one visible mass-status disruptor.
The second Bonesnatch makes the player commit to proper undead answers instead of clearing the bog
with generic burst. The Malboro remains one source only; the Floating Eye remains one source only.

## Monster / Terrain Tuning Notes

```text
Set JobLevel 8 on all monsters; keep aggressive Brave so they press onto the dry tiles you want.
PRESERVE undead flags: reraise/revive timers, heal-damages-undead, Phoenix-Down-instakill.
  Do NOT strip these — they are the fight's identity and its counterplay.
PRESERVE the swamp poison terrain and any sleep-follow-up; do NOT flatten the map to safe ground.
Malboro: keep Bad Breath but DO NOT stack additional mass-status monsters (one disruptor is the
  budget; more would cross into the "status spam" the project avoids).
Second Bonesnatch: place it where it threatens a dry-ground holdout from a different angle than the
  first, but do not let both start adjacent to the player.
Keep teleport/odd-movement on the monsters that have it so safe spacing stays a real problem.
```

## Positioning Plan

```text
Spread the undead across the bog between the player and the dry/elevated tiles, so the player
  must hold safe ground and fight ranged rather than wade in.
Malboro starts central with reach toward the player's likely safe cluster — the player must
  avoid clumping or eat Bad Breath.
Bonesnatches start split: one central, one offset, so Phoenix Down/Holy users must choose targets.
Floating Eye starts at range with a sightline to the player's dry holdout.
Preserve the swamp tiles and any elevated safe spots; do NOT pave the map.
```

The bog should say: "stay on dry ground, fight ranged, and kill the undead for good with the
right tools" — the original's lesson, lethal at scale.

## Simulation Plan and Results

Simulation artifact:

```text
tmp/fft-level-design-017-tchigolith-fenlands/
```

Model scope:

```text
First four rounds only; compares undead/status pressure. It rejects candidates that increase
mass-status sources instead of undead attrition.
```

Iteration results:

| Candidate | Monsters | Enemy actions | Action ratio | Pressure | Delta vs v1 | Result |
|-----------|----------|---------------|--------------|----------|-------------|--------|
| v1 current: 2 Ghoul, 2 Skeleton, 1 Bonesnatch, 1 Malboro, 1 Eye | 7 | 24.6 | 1.23 | 62.4 | 0.0% | Baseline |
| Add second Malboro | 8 | 27.8 | 1.39 | 76.0 | +21.8% | Rejected: mass status spam |
| Add second Floating Eye | 8 | 28.4 | 1.42 | 71.2 | +14.1% | Rejected: status stack |
| Add second Bonesnatch | 8 | 28.2 | 1.41 | 72.0 | +15.4% | Accepted |

Decision:

```text
Add one Bonesnatch. Keep exactly one Malboro and one Floating Eye. Preserve undead counterplay and
do not add human enemies or extra status engines.
```

## Current Implementation (v1, entry 410 — superseded by v2 design)

Applied with `python tools/battle_patch.py tchigolith`; diff contained to local entry 26 (global
410), 14 bytes. Three tougher monsters (Bonesnatch s1, tougher Skeleton s3, Malboro s7) → L101; the
two Ghouls, the other Skeleton, and the Floating Eye → L100; JobLevel 8 on all seven. The undead/
status mechanic IS the escalation — no monster added.

This implementation remains the shipped v1 data. The v2 redesign above is **documentation only** in
this pass; it requires a later ENTD implementation pass to add or convert one monster into the second
Bonesnatch and keep status source counts unchanged.

## Future Implementation Checklist (v2)

- [x] Identify Tchigolith ENTD entry (410); fill "Local Data Confirmed".
- [x] Dump original entry; verify 7-monster undead roster (+ disabled s8).
- [x] Confirm monster job IDs; undead flags persist (Level/JobLevel-only edit, job/flags untouched).
- [x] Swamp terrain untouched (not edited at all — terrain is not in the ENTD slot data).
- [ ] Add or convert one monster into a second Bonesnatch; do not add another Malboro or Floating Eye.
- [ ] Set levels: elite Bonesnatch + Malboro `102`; second Bonesnatch + tougher Skeleton `101`;
  Ghouls, other Skeleton, Floating Eye `100`.
- [ ] Set JobLevel `8` on all active monsters; no equipment.
- [ ] Keep ONE mass-status monster (Malboro) and ONE gaze/status support (Floating Eye).
- [ ] Patch the embedded ENTD in a later implementation pass; no binary/data change in this doc pass.
- [ ] Re-dump and diff; changes small and intentional.
- [ ] Playtest from a NG+ save; verify undead reraise + Phoenix-Down-kill still work.

## Test Questions

- Do the undead genuinely reraise, forcing the player to permakill them (Phoenix Down / Holy)?
- Is "weaponize healing against the undead" rewarded the way the original taught, at scale?
- Does the poison/sleep bog punish melee and reward a ranged holdout on dry ground?
- Is Malboro's Bad Breath a real threat without tipping into oppressive status spam?
- Does the second Bonesnatch make undead permakill tools matter without creating a cleanup slog?
- Does teleportation keep safe spacing a genuine problem?
- Is it a distinct fight from the other Chapter 2 battles — a status/attrition horror, not a brawl?
- Is it fair at NG+ for a prepared party and punishing for an unprepared one, as intended?

## Sources

- Game8, "Tchigolith Fenlands Walkthrough (Battle 16)": fixed roster (2 Ghoul, 2 Skeleton,
  1 Bonesnatch, 1 Malboro, 1 Floating Eye), objective "Defeat all enemies!", deploy 5,
  recommended level ~17, swamp poison terrain + sleep follow-up, undead heal-weakness +
  Phoenix-Down-instakill, teleporting foes, all-ranged-team recommendation.
  https://game8.co/games/Final-Fantasy-Tactics/archives/552765
- Final Fantasy Wiki: undead mechanics (reraise, healing damages undead).
  https://finalfantasy.fandom.com/wiki/Undead_(status)
- Local: `docs/battles/011-chapter-2-overview.md` (enemy-party escalation rule), `003-siedge-weald.md`
  (monster-fight handling), `013-araguay-woods.md` (monster tuning).
</content>
