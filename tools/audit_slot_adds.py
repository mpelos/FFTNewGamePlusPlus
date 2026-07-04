"""Audit every slot-add in the modded ENTD against the two formation layers.

For each entd4 entry, compares the modded embedded .bin against the vanilla
extract and, for every ADDED slot (present in modded, empty in vanilla), checks
the conditions that decide whether the unit will actually materialize in-game:

1. Flags bit 0x40 on the ADDED slot: for plain/formation-static adds this is
   a validated blocker, but Recipe B/script-managed adds are allowed to keep
   the sibling 0xD0 convention when their event override and NXD row are both
   present. See docs/modding/10.
2. GATING (HYPOTHESIS — see the work/ journals): if any slot BEFORE the added
   one has the formation-present bit (flags & 0x80) CLEAR, the added slot may
   need an `OverrideEntryData` row (docs/modding/08). Row causality was never
   isolated (Zaland shipped the row in both the failing and working tests),
   so treat the gating column as a heuristic flag, not a verdict.
3. NXD row existence for (entry, slot) in the source OverrideEntryData.
4. root.nxl row count == actual OverrideEntryData row count.
5. UnitID (offset 0x20) uniqueness of the added slot within the entry.
6. Wave adds (added slot itself lacks 0x80) additionally need event/runtime
   activation (docs/modding/04) — flagged as a warning, not auto-checkable.

Run from anywhere: paths are anchored to the repo root. Pass global entry numbers
to scope the audit, e.g. `python tools/audit_slot_adds.py 409`. Exit code 1 on ERROR.
"""

import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
VANILLA_BIN = ROOT / "extracted/enhanced_0002_selected/fftpack/battle_entd4_ent.bin"
MODDED_BIN = ROOT / "src/fftivc.battles.ngplus/entd/battle_entd4_ent.bin"
NXD_DIR = ROOT / "src/fftivc.battles.ngplus/FFTIVC/data/enhanced/nxd"
SCRIPT_DIR = ROOT / "src/fftivc.battles.ngplus/FFTIVC/data/enhanced/script/enhanced"
FF16TOOLS = ROOT / "tools/FF16Tools.CLI-1.13.2-win-x64/win-x64/FF16Tools.CLI.exe"

ENTRY = 0x280
SLOT = 0x28
BASE = 384


def populated(data, g):
    """slot -> (job, flags, uid) for every real unit in the entry."""
    base = (g - BASE) * ENTRY
    out = {}
    for s in range(16):
        row = data[base + s * SLOT: base + (s + 1) * SLOT]
        if row[0x0A] != 0 or row[0x18] != 0:
            out[s] = (row[0x0A], row[0x18], row[0x20])
    return out


def load_override_rows():
    """(entry, slot) set + total row count from the SOURCE OverrideEntryData."""
    with tempfile.TemporaryDirectory() as tmp:
        db = Path(tmp) / "nxd.sqlite"
        res = subprocess.run(
            [str(FF16TOOLS), "nxd-to-sqlite", "-g", "fft",
             "-i", str(NXD_DIR), "-o", str(db)],
            capture_output=True, text=True)
        if res.returncode != 0 or not db.exists():
            sys.exit(f"FF16Tools conversion failed:\n{res.stdout}\n{res.stderr}")
        con = sqlite3.connect(db)
        rows = set(con.execute("select Key, Key2 from overrideentrydata"))
        con.close()
    return rows, len(rows)


def root_nxl_count():
    for line in (NXD_DIR / "root.nxl").read_text().splitlines():
        if line.startswith("overrideentrydata,"):
            return int(line.split(",")[2])
    sys.exit("root.nxl has no overrideentrydata line")


def event_managed_add_ok(entry, slot, uid):
    """Known script-managed slot-adds with objective marker checks."""
    if (entry, slot, uid) == (407, 8, 0x86):
        event140 = SCRIPT_DIR / "event140.e"
        if not event140.exists():
            return False
        data = event140.read_bytes()
        return (
            data.count(bytes.fromhex("45 86 00 01")) == 1
            and data.count(bytes.fromhex("5f 86 00 00 0a 00 00")) == 1
            and data.count(bytes.fromhex("11 86 00 02 00 00")) == 1
        )
    if (entry, slot, uid) == (413, 7, 0x86):
        event176 = SCRIPT_DIR / "event176.e"
        if not event176.exists():
            return False
        data = event176.read_bytes()
        return (
            data.count(bytes.fromhex("5f 86 00 01 06 00 00")) == 1
            and data.count(bytes.fromhex("44 86 00")) == 1
            and data.count(bytes.fromhex("11 86 00 02 00 00")) == 1
        )
    return False


def main():
    entry_filter = {int(a, 0) for a in sys.argv[1:]} if len(sys.argv) > 1 else None
    van = VANILLA_BIN.read_bytes()
    mod = MODDED_BIN.read_bytes()
    rows, row_count = load_override_rows()
    nxl_count = root_nxl_count()

    errors, warnings = [], []
    print("=== slot-add audit (modded vs vanilla entd4) ===")

    if row_count != nxl_count:
        errors.append(f"root.nxl says {nxl_count} rows but OverrideEntryData has "
                      f"{row_count} — the game will ignore the table")

    for e in range(128):
        g = BASE + e
        if entry_filter is not None and g not in entry_filter:
            continue
        v, m = populated(van, g), populated(mod, g)
        added = sorted(set(m) - set(v))
        if not added:
            continue
        battle_rows = sorted(k2 for (k, k2) in rows if k == g)
        for s in added:
            job, flags, uid = m[s]
            # gating: any earlier slot without the formation-present bit stops
            # the plain scan before it reaches this slot
            gated = any(m[p][1] & 0x80 == 0 for p in m if p < s)
            has_row = (g, s) in rows
            wave = flags & 0x80 == 0
            uid_clash = [p for p in m if p != s and m[p][2] == uid]
            event_ok = event_managed_add_ok(g, s, uid)
            tag = f"entry {g} s{s} (job={job}, flags=0x{flags:02X}, uid=0x{uid:02X})"
            print(f"{tag}: gated={gated} nxd_row={has_row} event_layer={event_ok} "
                  f"battle_rows={battle_rows}")
            if flags & 0x40 and not (has_row and event_ok):
                errors.append(f"{tag}: added slot carries flags bit 0x40 "
                              f"(clone-copied?) — validated blocker: the unit "
                              f"never materializes; use 0x90-style flags "
                              f"(docs/modding/10)")
            if gated and not has_row:
                errors.append(f"{tag}: GATED add without an OverrideEntryData row "
                              f"— high risk it will not materialize "
                              f"(hypothesis; docs/modding/08)")
            if not gated and not has_row and battle_rows:
                warnings.append(f"{tag}: not gated, but the battle has NXD rows — "
                                f"a matching row is cheap insurance (docs/modding/08)")
            if not battle_rows and not has_row:
                warnings.append(f"{tag}: battle has ZERO OverrideEntryData rows — "
                                f"untested territory; playtest before adding its "
                                f"first row")
            if wave:
                warnings.append(f"{tag}: added slot lacks the 0x80 present bit — "
                                f"delayed-wave add, ALSO needs event/runtime "
                                f"activation (docs/modding/04)")
            if uid_clash:
                errors.append(f"{tag}: UnitID 0x{uid:02X} collides with slot(s) "
                              f"{uid_clash}")

    print()
    for w in warnings:
        print(f"WARN : {w}")
    for e in errors:
        print(f"ERROR: {e}")
    n_ok = "no" if not errors else len(errors)
    print(f"\n{len(warnings)} warning(s), {len(errors)} error(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
