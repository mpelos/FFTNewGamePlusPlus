# 020 - Golgollada Gallows

Status: ✅ implemented (v1, entry 414) — Gaffgarion sub-boss is the built-in escalation. **v2 redesign documented only** (implementation pending).
Chapter: 2 — "The Manipulator and the Subservient"
Battle order: Battle 19 (after Balias Swale)
Target version: Enhanced v1.5.0
ENTD: global entry **414** (battle_entd4, local entry 30) — confirmed by composition (3K/2A/2TM + boss)
File: `entd/battle_entd4_ent.bin` (embedded; swapped only in NG+ by the code mod)

> Implemented via `tools/battle_patch.py golgollada`. NG+-only by construction. See
> `011-chapter-2-overview.md`.

## Original Battle

Objective:

```text
Defeat all enemies!  (Gaffgarion RETREATS once sufficiently damaged — he does NOT die here.
  Beating him down to his retreat threshold, then clearing the rest, clears the stage.)
```

Player deployment:

```text
Up to 5 units, including Ramza — across a SPLIT deployment (Team A starts closer to Gaffgarion).
No guests: this is the first Chapter 2 fight with no allied guest — every unit is yours to manage.
```

Original enemy composition:

```text
1x Gaffgarion   (Dark Knight sub-boss — Shadowblade/Drain: damages a unit AND heals himself)
3x Knight
2x Archer
2x Time Mage    (Haste/Slow tempo support)
```

Public walkthrough details:

```text
Recommended level: ~22.
Ramza has fallen into Gaffgarion's trap; fight your way out.
Gaffgarion's threat is SUSTAIN: Shadowblade (Drain) damages a target and heals him, making a
  prolonged slugfest dangerous. The intended counter is to STRIP HIS WEAPON — Rend Weapon
  (Knight), Arm Shot (Mustadio), or Steal Weapon (Thief). Disarmed, his Drain stops and he folds.
The Knights screen him; the Archers add ranged pressure; the Time Mages Haste him / Slow you.
Split deployment: the team nearest Gaffgarion should be your strongest attackers.
```

Design reading:

The Gallows is **the Gaffgarion sub-boss fight** — the first time the player must beat the Dark
Knight down as a committed enemy (at Zeirchele he merely turned mid-battle). Its identity is a
**sustain puzzle**: Gaffgarion's Shadowblade Drain heals him as he hits, so trading blows is a
losing game — the player must **disarm him** (Rend / Arm Shot / Steal Weapon) to switch off the
sustain, while his Knight wall and Time-Mage tempo support try to keep him swinging. It teaches
the player that a boss can be solved by **denial** (take his weapon) rather than raw damage, under
a split deployment with no guest crutch. He retreats rather than dies, so this is the *threat*
chapter for Gaffgarion; the *payoff* (his death and rare drop) comes at Lionel Gate.

For New Game++ the identity must stay: **a no-guest split-deployment trap where a self-healing
Dark Knight must be disarmed (not out-damaged) while his Knights screen and Time Mages keep him
fast — denial over brute force.**

## Local Data Confirmed (entry 414)

```text
slot  cid    flags  job        role                       action
s0    0x11   0x80   17         Gaffgarion (SUB-BOSS)      SCALE -> L103 (job/sec kept)
s1    0x81   0x40   77 Archer  ranged                     SCALE -> L101
s2    0x80   0x80   76 Knight  screen (Rend)              SCALE -> L101
s3    0x80   0x80   76 Knight  screen (Rend)              SCALE -> L101
s4    0x80   0x80   76 Knight  body                       SCALE -> L101
s5    0x81   0x40   77 Archer  ranged                     SCALE -> L100
s6    0x81   0x40   81 TMage   tempo (Haste/Slow)         SCALE -> L101 (jl4)
s7    0x81   0x40   81 TMage   tempo (Haste/Slow)         SCALE -> L101 (jl4)
```

