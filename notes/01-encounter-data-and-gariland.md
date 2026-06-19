# Encounter data model + starting battle (Gariland, Chapter 1)

## The encounter table: `OverrideEntryData`

FFT TIC stores per-unit battle data in the NXD table **`OverrideEntryData`** — the
remaster's name for the classic **ENTD** ("Entry Data"). Confirmed from the official
table-layout repo: **Nenkai/fftivc-nex-layouts** (`OverrideEntryData.layout`), the layout
source FF16Tools uses to convert NXD ⇄ SQLite.

**Key property — it's an OVERRIDE/patch table.** Each column only patches the original ENTD
field **if set** (most are "if not zero / if >= 0, cast and patch that field"). Leave a
column at its default and the game keeps the original value. → **Low-risk editing: we only
change the fields we explicitly set.**

**Table type:** `DoubleKeyed` → each row is keyed by **(BattleId, UnitSlot)**. One battle =
a group of rows sharing the first key; each enemy/ally unit = one row (slot 0–15).

### Columns that matter for this mod (offset → meaning)

| Column | Meaning / use |
|--------|---------------|
| `Spriteset` | unit sprite/graphic |
| `MainJob` | the unit's job/class (→ `Job` table id) |
| `JobUnlock` | unlocked job flags |
| `SecondarySkillset` | secondary command (→ skillset) |
| `Reaction` / `Support` / `Movement` | the R/S/M ability slots |
| `Head` / `Body` / `Accessory` / `RightHand` / `LeftHand` | the 5 equipment slots (→ `Item` table ids) |
| `InitialDirection` | facing |
| `UnitId+characontrolid+Id` | named-unit link (boss/special) |
| `Present` | always/randomly-present flags (mask 0xC) |
| **`Level`** | **unit level — the scaling lever (see below). `>0` patches it.** |
| `JobLevel` | job level |
| `Bravery` / `Faith` | Brave / Faith stats |
| `PositionX` / `PositionY` / `HigherElevation` | tile placement |
| `Disable` | if set, unit is removed (sprite→0, no other patches) |

### The level-scaling lever

`Level` is a `short`; if `> 0` it patches the ENTD level byte. The engine's ENTD level rule
(classic FFT, inherited): **value > 99 → actual level = party's highest level + (value − 100)**.

- `100` → exactly party level
- `103` → party level + 3
- `1`–`99` → fixed level

So to make Gariland scale: set each enemy's `Level` to `100 + desiredOffset`.

> ⚠️ STEP-0 VERIFY: confirm the remaster honors the `>99` relative encoding for **story**
> battles before scaling the whole campaign. Test on Gariland with `Level=100`.

## Which battle is "Chapter 1, first battle"?

- **Battle 1 (Prologue / skip):** Orbonne Monastery — scripted tutorial.
- **Battle 2 (OUR START):** **Magick City of Gariland** — Ramza + cadets vs. a band of
  thieves. Stock enemy composition: **4× Squire + 1× Chemist** (+ unique leader), recommended
  party level 1, 1-star difficulty.

### Finding Gariland's BattleId in the data

`OverrideEntryData` rows are grouped by the first key (BattleId). To identify Gariland's id:
1. Unpack + convert to SQLite (below), open `OverrideEntryData`.
2. Cross-reference with `Map` / `PlaceName` / `Chapter` / `ScenarioId` / `EventId` tables to
   map BattleId → location/scenario.
3. Classic-FFT hint: Gariland is the first Chapter-1 story battle (classic ENTD id near
   `0x100`); use this as a starting hypothesis, then confirm by the cross-reference and an
   in-game test.
4. FFTIvaliceEditor lists encounters by name — fastest sanity check.

## How to start (concrete)

1. Install **.NET 8** (+ .NET 9 for FFTIvaliceEditor). Get **FF16Tools** into `tools\`.
2. Back up `data\enhanced\modded*.pac` → `backups\` (pre-existing overlays!).
3. Find the pac holding the nex DB and unpack into `extracted\`:
   ```
   FF16Tools.CLI.exe unpack-all -i "D:\SteamLibrary\steamapps\common\FINAL FANTASY TACTICS - The Ivalice Chronicles\data\enhanced\0000.pac"
   ```
   (locate `OverrideEntryData.nxd` + the other `.nxd`/`root.nxl` among the extracted files;
   `0000.pac` (989 MB) is the most likely system/data archive — confirm by searching the
   extracted tree for `OverrideEntryData`.)
4. Convert the nex dir to SQLite:
   ```
   FF16Tools.CLI.exe nxd-to-sqlite -i <dir with the .nxd files>
   ```
5. Edit `OverrideEntryData` rows for Gariland in SQLiteStudio (set `Level`, `MainJob`,
   equipment, `Position`, `Present`, etc. on the enemy-team rows).
6. Convert back (optionally only that table):
   ```
   FF16Tools.CLI.exe sqlite-to-nxd -i <sqlite file> -t OverrideEntryData
   ```
   If rows were added/removed, update `root.nxl` row count.
7. Place the rebuilt nxd in the mod folder `FFTIVC\data\enhanced\…`, load via Reloaded-II,
   test in-game.

## How to change the enemies (recipe for one battle)

For each enemy row of the target BattleId:
- **Scale level:** `Level = 100 + offset` (e.g. 100–105).
- **Reclass:** set `MainJob` to a new job id (from `Job` table) → "change composition."
- **Re-gear:** set `Head/Body/Accessory/RightHand/LeftHand` to item ids (from `Item` table).
- **Skills:** set `SecondarySkillset`, `Reaction`, `Support`, `Movement`.
- **Stats:** `Bravery` / `Faith` if desired.
- **Placement:** `PositionX` / `PositionY` / `HigherElevation` / `InitialDirection`.
- **Add/remove units:** add rows (new UnitSlot) or set `Disable` to drop one. Update
  `root.nxl` if row count changes.

## Sources
- Table layouts (authoritative): https://github.com/Nenkai/fftivc-nex-layouts
  (`OverrideEntryData.layout`, `Battle.layout`, `EntryNo.layout`, `EntryArea.layout`)
- NXD ⇄ SQLite workflow: https://nenkai.github.io/ffxvi-modding/tutorials/nex/nxd_editing/
- ENTD level rule (>99 = party level + value−100): https://ffhacktics.com/wiki/ENTD
- Gariland battle composition: https://game8.co/games/Final-Fantasy-Tactics/archives/553163
  and https://strategywiki.org/wiki/Final_Fantasy_Tactics/Gariland_Magic_City
- Enemy leveling / NG+ context: https://steamcommunity.com/app/1004640/discussions/0/624436764983028135/
