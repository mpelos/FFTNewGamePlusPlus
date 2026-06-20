# 009 - Ziekden Fortress (Fort Zeakden)

Status: designed (not yet implemented)
Chapter: 1 — **FINALE**
Battle order: Battle 10 (after Fovoham Windflats); last battle of "The Meager"
Target version: Enhanced v1.5.0
ENTD: global entry **TBD** — confirm on Windows game data
File: `battle_entd*_ent.bin` (TBD) / `OverrideEntryData` rows (TBD)

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `000-chapter-1-overview.md`.

## Original Battle

Objective:

```text
Defeat Argath!  (boss kill — the fight ends when the boss falls, not when all enemies die)
```

Player deployment:

```text
Up to 4 units, including Ramza, across a split two-zone field.
Ally: Delita fights alongside the party as a story unit.
```

Original enemy composition:

```text
1x Argath (boss)
3x Knight
2x Black Mage
```

Public walkthrough details:

```text
Recommended level: ~9 — the highest of Chapter 1; this is the climax.
Snowbound fortress: a split battlefield that forces divided deployment, like Sand Rat.
The two Black Mages are the biggest threat if left unchecked.
The enemy Knights carry Rend abilities (equipment BREAK) — the game expects the player to
  bring the Safeguard support ability to protect their gear.
Story: this is the famous Ziekden tragedy (the Tietra hostage scene and the Ramza/Delita
  rift). That sequence is scripted cutscene, not a battle mechanic.
```

Design reading:

Ziekden is **the chapter's exam and its emotional climax in one**. Mechanically it raises every
bar at once: a real **boss** with a kill-the-leader objective, the highest recommended level of
the chapter, a **split deployment** that strains your force, two **Black Mages** as the standout
damage threat, and Knights that **break your equipment** (the one fight the original explicitly
expects you to counter with Safeguard). It is meant to feel like a wall you only clear once
you've internalized everything Chapter 1 taught.

For New Game++ the identity must be: **a genuine boss fight against Argath and his Knight/mage
escort on a divided snowfield, where the boss, the mages, and the gear-breaking Knights each
demand an answer.** This is the only Chapter 1 fight that should out-tier everything before it.

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm slots: Argath (named/boss unit) + 3 Knight + 2 Black Mage, plus split player/ally slots.
Confirm Argath's named-unit link (UnitId / charactercontrolid) — do NOT break the boss scripting.
Confirm the two player deployment zones are preserved.
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
LEAVE all scripted story/cutscene units (hostage scene) untouched.
```

Job IDs (carry over known, verify the rest in-game):

```text
Argath boss job id     (TBD - verify; likely a named/special unit, handle with care)
Knight job id          (TBD - verify; shares with Dorter/Sand Rat)
Black Mage job id      (TBD - verify; shares with Dorter)
```

## New Game++ Design Goal

Keep the identity:

```text
A climactic boss fight: kill Argath while his escort — gear-breaking Knights and two real
Black Mages — pressures a split party on a snowy fortress. The hardest fight of the chapter.
```

Raise the challenge by:

```text
Giving Argath a true boss kit: level +3, durable gear, a reaction that punishes focus-fire,
  so he is a deliberate centerpiece rather than a slightly bigger Knight.
Scaling the two Black Mages so their AoE is the standout threat the walkthroughs warn about.
KEEPING Rend / equipment break on the Knights (see special note) — this is the one fight where
  break is canonical AND telegraphed, so it stays as the signature "bring Safeguard" threat.
