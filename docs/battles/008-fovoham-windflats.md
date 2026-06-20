# 008 - Fovoham Windflats (Windmill Shed)

Status: designed (not yet implemented)
Chapter: 1
Battle order: Battle 9 (after Lenalian Plateau)
Target version: Enhanced v1.5.0
ENTD: global entry **TBD** — confirm on Windows game data
File: `battle_entd*_ent.bin` (TBD) / `OverrideEntryData` rows (TBD)

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `000-chapter-1-overview.md`.

## Original Battle

Objective:

```text
Defeat Wiegraf!  (boss fight — Wiegraf retreats automatically once his HP drops low enough)
```

Player deployment:

```text
Up to 4 units, including Ramza. No guests.
```

Original enemy composition:

```text
1x Wiegraf (boss — Corpse Brigade leader; Holy Knight / sword-skill class)
1x Knight
2x Monk
1x Chocobo
```

Public walkthrough details:

```text
Recommended level: ~8 — the highest in Chapter 1 before the Ziekden finale.
Open windmill field (Fovoham Windflats).
This is the FIRST real showdown with Wiegraf and a clear difficulty spike.
Wiegraf wields Judgment Blade — a devastating ranged sword skill that can cripple the party.
His Monks hit hard. The Chocobo adds mobility (and can self/ally heal with Choco Cure).
Strategy: kill the Monks first, then Rend Weapon on Wiegraf to disable his sword skills, then
  finish him. It's a full engagement, not a 1v1 duel.
```

Design reading:

Fovoham is **the Wiegraf spike** — the player's first clash with the Corpse Brigade's actual
leader, and the dress rehearsal for the finale. Wiegraf is not a brawler like his sister; he is
a disciplined **Holy Knight** whose **Judgment Blade** reaches across the field for huge damage.
The fight teaches the player to **respect a sword-skill boss** (his power is in his weapon — so
breaking it is the counter), to **clear his hard-hitting Monk bodyguards** before they pile on,
and to manage a **mobile Chocobo** that keeps the squad topped up. It is meant to feel like a
wall — the second-hardest fight of the chapter, just under Ziekden.

For New Game++ the identity must stay: **a tense open-field duel-plus-escort where a ranged
sword-skill boss and his bruiser guard punish a careless approach — and the counter is to break
his blade and thin his bodyguards before closing.**

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm slots: Wiegraf (named/boss) + 1 Knight + 2 Monk + 1 Chocobo, plus player slots.
Confirm Wiegraf's named-unit link (UnitId / charactercontrolid) and his AUTO-RETREAT trigger —
  do NOT break the boss scripting (he flees at low HP rather than dying here).
Confirm Wiegraf's sword skillset (Judgment Blade etc.) so Rend-Weapon counterplay still works.
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
```

Job IDs (verify all in-game):

```text
Wiegraf boss job id    (TBD - verify; named/special Holy Knight unit, handle with care)
Knight job id          (TBD - verify)
Monk job id            (TBD - verify; shares with Sand Rat)
Chocobo job id         (TBD - verify; monster, no equipment)
```

## New Game++ Design Goal

Keep the identity:

```text
A ranged sword-skill boss (Wiegraf + Judgment Blade) backed by hard Monk bodyguards and a
mobile healing Chocobo, on an open field. Break his blade, clear the Monks, then close. Spike.
```

Raise the challenge by:

```text
Giving Wiegraf a true boss kit at level +3 — durable, with his signature Judgment Blade as a
  real ranged threat — so he reads as the pre-finale wall, a step above Milleuda.
Keeping both Monks as genuine bruisers (high PA, Chakra sustain, ranged Earth Slash) so the
  "kill the bodyguards first" lesson holds at scale.
Keeping the Chocobo for mobility + Choco Cure sustain — it should prolong the fight, not win it.
Preserving the Rend-Weapon counterplay: Wiegraf's damage lives in his sword, so breaking it is
  the intended answer. Do NOT make his threat weapon-independent.
