# 052 - Mullonde Cathedral Nave (Murond Holy Place)

Status: ✅ implemented (v1, entry 461) — TIER-S unlock (Chaos Blade)
Chapter: 4 — "In the Name of Love"
Battle order: Battle 47 (Mullonde chain 2 of 3 — NO resupply across 46→47→48)
Target version: Enhanced v1.5.0
ENTD: global entry **461** (local 77, entd4)
File: `battle_entd4_ent.bin`

## Implemented (v1, entry 461)

```text
DATA (story order 459 Eagrose -> 460 Exterior -> 461 Nave; three named bosses, NO generics):
  slot 0 = Folmarv   (name 36, job 36 Divine-Knight-class; eq head154/body182/acc232/rh30/lh139 shield).
  slot 1 = Loffrey   (name 37, job 37 Divine-Knight-class; rh=29 Icebrand, lh=138 shield).
  slot 2 = Cletienne (name 39, job 39 Sorcerer; rh=57 rod, no shield).
  slot 3 = job 39 clone (name255, lvl 65, eq=0) -> scripting/summon placeholder (left untouched).

CHANGE: scale to the human-boss band + jl8 (full kit, incl. the equip-break). Folmarv 105 (leader),
  Loffrey & Cletienne 104.
  *** TIER-S UNLOCK ***: Folmarv's rh set to CHAOS BLADE (37). It is a KnightSword, so it BOTH powers
  his Divine Sword / Unyielding-Blade equip-break AND is the steal/drop reward -- delivered on the named
  kill target. Folmarv has real equip slots (unlike the Lucavi), so this works directly via ENTD.
  Loffrey & Cletienne RETREAT when one boss falls -> NO drop here; their Tier-S items pay where they
  DIE later (Loffrey -> Robe of Lords at Vaults 5th 055; Cletienne -> Materia Blade at Necrohol 056).
  Their gear is KEPT as-is. Win-on-one-falls + equip-break (Folmarv+Loffrey) + caster pressure preserved
  (only level/jl + Folmarv's blade changed; reactions/scripting untouched). Buried Elixir left as-is.
```

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `037-chapter-4-overview.md`. MULLONDE CHAIN: 46 (`051`) → 47 (`052`) → 48 (`053`), one loadout.
> **TIER-S UNLOCK BEGINS HERE** — the first best-of-best item drops in this battle.

## Original Battle

Objective:

```text
Defeat Folmarv!   (the fight ENDS the instant ANY of the three bosses falls to critical / is defeated —
                   the other two RETREAT. Folmarv is the named, intended kill target.)
```

Player deployment:

```text
Up to 5 units, including Ramza. No outfitter (chain 2/3).
```

Original enemy composition (verified via Game8, Battle 47):

```text
Folmarv Tengille   (BOSS — leader of the Knights Templar; Divine Knight; "Unyielding Blade" equip-break)
Loffrey Wodring    (BOSS — Knights Templar; Divine Knight; "Unyielding Blade" equip-break)
Cletienne Duroi    (BOSS — Knights Templar; Sorcerer / caster; ranged magic pressure)
```

> No generic support units in the original — a PURE three-boss Templar rush. (Verified: Game8 lists
> only the three named enemies.)

Public walkthrough details:

```text
Recommended level: ~60.  Difficulty: 4/5 stars.  Deploy up to 5.
Win: "Defeat Folmarv!" — but the fight ENDS once ANY of the three drops to critical / is defeated; the
  other two RETREAT. You only have to break through ONE. Folmarv is the named, intended target.
TERRAIN: the cathedral NAVE — pillared holy interior, raised altar/aisle elevation.
THE THREAT — all three are boss-tier Templars acting at once: Folmarv & Loffrey wield "UNYIELDING
  BLADE" (Divine Knight equip-break) that DESTROYS your weapons and armor; Cletienne adds ranged magic
  so you cannot simply turtle behind one wall. Three high-level bosses, one party of five.
WALKTHROUGH TIPS: use CRUSH / Rend (Meliadoul's Crush abilities) to BREAK the Templars' weapons first
  and neuter Unyielding Blade; equip Auto-Potion; Holy Sword (Agrias/Orlandeau) ignores elevation and
  hits the back line; Brawler/Ninja Ramza chases Cletienne or Loffrey; Mustadio/Chemist disrupts casters.
Spoils: 17,600 Gil; buried (rare Elixir possible).
```

