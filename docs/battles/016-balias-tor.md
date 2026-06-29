# 016 - Balias Tor (Bariaus Hill)

Status: ✅ implemented (v1, entry 409) — Summoner job is the built-in escalation. **v2 redesign documented only** (implementation pending).
Chapter: 2 — "The Manipulator and the Subservient"
Battle order: Battle 15 (after Castled City of Zaland)
Target version: Enhanced v1.5.0
ENTD: global entry **409** (battle_entd4, local entry 25) — confirmed by sequence + composition
File: `entd/battle_entd4_ent.bin` (embedded; swapped only in NG+ by the code mod)

> Implemented via `tools/battle_patch.py balias_tor`. NG+-only by construction. See
> `011-chapter-2-overview.md`.

## Original Battle

Objective:

```text
Defeat all enemies!
```

Player deployment:

```text
Up to 4 units, including Ramza. No guests.
```

Original enemy composition:

```text
2x Summoner
2x Knight
2x Archer
```

Public walkthrough details:

```text
Recommended level: ~16.
Hill terrain; the enemy is split into left / center / right groups.
The Summoners are the primary danger: take them out fast before they drop Ifrit (or another
  big summon) on your party. Their summons are slow to charge but hit a wide area hard.
The Knights threaten gear loss via Rend (equipment break) — Safeguard is valuable.
A Chemist is "indispensable" for sustained healing/revival.
```

Design reading:

Balias Tor is **the first Summoner fight** — the chapter's marquee new caster threat. Summoners
trade speed for reach: a charging summon (Ifrit/Shiva/Ramuh/Titan) is telegraphed but, when it
lands, blankets a group for heavy elemental damage. The fight teaches the player to **race the
charge** (rush or snipe the Summoners before they unleash), to **respect break-Knights**
(Safeguard), and to manage a **three-flank hill**. It is a tempo-and-priority puzzle: ignore the
Summoners and a single cast can wreck the party.

For New Game++ the identity must stay: **a three-flank hill where slow-but-devastating Summoners
must be raced down before they cast, while break-Knights and Archers screen them — priority and
tempo are the whole fight.**

## Local Data Confirmed (entry 409)

```text
slot  cid    name  flags  job          role                   action
s0    0x22   34    0x89   34           Mustadio (disabled)    LEAVE (lvl 254)
s1    0x34   52    0x49   52           story unit (disabled)  LEAVE (lvl 254)
s2    0x80   255   0x80   76 Knight    break-wall             SCALE -> L101
s3    0x80   255   0x80   77 Archer    ranged support         SCALE -> L101
s4    0x80   255   0x80   77 Archer    ranged support         SCALE -> L100
s5    0x81   255   0x40   82 Summoner  priority AoE caster     SCALE -> L101
s6    0x81   255   0x40   82 Summoner  priority AoE caster     SCALE -> L101
s7    0x80   255   0x80   76 Knight    break-wall             SCALE -> L101
```

Job IDs: **Summoner 82** (first use in the mod), Knight 76, Archer 77. Summon is innate to job 82 at
jl8; the Knights' Rend comes innately from their Battle Skill command at jl8 (the sanctioned break
exception, as at Ziekden) — no secondary skillset needed for either.

PLAYTEST: the "mid-tier summons only" guideline can't be enforced through ENTD level/joblevel (no
ability-id control there), and jl8 is kept for caster-stat consistency with the mod's other casters.
If best-tier summons show up and over-spike the curve, cap the Summoners' level/joblevel.

## Enemy Party Escalation (Chapter 2 redesign)

```text
VANILLA SPIRIT: first real Summoner showcase on a split hill; race the charge before the summon
  lands.
CHAPTER-2 UPGRADE: keep exactly 2 Summoners, 2 Knights, and 2 Archers, then add one Chemist as the
  sustain/revive support that makes target priority matter.
WHY: a third Summoner over-stacks the first showcase's AoE, and a Time Mage/Haste support muddies
  the core lesson by making summons feel less raceable. A Chemist supports the cell without changing
  the headline: kill or interrupt the Summoners.
WHAT IS NOT CHANGED: Summoners remain the priority, Knights keep limited Rend pressure, Archers
  punish the rush, and summon charge time remains the fair answer.
```

Chapter 2 requirements applied:

```text
- Every active human enemy has full equipment.
- Every active human enemy has intentional reaction, support, and movement.
- Secondary is optional; Chemist uses Item, Knights use Rend, Summoners rely on Summon.
- Rend remains limited to the two Knights.
- No hard-lock status or instant-cast Summoner framing is introduced.
```

## Sanctioned exception — Knight Rend (break) stays

```text
Like Ziekden (009), the Knights here carry canonical Rend (equipment break) and the game
telegraphs Safeguard as the counter. It stays, constrained:
ALLOWED: Rend on the two Knights (the fight's secondary threat).
GUARDRAIL: only the two canonical Knights carry it; shop-tier breakable gear only; the player's
  Safeguard counter remains valid, so it is fair at NG+ scale.
```