Job IDs: Knight 76, Archer 77, Time Mage 81; Gaffgarion's enemy-version job is **17** (cid 0x11 —
his committed-enemy incarnation here and at Lionel Gate; distinct from his early-Chapter ally
entry). Gaffgarion's **job 17 + secondary are PRESERVED**, so his Shadowblade/Drain sustain and his
RETREAT-at-threshold scripting (he must not die here) stay intact; his Runeblade is strong but
non-rare and STRIPPABLE so the disarm counter (Rend / Steal Weapon) shuts off his sustain. No rare
loot here (reserved for Lionel Gate). Both Time Mages jl-capped to 4 (Haste/Slow, no hard lock).

## Enemy Party Escalation (Chapter 2 redesign)

```text
VANILLA SPIRIT: a sprung Order trap with no guest support, split deployment, and Gaffgarion's
  self-healing Dark Knight pressure.
CHAPTER-2 UPGRADE: keep the canonical 8-unit trap exactly: Gaffgarion, 3 Knights, 2 Archers, and
  2 Time Mages. The v2 change is not a new job; it is making the existing trap coherent with full
  gear, full R/S/M, better screen roles, and a more mobile but still strippable Gaffgarion.
WHY: Shadowblade sustain + Haste support + a Knight screen is already the headline. Adding a
  Geomancer, extra caster, or second engine makes the fight less readable instead of better.
WHAT IS NOT CHANGED: the answer remains denial. Disarm Gaffgarion's weapon or kill/silence the
  Time Mages before trying to win the attrition race.
```

Chapter 2 requirements applied:

```text
- Every active human enemy has full equipment.
- Every active human enemy has intentional reaction, support, and movement.
- Secondary is optional; Gaffgarion's preserved Dark Knight kit and the generic primary jobs carry
  the roles.
- No active guests are present.
- Gaffgarion must remain weapon-dependent and strippable: no Safeguard/Maintenance, no
  Shirahadori/Blade Grasp, and no non-strippable rare weapon here.
```

## Sanctioned exceptions (carried precedents)

```text
TIME MAGE control — allowed (Lenalian 007 / Goug 018 precedent): the TWO canonical Time Mages are
  restricted to Haste (on Gaffgarion) / Slow (on the player) ONLY. NO Stop, Immobilize, Don't
  Move, Don't Act. This battle is the one sanctioned place two Time Mages co-exist, because they
  are canonical to the Gallows AND because Gaffgarion (not the Time Mages) is the headline; they
  exist to keep HIM fast, reinforcing the "shut him down" priority — not to lock the player.
DRAIN / self-heal on the boss — allowed and intended: Shadowblade is the fight's puzzle. It stays
  WEAPON-dependent so the disarm counter (Rend / Steal Weapon) remains the fair, telegraphed answer.
```

## Boss rare loot

```text
None HERE. Gaffgarion RETREATS — he does not die at the Gallows, so there is no drop. His rare,
non-buyable signature item is reserved for Lionel Gate (021), where he is defeated for good.
Per the Chapter 2 overview, give him a strong but NON-rare (shop-tier-best) dark blade here so
that disarming him is meaningful but no rare item can be stolen/dropped before his real death.
```

## Proposed Composition (New Game++ Golgollada Gallows v2)

Keep the exact roster; Gaffgarion is the sub-boss spike. Gaffgarion `103`; the screen and support
sit at `100`–`102` with the Time Mages and lead Knight carrying the pressure.

| Slot | Role | Job | Level | Br/Fa | Purpose |
| ------ | ------ | ----- | ------- | --- | --------- |
| n | Gaffgarion (SUB-BOSS) | Dark Knight | `103` | `82/60` | Hasted Shadowblade sustain; mobile but strippable. |
| n | Shield Knight | Knight | `102` | `76/48` | Primary bodyguard; blocks the clean disarm lane. |
| n | Rend Knight | Knight | `101` | `76/48` | Secondary screen; threatens gear if ignored. |
| n | Split Punisher | Knight | `101` | `76/48` | Pressures the weaker team and prevents five-unit dogpile. |
| n | Archer | Archer | `101` | `74/50` | Ranged punishment on the rush to Gaffgarion. |
| n | Archer | Archer | `100` | `74/50` | Second bow; covers the other deployment lane. |
| n | Haste Time Mage | Time Mage | `102` | `58/72` | Hastes Gaffgarion early; priority support target. |
| n | Slow Time Mage | Time Mage | `101` | `58/72` | Slows the disarm route; no hard-lock spells. |

