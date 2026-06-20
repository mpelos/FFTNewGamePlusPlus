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

---

## ⚠️ FLAG HUNT — value-scan approach struggling (2026-06-19, later)

The first "flag" `0x15873C642` (=6) was a FALSE POSITIVE: later read 0 in NG+ and 6 in a
normal save — its value floats. Root cause: that whole `0x15873Cxxx` block is in a region CE
labels as module (AllocationBase 0x140000000) but is **RWX and volatile** — likely a managed/
reallocated heap mapped near the module, NOT clean static `.bss`.

Redid the hunt with MATCHED-PROGRESS saves (new Normal save made at the same point as the NG+
save: "1 Aries, defeat the band of thieves fled to Gariland") + a reload→Unchanged filter to
kill volatile memory. Mode check discovered: **world-map Ramza sprite = BLUE in Normal, RED in
NG+** (reliable visual mode indicator). Funnel reached 29 candidates, but the next
NG+→Normal "Changed" returned 0 — and the user independently re-ran the whole alternating
recipe 3× and hit 0 every time.

User also noted a near-miss `0x15873C4D7` = 121 (NG+) / 123 (Normal) — REJECTED (same volatile
block; values aren't a clean 0/nonzero flag).

### Conclusion / hypothesis
The NG+ state almost certainly lives in memory that is **re-allocated on every save load**, so a
fixed-address value scan keeps contradicting itself → converges to 0. Flat value scanning is the
wrong tool here.

### Next strategies to try (in order)
1. **Pointer scan** in CE: find a stable pointer chain (module-static base → … → flag) so the
   address survives reallocation/restart. Verify the chain across a game restart.
2. **Confirm region type first**: only trust a candidate if its address is in TRUE static memory
   (low module offset, RW not RWX) AND survives a game restart. Don't trust anything in 0x15873Cxxx.
3. **Alternative detection** if no static flag exists:
   - Read NG+ status from the SAVE on load (hook save-load, read NG+ field), or
   - Use the per-battle **EventId** (NG+ Gariland=237 vs normal=9) at battle setup — hunt the
     EventId in memory during an actual battle (exact-value scan for 237 vs 9), then hook there.

---

## ❌ NO PERSISTENT NG+ FLAG IN RAM (2026-06-19, conclusion)

After a rigorous redo (matched-progress saves: a fresh Normal save made at the SAME point as an
NG+ save — both "1 Aries / defeat the thieves fled to Gariland"; Ramza sprite color = mode check:
BLUE=normal, RED=NG+), plus the anti-volatile technique (reload-same-save → "Unchanged" to drop
reallocating memory), ~10 attempts found **no stable byte that tracks NG+ vs normal**.

- The earlier `0x1873C642` candidate was a FALSE POSITIVE: its value (6) drifted to 0 even within
  NG+ and read 6 in a normal save on a later load → it lived in a reallocating/volatile region
  (RWX, CE-labeled module but dynamic).
- Root cause / user's insight: **the game makes no NG+ vs normal distinction during play**, so it
  keeps no queryable "is NG+" global. NG+ ("Continuous") is just a carry-over START condition.

### Implication
Runtime gating via a memory flag is NOT viable (nothing reliable to read at world map / battle
time). Any remaining distinction would be at the event/save-load routing level (e.g. Continuous
timeline vs normal), which is NOT findable by value scanning — it would need code-level RE (Ghidra:
find the save-load routine that picks Continuous vs normal flow / the EventId dispatch). Big effort,
uncertain payoff.

### Practical path forward (recommended)
**Manual toggle:** ship as a data mod; player enables "New Game++" in Reloaded-II only when playing
NG+, disables for a first playthrough. Zero code, ships now, standard for "harder NG+" mods.
Optional cheap check first: diff a normal vs NG+ SAVE FILE on disk to see if NG+ is even marked
there (would tell us whether a save-load hook is theoretically possible).

### Confirmed negative with the rigorous method (2026-06-19, follow-up)
Ran the full anti-volatile matched-pair method end to end (I drove CE; user swapped saves):
snapshot on matched-Normal (1 Aries) → reload-same Normal "Unchanged" (anti-volatile) → matched-NG+
"Changed" (40) → reload-same NG+ "Unchanged" (29) → matched-Normal "Changed" = **0**.
Then the definitive live test: put all 29 survivors in the address list and toggled Normal↔NG+ —
all 29 read IDENTICAL values in both modes (e.g. 129,45,7,119,170,3,73,72,57). None tracks mode.
=> Definitively: no statically-addressable memory value distinguishes NG+ from normal. CONCLUSION
STANDS: automatic runtime gating is not possible via value scanning. Go with the manual toggle.

---

## 🔄 USER'S IDEA: detect NG+ at save-load, set our OWN flag (2026-06-19)

Since the game keeps no runtime NG+ flag, fabricate one: detect NG+ when a save is read, set a
flag we control, read it in the ENTD hook.

### Save format findings (.psol)
- `fft_enhanced_b96bc3fb.psol` in `%LOCALAPPDATA%\SquareEnix\FINAL FANTASY TACTICS - The Ivalice Chronicles\`.
  ONE file holds ALL slots. Magic `PSOL`, version `02 00 00 03`, size field at +0x10, count(9?) at +0x38.
- It's a key-value DB: keys = 64-bit field-name HASHES rendered as 16-hex UTF-16 (entries start
  ~0x2D18, stride 0x22). Index region (first ~0x30000) low-entropy/readable; value bodies high-entropy
  (encrypted+hash-checked). Locked while game runs (close game to read). Copy: work/save_copy.psol.
- FFXVI (same engine) save research (Nenkai): saves are "binary, no steam id check, encrypted & hash
  checked." Engine has **SerializeSave / DeserializeSave with an `asXml` bool** → dumps NAMED fields as
  XML. FFXVI sigs (ffxvi.exe 1.0.1): SerializeSave=sub_140796D58, DeserializeSave=sub_140796C94.
  FF16Tools can unpack/pack + fix checksum (FFXVI .png saves; .psol/FFT not officially supported).

### Concrete plan (de-risked by FFXVI research)
1. Find FFT's SerializeSave/DeserializeSave signatures in fft_enhanced.exe (analogous to FFXVI; Ghidra).
2. Use the `asXml` path to dump an NG+ save as XML → read field names → identify the NG+/Continuous
   field + its value (THE de-hash shortcut).
3. Code mod: hook DeserializeSave → read NG+ field at load → set our own flag.
4. Hook the ENTD file read (build on modloader's FFTPackHooks/ResourceManagerHooks) → serve modded
   ENTD if flag set, else vanilla. (Battle ENTD is read after a save is loaded, so flag is ready.)

### Status / recommendation
Path is OPEN and well-scoped, but it's a real code-mod project (Ghidra RE of save sigs + 2 hooks).
Recommend: ship **manual toggle as v1** (usable now), pursue this **save-hook auto-detection as v2**.

---

## ✅✅ NG+ DETECTABLE FROM THE SAVE FILE (2026-06-19) — user's idea WORKS

Offline-decoded the real saves and found a rock-solid NG+ flag. This proves the "detect NG+ at
save-load, set our own flag" approach is viable.

### Save files (real ones; NOT the .psol, which is config)
- `%USERPROFILE%\OneDrive\Documentos\My Games\FINAL FANTASY TACTICS - The Ivalice Chronicles\Steam\<id>\`
  - `enhanced.png`     = manual slots (inner file `fftsave.bin`, ~2 MB decompressed, all slots)
  - `autoenhanced.png` = autosave / live current-game state (many `resume_*.sav` inner files)
- Format = Faith/FF16 engine save: PNG -> `ffTo` chunk -> UMIF TOC -> per inner-file XOR + zlib.
  - XOR key `0x0F3F80FE5F1FC4F3`; zlib uses a 0x8000 preset dict (Nenkai/FF16Tools CompressDict.cs).
  - Fully reproduced offline in Python: `tools/fft_save_decode.py` (decode_png + manual_slots + is_ngplus).

### THE NG+ FLAG
In `fftsave.bin`, per manual slot (slots aligned so the `Arthur` roster marker is at slot+0x85C,
slot stride 0x9CE4): **byte at slot offset `0x08AFB` == 1 for New Game+, 0 for normal.**
(0x08CA7 / 0x08DFB / 0x0972C are identical alternates.) Found via a 2-vs-4 partition across the
user's 6 saves (4 normal at different story points + 2 NG+): the {NG+ slots} group had 169 mode-
constant offsets; these four are the clean 1/0 ones. Validated 100% across all 6 slots (user
confirmed slot5=NG+ matched, slot4=normal matched).

### Runtime delivery (next design step)
Plan: code mod reads the **autosave** (autoenhanced.png, = current game) on disk, decodes it, reads
the NG+ flag -> sets our own flag -> ENTD hook serves modded/vanilla. NEED: locate the NG+ flag
offset in the autosave's `resume_*` format (different layout/size than manual `fftsave.bin`).
=> Controlled capture: load NG+, play briefly to force an autosave, close, decode autoenhanced.png,
diff vs a normal autosave to find the flag offset there. (Current autosave reads 0 = likely a stale
normal-game state from making the matched-normal save.)

### Strengthened: validated across all 7 used slots (2026-06-19)
Re-enumerated slots by FIXED stride 0x9CE4 (not by the 'Arthur' marker, which is absent in saves
where Argath/Arthur has left the party). fftsave.bin has 7 USED slots (indices 0-6; rest of the
~50 stride positions are empty). User inventory = 3 NG+ + 3 cleared + 1 early-normal.
Result: byte `0x08AFB` == 1 for slots {0,5,6} (the 3 NG+) and == 0 for {1,2,3,4} (the 4 normal).
Slot 5 is an NG+ save WITHOUT an Arthur marker -> flag is independent of roster/progress. CONFIRMED.
Refinement: `0x08AFB` and `0x0972C` are the robust flags; `0x08CA7`/`0x08DFB` were false alternates
(0 in slot 5's NG+). Use **0x08AFB**.

---

## Runtime architecture finalized (2026-06-19): file-read hook, NOT DeserializeSave

- Static RE of the engine save funcs is impractical: fft_enhanced.exe is OBFUSCATED (Denuvo-style;
  sections named .xcode/.edata, .edata ~350MB). XOR key constant lives at file 0x31749EC (.edata);
  UMIF/fftsave/resume_en/NewGame/Continuous strings present, but clean static disasm of DeserializeSave
  is hard. So DON'T hook the game function.
- Instead: hook **ReadFile (kernel32)** — when the game reads a save to load, decode bytes with our
  decoder and read the NG+ flag, set our own flag. Denuvo-proof; modloader already does API hooks
  (CreateProcessA). Then the ENTD file hook serves modded/vanilla per the flag.

### NG+ flag offsets (final)
- Manual save `fftsave.bin`, per slot: **0x08AFB** (and 0x0972C). 1=NG+, 0=normal.
- Autosave resume `*_main`/`*_world` format = manual format + a 0x154 header => flag at **0x8C4F**.
  (Confirmed: resume_en02_main.sav matched the manual flag's 33-byte context exactly, flag=1.)
- Caveat: the autosave has many resume_* files; only the current-context ones hold the live value
  (staleness). Hooking the READ at load time avoids picking the wrong stale file.

### Open runtime questions (for the C# code mod)
1. Does the game read saves via plain ReadFile, or its own IO layer? (modloader ResourceManagerHooks
   suggests a custom layer — may need to hook there instead, reusing modloader's sig approach.)
2. Manual-slot load: the read returns all slots (fftsave.bin) — need the chosen slot index, OR rely on
   the post-load autosave write. Continue/NG+ play loads the autosave (single current game) = clean.

---

## ✅ COMPLETE BUILD PLAN (2026-06-19) — Denuvo-free, reuses modloader's published sigs

The Nenkai modloader is open-source and already locates these functions by signature. We reuse the
SAME signatures (no Ghidra / Denuvo RE needed by us).

### Hook B — conditional ENTD (the application side)
Hook the fftpack reader `fileReadRequestOffset(int fileIndex, long sectorOffset, long size, void* out)`.
- Sig (from FFTPackHooks.cs): `48 89 5C 24 ?? 48 89 6C 24 ?? 48 89 74 24 ?? 57 48 83 EC ?? 80 3D ?? ?? ?? ?? ?? 4C 89 CE`
- byteOffset = sectorOffset * 0x800.
- ENTD fileIndexes (fftpack.txt): 224=battle_entd1_ent.bin, 225=entd2, 226=entd3, **227=entd4**.
- Impl: if fileIndex in 224..227 AND our NG+ flag set -> memcpy our modded ENTD[byteOffset..+size]
  into `out`, return 0 (handled). Else call OriginalFunction (vanilla / or modloader's modpack).

### Hook A — NG+ detection
Hook `faith::Resource::ResourceManager::OpenFileAndCache(void* a1, FileResult* a2)`.
- Sig (from ResourceManagerHooks.cs): `48 8B C4 48 89 58 ?? 48 89 68 ?? 48 89 70 ?? 48 89 78 ?? 41 56 48 83 EC ?? 33 ED 48 8B F2`
- FileResult->PathPtr = filename. When a save (enhanced.png / autoenhanced.png) is opened, read+decode
  it with our decoder, read NG+ flag, cache it. (Or simpler: re-read autosave on demand in Hook B.)
- Flag offsets: manual fftsave.bin slot+0x08AFB ; autosave resume main/world slot+0x8C4F. 1=NG+,0=normal.

### Decoder port to C#
Port tools/fft_save_decode.py: PNG 'ffTo' chunk -> UMIF TOC -> per-file XOR(0x0F3F80FE5F1FC4F3) +
zlib inflate with 0x8000 preset dict (CompressDict). C# has System.IO.Compression / can ship the dict.

### Remaining build tasks
1. Install .NET SDK 8 (to compile the Reloaded C# mod DLL). [needs user]
2. Scaffold Reloaded mod project (ModConfig ModDll, deps already present).
3. Implement Hook A + Hook B + the decoder; embed our modded ENTD as a mod resource.
4. Build, deploy, test in NG+ vs normal.
