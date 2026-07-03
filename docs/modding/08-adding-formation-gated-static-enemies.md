# Adding a new enemy to a formation-gated static roster

This document covers a third slot-add case discovered and validated on **Zeirchele Falls**
(Chapter 2, ENTD entry `405`): the new unit is not an event-scripted wave enemy like Merchant
Dorter, but a plain ENTD high-slot add is still ignored until the battle's `OverrideEntryData`
formation layer is expanded.

Use this technique when:

- the battle's active enemies are meant to be present when tactical control starts;
- there is no delayed enemy-arrival wave that needs choreography or registration;
- a new ENTD slot looks correct in the binary but does not appear in-game;
- the battle has `OverrideEntryData` rows only through the old highest slot.

For ordinary fully-static rosters where the new ENTD slot appears immediately, use the plain slot
add described in [06-job-swap-fallback-and-battle-inventory.md](06-job-swap-fallback-and-battle-inventory.md).
For delayed/event-spawned waves, use
[04-adding-event-spawned-enemies.md](04-adding-event-spawned-enemies.md).

## Core fact

Some battles have two relevant formation layers:

1. **Base ENTD slot data** in `battle_entd*_ent.bin`: job, level, equipment, UnitID, position, flags.
2. **`OverrideEntryData` NXD rows** keyed by `Key` (battle/ENTD entry) and `Key2` (slot index).

If the ENTD contains a valid new high slot but `OverrideEntryData` rows stop before that slot, the
game can ignore the new unit. In Zeirchele, the ENTD `s11` unit was valid but the battle stayed at
six enemies until the NXD table gained row `Key=405, Key2=11`.

Two caveats added after the Zaland (407 s8) add, 2026-07-02:

- **The NXD row is NOT sufficient if the added slot's flags carry bit `0x40`.** Zaland's add,
  cloned from a `0xD0`-flagged sibling, had its row in place and still never appeared; forcing
  flags to `0x90` (one byte) made it spawn. Check the flags BEFORE reaching for this recipe — see
  [10-event-scripts-and-the-e-files.md](10-event-scripts-and-the-e-files.md).
- **The row's necessity has not been isolated.** In both Zeirchele and Zaland the row was present
  in every decisive test, so "row required" rests on pre-journal iterations with concurrent
  variables. Shipping the row remains current practice; a row-removal test on a working add would
  settle whether it is load-bearing.

This is not the Merchant Dorter event-spawn problem. There is no copied choreography block and no
`AddUnit` registration entry. The roster is static, but the static formation is gated by NXD.

## Proven example: Zeirchele Falls

Vanilla-relevant roster:

```text
s0    Gaffgarion, enemy/betrayer (charId 0x05)
s1    Ovelia, VIP ally (charId 0x0C)
s2    intro corpse actor (Knight), level 0xfe, UnitID 0x80
s3    intro corpse actor (Knight), level 0xfe, UnitID 0x81
s4-s8 five active Knights
s9    Gaffgarion escort form (charId 0x17), event-added by the intro script
s10   Agrias (charId 0x34), event-added by the intro script
```

Important distinction: `s2` and `s3` are not spare active-enemy slots. They are story corpse
placeholders shown during the intro scene and removed by `event129.e` before tactical control. They
must remain byte-for-byte vanilla. Replacing either one changes the cutscene body, not the combat
roster. Likewise `s9`/`s10` are the intro script's `AddUnit` targets, not free slots.

The working add (final composition):

```text
ENTD:  entry 405, slot s11, UnitID 0x87, Knight, enemy control byte 0x90
ENTD:  the battle's new job (White Mage) lives in vanilla active slot s7 via job-swap
NXD:   OverrideEntryData row Key=405, Key2=11 added, shaped like the battle's ACTIVE-ENEMY rows
root:  root.nxl count changed from overrideentrydata,96,517,3 to overrideentrydata,96,518,3
```

Two constraints shaped that composition, both proven in-game:

- **Sprite-sheet budget** (see [09-sprite-sheet-budget.md](09-sprite-sheet-budget.md)): the added
  high-slot unit is a Knight — a sheet the battle already loads — because Zeirchele tolerates
  exactly one NEW generic sheet (the s7 White Mage). The earlier composition with two new sheets
  (Archer + White Mage) corrupted Agrias's sprite/portrait regardless of which slot held which job.
- **Row shape**: clone the NXD row from one of the battle's active-enemy rows, not from the trailing
  story/corpse rows. In Zeirchele every vanilla active Knight row carries `Unknown64='[60,60,60]'`
  while story/corpse rows carry `'[]'`. A corpse-shaped (all-default) row still materializes the
  unit, so this is convention-matching rather than a hard gate — but the active-enemy shape is the
  vanilla pattern for combat rows and costs nothing.

`Unknown9C` is **not** a per-battle end marker. Vanilla Zeirchele carries `Unknown9C=150` on rows
`Key2=0` and `Key2=10` and `112` on `Key2=1` (all named story units), with `0` on every generic
combat row. The working patch leaves all vanilla `Unknown9C` values untouched and uses `0` on the
new row, matching the combat-row convention. Moving the value between rows is neither needed nor
meaningful.

In-game result: Zeirchele starts with seven enemies (Gaffgarion + five Knights + the s7 White Mage),
Agrias renders normally, and the vanilla intro corpses remain normal story scenery.

## Procedure

1. **Confirm this is not a delayed wave.** A scripted betrayal, retreat, death, or corpse removal is
   not the same as a scripted enemy arrival. Only use the event-spawned recipe if the new enemy must
   be activated by an event wave.

2. **Identify cutscene/story placeholders before choosing a slot.** Slots with level `0xfe`, unusual
   story UnitIDs, or removal commands in the event script may be scenery or named story actors. Do
   not repurpose them just because they disappear before combat.

