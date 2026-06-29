# 022 - Lionel Castle Oratory — Cúchulainn (Lionel Castle Keep)

Status: ✅ implemented (v1, entry 425) — CHAPTER 2 COMPLETE (rare loot deferred to reward table). **v2 redesign documented only** (implementation pending).
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

## Enemy Party Escalation (Chapter 2 redesign)

```text
VANILLA SPIRIT: the first Lucavi reveal; a single demon that fights like an army through mass
  status, run-up execution, dark/poison identity, and Holy weakness.
CHAPTER-2 UPGRADE: keep Cúchulainn solo at level `104` and make the fight explicitly chain-aware:
  it must be tested immediately after Lionel Gate, with no resupply and moderate resource tax.
WHY: Cúchulainn has no gear, no allies, and no party synergy. The fair Chapter 2 spike is the
  demon's Nightmare/Holy pattern under chain pressure, not a higher hidden stat wall.
WHAT IS NOT CHANGED: Nightmare remains telegraphed, Holy remains decisive, and the answer is still
  spread/cleanse/Immobilize/Holy burst.
```

Chapter 2 requirements applied:

```text
- No active human enemies exist, so equipment and R/S/M completeness do not apply here.
- No active guests are present.
- No minions, no second mass-status source, no instant Nightmare, and no removed Holy weakness.
- Keep level `104` as the Chapter 2 capstone band unless a later implementation review explicitly
  reopens the chapter-level policy.
- Reward handling is outside the monster ENTD slot: 108 Gems should be a reward-table/battle reward,
  not fake equipment on the Unarmed Lucavi slot.
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
  "no best equipment yet" rule. Second rare boss reward of the mod (after Gaffgarion's Blood Sword).
ALT if 108 Gems is unsuitable on the demon's slot: a Cursed Ring (flavor) or a Mage's Cloak-tier
  rare. Verify Cúchulainn's ENTD slot supports an accessory + rare drop/steal; if the Lucavi unit
  cannot carry equipment, assign the rare as a GUARANTEED battle reward/treasure instead.
DO NOT use the rare-variant treasure already in the room (e.g. Bizen Osafune katana) as the boss
  drop — keep the boss's signature item distinct and demon-themed.
```

## Proposed Composition (New Game++ Oratory v2)

A single boss, scaled as the chapter spike. Cúchulainn stays at `104`; the v2 requirement is that
the fight must be validated from the Lionel Gate no-resupply chain, not from a fresh save.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Cúchulainn (BOSS) | Lucavi Demon | `104` | One-unit army: Nightmare mass-status + run-up execute; weak to Holy; dark-absorb. |

Reasoning:

The faithful move is to **scale the lone demon as a fair spike and preserve every mechanic**. At
`104`, Cúchulainn should threaten a full tuned party alone, but the fight stays solvable by
tactics: spread to deny Nightmare's multi-target value, Immobilize to stop executes, cleanse
Doom/Sleep, and burn him down with Holy. Keep the Holy weakness and dark-absorb so build choice
matters, and keep Nightmare telegraphed so spacing/cleansing is enough. The no-resupply lead-in
means the player must arrive from the Gate with reserves. If playtest shows Holy trivializes the
fight, reopen tuning explicitly; do not solve it with minions, instant Nightmare, or removing Holy.

## Boss Tuning Notes (no equipment levers — it's a monster)