```

Boss-loot policy (Chapter 1): Wiegraf uses STRONG but NON-UNIQUE shop-tier gear. Rare,
non-buyable boss items begin in Chapter 2 — not here. (Wiegraf returns as a far bigger threat
later in the game; save the special loot for then.)

Avoid for this battle:

```text
Making Judgment Blade unavoidable/one-shotting an endgame party — keep Rend-Weapon a real out.
Time Mage control or status lock (that was Lenalian's lane; this fight is burst + bodyguards).
A second boss-tier unit (Wiegraf alone carries the spike; the rest are +0..+1).
Superboss unique gear on Wiegraf (Ch1 = non-unique only).
Pushing the generic escort past +1.
```

## Proposed Composition (New Game++ Fovoham v1)

Keep the exact original shape: Wiegraf + 1 Knight + 2 Monk + 1 Chocobo. Wiegraf at boss tier
(`103`, the chapter's joint-highest with Argath); the Monks and Knight at `101`; Chocobo `100`.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | **Wiegraf (boss)** | Holy Knight / sword-skill | `103` | The objective + the spike. Judgment Blade reaches the backline; flees at low HP. |
| n | Knight | Knight | `101` | Bodyguards Wiegraf; stalls the approach. |
| n | Monk | Monk | `101` | Hard-hitting bruiser; Chakra sustain + ranged Earth Slash. |
| n | Monk | Monk | `101` | Second bruiser; the "clear these first" threat. |
| n | Chocobo | Chocobo | `100` | Mobility + Choco Cure; prolongs the fight, doesn't win it. |

Reasoning:

The roster is already a "ranged boss + bruiser guard + mobile healer," so the faithful move is
to **scale it and elevate Wiegraf to a real boss**. Judgment Blade at `103` is the headline
danger the walkthroughs warn about — but because it is a *sword* skill, the original's counter
(break his weapon) still works, so the spike stays fair. Two scaled Monks preserve the "kill the
bodyguards first" puzzle; the Chocobo's Choco Cure keeps the fight honest without being a second
boss. Wiegraf at `103` ties Argath as the chapter's hardest single unit — correct for a
pre-finale showdown.

## Builds (final-shop quality, Holy Knight flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Wiegraf - Boss (Lv 103)

```text
Job: Holy Knight / sword-skill class (id TBD — preserve the named-unit link + auto-retreat)
JobLevel: 8
Primary/Secondary: his sword skillset incl. Judgment Blade (id TBD) — keep it WEAPON-dependent
Reaction: Counter or Damage Split (id TBD) — punishes dogpiling
Support: Attack Boost (465)
Movement: Movement +1 (486)

Head: shop heavy helm (id TBD)
Body: shop heavy armor (id TBD)        - a disciplined knight, well-armored
Accessory: Bracers (218)
Right hand: a strong shop sword (Runeblade 30 / Icebrand 29) — NON-unique, and BREAKABLE so
  Rend Weapon disables his sword skills (the intended counter)
Left hand: shop shield (id TBD)
```

Role: the pre-finale wall. His Judgment Blade is the threat; his breakable sword is the out.
Durable and disciplined, distinct from his sister's brawler kit. Strong but non-unique.

### Knight (Lv 101)

```text
Job: Knight (id TBD)   JobLevel: 8   Secondary: none (NO Break)
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head/Body: shop heavy helm + heavy armor (ids TBD)
Accessory: Bracers (218)
Right hand: Runeblade (30) or Icebrand (29)   Left hand: shop shield (id TBD)
```

Role: the wall in front of Wiegraf. Buys the Monks time to close and Wiegraf time to swing.

### Monk x2 (Lv 101)

```text
Job: Monk (id TBD)   JobLevel: 8   Secondary: none (innate Martial Arts)
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head: Headband (163)
Body: Power Garb (195) or Earth Clothes-tier (id TBD)   - Monks wear clothing, NOT heavy armor
Accessory: Bracers (218)
Right hand: none (bare-handed — Martial Arts; do NOT equip a weapon)
Left hand: none (255)
```

Role: the hard-hitting bodyguards. Chakra sustain + ranged Earth Slash mean they must be
cleared before they pile onto whoever engages Wiegraf — the original's core tactical order.

### Chocobo (Lv 100)

```text
Job: Chocobo (monster, id TBD)   JobLevel: 8
Equipment: none (monster)
Skills: Choco Attack / Choco Cure (Choco Ball only if its tier is non-threatening at scale)
Reaction / Support / Movement: monster defaults (verify legal monster skills)
```

Role: mobility + a trickle of healing. It should make the fight last a little longer (the
player may want to kill or zone it), never carry the enemy team. Keep it a single Chocobo.

## Positioning Plan

```text
Wiegraf starts at range, near the windmill / a slight rise, with long sightlines so Judgment
  Blade threatens the player's approach lane from turn 1.
The Knight starts in front of Wiegraf as a bodyguard wall.
Both Monks start forward/flanking, with movement lanes to reach the player quickly — they are
  meant to be the first contact and the first kills.
The Chocobo starts mobile on a flank, free to reposition and Choco Cure the wounded.
No guests; place the player's deployment so the approach to Wiegraf is exposed to his blade.
```

The field should say: "a ranged boss is covered by a wall and two fast bruisers, with a healer
darting around." Break the blade, clear the Monks, then close — exactly the original's read.

## Implementation Checklist

- [ ] Identify Fovoham `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify Wiegraf + 1 Knight + 2 Monk + 1 Chocobo + player slots.
- [ ] Confirm Wiegraf's named-unit link AND his auto-retreat-at-low-HP trigger; do NOT break it.
- [ ] Confirm his sword skillset stays weapon-dependent so Rend Weapon disables Judgment Blade.
- [ ] Confirm Monk (no weapon, clothing) and Chocobo (monster, no gear) builds are legal.
- [ ] Map shop-tier heavy armor / shield / PA-clothing item IDs in `ItemData.xml`.
- [ ] Set levels: Wiegraf `103`; Knight + both Monks `101`; Chocobo `100`.
- [ ] Set JobLevel `8` on all active enemy slots.
- [ ] Give Wiegraf a focus-fire reaction; keep his sword breakable + gear NON-unique.
- [ ] Knight has NO Break; Monks carry NO weapon.
- [ ] Patch via the correct layer; keep the diff inside the Fovoham window only.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify boss link + retreat.
- [ ] Install mod, test from a New Game+ save; confirm Judgment Blade is scary but Rend-able.

## Test Questions

- Is Wiegraf the second-hardest single unit of the chapter (just under Argath), as intended?
- Is Judgment Blade a genuine threat at scale while Rend Weapon remains a real, fair counter?
- Do the two Monks enforce the "clear the bodyguards first" order without overshadowing the boss?
- Does the Chocobo prolong the fight a little without ever carrying the enemy team?
- Does Wiegraf's auto-retreat (flee at low HP) still trigger correctly instead of him dying here?
- Is it clearly harder than Lenalian but a notch below the Ziekden finale, per the curve?
- Does it still read as a disciplined-knight showdown on the windflats, not a designed arena?

## Sources

- Game8, "Fovoham Windflats Walkthrough (Battle 9)": roster (Wiegraf boss + Knight + 2 Monk +
  Chocobo), objective "Defeat Wiegraf!", deploy 4, recommended level ~8, Judgment Blade as the
  devastating threat, kill-Monks-then-Rend-Weapon strategy, auto-retreat at low HP, full
  engagement (not a 1v1 duel).
  https://game8.co/games/Final-Fantasy-Tactics/archives/553170
- Final Fantasy Wiki, "Fovoham Windflats" / Wiegraf Folles: story context (Milleuda's brother,
  Corpse Brigade leader, first showdown; he returns far stronger later).
  https://finalfantasy.fandom.com/wiki/Fovoham_Windflats
- Local: `docs/battles/000-chapter-1-overview.md` (design rules), `005-sand-rat-sietch.md`
  (Monk build), `009-ziekden-fortress.md` (boss-kit + break handling), `007-lenalian-plateau.md`.
</content>