## Boss rare loot

```text
None. No named boss/leader here — no rare item (per the Chapter 2 overview). Generics stay
shop-tier. (The Summoners' summon spells are the threat, not their loot.)
```

## Proposed Composition (New Game++ Balias Tor v2)

Use seven enemies: 2 optimized Summoners, 2 Rend Knights, 2 Archers, 1 Chemist. The Summoners stay
the headline, but the Chemist makes "ignore support and race only one flank" less free.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Fast Summoner | Summoner | `102` | Swiftness caster; still raceable, but the clock is real. |
| n | Power Summoner | Summoner | `101` | Arcane Strength caster; punishes ignored flank. |
| n | Knight (Rend) | Knight | `101` | Break-wall; screens a Summoner. Safeguard-telegraphed threat. |
| n | Knight (Rend) | Knight | `101` | Second break-wall; protects the other Summoner. |
| n | Archer | Archer | `101` | Ranged support; punishes the rush toward the Summoners. |
| n | Archer | Archer | `100` | Second bow; covers the center/hill. |
| n | Chemist (NEW) | Chemist | `101` | Item sustain/revive; forces target priority. |

Reasoning:

The faithful move is to **scale and lean into the Summoners**. Two summon-casters on opposite
flanks force the player to choose a side and race a charge while the other winds up. The Rend
Knights screen them; Archers punish the approach; the Chemist creates a support target that can
undo sloppy focus fire. Keep the summons mid-tier (Ifrit/Shiva/Ramuh/Titan), not best summons, and
keep charge times so the race-the-cast counter is real.

## Builds (final-shop quality; hill garrison + summoner flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Summoner x2 (Lv 102 / 101) — fight identity

```text
Fast Summoner:
Job: Summoner (id TBD)   JobLevel: 8   Secondary: none
Primary: Summon (mid-tier: Ifrit / Shiva / Ramuh / Titan — NOT best summons)
Reaction: Mana Shield / Reflexes (id TBD / 449)
Support: Swiftness (id TBD)   Movement: Movement +1 (486)
Head: cloth/mage hat (id TBD)   Body: shop robe (id TBD)
Accessory: Featherweave Cloak (234) or magic-defensive accessory (id TBD)
Right hand: shop magic-boost rod/staff (id TBD)   Left hand: none (255)

Power Summoner:
Job: Summoner (id TBD)   JobLevel: 8   Secondary: none
Primary: Summon (mid-tier only)
Reaction: Reflexes (449)
Support: Arcane Strength (id TBD)   Movement: Movement +1 (486)
Head: cloth/mage hat (id TBD)   Body: shop robe (id TBD)
Accessory: Featherweave Cloak (234) or magic-defensive accessory (id TBD)
Right hand: shop magic-boost rod/staff (id TBD)   Left hand: none (255)
```

Role: the priority threat. Slow charge, wide AoE — must be raced down. Keep charge times so the
player can interrupt by closing/sniping; do NOT make summons instant or the lesson dies.

### Knight x2 (Lv 101) — Rend (break)

```text
Job: Knight (id TBD)   JobLevel: 8   Secondary: the Knight break command (Rend, id TBD)
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head/Body: shop heavy helm + heavy armor (ids TBD)
Accessory: Bracers (218)   Right hand: Runeblade (30) or Icebrand (29)   Left: shop shield (id TBD)
```

Role: the screen in front of the Summoners. Rend punishes a careless rush; bring Safeguard.

### Archer x2 (Lv 101 / 100)

```text
Job: Archer (77)   JobLevel: 8   Secondary: none
Reaction: Reflexes (449)   Support: Concentration (469)   Movement: Movement +1 (486)
Head: Thief's Cap (168)   Body: Black Garb (198)   Accessory: Bracers (218)
Right hand: Windslash Bow (87)   Left hand: none / two-hand marker (254)
```

Role: ranged support that punishes the player's dash toward the Summoners.

### Chemist (Lv 101) — NEW sustain

```text
Job: Chemist (75)   JobLevel: 8   Secondary: none
Primary: Item (Hi-Potion/X-Potion tier, Phoenix Down, Remedy; tune inventory in implementation)
Reaction: Auto-Potion (id TBD) or Reflexes (449)
Support: Throw Items (id TBD)   Movement: Movement +1 (486)
Head: Thief's Cap (168)   Body: Black Garb (198)   Accessory: Featherweave Cloak (234)
Right hand: Mythril Gun (72) or strong shop gun (id TBD)   Left hand: none (255)
```

Role: sustain/revive pressure. It should make the player care about support, not create an
unending stall; tune potion tier if cleanup drags.

## Positioning Plan

```text
Summoners start on the left and right flanks of the hill, behind their Knight screens, with
  sightlines over the center where the player must cross.
The two Rend-Knights start in front of / beside their Summoners, between the player and the casters.
The Archers start center / on the hill's high ground, covering the approach lanes to both flanks.
The Chemist starts behind the center, close enough to throw items to either flank but reachable by
  a committed rush or ranged answer.
This recreates the original's left/center/right split: the player must pick a flank, race a
  summon, and eat fire from the rest.
```

