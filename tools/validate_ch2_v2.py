#!/usr/bin/env python3
"""Validate the implemented Chapter 2 v2 battle redesign data.

This is an objective binary/data validator for docs/battles/012-022. It checks the
embedded ENTD that the code mod ships and the Merchant Dorter event script override.
It does not judge balance; in-game balance remains a playtest task.
"""

from __future__ import annotations

from pathlib import Path


ENTRY = 0x280
SLOT = 0x28
ENTD = Path("src/fftivc.battles.ngplus/entd/battle_entd4_ent.bin")
VANILLA_ENTD = Path("extracted/enhanced_0002_selected/fftpack/battle_entd4_ent.bin")
EVENT119 = Path("src/fftivc.battles.ngplus/FFTIVC/data/enhanced/script/enhanced/event119.e")
EVENT140 = Path("src/fftivc.battles.ngplus/FFTIVC/data/enhanced/script/enhanced/event140.e")
ROOT_NXL = Path("src/fftivc.battles.ngplus/FFTIVC/data/enhanced/nxd/root.nxl")


def slot(data: bytes, entry: int, slot_no: int) -> bytes:
    offset = (entry % 128) * ENTRY + slot_no * SLOT
    return data[offset : offset + SLOT]


def field(data: bytes, entry: int, slot_no: int, offset: int) -> int:
    return slot(data, entry, slot_no)[offset]


def field16(data: bytes, entry: int, slot_no: int, offset: int) -> int:
    row = slot(data, entry, slot_no)
    return int.from_bytes(row[offset : offset + 2], "little")


def roster(data: bytes, entry: int, slots: list[int], offset: int) -> list[int]:
    return [field(data, entry, slot_no, offset) for slot_no in slots]


def rank(job: int) -> int:
    return job - 0x4A


