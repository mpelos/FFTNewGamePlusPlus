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
game can ignore the new unit. In Zeirchele, the ENTD `s11` White Mage was valid but the battle stayed
at six enemies until the NXD table gained row `Key=405, Key2=11`.

This is not the Merchant Dorter event-spawn problem. There is no copied choreography block and no
`AddUnit` registration entry. The roster is static, but the static formation is gated by NXD.

## Proven example: Zeirchele Falls

Vanilla-relevant roster:

```text
s0    Gaffgarion, enemy/betrayer
s1    Ovelia, VIP ally
s2    intro corpse actor, level 0xfe, UnitID 0x80
s3    intro corpse actor, level 0xfe, UnitID 0x81
s4-s8 five active Knights
s9    Agrias, ally
s10   named story unit
```

Important distinction: `s2` and `s3` are not spare active-enemy slots. They are story corpse
placeholders shown during the intro scene and removed by `event129.e` before tactical control. They
must remain byte-for-byte vanilla. Replacing either one changes the cutscene body, not the combat
roster.

The working v2 add:

```text
ENTD:  entry 405, slot s11, UnitID 0x87, White Mage, enemy control byte 0x90
NXD:   OverrideEntryData row Key=405, Key2=11 added
NXD:   Unknown9C marker moved from Key=405, Key2=10 to Key=405, Key2=11
root:  root.nxl count changed from overrideentrydata,96,517,3 to overrideentrydata,96,518,3
```

Validation evidence from the source NXD after the working patch:

```text
count 518
(405, 8, 0)
(405, 9, 0)
(405, 10, 0)
(405, 11, 150)
```

In-game result: Zeirchele starts with seven enemies, including the new White Mage, while the vanilla
intro corpses remain normal story scenery.

## Procedure

1. **Confirm this is not a delayed wave.** A scripted betrayal, retreat, death, or corpse removal is
   not the same as a scripted enemy arrival. Only use the event-spawned recipe if the new enemy must
   be activated by an event wave.

2. **Identify cutscene/story placeholders before choosing a slot.** Slots with level `0xfe`, unusual
   story UnitIDs, or removal commands in the event script may be scenery or named story actors. Do
   not repurpose them just because they disappear before combat.

3. **Add the new ENTD slot normally.** Clone a compatible active enemy slot, assign a free UnitID,
   set job/equipment/level/R-S-M, set a valid position, and use enemy-side flags/control bytes
   matching the battle's active enemies.

4. **Inspect `OverrideEntryData` for that battle key.** Convert the current source NXD to SQLite and
   check the rows for the target `Key`:

   ```powershell
   tools\FF16Tools.CLI-1.13.2-win-x64\win-x64\FF16Tools.CLI.exe nxd-to-sqlite -g fft -i src\fftivc.battles.ngplus\FFTIVC\data\enhanced\nxd -o tmp\verify-nxd\current.sqlite
   ```

   Then query:

   ```sql
   select Key, Key2, Unknown9C
   from overrideentrydata
   where Key = <entry>
   order by Key2;
   ```

5. **If rows stop before the new slot, insert a row for the new `Key2`.** Preserve the table's schema
   exactly. The Zeirchele patch cloned the existing known-good sentinel-shaped row pattern and changed
   only the key fields and marker placement needed for the new slot.

6. **Move the per-battle `Unknown9C` marker to the new final row.** In Zeirchele, the old last row was
   `Key=405, Key2=10, Unknown9C=150`. The working patch set that old row's `Unknown9C` to `0` and put
   `Unknown9C=150` on the new `Key2=11` row. Treat this as a proven rule for this formation-gated
   pattern: the marker belongs on the last row the formation layer should consider for that battle.

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
   `overrideentrydata.nxd` and matching `root.nxl`.

   ```powershell
   tools\FF16Tools.CLI-1.13.2-win-x64\win-x64\FF16Tools.CLI.exe sqlite-to-nxd -g fft -i tmp\verify-nxd\current.sqlite -o tmp\verify-nxd\out -t OverrideEntryData
   ```

   Copy the generated `overrideentrydata.nxd` and the edited `root.nxl` into the mod's
   `FFTIVC\data\enhanced\nxd\` folder, then rebuild/deploy if the project file copy step is needed.

9. **Validate both layers.** Check the ENTD slot bytes and the NXD row:

   - new ENTD slot has the intended job, UnitID, level, and flags;
   - cutscene placeholder slots remain byte-for-byte vanilla if they are not active enemies;
   - `overrideentrydata` row count matches `root.nxl`;
   - the target `Key/Key2` row exists;
   - the marker moved from the old final row to the new final row.

10. **Playtest from before battle load.** If the battle is already loaded in memory, the new NXD and
    ENTD data may not be reread. Return to a save/state before entering the battle.

## Failure signatures

| Symptom | Likely cause | Fix |
|---|---|---|
| ENTD `s11` looks correct but battle still has old enemy count | `OverrideEntryData` rows stop before `s11` | Add matching NXD row and move the marker. |
| A cutscene corpse/body changes job but disappears before combat | Repurposed a story placeholder slot | Restore the placeholder and add a separate combat slot. |
| New unit appears in intro scenery or wrong timing | Used an always-present/intro slot when the battle actually needs an event wave | Reclassify as event-spawned and use doc `04`. |
| New unit appears but wrong tile | Slot activation worked; placement is wrong | Iterate ENTD coordinates and verify visually. |
| NXD converts/deploys but game ignores table | `root.nxl` row count does not match the NXD | Update `root.nxl` count and redeploy. |

## Decision rule

Use this Zeirchele-style NXD expansion only after an ENTD-only static slot-add fails in a battle
whose roster is not delayed by event scripting. If the unit is supposed to arrive during a wave, do
not try to solve it with `OverrideEntryData`; use the three-layer event-spawn recipe instead.
