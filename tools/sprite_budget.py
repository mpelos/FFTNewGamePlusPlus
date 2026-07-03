#!/usr/bin/env python3
"""Static sprite-sheet budget analyzer for TIC battles.

Background (proven in-game on Zeirchele Falls, entry 405, 2026-07-01): the engine
inherits classic FFT's per-battle unique-spritesheet budget. On PSX the limit is a
constant 9 total sheets (BATTLE.BIN 0x00118910), with the player's deploy CAPACITY
reserved up front; exceeding it corrupts the sprite/palette of the last-allocated
unit (event-added guests allocate last, so they are the usual victims). TIC's exact
constant is unverified, but the empirical red line from Zeirchele playtests is:

  vanilla non-player sheets + 1 new generic sheet   -> OK
  vanilla non-player sheets + 2 new generic sheets  -> Agrias palette corruption

This tool counts unique sprite identities per ENTD entry so any future battle edit
can check its headroom BEFORE a playtest:

  unique sheets = unique named charIds (0x02, < 0x80)   [same character may use 2
                  cids for story/guest forms; they MAY share a sheet - flagged]
                + unique generic jobs (0x0A, when cid is 0xFF/0x00)

Player-side sheets (Ramza + deployed generics) are NOT in the ENTD; add the map's
deploy capacity on top when judging headroom.

Usage:
  python tools/sprite_budget.py               # report implemented Chapter 2 entries
  python tools/sprite_budget.py 405 403       # only these global entries
  python tools/sprite_budget.py --all-vanilla # every entry of all 4 vanilla files
"""

from __future__ import annotations

import sys
from pathlib import Path
from xml.etree import ElementTree

ENTRY = 0x280
SLOT = 0x28
ROOT = Path(__file__).resolve().parent.parent
MODDED_ENTD4 = ROOT / "src/fftivc.battles.ngplus/entd/battle_entd4_ent.bin"
VANILLA_DIR = ROOT / "extracted/enhanced_0002_selected/fftpack"
SPECIAL_NAMES = ROOT / "work/SpecialNames.xml"


def load_names() -> dict[int, str]:
    # PSX-era FFTPatcher name table. Treat as a HINT: TIC in-game evidence has already
    # contradicted it at least once (cid 0x05 is the Zeirchele Gaffgarion betrayer in
    # TIC, while this table says Delita). Names are only used for annotations.
    if not SPECIAL_NAMES.exists():
        return {}
    tree = ElementTree.parse(SPECIAL_NAMES)
    return {
        int(e.get("byte"), 16): e.get("name")
        for e in tree.getroot().iter("SpecialName")
        if e.get("byte") and e.get("name")
    }


NAMES = load_names()


def analyze_entry(data: bytes, global_entry: int):
    base = (global_entry % 128) * ENTRY
    named: dict[int, list[int]] = {}
    generic_jobs: dict[int, list[int]] = {}
    disabled = []
    for s in range(16):
        row = data[base + s * SLOT : base + (s + 1) * SLOT]
        if all(v == 0 for v in row):
            continue
        cid, lvl, job = row[0x02], row[0x03], row[0x0A]
        if lvl == 0xFE and (row[0x18] & 0x80) == 0 and cid in (0xFF, 0x00):
            # disabled placeholder that never draws; still listed for awareness
            disabled.append(s)
        if cid not in (0x00, 0xFF) and cid < 0x80:
            named.setdefault(cid, []).append(s)
        elif job != 0x00:
            generic_jobs.setdefault(job, []).append(s)
    return named, generic_jobs, disabled


def describe(named, generic_jobs) -> str:
    parts = []
    for cid, slots in sorted(named.items()):
        name = NAMES.get(cid, "?")
        parts.append(f"cid 0x{cid:02X}({name}) s{','.join(map(str, slots))}")
    for job, slots in sorted(generic_jobs.items()):
        parts.append(f"job {job} s{','.join(map(str, slots))}")
    return "; ".join(parts)


def report(entries: list[int]) -> None:
    vanilla = (VANILLA_DIR / "battle_entd4_ent.bin").read_bytes()
    modded = MODDED_ENTD4.read_bytes()
    print(f"{'entry':>5} {'van total':>9} {'mod total':>9} {'net':>4}  risk")
    for e in entries:
        vn, vj, _ = analyze_entry(vanilla, e)
        mn, mj, _ = analyze_entry(modded, e)
        van_total = len(vn) + len(vj)
        mod_total = len(mn) + len(mj)
        net = mod_total - van_total
        new_named = set(mn) - set(vn)
        new_jobs = set(mj) - set(vj)
        removed = (set(vn) - set(mn), set(vj) - set(mj))
        risk = ""
        if net >= 2:
            risk = "RED (Zeirchele-proven corruption pattern)"
        elif net == 1 and len(mn) >= 3:
            risk = "watch (net +1 on a special-heavy battle; Zeirchele-class)"
        print(f"{e:>5} {van_total:>9} {mod_total:>9} {net:>+4}  {risk}")
        if new_named or new_jobs:
            adds = describe({c: mn[c] for c in new_named},
                            {j: mj[j] for j in new_jobs})
            print(f"       adds: {adds}")
        if removed[0] or removed[1]:
            rem = ", ".join([f"cid 0x{c:02X}" for c in sorted(removed[0])]
                            + [f"job {j}" for j in sorted(removed[1])])
            print(f"       removes: {rem}")


def report_vanilla_all() -> None:
    for i in (1, 2, 3, 4):
        data = (VANILLA_DIR / f"battle_entd{i}_ent.bin").read_bytes()
        for local in range(128):
            e = (i - 1) * 128 + local
            named, jobs, _ = analyze_entry(data, e)
            total = len(named) + len(jobs)
            if total == 0:
                continue
            print(f"e{e:03d} sheets={total:2d} named={len(named)} jobs={len(jobs)}  "
                  f"{describe(named, jobs)}")


def main() -> None:
    args = sys.argv[1:]
    if args and args[0] == "--all-vanilla":
        report_vanilla_all()
        return
    entries = [int(a) for a in args] if args else [403, 404, 405, 407, 409, 410, 411, 413, 414, 415, 425]
    report(entries)


if __name__ == "__main__":
    main()
