# Endgame gauntlet (battles 49–53) — entry mapping resolved (in-game 2026-06-21)

**Update:** the blocker is fully dissolved. All six battle-entries were mapped by entering each
in-game and matching the **on-screen roster** to a vanilla entd4 dump (the offline-only guess had
failed). **All six are designed entd4 entries** — moddable with the existing entd4 swap. The earlier
"Vaults 4th = template 25 + OverrideEntryData" theory was DISPROVEN: Vaults 4th is just entry 435,
where Loffrey is a scripted cutscene-NPC who walks out the door (no fight), leaving the 6 generic
enemies as the real roster.

## Final map (authoritative — matched by on-screen roster, all implemented)

| Battle | Doc | Entry | File | Roster | Mod path |
|--------|-----|-------|------|--------|----------|
| 49 Vaults 4th        | 054 | **435** | entd4 | Loffrey (job37, cutscene-exits, NO fight) + 3 Knight/2 Monk/1 Archer | ENTD direct ✅ |
| 50 Vaults 5th        | 055 | **436** | entd4 | Loffrey (job37, FIGHTS & dies) + 2 Black Mage/2 Summoner/1 Time Mage | ENTD direct ✅ |
| 51 Necrohol – The Capitoline  | 056 | **438** | entd4 | Cletienne (job39) + 2 Samurai/2 Ninja/2 Time Mage | ENTD direct ✅ |
| 52 Necrohol – Lost Halidom    | 057 | **439** | entd4 | Barich (job43) + Chemist + 4 dragons (jobs 135/139/140/141) | ENTD direct ✅ |
| 53 Airship Graveyard – Phase 1 | 058 | **440** | entd4 | Folmarv (job36) → Hashmal + Celia/Lettie (job44) + Lucavi (job64) | ENTD direct ✅ (scripted) |
| 53 Airship Graveyard – Phase 2 | 058 | **441** | entd4 | Ultima (job20) + 4 Ultima Demon (job154) + Lucavi (49/65/73) | ENTD direct ✅ (scripted) |

## Key findings

- **`[battle-id]` LAGS — do not trust it.** The diagnostic reads `resume_en*_attack/fturn.sav`
  @0x16C, which holds the PREVIOUS battle's entry on first read. Every entry above was confirmed by
  the on-screen roster, not the printed number. To get a fresh read, ENTER THE BATTLE TWICE (the 2nd
  read is current). `resume_enwm_main.sav` @0x16C is TEXT (SHIFT-JIS), not the entry — a dead end.
- **Vaults 4th = entry 435 (NOT a template battle).** Loffrey appears in slot0 as a scripted
  cutscene NPC who animates in and exits through the door — he never fights. The real roster is
  slots 1–6 (3 Knight/2 Monk/1 Archer). Entry 436 (Vaults 5th) is the SAME Loffrey but scripted to
  fight and die, alongside the caster band. Neighboring entries differ by event script, not data.
- **No current gauntlet reward note:** Hashmal (440) / Ultima (441) have **eq=255** (no equip slots),
  but the current reward ledger does not place usable NG++ rewards inside `054`-`058`. Do not use the
  final gauntlet for Ragnarok, Materia Blade, or any other late reward payload.

## Current reward policy

- No usable NG++ reward is added inside `054`-`058`.
- `052` Mullonde Nave pays **Chaos Blade + Escutcheon + Lordly Robe** before the point of no return.
- `053` Mullonde Sanctuary pays **Ragnarok + Ribbon** before the final gauntlet.
- **Materia Blade** is outside the campaign-battle reward plan and must not be restored to `057`.
- Vaults 4th (435) generics keep no signature drop or boss reward.

## Status

1. ✅ Entry mapping is resolved for all six entd4 records (`435`/`436`/`438`/`439`/`440`/`441`).
2. ✅ The current design docs treat the final gauntlet as challenge content only: no usable rewards,
   no steal-dependent rares, and no late unique payloads inside `054`-`058`.
3. Historical Move-Find notes for Materia Blade/Ragnarok are superseded by
   `chapter-4-rewards-implementation.md` and must not be used as the current battle-design source.
