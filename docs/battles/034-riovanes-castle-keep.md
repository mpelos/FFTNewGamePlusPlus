# 034 - Riovanes Castle Keep — Wiegraf -> Belias (Velius)

Status: ✅ implemented (v1, entry 432) — redesign plan v2 docs-only
Chapter: 3 — "The Valiant" — **CHAPTER SPIKE**
Battle order: Battle 31 (after Riovanes Castle Gate) — **Riovanes chain 2 of 3**
Target version: Enhanced v1.5.0
ENTD: global entry **432** (local entry 48, `battle_entd4_ent.bin`)
File: `battle_entd4_ent.bin` (embedded NG+ swap)

Implemented composition (entry 432, vanilla-dump verified):

- s0 **Wiegraf** (Phase-1 solo-duel boss, job 40 Holy Knight) — L104 + **Defender (33)** equipped as
  his stealable rare weapon. Solo-duel lock + transform trigger preserved.
- s5 **Belias/Velius** (Phase-2 Lucavi, job 60) — L105; demon kit + transform/spawn preserved.
- s6,s7,s8 **Archaeodaemon** (job 153) — L103/L103/L102. TIC has **3 adds**, not the public
  walkthrough's 4.
- s1-s4 (L1 placeholder Knights) + s9-s11 (L1 placeholder Wiegraf) are transform-scripting artifacts;
  leave untouched.

> Defense Ring is NOT set in the ENTD: a Lucavi demon has no equipment slots (`eq = 255`). It must be
> delivered through the reward layer as a guaranteed reward unless a future data pass proves a legal
> slot exists.

## Original Battle

Objective:

```text
Defeat Wiegraf! then Defeat Belias! (a two-phase fight; Wiegraf dies here for good as Belias.)
```

Player deployment:

```text
PHASE 1: Ramza alone — a 1v1 solo duel vs Wiegraf. No allies, no swaps.
PHASE 2: up to 5 units — the full party joins once Wiegraf transforms into Belias.
CHAIN: arrives from the Gate on one loadout; immediately followed by the Castle Roof with no
  resupply. This is the middle of the no-resupply Riovanes chain (Gate -> Keep -> Roof).
```

Original enemy composition:

```text
PHASE 1: 1x Wiegraf (Holy Knight — Holy Sword pressure).
PHASE 2: 1x Belias (Lucavi demon = Velius — high stats, powerful AoE) + Archaeodaemon adds.
```

Public walkthrough details:

```text
Recommended level: ~35. The hardest fight of Chapter 3.
PHASE 1: Ramza alone vs Wiegraf's Holy Knight skills. A classic answer is a Monk Ramza: no-MP
  Martial Arts, Chakra self-healing, and enough durability to grind Wiegraf down.
PHASE 2: Wiegraf becomes Belias. Public guides describe four Archaeodaemons; this mod's TIC entry
  currently has three. Belias has high stats and powerful AoE; Gravity/Graviga percentage damage is
  recommended, while the party spreads and controls adds.
No resupply into the Roof afterward.
```

Design reading:

The Keep is **the chapter's defining trial**: first a personal solo duel, then the Lucavi reveal.
Act one asks whether Ramza's own build can survive Wiegraf without party support. That cannot become
a guest-protection coin flip or a hard-lock build check; the canonical no-MP Monk answer, tanky solo
setups, and risky Thief/Steal-Weapon lines must all stay alive. Act two turns the personal duel into a
full-party boss spike: Belias is an army-of-one Lucavi backed by demon adds, answered by Gravity,
spacing, burst windows, and add control.

For New Game++ the identity is: **a fair but punishing solo skill-check against a complete Wiegraf,
then a full-party Lucavi spike against Belias plus the TIC-confirmed three Archaeodaemons, on the same
no-resupply Riovanes loadout.**

## Local Data Confirmed

```text
Entry 432 / local entry 48 / battle_entd4_ent.bin:
  s0  Wiegraf        job 40 Holy Knight    L104   active phase-1 duel boss
      Right hand: Defender item 33. Keep stealable/disarmable.
  s5  Belias/Velius  job 60 Lucavi         L105   active phase-2 boss; no equipment slots
  s6  Archaeodaemon  job 153               L103   active phase-2 add
  s7  Archaeodaemon  job 153               L103   active phase-2 add
  s8  Archaeodaemon  job 153               L102   active phase-2 add
  s1-s4  L1 placeholder Knights            transform scripting artifacts
  s9-s11 L1 placeholder Wiegraf slots       transform scripting artifacts

Preserve: Ramza-only phase-1 deployment lock, Wiegraf -> Belias transform trigger, full-party phase-2
join, 3-add spawn in the current TIC data, and no-resupply chain into Roof.
```

Job / item IDs:

```text
Holy Knight / Wiegraf job id: 40
Belias/Velius job id:        60
Archaeodaemon job id:        153
Defender item id:            33
Defense Ring item id:        TBD reward-layer id; not ENTD equipment on Belias
```

## Enemy Party Escalation (Chapter 3 redesign)