Reasoning:

The faithful move is to **make Gaffgarion the spike and keep the disarm puzzle central**. At `103`
with intact Shadowblade and early Haste, he should out-sustain a stand-up fight. The player must
either force a disarm through the three-Knight screen or remove the Time Mages before committing to
the boss. The no-guest split deployment forces the player to balance both teams: the near team needs
disarm + burst, while the far team prevents the screen from collapsing inward. He retreats at
threshold, with no rare drop, preserving the Lionel Gate payoff.

## Builds (final-shop quality; Order ambush + Dark Knight flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Gaffgarion — Dark Knight SUB-BOSS (Lv 103)

```text
Job: Dark Knight (id TBD)   JobLevel: 8   Primary: Dark Sword / Shadowblade (Drain) — WEAPON-tied
Secondary: none extra (the Drain command is the threat)
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +2 (487)
Head/Body: shop heavy helm + heavy armor (ids TBD)
Accessory: Bracers (218)
Right hand: a STRONG but NON-RARE dark blade (shop-tier-best, id TBD — NOT his Lionel rare drop)
Left hand: none / two-hand marker (254)
Forbidden on Gaffgarion here: Safeguard/Maintenance, Shirahadori/Blade Grasp, non-strippable weapon.
RETREATS at HP threshold — do NOT let him die here; no rare loot at the Gallows.
```

Role: the sustain boss. Out-heals a slugfest via Shadowblade; the answer is to take his weapon.

### Knight x3 (Lv 102 / 101 / 101) — screen

```text
Shield Knight:
Job: Knight (76)   JobLevel: 8   Secondary: none
Primary: Battle Skill / Rend is inherent to the job.
Reaction: Counter (442)   Support: Defense Boost (id TBD)   Movement: Movement +1 (486)
Head/Body: shop heavy helm + heavy armor (ids TBD)
Accessory: Bracers (218)   Right hand: Runeblade (30) or Icebrand (29)   Left: shop shield (id TBD)

Rend Knight:
Job: Knight (76)   JobLevel: 8   Secondary: none
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head/Body: shop heavy helm + heavy armor (ids TBD)
Accessory: Bracers (218)   Right hand: Runeblade (30) or Icebrand (29)   Left: shop shield (id TBD)

Split Punisher:
Job: Knight (76)   JobLevel: 8   Secondary: none
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head/Body: shop heavy helm + heavy armor (ids TBD)
Accessory: Bracers (218)   Right hand: Runeblade (30) or Icebrand (29)   Left: shop shield (id TBD)
```

Role: the screen that makes reaching Gaffgarion with a disarmer costly. They may threaten gear
through Knight tools, but they do not carry rare gear and they do not replace Gaffgarion as the
headline.

### Archer x2 (Lv 101 / 100)

```text
Job: Archer (77)   JobLevel: 8   Secondary: none
Reaction: Reflexes (449)   Support: Concentration (469)   Movement: Movement +1 (486)
Head: Thief's Cap (168)   Body: Black Garb (198)   Accessory: Bracers (218)
Right hand: Windslash Bow (87)   Left hand: none / two-hand marker (254)
```

Role: ranged punishment on the dash toward Gaffgarion.

### Time Mage x2 (Lv 102 / 101) — Haste/Slow only

