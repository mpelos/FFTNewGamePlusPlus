"""Patch event176.e (Balias Swale intro) to choreograph the added Geomancer.

Balias Swale's six vanilla enemies are 0xD0 flagged in ENTD, but unlike the
delayed-wave scripts (Merchant/Goug/Zaland), the intro script that references
Agrias and the original uids 0x80-0x85 has no AddUnit bracket for that enemy
family. It does, however, explicitly warps/colors/draws each vanilla enemy.

The mod adds s7 as uid 0x86, a Geomancer at ENTD tile (1,6). The first attempt
used a compact warp/draw block after the existing group; it materialized, but
looked wrong because the unit teleported into place and then played movement.

This version mirrors the nearby Black Mage (uid 0x85, two tiles away on the
same side of the map) by interleaving uid 0x86 records into the same entrance
sequence: initial warp, setup, movement, color prep, draw/fade, settle move,
and idle pose. The companion OverrideEntryData row (413,7) expands the
formation layer to include the new slot.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PRISTINE = ROOT / "tmp/pac0005/script/enhanced/event176.e"
OUT = ROOT / "src/fftivc.battles.ngplus/FFTIVC/data/enhanced/script/enhanced/event176.e"

PRISTINE_SHA = "96879F9B368B24BEA672A70D71D7F1554901132944870ABCEEE1F41378C8495F"
PRISTINE_SIZE = 1548

INSERTIONS = [
    # Offsets are pristine event176.e positions and are applied end-first.
    (0x370, bytes.fromhex("2d 86 00 00 00 01 00"), "2d 85 00 00 00 01 00"),
    (0x369, bytes.fromhex("11 86 00 02 00 00"), "11 85 00 02 00 00"),
    (0x363, bytes.fromhex("6f 86 00"), "6f 85 00"),
    (0x360, bytes.fromhex("3b 86 00 00 00 00 00 00 00 00 01 34 00"),
     "3b 85 00 00 00 00 00 00 00 00 01 34 00"),
    (0x353, bytes.fromhex("32 86 00 08 00 00 00 04"), "32 85 00 08 00 00 00 04"),
    (0x347, bytes.fromhex("44 86 00"), "44 85 00"),
    (0x344, bytes.fromhex("11 86 00 04 00 00"), "11 85 00 04 00 00"),
    (0x29A, bytes.fromhex("32 86 00 01 00 00 00 00"), "32 85 00 01 00 00 00 00"),
    (0x27A, bytes.fromhex("6f 86 00"), "6f 85 00"),
    (0x277, bytes.fromhex("3b 86 00 d2 ff 00 00 00 00 00 01 01 00"),
     "3b 85 00 d2 ff 00 00 00 00 00 01 01 00"),
    (0x25A, bytes.fromhex("2d 86 00 0c 00 02 00"), "2d 85 00 0c 00 02 00"),
    (0x253, bytes.fromhex("5f 86 00 01 06 00 00"), "5f 85 00 01 08 00 00"),
]


def main() -> int:
    data = PRISTINE.read_bytes()
    sha = hashlib.sha256(data).hexdigest().upper()
    if len(data) != PRISTINE_SIZE or sha != PRISTINE_SHA:
        sys.exit(f"pristine event176.e mismatch ({len(data)}B, {sha}) - refusing to patch")

    out = bytearray(data)
    for off, ins, guard_hex in INSERTIONS:
        guard = bytes.fromhex(guard_hex)
        if out[off - len(guard):off] != guard:
            sys.exit(f"context guard failed at 0x{off:X} - refusing to patch")
        out[off:off] = ins

    expected = PRISTINE_SIZE + sum(len(ins) for _, ins, _ in INSERTIONS)
    if len(out) != expected:
        sys.exit(f"size mismatch: got {len(out)}, expected {expected}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(out)
    print(f"wrote {OUT}")
    print(f"size {len(out)} (0x{len(out):X}) = pristine {PRISTINE_SIZE} + {len(out) - PRISTINE_SIZE} inserted")
    print(f"sha256 {hashlib.sha256(out).hexdigest().upper()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