```text
The escalation is built into the two-phase structure: solo Wiegraf first, then Belias plus demon adds.
No extra generic caste and no fourth add are needed. Chapter 3 difficulty comes from making Wiegraf a
complete human boss and making Belias's one mass-pressure source matter, not from breaking the TIC
spawn or stacking unavoidable status.
```

Wiegraf follows Chapter 3's full-setup rule: complete gear, JobLevel 8, reaction/support/movement, and
a legal secondary if available. Belias and Archaeodaemons follow Lucavi/monster legality: no normal
equipment, no fake gear slots, and no second mass-status engine.

## Sanctioned Exceptions

```text
SOLO-DUEL fairness:
  Wiegraf may be strong and complete, but phase 1 must remain winnable by a prepared solo Ramza.
  No hard lock, no Stop/Don't Act/Petrify loop, no Safeguard/Maintenance on Wiegraf, and no
  disarm-proof Defender. MP pressure must not invalidate no-MP Martial Arts.

LUCAVI mass AoE/status:
  Belias may be the single mass-AoE/status source, telegraphed and counterable by spacing,
  Gravity/Graviga, and add control. No instant mass wipe and no second mass source from the adds.

DEMON add legality:
  Archaeodaemons are monster bodies. They do not need human equipment packages, but they should not
  gain artificial multi-target hard-lock tools.
```

## Boss Rare Loot

```text
Two rares are justified here: this is the marquee Chapter 3 spike with two boss forms. Both are
mid-high and Chapter-4-safe.

1) Wiegraf -> Defender (Knight Sword; non-buyable). Equipped in phase 1 as his stealable weapon.
   This pays off the deferred Wiegraf rare from the Vaults. It sits above the Chapter 2 rare baseline
   and below Save the Queen / Excalibur / Ragnarok / Chaos Blade.

2) Belias -> Defense Ring (accessory; non-buyable). Because Belias has no ENTD equipment slots, this
   is a guaranteed reward-layer item, not an equipped/drop/steal slot, unless future tooling proves
   otherwise. It sits above Chapter 2's 108 Gems and below Ribbon / best Chapter 4 accessories.
```

The map's rare treasure (Diamond Armor / Jujitsu Gi / Chameleon Robe / Germinas Boots) is existing map
treasure, not boss loot; leave it as-is.

## Proposed Composition (New Game++ Riovanes Keep v2)

Two phases. Wiegraf `104`; Belias `105`; Archaeodaemons `103`/`103`/`102`.

### Phase 1 — Solo Duel

| Slot | Role | Job | Level | Br/Fa | Purpose |
| ------ | ------ | ----- | ------- | --- | --------- |
| s0 | Wiegraf (duel boss) | Holy Knight (40) | `104` | `88/60` | Complete 1v1 skill check; Defender steal target; no hard lock. |

### Phase 2 — Belias + Three Adds

| Slot | Role | Job | Level | Br/Fa | Purpose |
| ------ | ------ | ----- | ------- | --- | --------- |
| s5 | Belias / Velius | Lucavi (60) | `105` | `88/82` | Army-of-one demon; one telegraphed mass source. Gravity is the answer. |
| s6 | Archaeodaemon | Archaeodaemon (153) | `103` | `84/72` | Demon add; screens Belias and pressures spacing. |
| s7 | Archaeodaemon | Archaeodaemon (153) | `103` | `84/72` | Second add; flanks and punishes clumping. |
| s8 | Archaeodaemon | Archaeodaemon (153) | `102` | `84/72` | Third add; enough swarm without exhausting the Roof chain. |

Reasoning:

The faithful v2 move is to raise Wiegraf to a complete Chapter 3 human boss while preserving every
solo answer that makes the duel tactical: no-MP Monk, durable self-heal builds, and risky steal/disarm
plans against Defender. Phase 2 then supplies the chapter spike through Belias's Lucavi stats and one
mass-pressure source, plus the three confirmed Archaeodaemons. The player should feel the wall, but
the solution space remains readable: prepare Ramza, survive the reveal, spread out, use Gravity, and
leave enough resources for Roof.

Simulation result (`tmp/fft-level-design-034-riovanes-castle-keep/iteration-results.md`):

```text
v2 complete fair 3-add Lucavi spike: Accepted.
Solo fairness 79.3; prepared Ramza win 100.0; Lucavi pressure 228.8; Gravity viability 72.0;
chain strain 40.9; answerability 73.4.

Rejected: public 4-add variant (does not match TIC data and overtaxes the Roof chain), disarm-proof
Wiegraf, hard-lock Wiegraf, and instant/double-source Belias pressure.
```

## Builds (complete human setup; Lucavi/monster legality)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Wiegraf — Holy Knight Duel Boss (Lv 104) — rare: Defender

