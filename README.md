# FFT: The Ivalice Chronicles - New Game++

Battle rebalance mod for **FINAL FANTASY TACTICS - The Ivalice Chronicles** on Steam/PC,
targeting the **Enhanced** version on game patch **v1.5.0**.

Patch 1.5.0 added New Game+, but story battles keep their original low fixed levels. This
project changes story encounters one by one so enemies scale with the player's highest
character level and each fight can be redesigned with new jobs, gear, skills, unit counts,
and placement.

The visible Reloaded-II mod name is:

```text
New Game++
```

The internal mod id is:

```text
fftivc.battles.rescale
```

## Confirmed Result

The key mechanic is now proven in-game.

Classic FFT ENTD uses a special level encoding:

```text
1-99  = fixed level
100   = party highest level + 0
101   = party highest level + 1
105   = party highest level + 5
```

We tested this in **Ivalice Chronicles Enhanced v1.5.0** on the first Chapter 1 battle,
**Magick City of Gariland**. Changing the five enemy level bytes from `1` to `100` made the
enemies scale in New Game+ instead of remaining level 1.

So the core mod strategy is valid:

```text
For each story battle, find its ENTD entry, identify enemy slots, set enemy Level to 100 + offset.
```

## Local Paths

Game install:

```text
D:\SteamLibrary\steamapps\common\FINAL FANTASY TACTICS - The Ivalice Chronicles
```

Target executable:

```text
D:\SteamLibrary\steamapps\common\FINAL FANTASY TACTICS - The Ivalice Chronicles\FFT_enhanced.exe
```

Project:

```text
D:\Projects\FFTModNewGame++
```

Reloaded-II mods directory on this PC:

```text
C:\Reloaded-II\Mods
```

Project mod folder:

```text
D:\Projects\FFTModNewGame++\mod\fftivc.battles.rescale
```

Installed/tested Reloaded-II copy:

```text
C:\Reloaded-II\Mods\fftivc.battles.rescale
```

## Tools Used

| Tool | Purpose |
|------|---------|
| Reloaded-II | Launches the game with mods enabled. |
| fftivc.utility.modloader | FFT-specific Reloaded-II loader by Nenkai. Required dependency. |
| FF16Tools | Extracts `.pac` files and converts NXD tables to/from SQLite. |
| SQLite DB | Used to inspect NXD tables such as `SortieConfirm` and `OverrideEntryData`. |
| `tools\entd_tool.py` | Local helper script to dump and patch binary ENTD entries. |

## File Types We Care About

The game stores data in `.pac` archives under:

```text
<game>\data\enhanced
```

Important findings:

```text
0002.pac -> fftpack/battle_entd1_ent.bin
0002.pac -> fftpack/battle_entd2_ent.bin
0002.pac -> fftpack/battle_entd3_ent.bin
0002.pac -> fftpack/battle_entd4_ent.bin
0004.pac -> NXD database tables, including OverrideEntryData, SortieConfirm, EventId, Map
```

The `battle_entd*_ent.bin` files are the base encounter data.

The `OverrideEntryData` NXD table is a sparse patch layer. If a value is unset, the game uses
the base binary ENTD value. For Gariland, `OverrideEntryData` had placeholder rows but no
level override, so editing `battle_entd4_ent.bin` worked.

## Reloaded-II Mod Structure

The mod folder must look like this:

```text
fftivc.battles.rescale\
  ModConfig.json
  FFTIVC\
    data\
      enhanced\
        fftpack\
          battle_entd4_ent.bin
```

For FFTPack files, the loader docs confirm this rule:

```text
FFTIVC\data\enhanced\fftpack\<file>
```

Files placed there are loaded from the mod folder and inserted into the generated modded
overlay.

To install/update the mod in Reloaded-II:

```powershell
New-Item -ItemType Directory -Force -Path "C:\Reloaded-II\Mods\fftivc.battles.rescale"
Copy-Item -LiteralPath "D:\Projects\FFTModNewGame++\mod\fftivc.battles.rescale\ModConfig.json" -Destination "C:\Reloaded-II\Mods\fftivc.battles.rescale\ModConfig.json" -Force
Copy-Item -LiteralPath "D:\Projects\FFTModNewGame++\mod\fftivc.battles.rescale\FFTIVC" -Destination "C:\Reloaded-II\Mods\fftivc.battles.rescale" -Recurse -Force
```

Do not copy the whole source folder onto an existing destination folder, or PowerShell may
create a nested `fftivc.battles.rescale\fftivc.battles.rescale` folder. Reloaded-II reads
the root folder only.

Then restart Reloaded-II and enable:

```text
FINAL FANTASY TACTICS - The Ivalice Chronicles Mod Loader
New Game++
```

Launch through Reloaded-II, not directly through Steam.

## ENTD Binary Layout

Each story/random battle uses one ENTD entry.

The Enhanced version has four ENTD binary files:

| File | Global entries |
|------|----------------|
| `battle_entd1_ent.bin` | `0-127` |
| `battle_entd2_ent.bin` | `128-255` |
| `battle_entd3_ent.bin` | `256-383` |
| `battle_entd4_ent.bin` | `384-511` |

Confirmed layout:

```text
128 entries per file
0x280 bytes per entry
16 unit slots per entry
0x28 bytes per unit slot
level byte at unit slot offset 0x03
```

Formula:

```text
file number        = global_entry // 128 + 1
local entry        = global_entry % 128
entry file offset  = local_entry * 0x280
unit file offset   = entry file offset + slot * 0x28
level byte offset  = unit file offset + 0x03
```

Known useful unit fields from the binary:

| Slot offset | Meaning |
|-------------|---------|
| `0x00` | Sprite set |
| `0x01` | Flags |
| `0x02` | Name/special id |
| `0x03` | Level |
| `0x06` | Bravery |
| `0x07` | Faith |
| `0x08` | `JobUnlock` / roster JP target index. Do not treat it as a visible rank. |
| `0x09` | `JobLevel` seed for the job selected by `0x08` |
| `0x0A` | Main job |
| `0x0B` | Secondary skillset |
| `0x0C` | Reaction ability, 2 bytes |
| `0x0E` | Support ability, 2 bytes |
| `0x10` | Movement ability, 2 bytes |
| `0x18` | Control/team flags; OR with `0x08` to make an allied guest player-controllable while preserving the other bits |

Guest handling:

```text
The runtime guest scaler applies to known guest charIds where mainJob == charId. It sets party-level
scaling and 0x18 |= 0x08 so allied guests are player-controllable globally.
The prologue Orbonne entry (global 387) is explicitly skipped, so Gaffgarion/Agrias remain vanilla
AI there. Enemy/boss forms with reused charIds are skipped by the mainJob == charId guard or by the
enemy-team bit.

Important implementation detail: do this for full ENTD reads and partial ENTD reads. Some event/join
code can read only the slice it needs; if guest scaling only runs when `sectorOffset == 0` and
`size == 0x14000`, a joined guest such as pre-Gariland Delita can still be cached into the save at
the vanilla level.
```

Roster Job Level / save-cache caveat:

```text
Once a guest has joined the roster, visible Job Level and JP live in the saved roster cache, not
only in ENTD. ENTD byte 0x09 can seed a job level at join time, but it does not repair a guest who
is already cached into the save.

Do not patch joined guests by blind live-memory scanning. A short-lived scanner experiment was
removed because the target structure was not validated. Do not reuse the old guessed roster offsets
(`level +0x02`, `job +0x03`, `first job JP +0xF0`) unless they are independently revalidated from
decoded save data.

The confirmed join-time ENTD source for Chapter-1 Delita is battle_entd4_ent.bin entry 392 slot 1,
which controls his character level before Gariland. This must be patched on both full ENTD reads and
partial ENTD reads, because join/event code can cache a guest before the first battle load.

2026-06-29 finding: setting entry 392 slot 1 `0x08=7, 0x09=8` made Delita receive Time Mage
Job Level 8, while Squire stayed Job Level 1. Therefore `0x08` is a job/JP target index, not a
zero-based rank. Vanilla Delita/Argath Squire records use `0x08=1, 0x09=1`; the current test build
uses `0x08=1, 0x09=8` for the known Chapter-1 Squire guest join records.

2026-06-29 autosave confirmation: the bad cached Delita record can be repaired safely from the
decoded save. In the active autosave, Delita's Brave/Faith fingerprint `47 37` was found in
`resume_enwm_main.sav`/`resume_enbtl_world.sav` at `0x7BCA` and in battle-state resumes at
`0x8CB7A`. From that fingerprint:

- packed visible job levels start at `br_fa + 0x56`
- job JP u16 table starts at `br_fa + 0x62`
- bad bytes `12 11 11 38 ...` mean Squire Lv1 / Chemist Lv2 / ... / Black Mage Lv3 / Time Mage Lv8
- fixed bytes `82 11 11 31 ...` mean Squire Lv8 / Chemist Lv2 / ... / Black Mage Lv3 / Time Mage Lv1

`tools/fft_save_patch_delita.py` performs this narrow repair on `autoenhanced.png` with a backup:

python tools/fft_save_patch_delita.py "<save dir>\autoenhanced.png" --in-place
```

## First Confirmed Battle: Gariland

Battle:

```text
Magick City of Gariland
First Chapter 1 battle after the prologue
```

Confirmed ENTD location:

```text
global ENTD entry: 388
file: battle_entd4_ent.bin
local entry inside entd4: 4
```

Evidence:

```text
SortieConfirm key 4 -> MapId 22, matching Gariland/Magick City.
ENTD entry 388 has one special/player-side slot plus five level-1 generics.
Enemy jobs are 74, 74, 74, 75, 74.
That matches the stock battle shape: 4 Squires + 1 Chemist.
OverrideEntryData key 388 has rows for slots 0-5, but Level=-1, so base ENTD levels apply.
```