```text
Haste Time Mage:
Job: Time Mage (81)   JobLevel: 4 cap or command-filter equivalent   Secondary: none
Skillset limit: Haste (on Gaffgarion) / Slow (on the player) / Float-tier ONLY.
  NO Stop, Immobilize, Don't Move, Don't Act.
Reaction: Reflexes (449)   Support: Swiftness/Short Charge (id TBD)   Movement: Movement +1 (486)
Head: cloth/mage hat (id TBD)   Body: shop robe (id TBD)
Accessory: Featherweave Cloak (234)   Right hand: shop magic-boost rod (id TBD)   Left: none (255)

Slow Time Mage:
Job: Time Mage (81)   JobLevel: 4 cap or command-filter equivalent   Secondary: none
Skillset limit: Haste/Slow/Float-tier ONLY.
Reaction: Reflexes (449)   Support: MA/Magick-boost or Swiftness (id TBD)   Movement: Movement +1 (486)
Head: cloth/mage hat (id TBD)   Body: shop robe (id TBD)
Accessory: Featherweave Cloak (234)   Right hand: shop magic-boost rod (id TBD)   Left: none (255)
```

Role: keep Gaffgarion fast so his Drain swings more often — reinforcing "disarm him quickly,"
without ever locking the player down.

## Positioning Plan

```text
Gaffgarion starts deep on his side, behind the Knight screen, near the Team-A deployment so the
  player's strongest team faces him first, but not so deep that disarm cannot be attempted by
  round 2-3.
The Shield Knight and Rend Knight start between Gaffgarion and the player's disarmer's path; the
  Split Punisher pressures the far (Team-B) deployment.
The two Archers hold mid-range covering both approach lanes.
The two Time Mages start near/behind Gaffgarion so they can Haste him early, but they must remain
  reachable by a committed dive, Silence, or ranged pressure.
Preserve the split deployment zones and Gaffgarion's RETREAT scripting.
```

The Gallows should say: "you're trapped with a self-healing Dark Knight — take his sword or lose
the war of attrition — and do it before the Time Mages keep him swinging all day."

## Simulation Plan and Results

Simulation artifact:

```text
tmp/fft-level-design-020-golgollada-gallows/
```

Model scope:

```text
First four rounds only; compares the armed Gaffgarion pressure, the pressure after weapon denial,
and the risk of variants that invalidate the intended answer. The model accepts pressure only when
the disarm payoff remains high and rejects Safeguard, hard-lock Time Magic, and extra enemy bodies.
```

Iteration results:

| Candidate | Enemies | Enemy actions | Action ratio | Pressure armed | Pressure disarmed | Disarm payoff | Delta vs v1 | Result |
|-----------|---------|---------------|--------------|----------------|-------------------|---------------|-------------|--------|
| v1 current trap | 8 | 26.6 | 2.11 | 127.1 | 73.2 | 42.4% | +0.0% | Baseline |
| Gaffgarion with Safeguard | 8 | 26.6 | 2.11 | 142.7 | 85.4 | 8.9% | +12.3% | Rejected: invalidates disarm |
| Hard-lock Time Mages | 8 | 26.8 | 2.20 | 163.5 | 83.5 | 42.6% | +28.6% | Rejected: hard control |
| Extra Archer body | 9 | 30.0 | 2.50 | 155.9 | 85.2 | 42.4% | +22.7% | Rejected: too dense |
| v2 sharpened disarm trap | 8 | 26.8 | 2.20 | 143.5 | 81.3 | 43.4% | +12.9% | Accepted |

Decision:

```text
Keep the canonical 8-enemy trap and sharpen existing roles. Gaffgarion stays strippable, Time
Mages stay Haste/Slow only, and the single stronger add is a Knight Captain inside the existing
three-Knight screen rather than an extra enemy.
```

## Current Implementation (v1, entry 414 — superseded by v2 design)

Applied with `python tools/battle_patch.py golgollada`; diff contained to local entry 30 (global
414), 77 bytes.