Design reading:

The Nave is **the triple-Templar boss rush** — the escalation of Bervenia (`039`)'s single
equipment-break duel into **three boss-tier Knights Templar at once**. Its identity is **a focus-fire
race under an equipment-destruction threat**: Folmarv and Loffrey can **shred your weapons and armor**
with Unyielding Blade while Cletienne rains magic, so the player must **disarm the break-knights**
(Crush / Steal Weapon) and **burst ONE boss** before attrition strips the party — all while the
win-on-one-falls rule rewards *picking a target and committing* rather than fighting all three to the
death. Because the others **retreat** when one drops, only the focused boss actually dies.

For New Game++ the identity must stay: **three boss-tier Templars at once; an equipment-break threat
that punishes turtling; win the instant ONE falls (the other two retreat); a focus-and-commit race on
no resupply, the heart of the Mullonde chain.** And because only the focused boss dies — and the named
target is **Folmarv** — this is the clean place to open the **Tier-S best-of-best** unlock: **Folmarv
carries the dark Templar's blade, the Chaos Blade.** The two who retreat drop nothing (flee = no drop).

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm slots: Folmarv + Loffrey + Cletienne (three named bosses, NO generics). NO outfitter (chain 2/3).
Confirm the win condition: fight ENDS when ANY one drops to critical / is defeated; the other two RETREAT.
Keep all three at boss strength + the Unyielding Blade equip-break (on Folmarv & Loffrey only) + the
  Cletienne caster pressure. These ARE the fight.
Confirm whether OverrideEntryData carries Level / equipment, or leaves them at -1.
Set Folmarv's drop/steal = the Tier-S CHAOS BLADE (see Boss rare loot). Loffrey/Cletienne RETREAT → NO drop.
Leave the buried map treasure (possible Elixir) as-is — existing loot.
```

Job IDs (carry over known, verify the rest in-game):

```text
Folmarv  — Divine Knight / Knight Blade job id   (TBD - verify; Unyielding Blade equip-break leader)
Loffrey  — Divine Knight / Knight Blade job id   (TBD - verify; Unyielding Blade equip-break)
Cletienne — Sorcerer / caster job id             (TBD - verify; ranged magic; recurs at Necrohol 056)
```

## Job Escalation (Chapter 4 rule)

```text
CHANGE: keep the PURE three-boss Templar rush (adding generics would dilute the triple-boss identity),
  but escalate the trio to FULL Ch4 boss strength and make the MIXED kit the demand: two Divine-Knight
  equip-breakers (Folmarv, Loffrey) + one Sorcerer (Cletienne) so you cannot turtle behind a single wall.
WHY: the chapter wants more challenge via jobs WITHOUT breaking battle strategy. Here the "changed job"
  is Cletienne as a genuine caster threat flanking the two break-knights — three distinct pressure
  vectors (melee equip-break x2 + ranged magic) on one party of five. That is the escalation; bolting
  on generic adds would turn a clean boss rush into a mob fight. Consistent with prior pure-boss docs.
CONSTRAINTS (carried): EQUIP-BREAK CAPPED — only Folmarv & Loffrey carry Unyielding Blade (2 sources,
  telegraphed); Cletienne does NOT break gear. Breaks are recoverable (answer = Crush/Steal Weapon to
  disarm first, or break-resist gear) — NOT a hard lock. Cletienne's magic = intact charge times,
  race-able, soft (no permanent status lock). Win-on-one-falls preserved (the other two retreat).
WHAT IS NOT CHANGED: three named bosses, no generics, the Unyielding Blade threat, the caster pressure,
  and the "Defeat Folmarv / ends when one falls" rule remain.
```

## Sanctioned exceptions (carried precedents)

```text
UNYIELDING BLADE (equip-break, Folmarv & Loffrey) — Divine-Knight weapon/armor break; the answer is
  CRUSH / Steal Weapon (disarm them first) or break-resist gear. CAPPED at 2 sources, telegraphed,
  recoverable — NOT a hard lock (039 Bervenia precedent).