3. **Check the sprite-sheet budget before choosing the new unit's job.** Run
   `python tools/sprite_budget.py <entry>` and keep the battle at net +1 unique sheet or less versus
   vanilla (see [09-sprite-sheet-budget.md](09-sprite-sheet-budget.md)). If the design's new job
   would be the second new sheet, either reuse an existing sheet for the added slot and job-swap the
   new job into a vanilla slot, or drop/substitute a sheet elsewhere.

4. **Add the new ENTD slot normally.** Clone a compatible active enemy slot, assign a free UnitID,
   set job/equipment/level/R-S-M, set a valid position, and use enemy-side flags/control bytes
   matching the battle's active enemies.

5. **Inspect `OverrideEntryData` for that battle key.** Convert the current source NXD to SQLite and
   check the rows for the target `Key`:

   ```powershell
   tools\FF16Tools.CLI-1.13.2-win-x64\win-x64\FF16Tools.CLI.exe nxd-to-sqlite -g fft -i src\fftivc.battles.ngplus\FFTIVC\data\enhanced\nxd -o tmp\verify-nxd\current.sqlite
   ```

   Then query:

   ```sql
   select *
   from overrideentrydata
   where Key = <entry>
   order by Key2;
   ```

6. **If rows stop before the new slot, insert a row for the new `Key2`.** Preserve the table's schema
   exactly and clone the row **from one of the battle's active-enemy rows** (in Zeirchele these
   differ from story/corpse rows only in `Unknown64`, which is `'[60,60,60]'` on every active Knight
   row). Change only the key fields (`Key2`) for the new slot. Leave every vanilla row untouched —
   including `Unknown9C`, which is not an end marker (named story rows carry values like 150/112;
   generic combat rows carry 0; the new combat row uses 0).

7. **Update `root.nxl` to match the new NXD row count.** If `overrideentrydata.nxd` gains one row,
   the `root.nxl` table line must gain one row too. Zeirchele changed:

   ```text
   overrideentrydata,96,517,3
   ```

   to:

   ```text
   overrideentrydata,96,518,3
   ```

8. **Convert SQLite back to NXD and deploy both files.** The game needs the updated
   `overrideentrydata.nxd` and matching `root.nxl`. Roundtrip fidelity can be proven first by
   regenerating the NXD from an unmodified SQLite export and comparing hashes — the converter
   reproduces the file byte-for-byte, so a regenerated file differs only by the intended edit.

   ```powershell
   tools\FF16Tools.CLI-1.13.2-win-x64\win-x64\FF16Tools.CLI.exe sqlite-to-nxd -g fft -i tmp\verify-nxd\current.sqlite -o tmp\verify-nxd\out -t OverrideEntryData
   ```

   (The `-t` table-name filter is case-sensitive: `OverrideEntryData`, not `overrideentrydata`.)
   Copy the generated `overrideentrydata.nxd` and the edited `root.nxl` into the mod's
   `FFTIVC\data\enhanced\nxd\` folder — these are loose file overrides, served without a DLL
   rebuild — and also into the deployed Reloaded-II mod folder if not using the project build's
   copy step.

9. **Validate both layers.** Check the ENTD slot bytes and the NXD row:

   - new ENTD slot has the intended job, UnitID, level, and flags;
   - cutscene placeholder slots remain byte-for-byte vanilla if they are not active enemies;
   - `overrideentrydata` row count matches `root.nxl`;
   - the target `Key/Key2` row exists and matches the active-enemy row shape;
   - all vanilla rows (including their `Unknown9C` values) are untouched.

10. **Playtest from before battle load.** If the battle is already loaded in memory, the new NXD and
    ENTD data may not be reread. Return to a save/state before entering the battle. Playtest with
    the map's FULL player deployment: sprite-budget corruption only manifests when player capacity
    plus ENTD sheets cross the budget (see [09-sprite-sheet-budget.md](09-sprite-sheet-budget.md)).

## Failure signatures

| Symptom | Likely cause | Fix |
|---|---|---|
| Added unit absent although ENTD AND its NXD row are correct | Added slot's flags carry bit `0x40` (clone-copied from a `0xD0` sibling) | Force the flags to `0x90`-style values — validated on Zaland 407 s8; see [10-event-scripts-and-the-e-files.md](10-event-scripts-and-the-e-files.md). |
| ENTD `s11` looks correct but battle still has old enemy count | `OverrideEntryData` rows stop before `s11` | Add a matching NXD row (active-enemy shape) and update `root.nxl`. |
| A cutscene corpse/body changes job but disappears before combat | Repurposed a story placeholder slot | Restore the placeholder and add a separate combat slot. |
| New unit appears in intro scenery or wrong timing | Used an always-present/intro slot when the battle actually needs an event wave | Reclassify as event-spawned and use doc `04`. |
| New unit appears but wrong tile | Slot activation worked; placement is wrong | Iterate ENTD coordinates and verify visually. |
| NXD converts/deploys but game ignores table | `root.nxl` row count does not match the NXD | Update `root.nxl` count and redeploy. |
| A guest/story unit renders with palette-garbage sprite and portrait after the add | Battle is over the sprite-sheet budget (the added unit's job introduced one new sheet too many) | Reuse an existing sheet for the added slot; see [09-sprite-sheet-budget.md](09-sprite-sheet-budget.md). |

## Decision rule

Use this Zeirchele-style NXD expansion only after an ENTD-only static slot-add fails in a battle
whose roster is not delayed by event scripting. If the unit is supposed to arrive during a wave, do
not try to solve it with `OverrideEntryData`; use the three-layer event-spawn recipe instead.
