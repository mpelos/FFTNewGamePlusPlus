# 032 - The Yuguewood (Yuguo Woods)

Status: ✅ implemented (v1, entry 430) — NG+ only; pending playtest. **v2 redesign documented only** (implementation pending).
Chapter: 3 — "The Valiant"
Battle order: Battle 29 (after Walled City of Yardrow)
Target version: Enhanced v1.5.0
ENTD: global entry **430** (local entry 46, `battle_entd4_ent.bin`)
File: `battle_entd4_ent.bin` (embedded NG+ swap) — `tools/battle_patch.py yuguewood`

Implemented composition (entry 430, vanilla-dump verified). Roster match confirms the entry
(enemy-variant mage job ids: **66 = Black Mage** (equips Rod), **68 = Time Mage** (equips Staff) —
distinct from the player-generic 80/81):
- s1,s3 Black Mage (66) L101/L100 — Mage Hat/shop Robe/Featherweave/shop Rod; jl8; Reflexes/Atk Boost/Mv+1.
- s2,s4 Time Mage (68) L101 — Mage Hat/shop Robe/Featherweave/shop **Staff**; **jl CAPPED to 4**
  (Haste/Slow/Float only — no Stop/Immobilize); Reflexes/Mv+1.
- s5 Ghoul (112) L100, s6 Ghast (113) L100, s7 Revenant (114) L101 — level+jl only (monsters, no gear);
  undead reraise/heal-weakness/Seal-Evil/Entice flags + swamp terrain untouched.
- s0 = Rapha placeholder (level 0xFE) — left untouched. No boss → no rare.

> ⚠️ Verify in-game: the undead sit at level 0xFE in the base .bin (the norm for undead game-wide).
> We scale their .bin level per the tchigolith (410) precedent, but if the enhanced edition's
> OverrideEntryData drives undead levels for this entry, that layer wins — confirm the undead actually
> scale (if not, move their levels to the override layer).

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `024-chapter-3-overview.md`.

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
1x Ghoul     (undead — reraises; status touch)
1x Ghast     (undead — reraises; status touch)
1x Revenant  (undead — reraises; tougher body)
2x Black Mage (ranged elemental magic)
2x Time Mage  (Haste the undead / Slow the player)
```

Public walkthrough details:

```text
Recommended level: ~33.  Difficulty: 2/5 stars.
Swamp woods with mobility challenges (soft/awkward terrain).
The undead RERAISE and revive unless permakilled; HEALING magic DAMAGES them, and a Chemist's
  Phoenix Down / Hi-Potion INSTAKILLS them. Mustadio's SEAL EVIL petrifies them out of the fight,
  and an Orator's ENTICE can flip an undead to your side (Traitor).
The Black Mages add ranged elemental damage; the Time Mages HASTE the undead (more attacks) and
  SLOW the player.
```

Design reading:

The Yuguewood is **the second undead fight — now with a living caster backline**. Where Tchigolith
(`017`) was a pure-monster undead bog, Yuguo pairs reraising undead with **Black Mage magic and
Time-Mage tempo**: the undead won't stay dead (permakill with Phoenix Down / Holy / Seal Evil),
while the casters shell you from range and **Haste the undead** so they swing more often and **Slow**
your cleanup. The swamp hampers movement, making the attrition bite. The lesson builds on Tchigolith
— *weaponize healing against the undead, permakill them* — but adds **tempo and ranged pressure**,
so the player must close the kill faster before the Hasted dead and the mages grind them down. The
player's own anti-undead tools (Phoenix Down, Holy, Seal Evil, even Entice) are richly rewarded.

For New Game++ the identity must stay: **a swampy undead attrition fight where reraising dead must be
permakilled with healing/Holy/Seal Evil, now Hasted by Time Mages and shelled by Black Mages —
won by closing the permakill faster under tempo and ranged pressure.**

## Local Data Confirmed

```text
ENTD entry 430 confirmed in `024-chapter-3-overview.md` and v1 implementation.
Roster: 1 Ghoul + 1 Ghast + 1 Revenant + 2 Black Mage + 2 Time Mage, plus the player slots.
CRITICAL: preserve the UNDEAD flags (reraise/revive + heal-damages-undead + Phoenix-Down-instakill +
  Seal-Evil-petrify + Entice-able) on the Ghoul/Ghast/Revenant. These ARE the fight.
