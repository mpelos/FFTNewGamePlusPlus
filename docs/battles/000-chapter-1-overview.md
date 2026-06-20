# Chapter 1 — "The Meager": New Game++ Design Overview

This is the master plan for rescaling and redesigning every **Chapter 1** story battle of
*FINAL FANTASY TACTICS - The Ivalice Chronicles* (Enhanced v1.5.0) for New Game++.

Each battle gets its own design doc. This file holds the shared philosophy, the battle list,
the per-battle status table, and the design rules that keep every fight consistent.

## Naming note (Ivalice Chronicles / WotL retranslation)

The remaster uses the War of the Lions retranslation. Classic PSX names map as:

```text
Sweegy Woods      -> Siedge Weald
Dorter Trade City -> Dorter Slums
Sand Rat Cellar   -> Sand Rat Sietch
Death Corps       -> Corpse Brigade
Algus             -> Argath
Fort Zeakden      -> Ziekden Fortress
```

## Chapter 1 battle list

"Battle N" follows the in-game/Game8 numbering. Doc numbers are our own design order.

| Doc | Battle | Location | Role in story | Design status |
|-----|--------|----------|---------------|---------------|
| (skip) | 1 | Orbonne Monastery | Scripted tutorial | Out of scope — see below |
| `001` | 2 | Magick City of Gariland | First real fight; city street brawl | ✅ Implemented (final-shop v1) |
| `002` | 3 | Mandalia Plain | First monster + escort a reckless guest | 📝 Designed |
| `003` | 4 | Siedge Weald (Sweegy Woods) | Monster-pack woodland; Bombs | 📝 Designed |
| `004` | 5 | Dorter Slums | First difficulty spike; rooftop ranged+magic | 📝 Designed |
| `005` | 6 | Sand Rat Sietch | Cramped corridors; split-team melee attrition | 📝 Designed |
| `006` | 7 | Brigands' Den | Milleuda boss; rainy thieves + healers | 📝 Designed |
| `007` | 8 | Lenalian Plateau | Milleuda falls; mage-heavy field + Time Mage | 📝 Designed |
| `008` | 9 | Fovoham Windflats | Wiegraf duel; Judgment Blade spike | 📝 Designed |
| `009` | 10 | Ziekden Fortress | Chapter finale; Argath boss + hostage | 📝 Designed |
| `010` | — | Chapter 1 Balance Review | Cross-battle curve + consistency audit | ✅ Done (all 10) |

**Battle count corrected:** Chapter 1 "The Meager" has **10 story battles**, not 7. The
Milleuda/Wiegraf (Corpse Brigade leaders) arc — Brigands' Den, Lenalian Plateau, Fovoham
Windflats — sits between Sand Rat (Battle 6) and the Ziekden finale (Battle 10). These three
were added in a backfill pass; Ziekden and the balance review were renumbered to `009`/`010`
to keep the docs in story order.

**Design status:** COMPLETE — `001` implemented and tested; `002`–`009` designed on paper.
The cross-battle audit (`010-chapter-1-balance-review.md`) covers all 10 battles. Remaining
work: identify each `BattleId`/ENTD entry on the Windows game files, patch, and playtest in
story order (see the review doc for the order and risks).

**Chapter boundary:** Chapter 1 "The Meager" ends at Ziekden Fortress (Battle 10), after which
Delita leaves the party. The next playable battle (Merchant City of Dorter, Battle 11) opens
Chapter 2 "The Manipulator and the Subservient" — covered in a separate Chapter 2 overview.

### Why Orbonne (Battle 1) is skipped

Battle 1 is the opening tutorial: a fixed, scripted teaching fight with forced moves and a
guaranteed outcome. It has no New Game+ replay value and scaling it would fight the tutorial
scripting. We leave it stock. If desired later, it can be revisited as an optional "tutorial
hard mode," but it is intentionally not part of the Chapter 1 rescale pass.

## Core scaling mechanic (recap)

Proven on Gariland. The enemy `Level` field uses the classic ENTD encoding:

```text
1-99 = fixed level
100  = party's highest level + 0
101  = party's highest level + 1   (etc.)
```

In TIC, the moddable layer is the NXD table **`OverrideEntryData`** (keyed by
`BattleId, UnitSlot`); it patches the base `battle_entd*_ent.bin` only for fields that are
set. Gariland was done directly in the `.bin` because its override rows left `Level=-1`.
For each new battle, confirm whether to patch via the `.bin` or via `OverrideEntryData`
once the BattleId and override rows are dumped on the Windows game data.

> ⚠️ Every new battle doc lists its **enemy data (BattleId / ENTD entry / slot offsets) as
> TBD** until dumped from the real game files on the Windows machine. These docs are the
> *design layer*; the byte-level patch is applied on the machine that has `extracted/`.

## Design philosophy

