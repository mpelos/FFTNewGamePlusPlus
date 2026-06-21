# Endgame gauntlet (battles 49–53) — BLOCKED on in-game entry IDs

Status as of this pass: **Chapter 4 battles 33–48 are implemented & committed (16 of 21).**
The final five — the endgame gauntlet — could **not** be mapped to ENTD entries offline and were
**not patched** (guessing would risk corrupting the campaign's finale).

| Battle | Doc | Boss / Tier-S reward | Blocker |
|--------|-----|----------------------|---------|
| 49 Vaults 4th        | 054 | none (generic skirmish)         | no entry matches "3 Knight + 2 Monk + 1 Archer" |
| 50 Vaults 5th        | 055 | Loffrey → Robe of Lords         | Loffrey (job 37) appears ONLY at the Nave (461) |
| 51 Necrohol          | 056 | Cletienne → Materia Blade       | Cletienne (job 39) appears ONLY at the Nave (461) |
| 52 Lost Halidom      | 057 | relic → Escutcheon (+ Barich)   | Barich (job 43) appears ONLY at Bed Desert (447) |
| 53 Airship Graveyard | 058 | Ultima → Ragnarok (capstone)    | scripted 2-phase Hashmal→Ultima; high-risk, unconfirmed |

## What was found offline (entd4)

- **Confirmed story battles end at entry 462** (Mullonde Sanctuary). Every confirmed story battle
  (442–462) has at least the boss with an **explicit level + real equipment**.
- **Entries 463–469**: lvl254-placeholder-heavy with recurring guests **name31 / name72** →
  look **procedural / Deep Dungeon (Midlight's Deep)**, not designed story rosters. Docs' generic
  rosters match nothing here.
- **Entry 470**: all-Lucavi assembly (jobs/names 60 Velius, 62 Zalera, 64, 65, 67, 69 Adramelk, 73)
  + 7 Summoners — a "summon the Lucavi" set-piece, not the 2-boss finale.
- **Entry 471**: name20 (lvl 101, already wearing Ribbon 171 + Luminous Robe 206) + 4 Ultima Demons
  (job 154) + name49 ×2 + name65/73 (Lucavi) — designed-looking, but does not cleanly match the
  Hashmal→Ultima finale.
- **Entries 472–495**: uniform-job template/roster dumps (16× the same job) — not battles.

Conclusion: the death-battles for Loffrey / Cletienne / Barich and the Vaults skirmishes are **not
present as standard designed-roster ENTD entries** in the expected range. They are likely
**OverrideEntryData-driven or scripted**, or use entries that only the runtime can disambiguate.

## Exact next step (unblocks all five)

The mod's runtime logs `[battle-id]` (the global ENTD entry) on battle entry — the ground-truth
confirmation (see memory `fft-tic-entd-entry-id`). From a NG+ save, enter each of battles 49–53 and
record the printed `[battle-id]`. With those five entry numbers, each battle can be dumped, verified
against its doc, and patched with the same per-battle pipeline used for 33–48
(`tools/battle_patch.py` → `dotnet build`).

Tier-S items still to place once entries are known: Robe of Lords (207, Loffrey), Materia Blade
(32, Cletienne), Escutcheon (143, Lost Halidom relic), Ragnarok (36, Ultima capstone). Note any
Lucavi boss (Hashmal/Ultima) has **eq=255** (no equip slots), so its Tier-S reward must go through
the **map Move-Find reward layer** (same as Belias Defense Ring / Zalera Aegis Shield), not ENTD gear.