Successful patch:

| Slot | File offset | Old level | New level |
|------|-------------|-----------|-----------|
| 1 | `0x00A2B` | `1` | `100` |
| 2 | `0x00A53` | `1` | `100` |
| 3 | `0x00A7B` | `1` | `100` |
| 4 | `0x00AA3` | `1` | `100` |
| 5 | `0x00ACB` | `1` | `100` |

Slot `0` was intentionally left unchanged because it appears to be Ramza/special/player-side.

The patched file is:

```text
mod\fftivc.battles.rescale\FFTIVC\data\enhanced\fftpack\battle_entd4_ent.bin
```

## Helper Script

Script:

```text
tools\entd_tool.py
```

Dump an ENTD entry:

```powershell
python .\tools\entd_tool.py dump-entry --input .\extracted\enhanced_0002_selected\fftpack\battle_entd4_ent.bin --entry 388 --csv .\work\entd_388_gariland_candidate.csv
```

Patch selected slots to level `100`:

```powershell
python .\tools\entd_tool.py patch-levels --input .\extracted\enhanced_0002_selected\fftpack\battle_entd4_ent.bin --output .\work\battle_entd4_ent.gariland-level100.bin --entry 388 --slots 1 2 3 4 5 --level 100
```

Copy the patched file into the mod:

```powershell
Copy-Item .\work\battle_entd4_ent.gariland-level100.bin .\mod\fftivc.battles.rescale\FFTIVC\data\enhanced\fftpack\battle_entd4_ent.bin -Force
```

Sanity check after patching:

```text
Only the intended bytes should differ from the original.
For the Gariland validation patch, exactly 5 bytes changed.
```

## Workflow for the Next Battles

1. Identify the story battle's map/event.
2. Correlate it with `SortieConfirm`, `EventId`, scenario tables, and ENTD candidates.
3. Dump likely ENTD entries with `tools\entd_tool.py`.
4. Match the unit pattern against the known battle composition.
5. Identify enemy slots; avoid player, guest, or scripted special slots.
6. Patch enemy Level to `100 + offset`.
7. Optionally change jobs, gear, skills, and placement.
8. Copy the patched `battle_entd*_ent.bin` into the mod folder.
9. Copy/update the mod into `C:\Reloaded-II\Mods`.
10. Launch via Reloaded-II and test in-game.
11. Record the battle id, offsets, slots, and design notes in `notes\`.

## Project Layout

```text
D:\Projects\FFTModNewGame++\
  README.md
  tools\
    entd_tool.py
    FF16Tools.CLI-1.13.2-win-x64\
  extracted\
    enhanced_0002_selected\
    enhanced_0004\
  work\
    enhanced_0004.sqlite
    entd_388_gariland_candidate.csv
    entd_388_gariland_level100_patch.csv
  mod\
    fftivc.battles.rescale\
  docs\
    battles\
      001-gariland.md
  backups\
    enhanced_modded_20260619_182139\
  notes\
    01-encounter-data-and-gariland.md
    02-gariland-first-patch.md
```

## Safety Notes

- Do not edit game files directly unless intentionally testing a throwaway setup.
- Keep original extracted files untouched under `extracted\`.
- Write patched outputs to `work\` first.
- Copy patched files into `mod\`, then into `C:\Reloaded-II\Mods`.
- Existing `data\enhanced\modded*.pac` files were backed up under `backups\`.
- After every game update, re-extract the touched files and reapply patches to the new
  vanilla data instead of carrying old binaries forward blindly.

## Current Status

Done:

- Game install found.
- FF16Tools downloaded.
- Relevant ENTD files extracted.
- NXD tables converted to SQLite.
- Gariland identified as ENTD entry `388`.
- Enemy slots `1-5` patched from level `1` to `100`.
- Reloaded-II mod folder created.
- Mod installed under `C:\Reloaded-II\Mods`.
- Mod renamed to **New Game++**.
- In-game test succeeded.

Next:

- Start designing the full New Game++ Gariland composition.
- Identify the next Chapter 1 story battle.
- Build a battle-by-battle design table so the whole campaign can be patched systematically.

## Sources

- Nenkai `fftivc.utility.modloader`: https://github.com/Nenkai/fftivc.utility.modloader
- Nenkai FFT mod guide: https://nenkai.github.io/ffxvi-modding/modding/creating_mods_fft/
- Nenkai FF16Tools: https://github.com/Nenkai/FF16Tools
- FF16Tools extraction docs: https://nenkai.github.io/ffxvi-modding/tutorials/file_extraction/
- NXD editing docs: https://nenkai.github.io/ffxvi-modding/tutorials/nex/nxd_editing/
- Final Fantasy Hacktics ENTD reference: https://ffhacktics.com/wiki/ENTD
- Reloaded-II: https://github.com/Reloaded-Project/Reloaded-II
- FFTIvaliceEditor: https://github.com/mullerdane85-hash/FFTIvaliceEditor
