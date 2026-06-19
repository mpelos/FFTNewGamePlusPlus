# Gariland validation patch

Date: 2026-06-19

Target: Enhanced v1.5.0, first Chapter 1 battle after the prologue.

## Current hypothesis

Global ENTD entry `388` is Magick City of Gariland.

Evidence:

- `SortieConfirm` key `4` points to `MapId=22`, matching Gariland/Magick City.
- The ENTD shape for entry `388` is one special/player-side slot plus five level-1 generics.
- Enemy job pattern is `74, 74, 74, 75, 74`, matching the known stock composition of 4 Squires + 1 Chemist.
- `OverrideEntryData` has rows for key `388`, slots `0-5`, but `Level=-1` on all of them, so the base ENTD level bytes are currently in effect.

## Patch made

Source:

`extracted/enhanced_0002_selected/fftpack/battle_entd4_ent.bin`

Patched output:

`mod/fftivc.battles.rescale/FFTIVC/data/enhanced/fftpack/battle_entd4_ent.bin`

Entry `388` lives in `battle_entd4_ent.bin` as local entry `4`.

Changed level byte from `1` to `100` for slots `1-5`:

| Slot | Absolute offset in entd4 file | Old | New |
|------|-------------------------------|-----|-----|
| 1 | `0x00A2B` | `1` | `100` |
| 2 | `0x00A53` | `1` | `100` |
| 3 | `0x00A7B` | `1` | `100` |
| 4 | `0x00AA3` | `1` | `100` |
| 5 | `0x00ACB` | `1` | `100` |

Slot `0` was intentionally left fixed at level `1`; it appears to be the Ramza/special/player-side entry.

## How to reproduce

Dump:

```powershell
python .\tools\entd_tool.py dump-entry --input .\extracted\enhanced_0002_selected\fftpack\battle_entd4_ent.bin --entry 388 --csv .\work\entd_388_gariland_candidate.csv
```

Patch:

```powershell
python .\tools\entd_tool.py patch-levels --input .\extracted\enhanced_0002_selected\fftpack\battle_entd4_ent.bin --output .\work\battle_entd4_ent.gariland-level100.bin --entry 388 --slots 1 2 3 4 5 --level 100
```

Deploy:

```powershell
Copy-Item .\work\battle_entd4_ent.gariland-level100.bin .\mod\fftivc.battles.rescale\FFTIVC\data\enhanced\fftpack\battle_entd4_ent.bin -Force
```

## In-game test

Install/enable `mod/fftivc.battles.rescale` in Reloaded-II with dependency `fftivc.utility.modloader`.

Use a New Game+ file with a high-level roster and start the first Chapter 1 battle at Gariland. Expected result: the five enemies should enter near the highest party level, not level 1.

If this works, the `Level=100` story-battle scaling mechanic is confirmed for v1.5.0 and we can start designing the full Gariland New Game++ composition.
