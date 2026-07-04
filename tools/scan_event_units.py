"""Scan extracted .e event scripts for AddUnit unit-registration brackets.

Answers the pre-implementation question of docs/modding/10: "are this battle's
units delivered by an event script, or are they plain static ENTD units?"

- If a battle's enemy uids appear in a script's AddUnitStart/AddUnit/AddUnitEnd
  bracket, those units are EVENT-DELIVERED: adding a sibling requires the
  three-layer recipe of docs/modding/04 (ENTD + choreography + registration)
  in the file that is actually loaded (confirm via Reloaded file-access
  logging — NXD joins can name the wrong file).
- If they do not appear in any bracket, the units are STATIC: the ENTD slot
  (with 0x40-free present flags, e.g. 0x90) is the mechanism, no script edit
  is needed for the unit to function (validated: Gariland, Araguay, Zeirchele,
  Zaland), at most a cosmetic intro-pose gap remains.

Bracket encoding (docs/modding/03): 0x49 AddUnitStart, then one 4-byte record
`45 <uid> 00 <draw>` per unit, then 0x4A AddUnitEnd. Draw is usually 0 or 1. This is a byte-scan
approximation, not a full opcode walk — good enough because the record shape
is distinctive.

Usage:
  python tools/scan_event_units.py 0x80 0x81      # scripts registering these uids
  python tools/scan_event_units.py --all           # dump every bracket
"""

import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "tmp/pac0005/script/enhanced"


def brackets(data):
    out = []
    i = 0
    while i < len(data):
        if data[i] == 0x49:
            j = i + 1
            uids = []
            while (j + 3 < len(data) and data[j] == 0x45
                   and data[j + 2] == 0x00 and data[j + 3] in (0x00, 0x01)):
                uids.append(data[j + 1])
                j += 4
            if uids and j < len(data) and data[j] == 0x4A:
                out.append((i, uids))
                i = j
        i += 1
    return out


def main(argv):
    if not SCRIPTS.is_dir():
        sys.exit(f"extracted scripts not found: {SCRIPTS} "
                 f"(extract 0005.pac first — see docs/modding/04)")
    if not argv:
        print(__doc__)
        return 2
    want = None
    if argv != ["--all"]:
        want = {int(a, 0) for a in argv}
    for f in sorted(SCRIPTS.glob("event*.e")):
        data = f.read_bytes()
        for off, uids in brackets(data):
            if want is not None and not (want & set(uids)):
                continue
            print(f"{f.name} ({len(data)}B) @0x{off:X}: "
                  f"{[hex(u) for u in uids]}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
