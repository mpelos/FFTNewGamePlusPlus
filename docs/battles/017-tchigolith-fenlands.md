# 017 - Tchigolith Fenlands

Status: ✅ implemented (v1, entry 410) — undead/status is the built-in escalation
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

## Job Escalation (Chapter 2 rule)

```text
THE NEW JOBS ARE BUILT IN: this battle canonically debuts the UNDEAD (Ghoul/Skeleton/Bonesnatch)
plus a status Malboro and Floating Eye — none seen earlier in the mod. The undead-reraise +
heal-as-weapon mechanic AND the poison/sleep swamp ARE this fight's escalation; per the "one new
wrinkle" rule, NO additional job is added. Keep the 7-monster roster intact.
WHY: undead that won't stay dead, on status terrain, with mass-status support, is already a
  dense new puzzle. Adding a human commander or more archetypes would muddy it.
```

## Boss rare loot

```text
None. No named boss here — no rare item (per the Chapter 2 overview). Monsters carry no gear.
```

## Proposed Composition (New Game++ Tchigolith v1)

Keep the exact 7-monster roster; scale and preserve the undead/terrain mechanics. The tougher
undead and the Malboro at `101`, the rest at `100`.

| Slot | Monster | Level | Purpose |
|------|---------|-------|---------|
| n | Ghoul (undead) | `100` | Undead body; reraises. Melee + status touch. |
| n | Ghoul (undead) | `100` | Second undead body; attrition. |
| n | Skeleton (undead) | `100` | Undead striker; reraises unless permakilled. |
| n | Skeleton (undead) | `101` | Tougher of the pair; pressures dry ground. |
| n | Bonesnatch (undead) | `101` | Elite undead; the durable attrition threat. |
| n | Malboro | `101` | Bad Breath mass status — the headline disruptor. |
| n | Floating Eye | `100` | Gaze status; chips and disables from range. |

Reasoning:

The faithful move is to **scale while preserving the mechanics** — the difficulty here is not
big numbers, it's **undead that revive**, **mass status**, and **terrain**. Keeping the undead
flags means a player who doesn't exploit Phoenix Down / Holy faces endless attrition, exactly as
intended; the Malboro at `101` makes Bad Breath a real threat at party level; the bog keeps
punishing melee. A prepared all-ranged team that weaponizes healing is rewarded — the original's
whole point, now with teeth.

## Monster / Terrain Tuning Notes

```text
Set JobLevel 8 on all monsters; keep aggressive Brave so they press onto the dry tiles you want.
PRESERVE undead flags: reraise/revive timers, heal-damages-undead, Phoenix-Down-instakill.
  Do NOT strip these — they are the fight's identity and its counterplay.
PRESERVE the swamp poison terrain and any sleep-follow-up; do NOT flatten the map to safe ground.
Malboro: keep Bad Breath but DO NOT stack additional mass-status monsters (one disruptor is the
  budget; more would cross into the "status spam" the project avoids).
Keep teleport/odd-movement on the monsters that have it so safe spacing stays a real problem.
```

## Positioning Plan

```text
Spread the undead across the bog between the player and the dry/elevated tiles, so the player
  must hold safe ground and fight ranged rather than wade in.
Malboro starts central with reach toward the player's likely safe cluster — the player must
  avoid clumping or eat Bad Breath.
Floating Eye starts at range with a sightline to the player's dry holdout.
Preserve the swamp tiles and any elevated safe spots; do NOT pave the map.
```

The bog should say: "stay on dry ground, fight ranged, and kill the undead for good with the
right tools" — the original's lesson, lethal at scale.

## Implemented (v1, entry 410)

Applied with `python tools/battle_patch.py tchigolith`; diff contained to local entry 26 (global
410), 14 bytes. Three tougher monsters (Bonesnatch s1, tougher Skeleton s3, Malboro s7) → L101; the
two Ghouls, the other Skeleton, and the Floating Eye → L100; JobLevel 8 on all seven. The undead/
status mechanic IS the escalation — no monster added.

## Implementation Checklist

- [x] Identify Tchigolith ENTD entry (410); fill "Local Data Confirmed".
- [x] Dump original entry; verify 7-monster undead roster (+ disabled s8).
- [x] Confirm monster job IDs; undead flags persist (Level/JobLevel-only edit, job/flags untouched).
- [x] Swamp terrain untouched (not edited at all — terrain is not in the ENTD slot data).
- [x] Set levels: tougher Skeleton + Bonesnatch + Malboro `101`; the rest `100`.
- [x] Set JobLevel `8` on all scaled monsters; no equipment.
- [x] Keep ONE mass-status monster (Malboro); none added.
- [x] Patch the embedded ENTD (NG+-only); diff inside entry 410 only.
- [x] Re-dump and diff; changes small and intentional.
- [ ] Playtest from a NG+ save; verify undead reraise + Phoenix-Down-kill still work.

## Test Questions

- Do the undead genuinely reraise, forcing the player to permakill them (Phoenix Down / Holy)?
- Is "weaponize healing against the undead" rewarded the way the original taught, at scale?
- Does the poison/sleep bog punish melee and reward a ranged holdout on dry ground?
- Is Malboro's Bad Breath a real threat without tipping into oppressive status spam?
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
- Local: `docs/battles/011-chapter-2-overview.md` (job-escalation rule), `003-siedge-weald.md`
  (monster-fight handling), `013-araguay-woods.md` (monster tuning).
</content>
