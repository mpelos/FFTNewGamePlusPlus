# 060 - Chapter 4 Sidequest Level Scaling

## Scope

All optional Chapter 4 combat content is retained exactly as shipped: jobs, composition,
equipment, abilities, Brave/Faith, placement, objectives, rewards, and guest behavior are
unchanged.  New Game++ changes only enemy levels:

- ordinary enemies alternate between level encodings `100` and `101`;
- the encounter leader uses `102`;
- allied guests and recruitment/cutscene records remain vanilla.

## Complete battle inventory

| Sidequest | Battles covered | Level rule |
|---|---:|---|
| Beowulf / Reis / Construct 8 / Cloud chain | Colliery Underground Third Floor; Second Floor; First Floor; Underground Passage in Goland; Nelveska Temple; Zarghidas Trade City | Enemies 100-101; Construct 7 at 102 |
| Midlight's Deep | Nogias, Terminus, Delta, Valkyries, Mlapan, Tiger, Bridge, Voyage, Horror, End | Every random formation enemy 100-101; Elidibus at 102 |

The non-combat Goug scenes, Reis's transformation/recruitment records, the Bervenia Volcano
Materia Blade visit, and inaccessible test/debug formations are intentionally not treated as
battles.  No enemy level exists to scale in the non-combat records.

## Data coverage

- `battle_entd4_ent.bin`: global entries 463-466 (Goland), 468 (Nelveska), and
  475 (Zarghidas).
- `battle_entd3_ent.bin`: EntryNo 90, the dedicated Midlight END encounter with Elidibus.
- `battle_entd1_ent.bin`: every random formation selected for Midlight's Deep map assets
  78-82 (EntryNo 73-80, 85-92, 94, 97-104, and 107-127).

The ENTD1 list was derived by joining `EntryNo.SortieConfirmId` to `SortieConfirm.MapId`, rather
than by assuming a contiguous range.  Entries for other maps inside that numeric window are
therefore excluded.

## Validation checklist

- Only byte `+0x03` (level) differs from the source ENTD1 records.
- Existing v3 changes in ENTD4 remain intact; this patch changes only `+0x03` in the listed slots.
- Beowulf, Reis, Cloud, and other allies are not level-patched.
- Construct 7 and Elidibus are the only leaders and are level 102.
- All other active sidequest enemies are level 100 or 101.