```text
s0  Gaffgarion  L103 jl8  (job 17 + secondary KEPT)  R Counter  S Atk-Boost  M +1  heavy kit + Runeblade(strippable) + Shield
s2  Knight      L101 jl8  R Counter  S Atk-Boost  M +1  heavy shop kit + Runeblade + Shield  (Rend innate)
s3  Knight      L101 jl8  (same kit)
s4  Knight      L101 jl8  (same kit)
s1  Archer      L101 jl8  R Reflexes  S Concentration  M +1  Thief's Cap / Black Garb / Bracers + Windslash Bow
s5  Archer      L100 jl8  (same kit)
s6  Time Mage   L101 jl4  R Reflexes  M +1  Mage Hat / shop Robe / Featherweave + shop Rod  (Haste/Slow)
s7  Time Mage   L101 jl4  (same kit)
```

This implementation remains the shipped v1 data. The v2 redesign above is **documentation only** in
this pass; it requires a later implementation pass to tune movement/support roles, verify the
Time Mage command filter/cap, and re-check the disarm window in game.

## Future Implementation Checklist (v2)

- [x] Identify Golgollada ENTD entry (414); fill "Local Data Confirmed".
- [x] Dump original entry; verify Gaffgarion + 3 Knight + 2 Archer + 2 Time Mage.
- [x] Confirm job IDs; keep Shadowblade WEAPON-tied (Runeblade, strippable).
- [ ] Give Gaffgarion a strong NON-RARE, strippable blade and explicitly no Safeguard/Maintenance.
- [ ] Set v2 levels: Gaffgarion `103`; Shield Knight + Haste Time Mage `102`; Rend Knight +
  Split Punisher + lead Archer + Slow Time Mage `101`; second Archer `100`.
- [ ] Set JobLevel `8` on non-Time-Mage enemies; keep Time Mages at jl4 or command-filtered.
- [ ] Give every active human enemy complete equipment plus intentional reaction/support/movement.
- [ ] Verify Time Mages only use Haste/Slow/Float-tier tools; no hard-lock spells.
- [ ] Preserve Gaffgarion's job/secondary -> retreat + Drain scripting intact.
- [ ] Preserve split deployment and retreat threshold; no rare item/drop here.
- [ ] Patch the embedded ENTD in a later implementation pass; no binary/data change in this doc pass.
- [ ] Re-dump and diff; changes small and intentional.
- [ ] Playtest from a NG+ save; confirm disarm shuts off sustain and he retreats (no death/drop).

## Test Questions

- Is Gaffgarion a real sustain threat — does trading blows without disarming him lose the fight?
- Is the disarm counter (Rend / Steal Weapon) reachable through the Knight screen, and decisive?
- Does Gaffgarion stay strippable (no Safeguard/Maintenance or non-strippable weapon behavior)?
- Do the two Time Mages reinforce "shut Gaffgarion down fast" without locking the player out?
- Can the player also answer the fight by killing/silencing Time Mages before committing to the boss?
- Does the no-guest split deployment force genuine two-team management?
- Does he RETREAT (not die) with no lootable rare item, preserving the Lionel Gate payoff?
- Is it a clear step above the generic Ch2 fights but below Lionel Gate / Cúchulainn?
- Does it still read as a sprung trap by the Order, not a designed arena?

## Sources

- Game8, "Golgollada Gallows Walkthrough (Battle 19)": roster (Gaffgarion + 3 Knight, 2 Archer,
  2 Time Mage), objective "Defeat all enemies!", recommended level ~22, deploy 5 with split zones
  (Team A near Gaffgarion), no guest, Gaffgarion's Shadowblade/Drain sustain and the disarm
  counter (Rend / Arm Shot / Steal Weapon), "gang up on Gaffgarion until he retreats."
  https://game8.co/games/Final-Fantasy-Tactics/archives/553179
- Final Fantasy Wiki, "Golgollada Gallows": story/terrain context.
  https://finalfantasy.fandom.com/wiki/Golgollada_Gallows
- Local: `docs/battles/011-chapter-2-overview.md` (enemy-party escalation + boss-loot rules),
  `014-zeirchele-falls.md` (Gaffgarion's betrayal / Dark Knight intro), `018-goug-lowtown.md`
  (Time Mage Haste/Slow limit), `016-balias-tor.md` (Knight Rend exception).
</content>