Keep the swamp terrain / mobility flags (the bog is part of the attrition).
Keep Time Mage to Haste/Slow/Float only; keep Black Mage cast cadence normal.
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
```

Job/monster IDs:

```text
66 = enemy-variant Black Mage (confirmed; equips Rod)
68 = enemy-variant Time Mage (confirmed; equips Staff)
112 = Ghoul (confirmed undead monster)
113 = Ghast (confirmed undead monster)
114 = Revenant (confirmed undead monster)
```

## Enemy Party Escalation (Chapter 3 redesign)

```text
VANILLA SPIRIT: reraising undead in swamp terrain must be permakilled with healing/Holy/Seal Evil
  while living casters punish slow cleanup.
CHAPTER-3 UPGRADE: keep the exact 3 undead / 2 Black Mage / 2 Time Mage roster, but complete every
  active human caster setup with secondary/reaction/support/movement. Monsters keep monster legality.
WHY: caster tempo on undead is already the escalation. Adding Oracle/status, extra undead, instant
  magic, or hard-lock Time Magic turns a moderate permakill fight into a slog or lockdown puzzle.
WHAT IS NOT CHANGED: undead counters remain strong and visible; Time Mages amplify Haste/Slow only;
  Black Mages create ranged pressure with normal cast cadence.
```

Chapter 3 requirements applied:

```text
- Every active human enemy has full equipment.
- Every active human enemy has secondary, reaction, support, and movement.
- Monsters preserve monster legality: no equipment and no human ability completeness requirement.
- The party has real synergy: undead reraise + Time Mage tempo + Black Mage ranged punishment.
- No guests are present.
- No Oracle/status add, no extra undead body, no hard-lock Time Magic, no instant Black Magic.
```

## Sanctioned exceptions (carried precedents)

```text
UNDEAD reraise + heal-weakness — allowed and intended (Tchigolith 017 precedent): preserved as
  mechanic AND counterplay (Phoenix Down / Hi-Potion / Holy permakill; Seal Evil petrify; Entice flip).
TIME MAGE control — allowed (Lenalian 007 / Goug 018 / Gallows 020 / Vaults 027 precedent): the TWO
  Time Mages are Haste (on the undead) / Slow (on the player) / Float ONLY. NO Stop, Immobilize,
  Don't Move, Don't Act. They amplify the undead (the headline), not lock the player.
ONE-DISRUPTOR mass-status cap (017): the undead's status is single-target touch only; there is NO
  mass-status monster here (no Malboro), so the cap is respected — do NOT add one.
```

## Boss rare loot

```text
None. No named boss here — no rare boss item (per the Chapter 3 overview). The undead/casters stay
shop-tier (monsters carry no gear). The map's rare TREASURE (Bestiary / Mythril Spear / Iron Fan /
Damask Cloth) is existing map treasure, not boss loot; leave it as-is.
```

## Proposed Composition (New Game++ Yuguewood v2)

Keep the exact roster; scale and preserve the undead + tempo mechanics. The Revenant and one Time
Mage anchor at `101`–`102`; the rest at `100`–`101`. Moderate (2/5★).

| Slot | Role | Job | Level | Br/Fa | Purpose |
| ------ | ------ | ----- | ------- | --- | --------- |
| n | Revenant (undead) | Revenant | `101` | `86/35` | Tougher reraising body; attrition anchor. |
| n | Ghoul (undead) | Ghoul | `100` | `86/35` | Reraises; status touch; bog melee. |
| n | Ghast (undead) | Ghast | `100` | `86/35` | Reraises; status touch; second dead body. |
| n | Time Mage | Time Mage | `101` | `60/74` | Hastes the undead (more swings) / Slows the player. |
| n | Time Mage | Time Mage | `101` | `60/74` | Second tempo caster; reinforces the Hasted-dead clock. |
| n | Black Mage | Black Mage | `101` | `58/78` | Ranged elemental damage on the player's cleanup line. |
| n | Black Mage | Black Mage | `100` | `58/78` | Second mage; punishes a clumped permakill. |

Reasoning:

The faithful move is to **preserve the undead mechanics and add tempo + ranged pressure**. The three
undead reraise unless permakilled, so a player who doesn't exploit Phoenix Down / Holy / Seal Evil
faces endless attrition — exactly Tchigolith's lesson — but now the Time Mages Haste the dead (faster
swings) and Slow the cleanup, while the Black Mages shell from range and punish clumping. The swamp
hampers repositioning, so the player must permakill efficiently under pressure. Modest levels keep it
a fair 2/5★ — a tempo'd undead attrition puzzle, harder than Tchigolith but not a wall, sitting
between Yardow and the Riovanes finale.

## Builds / Monster Tuning Notes

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Undead x3 — Ghoul / Ghast / Revenant (Lv 100–101)

```text
Set JobLevel 8; keep aggressive Brave so they press onto the player's line.
PRESERVE undead flags: reraise/revive timers, heal-damages-undead, Phoenix-Down/Hi-Potion-instakill,
  Seal-Evil-petrify, Entice-able. Keep their single-target status touch (poison/zombie/etc.).