```text
Job: Holy Knight (40)   JobLevel: 8
Primary: Holy Sword
Secondary: Item or basic Fundaments-style command, if legal in this slot
Reaction: Counter / Parry-style reaction
Support: Attack Boost (465) or legal offensive support
Movement: Movement +1 (486) or legal mobility
Head/Body: final-shop heavy helm + heavy armor his job allows
Accessory: Bracers (218) or final-shop offensive accessory
Right hand: Defender (33) — his rare and Steal-Weapon target
Left hand: final-shop shield if legal

Guardrails: no Safeguard/Maintenance, no hard-lock status, no disarm-proof weapon, and no secondary
engine that invalidates the no-MP Martial-Arts answer.
```

Role: the personal wall. He is complete, dangerous, and worth stealing from, but the duel is still won
by preparation and execution.

### Belias / Velius — Lucavi Boss (Lv 105) — rare: Defense Ring via reward layer

```text
Job: Belias / Velius (60)   JobLevel: 8 if the slot supports it
Primary: canonical Lucavi kit; high stats + one powerful, telegraphed mass AoE/status source
Secondary/Reaction/Support/Movement: monster/Lucavi-legal only; do not fake human equipment slots
Equipment: none in ENTD (`eq = 255`)
Reward: Defense Ring via guaranteed reward layer

Guardrails: no instant mass wipe, no hard lock, no second mass source. Gravity/Graviga percentage
damage must remain viable against the big HP bar.
```

Role: the chapter apex: one demon boss that turns spacing, Gravity, and add management into the exam.

### Archaeodaemon x3 (Lv 103 / 103 / 102)

```text
Job: Archaeodaemon (153)   JobLevel: 8 if the slot supports it
Equipment: none; monster/demon legality
Allowed: aggressive Brave, single-target demon pressure, flanking, screening Belias
Forbidden: artificial multi-target hard-lock or extra mass-status engine
```

Role: the swarm. Three bodies are enough to force add-control decisions without making Roof cleanup
unfair.

## Positioning Plan

```text
PHASE 1: preserve the duel arena and Ramza-only deployment lock.
PHASE 2: on transform, Belias spawns centrally and the three Archaeodaemons use the current TIC spawn
  pattern. Preserve room to spread against AoE.
Preserve the transform trigger, full-party join, and no-resupply chain link into Roof.
```

The Keep should say: "first you, alone, against the Holy Knight; then everyone, against the demon he
becomes and the three it calls. Spread, sap its health, steal only if you can afford it, and do not
spend what the roof will demand."

## Implementation Checklist

- [x] Confirm entry 432 active slots and current 3-add TIC spawn in the doc.
- [x] Confirm Wiegraf job 40, Belias job 60, Archaeodaemon job 153, Defender item 33.
- [x] Record Defense Ring as reward-layer only unless a future data pass proves a legal Lucavi slot.
- [ ] Preserve phase-1 solo lock, Wiegraf -> Belias transform, full-party phase-2 join, and no-resupply chain.
- [ ] Complete Wiegraf's human setup: secondary if legal, reaction, support, movement, final-shop gear.
- [ ] Preserve Defender as Wiegraf's stealable/disarmable phase-1 weapon.
- [ ] Constrain Belias to one telegraphed mass-AoE/status source; no instant hard lock.
- [ ] Preserve exactly three Archaeodaemons from the current TIC data.
- [ ] Set/verify levels: Wiegraf `104`; Belias `105`; Archaeodaemons `103`/`103`/`102`.
- [ ] Patch only through the correct future implementation layer; keep this redesign docs-only for now.
- [ ] Re-dump and diff after implementation; verify both phases, three adds, Defender, and reward-layer item.
- [ ] Test from a New Game+ save: solo duel is hard-but-fair; Belias is beatable with Gravity/spacing/add
      control; enough resources remain for Roof.

## Test Questions

- Is phase 1 a hard-but-fair solo skill check rather than a hard-lock build check?
- Does no-MP Martial-Arts Ramza remain a valid answer?
- Is Defender stealable/disarmable instead of protected by Safeguard/Maintenance?
- Does phase 2 use Belias plus exactly three Archaeodaemons in this mod's data?
- Is Belias the only mass-AoE/status source, with Gravity percentage damage still valuable?
- Does the fight feel like the chapter's spike without leaving the player helpless for Roof?
- Do Defender and reward-layer Defense Ring stay mid-high and Chapter-4-safe?
- Does the two-phase Wiegraf -> Belias structure remain intact?

## Sources

- Game8, "Riovanes Castle Keep Walkthrough (Battle 31)": public phase reading, solo duel, Belias,
  Archaeodaemon adds, Gravity/Graviga answer, no-resupply chain into Roof, rewards/treasure.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553191
- Final Fantasy Wiki, "Velius" / "Wiegraf Folles": Lucavi context and Wiegraf transform.
  https://finalfantasy.fandom.com/wiki/Velius
- Local: `docs/battles/024-chapter-3-overview.md` (chapter rules), `022-lionel-castle-oratory.md`
  (Cuchulainn Lucavi precedent), `028-monastery-vaults-3rd.md` and `029-monastery-vaults-1st.md`
  (Wiegraf rare and disarm/steal precedent), `tmp/fft-level-design-034-riovanes-castle-keep/`
  (coarse simulation and rejected variants).
