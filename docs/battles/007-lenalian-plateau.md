# 007 - Lenalian Plateau (Lenalia Plateau)

Status: ✅ implemented (v1) — NG+ only, awaiting playtest
Chapter: 1
Battle order: Battle 8 (after Brigands' Den)
Target version: Enhanced v1.5.0
ENTD: global entry **399** (local entry 15, `battle_entd4_ent.bin`)
Patcher: `tools/battle_patch.py lenalian`

> Identified by exact roster (the only entry with a Time Mage). **Milleuda = slot s1**
> (name_id=75, same boss as Brigands' 395 — identity preserved by set_slot). Vanilla slots:
> s1 Milleuda, s2/s6 Knight, s3/s5 Black Mage, s4 Time Mage (s0 = guest Delita only; Argath has
> left). No OverrideEntryData. Implemented: Milleuda L102 (boss kit); Knights s2 L101 / s6 L100;
> Black Mages s3,s5 L101 (robe/rod); Time Mage s4 L101 with **JobLevel CAPPED at 4** so it stays
> on early-tier Time magic (Haste/Slow) and does NOT get hard lockdown (Stop/Immobilize) per the
> doc's control limit — verify in-game it never casts Stop; lower further if it does. 60 bytes.

## Original Battle

Objective:

```text
Defeat all enemies!  (in practice the fight ends when Milleuda — the boss — falls)
```

Player deployment:

```text
Up to 5 units, including Ramza. No guests — this is the party's own patrol clash.
```

Original enemy composition:

```text
1x Milleuda (boss — her second and final appearance)
3x Knight
2x Black Mage
1x Time Mage
```

Public walkthrough details:

```text
Recommended level: ~6
Open plateau/field terrain.
The two Black Mages are the primary early danger — they spam Level 2 (AoE) spells.
A Time Mage appears here — the first battlefield control in the game (Haste allies / Slow you).
Milleuda is formidable; the guide suggests Rend Power to weaken her physical hits, and keeping
  an Archer positioned apart so the Black Mages can't catch the party in one AoE.
Story: Milleuda dies here — the first death that lands on Ramza. The battle ends on her defeat.
```

Design reading:

Lenalian is **Milleuda's last stand and the chapter's first magic-control fight**. Where
Brigands' Den kept her alive with healers, here she stakes everything on a mage-heavy patrol:
two Black Mages throwing AoE and — for the first time — a **Time Mage** bending the battlefield
with Haste/Slow. It teaches the player to **respect enemy magic positioning** (don't clump into
a Level 2 spell), to handle **tempo control**, and to weaken a tough boss with Rend rather than
trading blows. Thematically it is a tragedy: a harder, sadder rematch that ends with her death.

For New Game++ the identity must stay: **an open-field magic gauntlet around a determined boss,
where stacked Black Mage AoE and a Time Mage's tempo control punish poor spacing — and the win
is reaching Milleuda one last time.**

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm slots: Milleuda (named/boss) + 3 Knight + 2 Black Mage + 1 Time Mage, plus player.
Confirm Milleuda's named-unit link (UnitId / charactercontrolid) — do NOT break boss scripting
  or the death/cutscene sequence that follows her defeat.
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
```

Job IDs (verify all in-game):

```text
Milleuda boss job id   (TBD - verify; named/special unit, same link as Brigands' Den)
Knight job id          (TBD - verify)
Black Mage job id      (TBD - verify; shares with Dorter/Ziekden)
Time Mage job id       (TBD - verify; FIRST use of this job in the mod)
```

## New Game++ Design Goal

Keep the identity:

```text
A mage-heavy open-field last stand. Two Black Mages punish clumping with AoE; a Time Mage
controls tempo; three Knights wall the casters; Milleuda is the objective. Spacing is the test.
```

Raise the challenge by:

```text
Scaling the two Black Mages so their AoE is the real threat the walkthroughs warn about —
  the player must spread out and close distance or get caught.
Keeping the Time Mage as genuine tempo pressure (Haste on its squad, Slow on the player),
  the chapter's first taste of control — but kept FAIR (see the limit below).
Giving Milleuda a slightly tougher boss kit than Brigands' Den (this is her harder rematch),
  still at boss +2 and still non-unique.
Using the three Knights as a real wall so the mages get time to cast.
```

### Special note — Time Mage control is allowed HERE (limited)

The chapter-wide rules (`000-chapter-1-overview.md`) say avoid Time Mage control in Chapter 1.
**Lenalian is the sanctioned exception** because the original fight *contains* a Time Mage and
introducing tempo control is the point of this battle. To keep it fair at NG+ scale:

```text
ALLOWED: Haste (on its own squad), Slow (on the player), Float/Reflect-style utility.
FORBIDDEN here: Stop, Immobilize, Don't Move, Don't Act — no hard lockdown on an endgame party.
Only ONE Time Mage (as in the original); do not stack control casters.
```

Boss-loot policy (Chapter 1): Milleuda uses STRONG but NON-UNIQUE shop-tier gear. Rare,
non-buyable boss items begin in Chapter 2 — not here.

Avoid for this battle:

```text
Hard status lock (see the Time Mage limit above).
A second control caster or a healer stack (that was the previous fight's puzzle, not this one).
Superboss unique gear on Milleuda (Ch1 = non-unique only).
Pushing generics past +1 (only the boss reaches +2).
```

## Proposed Composition (New Game++ Lenalian v1)

Keep the exact original shape: Milleuda + 3 Knight + 2 Black Mage + 1 Time Mage. Milleuda at
boss tier (`102`); the casters and lead Knight at `101`; the other two Knights at `100`.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | **Milleuda (boss)** | Milleuda / Squire-fighter | `102` | The objective; her harder last stand. Fight ends when she falls. |
| n | Knight | Knight | `101` | Lead wall; anchors the casters' front. |
| n | Knight | Knight | `100` | Flank wall; splits the player's approach. |
| n | Knight | Knight | `100` | Roving body; reinforces the breaking side. |
| n | Black Mage | Black Mage | `101` | AoE threat #1 — Level 2 spells punish clumping. |
| n | Black Mage | Black Mage | `101` | AoE threat #2 — the pair is the real danger. |
| n | Time Mage | Time Mage | `101` | Tempo control: Haste its squad, Slow the player (NO hard lock). |

Reasoning:

The roster already is the "magic gauntlet around a boss," so the faithful move is to **scale,
gear, and add controlled tempo pressure**. Two scaled Black Mages make spacing matter exactly
as the original taught; the Time Mage introduces tempo without crossing into lockdown; three
Knights buy the casters time. Milleuda at `102` (a notch above her Brigands' Den kit) reads as
the harder rematch this battle is meant to be. The kill-the-boss flow and her death scene stay
intact.

## Builds (final-shop quality, Corpse Brigade leadership flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Milleuda - Boss (Lv 102, harder rematch)

```text
Job: Milleuda / Squire-fighter (id TBD — preserve the named-unit link)   JobLevel: 8
Secondary: Fundaments (5) — Squire utility, fits a rallying leader making a last stand
Reaction: Damage Split or Counter (id TBD) — punishes dogpiling
Support: Attack Boost (465)
Movement: Movement +1 (486)

Head: Headband (163) or shop hat (id TBD)
Body: Power Garb (195) or shop light armor (id TBD)   - slightly better than Brigands' Den
Accessory: Bracers (218)
Right hand: Runeblade (30) (NON-unique; a touch stronger than her Brigands' Den blade)
Left hand: shop shield (id TBD) or none
```

Role: the determined boss. Tougher than her first appearance; the Rend-her-power tactic the
guide suggests should be rewarded. Still non-unique, still boss +2.

### Knight x3 (Lv 101 / 100 / 100)

```text
Job: Knight (id TBD)   JobLevel: 8   Secondary: none (NO Break)
Reaction: Counter (442)
Support: Attack Boost (465)
Movement: Movement +1 (486)

Head/Body: shop heavy helm + heavy armor (ids TBD)
Accessory: Bracers (218)
Right hand: Runeblade (30) or Icebrand (29)
Left hand: shop shield (id TBD)
```

Role: the wall that protects the casters. Three of them on open ground force the player to
fight through rather than skirmish around to the mages.

### Black Mage x2 (Lv 101)

```text
Job: Black Mage (id TBD)   JobLevel: 8   Secondary: none
Reaction: Reflexes (449) or magic-defensive reaction (id TBD)
Support: MA/Magick-boost support if available (id TBD)
Movement: Movement +1 (486)

Head: cloth/mage hat (id TBD)
Body: shop robe (Black Robe / Light Robe-tier, id TBD)
Accessory: Featherweave Cloak (234)
Right hand: shop magic-boost rod (id TBD)
Left hand: none (255)
```

Role: the headline threat. Level 2 AoE at party level punishes any cluster — the player must
spread and close, exactly the original's lesson.

### Time Mage x1 (Lv 101) — NEW job in the mod

```text
Job: Time Mage (id TBD)   JobLevel: 8   Secondary: none
Reaction: Reflexes (449) or magic-defensive reaction (id TBD)
Support: MA/Magick-boost support if available (id TBD)
Movement: Movement +1 (486)

Head: cloth/mage hat (id TBD)
Body: shop robe (id TBD)
Accessory: Featherweave Cloak (234)
Right hand: shop magic-boost rod/staff (id TBD)
Left hand: none (255)

Skillset limit: Haste / Slow / Float / Reflect-tier ONLY. NO Stop, Immobilize, Don't Move,
  or Don't Act (see the control limit above).
```

Role: the chapter's first tempo controller. Hastes its own squad and Slows the player to widen
the casters' window — pressure without removing the player's agency.

## Positioning Plan

```text
Milleuda starts central/forward as the rallying point — the objective the player fights toward.
The three Knights start in a loose wall in front of and beside the casters, covering both
  approach lanes on the open plateau.
Both Black Mages start in the back with wide sightlines — far enough that reaching them costs
  the player a turn or two of exposure.
The Time Mage starts behind the Knight wall, safe enough to keep Hasting/Slowing.
No guests; place the player's deployment to allow (but not force) a spread-out approach.
```

The open field plus stacked AoE plus tempo control should make **spacing and target priority**
the whole puzzle — kill or pressure the mages, manage Slow, then close on Milleuda.

## Implementation Checklist

- [ ] Identify Lenalian `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify Milleuda + 3 Knight + 2 Black Mage + 1 Time Mage + player.
- [ ] Confirm Milleuda's named-unit link; DO NOT break boss scripting or her death cutscene.
- [ ] Confirm Time Mage job id and constrain its skillset to Haste/Slow-tier (no hard lock).
- [ ] Map shop-tier robe / rod / heavy-armor item IDs in `ItemData.xml`.
- [ ] Set levels: Milleuda `102`; lead Knight + 2 Black Mage + Time Mage `101`; 2 Knights `100`.
- [ ] Set JobLevel `8` on all active enemy slots.
- [ ] Give Milleuda a slightly stronger (still non-unique) kit than Brigands' Den.
- [ ] Knights have NO Break; Time Mage has NO Stop/Immobilize/Don't Move/Don't Act.
- [ ] Patch via the correct layer; keep the diff inside the Lenalian window only.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify boss link intact.
- [ ] Install mod, test from a New Game+ save; confirm the fight ends on Milleuda's defeat.

## Test Questions

- Do the two Black Mages make spacing genuinely matter (is clumping punished by Level 2 AoE)?
- Does the Time Mage add real tempo pressure without feeling like a lockdown / agency-remover?
- Is Milleuda noticeably tougher than her Brigands' Den appearance (a true rematch)?
- Is "deal with the mages, manage Slow, then close on Milleuda" the obvious winning read?
- Does the fight end cleanly on Milleuda's defeat, with her death cutscene intact?
- Is it harder than Brigands' Den but below Fovoham/Ziekden, per the curve?
- Does it still feel like a tragic open-field last stand, not a designed arena?

## Sources

- Game8, "Lenalian Plateau Walkthrough (Battle 8)": roster (Milleuda boss, 3 Knight, 2 Black
  Mage, 1 Time Mage), objective, deploy 5, recommended level ~6, Black Mages spam Level 2
  spells, Rend-Power-on-Milleuda tip, battle ends on her defeat.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553169
- Final Fantasy Wiki, "Milleuda Folles": her death at Lenalia and its impact on Ramza.
  https://finalfantasy.fandom.com/wiki/Milleuda_Folles
- Local: `docs/battles/000-chapter-1-overview.md` (design rules + the Time Mage exception),
  `006-brigands-den.md` (Milleuda's first kit), `004-dorter-slums.md` (Black Mage build).
</content>
