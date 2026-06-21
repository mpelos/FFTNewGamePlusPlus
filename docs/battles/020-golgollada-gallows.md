# 020 - Golgollada Gallows

Status: ✅ implemented (v1, entry 414) — Gaffgarion sub-boss is the built-in escalation
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

## Job Escalation (Chapter 2 rule)

```text
THE ESCALATION IS BUILT IN: this is the first fight where Gaffgarion is a committed Dark Knight
SUB-BOSS you must beat to his retreat threshold — his Shadowblade/Drain SUSTAIN is the new
tactical wrinkle (a boss you solve by DENIAL/disarm, not raw damage). Per "one new wrinkle per
fight," NO additional generic job is swapped in; the canonical 3 Knight / 2 Archer / 2 Time Mage
screen is kept.
WHY: a self-healing boss + disarm puzzle + no-guest split deployment is already a dense step up.
  Adding another new job on top would muddy the "disarm Gaffgarion" read.
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

## Proposed Composition (New Game++ Golgollada Gallows v1)

Keep the exact roster; Gaffgarion is the sub-boss spike. Gaffgarion `103`; Knights `101`; Time
Mages `101`; Archers `100`–`101`.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Gaffgarion (SUB-BOSS) | Dark Knight | `103` | Shadowblade/Drain sustain; must be DISARMED, then beaten to retreat. |
| n | Knight (Rend) | Knight | `101` | Screens Gaffgarion; break-wall on the approach. |
| n | Knight (Rend) | Knight | `101` | Second screen; contests the disarmer reaching Gaffgarion. |
| n | Knight | Knight | `101` | Third body; pressures the player's weaker split team. |
| n | Archer | Archer | `101` | Ranged punishment on the rush to Gaffgarion. |
| n | Archer | Archer | `100` | Second bow; covers the other deployment lane. |
| n | Time Mage | Time Mage | `101` | Hastes Gaffgarion (keeps his Drain swinging) / Slows the player. |
| n | Time Mage | Time Mage | `101` | Second tempo caster; reinforces the "shut Gaffgarion down fast" clock. |

Reasoning:

The faithful move is to **make Gaffgarion the spike and keep the disarm puzzle central**. At `103`
with intact Shadowblade he genuinely out-sustains a stand-up fight, so the player must commit a
disarmer (Rend / Steal Weapon) through the three-Knight screen while two Time Mages keep him fast
and the Archers punish the rush. The no-guest split deployment forces the player to balance both
teams — the one near Gaffgarion needs the disarm + damage, the far team must survive the Knights.
He retreats at threshold (no kill, no drop), preserving the Lionel Gate payoff. This is a clear
step above the generic fights but still a notch below the true bosses (Lionel Gate, Cúchulainn).

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
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head/Body: shop heavy helm + heavy armor (ids TBD)
Accessory: Bracers (218)
Right hand: a STRONG but NON-RARE dark blade (shop-tier-best, id TBD — NOT his Lionel rare drop)
Left hand: none / two-hand marker (254)
RETREATS at HP threshold — do NOT let him die here; no rare loot at the Gallows.
```

Role: the sustain boss. Out-heals a slugfest via Shadowblade; the answer is to take his weapon.

### Knight x3 (Lv 101) — 2x Rend

```text
Job: Knight (id TBD)   JobLevel: 8   Secondary: Rend (break) on TWO of the three (id TBD)
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head/Body: shop heavy helm + heavy armor (ids TBD)
Accessory: Bracers (218)   Right hand: Runeblade (30) or Icebrand (29)   Left: shop shield (id TBD)
```

Role: the screen that makes reaching Gaffgarion with a disarmer costly; Safeguard stays relevant.

### Archer x2 (Lv 101 / 100)

```text
Job: Archer (77)   JobLevel: 8   Secondary: none
Reaction: Reflexes (449)   Support: Concentration (469)   Movement: Movement +1 (486)
Head: Thief's Cap (168)   Body: Black Garb (198)   Accessory: Bracers (218)
Right hand: Windslash Bow (87)   Left hand: none / two-hand marker (254)
```

Role: ranged punishment on the dash toward Gaffgarion.

### Time Mage x2 (Lv 101) — Haste/Slow only

```text
Job: Time Mage (id TBD)   JobLevel: 8   Secondary: none
Skillset limit: Haste (on Gaffgarion) / Slow (on the player) / Float-tier ONLY.
  NO Stop, Immobilize, Don't Move, Don't Act.
Reaction: Reflexes (449)   Support: MA/Magick-boost (id TBD)   Movement: Movement +1 (486)
Head: cloth/mage hat (id TBD)   Body: shop robe (id TBD)
Accessory: Featherweave Cloak (234)   Right hand: shop magic-boost rod (id TBD)   Left: none (255)
```

Role: keep Gaffgarion fast so his Drain swings more often — reinforcing "disarm him quickly,"
without ever locking the player down.

## Positioning Plan

```text
Gaffgarion starts deep on his side, behind the Knight screen, near the Team-A deployment so the
  player's strongest team faces him first.
Two Rend-Knights start between Gaffgarion and the player's disarmer's path; the third Knight
  pressures the far (Team-B) deployment.
The two Archers hold mid-range covering both approach lanes.
The two Time Mages start near/behind Gaffgarion so they can Haste him early.
Preserve the split deployment zones and Gaffgarion's RETREAT scripting.
```

The Gallows should say: "you're trapped with a self-healing Dark Knight — take his sword or lose
the war of attrition — and do it before the Time Mages keep him swinging all day."

## Implemented (v1, entry 414)

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

## Implementation Checklist

- [x] Identify Golgollada ENTD entry (414); fill "Local Data Confirmed".
- [x] Dump original entry; verify Gaffgarion + 3 Knight + 2 Archer + 2 Time Mage.
- [x] Confirm job IDs; keep Shadowblade WEAPON-tied (Runeblade, strippable).
- [x] Give Gaffgarion a strong NON-RARE dark blade (no rare drop here).
- [x] Both Time Mages jl-capped to 4 (Haste/Slow, no hard lock).
- [x] Knights carry Rend innately (Battle Skill at jl8); shop-tier breakable gear.
- [x] Set levels: Gaffgarion `103`; Knights + Time Mages + one Archer `101`; second Archer `100`.
- [x] Set JobLevel `8` (Time Mages jl4).
- [x] PRESERVE Gaffgarion's job/secondary -> retreat + Drain scripting intact.
- [x] Patch the embedded ENTD (NG+-only); diff inside entry 414 only.
- [x] Re-dump and diff; changes small and intentional.
- [ ] Playtest from a NG+ save; confirm disarm shuts off sustain and he retreats (no death/drop).

## Test Questions

- Is Gaffgarion a real sustain threat — does trading blows without disarming him lose the fight?
- Is the disarm counter (Rend / Steal Weapon) reachable through the Knight screen, and decisive?
- Do the two Time Mages reinforce "shut Gaffgarion down fast" without locking the player out?
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
- Local: `docs/battles/011-chapter-2-overview.md` (job-escalation + boss-loot rules),
  `014-zeirchele-falls.md` (Gaffgarion's betrayal / Dark Knight intro), `018-goug-lowtown.md`
  (Time Mage Haste/Slow limit), `016-balias-tor.md` (Knight Rend exception).
</content>