CLETIENNE CASTER MAGIC — ranged magic pressure; INTACT charge times, race-able, soft (028 precedent).
WIN-ON-ONE-FALLS — defeating ANY one boss ends the fight; the other two RETREAT (vanilla rule; flee = no drop).
TRIPLE BOSS-TIER (no generics) — three named Templars at once; the escalation is concentration, not count.
```

## Boss rare loot — TIER-S (first best-of-best)

```text
FOLMARV TENGILLE → CHAOS BLADE (Tier-S — the dark Knights-Templar blade).
  Steal-or-drop on Folmarv, the NAMED, intended kill target. Thematically the corrupted Templar
  leader's own dark sword — the iconic best-of-best dark blade, fitting the man who damns Ivalice.
  RATIONALE: only the FOCUSED boss dies (the other two retreat → flee = NO drop), and the objective
  literally names Folmarv, so the rewarded line is "commit to Folmarv, kill him, take the Chaos Blade."
  This OPENS the Tier-S tier (per 037): the best-of-best now begins, running through the endgame docs.
  LOFFREY & CLETIENNE → NO drop (they retreat). Their Tier-S items pay out where they DIE later:
    Loffrey → Vaults 5th (055), Cletienne → Necrohol (056).
  Buried map Elixir stays as-is (existing loot).
```

> Tier-S ledger (per 037): Chaos Blade (here, 052) · then Robe of Lords (Loffrey, 055) · Materia Blade
> (Cletienne, 056) · Ribbon (undead Zalbaag, 053) · Escutcheon (Lost Halidom, 057) · Ragnarok (FINAL
> capstone, 058). Excalibur stays with Orlandeau (player) — never on an enemy.

## Proposed Composition (New Game++ Mullonde Nave v1)

Keep the three bosses; no generics. Human-boss band: Folmarv (leader) `105`, Loffrey & Cletienne `104`.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Folmarv (BOSS, objective) | Divine Knight | `105` | Equip-break leader; carries the Tier-S Chaos Blade; the intended kill. |
| n | Loffrey (BOSS) | Divine Knight | `104` | Second equip-breaker; pincers with Folmarv; retreats if Folmarv falls first. |
| n | Cletienne (BOSS) | Sorcerer | `104` | Ranged magic; denies turtling; retreats if a knight falls first. |

Reasoning:

The faithful move is **three boss-tier Templars, no padding** — the pressure is concentration, not
crowd. Folmarv (`105`) and Loffrey (`104`) bring the **equip-break race** (capped 2 sources, answerable
with Crush / Steal Weapon); Cletienne (`104`) is the **caster who punishes turtling**, forcing the
party to move under fire. The win-on-one-falls rule keeps the original's *commit-to-a-target* tactics:
the player picks Folmarv (the named objective + the Chaos Blade), disarms the break-knights, and bursts
him before attrition bites — on no resupply, mid-Mullonde. It's a clean 4/5★ boss rush, harder than
Bervenia by virtue of being **three at once**.

## Builds (boss-tier; corrupted-Templar flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Folmarv Tengille (Lv 105) — BOSS, objective, Tier-S carrier

```text
Job: Divine Knight (id TBD)   JobLevel: 8   Primary: Unyielding Blade / Divine Sword (equip-break + drain)
Reaction: Damage Split / Reflexes (id TBD)   Support: break-resist / Defense Boost (id TBD)   Movement: Move +2 (id TBD)
Head: Genji Helm-tier (id TBD)   Body: heavy boss armor (id TBD)
Accessory: break-resist accessory (id TBD)   Right hand: CHAOS BLADE (Tier-S steal/drop, id TBD)   Left: shield (id TBD)
The named kill target; disarm-and-burst him for the Chaos Blade. Equip-break CAPPED, telegraphed.
```

Role: the leader; equip-break + the Tier-S reward; the focus-and-commit target.

### Loffrey Wodring (Lv 104) — BOSS, equip-break

```text
Job: Divine Knight (id TBD)   JobLevel: 8   Primary: Unyielding Blade / Divine Sword (equip-break)
Reaction: Reflexes (449)   Support: Defense Boost (id TBD)   Movement: Move +2 (id TBD)
Head: heavy helm (id TBD)   Body: heavy armor (id TBD)   Accessory: shop accessory (id TBD)
Right hand: knight sword (id TBD)   Left: shield (id TBD)
RETREATS if Folmarv (or Cletienne) falls first → NO drop (his Tier-S pays at Vaults 5th, 055).
```

Role: the second break-knight; pincers Folmarv; capped equip-break.

### Cletienne Duroi (Lv 104) — BOSS, caster

```text
Job: Sorcerer (id TBD)   JobLevel: 8   Primary: Black/area magic (INTACT charge times, race-able)
Reaction: Reflexes (449)   Support: MA-boost (id TBD)   Movement: Move +1 (486)
Head: mage hat (id TBD)   Body: shop robe (id TBD)   Accessory: Featherweave Cloak (234)
Right hand: magic-boost rod (id TBD)   Left: none (255)
No equip-break. RETREATS if a knight falls first → NO drop (his Tier-S pays at Necrohol, 056).
```

Role: ranged magic; denies turtling; soft (no permanent lock).

## Positioning Plan

```text
The cathedral NAVE: pillared holy interior with a raised altar/aisle (elevation). Place Folmarv &
  Loffrey forward to pressure the party with equip-break; Cletienne on the raised altar/back line for
  ranged magic sightlines (forcing the player to advance under fire or answer with elevation-ignoring
  Holy Sword). Keep the pillars as cover and the altar height.
