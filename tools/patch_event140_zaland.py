"""Patch event140.e (Zaland intro) to choreograph the added s8 Dragoon (uid 0x86).

Zaland's six vanilla enemies (flags 0xD0) are script-managed: event140.e registers
them in two AddUnit brackets and choreographs their entrance (warp -> color-prep ->
draw/fade-in -> alert pose 0x03 -> idle pose 0x02) while Mustadio (0x22) runs.
The mod's added s8 Dragoon must mirror its wave-2 siblings (0x83-0x85, which
include the other Dragoon s4/0x83), so this patch makes three insertions into the
PRISTINE file (offsets are pristine-file positions; applied end-first):

  A @0x168  registration    `45 86 00 01` appended inside bracket 2, before its 4A
  B @0x30B  entrance block  WarpUnit (6,9) + ColorUnit prep + Draw + ColorUnit
                            fade-in + UnitAnim 0x03, right after the three wave-2
                            Draw records
  C @0x37D  final idle      `11 86 00 02 00 00`, right after 0x85's own idle record

Insertion-safety: each site is a record boundary; the format has no length/offset
fields to desync (docs/modding/03, validated live by the event119.e Merchant patch).

Writes the patched file to the mod source tree (deployed by `dotnet build`).
Idempotent: verifies the pristine input hash and produces a fixed-size output.
"""

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRISTINE = ROOT / "tmp/pac0005/script/enhanced/event140.e"
OUT = ROOT / "src/fftivc.battles.ngplus/FFTIVC/data/enhanced/script/enhanced/event140.e"

PRISTINE_SHA = "BD98A99D679A53E7F8A964AE65E223059BB4D5AFBFAB33B8991D10BC5430C14E"
PRISTINE_SIZE = 1367

ENTRANCE_BLOCK = bytes.fromhex(
    "5f 86 00 00 0a 00 00"        # WarpUnit  uid=0x86 tile=(0,10) — the s8 ENTD tile
    "32 86 00 01 00 00 00 00"     # ColorUnit prep (same shape as siblings' pre-draw prep)
    "44 86 00"                    # Draw
    "32 86 00 08 00 00 00 02"     # ColorUnit fade-in (siblings' post-draw record)
    "11 86 00 03 00 00"           # UnitAnim alert pose 0x03 (wave-2 initial pose)
    .replace(" ", "")
)

# (offset_in_pristine, bytes) — applied highest offset first
INSERTIONS = [
    (0x37D, bytes.fromhex("118600020000")),   # C: idle pose 0x02, after 0x85's idle
    (0x30B, ENTRANCE_BLOCK),                   # B: entrance, after wave-2 draws
    (0x168, bytes.fromhex("45860001")),        # A: AddUnit uid=0x86 draw=1, before 4A
]

# context guards: byte(s) that must immediately precede each insertion point
GUARDS = {
    0x37D: bytes.fromhex("118500020000"),  # 0x85's idle record
    0x30B: bytes.fromhex("448500"),        # last wave-2 Draw
    0x168: bytes.fromhex("45850001"),      # last bracket-2 AddUnit record
}


def main():
    data = PRISTINE.read_bytes()
    if len(data) != PRISTINE_SIZE or hashlib.sha256(data).hexdigest().upper() != PRISTINE_SHA:
        sys.exit(f"pristine event140.e mismatch ({len(data)}B) — refusing to patch")
    out = bytearray(data)
    for off, ins in INSERTIONS:
        guard = GUARDS[off]
        if out[off - len(guard):off] != guard:
            sys.exit(f"context guard failed at 0x{off:X} — refusing to patch")
        out[off:off] = ins
    expected = PRISTINE_SIZE + sum(len(i) for _, i in INSERTIONS)
    assert len(out) == expected, (len(out), expected)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(out)
    print(f"wrote {OUT}")
    print(f"size {len(out)} (0x{len(out):X}) = pristine {PRISTINE_SIZE} + "
          f"{len(out) - PRISTINE_SIZE} inserted")
    print(f"sha256 {hashlib.sha256(out).hexdigest().upper()}")


if __name__ == "__main__":
    main()