def run() -> int:
    entd = ENTD.read_bytes()
    vanilla = VANILLA_ENTD.read_bytes()
    event119 = EVENT119.read_bytes()
    event140 = EVENT140.read_bytes()
    root_nxl = ROOT_NXL.read_text(encoding="utf-8")
    checks: list[tuple[str, bool]] = []

    def check(name: str, condition: bool) -> None:
        checks.append((name, condition))

    # Merchant Dorter, event-spawned slot-add reference case.
    check(
        "403 Merchant Knight slot s9 uid 0x86",
        field(entd, 403, 9, 0x0A) == 76 and field(entd, 403, 9, 0x20) == 0x86,
    )
    check(
        "403 Merchant roster jobs",
        roster(entd, 403, [1, 4, 5, 6, 7, 8, 9], 0x0A)
        == [83, 77, 77, 83, 80, 80, 76],
    )
    check(
        "403 Merchant roster levels",
        roster(entd, 403, [1, 4, 5, 6, 7, 8, 9], 0x03)
        == [100, 101, 100, 100, 102, 101, 102],
    )
    check("403 Merchant Knight jobrank", field(entd, 403, 9, 0x08) == rank(76))
    check("event119 has one 45 86 00 01 registration", event119.count(bytes.fromhex("45 86 00 01")) == 1)
    check("event119 has one 5f 86 00 choreography marker", event119.count(bytes.fromhex("5f 86 00")) == 1)
    check("event119 source size 0x779", len(event119) == 0x779)

    # Generic human job-rank seeds should match the visible job for re-jobbed/tuned Ch2 generics.
    for entry, slots in {
        405: [4, 5, 6, 7, 8, 11],
        407: [1, 2, 3, 4, 5, 6, 8],
        409: [2, 3, 4, 5, 6, 7, 8],
        411: [2, 3, 5, 6, 7, 8, 9],
        413: [1, 2, 3, 4, 5, 6, 7],
        414: [1, 2, 3, 4, 5, 6, 7],
        415: [1, 2, 3, 4, 5, 6],
    }.items():
        for slot_no in slots:
            job = field(entd, entry, slot_no, 0x0A)
            if 74 <= job <= 89:
                actual = field(entd, entry, slot_no, 0x08)
                check(f"{entry} s{slot_no} jobrank {actual} == job {job}-0x4a", actual == rank(job))

    check(
        "404 Boco level/control",
        field(entd, 404, 0, 0x03) == 100 and (field(entd, 404, 0, 0x18) & 0x08) != 0,
    )
    check("404 roster jobs", roster(entd, 404, [1, 2, 3, 4, 5, 6, 9], 0x0A) == [98, 98, 99, 99, 98, 98, 104])
    check("404 roster levels", roster(entd, 404, [1, 2, 3, 4, 5, 6, 9], 0x03) == [100, 100, 101, 102, 100, 100, 101])
    check("405 intro corpse s2 untouched", slot(entd, 405, 2) == slot(vanilla, 405, 2))
    check("405 intro corpse s3 untouched", slot(entd, 405, 3) == slot(vanilla, 405, 3))
    check("405 white mage low slot s7", field(entd, 405, 7, 0x0A) == 79 and field(entd, 405, 7, 0x20) == 0x85)
    check("405 extra knight slot s11 uid 0x87", field(entd, 405, 11, 0x0A) == 76 and field(entd, 405, 11, 0x20) == 0x87)
    check("405 single new sheet: s8 reverted to Knight", field(entd, 405, 8, 0x0A) == 76)
    check("405 s8 crossbow-knight kit", field16(entd, 405, 8, 0x0C) == 449 and field16(entd, 405, 8, 0x0E) == 469 and field16(entd, 405, 8, 0x10) == 486 and roster(entd, 405, [8], 0x12) == [154] and roster(entd, 405, [8], 0x13) == [184] and roster(entd, 405, [8], 0x14) == [218] and roster(entd, 405, [8], 0x15) == [82] and roster(entd, 405, [8], 0x16) == [139])
    check("405 enemy levels", roster(entd, 405, [0, 4, 5, 6, 7, 8, 11], 0x03) == [103, 102, 101, 101, 101, 101, 100])
    check("405 knight/extra-knight placement polish", (field(entd, 405, 8, 0x19), field(entd, 405, 8, 0x1A), field(entd, 405, 11, 0x19), field(entd, 405, 11, 0x1A)) == (5, 9, 3, 9))
    check("405 white mage high-ground placement", (field(entd, 405, 7, 0x19), field(entd, 405, 7, 0x1A)) == (6, 8))
    check("OverrideEntryData row count updated for 405/s11, 407/s8, 409/s8, and 410/s9", "overrideentrydata,96,521,3" in root_nxl)
    check("407 second dragoon", field(entd, 407, 8, 0x0A) == 87 and field(entd, 407, 8, 0x20) == 0x86)
    check("407 second dragoon placement", (field(entd, 407, 8, 0x19), field(entd, 407, 8, 0x1A)) == (0, 10))
    # Zaland's enemies are script-managed (0xD0 + event140.e AddUnit); the added s8 mirrors its
    # siblings: 0xD0 in the ENTD plus registration/choreography in event140.e
    # (tools/patch_event140_zaland.py). 0xD0 without the script patch never materializes;
    # 0x90 materializes but stays outside the intro choreography (both playtested 2026-07-02).
    check("407 s8 flags 0xD0 (script-managed, like siblings)", field(entd, 407, 8, 0x18) == 0xD0)
    check("event140 has one 45 86 00 01 registration", event140.count(bytes.fromhex("45860001")) == 1)
    check("event140 has one 5f 86 00 warp to (0,10)", event140.count(bytes.fromhex("5f8600000a0000")) == 1)
    check("event140 has alert+idle poses for uid 0x86",
          event140.count(bytes.fromhex("118600030000")) == 1
          and event140.count(bytes.fromhex("118600020000")) == 1)
    check("event140 patched size 0x581", len(event140) == 0x581)
    check("407 levels", roster(entd, 407, [1, 2, 3, 4, 5, 6, 8], 0x03) == [101, 102, 101, 102, 101, 100, 101])
    check("409 chemist slot", field(entd, 409, 8, 0x0A) == 75 and field(entd, 409, 8, 0x20) == 0x86)
    check("409 chemist placement", (field(entd, 409, 8, 0x19), field(entd, 409, 8, 0x1A)) == (13, 4))
    check("409 levels", roster(entd, 409, [2, 3, 4, 5, 6, 7, 8], 0x03) == [101, 101, 100, 102, 101, 101, 101])
    check("410 second bonesnatch", field(entd, 410, 9, 0x0A) == 110 and field(entd, 410, 9, 0x20) == 0x86)
    check("410 monster jobs", roster(entd, 410, [1, 2, 3, 4, 5, 6, 7, 9], 0x0A) == [110, 109, 109, 112, 112, 115, 130, 110])
    check("411 roles", roster(entd, 411, [2, 3, 5, 6, 7, 8, 9], 0x0A) == [81, 83, 77, 77, 82, 82, 83])
    check("411 levels", roster(entd, 411, [2, 3, 5, 6, 7, 8, 9], 0x03) == [102, 101, 101, 100, 102, 101, 100])
    check("413 geomancer slot", field(entd, 413, 7, 0x0A) == 86 and field(entd, 413, 7, 0x20) == 0x86)
    check("413 levels", roster(entd, 413, [1, 2, 3, 4, 5, 6, 7], 0x03) == [101, 101, 100, 100, 102, 101, 101])
    check("414 gallows levels", roster(entd, 414, [0, 1, 2, 3, 4, 5, 6, 7], 0x03) == [103, 101, 102, 101, 101, 100, 102, 101])
    check("415 gate levels", roster(entd, 415, [0, 1, 2, 3, 4, 5, 6], 0x03) == [103, 101, 100, 102, 101, 101, 102])
    check("415 blood sword equipped", field(entd, 415, 0, 0x15) == 23)
    check(
        "425 Cuchulainn tune + 108 Gems spoil",
        field(entd, 425, 9, 0x03) == 104
        and field(entd, 425, 9, 0x09) == 8
        and field(entd, 425, 9, 0x06) == 88
        and field(entd, 425, 9, 0x07) == 82
        and field(entd, 425, 9, 0x1E) == 226,
    )

    passed = 0
    for name, ok in checks:
        if ok:
            passed += 1
        print(f"{'PASS' if ok else 'FAIL'} - {name}")
    print()
    print(f"{passed}/{len(checks)} checks passed")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(run())
