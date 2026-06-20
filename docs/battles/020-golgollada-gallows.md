# 020 - Golgollada Gallows

Status: designed (not yet implemented)
Chapter: 2 — "The Manipulator and the Subservient"
Battle order: Battle 19 (after Balias Swale)
Target version: Enhanced v1.5.0
ENTD: global entry **TBD** — confirm on Windows game data
File: `battle_entd*_ent.bin` (TBD) / `OverrideEntryData` rows (TBD)

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `011-chapter-2-overview.md`.

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

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm slots: Gaffgarion + 3 Knight + 2 Archer + 2 Time Mage, plus the player's split teams.
DO NOT touch Gaffgarion's RETREAT scripting (he must withdraw at his HP threshold, not die — his
  death + rare drop are reserved for Lionel Gate, 021).
Keep Gaffgarion's Shadowblade/Drain tied to his WEAPON so the disarm counter stays valid.
Confirm the split deployment zones (Team A near Gaffgarion).
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
```

Job IDs (carry over known, verify the rest in-game):

```text
77 = Archer            (confirmed)
Knight job id          (TBD - verify)
Time Mage job id       (TBD - verify; from Lenalian/Goug)
Dark Knight job id     (TBD - verify; Gaffgarion — from Zeirchele 014)
```

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

## Implementation Checklist

- [ ] Identify Golgollada `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify Gaffgarion + 3 Knight + 2 Archer + 2 Time Mage + split player zones.
- [ ] Confirm Dark Knight / Knight / Time Mage job IDs; keep Shadowblade WEAPON-tied (disarmable).
- [ ] Give Gaffgarion a strong NON-RARE dark blade (no rare drop here — reserved for Lionel Gate).
- [ ] Constrain BOTH Time Mages to Haste/Slow (no hard lock).
- [ ] Put Rend on TWO of the three Knights; shop-tier breakable gear only.
- [ ] Set levels: Gaffgarion `103`; Knights + Time Mages + one Archer `101`; second Archer `100`.
- [ ] Set JobLevel `8` on all active enemy slots.
- [ ] PRESERVE Gaffgarion's RETREAT threshold scripting (he must NOT die here).
- [ ] Patch via the correct layer; keep the diff inside the Golgollada window only.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify retreat + Drain intact.
- [ ] Install mod, test from a New Game+ save; confirm disarm shuts off his sustain and he retreats.

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