Preserve: three named bosses (no generics), the equip-break pincer + caster back line, and the
  win-on-one-falls rule. The Chaos Blade rides on Folmarv, the intended target.
```

The nave should say: "three of the Knights Templar bar the altar — break one and the others flee.
Choose Folmarv, strip his guard, and take the dark blade from the man who would damn Ivalice."

## Implementation Checklist

- [ ] Identify Mullonde Nave `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify three named bosses (Folmarv/Loffrey/Cletienne), NO generics.
- [ ] Confirm win condition: fight ENDS when ANY one drops to critical/defeated; other two RETREAT.
- [ ] Keep Unyielding Blade equip-break on Folmarv & Loffrey ONLY (2 sources, capped, telegraphed).
- [ ] Keep Cletienne caster (intact charge times, race-able, no permanent lock).
- [ ] Set levels: Folmarv `105`, Loffrey & Cletienne `104`. JobLevel `8` on all three.
- [ ] Set Folmarv's steal/drop = Tier-S **Chaos Blade**; Loffrey & Cletienne carry NO rare here (they flee).
- [ ] Patch via the correct layer; keep the diff inside the Mullonde Nave window only.
- [ ] Re-dump and diff; confirm small, intentional changes; verify the 3-boss roster + win rule + Chaos Blade.
- [ ] Install mod, test from a New Game+ save; confirm focus-and-commit play, the equip-break is
      answerable (not a hard lock), and killing Folmarv yields the Chaos Blade.

## Test Questions

- Is it a clean focus-and-commit race — three boss-tier Templars, win the instant ONE falls (others retreat)?
- Is the equip-break a real but ANSWERABLE threat (2 capped sources; Crush / Steal Weapon / break-resist)?
- Does Cletienne's magic genuinely deny turtling (must move under fire / answer with elevation-ignoring hits)?
- Is Folmarv clearly the rewarded target (named objective + the Tier-S Chaos Blade) and do the others
  drop NOTHING when they retreat (flee = no drop)?
- Is it survivable on ONE loadout (no resupply, chain 2/3) yet a clear step up from Bervenia (three at once)?
- Does it read as the Knights Templar's last stand at the altar, not a designed mob?

## Sources

- Game8, "Mullonde Cathedral Nave Walkthrough (Battle 47)": three named bosses (Folmarv, Loffrey,
  Cletienne), "Defeat Folmarv!", win = fight ends when ANY one drops to critical / is defeated (others
  retreat), rec ~60, 4/5 stars, deploy 5, Unyielding Blade equip-break + Crush/Rend counter advice,
  Holy Sword / Auto-Potion tips, spoils 17,600 Gil + buried Elixir.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553207
- Final Fantasy Wiki, "Folmarv Tengille" / "Loffrey Wodring" / "Cletienne Duroi": Divine Knight /
  Sorcerer classes and Unyielding Blade context.
  https://finalfantasy.fandom.com/wiki/Folmarv_Tengille
- Local: `037-chapter-4-overview.md` (Tier-S tiering), `039-bervenia.md` (Meliadoul equip-break duel —
  the single-boss precedent this escalates), `051-mullonde-exterior.md` (chain 1/3),
  `053-mullonde-sanctuary.md` (chain 3/3 — to be designed), `055`/`056` (Loffrey/Cletienne death drops).
```