The hill should force a choice: commit to one Summoner and race its charge while the other winds
up and the center harasses — the original's priority-and-tempo puzzle, at scale.

## Simulation Plan and Results

Simulation artifact:

```text
tmp/fft-level-design-016-balias-tor/
```

Model scope:

```text
First four rounds only; compares Summoner-cell pressure and rejects candidates that dilute the
first-Summoner lesson with Time Mage tempo or too many summon sources.
```

Iteration results:

| Candidate | Enemies | Enemy actions | Action ratio | Pressure | Delta vs v1 | Result |
|-----------|---------|---------------|--------------|----------|-------------|--------|
| v1 current: 2 Summoner, 2 Knight, 2 Archer | 6 | 21.2 | 1.32 | 56.0 | 0.0% | Baseline |
| Add Time Mage tempo | 7 | 24.8 | 1.55 | 65.6 | +17.1% | Rejected: extra tempo system |
| Add third Summoner | 7 | 24.2 | 1.51 | 68.0 | +21.4% | Rejected: too much first-showcase AoE |
| 2 optimized Summoner, 2 Knight, 2 Archer, 1 Chemist | 7 | 25.4 | 1.58 | 68.9 | +23.0% | Accepted |

Decision:

```text
Use exactly two optimized Summoners and one Chemist support. Do not add Time Mage tempo or a third
Summoner. Preserve charge-time counterplay and keep Rend limited to the two Knights.
```

## Current Implementation (v1, entry 409 — superseded by v2 design)

Applied with `python tools/battle_patch.py balias_tor`; diff contained to local entry 25 (global 409),
62 bytes. The Summoner job IS the escalation — no extra job swap.

```text
s5  Summoner  L101 jl8  R Reflexes  M +1  Mage Hat / shop Robe / Featherweave + shop Rod
s6  Summoner  L101 jl8  (same kit)
s2  Knight    L101 jl8  R Counter  S Atk-Boost  M +1  heavy shop kit + Runeblade + Shield  (Rend innate)
s7  Knight    L101 jl8  (same kit)
s3  Archer    L101 jl8  R Reflexes  S Concentration  M +1  Thief's Cap / Black Garb / Bracers + Windslash Bow
s4  Archer    L100 jl8  (same kit)
```

This implementation remains the shipped v1 data. The v2 redesign above is **documentation only** in
this pass; it requires a later ENTD implementation pass to add the Chemist and tune the Summoners'
support/gear without changing first-playthrough behavior.

## Future Implementation Checklist (v2)

- [x] Identify Balias Tor ENTD entry (409); fill "Local Data Confirmed".
- [x] Dump original entry; verify 2 Summoner + 2 Knight + 2 Archer.
- [x] Confirm Summoner job id (82); Summon innate at jl8. (Summon-tier control = playtest item.)
- [x] Knights keep Rend innately (Battle Skill at jl8); shop-tier breakable gear.
- [ ] Add one Chemist support in a verified center/backline slot.
- [ ] Set levels: fast Summoner `102`; power Summoner + both Knights + lead Archer + Chemist `101`;
  second Archer `100`.
- [ ] Set JobLevel `8` on all active enemy slots.
- [ ] Give every active human enemy complete equipment plus intentional reaction/support/movement.
- [ ] Keep exactly two Summoners; do not add Time Mage tempo here.
- [ ] Patch the embedded ENTD in a later implementation pass; no binary/data change in this doc pass.
- [ ] Re-dump and diff; changes small and intentional.
- [ ] Playtest from a NG+ save; verify summons are scary but race-able; check summon tier.

## Test Questions

- Are the Summoners the clear priority — does ignoring them risk a party-wrecking summon?
- Can the player still RACE the cast (charge times intact), or do summons land too fast?
- Does the Chemist create target priority without causing a cleanup slog?
- Do the Rend-Knights make the rush costly while Safeguard keeps it fair?
- Does the three-flank hill force a real "pick a side" decision?
- Are the summons mid-tier (no best-summon power crept in early)?
- Is it harder than Zaland (a true caster threat) but below the Gaffgarion/Cúchulainn bosses?
- Does it still read as a hill ambush by a summoner cell, not a designed arena?

## Sources

- Game8, "Balias Tor Walkthrough (Battle 15)": roster (2 Summoner, 2 Knight, 2 Archer),
  objective "Defeat all enemies!", deploy 4, recommended level ~16, left/center/right hill
  groups, Summoners as the primary threat (race the summon), Knights' Rend / Safeguard counter,
  Chemist indispensable.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553176
- Final Fantasy Wiki, "Bariaus Hill": story/terrain context.
  https://finalfantasy.fandom.com/wiki/Bariaus_Hill
- Local: `docs/battles/011-chapter-2-overview.md` (enemy-party escalation rule), `009-ziekden-fortress.md`
  (the Rend/break exception precedent), `004-dorter-slums.md` (Black Mage/Archer builds).
</content>
