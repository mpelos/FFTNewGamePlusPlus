# 006 - Brigands' Den (Thieves Fort)

Status: designed (not yet implemented)
Chapter: 1
Battle order: Battle 7 (after Sand Rat Sietch)
Target version: Enhanced v1.5.0
ENTD: global entry **TBD** — confirm on Windows game data
File: `battle_entd*_ent.bin` (TBD) / `OverrideEntryData` rows (TBD)

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `000-chapter-1-overview.md`.

## Original Battle

Objective:

```text
Defeat Milleuda!  (boss kill — the fight ends when Milleuda falls, not when all enemies die)
```

Player deployment:

```text
Up to 4 units, including Ramza.
Allies: Argath and Delita assist as story units.
```

Original enemy composition:

```text
1x Milleuda (boss — Corpse Brigade leader, Wiegraf's sister)
1x Knight
2x White Mage
3x Thief
```

Public walkthrough details:

```text
Recommended level: ~5
Rainy map with a raised platform on the right side.
Rain AMPLIFIES Thunder damage (for both sides).
The White Mages drag the fight out by healing allies and also throw offensive magic.
The Thieves are fast and harass; the Knight anchors.
Standard read: deal with the healers, then focus Milleuda once her HP drops to end it.
```

Design reading:

Brigands' Den is **the first fight against a named boss** and the first time the player meets
the Corpse Brigade's *leadership* rather than its rabble. Milleuda is an idealist, not a thug,
and the fight is framed as a raid on a thieves' hideout in the rain. Mechanically it teaches
three new lessons: a **kill-the-boss objective** (you don't have to clear the map), **enemy
healers that prolong a fight** (you must remove or pressure the White Mages, or Milleuda never
dies), and a **weather gimmick** (rain boosts Thunder). The three Thieves add speed and theft.

For New Game++ the identity must stay: **a rainy hideout raid where a charismatic boss is kept
alive by healers while fast thieves harass you — and the win condition is reaching her.**

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm slots: Milleuda (named/boss unit) + 1 Knight + 2 White Mage + 3 Thief, plus player/ally.
Confirm Milleuda's named-unit link (UnitId / charactercontrolid) — do NOT break boss scripting.
Confirm the map keeps its rain flag (Thunder amplification is part of the design).
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
```

Job IDs (carry over known, verify the rest in-game):

```text
83 = Thief             (confirmed)
Milleuda boss job id   (TBD - verify; named/special unit, handle with care)
Knight job id          (TBD - verify; shares with Dorter/Sand Rat)
White Mage job id      (TBD - verify)
```

## New Game++ Design Goal

Keep the identity:

```text
A rainy raid on a thieves' den. Milleuda is the objective; her White Mages keep her and the
squad standing; three Thieves harass and steal; the rain rewards Thunder. Reach the boss.
```

Raise the challenge by:

```text
Giving Milleuda a real (but modest) boss kit — level +2, durable gear, a reaction that
  punishes focus-fire — so the first named boss feels deliberate, not just a bigger Thief.
Scaling the two White Mages so their healing genuinely prolongs the fight (the core puzzle):
  the player must split fire onto the healers, or Milleuda's HP keeps topping off.
Keeping all three Thieves so the backline stays under fast, stealing pressure.
Leaning into the rain: at least one enemy carries Thunder so the weather gimmick still bites.
```

Boss-loot policy (Chapter 1):

```text
Milleuda is a Chapter 1 boss, so she uses STRONG but NON-UNIQUE shop-tier gear (like Argath).
Rare, non-buyable boss items begin in CHAPTER 2 per the campaign plan — not here. This keeps
the Ch1 reward/escalation curve flat and saves rare drops for when they mean more.
```

Avoid for this battle (see overview rules):

```text
Time Mage control (that arrives next battle, at Lenalian) — keep the pressure to heal + harass.
Steal Heart / charm on the Thieves (cheap this early); keep theft to gear/gil at most.
Superboss unique gear on Milleuda (Ch1 = non-unique only).
Pushing generics past +1 (only the boss reaches +2).
```

## Proposed Composition (New Game++ Brigands' Den v1)

Keep the exact original shape: Milleuda + 1 Knight + 2 White Mage + 3 Thief. Milleuda at boss
tier (`102`); healers and Knight at `101`; the three Thieves at `100`.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | **Milleuda (boss)** | Milleuda / Squire-fighter | `102` | The objective. Durable charismatic frontliner; fight ends when she falls. |
| n | Knight | Knight | `101` | Bodyguards Milleuda and the healers; stalls the approach. |
| n | White Mage | White Mage | `101` | Sustain engine #1 — heals the squad; the reason the fight drags. |
| n | White Mage | White Mage | `101` | Sustain engine #2 + offensive magic; carries Thunder for the rain. |
| n | Thief | Thief | `100` | Fast flanker; harasses the backline, steals. |
| n | Thief | Thief | `100` | Second flanker; splits the player's attention. |
| n | Thief | Thief | `100` | Third flanker; speed-in-numbers pressure. |

Reasoning:

The roster is already a perfect "boss + healers + harassers" puzzle, so the faithful move is to
**scale, gear, and elevate the boss**. The two White Mages are the heart of the fight: at party
level their heals actually keep Milleuda alive, forcing the player to either burst the boss
faster than the heals or silence/kill the mages first — exactly the original's lesson, now with
teeth. Milleuda at `102` with a focus-fire-punishing reaction makes reaching her meaningful.
Three Thieves keep the rainy-raid chaos. One White Mage carrying Thunder keeps the rain gimmick
live (and the player can exploit it too).

## Builds (final-shop quality, Corpse Brigade leadership flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Milleuda - Boss (Lv 102)

```text
Job: Milleuda / Squire-fighter (id TBD — preserve the named-unit link)   JobLevel: 8
Secondary: Fundaments (5) — Squire utility (Yell/Tailwind-style) fits a rallying leader
Reaction: Damage Split or Counter (id TBD) — punishes the player dogpiling the boss
Support: Attack Boost (465)
Movement: Movement +1 (486)

Head: Headband (163) or a shop hat (id TBD)
Body: Power Garb (195) or shop light armor (id TBD)
Accessory: Bracers (218)
Right hand: a strong shop sword — Icebrand (29) or Runeblade (30) (NON-unique)
Left hand: shop shield (id TBD) or none
```

Role: the charismatic frontline boss. Durable enough to be a real objective, with a reaction
that taxes a careless alpha-strike. Strong but pointedly non-unique (Chapter 1 boss).

### Knight (Lv 101)

```text
Job: Knight (id TBD)   JobLevel: 8   Secondary: none (NO Break skillset)
Reaction: Counter (442)
Support: Attack Boost (465)
Movement: Movement +1 (486)

Head/Body: shop heavy helm + heavy armor (ids TBD)   - Knights CAN wear heavy armor
Accessory: Bracers (218)
Right hand: Runeblade (30) or Icebrand (29)
Left hand: shop shield (id TBD)
```

Role: the wall between the player and Milleuda/healers. Buys the White Mages time to heal.

### White Mage x2 (Lv 101)

```text
Job: White Mage (id TBD)   JobLevel: 8   Secondary: none (innate White Magick;
  one mage may carry a single offensive Thunder option for the rain — id TBD)
Reaction: Reflexes (449) or a magic-defensive reaction (id TBD)
Support: MA/Magick-boost support if available (id TBD)
Movement: Movement +1 (486)

Head: cloth/mage hat (id TBD)
Body: shop robe (e.g. Light Robe-tier, id TBD)
Accessory: Featherweave Cloak (234)
Right hand: shop staff that boosts magic / healing (id TBD)
Left hand: none (255)
```

Role: the sustain engines and the whole reason the fight is a puzzle. Kill or pressure them or
Milleuda never stays down. The Thunder option keeps the rain gimmick two-sided.

### Thief x3 (Lv 100)

```text
Job: Thief (83)   JobLevel: 8   Secondary: Steal (mild — NO Steal Heart)
Reaction: First Strike (453)
Support: Attack Boost (465)
Movement: Movement +2 (487)

Head: Thief's Cap (168)
Body: Black Garb (198)
Accessory: Germinas Boots (210)
Right hand: Air Knife (9)
Left hand: none / two-hand marker (254)
```

Role: speed-in-numbers harassment. They flank the backline and steal, forcing the player to
protect their support while pushing toward Milleuda. Keep theft to gear/gil — no charm.

## Positioning Plan

```text
Milleuda starts deep, on or behind the raised platform on the right — the player must fight
  across the den to reach the objective.
Knight starts in front of Milleuda / the healers as a bodyguard wall.
Both White Mages start on the raised platform behind the Knight — protected, with sightlines
  to heal the whole squad (and to lob Thunder in the rain).
The three Thieves start spread wide / forward, with movement lanes to loop to the backline.
Preserve the rain flag and Argath/Delita ally placement.
```

The map should say: "the boss is guarded and healed on high ground, and you're being harassed
on the way in." Reaching and bursting Milleuda before the heals out-pace you is the puzzle.

## Implementation Checklist

- [ ] Identify Brigands' Den `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify Milleuda + 1 Knight + 2 White Mage + 3 Thief + player/ally.
- [ ] Confirm Milleuda's named-unit link; DO NOT break boss/cutscene scripting.
- [ ] Confirm White Mage job/equipment and a legal offensive-Thunder option for the rain.
- [ ] Map shop-tier staff / robe / light-armor item IDs in `ItemData.xml`.
- [ ] Set levels: Milleuda `102`; Knight + both White Mages `101`; all three Thieves `100`.
- [ ] Set JobLevel `8` on all active enemy slots.
- [ ] Give Milleuda Fundaments + a focus-fire reaction; keep her gear NON-unique.
- [ ] Keep Thief Steal mild (no Steal Heart); Knight has NO Break.
- [ ] Preserve the rain flag and the raised-platform positions.
- [ ] Patch via the correct layer; keep the diff inside the Brigands' Den window only.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify boss link intact.
- [ ] Install mod, test from a New Game+ save; confirm "Defeat Milleuda" still ends it.

## Test Questions

- Do the two White Mages make the fight a real "kill the healers first" puzzle at scale?
- Does Milleuda feel like the first named boss — durable, punishes dogpiling — without a wall?
- Is the kill-the-boss objective intact (fight ends on Milleuda's defeat, not full clear)?
- Do three Thieves harass meaningfully without their theft feeling cheap?
- Does the rain still matter (is Thunder noticeably stronger for both sides)?
- Is it harder than Sand Rat but easier than Lenalian/Fovoham, per the curve?
- Does it still read as a rainy raid on a thieves' den, not a designed arena?

## Sources

- Game8, "Brigands' Den Walkthrough (Battle 7)": roster (Milleuda boss, 1 Knight, 2 White
  Mage, 3 Thief), objective "Defeat Milleuda!", deploy 4, recommended level ~5, raised
  platform + rain (Thunder amplified), White Mages prolong the fight with heals + offensive
  magic, allies Ramza/Argath/Delita.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553168
- Final Fantasy Wiki, "Milleuda Folles" / "Brigands' Den": story context (Wiegraf's sister,
  Corpse Brigade leadership, the ideological confrontation).
  https://finalfantasy.fandom.com/wiki/Milleuda_Folles
- Local: `docs/battles/000-chapter-1-overview.md` (design rules), `009-ziekden-fortress.md`
  (boss-kit approach), `001-gariland.md` (confirmed Thief/item/skill IDs).
</content>