No equipment (monsters); levers are Level, JobLevel, Brave, innate skill tier.
```

Role: the reraising attrition core — must be permakilled, not just dropped.

### Time Mage x2 (Lv 101) — Haste/Slow only

```text
Job: Time Mage (68)   JobLevel: 4 cap or command-filter equivalent
Secondary: Item or low-tier Black/White Magic if legal; no hard status/control
Skillset limit: Haste (on the undead) / Slow (on the player) / Float-tier ONLY.
  NO Stop, Immobilize, Don't Move, Don't Act.
Reaction: Reflexes (449)   Support: MA/Magick-boost (id TBD)   Movement: Movement +1 (486)
Head: cloth/mage hat (id TBD)   Body: shop robe (id TBD)
Accessory: Featherweave Cloak (234)   Right hand: shop magic-boost rod (id TBD)   Left: none (255)
```

Role: the tempo amplifier — Hasted undead swing more; Slow drags the player's permakill.

### Black Mage x2 (Lv 101 / 100)

```text
Job: Black Mage (66)   JobLevel: 8   Primary: Black Magic
Secondary: Item or low-tier White Magic if legal; no Time Magic / no hard control
Reaction: Reflexes (449)   Support: MA/Magick-boost (id TBD)   Movement: Movement +1 (486)
Head: cloth/mage hat (id TBD)   Body: shop robe (id TBD)
Accessory: Featherweave Cloak (234)   Right hand: shop magic-boost rod (id TBD)   Left: none (255)
```

Role: ranged elemental punishment on the cleanup line; forces the player to spread.

## Positioning Plan

```text
The three undead start spread across the bog between the player and dry ground, pressing melee.
The 2 Time Mages start back so they can Haste the undead turn 1; the 2 Black Mages flank with lines
  onto the player's likely cleanup cluster.
