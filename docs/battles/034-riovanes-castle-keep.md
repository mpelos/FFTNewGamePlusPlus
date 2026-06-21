# 034 - Riovanes Castle Keep — Wiegraf → Belias (Velius)

Status: ✅ implemented (v1, entry 432)
Chapter: 3 — "The Valiant" — **CHAPTER SPIKE**
Battle order: Battle 31 (after Riovanes Castle Gate) — **Riovanes chain 2 of 3**
Target version: Enhanced v1.5.0
ENTD: global entry **432** (local entry 48, `battle_entd4_ent.bin`)
File: `battle_entd4_ent.bin` (embedded NG+ swap) — `tools/battle_patch.py riovanes_keep`

Implemented composition (entry 432, vanilla-dump verified):
- s0 **Wiegraf** (Phase-1 solo-duel boss, job 40 Holy Knight) — L104 + **Defender (33)** as his
  equipped weapon (his rare; Steal-Weapon target in the duel). Job/secondary/jobLevel/other gear/
  solo-duel lock + transform trigger preserved; no skillset change → no new hard lock (duel stays fair).
- s5 **Belias/Velius** (Phase-2 Lucavi, job 60) — L105 (chapter top) only; demon kit + transform/spawn preserved.
- s6,s7,s8 **Archaeodaemon** (job 153) L103/L103/L102 — level only (demon adds; TIC has 3, not the
  walkthrough's 4).
- s1-s4 (lvl-1 placeholder Knights) + s9-s11 (lvl-1 placeholder Wiegraf) = transform-scripting
  artifacts — left untouched.

> ⚠️ Defense Ring (Belias's intended rare) is NOT set in the ENTD: a Lucavi demon has no equip slots
> (eq = 255). It must be delivered as a **reward-layer guaranteed reward** — TODO outside this patch.

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `024-chapter-3-overview.md`. (Belias is this version's name for the Lucavi VELIUS.)

## Original Battle

Objective:

```text
Defeat Wiegraf!  then  Defeat Belias!   (a TWO-PHASE fight; Wiegraf dies here for good — as Belias.)
```

Player deployment:

```text
PHASE 1: RAMZA ALONE — a 1v1 SOLO DUEL vs Wiegraf. No allies, no swaps. (The infamous wall.)
PHASE 2: up to 5 units — your FULL PARTY joins once Wiegraf transforms into Belias.
CHAIN: arrives from the Gate on one loadout; immediately followed by the Castle ROOF with NO
  resupply. This is the middle of the no-resupply Riovanes chain (Gate -> Keep -> Roof).
```

Original enemy composition:

```text
PHASE 1: 1x Wiegraf (Holy Knight — Holy Sword skills; MP-draining pressure).
PHASE 2: 1x Belias (Lucavi DEMON = Velius — high stats, powerful AoE) + 4x Archaeodaemon (demon adds).
```

Public walkthrough details:

```text
Recommended level: ~35.  THE hardest fight of Chapter 3.
PHASE 1 (solo): Ramza alone vs Wiegraf's Holy Knight skills. A classic answer is a MONK Ramza —
  Martial Arts cost no MP (so MP-drain can't disarm him) and Chakra self-heals; survive and grind
  him down. The phase is a personal skill check.
PHASE 2 (party): Wiegraf becomes Belias and spawns FOUR Archaeodaemons. Belias has high stats and
  powerful AoEs; GRAVITY / GRAVIGA (percentage HP damage) is recommended to chunk his big health
  bar, while the party spreads against AoE and clears or screens the adds.
No resupply into the Roof afterward.
```

Design reading:

The Keep is **the chapter's defining trial** — a two-act boss fight. Act one is the **solo duel**:
Ramza, alone, against a Holy Knight who can punish a mis-built character, so the player's *single*
unit and their kit are tested (the canonical answer, a no-MP Martial-Arts Monk with Chakra, must
stay viable). Act two is the **Lucavi reveal**: Wiegraf becomes Belias (Velius), the second demon,
who fights as an **army-of-one with four demon adds** and heavy AoE — solved by **percentage damage
(Gravity)**, **spacing**, and **add management**, echoing Cúchulainn (`022`) but bigger and preceded
by the duel. It is where Wiegraf finally **dies**, paying out the rare deferred from the Vaults. The
no-resupply chain makes it a marathon: survive the duel, then the demon, then walk straight into the
Roof.

For New Game++ the identity must stay: **a two-phase climax — a fair solo skill-check duel against a
Holy Knight, then a full-party fight against a high-AoE Lucavi and its four demon adds answered by
Gravity, spacing, and add control — the chapter's spike, on a no-resupply loadout.**

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm the TWO-PHASE scripting: (1) Ramza-ALONE solo duel vs Wiegraf; (2) the Wiegraf->Belias
  TRANSFORM that spawns 4 Archaeodaemons and brings the full party in.
CRITICAL: preserve the solo-duel deployment lock, the transform trigger, the 4-add spawn, and the
  no-resupply chain link into the Roof. These are the fight's identity.
Confirm Belias's AoE/status kit + whether he has any elemental weakness in this version (none listed
  by Game8; Gravity %-damage is the intended answer).
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
```

Job IDs (carry over known, verify the rest in-game):

```text
Holy Knight job id     (TBD - verify; Wiegraf — Holy Sword; from Fovoham 008 / Vaults 029)
Belias/Velius id       (TBD - verify; 2nd Lucavi DEMON — high stats + AoE)
Archaeodaemon id       (TBD - verify; demon add, x4)
Defender (knight sword) item id (TBD - verify; Wiegraf's rare — stealable in the duel)
Defense Ring item id   (TBD - verify; Belias's rare — mid-high accessory)
```

## Job Escalation (Chapter 3 rule)

```text
THE ESCALATION IS BUILT IN: a SOLO-DUEL phase (your one unit tested) followed by the SECOND LUCAVI
(Belias) with FOUR demon adds and heavy AoE — the densest single fight of the chapter. The two-phase
boss structure IS the escalation; per "one new wrinkle per fight," NO extra generic caste is added.
Keep the canonical Wiegraf (P1) and Belias + 4 Archaeodaemon (P2) shapes.
WHY: a personal skill-check duel plus a demon-army-of-one is already the chapter's hardest, most
  distinct problem. Adding more would muddy it.
```

## Sanctioned exceptions (carried + extended precedent)

```text
SOLO-DUEL fairness — the Phase 1 duel MUST stay winnable by a prepared solo Ramza. Wiegraf's Holy
  Sword may hit hard, but: NO hard lock (no Stop/Don't Act/Petrify), and his MP-drain/Holy Sword must
  not be able to fully disable a no-MP Martial-Arts build (the canonical Monk-Ramza answer stays
  valid). This phase is a skill check, NOT a coin-flip — tune Wiegraf so a reasonable Ramza wins.
LUCAVI mass-AoE/status (Belias) — allowed as a BOSS signature (Cúchulainn 022 precedent): ONE demon
  as the AoE source, telegraphed, counterable (spread out, Gravity %-damage, clear/screen adds),
  NOT instant, NO hard lock. The 4 Archaeodaemons are demon bodies (their own touch-status stays
  single-target); do NOT pile a second mass-status source on top of Belias.
```

## Boss rare loot

```text
TWO rares are justified here (the chapter's marquee fight, two boss forms — overview allows a second
rare when a fight has two notable foes). Both MID-HIGH, both Ch4-safe.

1) Wiegraf (Phase 1) -> DEFENDER (Knight Sword; non-buyable). His equipped weapon — STEALABLE during
   the solo duel (a tempting, risky Thief-Ramza play) and the deferred Vaults-Wiegraf rare finally
   paid out. Above Ancient Sword (Ch2) / Izlude's Reflect Mail (028); BELOW Save the Queen / Excalibur
   / Ragnarok / Chaos Blade (all Ch4-reserved). Note: in FFT Wiegraf TRANSFORMS rather than dropping,
   so the authentic way to obtain Defender is Steal Weapon in Phase 1 — set it as his equipped weapon.

2) Belias (Phase 2) -> DEFENSE RING (accessory; non-buyable; status-immunity / defensive). A demon's
   trinket dropped/stolen on his death. Above Ch2's 108 Gems; BELOW Ribbon / best accessories
   (Ch4-reserved). Assign as his rare drop/steal if the Lucavi slot supports equipment; else as a
   GUARANTEED battle reward (Cúchulainn 022 fallback).

DIFFERENTIATION: Defender (weapon) and Defense Ring (accessory) avoid colliding with Izlude's Reflect
Mail (armor, 028). The map's rare TREASURE (Diamond Armor / Jujitsu Gi / Chameleon Robe / Germinas
Boots) is existing map treasure, not boss loot; leave it as-is.
```

## Proposed Composition (New Game++ Riovanes Keep v1)

Two phases. Wiegraf (duel) `104`; Belias `105` (chapter top); Archaeodaemons `102`–`103`.

### Phase 1 — Solo Duel

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Wiegraf (DUEL BOSS) | Holy Knight | `104` | 1v1 skill check; Holy Sword pressure. Carries Defender (steal target). |

### Phase 2 — Belias + adds (full party)

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Belias (LUCAVI BOSS) | Belias / Velius | `105` | Army-of-one demon; high stats + telegraphed AoE. Gravity is the answer. Defense Ring. |
| n | Archaeodaemon | Archaeodaemon | `103` | Demon add; swarms / screens Belias. |
| n | Archaeodaemon | Archaeodaemon | `103` | Second add; flanks the party. |
| n | Archaeodaemon | Archaeodaemon | `102` | Third add; AoE fodder / pressure. |
| n | Archaeodaemon | Archaeodaemon | `102` | Fourth add; splits focus from Belias. |

Reasoning:

The faithful move is to **preserve both phases and keep each one's intended answer alive**. Phase 1
must remain a *fair* solo skill check: Wiegraf at `104` is dangerous but a prepared Ramza (Monk with
Chakra / a tanky disarm build) can win — so no hard lock, no MP-drain that nullifies the no-MP
answer. Phase 2 is the Lucavi army-of-one: Belias at `105` (the chapter's top band, +5) with heavy
but telegraphed AoE, plus four Archaeodaemons that swarm — solved by Gravity %-damage on Belias's big
bar, spreading against AoE, and clearing/screening adds. Two rares (Defender via duel-steal, Defense
Ring on Belias) reward the chapter's hardest fight. The no-resupply chain demands the player exit with
enough to survive the Roof — tune so a strong party can, without trivializing the spike.

## Builds (final-shop quality; Lucavi climax flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Wiegraf — Holy Knight DUEL BOSS (Lv 104) — rare: Defender (steal in duel)

```text
Job: Holy Knight (id TBD)   JobLevel: 8   Primary: Holy Sword (ranged waves; soft status only)
Reaction: Counter (442) or parry (id TBD)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head/Body: shop heavy helm + heavy armor (ids TBD)
Accessory: Bracers (218)   Right hand: DEFENDER (id TBD — his rare; Steal-Weapon target in P1)
Left: shop shield (id TBD)
FAIRNESS: no hard lock; MP-drain/Holy Sword must NOT nullify a no-MP Martial-Arts Ramza. Tune so a
  prepared solo Ramza can win.
```

Role: the solo skill check. Beatable by a prepared Ramza; Defender is a tempting steal for a Thief build.

### Belias (Velius) — LUCAVI BOSS (Lv 105) — rare: Defense Ring

```text
Job: Belias / Velius (id TBD)   JobLevel: 8   Primary: canonical Lucavi kit (high stats + powerful AoE)
Skillset limit: ONE telegraphed mass-AoE/status source (himself); NO hard lock; NOT instant.
Reaction: a demon reaction (id TBD)   Support: high innate   Movement: Movement +1 (486) / Ignore Height
Accessory/Drop: DEFENSE RING (id TBD — his rare; drop/steal if slot allows, else guaranteed reward)
Big HP bar -> Gravity/Graviga %-damage is the intended chip answer; keep that viable.
```

Role: the chapter's apex — army-of-one demon with four adds; spacing + Gravity + add control beat him.

### Archaeodaemon x4 (Lv 103 / 103 / 102 / 102)

```text
Job: Archaeodaemon (id TBD)   JobLevel: 8   (demon add; no equipment)
Keep aggressive Brave; their status touch stays single-target (no second mass-status source).
```

Role: the swarm — splits the party's focus and screens Belias.

## Positioning Plan

```text
PHASE 1: the duel arena — Ramza alone vs Wiegraf. Preserve the solo deployment lock.
PHASE 2: on transform, Belias spawns centrally with the 4 Archaeodaemons around him; the full party
  enters. Preserve the spawn pattern and the room geometry (room to spread vs AoE).
Preserve the transform trigger and the no-resupply chain link into the Roof.
```

The keep should say: "first you, alone, against the Holy Knight — then everyone, against the demon he
becomes and the four it calls. Spread, sap its health, and don't spend what the roof will demand."

## Implementation Checklist

- [ ] Identify Riovanes Keep `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify the two-phase scripting (solo Wiegraf -> Belias + 4 Archaeodaemons).
- [ ] Confirm Holy Knight / Belias / Archaeodaemon ids; confirm Belias's AoE kit + Gravity viability.
- [ ] PHASE-1 FAIRNESS: tune Wiegraf so a prepared SOLO Ramza wins; no hard lock; no-MP build stays valid.
- [ ] Set Defender as Wiegraf's equipped weapon (Steal-Weapon target / his rare).
- [ ] Set Defense Ring as Belias's rare drop/steal (or guaranteed reward if the Lucavi slot can't hold it).
- [ ] Constrain Belias to ONE telegraphed AoE/status source (no hard lock, not instant); adds single-status.
- [ ] Set levels: Wiegraf `104`; Belias `105`; Archaeodaemons `103`/`102`.
- [ ] Set JobLevel `8` on all active enemy slots.
- [ ] PRESERVE both phases, the transform + 4-add spawn, and the no-resupply chain into the Roof.
- [ ] Patch via the correct layer; keep the diff inside the Riovanes Keep window only.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify both phases + rares.
- [ ] Install mod, test from a New Game+ save: confirm the solo duel is hard-but-fair and Belias is
      beatable with Gravity/spacing/add-control while leaving resources for the Roof.

## Test Questions

- Is the Phase 1 solo duel a hard-but-FAIR skill check (a prepared Ramza wins; no hard lock)?
- Does a no-MP Martial-Arts Ramza remain a valid answer (MP-drain doesn't nullify it)?
- Is Belias a true army-of-one with the 4 adds — and is Gravity %-damage a viable chip answer?
- Is Belias's AoE telegraphed and spaceable, with only ONE mass source (no stacked status)?
- Do the two MID-HIGH rares (Defender via duel-steal, Defense Ring on Belias) land — and stay Ch4-safe?
- Is the fight survivable on the no-resupply loadout WITHOUT leaving the player helpless for the Roof?
- Is it clearly the chapter's hardest fight (the spike), yet beatable by tactics, not grinding?
- Does it preserve the iconic two-phase Wiegraf->Belias structure faithfully?

## Sources

- Game8, "Riovanes Castle Keep Walkthrough (Battle 31)": Phase 1 solo Ramza-vs-Wiegraf duel (Holy
  Knight, no-MP Martial-Arts answer), Phase 2 transform into Belias + four Archaeodaemons, high-stat
  AoE Belias with Gravity/Graviga recommended, objective "Defeat Wiegraf! Then Defeat Belias!",
  recommended level ~35, deploy 5, no-resupply chain into the Roof, rewards/treasure.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553191
- Final Fantasy Wiki, "Velius" / "Wiegraf Folles": Lucavi (Belias) kit + transform context.
  https://finalfantasy.fandom.com/wiki/Velius
- Local: `docs/battles/024-chapter-3-overview.md` (job-escalation + rare-loot rules),
  `022-lionel-castle-oratory.md` (Cúchulainn — Lucavi army-of-one design), `008-fovoham-windflats.md`
  & `029-monastery-vaults-1st.md` (Wiegraf Holy-Knight, deferred rare), `028-monastery-vaults-3rd.md`
  (Reflect Mail — differentiation).
</content>
