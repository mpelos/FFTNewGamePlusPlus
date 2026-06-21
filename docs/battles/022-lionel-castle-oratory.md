# 022 - Lionel Castle Oratory — Cúchulainn (Lionel Castle Keep)

Status: ✅ implemented (v1, entry 425) — CHAPTER 2 COMPLETE (rare loot deferred to reward table)
Chapter: 2 — "The Manipulator and the Subservient" (CHAPTER FINALE)
Battle order: Battle 21 (after Lionel Castle Gate)
Target version: Enhanced v1.5.0
ENTD: global entry **425** (battle_entd4, local entry 41) — confirmed: sole demon, job 60 (Gigas/Demon)
File: `entd/battle_entd4_ent.bin` (embedded; swapped only in NG+ by the code mod)

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `011-chapter-2-overview.md`. (Game8 labels this room "Lionel Castle Keep"; in-story it is
> the Oratory where the Cardinal reveals himself as the demon.)

## Original Battle

Objective:

```text
Defeat Cúchulainn!  (a single-target boss kill — the Cardinal transforms into the demon)
```

Player deployment:

```text
Up to 5 units, including Ramza. No guests.
NOTE: this immediately follows Lionel Castle Gate (Gaffgarion) with NO resupply between fights —
  the player arrives with whatever HP/MP/items survived the previous battle.
```

Original enemy composition:

```text
1x Cúchulainn   (Lucavi ZODIAC DEMON — a one-unit "army"; the only enemy on the field)
```

Public walkthrough details:

```text
Recommended level: ~23.  Difficulty: 4/5 stars.
Cúchulainn is a Zodiac Demon whose skills inflict NASTY STATUS:
  - NIGHTMARE: hits from range with a high chance of DOOM or SLEEP on MANY targets, then he runs
    up on later turns to one-hit-KO the disabled units.
  - (vanilla kit also includes dark/drain-flavored attacks, e.g. Blood Suck, and poison/Bio.)
WEAKNESS: Cúchulainn is WEAK TO HOLY — Holy Sword skills (Agrias) and Holy magic shred him.
COUNTERS the guide names: spread out (avoid overlapping his AoE), keep RANGED units attacking
  safely on the small arena, use Mustadio's Leg Shot to IMMOBILIZE him (stop the run-up), bring
  status cleansing (Chemist Remedy / Esuna), and lean on Holy damage.
The arena is small; ranged units can keep firing; spreading prevents multi-target status.
```

Design reading:

The Oratory is **the chapter's horror finale** — the first **Lucavi demon**, a lone monstrous boss
that fights like a whole army. Its identity is a **status-and-spacing duel**: Nightmare threatens
mass Doom/Sleep at range, then the demon closes to execute the disabled, so the player must **spread
out**, **cleanse status**, **lock him down** (Immobilize/Leg Shot), and **exploit his Holy
weakness** to burst him before attrition wins. It is the payoff to the chapter's rising monstrous
threat (after the undead and the Dark Knight), and the first **non-human boss with a rare drop**.
The no-resupply lead-in from the Gate makes resource discipline part of the test.

For New Game++ the identity must stay: **a lone Lucavi demon that mass-disables at range and
one-shots the disabled, beaten by spacing, status-cleansing, lockdown, and HOLY burst — a
spike-but-fair chapter capstone, not a numbers wall.**

## Local Data Confirmed (entry 425)

```text
slot   cid    flags  job              role                       action
s0-s7  0x28/  0x80   40 / 2           Cardinal Draclau + guards  LEAVE (lvl 254 cutscene actors)
       0x02                           + Ramza placeholder
s8     0x82   0x40   94 Chocobo       disabled                   LEAVE (lvl 254)
s9     0x3c   0x20   60 Gigas/Demon   Cúchulainn (SOLE enemy)    SCALE -> L104 (level only)
```