The mod's promise: **"story battles scale now."** Endgame New Game+ characters should no
longer trivialize Chapter 1. But Chapter 1 is the game's on-ramp, so the curve must rise
gently and each fight must still *feel like itself*.

### The five rules

1. **Preserve the battle's identity.** Keep the original's theme, enemy archetypes, terrain
   pressure, and "what this fight teaches." Gariland stays a street brawl; Dorter stays a
   rooftop-ranged wall; Siedge Weald stays a monster pack. We re-skin and re-tune, we do not
   replace the fantasy.

2. **Scale, don't escalate to boss tier.** Non-boss enemies sit at level `100` to `102`
   (party + 0..2). Leaders/uniques may go `+3`. Nothing in Chapter 1 should out-level the
   party by more than a few points.

3. **Final-shop gear, never superboss loot.** Enemies scale to an endgame party, so paper
   gear makes them irrelevant. Use strong gear that exists in shops or the loader's shop
   table. Forbidden: Genji set, Chaos Blade, Excalibur, Ragnarok, Save the Queen, and other
   unique steal/treasure rewards. Gear *flavor* follows the faction (academy cadets vs.
   Corpse Brigade deserters vs. monsters).

4. **Respect job equipment rules.** Generic enemy Squires don't wear shields/heavy armor;
   monsters wear nothing; mages use robes/rods. Builds must be legal for the job or they
   silently break.

5. **Keep the difficulty curve readable.** A returning player should feel the chapter ramp:
   Gariland (warm-up) < Mandalia (escort + first beast) < Siedge Weald (monster swarm) <
   Dorter (the wall) ≈ Sand Rat (attrition) < Brigands' Den (first named boss) <
   Lenalian (mage-heavy boss rematch) < Fovoham (Wiegraf spike) < Ziekden (finale). Add at
   most one new meaningful threat per fight; never bury the player in status/burst this early.

### Difficulty budget per battle

| Battle | Target feel | Level band | Allowed new threat |
|--------|-------------|------------|--------------------|
| Gariland | Warm-up, fast | 100–102 | one ranged unit |
| Mandalia | Escort tension | 100–102 | ranged pressure on the guest + keep the beast |
| Siedge Weald | Swarm management | 100–101 | extra monster, Bomb self-destruct threat |
| Dorter | The spike / the wall | 100–102 | real elevation + ranged + one mage |
| Sand Rat | Grind / corridor attrition | 100–102 | mixed melee+caster behind a chokepoint |
| Brigands' Den | First named boss; healers prolong | boss +2, adds 100–101 | Milleuda as a boss; White-Mage sustain; rain (Thunder) |
| Lenalian | Boss rematch, mage-heavy | boss +2, adds 100–102 | stacked Black Mages + first Time Mage (Haste/Slow) |
| Fovoham | Wiegraf spike | boss +3, adds 100–102 | Wiegraf's Judgment Blade + hard-hitting Monks |
| Ziekden | Climactic boss fight | boss +3, adds 100–102 | Argath as a genuine boss; protect the hostage beat |

### Things to avoid chapter-wide

```text
Black Mage burst stacking before Dorter
Time Mage control (Stop/Don't Move) anywhere in Chapter 1
Heavy status spam (Petrify, Charm, Death) on generics
More than one true caster per fight before Dorter
Boss-tier level offsets on generic units
Unique/superboss equipment
```

## Workflow for each battle (design -> implement)

1. Read this overview + the battle's own doc.
2. On the Windows machine, identify the battle's `BattleId` / ENTD entry (cross-reference
   `SortieConfirm`, `EventId`, `Map`, scenario tables; sanity-check with FFTIvaliceEditor).
3. Dump the entry with `tools/entd_tool.py` (or the `OverrideEntryData` rows) and confirm
   the original slot layout matches the doc's "Original Battle" section.
4. Apply the doc's New Game++ composition: levels, jobs, gear, skills, placement.
5. Patch via the appropriate layer (`.bin` or `OverrideEntryData`), keeping the diff minimal
   and inside the target battle's window.
6. Copy into the mod, install to Reloaded-II, test from a New Game+ save.
7. Record results and tuning notes back in the battle doc.

## Sources

- Game8, "Chapter 1: The Meager Walkthrough":
  https://game8.co/games/Final-Fantasy-Tactics/archives/543067
- StrategyWiki, FFT Chapter 1 battle pages:
  https://strategywiki.org/wiki/Final_Fantasy_Tactics
- Caves of Narshe FFT battle walkthrough (per-battle rosters):
  https://www.cavesofnarshe.com/fft/walkthrough.php
- FFHacktics ENTD reference: https://ffhacktics.com/wiki/ENTD
- Local: `docs/battles/001-gariland.md`, `notes/01-encounter-data-and-gariland.md`
</content>
</invoke>