```text
V2 target: keep Cúchulainn's Level byte at 104; keep his canonical JobLevel / innate skillset and
  Brave.
PRESERVE: Holy weakness, dark/poison ABSORB (heal-from-dark), Nightmare (Doom/Sleep) + run-up,
  and any Blood Suck / drain in his kit. These ARE the fight.
DO NOT: add minions, add a second mass-status source, make Nightmare instant, or remove the Holy
  weakness (that weakness is the intended "bring Agrias/Holy" counter and keeps the spike fair).
Assign the rare (108 Gems) as his drop/steal if the slot allows; else as a guaranteed reward.
Verify HP is high enough to threaten a level-104-scaled party of 5 arriving from Lionel Gate, but
  not so high that a Holy-leaning party can't win in a reasonable number of turns.
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

## Simulation Plan and Results

Simulation artifact:

```text
tmp/fft-level-design-022-lionel-castle-oratory/
```

Model scope:

```text
First four rounds only; compares a fresh-state reference, the real Gate-chain baseline, solo-boss
pressure, counterplay, and chain tax. It rejects minions, instant Nightmare, removed Holy weakness,
and HP-wall tuning.
```

Iteration results:

| Candidate | Enemies | Boss level | Boss actions | Effective pressure | Counterplay | Chain tax | Delta vs chain v1 | Result |
|-----------|---------|------------|--------------|--------------------|-------------|-----------|-------------------|--------|
| v1 solo demon from fresh state | 1 | 104 | 3.5 | 45.6 | 100.0 | 0.0 | -46.4% | Fresh reference |
| v1 solo demon from Gate chain | 1 | 104 | 3.5 | 85.0 | 100.0 | 24.6 | +0.0% | Chain baseline |
| Add Lucavi minions | 3 | 104 | 9.5 | 127.0 | 72.0 | 24.6 | +49.4% | Rejected: breaks solo Lucavi identity |
| Instant Nightmare | 1 | 104 | 3.5 | 179.6 | 65.0 | 24.6 | +111.3% | Rejected: unfair status cadence |
| Remove Holy weakness HP wall | 1 | 104 | 3.5 | 127.0 | 62.0 | 24.6 | +49.4% | Rejected: removes intended answer |
| v2 chain-aware solo Lucavi | 1 | 104 | 3.5 | 97.5 | 100.0 | 24.6 | +14.7% | Accepted |

Decision:

```text
Keep Cúchulainn solo at level `104` and make the v2 requirement chain-aware playtesting from Lionel
Gate. Do not add minions, remove Holy weakness, or make Nightmare instant. Put 108 Gems in the
reward path, not on the Unarmed ENTD slot.
```

## Current Implementation (v1, entry 425 — superseded by v2 design)

Applied with `python tools/battle_patch.py cuchulainn`; diff contained to local entry 41 (global
425), **1 byte** (level 25 → 104). Level-only scaling preserves the entire demon kit.

This implementation remains the shipped v1 data. The v2 redesign above is **documentation only** in
this pass; it requires a later implementation pass to test the Gate->Oratory chain as a chain and
wire the 108 Gems reward through the reward-table path.

## Future Implementation Checklist (v2)

- [x] Identify Oratory/Keep ENTD entry (425); fill "Local Data Confirmed".
- [x] Dump original entry; verify Cúchulainn is the SOLE active enemy (s9) + disabled cutscene actors.
- [x] Confirm demon job (60); Holy weakness + dark-absorb + Nightmare + run-up preserved (level-only edit).
- [ ] Keep Level `104`; test from the Lionel Gate no-resupply chain, not from a fresh save.
- [ ] Preserve canonical innate skillset / JobLevel 8 / Brave.
- [ ] Assign 108 Gems — DEFERRED: Unarmed monster has no gear slot; needs the reward table (not ENTD).
- [ ] Keep one mass-status source (the boss); no minions/second disruptor added.
- [ ] Preserve small-arena geometry (terrain not in ENTD slot data).
- [ ] Patch the embedded ENTD in a later implementation pass; no binary/data change in this doc pass.
- [ ] Re-dump and diff; change should remain minimal; kit intact.
- [ ] Playtest from a NG+ save (arriving from the Gate, no resupply); confirm Holy is decisive and
      Nightmare is survivable with spacing/cleansing.

## Test Questions

- Does Cúchulainn at `104` threaten a full tuned party ALONE when tested after Lionel Gate?
- If Holy burst trivializes the fight, can tuning be reopened without adding minions or removing Holy?
- Is Nightmare scary but counterable by spreading out + status cleansing (not an unavoidable wipe)?
- Is the Holy weakness clearly the intended answer — does a Holy-leaning party melt him fairly?
- Does dark-absorb punish a player who brings dark damage (build choice matters)?
- Does Immobilize/Leg Shot meaningfully stop his run-up executes?
- Does the no-resupply lead-in make resource discipline matter without being unfair?
- Does the reward-table path grant a MID-TIER demon-themed rare (108 Gems) — no Ch4-reserved best gear leaked?
- Are minions, instant Nightmare, and extra status sources still absent?
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