Cúchulainn is **job 60 (Gigas/Demon)** — a monster that equips Unarmed only, so scaling is
**level only** (104, the chapter's top band). Nothing else is touched, so his full canonical kit —
Nightmare (mass Doom/Sleep) + run-up execute, Holy weakness, dark/poison absorb, Blood Suck — and
his JobLevel 8 are preserved intact. The Cardinal/guards/Ramza/chocobo are disabled cutscene
placeholders (the Cardinal transforms into the demon via scripting), all left at lvl 254.

### Rare loot (108 Gems) — deferred to a reward-table pass

Cúchulainn's job (60) is **Unarmed — it has no equipment slot**, so 108 Gems cannot be set on his
ENTD slot. A guaranteed drop/treasure lives in a separate reward table (not the ENTD), which this
`.bin` patcher does not touch. The rare loot is therefore deferred to a future reward-table pass;
the boss scaling and all his mechanics are fully implemented.

## Job Escalation (Chapter 2 rule)

```text
THE NEW "JOB" IS THE DEMON ITSELF: Cúchulainn is the first Lucavi — a one-unit army with a
mass-status + Holy-weakness pattern unlike anything earlier in the mod. The demon IS this fight's
escalation; per "one new wrinkle per fight," there are NO generic jobs to add (it is a solo boss).
WHY: a lone boss that mass-disables and executes, with an elemental-weakness puzzle, is already
  the densest single-fight challenge of the chapter. Adding adds/minions would dilute the duel and
  blunt the "spread out vs his AoE" lesson.
```

## Sanctioned exception — boss mass-status (Nightmare)

```text
Cúchulainn's NIGHTMARE (mass Doom/Sleep) is allowed as a BOSS signature, NOT generic status spam:
ALLOWED: Nightmare + dark/drain attacks on the single demon.
GUARDRAILS: ONE status source (the boss); it is telegraphed (ranged cast, then run-up), and the
  game itself names the counters (spread out, Immobilize/Leg Shot, Remedy/Esuna cleansing, Holy
  burst). Keep his charge/turn cadence so the player has time to react — do NOT make Nightmare
  instant or stack a second mass-status source. This is the chapter's deliberate exception, mirrored
  on the undead/Malboro budget (017): exactly one disruptor at a time.
```

## Boss rare loot

```text
Cúchulainn -> 108 GEMS (accessory; non-buyable — rare poach/treasure in vanilla).
WHY IT FITS: a demon's trinket that grants broad elemental damage reduction — thematically apt for
  a Lucavi, and a tempting steal target. It is clearly MID-TIER (a defensive utility accessory),
  well below the Chapter-4-reserved best gear (Ribbon, Genji set, best robes), so it respects the
  "no best equipment yet" rule. Second rare boss drop of the mod (after Gaffgarion's Ancient Sword).
ALT if 108 Gems is unsuitable on the demon's slot: a Cursed Ring (flavor) or a Mage's Cloak-tier
  rare. Verify Cúchulainn's ENTD slot supports an accessory + rare drop/steal; if the Lucavi unit
  cannot carry equipment, assign the rare as a GUARANTEED battle reward/treasure instead.
DO NOT use the rare-variant treasure already in the room (e.g. Bizen Osafune katana) as the boss
  drop — keep the boss's signature item distinct and demon-themed.
```

## Proposed Composition (New Game++ Oratory v1)

A single boss, scaled as the chapter spike. Cúchulainn at `104` — the highest band of Chapter 2.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Cúchulainn (BOSS) | Lucavi Demon | `104` | One-unit army: Nightmare mass-status + run-up execute; weak to Holy; dark-absorb. |

Reasoning:

The faithful move is to **scale the lone demon as a fair spike and preserve every mechanic**. At
`104` (the chapter's top band, +1 over the Gaffgarion boss) with intact Lucavi stats, Cúchulainn
threatens a full party alone — but the fight stays **solvable by tactics, not levels**: spread to
deny Nightmare's multi-target value, Immobilize to stop the executes, cleanse Doom/Sleep, and burn
him down with Holy (his weakness). Keep the Holy weakness and dark-absorb so build choice matters
(bring Holy, leave dark home), and keep Nightmare telegraphed so spacing/cleansing is enough. The
no-resupply lead-in means the player must arrive from the Gate with reserves — resource discipline
is part of the capstone, without an unfair numbers wall.

## Boss Tuning Notes (no equipment levers — it's a monster)

```text
Set Cúchulainn's Level 104; keep his canonical JobLevel / innate skillset and Brave.
PRESERVE: Holy weakness, dark/poison ABSORB (heal-from-dark), Nightmare (Doom/Sleep) + run-up,
  and any Blood Suck / drain in his kit. These ARE the fight.
DO NOT: add minions, add a second mass-status source, make Nightmare instant, or remove the Holy
  weakness (that weakness is the intended "bring Agrias/Holy" counter and keeps the spike fair).
Assign the rare (108 Gems) as his drop/steal if the slot allows; else as a guaranteed reward.
Verify HP is high enough to threaten a level-104-scaled party of 5 but not so high that a
  Holy-leaning party can't win in a reasonable number of turns (Holy should feel decisive).
```

## Positioning Plan

```text
Cúchulainn starts centered in the small Oratory arena with range to the player's deployment.
The player should be able to spread on entry (deny Nightmare's multi-hit) and keep ranged/Holy
  units firing from safe tiles — preserve the compact arena that makes "spread out" meaningful.
No minions, no reinforcements: the whole field is the player vs the demon.
```

The Oratory should say: "a single demon, but it fights like an army — spread out, cleanse the
nightmares, pin it down, and bring the Light."

## Implemented (v1, entry 425)

Applied with `python tools/battle_patch.py cuchulainn`; diff contained to local entry 41 (global
425), **1 byte** (level 25 → 104). Level-only scaling preserves the entire demon kit.

## Implementation Checklist

- [x] Identify Oratory/Keep ENTD entry (425); fill "Local Data Confirmed".
- [x] Dump original entry; verify Cúchulainn is the SOLE active enemy (s9) + disabled cutscene actors.
- [x] Confirm demon job (60); Holy weakness + dark-absorb + Nightmare + run-up preserved (level-only edit).
- [x] Set Level `104`; canonical innate skillset / JobLevel 8 / Brave kept.
- [ ] Assign 108 Gems — DEFERRED: Unarmed monster has no gear slot; needs the reward table (not ENTD).
- [x] One mass-status source (the boss); no minions/second disruptor added.
- [x] Small-arena geometry untouched (terrain not in ENTD slot data).
- [x] Patch the embedded ENTD (NG+-only); diff inside entry 425 only.
- [x] Re-dump and diff; change is minimal (level only); kit intact.
- [ ] Playtest from a NG+ save (arriving from the Gate, no resupply); confirm Holy is decisive and
      Nightmare is survivable with spacing/cleansing.

## Test Questions

- Does Cúchulainn threaten a full level-104 party ALONE (true one-unit-army feel)?
- Is Nightmare scary but counterable by spreading out + status cleansing (not an unavoidable wipe)?
- Is the Holy weakness clearly the intended answer — does a Holy-leaning party melt him fairly?
- Does dark-absorb punish a player who brings dark damage (build choice matters)?
- Does Immobilize/Leg Shot meaningfully stop his run-up executes?
- Does the no-resupply lead-in make resource discipline matter without being unfair?
- Does he drop a MID-TIER demon-themed rare (108 Gems) — no Ch4-reserved best gear leaked?
- Is it the clear hardest fight of Chapter 2 (4/5★ capstone) yet solvable by tactics, not grinding?

## Sources

- Game8, "Lionel Castle Keep Walkthrough (Battle 21)": sole enemy Cúchulainn, objective "Defeat
  Cúchulainn!", recommended level ~23, 4/5 stars, deploy 5, Holy weakness, Nightmare mass-status
  (Doom/Sleep) + run-up one-shots, Leg Shot to Immobilize, spread-out small arena, rewards/treasure.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553181
- Final Fantasy Wiki, "Cúchulainn (Tactics)": Lucavi kit (Nightmare, Blood Suck, dark-absorb),
  Holy weakness.
  https://finalfantasy.fandom.com/wiki/C%C3%BAchulainn_(Tactics)
- Final Fantasy Wiki, "Lionel Castle": story/terrain context.
  https://finalfantasy.fandom.com/wiki/Lionel_Castle
- Local: `docs/battles/011-chapter-2-overview.md` (rare-boss-loot rule), `017-tchigolith-fenlands.md`
  (one-disruptor mass-status budget), `021-lionel-castle-gate.md` (no-resupply lead-in; first rare drop),
  `008-fovoham-windflats.md` (Wiegraf — boss-with-elemental-mechanic precedent).
</content>
