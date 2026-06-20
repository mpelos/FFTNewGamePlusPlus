# Conditioning battle changes to New Game+ only

Date: 2026-06-19

## The requirement
Battle changes (enemy scaling/composition + guest scaling) must apply ONLY in New Game+,
leaving a normal first playthrough 100% vanilla.

## Core finding: NG+ shares the encounter data with normal play
Investigated the NG+ ("Continuous") data path in `enhanced_0004.sqlite`:
- `ContinuousBattleTimeline` (46 rows) = only map/camera marker names (MapA, Point01, Move01,
  Stay01...). NOT battle/encounter data.
- `ContinuousSortieConfirm` (27 rows) = only NG+ rewards/UI params (gil, exp, UI ids). No
  separate ENTD/encounter reference.
- NG+ Gariland = EventId 237 (`ContinuousSortieConfirm:4`); it has **0** EnhancedBattleEvent
  opcodes → reuses the normal battle setup (EventId 9, `SortieConfirm:4`).
- There is **no** `ContinuousEntryData` / NG+ encounter / NG+ override table. Only `EntryNo`
  (512 ENTD entries) and one `OverrideEntryData` layer exist, shared by all play.
- Community confirms NG+ has the same battles / no difficulty upscaling.

=> **NG+ uses the SAME ENTD entries (e.g. 388/392) as the first playthrough.** Our
file-replacement mod therefore affects BOTH. Pure data editing cannot condition on NG+.

**CONFIRMED by user (2026-06-19):** started a fresh non-NG+ game; the characters scaled there
too -> the file-replacement changes DO leak into the first playthrough. Code mod required.
Decision: build the code mod. Also applies to composition changes (same requirement).

## The best way: a runtime code mod (Reloaded-II C# DLL)
Because the NG+/normal distinction is only a runtime game state, the only correct solution is
a code mod that:
1. **Detects NG+ state** — reads the in-memory flag the game sets for a "Continuous" game
   (e.g. a global GameMode/isContinuous boolean set on save load).
2. **Hooks encounter loading** — the function that loads `battle_entd*_ent.bin` / applies
   `OverrideEntryData` / finalizes encounter units.
3. **Applies our modded battle data only when NG+ is active**, otherwise passes the original
   data through.

The toolchain already supports this: the modloader (`fftivc.utility.modloader`) is itself a
Reloaded-II code mod and depends on `Reloaded.Memory.SigScan.ReloadedII` + Reloaded hooks.

### RE work needed
- Find the NG+ flag: diff memory between a normal save and a Continuous save (Cheat Engine),
  or sigscan the routine that reads `ContinuousSortieConfirm`.
- Find the encounter-load hook point.
- Write the C# mod (or extend the modloader) to conditionally overlay our ENTD bytes.

## Alternatives (with tradeoffs)
- **Relative levels only** (set levels to 100+, no composition change): auto-scales to party in
  BOTH playthroughs, so a first playthrough stays roughly vanilla in difficulty — BUT any
  composition/job changes still leak into the first playthrough. Fails the "untouched" goal if
  we change compositions.
- **Manual toggle**: keep it a pure data mod, and the player enables "New Game++" in Reloaded-II
  only when playing NG+, disables for a first playthrough. Zero code, but manual and
  unprotected against accidents. Acceptable as a stopgap since the mod is NG+-purposed.
- **Redirect NG+ battles to new ENTD entries**: would require changing the NG+ event path to
  point at new (unused) ENTD entries holding our battles. Needs decoding the external
  event->ENTD link (event_btlevt_bin.bin) — likely harder than the code-mod hook.

## Recommended path
1. (Cheap, decisive) Verify shared-vs-separate with ONE fresh (non-NG+) game test at Gariland.
   Expected: it IS modded (shared) — confirming we need the code mod. (~95% confident already.)
2. Build the code mod: locate the NG+ flag + encounter-load hook, then conditionally apply.

---

## ✅ NG+ FLAG FOUND (2026-06-19, Cheat Engine session)

**Flag = `fft_enhanced.exe + 0x1873C642` (1 byte). `0` = normal play, `6` (nonzero) = New Game+.**

### How it was found
- Method: CE "Unknown initial value" (Byte) snapshot on an NG+ save, then alternating
  scans across all 5 saves (3 normal + 2 NG+): Changed across mode, Unchanged within mode.
- Funnel: 132,468,736 → 200 (changed NG+→Normal1) → 79 (unchanged N1↔N2) → 71 (↔N3)
  → 4 (changed Normal3→NG+) → isolated 1 by live observation.
- Survivors examined live: only `0x15873C642` (this session's absolute addr) read **6 in BOTH
  NG+ saves and 0 in normal saves**. The other 3 were erratic / didn't actually change.

### Why it's static (module-relative)
- CE Memory Viewer region info: `AllocationBase=140000000 Module=FFT_enhanced.exe` for the page.
- Module base = `0x140000000`; absolute `0x15873C642` − base = **offset `0x1873C642`**.
- Exe on disk = 365,841,152 bytes = `0x15CE4B00` (~349 MB). Offset `0x1873C642` (~408 MB) sits
  just past raw file size → consistent with a `.bss` global (virtual size > raw size).
  `.bss` zero-init explains 0=normal default; set to 6 for NG+.

### Semantics note
- Value observed = **6** in NG+ (both saves), **0** in normal (all 3). Likely an NG+ marker or
  cycle counter. Code mod should test **`flag != 0`** (NOT `== 6`) so it works for any NG+ cycle.

### Still TODO for the code mod
1. Validate across a GAME RESTART: confirm `moduleBase + 0x1873C642` still reads 6(NG+)/0(normal)
   after relaunch (proves ASLR-robust module+offset, not a one-session fluke).
2. Find the ENTD-load / battle-setup hook point. Promising path: CE "Find out what ACCESSES this
   address" (F5) on the flag, then enter a battle in NG+ — the code that reads the flag at battle
   setup is our hook candidate AND yields a byte-signature for the code mod (update-robust).
3. Consider sig-scanning the flag's accessor instead of a hardcoded offset (survives game patches).
