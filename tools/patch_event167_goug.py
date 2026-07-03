"""Patch event167.e (Goug Lowtown) to spawn the added Time Mage with the Summoners.

Goug's second-wave Summoners are script-managed in event167.e:

  @0xDD4 bracket: AddUnit 0x86, AddUnit 0x88
  after bracket:  Warp/entrance choreography for 0x88 and 0x86

The ENTD adds s11 as uid 0x89, a Time Mage at tile (0,5). This patch inserts:

  A @0xDDD  registration    `45 89 00 01` before the Summoner bracket's closing 4A
  B @0xE6C  entrance block  copied from the 0x86 Summoner family and retargeted to 0x89,
                            with WarpUnit tile changed to (0,5)

Insertion offsets are pristine-file positions and are applied end-first. Writes the
patched file to the mod source tree, where `dotnet build` deploys it.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PRISTINE = ROOT / "tmp/pac0005/script/enhanced/event167.e"
OUT = ROOT / "src/fftivc.battles.ngplus/FFTIVC/data/enhanced/script/enhanced/event167.e"

PRISTINE_SHA = "92824564C77F7EC78E8B64F76C88757BB16B8AF0A0BA6F3F7761D2CA817415A3"
PRISTINE_SIZE = 3885

ENTRANCE_BLOCK = bytes.fromhex(
    "5f 89 00 00 05 00 03"        # WarpUnit uid=0x89 tile=(0,5)
    "3b 89 00 f0 ff 00 00 00 00 00 01 01 00"
    "6f 89 00"
    "32 89 00 01 fa fc fe 00"
    "f1 02 00"
    "44 89 00"
    "32 89 00 08 00 00 00 04"
    "3b 89 00 00 00 00 00 00 00 00 01 0e 00"
    "6f 89 00"
    "11 89 00 02 00 00"
    .replace(" ", "")
)

# (offset_in_pristine, bytes) - applied highest offset first
INSERTIONS = [
    (0xE6C, ENTRANCE_BLOCK),             # after uid 0x86's idle record, before next script phase
    (0xDDD, bytes.fromhex("45890001")),  # AddUnit uid=0x89 draw=1, before bracket close
]

GUARDS = {
    0xE6C: bytes.fromhex("118600020000"),  # uid 0x86's idle record
    0xDDD: bytes.fromhex("45880001"),      # last Summoner-bracket AddUnit record
}


def main() -> int:
    data = PRISTINE.read_bytes()
    sha = hashlib.sha256(data).hexdigest().upper()
    if len(data) != PRISTINE_SIZE or sha != PRISTINE_SHA:
        sys.exit(f"pristine event167.e mismatch ({len(data)}B, {sha}) - refusing to patch")

    out = bytearray(data)
    for off, ins in INSERTIONS:
        guard = GUARDS[off]
        if out[off - len(guard):off] != guard:
            sys.exit(f"context guard failed at 0x{off:X} - refusing to patch")
        out[off:off] = ins

    expected = PRISTINE_SIZE + sum(len(ins) for _, ins in INSERTIONS)
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