Preserve the swamp terrain / mobility flags so the attrition is felt.
Keep the undead reraise + all anti-undead counters intact.
```

The woods should say: "the dead won't lie down — burn them out with light and elixirs — but their
chronomancers keep them swinging and their mages keep you honest."

## Simulation Plan and Results

Simulation artifact:

```text
tmp/fft-level-design-032-yuguewood/
```

Model scope:

```text
First five rounds only; compares undead reraise pressure, caster tempo, Black Mage ranged pressure,
permakill access, and slog risk. It rejects Oracle/status additions, hard-lock Time Magic, extra
undead bodies, and instant/high-tier caster burst.
```

Iteration results:

| Candidate | Enemies | Action ratio | Undead threat | Tempo threat | Magic threat | Total pressure | Permakill access | Slog risk | Answerability | Result |
|-----------|---------|--------------|---------------|--------------|--------------|----------------|------------------|-----------|---------------|--------|
| v1 undead caster tempo shell | 7 | 0.95 | 54.0 | 33.0 | 35.0 | 122.0 | 65.9 | 16.7 | 76.0 | Baseline |
| v2 complete undead caster tempo | 7 | 1.00 | 57.6 | 36.0 | 37.8 | 139.4 | 73.1 | 17.6 | 74.4 | Accepted |
| Hard-lock Time Mage swamp | 7 | 1.00 | 57.6 | 63.0 | 37.8 | 188.4 | 42.4 | 22.0 | 37.2 | Rejected: hard-lock / lost permakill |
| Oracle undead status stack | 7 | 1.00 | 57.6 | 18.0 | 37.8 | 141.4 | 59.9 | 22.7 | 60.0 | Rejected: not in roster / status stack |
| Fourth undead bog slog | 8 | 1.14 | 76.8 | 36.0 | 37.8 | 158.6 | 69.6 | 29.3 | 67.3 | Rejected: extra undead slog |
| Instant Black Magic cleanup tax | 7 | 1.00 | 57.6 | 36.0 | 73.5 | 175.1 | 66.6 | 18.0 | 67.3 | Rejected: caster counterplay removed |

Decision:

```text
Use the exact seven-unit undead/caster roster. Complete the four human caster setups, keep Time
Magic to Haste/Slow/Float, and preserve every undead counter. Reject Oracle/status, extra undead,
hard-lock Time Magic, and instant Black Magic because they turn a moderate permakill tempo fight
into a slog or lockdown puzzle.
```

## Current Implementation (v1, entry 430 — superseded by v2 design)

The shipped v1 already establishes the confirmed enemy-variant caster ids, undead monsters, undead
flags, and Haste/Slow Time Mage cap on entry 430. The v2 redesign above is **documentation only** in
this pass; it requires a later implementation pass to add mandatory secondary setups for the four
active human casters and validate undead level scaling in-game.

## Future Implementation Checklist (v2)

- [x] Identify Yuguewood ENTD entry 430; fill "Local Data Confirmed".
- [x] Dump original entry; verify 1 Ghoul + 1 Ghast + 1 Revenant + 2 Black Mage + 2 Time Mage.
- [x] Confirm undead monster ids and enemy-variant Black/Time Mage ids.
- [ ] Confirm undead flags (reraise + heal-weakness + PD-kill + Seal-Evil + Entice) persist.
- [ ] Constrain BOTH Time Mages to Haste/Slow (no hard lock); keep Black Mage cadence normal.
- [ ] Keep the undead's status touch single-target (no mass-status; one-disruptor cap respected).
- [ ] Set levels: Revenant + both Time Mages + one Black Mage `101`; Ghoul/Ghast + second Black Mage `100`.
- [ ] Set caster JobLevel/command caps intentionally; aggressive Brave on the undead; no equipment on monsters.
- [ ] Give every active human caster full equipment plus secondary/reaction/support/movement.
- [ ] Preserve moderate tuning: no Oracle/status add, no extra undead, no hard-lock, no instant magic.
- [ ] Preserve the swamp terrain / mobility flags.
- [ ] Patch via the correct layer in a later implementation pass; no binary/data change in this doc pass.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify undead + Haste fairness.
- [ ] Install mod, test from a New Game+ save; verify permakill (PD/Holy/Seal Evil) works under Haste.

## Test Questions

- Do the undead genuinely reraise, forcing permakill (Phoenix Down / Holy / Seal Evil)?
- Is "weaponize healing against the undead" rewarded, now under Time-Mage Haste pressure?
- Do the Black Mages + Slow make the player close the permakill faster (tempo matters)?
- Does the swamp terrain make the attrition bite without being unfair?
- Is the one-disruptor cap respected (single-target status only; no mass-status added)?
- Does it read as a HARDER Tchigolith (undead + casters) rather than a repeat?
- Is it a fair 2/5★ — above Tchigolith, below the Riovanes finale?

## Sources

- Game8, "The Yuguewood Walkthrough (Battle 29)": roster (1 Ghoul, 1 Ghast, 1 Revenant, 2 Black
  Mage, 2 Time Mage), objective "Defeat all enemies!", recommended level ~33, 2/5 stars, deploy 5,
  swamp terrain, undead heal-weakness + Phoenix-Down-instakill + Seal Evil petrify + Orator Entice,
  rewards/treasure.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553188
- Final Fantasy Wiki, "Yuguo Woods" + undead mechanics.
  https://finalfantasy.fandom.com/wiki/Yuguo_Woods
- Local: `docs/battles/024-chapter-3-overview.md` (Chapter 3 complete-party + rare-loot rules),
  `017-tchigolith-fenlands.md` (undead handling + one-disruptor cap), `018-goug-lowtown.md`
  (Time Mage Haste/Slow limit), `025-mining-town-gollund.md` (enemy Orator already debuted).