Preserving the split deployment so the player fights toward the boss from two directions.
```

### Special note — equipment break is allowed HERE (and only here)

The chapter-wide rules (see `000-chapter-1-overview.md`) forbid Knight equipment-break because
breaking an endgame party's gear is normally unfun. **Ziekden is the deliberate exception:** the
original fight is *built* around Rend and openly tells the player to bring Safeguard. Removing
it would erase the fight's defining challenge. To keep it fair at NG+ scale:

```text
Give Rend/break to only 1-2 of the 3 Knights, not all three.
Keep break to weapons/armor tiers the player can re-buy (shop gear), never unique items.
The boss Argath does NOT spam break — his threat is presence and durability, not gear denial.
```

Avoid for this battle (see overview rules):

```text
Time Mage control / Stop-lock (the pressure is damage + break, not lockdown).
Superboss unique gear on Argath (he is a Chapter 1 noble, not an endgame superboss).
Touching the scripted hostage/cutscene units or the boss's named-unit link.
Pushing generics past +2 (only the boss reaches +3).
```

## Proposed Composition (New Game++ Ziekden v1)

Keep the exact original shape: Argath + 3 Knights + 2 Black Mages. Argath is the only unit at
boss tier (`103`); the mages and the captain Knight sit at `101-102`.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | **Argath (boss)** | Argath / Knight-type | `103` | The objective. Durable centerpiece; the fight ends when he falls. |
| n | Knight (Render) | Knight | `102` | Front anchor with **Rend** — the telegraphed break threat. |
| n | Knight (Render) | Knight | `101` | Second breaker on the other zone; covers the split. |
| n | Knight | Knight | `100` | Pure anchor, NO break; bodyguards the mages/boss. |
| n | Black Mage | Black Mage | `101` | Standout AoE threat #1; punishes the approach to the boss. |
| n | Black Mage | Black Mage | `101` | Standout AoE threat #2; the pair is the real danger. |

Reasoning:

The roster is already a proper finale, so the faithful move is to **scale it and elevate the
boss**, not redesign. Argath at `103` with a durable kit and a focus-fire-punishing reaction
makes the kill-the-leader objective meaningful instead of a coin-flip. Two scaled Black Mages
preserve the "mages are the biggest threat" reading. Two of the three Knights keep Rend so the
Safeguard lesson still lands; the third is a clean anchor so break never feels total. The split
field forces the player to fight toward Argath from two sides, exactly as designed.

## Builds (final-shop quality; boss gets a distinct, non-unique kit)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Argath - Boss (Lv 103)

```text
Job: Argath / Knight-type (id TBD — preserve the named-unit link)   JobLevel: 8
Secondary: Fundaments (5) — Squire utility (Yell/Tailwind-style) fits an arrogant noble (NO break)
Reaction: Damage Split or Counter (id TBD) — punishes the player dogpiling the boss
Support: Attack Boost (465)
Movement: Movement +1 (486)

Head: shop heavy helm (e.g. Crystal Helm-tier, id TBD)
Body: shop heavy armor (e.g. Crystal Mail-tier, id TBD)
Accessory: Bracers (218) or a defensive accessory (id TBD)
Right hand: a strong shop sword — Runeblade (30) or Icebrand (29) (NOT a unique blade)
Left hand: shop shield (e.g. Crystal Shield-tier, id TBD)
```

Role: the centerpiece. Tanky and confident; the Damage-Split/Counter reaction means the player
can't simply alpha-strike him down without consequence. Strong but pointedly NOT a superboss.

### Knight (Render) x2 (Lv 102 / 101)

```text
Job: Knight (id TBD)   JobLevel: 8   Secondary: the Knight break command (Rend, id TBD)
Reaction: Counter (442)
Support: Attack Boost (465)
Movement: Movement +1 (486)

Head: shop heavy helm (id TBD)
Body: shop heavy armor (id TBD)
Accessory: Bracers (218)
Right hand: Runeblade (30) or Icebrand (29)
Left hand: shop shield (id TBD)
```

Role: the telegraphed break threat. They threaten the player's weapons/armor — bring Safeguard
or lose gear, exactly as the original taught. Two of them, on opposite zones.

### Knight (Anchor) x1 (Lv 100)

```text
Job: Knight (id TBD)   JobLevel: 8   Secondary: none (NO break)
Reaction: Counter (442)
Support: Attack Boost (465)
Movement: Movement +1 (486)

