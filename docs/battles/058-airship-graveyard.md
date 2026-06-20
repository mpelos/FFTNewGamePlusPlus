# 058 - Airship Graveyard (THE FINAL BATTLE — Hashmal → Ultima)

Status: designed (not yet implemented)
Chapter: 4 — "In the Name of Love" (CAPSTONE — the last battle of the campaign / the mod)
Battle order: Battle 53 (ENDGAME GAUNTLET 5 of 5 — NO resupply across 49→50→51→52→53; the climax)
Target version: Enhanced v1.5.0
ENTD: global entry **TBD** — confirm on Windows game data
File: `battle_entd*_ent.bin` (TBD) / `OverrideEntryData` rows (TBD)

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `037-chapter-4-overview.md`. THE FINAL FIGHT — a TWO-PHASE Lucavi finale: Hashmal, then Ultima
> (who transforms to a stronger second form at low HP). HP/MP fully restore between the phases.

## Original Battle

Objective:

```text
"Defeat Hashmal!"  →  (HP/MP fully restored)  →  "Defeat Ultima!"  (including her second form)
The campaign ENDS in victory when Ultima's second form falls.
```

Player deployment:

```text
Up to 5 units, including Ramza. No outfitter (gauntlet 5/5 — the climax of the no-resupply run).
```

Original enemy composition (verified via Game8, Battle 53):

```text
PHASE 1 — HASHMAL (Lucavi):  Hashmal (BOSS — wide-area attacks) + demon support.
  [Note: Game8's roster line also carries "Barich (Lost Halidom)" as a label artifact from the prior
   battle (057); the phase-1 boss is HASHMAL. Verify the exact phase-1 demon support in-game.]

— on Hashmal's defeat: PARTY HP/MP FULLY RESTORED (a scripted breather before Ultima) —

PHASE 2 — ULTIMA (the final Lucavi):  Ultima (BOSS) + several Ultima Demons SURROUNDING your team.
  Ultima casts DISPELJA (strips your buffs) and ALMAGEST (deals a % of max HP as AoE damage).
  At LOW HP, Ultima TRANSFORMS into a stronger SECOND FORM (regains strength, stronger spells).
```

Public walkthrough details:

```text
Recommended level: 60+.  Difficulty: 4/5 stars (the scripted full-restore between phases eases the raw
  attrition vs the 5★ Lost Halidom, but this is the CLIMAX).  Deploy up to 5.
Win: defeat Hashmal, then defeat Ultima (second form). The game ends in victory.
TERRAIN: the Airship Graveyard (the buried ancient airship beneath Orbonne — the final arena).
THE THREAT —
  PHASE 1 HASHMAL: WIDE-AREA attacks (spread out); a Lucavi bruiser with demon support.
  INTERPHASE: HP/MP fully restored — re-buff and reposition before Ultima.
  PHASE 2 ULTIMA: surrounds you with Ultima Demons; DISPELJA strips your buffs; ALMAGEST hits the party
    for a % of max HP; at low HP she TRANSFORMS to a stronger second form with bigger spells.
WALKTHROUGH TIPS: spread vs wide-area/Almagest; re-apply buffs after Dispelja; status immunity (RIBBON,
  earned 053) blunts the demons; burst each form down with your best (Excalibur/Orlandeau, the Tier-S
  gear earned across the gauntlet).
Spoils: campaign victory.
```

Design reading:

The Airship Graveyard is **the capstone** — a **two-phase Lucavi finale** that is the entire mod's
climax. Its identity is **a scripted three-stage endurance duel**: **Hashmal** (wide-area Lucavi bruiser)
→ a **full HP/MP restore** (the game's one mercy) → **Ultima** amid an **Ultima-Demon surround**, who
**dispels your buffs** (Dispelja), **chips the whole party for % max HP** (Almagest), and at low HP
**transforms into a stronger second form** for the final escalation. It rewards everything the campaign
taught: **spread vs AoE, re-buff after dispel, answer status with the Ribbon, and burst each form** with
the best-in-game gear the player has assembled.

For New Game++ the identity must stay: **the two-phase Hashmal→Ultima finale with the mid-fight restore,
Dispelja + Almagest, the Ultima-Demon surround, and the low-HP transformation — the climactic, fair-but-
grand capstone of the no-resupply run.** Ultima stands at **Level 106 — the single highest level in the
mod.** And as the capstone, the final reward is **Ragnarok**, the legendary blade — earned for ending the
cycle and carried into the next **New Game++** loop.

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm BOTH phases: Phase 1 Hashmal (+ demon support); INTERPHASE full HP/MP restore; Phase 2 Ultima
  (+ Ultima Demons) with the low-HP SECOND FORM transformation. NO outfitter (gauntlet 5/5).
Confirm win sequence: defeat Hashmal → restore → defeat Ultima (second form) → campaign victory.
Keep Hashmal's WIDE-AREA attacks; the full RESTORE between phases; Ultima's DISPELJA + ALMAGEST + the
  Ultima-Demon surround + the SECOND-FORM transformation. These ARE the finale.
Confirm whether the two phases are ONE ENTD entry with scripted transition, or two chained entries.
Set the highest levels in the mod here: ULTIMA L106 (second form 106), Hashmal L105, Ultima Demons 104.
Set Ragnarok as the CAPSTONE reward (see Boss rare loot) — on victory / steal off Ultima form 1.
```

Unit / job IDs (verify in-game — these are scripted bosses):

```text
Hashmal — Lucavi job id      (TBD - verify; wide-area attacks; cf. 050 Adrammelech, 049 Zalera)
Ultima form 1 — Lucavi job id (TBD - verify; Dispelja + Almagest)
Ultima form 2 — Lucavi job id (TBD - verify; the transformed stronger form)
Ultima Demon — demon caste id (TBD - verify; the surround; cf. 048/049/053)
```

## Job Escalation (Chapter 4 rule)

```text
CHANGE: this is the scripted CAPSTONE — the escalation is APEX LEVEL and the climactic kit, not a new
  generic job. Ultima sits at L106 (the mod's single highest), Hashmal L105, the Ultima-Demon surround
  L104. The two-phase structure + transformation + full-restore are preserved exactly.
WHY: the finale's challenge is endurance and adaptation across three stages — spread vs wide-area/Almagest,
  re-buff after Dispelja, answer the demon surround with the Ribbon, and burst each form. Bolting on
  generics would cheapen the Lucavi climax. The "increase the challenge" mandate is met by APEX levels and
  the second-form escalation, faithfully.
CONSTRAINTS (carried — the finale must be GRAND but FAIR, no hard-lock):
  ALMAGEST = % of MAX HP AoE — telegraphed (charge), does NOT do 100% (leaves units alive at low HP,
    healable); spaceable; the signature threat, NOT an unavoidable wipe.
  DISPELJA = strips buffs — a soft reset answered by RE-BUFFING; not a lock.
  ULTIMA-DEMON SURROUND = a positional ambush, NOT an instant collapse; answerable by Ribbon (status) +
    spacing + the full HP/MP you enter Phase 2 with.
  HASHMAL WIDE-AREA = AoE, spaceable; demon support race-able.
  SECOND-FORM TRANSFORMATION = telegraphed climax escalation; bigger spells, but each still telegraphed/
    answerable — no scripted unavoidable party-wipe.
WHAT IS NOT CHANGED: the two-phase Hashmal→Ultima structure, the mid-fight restore, Dispelja/Almagest, the
  demon surround, and the second-form transformation all remain. This is the canonical finale, sharpened.
```

## Sanctioned exceptions (carried precedents)

```text
ALMAGEST (% max-HP AoE) — telegraphed, sub-100% (survivable at low HP, healable), spaceable. The
  signature finale threat; NOT an unavoidable wipe.
DISPELJA (buff strip) — soft reset; answer = re-buff. Not a lock.
ULTIMA-DEMON SURROUND — positional ambush at Phase 2 start; answer = Ribbon (status, earned 053) +
  spacing + the full HP/MP restore you enter with. Not an instant collapse.
HASHMAL WIDE-AREA — AoE bruiser; spaceable (050 Adrammelech 2-phase Lucavi precedent).
SECOND-FORM TRANSFORMATION — telegraphed climax escalation; each spell still answerable (050 phase-2
  precedent). No scripted unavoidable wipe.
TWO-PHASE + FULL RESTORE — the canonical finale structure; preserved exactly (the one mercy of the run).
```

## Boss rare loot — TIER-S CAPSTONE

```text
ULTIMA → RAGNAROK (Tier-S CAPSTONE — the legendary holy sword; the best-of-best, held for the very end).
  Defeating Ultima's second form ENDS the campaign in victory, so Ragnarok is framed as the CAPSTONE
  REWARD: the legendary blade earned for clearing the finale, and — fitting "New Game++" — CARRIED INTO
  THE NEXT ++ CYCLE. For the skilled, it is ALSO a STEAL off Ultima's FIRST form (before she transforms),
  rewarding the steal discipline the whole mod taught (Save the Queen, Chaos Blade, etc. were all steal-
  bait). Make the steal possible in Phase 2 form 1; otherwise grant it as the guaranteed victory capstone.
  Hashmal and the Ultima Demons drop nothing rare (scripted Lucavi / untameable demons).
  EXCALIBUR stays with Orlandeau (the player's own holy blade) — never on Ultima. Ragnarok is the enemy
  capstone; Excalibur the ally one — the two legendary holy swords, kept distinct.
```

> Tier-S ledger (COMPLETE): Chaos Blade (Folmarv, 052) · Ribbon (Zalbaag, 053) · Escutcheon (Loffrey,
> 055) · Robe of Lords (Cletienne, 056) · Materia Blade (Lost Halidom relic, 057) · **Ragnarok (Ultima
> CAPSTONE, 058)**. Tier-A leftovers unused this chapter (Genji Shield/Helm, Diamond Armlet) — see 059.

## Proposed Composition (New Game++ Airship Graveyard v1)

Two phases; apex levels — the mod's highest. Ultima `106` (both forms); Hashmal `105`; Ultima Demons `104`.

### Phase 1 — Hashmal

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Hashmal (BOSS) | Lucavi | `105` | Wide-area attacks (spread); the first wall; defeat → full restore. |
| n | Demon support | Demon caste | `104` | Screen Hashmal; race-able (verify exact support in-game). |
| n | Demon support | Demon caste | `104` | Second demon body; pressure, not the objective. |

> On Hashmal's defeat: PARTY HP/MP FULLY RESTORED (scripted). Re-buff / reposition for Ultima.

### Phase 2 — Ultima (+ surround), then her second form

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Ultima (BOSS, form 1→2) | Final Lucavi | `106` | Dispelja + Almagest; transforms to a stronger 2nd form at low HP; the final kill. |
| n | Ultima Demon | Demon caste | `104` | Surrounds the party at Phase 2 start; answer with Ribbon + spacing. |
| n | Ultima Demon | Demon caste | `104` | Second surround body. |
| n | Ultima Demon | Demon caste | `104` | Third surround body (verify exact count in-game). |

Reasoning:

The faithful move is **the canonical two-phase finale at apex level, kept grand but fair**. **Hashmal
(`105`)** opens with wide-area pressure (spread) until he falls and the party is **fully restored** — the
run's one mercy and a chance to re-buff. **Ultima (`106`, the mod's highest level)** then **surrounds**
the party with Ultima Demons (`104`), **dispels** your buffs, and **Almagests** the team for % max HP —
all telegraphed, survivable, and answerable with the **Ribbon** (earned `053`) + spacing + re-buffing.
At low HP she **transforms** for the climactic second form. Every threat is telegraphed and sub-lethal by
design — no scripted unavoidable wipe — so the finale tests **adaptation and burst**, not luck. The
**Ragnarok** capstone is earned on victory and carried into the next New Game++ cycle.

## Builds (the Lucavi finale)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Hashmal (Lv 105) — Phase 1 BOSS

```text
Job: Lucavi (id TBD)   JobLevel: 8   Primary: WIDE-AREA attacks (spaceable AoE) + Lucavi melee
Reaction: Damage Split / Counter (id TBD)   Support: Defense Boost (id TBD)   Movement: Move +2 (id TBD)
A wide-area bruiser; spread to answer. Defeat → scripted full HP/MP restore.
```

Role: the first wall; the AoE-spacing test; gateway to Ultima.

### Ultima (Lv 106) — Phase 2 BOSS, form 1 → second form

```text
Job: Final Lucavi (id TBD)   JobLevel: 8   Primary: DISPELJA (buff strip) + ALMAGEST (% max-HP AoE,
  telegraphed, sub-100%) + holy/dark high magic
Reaction: Reflexes / Damage Split (id TBD)   Support: MA-boost (id TBD)   Movement: Move +2 / fly (id TBD)
Right hand: RAGNAROK (Tier-S CAPSTONE — steal off form 1; else guaranteed victory capstone, id TBD)
At LOW HP → TRANSFORMS to a stronger SECOND FORM (bigger spells, each still telegraphed/answerable).
The mod's highest-level unit (106). Grand but FAIR — no unavoidable wipe.
```

Role: the final boss; the adaptation-and-burst climax; the Ragnarok capstone.

### Ultima Demon x3 (Lv 104) — the surround

```text
Job: Ultima Demon / demon caste (id TBD)   JobLevel: 8   Ultima / self-destruct (telegraphed) + demon magic
Reaction: Reflexes (449)   Support: MA-boost (id TBD)   Movement: Move +2 (id TBD)
Surround the party at Phase 2 start; answer with RIBBON (status, 053) + spacing. Untameable.
Verify exact count in-game.
```

Role: the Phase 2 positional ambush; answerable, not an instant collapse.

## Positioning Plan

```text
The Airship Graveyard (buried ancient airship beneath Orbonne): a grand final arena.
PHASE 1: Hashmal forward/center with his demon support — open ground to SPREAD vs wide-area attacks.
INTERPHASE: full HP/MP restore — re-buff and reposition.
PHASE 2: Ultima center; the Ultima Demons SURROUND the party's start — so position to break the surround
  (spacing + Ribbon), weather Dispelja/Almagest, and burst Ultima through both forms.
Preserve: the two-phase structure, the mid-fight restore, the demon surround, the transformation, and the
  telegraphed-but-fair threat profile. Ragnarok is the capstone, carried into the next New Game++ cycle.
```

The final arena should say: "the last Lucavi waits in the dead heart of the ancient airship — outlast
Hashmal, break Ultima's circle, weather the end of the world she casts, and end it; the legendary blade
you take from her is yours to carry into the cycle to come."

## Implementation Checklist

- [ ] Identify Airship Graveyard `BattleId` / ENTD entry(ies) on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify BOTH phases (Hashmal + support; Ultima + Ultima Demons + second form).
- [ ] Confirm the win sequence + the scripted full HP/MP restore between phases + the low-HP transformation.
- [ ] Keep Hashmal wide-area (spaceable); Ultima Dispelja (re-buff answer) + Almagest (telegraphed, sub-100%,
      survivable); demon surround answerable (Ribbon + spacing); second form telegraphed — NO unavoidable wipe.
- [ ] Set apex levels: Ultima `106` (both forms — the mod's HIGHEST), Hashmal `105`, Ultima Demons `104`.
- [ ] Set Ragnarok as the CAPSTONE: steal off Ultima form 1, else guaranteed victory reward; carries into NG++.
- [ ] Keep Excalibur with Orlandeau (ally) — never on Ultima.
- [ ] Patch via the correct layer (mind the two-phase scripting); keep the diff inside the finale window only.
- [ ] Re-dump and diff; confirm small, intentional changes; verify both phases + transformation + Ragnarok.
- [ ] Install mod, test from a New Game+ save; confirm it plays as a GRAND but FAIR two-phase finale —
      every threat telegraphed/answerable, the restore lands, both Ultima forms beatable, Ragnarok awarded.

## Test Questions

- Does it preserve the canonical two-phase finale (Hashmal → full restore → Ultima → second form) and end
  the campaign on the second form's defeat?
- Is every threat GRAND but FAIR — Almagest telegraphed/sub-100%/survivable, Dispelja answered by re-buff,
  the demon surround broken by Ribbon + spacing, the second form telegraphed — with NO unavoidable wipe?
- Is Ultima the mod's highest-level unit (106), and is the finale a clear climax over the gauntlet's prior fights?
- Is the Ragnarok capstone earned on victory (and/or stealable off form 1), carried into the next NG++ cycle,
  with Excalibur kept on Orlandeau?
- Is it winnable on ONE loadout as the 5th of five no-resupply fights, using the Tier-S gear assembled across
  the gauntlet?
- Does it read as the climactic Lucavi finale in the dead airship, the fitting end of the whole mod?

## Sources

- Game8, "Airship Graveyard Walkthrough (Battle 53 — Final Battle)": two phases (Defeat Hashmal → full
  HP/MP restore → Defeat Ultima), Ultima Dispelja + Almagest (% max HP), the low-HP second-form
  transformation, Ultima-Demon surround, Hashmal wide-area attacks, rec 60+, 4/5 stars, deploy 5.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553229
- Final Fantasy Wiki, "Ultima (Final Fantasy Tactics)" / "Hashmal": the final Lucavi and his lieutenant.
  https://finalfantasy.fandom.com/wiki/Ultima_(Final_Fantasy_Tactics)
- Local: `037-chapter-4-overview.md` (gauntlet + Tier-S tiering; Ultima L106), `050-eagrose-castle.md`
  (Adrammelech 2-phase Lucavi precedent), `049-limberry-undercroft.md` (Zalera Lucavi), `053-mullonde-
  sanctuary.md` (Ribbon — the status answer for the demon surround), `059-chapter-4-balance-review.md`
  (the chapter wrap-up — to be written).
```