Gear: same shop heavy kit as above.
```

Role: a clean wall that bodyguards the mages and Argath, so break never covers the whole field.

### Black Mage x2 (Lv 101)

```text
Job: Black Mage (id TBD)   JobLevel: 8   Secondary: none
Reaction: Reflexes (449) or a magic-defensive reaction (id TBD)
Support: MA/Magick-boost support if available (id TBD)
Movement: Movement +1 (486)

Head: cloth/mage hat (id TBD)
Body: shop robe (e.g. Black Robe / Light Robe-tier, id TBD)
Accessory: Featherweave Cloak (234) or magic-defensive accessory (id TBD)
Right hand: shop rod/staff that boosts magic (id TBD)
Left hand: none (255)
```

Role: the biggest threat, per the walkthroughs. At party level their Fire/Ice/Thunder AoE
genuinely punishes the approach to Argath; the player must close or silence them fast.

## Positioning Plan

```text
Argath starts deep in the fortress, central to both zones — the player fights inward to reach him.
One Render-Knight anchors each zone's approach so both halves of the split party meet a breaker.
The clean Anchor-Knight starts near Argath / the mages as a bodyguard wall.
Both Black Mages start behind the Knight line with sightlines over the two approach lanes,
  so their AoE covers the kill zone while the Knights stall.
Preserve the two player deployment zones and Delita's ally placement.
```

The map should read as a climactic assault: two fronts, gear under threat, mages raining AoE,
and a durable boss waiting at the center.

## Implementation Checklist

- [ ] Identify Ziekden `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify Argath + 3 Knight + 2 Black Mage + split player/ally slots.
- [ ] Confirm Argath's named-unit link and DO NOT break boss/cutscene scripting.
- [ ] Confirm Knight Rend command id and Black Mage job/equipment.
- [ ] Map shop-tier heavy armor / shield / robe / rod item IDs in `ItemData.xml`.
- [ ] Set levels: Argath `103`; Render-Knight `102`/`101`; mages `101`; anchor Knight `100`.
- [ ] Set JobLevel `8` on all active enemy slots.
- [ ] Give Rend to only 2 Knights; give Argath Fundaments (no break) + a focus-fire reaction.
- [ ] Equip per builds (all non-unique / shop-tier, including the boss).
- [ ] Preserve both player zones and Delita; keep enemy positions per the plan.
- [ ] Patch via the correct layer; keep the diff inside the Ziekden window only.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify boss link intact.
- [ ] Install mod, test from a New Game+ save; confirm the kill-Argath objective still ends it.

## Test Questions

- Is this clearly the hardest fight of Chapter 1 — a real step above Dorter?
- Does Argath feel like a boss (durable, punishes dogpiling) without being a superboss wall?
- Do the two Black Mages read as the top threat, as the walkthroughs say?
- Does keeping Rend on 2 Knights preserve the "bring Safeguard" challenge without feeling cheap?
- Does the split field force a genuine two-front assault toward the boss?
- Does the kill-the-leader objective still trigger correctly (fight ends on Argath's defeat)?
- Is the scripted Tietra/Delita story sequence completely intact and unaffected?
- Does it still feel like the Ziekden climax, not a generic boss arena?

## Sources

- Game8, "Ziekden Fortress Walkthrough (Chapter 1 finale)": roster (3 Knight, 2 Black Mage,
  boss Argath), objective "Defeat Argath!", split two-zone field, deploy 4, recommended
  level ~9, Black Mages as the biggest threat, enemy Knights' Rend / Safeguard counter.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553171
- StrategyWiki / Final Fantasy Wiki, "Fort Zeakden / Ziekden Fortress": boss Algus/Argath,
  Delita ally, the Tietra hostage tragedy (scripted story), snowbound split battlefield.
  https://strategywiki.org/wiki/Final_Fantasy_Tactics
- Local: `docs/battles/000-chapter-1-overview.md` (design rules + the break exception),
  `004-dorter-slums.md` (Black Mage + Knight builds), `005-sand-rat-sietch.md` (split-field
  handling), `001-gariland.md` (confirmed item/skill IDs).
</content>
