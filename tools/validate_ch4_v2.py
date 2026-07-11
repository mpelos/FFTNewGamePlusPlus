#!/usr/bin/env python3
"""Validate implemented Chapter 4 v2 battle data.

This is an objective binary/source validator for docs/battles/038-058. It should grow one battle at
a time as each Chapter 4 redesign is implemented. It does not judge balance; in-game balance remains
a playtest task.
"""

from __future__ import annotations

from pathlib import Path


ENTRY = 0x280
SLOT = 0x28
ENTD = Path("src/fftivc.battles.ngplus/entd/battle_entd4_ent.bin")


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


def run() -> int:
    entd = ENTD.read_bytes()
    checks: list[tuple[str, bool]] = []

    def check(name: str, condition: bool) -> None:
        checks.append((name, condition))

    # 038 - Dugeura Pass, entry 442.
    # v3 six-body Chapter 4 opener: Samurai parry screen, 2 Black Mages,
    # Geomancer terrain bruiser, 2 Dragoons.
    e = 442
    active = [0, 1, 2, 3, 4, 5]
    check("442 active jobs", roster(entd, e, active, 0x0A) == [88, 80, 86, 80, 87, 87])
    check("442 active levels", roster(entd, e, active, 0x03) == [101, 102, 102, 102, 102, 101])
    check("442 active job ranks", roster(entd, e, active, 0x08) == [14, 6, 12, 6, 13, 13])
    check("442 active job levels", roster(entd, e, active, 0x09) == [8, 8, 8, 8, 8, 8])
    check("442 active secondaries", roster(entd, e, active, 0x0B) == [17, 10, 9, 12, 9, 9])
    check("442 Brave targets", roster(entd, e, active, 0x06) == [88, 60, 84, 60, 86, 86])
    check("442 Faith targets", roster(entd, e, active, 0x07) == [60, 84, 60, 84, 40, 40])

    check("442 s0 Samurai R/S/M",
          field16(entd, e, 0, 0x0C) == 451
          and field16(entd, e, 0, 0x0E) == 476
          and field16(entd, e, 0, 0x10) == 487)
    check("442 s0 Samurai gear",
          roster(entd, e, [0], 0x12) == [154]
          and roster(entd, e, [0], 0x13) == [182]
          and roster(entd, e, [0], 0x14) == [217]
          and roster(entd, e, [0], 0x15) == [45]
          and roster(entd, e, [0], 0x16) == [254])

    for slot_no in (1, 3):
        check(f"442 s{slot_no} Black Mage R/S/M",
              field16(entd, e, slot_no, 0x0C) == 445
              and field16(entd, e, slot_no, 0x0E) == 482
              and field16(entd, e, slot_no, 0x10) == 494)
        check(f"442 s{slot_no} Black Mage gear",
              roster(entd, e, [slot_no], 0x12) == [167]
              and roster(entd, e, [slot_no], 0x13) == [205]
              and roster(entd, e, [slot_no], 0x14) == [170]
              and roster(entd, e, [slot_no], 0x15) == [56]
              and roster(entd, e, [slot_no], 0x16) == [255])

    check("442 s1/s3 Black Mage secondaries", roster(entd, e, [1, 3], 0x0B) == [10, 12])

    check("442 s2 Geomancer R/S/M",
          field16(entd, e, 2, 0x0C) == 437
          and field16(entd, e, 2, 0x0E) == 465
          and field16(entd, e, 2, 0x10) == 487)
    check("442 s2 Geomancer gear",
          roster(entd, e, [2], 0x12) == [168]
          and roster(entd, e, [2], 0x13) == [195]
          and roster(entd, e, [2], 0x14) == [214]
          and roster(entd, e, [2], 0x15) == [30]
          and roster(entd, e, [2], 0x16) == [255])

    for slot_no in (4, 5):
        check(f"442 s{slot_no} Dragoon R/S/M",
              field16(entd, e, slot_no, 0x0C) == 427
              and field16(entd, e, slot_no, 0x0E) == 465
              and field16(entd, e, slot_no, 0x10) == 492)
        check(f"442 s{slot_no} Dragoon gear",
              roster(entd, e, [slot_no], 0x12) == [154]
              and roster(entd, e, [slot_no], 0x13) == [182]
              and roster(entd, e, [slot_no], 0x14) == [213]
              and roster(entd, e, [slot_no], 0x15) == [103]
              and roster(entd, e, [slot_no], 0x16) == [255])

    check("442 reward spoils preserved", roster(entd, e, active, 0x1E) == [0, 58, 179, 0, 0, 0])

    # 039 - Free City of Bervenia, entry 443.
    # v3 keeps six enemies: Meliadoul break-duel, two Archers, two Summoners, one Monk flanker.
    e = 443
    active = [0, 1, 2, 3, 4, 5]
    check("443 active jobs", roster(entd, e, active, 0x0A) == [47, 82, 77, 77, 82, 78])
    check("443 active levels", roster(entd, e, active, 0x03) == [104, 102, 102, 102, 102, 102])
    check("443 active job levels", roster(entd, e, active, 0x09) == [8, 8, 8, 8, 8, 8])
    check("443 active secondaries", roster(entd, e, active, 0x0B) == [5, 10, 6, 6, 12, 6])
    check("443 Brave targets", roster(entd, e, active, 0x06) == [88, 60, 88, 88, 60, 90])
    check("443 Faith targets", roster(entd, e, active, 0x07) == [78, 84, 55, 55, 84, 35])

    check("443 Meliadoul boss R/S/M and gear",
          field16(entd, e, 0, 0x0C) == 442
          and field16(entd, e, 0, 0x0E) == 468
          and field16(entd, e, 0, 0x10) == 487
          and roster(entd, e, [0], 0x12) == [154]
          and roster(entd, e, [0], 0x13) == [184]
          and roster(entd, e, [0], 0x15) == [34]
          and roster(entd, e, [0], 0x16) == [139])

    for slot_no in (1, 4):
        check(f"443 s{slot_no} Summoner R/S/M",
              field16(entd, e, slot_no, 0x0C) == 446
              and field16(entd, e, slot_no, 0x0E) == 482
              and field16(entd, e, slot_no, 0x10) == 487)
        check(f"443 s{slot_no} Summoner gear",
              roster(entd, e, [slot_no], 0x12) == [167]
              and roster(entd, e, [slot_no], 0x13) == [202]
              and roster(entd, e, [slot_no], 0x14) == [234]
              and roster(entd, e, [slot_no], 0x15) == [56]
              and roster(entd, e, [slot_no], 0x16) == [255])

    for slot_no in (2, 3):
        check(f"443 s{slot_no} Archer R/S/M",
              field16(entd, e, slot_no, 0x0C) == 449
              and field16(entd, e, slot_no, 0x0E) == 474
              and field16(entd, e, slot_no, 0x10) == 492)
        check(f"443 s{slot_no} Archer gear",
              roster(entd, e, [slot_no], 0x12) == [168]
              and roster(entd, e, [slot_no], 0x13) == [198]
              and roster(entd, e, [slot_no], 0x14) == [218]
              and roster(entd, e, [slot_no], 0x15) == [87]
              and roster(entd, e, [slot_no], 0x16) == [254])

    check("443 s5 Monk R/S/M",
          field16(entd, e, 5, 0x0C) == 442
          and field16(entd, e, 5, 0x0E) == 477
          and field16(entd, e, 5, 0x10) == 487)
    check("443 s5 Monk gear",
          roster(entd, e, [5], 0x12) == [255]
          and roster(entd, e, [5], 0x13) == [198]
          and roster(entd, e, [5], 0x14) == [218]
          and roster(entd, e, [5], 0x15) == [255]
          and roster(entd, e, [5], 0x16) == [255])
    check("443 reward spoils preserved", roster(entd, e, active, 0x1E) == [0, 0, 0, 225, 252, 34])

    # 040 - Finnath Creek, entry 444.
    # De-randomized v3 flock: 2 Red Chocobo, 2 yellow Chocobo, 1 Black Chocobo, 1 Wild Boar.
    e = 444
    cleared = [0, 1, 2, 3, 4, 5]
    active = [6, 7, 8, 9, 10, 11]
    check("444 old variant records cleared", roster(entd, e, cleared, 0x20) == [255, 255, 255, 255, 255, 255])
    check("444 fixed flock jobs", roster(entd, e, active, 0x0A) == [96, 96, 94, 94, 95, 123])
    check("444 fixed flock levels", roster(entd, e, active, 0x03) == [102, 102, 101, 101, 101, 100])
    check("444 fixed flock job levels", roster(entd, e, active, 0x09) == [8, 8, 8, 8, 8, 8])
    check("444 fixed flock Brave", roster(entd, e, active, 0x06) == [90, 90, 90, 90, 90, 60])
    check("444 fixed flock Faith", roster(entd, e, active, 0x07) == [30, 30, 30, 30, 30, 40])
    check("444 fixed flock control flags", roster(entd, e, active, 0x18) == [0x90, 0x90, 0x90, 0x90, 0x90, 0x90])
    check("444 fixed flock unit ids", roster(entd, e, active, 0x20) == [0x80, 0x81, 0x82, 0x83, 0x84, 0x85])
    check("444 no equipment spoils", roster(entd, e, active, 0x1E) == [0, 0, 0, 0, 0, 0])

    # 041 - Outlying Church, entry 445.
    # Zalmo focus fight; current test seeds secondary-job buckets at JL8 and palettes Knights A/B/C.
    e = 445
    active = [1, 2, 3, 4, 5, 6]
    check("445 inactive placeholder preserved",
          field(entd, e, 0, 0x03) == 254
          and field(entd, e, 0, 0x0A) == 5
          and field(entd, e, 0, 0x18) == 0x84)
    check("445 active jobs", roster(entd, e, active, 0x0A) == [16, 85, 85, 76, 76, 76])
    check("445 active levels", roster(entd, e, active, 0x03) == [104, 102, 102, 102, 102, 101])
    check("445 active job unlock buckets", roster(entd, e, active, 0x08) == [11, 16, 16, 4, 4, 4])
    check("445 active job levels", roster(entd, e, active, 0x09) == [8, 8, 8, 8, 8, 8])
    check("445 active secondaries", roster(entd, e, active, 0x0B) == [16, 11, 11, 9, 9, 9])
    check("445 Brave targets", roster(entd, e, active, 0x06) == [72, 68, 72, 88, 88, 88])
    check("445 Faith targets", roster(entd, e, active, 0x07) == [82, 78, 82, 42, 42, 42])
    check("445 Knight palette restored", roster(entd, e, [4, 5, 6], 0x17) == [4, 4, 4])
    check("445 Knight sprite restored", roster(entd, e, [4, 5, 6], 0x00) == [128, 128, 128])

    check("445 Zalmo R/S/M and gear",
          field16(entd, e, 1, 0x0C) == 449
          and field16(entd, e, 1, 0x0E) == 466
          and field16(entd, e, 1, 0x10) == 487
          and roster(entd, e, [1], 0x12) == [167]
          and roster(entd, e, [1], 0x13) == [206]
          and roster(entd, e, [1], 0x14) == [239]
          and roster(entd, e, [1], 0x15) == [114]
          and roster(entd, e, [1], 0x16) == [254])

    for slot_no in (2, 3):
        check(f"445 s{slot_no} Mystic R/S/M",
              field16(entd, e, slot_no, 0x0C) == 445
              and field16(entd, e, slot_no, 0x0E) == 482
              and field16(entd, e, slot_no, 0x10) == 494)
        check(f"445 s{slot_no} Mystic gear",
              roster(entd, e, [slot_no], 0x12) == [167]
              and roster(entd, e, [slot_no], 0x13) == [205]
              and roster(entd, e, [slot_no], 0x14) == [217]
              and roster(entd, e, [slot_no], 0x15) == [56]
              and roster(entd, e, [slot_no], 0x16) == [255])

    for slot_no in (4, 5, 6):
        check(f"445 s{slot_no} Knight R/S/M",
              field16(entd, e, slot_no, 0x0C) == 453
              and field16(entd, e, slot_no, 0x0E) == 465
              and field16(entd, e, slot_no, 0x10) == 487)
        check(f"445 s{slot_no} Knight gear",
              roster(entd, e, [slot_no], 0x12) == [154]
              and roster(entd, e, [slot_no], 0x13) == [182]
              and roster(entd, e, [slot_no], 0x14) == [216]
              and roster(entd, e, [slot_no], 0x15) == [30]
              and roster(entd, e, [slot_no], 0x16) == [139])
    check("445 reward spoils preserved", roster(entd, e, active, 0x1E) == [223, 206, 0, 0, 0, 0])

    # 042 - Beddha Sandwaste / Bed Desert, entry 447.
    # Six active enemies plus two Barich script placeholders. v3 keeps the gun duel focused on Barich.
    e = 447
    active = [0, 1, 2, 3, 4, 5]
    check("447 active jobs", roster(entd, e, active, 0x0A) == [43, 88, 88, 80, 86, 86])
    check("447 active levels", roster(entd, e, active, 0x03) == [104, 102, 102, 102, 102, 101])
    check("447 active job ranks", roster(entd, e, active, 0x08) == [0, 14, 14, 6, 12, 12])
    check("447 active job levels", roster(entd, e, active, 0x09) == [8, 8, 8, 8, 8, 8])
    check("447 active secondaries", roster(entd, e, active, 0x0B) == [0, 9, 9, 6, 6, 6])
    check("447 Brave targets", roster(entd, e, active, 0x06) == [84, 88, 88, 60, 84, 84])
    check("447 Faith targets", roster(entd, e, active, 0x07) == [55, 60, 60, 84, 60, 60])

    check("447 Barich boss R/S/M and Stoneshooter",
          field16(entd, e, 0, 0x0C) == 449
          and field16(entd, e, 0, 0x0E) == 466
          and field16(entd, e, 0, 0x10) == 491
          and roster(entd, e, [0], 0x12) == [168]
          and roster(entd, e, [0], 0x13) == [198]
          and roster(entd, e, [0], 0x14) == [234]
          and roster(entd, e, [0], 0x15) == [73]
          and roster(entd, e, [0], 0x16) == [254])

    for slot_no in (1, 2):
        check(f"447 s{slot_no} Samurai R/S/M",
              field16(entd, e, slot_no, 0x0C) == 451
              and field16(entd, e, slot_no, 0x0E) == 476
              and field16(entd, e, slot_no, 0x10) == 488)
        check(f"447 s{slot_no} Samurai gear",
              roster(entd, e, [slot_no], 0x12) == [154]
              and roster(entd, e, [slot_no], 0x13) == [182]
              and roster(entd, e, [slot_no], 0x14) == [215]
              and roster(entd, e, [slot_no], 0x15) == [45]
              and roster(entd, e, [slot_no], 0x16) == [254])

    check("447 s3 Black Mage R/S/M",
          field16(entd, e, 3, 0x0C) == 449
          and field16(entd, e, 3, 0x0E) == 467
          and field16(entd, e, 3, 0x10) == 486)
    check("447 s3 Black Mage gear",
          roster(entd, e, [3], 0x12) == [167]
          and roster(entd, e, [3], 0x13) == [205]
          and roster(entd, e, [3], 0x14) == [234]
          and roster(entd, e, [3], 0x15) == [56]
          and roster(entd, e, [3], 0x16) == [255])

    for slot_no in (4, 5):
        check(f"447 s{slot_no} Geomancer R/S/M",
              field16(entd, e, slot_no, 0x0C) == 437
              and field16(entd, e, slot_no, 0x0E) == 465
              and field16(entd, e, slot_no, 0x10) == 487)
        check(f"447 s{slot_no} Geomancer gear",
              roster(entd, e, [slot_no], 0x12) == [167]
              and roster(entd, e, [slot_no], 0x13) == [195]
              and roster(entd, e, [slot_no], 0x14) == [217]
              and roster(entd, e, [slot_no], 0x15) == [30]
              and roster(entd, e, [slot_no], 0x16) == [255])

    check("447 Barich placeholders preserved",
          roster(entd, e, [6, 7], 0x0A) == [43, 43]
          and roster(entd, e, [6, 7], 0x09) == [0, 0]
          and roster(entd, e, [6, 7], 0x18) == [0xD0, 0xD0]
          and roster(entd, e, [6, 7], 0x20) == [0x85, 0x86])
    check("447 guaranteed gun spoils preserved", roster(entd, e, active, 0x1E) == [74, 75, 76, 0, 0, 0])

    # 043 - Fort Besselat Wall, entries 448 South / 449 North.
    # Branching wall assault: South melee/stealth, North ranged/AoE. Both paths pay the same bow rewards.
    e = 448
    active = [0, 1, 2, 3, 4, 5, 6]
    check("448 South v3 active jobs", roster(entd, e, active, 0x0A) == [76, 76, 76, 80, 80, 89, 78])
    check("448 South v3 active levels", roster(entd, e, active, 0x03) == [101, 102, 102, 102, 101, 102, 101])
    check("448 South v3 job buckets", roster(entd, e, active, 0x08) == [2, 14, 14, 6, 6, 15, 4])
    check("448 South v3 job levels", roster(entd, e, active, 0x09) == [8, 8, 8, 0, 0, 8, 8])
    check("448 South v3 secondaries", roster(entd, e, active, 0x0B) == [0x21, 8, 8, 0, 0, 9, 0])
    check("448 South v3 Brave targets", roster(entd, e, active, 0x06) == [88, 88, 88, 62, 62, 90, 88])
    check("448 South v3 Faith targets", roster(entd, e, active, 0x07) == [42, 42, 42, 84, 84, 35, 38])

    check("448 s0 Knight Leader Holy Sword kit",
          field16(entd, e, 0, 0x0C) == 442
          and field16(entd, e, 0, 0x0E) == 465
          and field16(entd, e, 0, 0x10) == 488
          and roster(entd, e, [0], 0x12) == [154]
          and roster(entd, e, [0], 0x13) == [182]
          and roster(entd, e, [0], 0x14) == [218]
          and roster(entd, e, [0], 0x15) == [33]
          and roster(entd, e, [0], 0x16) == [139])

    for slot_no in (1, 2):
        check(f"448 s{slot_no} Samurai wall kit",
              field16(entd, e, slot_no, 0x0C) == 427
              and field16(entd, e, slot_no, 0x0E) == 466
              and field16(entd, e, slot_no, 0x10) == 488
              and roster(entd, e, [slot_no], 0x12) == [154]
              and roster(entd, e, [slot_no], 0x13) == [184]
              and roster(entd, e, [slot_no], 0x14) == [218]
              and roster(entd, e, [slot_no], 0x15) == [82]
              and roster(entd, e, [slot_no], 0x16) == [139])

    for slot_no, gun in ((3, 74), (4, 76)):
        check(f"448 s{slot_no} Black Mage gun kit",
              field16(entd, e, slot_no, 0x0C) == 449
              and field16(entd, e, slot_no, 0x0E) == 461
              and field16(entd, e, slot_no, 0x10) == 498
              and field(entd, e, slot_no, 0x15) == gun
              and roster(entd, e, [slot_no], 0x12) == [167]
              and roster(entd, e, [slot_no], 0x13) == [202]
              and roster(entd, e, [slot_no], 0x14) == [217]
              and roster(entd, e, [slot_no], 0x16) == [254])

    check("448 s5 Ninja Martial Arts kit",
          field16(entd, e, 5, 0x0C) == 442
          and field16(entd, e, 5, 0x0E) == 472
          and field16(entd, e, 5, 0x10) == 491
          and roster(entd, e, [5], 0x12) == [168]
          and roster(entd, e, [5], 0x13) == [195]
          and roster(entd, e, [5], 0x14) == [218]
          and roster(entd, e, [5], 0x15) == [255]
          and roster(entd, e, [5], 0x16) == [255])
    check("448 s6 Monk flanker kit",
          field16(entd, e, 6, 0x0C) == 442
          and field16(entd, e, 6, 0x0E) == 477
          and field16(entd, e, 6, 0x10) == 491
          and roster(entd, e, [6], 0x12) == [170]
          and roster(entd, e, [6], 0x13) == [195]
          and roster(entd, e, [6], 0x14) == [218]
          and roster(entd, e, [6], 0x15) == [255]
          and roster(entd, e, [6], 0x16) == [255])
    check("448 bow spoils preserved",
          field(entd, e, 3, 0x1E) == 90
          and field(entd, e, 4, 0x1E) == 91)

    e = 449
    active = [0, 1, 2, 3, 4, 5]
    check("449 North v3 active jobs", roster(entd, e, active, 0x0A) == [76, 86, 86, 80, 82, 76])
    check("449 North v3 active levels", roster(entd, e, active, 0x03) == [102, 102, 101, 101, 102, 102])
    check("449 North v3 job buckets", roster(entd, e, active, 0x08) == [4, 12, 12, 6, 8, 4])
    check("449 North v3 job levels", roster(entd, e, active, 0x09) == [8, 8, 8, 0, 8, 8])
    check("449 North v3 secondaries", roster(entd, e, active, 0x0B) == [0x21, 0, 0, 0, 12, 9])
    check("449 North v3 Brave targets", roster(entd, e, active, 0x06) == [88, 86, 86, 62, 60, 88])
    check("449 North v3 Faith targets", roster(entd, e, active, 0x07) == [42, 40, 40, 84, 84, 40])

    check("449 s0 Knight Leader Holy Sword kit",
          field16(entd, e, 0, 0x0C) == 442
          and field16(entd, e, 0, 0x0E) == 465
          and field16(entd, e, 0, 0x10) == 488
          and roster(entd, e, [0], 0x12) == [154]
          and roster(entd, e, [0], 0x13) == [182]
          and roster(entd, e, [0], 0x14) == [218]
          and roster(entd, e, [0], 0x15) == [33]
          and roster(entd, e, [0], 0x16) == [139])

    for slot_no in (1, 2):
        check(f"449 s{slot_no} Geomancer MA kit",
              field16(entd, e, slot_no, 0x0C) == 437
              and field16(entd, e, slot_no, 0x0E) == 467
              and field16(entd, e, slot_no, 0x10) == 487
              and roster(entd, e, [slot_no], 0x12) == [167]
              and roster(entd, e, [slot_no], 0x13) == [202]
              and roster(entd, e, [slot_no], 0x14) == [226]
              and roster(entd, e, [slot_no], 0x15) == [30]
              and roster(entd, e, [slot_no], 0x16) == [136])

    check("449 s3 Black Mage shooter kit",
          field16(entd, e, 3, 0x0C) == 449
          and field16(entd, e, 3, 0x0E) == 461
          and field16(entd, e, 3, 0x10) == 498
          and roster(entd, e, [3], 0x12) == [167]
          and roster(entd, e, [3], 0x13) == [202]
          and roster(entd, e, [3], 0x14) == [217]
          and roster(entd, e, [3], 0x15) == [75]
          and roster(entd, e, [3], 0x16) == [254])
    check("449 s0/s3 position swap preserves talk slot",
          (field(entd, e, 0, 0x19), field(entd, e, 0, 0x1A),
           field(entd, e, 3, 0x19), field(entd, e, 3, 0x1A)) == (7, 4, 9, 7))
    check("449 s4 Summoner Time Magic kit",
          field16(entd, e, 4, 0x0C) == 446
          and field16(entd, e, 4, 0x0E) == 482
          and field16(entd, e, 4, 0x10) == 487
          and roster(entd, e, [4], 0x12) == [167]
          and roster(entd, e, [4], 0x13) == [202]
          and roster(entd, e, [4], 0x14) == [234]
          and roster(entd, e, [4], 0x15) == [56]
          and roster(entd, e, [4], 0x16) == [255])
    check("449 s5 Knight Martial Arts kit",
          field16(entd, e, 5, 0x0C) == 453
          and field16(entd, e, 5, 0x0E) == 477
          and field16(entd, e, 5, 0x10) == 488
          and roster(entd, e, [5], 0x12) == [154]
          and roster(entd, e, [5], 0x13) == [182]
          and roster(entd, e, [5], 0x14) == [218]
          and roster(entd, e, [5], 0x15) == [30]
          and roster(entd, e, [5], 0x16) == [30])
    check("449 bow spoils preserved",
          field(entd, e, 0, 0x1E) == 90
          and field(entd, e, 3, 0x1E) == 91)

    # 044 - Fort Besselat Sluice Gate v3, entry 450.
    # Lever objective race: 2 Summon Black Mages, 2 lever Knights, 2 battle Samurais, 2 Geomancers.
    e = 450
    active = [0, 1, 2, 3, 4, 5, 6, 7]
    check("450 v3 active jobs", roster(entd, e, active, 0x0A) == [86, 86, 88, 88, 80, 80, 76, 76])
    check("450 active levels", roster(entd, e, active, 0x03) == [100, 100, 100, 100, 100, 100, 102, 102])
    check("450 v3 job buckets", roster(entd, e, active, 0x08) == [12, 12, 14, 14, 8, 8, 14, 14])
    check("450 active job levels", roster(entd, e, active, 0x09) == [8] * 8)
    check("450 v3 secondaries", roster(entd, e, active, 0x0B) == [0, 0, 0, 0, 13, 13, 8, 8])
    check("450 Brave targets", roster(entd, e, active, 0x06) == [82, 82, 88, 88, 60, 60, 88, 88])
    check("450 Faith targets", roster(entd, e, active, 0x07) == [45, 45, 42, 42, 84, 84, 42, 42])

    for slot_no in (0, 1):
        check(f"450 s{slot_no} Geomancer R/S/M",
              field16(entd, e, slot_no, 0x0C) == 451
              and field16(entd, e, slot_no, 0x0E) == 467
              and field16(entd, e, slot_no, 0x10) == 487)
        check(f"450 s{slot_no} Geomancer gear",
              roster(entd, e, [slot_no], 0x12) == [167]
              and roster(entd, e, [slot_no], 0x13) == [202]
              and roster(entd, e, [slot_no], 0x14) == [226]
              and roster(entd, e, [slot_no], 0x15) == [30]
              and roster(entd, e, [slot_no], 0x16) == [139])

    for slot_no in (6, 7):
        check(f"450 s{slot_no} lever Knight R/S/M",
              field16(entd, e, slot_no, 0x0C) == 449
              and field16(entd, e, slot_no, 0x0E) == 466
              and field16(entd, e, slot_no, 0x10) == 487)
        check(f"450 s{slot_no} lever Knight gear",
              roster(entd, e, [slot_no], 0x12) == [154]
              and roster(entd, e, [slot_no], 0x13) == [184]
              and roster(entd, e, [slot_no], 0x14) == [218]
              and roster(entd, e, [slot_no], 0x15) == [82]
              and roster(entd, e, [slot_no], 0x16) == [139])

    for slot_no in (4, 5):
        check(f"450 s{slot_no} Summon Black Mage R/S/M",
              field16(entd, e, slot_no, 0x0C) == 449
              and field16(entd, e, slot_no, 0x0E) == 482
              and field16(entd, e, slot_no, 0x10) == 487)
        check(f"450 s{slot_no} Summon Black Mage gear",
              roster(entd, e, [slot_no], 0x12) == [167]
              and roster(entd, e, [slot_no], 0x13) == [205]
              and roster(entd, e, [slot_no], 0x14) == [234]
              and roster(entd, e, [slot_no], 0x15) == [56]
              and roster(entd, e, [slot_no], 0x16) == [255])

    for slot_no in (2, 3):
        check(f"450 s{slot_no} battle Samurai R/S/M",
              field16(entd, e, slot_no, 0x0C) == 427
              and field16(entd, e, slot_no, 0x0E) == 467
              and field16(entd, e, slot_no, 0x10) == 488)
        check(f"450 s{slot_no} battle Samurai gear",
              roster(entd, e, [slot_no], 0x12) == [154]
              and roster(entd, e, [slot_no], 0x13) == [184]
              and roster(entd, e, [slot_no], 0x14) == [218]
              and roster(entd, e, [slot_no], 0x15) == [46]
              and roster(entd, e, [slot_no], 0x16) == [139])

    check("450 static flags and positions preserved",
          roster(entd, e, active, 0x18) == [0x90] * 8
          and [(field(entd, e, s, 0x19), field(entd, e, s, 0x1A)) for s in active]
          == [(11, 9), (10, 0), (6, 0), (5, 1), (5, 8), (8, 5), (8, 7), (8, 2)])
    check("450 Kaiser Shield spoil preserved", field(entd, e, 2, 0x1E) == 141)

    # 045 - Mount Germinas, entry 452.
    # v3 vertical mobility skirmish: two Ninjas, two Thieves, two Archers; ninja arsenal paid via spoils.
    e = 452
    active = [0, 1, 2, 3, 4, 5]
    check("452 active jobs", roster(entd, e, active, 0x0A) == [89, 89, 83, 77, 83, 77])
    check("452 active levels", roster(entd, e, active, 0x03) == [102, 101, 101, 102, 100, 100])
    check("452 job buckets", roster(entd, e, active, 0x08) == [14, 4, 4, 19, 15, 19])
    check("452 active job levels", roster(entd, e, active, 0x09) == [8, 8, 8, 8, 8, 8])
    check("452 active secondaries", roster(entd, e, active, 0x0B) == [9, 9, 9, 6, 20, 6])
    check("452 Brave targets", roster(entd, e, active, 0x06) == [90, 90, 88, 82, 88, 82])
    check("452 Faith targets", roster(entd, e, active, 0x07) == [35, 38, 38, 45, 38, 45])

    check("452 s0 Apex Ninja R/S/M and visible Ninja Gear",
          field16(entd, e, 0, 0x0C) == 451
          and field16(entd, e, 0, 0x0E) == 472
          and field16(entd, e, 0, 0x10) == 491
          and roster(entd, e, [0], 0x12) == [168]
          and roster(entd, e, [0], 0x13) == [197]
          and roster(entd, e, [0], 0x14) == [218]
          and roster(entd, e, [0], 0x15) == [18]
          and roster(entd, e, [0], 0x16) == [17])
    check("452 s1 barehand Ninja kit",
          field16(entd, e, 1, 0x0C) == 453
          and field16(entd, e, 1, 0x0E) == 472
          and field16(entd, e, 1, 0x10) == 488
          and roster(entd, e, [1], 0x12) == [163]
          and roster(entd, e, [1], 0x13) == [195]
          and roster(entd, e, [1], 0x14) == [218]
          and roster(entd, e, [1], 0x15) == [255]
          and roster(entd, e, [1], 0x16) == [255])
    check("452 s2 martial Thief kit",
          field16(entd, e, 2, 0x0C) == 449
          and field16(entd, e, 2, 0x0E) == 472
          and field16(entd, e, 2, 0x10) == 488
          and roster(entd, e, [2], 0x12) == [163]
          and roster(entd, e, [2], 0x13) == [195]
          and roster(entd, e, [2], 0x14) == [218]
          and roster(entd, e, [2], 0x15) == [255]
          and roster(entd, e, [2], 0x16) == [255])

    for slot_no in (3, 5):
        check(f"452 s{slot_no} Archer R/S/M",
              field16(entd, e, slot_no, 0x0C) == 449
              and field16(entd, e, slot_no, 0x0E) == 474
              and field16(entd, e, slot_no, 0x10) == 491)
        check(f"452 s{slot_no} Archer gear",
              roster(entd, e, [slot_no], 0x12) == [168]
              and roster(entd, e, [slot_no], 0x13) == [195]
              and roster(entd, e, [slot_no], 0x14) == [218]
              and roster(entd, e, [slot_no], 0x15) == [90]
              and roster(entd, e, [slot_no], 0x16) == [254])

    check("452 s4 Throw Thief kit",
          field16(entd, e, 4, 0x0C) == 424
          and field16(entd, e, 4, 0x0E) == 477
          and field16(entd, e, 4, 0x10) == 491
          and roster(entd, e, [4], 0x12) == [168]
          and roster(entd, e, [4], 0x13) == [195]
          and roster(entd, e, [4], 0x14) == [218]
          and roster(entd, e, [4], 0x15) == [10]
          and roster(entd, e, [4], 0x16) == [8])

    check("452 static flags, positions, and unit ids preserved",
          roster(entd, e, active, 0x18) == [0x90] * 6
          and [(field(entd, e, s, 0x19), field(entd, e, s, 0x1A)) for s in active]
          == [(4, 6), (1, 4), (5, 0), (9, 0), (4, 4), (7, 4)]
          and roster(entd, e, active, 0x20) == [0x80, 0x81, 0x82, 0x83, 0x84, 0x85])

    check("452 ninja arsenal spoils preserved",
          field(entd, e, 0, 0x1E) == 197
          and field(entd, e, 1, 0x1E) == 18
          and field(entd, e, 2, 0x1E) == 17)

    # 046 - Lake Poescas / Poeskas Lake, entry 453.
    # v3 all-undead roster: four equipped special human undead jobs + two equipment-less Revenants.
    e = 453
    active = [0, 1, 2, 3, 4, 5]
    check("453 undead jobs", roster(entd, e, active, 0x0A) == [70, 63, 63, 71, 114, 114])
    check("453 v3 levels", roster(entd, e, active, 0x03) == [102, 101, 100, 102, 101, 100])
    check("453 v3 job buckets", roster(entd, e, active, 0x08) == [19, 19, 1, 8, 0, 0])
    check("453 v3 job levels", roster(entd, e, active, 0x09) == [8, 8, 8, 8, 0, 0])
    check("453 v3 secondaries", roster(entd, e, active, 0x0B) == [17, 6, 6, 11, 0, 0])
    check("453 Brave targets", roster(entd, e, active, 0x06) == [72, 88, 88, 72, 90, 88])
    check("453 Faith targets", roster(entd, e, active, 0x07) == [84, 70, 70, 84, 55, 55])
    check("453 active flags preserved", roster(entd, e, active, 0x01) == [0x80, 0x80, 0x80, 0x40, 0x20, 0x20])
    check("453 unit ids preserved", roster(entd, e, active, 0x20) == [0x80, 0x81, 0x82, 0x83, 0x84, 0x85])
    check("453 control flags and positions preserved",
          roster(entd, e, active, 0x18) == [0x90] * 6
          and [(field(entd, e, s, 0x19), field(entd, e, s, 0x1A)) for s in active]
          == [(6, 9), (8, 11), (6, 11), (9, 6), (0, 2), (10, 3)])

    check("453 s0 Mystic kit",
          field16(entd, e, 0, 0x0C) == 445
          and field16(entd, e, 0, 0x0E) == 467
          and field16(entd, e, 0, 0x10) == 487
          and roster(entd, e, [0], 0x12) == [167]
          and roster(entd, e, [0], 0x13) == [205]
          and roster(entd, e, [0], 0x14) == [217]
          and roster(entd, e, [0], 0x15) == [56]
          and roster(entd, e, [0], 0x16) == [255])
    for slot_no, body, acc, movement in ((1, 195, 218, 491), (2, 199, 234, 488)):
        check(f"453 s{slot_no} undead Archer kit",
              field16(entd, e, slot_no, 0x0C) == 449
              and field16(entd, e, slot_no, 0x0E) == 474
              and field16(entd, e, slot_no, 0x10) == movement
              and roster(entd, e, [slot_no], 0x12) == [168]
              and roster(entd, e, [slot_no], 0x13) == [body]
              and roster(entd, e, [slot_no], 0x14) == [acc]
              and roster(entd, e, [slot_no], 0x15) == [90]
              and roster(entd, e, [slot_no], 0x16) == [254])
    check("453 s3 Summoner kit",
          field16(entd, e, 3, 0x0C) == 449
          and field16(entd, e, 3, 0x0E) == 482
          and field16(entd, e, 3, 0x10) == 494
          and roster(entd, e, [3], 0x12) == [167]
          and roster(entd, e, [3], 0x13) == [205]
          and roster(entd, e, [3], 0x14) == [217]
          and roster(entd, e, [3], 0x15) == [56]
          and roster(entd, e, [3], 0x16) == [255])
    for slot_no in (4, 5):
        check(f"453 s{slot_no} Revenant equipment empty",
              roster(entd, e, [slot_no], 0x12) == [0]
              and roster(entd, e, [slot_no], 0x13) == [0]
              and roster(entd, e, [slot_no], 0x14) == [0]
              and roster(entd, e, [slot_no], 0x15) == [0]
              and roster(entd, e, [slot_no], 0x16) == [0])
    check("453 cursed/phoenix spoils preserved", roster(entd, e, active, 0x1E) == [222, 253, 253, 0, 0, 0])

    # 047 - Limberry Castle Gate, entry 454.
    # v3 Assassin flee race: explicit dual weapons, fixed remaining gear, low-band Reaver escort.
    e = 454
    active = [0, 1, 2, 3, 4, 5]
    check("454 active jobs", roster(entd, e, active, 0x0A) == [45, 46, 150, 150, 150, 150])
    check("454 active levels", roster(entd, e, active, 0x03) == [102, 102, 101, 101, 100, 100])
    check("454 active job levels preserved", roster(entd, e, active, 0x09) == [3, 3, 0, 0, 0, 0])
    check("454 Brave targets", roster(entd, e, active, 0x06) == [92, 92, 88, 88, 88, 88])
    check("454 Faith targets", roster(entd, e, active, 0x07) == [90, 90, 76, 76, 76, 76])
    check("454 fixed-kit assassin flags", roster(entd, e, [0, 1], 0x01) == [0x40, 0x40])
    check("454 Reaver monster flags", roster(entd, e, [2, 3, 4, 5], 0x01) == [0x20, 0x20, 0x20, 0x20])
    check("454 Celia fixed armor and dual Masamune",
          roster(entd, e, [0], 0x12) == [254]
          and roster(entd, e, [0], 0x13) == [254]
          and roster(entd, e, [0], 0x14) == [254]
          and roster(entd, e, [0], 0x15) == [46]
          and roster(entd, e, [0], 0x16) == [46])
    check("454 Lettie fixed armor and Koga/Iga",
          roster(entd, e, [1], 0x12) == [254]
          and roster(entd, e, [1], 0x13) == [254]
          and roster(entd, e, [1], 0x14) == [254]
          and roster(entd, e, [1], 0x15) == [18]
          and roster(entd, e, [1], 0x16) == [17])
    for slot_no in (2, 3, 4, 5):
        check(f"454 s{slot_no} Reaver no-equipment shape",
              roster(entd, e, [slot_no], 0x12) == [255]
              and roster(entd, e, [slot_no], 0x13) == [255]
              and roster(entd, e, [slot_no], 0x14) == [255]
              and roster(entd, e, [slot_no], 0x15) == [255]
              and roster(entd, e, [slot_no], 0x16) == [255])

    # 048 - Limberry Castle Keep, entry 456.
    # Elmdor parry race with fixed assassins and Ultima Demon transform forms.
    e = 456
    active = [0, 1, 2, 3, 4]
    check("456 active jobs", roster(entd, e, active, 0x0A) == [27, 45, 46, 154, 154])
    check("456 active levels", roster(entd, e, active, 0x03) == [102, 101, 101, 100, 100])
    check("456 active job levels preserved", roster(entd, e, active, 0x09) == [8, 3, 3, 0, 0])
    check("456 Brave targets", roster(entd, e, active, 0x06) == [90, 90, 90, 88, 88])
    check("456 Faith targets", roster(entd, e, active, 0x07) == [65, 60, 60, 76, 76])
    check("456 Elmdor R/S/M preserved",
          field16(entd, e, 0, 0x0C) == 451
          and field16(entd, e, 0, 0x0E) == 472
          and field16(entd, e, 0, 0x10) == 499)
    check("456 Elmdor Chirijiraden/Genji gear",
          roster(entd, e, [0], 0x12) == [155]
          and roster(entd, e, [0], 0x13) == [183]
          and roster(entd, e, [0], 0x14) == [216]
          and roster(entd, e, [0], 0x15) == [47]
          and roster(entd, e, [0], 0x16) == [140])
    check("456 Celia fixed armor, Featherweave, dual Masamune",
          roster(entd, e, [1], 0x12) == [254]
          and roster(entd, e, [1], 0x13) == [254]
          and roster(entd, e, [1], 0x14) == [234]
          and roster(entd, e, [1], 0x15) == [46]
          and roster(entd, e, [1], 0x16) == [46])
    check("456 Lettie fixed armor, Featherweave, Koga/Iga",
          roster(entd, e, [2], 0x12) == [254]
          and roster(entd, e, [2], 0x13) == [254]
          and roster(entd, e, [2], 0x14) == [234]
          and roster(entd, e, [2], 0x15) == [18]
          and roster(entd, e, [2], 0x16) == [17])
    for slot_no in (3, 4):
        check(f"456 s{slot_no} Ultima Demon no-equipment shape",
              roster(entd, e, [slot_no], 0x12) == [0]
              and roster(entd, e, [slot_no], 0x13) == [0]
              and roster(entd, e, [slot_no], 0x14) == [0]
              and roster(entd, e, [slot_no], 0x15) == [0]
              and roster(entd, e, [slot_no], 0x16) == [0])
    check("456 Masamune/Genji/Chirijiraden spoils preserved",
          roster(entd, e, active, 0x1E) == [46, 183, 47, 0, 0])

    # 049 - Limberry Castle Undercroft v3, entry 457.
    # Six active slots: Zalera + 2 Archaeodaemon + Undead Mystic + 2 Undead Knights.
    e = 457
    active = [1, 2, 3, 4, 5, 6]
    check("457 placeholder Elmdor preserved",
          field(entd, e, 0, 0x03) == 43
          and field(entd, e, 0, 0x0A) == 27
          and roster(entd, e, [0], 0x12) == [255])
    check("457 Meliadoul join record preserved",
          field(entd, e, 7, 0x03) == 254
          and field(entd, e, 7, 0x0A) == 42
          and roster(entd, e, [7], 0x12) == [153]
          and roster(entd, e, [7], 0x13) == [206]
          and roster(entd, e, [7], 0x14) == [213]
          and roster(entd, e, [7], 0x15) == [34]
          and roster(entd, e, [7], 0x16) == [136])
    check("457 active identity bytes", roster(entd, e, active, 0x00) == [62, 130, 130, 70, 61, 61])
    check("457 active jobs", roster(entd, e, active, 0x0A) == [62, 153, 153, 70, 61, 61])
    check("457 active levels", roster(entd, e, active, 0x03) == [102, 100, 100, 101, 101, 101])
    check("457 v3 job buckets", roster(entd, e, active, 0x08) == [0, 0, 0, 19, 4, 4])
    check("457 v3 job levels", roster(entd, e, active, 0x09) == [8, 8, 8, 8, 8, 8])
    check("457 v3 secondaries", roster(entd, e, active, 0x0B) == [108, 0, 0, 17, 9, 9])
    check("457 Brave targets", roster(entd, e, active, 0x06) == [92, 88, 88, 72, 88, 88])
    check("457 Faith targets", roster(entd, e, active, 0x07) == [86, 76, 76, 84, 40, 40])
    check("457 control flags and positions preserved",
          roster(entd, e, active, 0x18) == [0xD4, 0xD0, 0xD0, 0xD0, 0xD0, 0xD0]
          and [(field(entd, e, s, 0x19), field(entd, e, s, 0x1A)) for s in active]
          == [(2, 15), (4, 3), (1, 3), (4, 1), (4, 14), (1, 14)]
          and roster(entd, e, active, 0x20) == [0x3E, 0x80, 0x81, 0x82, 0x83, 0x84])
    check("457 Zalera no-equipment shape",
          roster(entd, e, [1], 0x12) == [255]
          and roster(entd, e, [1], 0x13) == [255]
          and roster(entd, e, [1], 0x14) == [255]
          and roster(entd, e, [1], 0x15) == [255]
          and roster(entd, e, [1], 0x16) == [255])
    for slot_no in (2, 3):
        check(f"457 s{slot_no} Archaeodaemon innate kit",
              field16(entd, e, slot_no, 0x0C) == 510
              and field16(entd, e, slot_no, 0x0E) == 510
              and field16(entd, e, slot_no, 0x10) == 510
              and roster(entd, e, [slot_no], 0x12) == [0]
              and roster(entd, e, [slot_no], 0x13) == [0]
              and roster(entd, e, [slot_no], 0x14) == [0]
              and roster(entd, e, [slot_no], 0x15) == [0]
              and roster(entd, e, [slot_no], 0x16) == [0])
    check("457 s4 Undead Mystic kit",
          field16(entd, e, 4, 0x0C) == 445
          and field16(entd, e, 4, 0x0E) == 467
          and field16(entd, e, 4, 0x10) == 487
          and roster(entd, e, [4], 0x12) == [167]
          and roster(entd, e, [4], 0x13) == [205]
          and roster(entd, e, [4], 0x14) == [217]
          and roster(entd, e, [4], 0x15) == [56]
          and roster(entd, e, [4], 0x16) == [255])
    for slot_no in (5, 6):
        check(f"457 s{slot_no} Undead Knight kit",
              field16(entd, e, slot_no, 0x0C) == 442
              and field16(entd, e, slot_no, 0x0E) == 477
              and field16(entd, e, slot_no, 0x10) == 488
              and roster(entd, e, [slot_no], 0x12) == [154]
              and roster(entd, e, [slot_no], 0x13) == [182]
              and roster(entd, e, [slot_no], 0x14) == [218]
              and roster(entd, e, [slot_no], 0x15) == [30]
              and roster(entd, e, [slot_no], 0x16) == [30])
    check("457 inactive raw records preserved",
          roster(entd, e, [8, 9], 0x0A) == [111, 111]
          and roster(entd, e, [8, 9], 0x03) == [103, 103]
          and roster(entd, e, [8, 9], 0x20) == [0x85, 0x86])
    check("457 Aegis/Zeus spoils preserved",
          field(entd, e, 1, 0x1E) == 136
          and field(entd, e, 2, 0x1E) == 65)

    # 050 - Eagrose Castle / Igros Castle, entry 459.
    # Two-phase Dycedarg -> Adramelk fight. Slot 0 guest must be player-controlled if active.
    e = 459
    active = [0, 1, 2, 3, 4, 5, 6, 7]
    check("459 active jobs", roster(entd, e, active, 0x0A) == [8, 9, 76, 76, 76, 76, 76, 69])
    check("459 active levels", roster(entd, e, active, 0x03) == [103, 104, 103, 103, 103, 103, 103, 105])
    check("459 active job levels", roster(entd, e, active, 0x09) == [8, 8, 8, 8, 1, 1, 1, 0])
    check("459 active secondaries", roster(entd, e, active, 0x0B) == [254, 71, 6, 6, 6, 6, 6, 120])
    check("459 Brave targets", roster(entd, e, active, 0x06) == [70, 88, 88, 88, 84, 84, 84, 92])
    check("459 Faith targets", roster(entd, e, active, 0x07) == [65, 60, 42, 42, 55, 55, 55, 86])
    check("459 guest player-control bit", field(entd, e, 0, 0x18) == 0x8C)
    check("459 guest gear preserved",
          roster(entd, e, [0], 0x12) == [154]
          and roster(entd, e, [0], 0x13) == [182]
          and roster(entd, e, [0], 0x14) == [210]
          and roster(entd, e, [0], 0x15) == [30]
          and roster(entd, e, [0], 0x16) == [139])
    check("459 Dycedarg gear and R/S/M",
          field16(entd, e, 1, 0x0C) == 450
          and field16(entd, e, 1, 0x0E) == 479
          and field16(entd, e, 1, 0x10) == 486
          and roster(entd, e, [1], 0x12) == [156]
          and roster(entd, e, [1], 0x13) == [181]
          and roster(entd, e, [1], 0x14) == [215]
          and roster(entd, e, [1], 0x15) == [33]
          and roster(entd, e, [1], 0x16) == [136])

    for slot_no in (2, 3, 4, 5, 6):
        check(f"459 s{slot_no} Knight R/S/M",
              field16(entd, e, slot_no, 0x0C) == 442
              and field16(entd, e, slot_no, 0x0E) == 465
              and field16(entd, e, slot_no, 0x10) == 486)
        check(f"459 s{slot_no} Knight armor",
              roster(entd, e, [slot_no], 0x12) == [154]
              and roster(entd, e, [slot_no], 0x13) == [182]
              and roster(entd, e, [slot_no], 0x14) == [218]
              and roster(entd, e, [slot_no], 0x16) == [139])

    check("459 Adramelk no-equipment shape",
          roster(entd, e, [7], 0x12) == [255]
          and roster(entd, e, [7], 0x13) == [255]
          and roster(entd, e, [7], 0x14) == [255]
          and roster(entd, e, [7], 0x15) == [255]
          and roster(entd, e, [7], 0x16) == [255])
    check("459 placeholders preserved",
          roster(entd, e, [8, 9], 0x03) == [254, 254]
          and roster(entd, e, [8, 9], 0x0A) == [8, 8]
          and roster(entd, e, [8, 9], 0x18) == [0xC0, 0xC0])
    check("459 Maximillian/Grand Helm/Venetian spoils preserved",
          field(entd, e, 1, 0x1E) == 185
          and field(entd, e, 2, 0x1E) == 156
          and field(entd, e, 3, 0x1E) == 142)

    # 051 - Mullonde Cathedral Exterior / Murond Holy Place, entry 460.
    # Chain opener: six static caster enemies, hidden White Mage sustain engine, no added slots.
    e = 460
    active = [0, 1, 2, 3, 4, 5]
    check("460 active jobs", roster(entd, e, active, 0x0A) == [79, 82, 86, 86, 84, 84])
    check("460 active levels", roster(entd, e, active, 0x03) == [103, 102, 102, 102, 102, 102])
    check("460 active job levels", roster(entd, e, active, 0x09) == [8, 8, 8, 8, 8, 8])
    check("460 active secondaries", roster(entd, e, active, 0x0B) == [6, 6, 6, 6, 6, 6])
    check("460 Brave targets", roster(entd, e, active, 0x06) == [60, 60, 68, 68, 68, 68])
    check("460 Faith targets", roster(entd, e, active, 0x07) == [84, 84, 78, 78, 78, 78])

    for slot_no in (0, 1):
        check(f"460 s{slot_no} pure caster R/S/M",
              field16(entd, e, slot_no, 0x0C) == 449
              and field16(entd, e, slot_no, 0x0E) == 467
              and field16(entd, e, slot_no, 0x10) == 486)
        check(f"460 s{slot_no} caster gear",
              roster(entd, e, [slot_no], 0x12) == [167]
              and roster(entd, e, [slot_no], 0x13) == [206]
              and roster(entd, e, [slot_no], 0x14) == [234])

    check("460 White Mage staff and reward",
          field(entd, e, 0, 0x15) == 64
          and field(entd, e, 0, 0x1E) == 66)
    check("460 Summoner Dragon Rod and minor spoil",
          field(entd, e, 1, 0x15) == 57
          and field(entd, e, 1, 0x1E) == 242)

    for slot_no in (2, 3):
        check(f"460 s{slot_no} Geomancer R/S/M",
              field16(entd, e, slot_no, 0x0C) == 442
              and field16(entd, e, slot_no, 0x0E) == 465
              and field16(entd, e, slot_no, 0x10) == 486)
        check(f"460 s{slot_no} Geomancer gear",
              roster(entd, e, [slot_no], 0x12) == [167]
              and roster(entd, e, [slot_no], 0x13) == [206]
              and roster(entd, e, [slot_no], 0x14) == [234]
              and roster(entd, e, [slot_no], 0x15) == [56])

    for slot_no in (4, 5):
        check(f"460 s{slot_no} Orator R/S/M",
              field16(entd, e, slot_no, 0x0C) == 449
              and field16(entd, e, slot_no, 0x0E) == 466
              and field16(entd, e, slot_no, 0x10) == 486)
        check(f"460 s{slot_no} Orator gear",
              roster(entd, e, [slot_no], 0x12) == [167]
              and roster(entd, e, [slot_no], 0x13) == [206]
              and roster(entd, e, [slot_no], 0x14) == [234]
              and roster(entd, e, [slot_no], 0x15) == [72])

    check("460 Faerie Harp spoil preserved", field(entd, e, 2, 0x1E) == 94)

    # 052 - Mullonde Cathedral Nave / Murond Holy Place, entry 461.
    # Pure three-boss focus race: Folmarv + Loffrey are the only break bosses; Cletienne is caster pressure.
    e = 461
    active = [0, 1, 2]
    check("461 active jobs", roster(entd, e, active, 0x0A) == [36, 37, 39])
    check("461 active levels", roster(entd, e, active, 0x03) == [105, 104, 104])
    check("461 active job levels", roster(entd, e, active, 0x09) == [8, 8, 8])
    check("461 Brave targets", roster(entd, e, active, 0x06) == [90, 90, 65])
    check("461 Faith targets", roster(entd, e, active, 0x07) == [55, 55, 88])
    check("461 Folmarv Chaos Blade kit",
          field16(entd, e, 0, 0x0C) == 442
          and field16(entd, e, 0, 0x0E) == 466
          and field16(entd, e, 0, 0x10) == 486
          and roster(entd, e, [0], 0x12) == [154]
          and roster(entd, e, [0], 0x13) == [182]
          and roster(entd, e, [0], 0x14) == [232]
          and roster(entd, e, [0], 0x15) == [37]
          and roster(entd, e, [0], 0x16) == [139])
    check("461 Loffrey break kit",
          field16(entd, e, 1, 0x0C) == 437
          and field16(entd, e, 1, 0x0E) == 466
          and field16(entd, e, 1, 0x10) == 489
          and roster(entd, e, [1], 0x12) == [152]
          and roster(entd, e, [1], 0x13) == [180]
          and roster(entd, e, [1], 0x14) == [224]
          and roster(entd, e, [1], 0x15) == [29]
          and roster(entd, e, [1], 0x16) == [138])
    check("461 Cletienne caster kit",
          field16(entd, e, 2, 0x0C) == 435
          and field16(entd, e, 2, 0x0E) == 468
          and field16(entd, e, 2, 0x10) == 492
          and roster(entd, e, [2], 0x12) == [166]
          and roster(entd, e, [2], 0x13) == [196]
          and roster(entd, e, [2], 0x14) == [232]
          and roster(entd, e, [2], 0x15) == [57]
          and roster(entd, e, [2], 0x16) == [254])
    check("461 script placeholder preserved",
          field(entd, e, 3, 0x03) == 65
          and field(entd, e, 3, 0x0A) == 39
          and field(entd, e, 3, 0x18) == 0xD0
          and roster(entd, e, [3], 0x12) == [0]
          and roster(entd, e, [3], 0x13) == [0]
          and roster(entd, e, [3], 0x14) == [0]
          and roster(entd, e, [3], 0x15) == [0]
          and roster(entd, e, [3], 0x16) == [0])
    check("461 Chaos/Escutcheon/Lordly spoils preserved",
          field(entd, e, 0, 0x1E) == 37
          and field(entd, e, 1, 0x1E) == 143
          and field(entd, e, 2, 0x1E) == 207)

    # 053 - Mullonde Cathedral Sanctuary / Murond Holy Place, entry 462.
    # Chain closer: Zalbaag is the sole focus target; demons are screen pressure; Ragnarok is spoil-only.
    e = 462
    active = [1, 2, 3, 4]
    check("462 active jobs", roster(entd, e, active, 0x0A) == [51, 153, 153, 154])
    check("462 active levels", roster(entd, e, active, 0x03) == [105, 103, 103, 103])
    check("462 Brave targets", roster(entd, e, active, 0x06) == [90, 88, 88, 88])
    check("462 Faith targets", roster(entd, e, active, 0x07) == [78, 76, 76, 76])
    check("462 Zalbaag Runeblade/Ribbon kit",
          field(entd, e, 1, 0x09) == 8
          and field(entd, e, 1, 0x0B) == 63
          and field16(entd, e, 1, 0x0C) == 424
          and field16(entd, e, 1, 0x0E) == 466
          and field16(entd, e, 1, 0x10) == 493
          and roster(entd, e, [1], 0x12) == [154]
          and roster(entd, e, [1], 0x13) == [182]
          and roster(entd, e, [1], 0x14) == [171]
          and roster(entd, e, [1], 0x15) == [30]
          and roster(entd, e, [1], 0x16) == [139])
    for slot_no in (2, 3, 4):
        check(f"462 s{slot_no} demon no-equipment shape",
              roster(entd, e, [slot_no], 0x12) == [0]
              and roster(entd, e, [slot_no], 0x13) == [0]
              and roster(entd, e, [slot_no], 0x14) == [0]
              and roster(entd, e, [slot_no], 0x15) == [0]
              and roster(entd, e, [slot_no], 0x16) == [0])
    check("462 placeholders preserved",
          field(entd, e, 0, 0x03) == 254
          and field(entd, e, 0, 0x0A) == 36
          and roster(entd, e, [0], 0x12) == [255]
          and field(entd, e, 5, 0x03) == 254
          and field(entd, e, 5, 0x0A) == 51
          and field(entd, e, 5, 0x18) == 0xD0
          and roster(entd, e, [5], 0x12) == [255])
    check("462 Ragnarok/Ribbon/Elixir spoils preserved",
          field(entd, e, 1, 0x1E) == 36
          and field(entd, e, 2, 0x1E) == 171
          and field(entd, e, 3, 0x1E) == 245)

    # 054 - Monastery Vaults, Fourth Level, entry 435.
    # Endgame gauntlet opener: Loffrey exits by script; six active generics with capped Rend pressure.
    e = 435
    active = [1, 2, 3, 4, 5, 6]
    check("435 Loffrey cutscene slot preserved",
          field(entd, e, 0, 0x03) == 1
          and field(entd, e, 0, 0x0A) == 37
          and field(entd, e, 0, 0x06) == 90
          and field(entd, e, 0, 0x07) == 55
          and roster(entd, e, [0], 0x12) == [153]
          and roster(entd, e, [0], 0x13) == [181]
          and roster(entd, e, [0], 0x14) == [211]
          and roster(entd, e, [0], 0x15) == [33]
          and roster(entd, e, [0], 0x16) == [136])
    check("435 active jobs", roster(entd, e, active, 0x0A) == [76, 76, 76, 78, 78, 89])
    check("435 active levels", roster(entd, e, active, 0x03) == [103, 103, 102, 102, 102, 103])
    check("435 active job levels", roster(entd, e, active, 0x09) == [8, 8, 1, 8, 8, 8])
    check("435 active secondaries", roster(entd, e, active, 0x0B) == [6, 6, 6, 5, 5, 14])
    check("435 Brave targets", roster(entd, e, active, 0x06) == [88, 88, 88, 88, 88, 90])
    check("435 Faith targets", roster(entd, e, active, 0x07) == [42, 42, 42, 40, 40, 35])
    for slot_no in (1, 2):
        check(f"435 s{slot_no} Rend Knight kit",
              field16(entd, e, slot_no, 0x0C) == 442
              and field16(entd, e, slot_no, 0x0E) == 465
              and field16(entd, e, slot_no, 0x10) == 486
              and roster(entd, e, [slot_no], 0x12) == [154]
              and roster(entd, e, [slot_no], 0x13) == [182]
              and roster(entd, e, [slot_no], 0x14) == [218]
              and roster(entd, e, [slot_no], 0x15) == [30]
              and roster(entd, e, [slot_no], 0x16) == [139])
    check("435 s3 guard Knight kit",
          field16(entd, e, 3, 0x0C) == 442
          and field16(entd, e, 3, 0x0E) == 466
          and field16(entd, e, 3, 0x10) == 486
          and roster(entd, e, [3], 0x12) == [154]
          and roster(entd, e, [3], 0x13) == [182]
          and roster(entd, e, [3], 0x14) == [218]
          and roster(entd, e, [3], 0x15) == [30]
          and roster(entd, e, [3], 0x16) == [139])
    for slot_no in (4, 5):
        check(f"435 s{slot_no} Monk kit",
              field16(entd, e, slot_no, 0x0C) == 442
              and field16(entd, e, slot_no, 0x0E) == 465
              and field16(entd, e, slot_no, 0x10) == 486
              and roster(entd, e, [slot_no], 0x12) == [163]
              and roster(entd, e, [slot_no], 0x13) == [195]
              and roster(entd, e, [slot_no], 0x14) == [218])
    check("435 Ninja replaces Archer",
          field16(entd, e, 6, 0x0C) == 449
          and field16(entd, e, 6, 0x0E) == 465
          and field16(entd, e, 6, 0x10) == 487
          and roster(entd, e, [6], 0x12) == [168]
          and roster(entd, e, [6], 0x13) == [198]
          and roster(entd, e, [6], 0x14) == [218]
          and roster(entd, e, [6], 0x15) == [14]
          and roster(entd, e, [6], 0x16) == [14])
    check("435 no usable gauntlet spoils", roster(entd, e, active, 0x1E) == [0, 0, 0, 0, 0, 0])

    # 055 - Monastery Vaults, Fifth Level, entry 436.
    # Loffrey boss race through caster crossfire; no usable reward inside the final gauntlet.
    e = 436
    active = [0, 1, 2, 3, 4, 5]
    check("436 active jobs", roster(entd, e, active, 0x0A) == [37, 80, 80, 82, 82, 81])
    check("436 active levels", roster(entd, e, active, 0x03) == [105, 103, 103, 103, 103, 103])
    check("436 active job levels", roster(entd, e, active, 0x09) == [8, 8, 8, 8, 8, 4])
    check("436 active secondaries", roster(entd, e, active, 0x0B) == [61, 6, 6, 6, 6, 6])
    check("436 Brave targets", roster(entd, e, active, 0x06) == [90, 60, 60, 60, 60, 62])
    check("436 Faith targets", roster(entd, e, active, 0x07) == [55, 84, 84, 84, 84, 80])
    check("436 Loffrey non-rare break kit",
          field16(entd, e, 0, 0x0C) == 447
          and field16(entd, e, 0, 0x0E) == 466
          and field16(entd, e, 0, 0x10) == 487
          and roster(entd, e, [0], 0x12) == [154]
          and roster(entd, e, [0], 0x13) == [182]
          and roster(entd, e, [0], 0x14) == [210]
          and roster(entd, e, [0], 0x15) == [30]
          and roster(entd, e, [0], 0x16) == [139])
    for slot_no in (1, 2, 3, 4, 5):
        check(f"436 s{slot_no} caster R/S/M",
              field16(entd, e, slot_no, 0x0C) == 449
              and field16(entd, e, slot_no, 0x0E) == 467
              and field16(entd, e, slot_no, 0x10) == 486)
        check(f"436 s{slot_no} caster gear",
              roster(entd, e, [slot_no], 0x12) == [167]
              and roster(entd, e, [slot_no], 0x13) == [206]
              and roster(entd, e, [slot_no], 0x14) == [234]
              and roster(entd, e, [slot_no], 0x15) == [56]
              and roster(entd, e, [slot_no], 0x16) == [255])
    check("436 no usable gauntlet spoils", roster(entd, e, active, 0x1E) == [0, 0, 0, 0, 0, 0])

    # 056 - Necrohol of Mullonde / The Capitoline, entry 438.
    # Cletienne surge race with elite Samurai/Ninja/Time Mage screen; no usable gauntlet reward.
    e = 438
    active = [0, 1, 2, 3, 4, 5, 6]
    check("438 active jobs", roster(entd, e, active, 0x0A) == [39, 81, 81, 89, 89, 88, 88])
    check("438 active levels", roster(entd, e, active, 0x03) == [105, 104, 104, 104, 104, 104, 104])
    check("438 active job levels", roster(entd, e, active, 0x09) == [8, 8, 8, 8, 8, 8, 8])
    check("438 active secondaries", roster(entd, e, active, 0x0B) == [5, 6, 6, 6, 6, 6, 6])
    check("438 Brave targets", roster(entd, e, active, 0x06) == [65, 62, 62, 90, 90, 88, 88])
    check("438 Faith targets", roster(entd, e, active, 0x07) == [88, 80, 80, 35, 35, 60, 60])
    check("438 Cletienne no-reward surge kit",
          field16(entd, e, 0, 0x0C) == 423
          and field16(entd, e, 0, 0x0E) == 468
          and field16(entd, e, 0, 0x10) == 507
          and roster(entd, e, [0], 0x12) == [167]
          and roster(entd, e, [0], 0x13) == [198]
          and roster(entd, e, [0], 0x14) == [234]
          and roster(entd, e, [0], 0x15) == [65]
          and roster(entd, e, [0], 0x16) == [254])
    for slot_no in (1, 2):
        check(f"438 s{slot_no} Time Mage kit",
              field16(entd, e, slot_no, 0x0C) == 449
              and field16(entd, e, slot_no, 0x0E) == 467
              and field16(entd, e, slot_no, 0x10) == 486
              and roster(entd, e, [slot_no], 0x12) == [167]
              and roster(entd, e, [slot_no], 0x13) == [206]
              and roster(entd, e, [slot_no], 0x14) == [234]
              and roster(entd, e, [slot_no], 0x15) == [56]
              and roster(entd, e, [slot_no], 0x16) == [255])
    for slot_no in (3, 4):
        check(f"438 s{slot_no} Ninja flanker kit",
              field16(entd, e, slot_no, 0x0C) == 453
              and field16(entd, e, slot_no, 0x0E) == 465
              and field16(entd, e, slot_no, 0x10) == 487
              and roster(entd, e, [slot_no], 0x12) == [168]
              and roster(entd, e, [slot_no], 0x13) == [198]
              and roster(entd, e, [slot_no], 0x14) == [210]
              and roster(entd, e, [slot_no], 0x15) == [14]
              and roster(entd, e, [slot_no], 0x16) == [14])
    for slot_no in (5, 6):
        check(f"438 s{slot_no} Samurai screen kit",
              field16(entd, e, slot_no, 0x0C) == 442
              and field16(entd, e, slot_no, 0x0E) == 465
              and field16(entd, e, slot_no, 0x10) == 486
              and roster(entd, e, [slot_no], 0x12) == [154]
              and roster(entd, e, [slot_no], 0x13) == [182]
              and roster(entd, e, [slot_no], 0x14) == [218]
              and roster(entd, e, [slot_no], 0x15) == [45]
              and roster(entd, e, [slot_no], 0x16) == [254])
    check("438 no usable gauntlet spoils", roster(entd, e, active, 0x1E) == [0, 0, 0, 0, 0, 0, 0])

    # 057 - Lost Halidom / Lost Sacred Precincts, entry 439.
    # Barich control boss plus raceable Chemist sustain and four apex monsters; no usable gauntlet reward.
    e = 439
    active = [0, 1, 2, 3, 4, 5]
    check("439 active jobs", roster(entd, e, active, 0x0A) == [43, 75, 139, 140, 141, 135])
    check("439 active levels", roster(entd, e, active, 0x03) == [105, 104, 105, 105, 105, 105])
    check("439 active job levels", roster(entd, e, active, 0x09) == [8, 8, 8, 8, 8, 8])
    check("439 active secondaries", roster(entd, e, active, 0x0B) == [6, 5, 0, 0, 0, 0])
    check("439 Brave targets", roster(entd, e, active, 0x06) == [84, 72, 90, 90, 90, 90])
    check("439 Faith targets", roster(entd, e, active, 0x07) == [55, 68, 30, 30, 30, 30])
    check("439 Barich non-reward gun kit",
          field16(entd, e, 0, 0x0C) == 442
          and field16(entd, e, 0, 0x0E) == 472
          and field16(entd, e, 0, 0x10) == 493
          and roster(entd, e, [0], 0x12) == [168]
          and roster(entd, e, [0], 0x13) == [206]
          and roster(entd, e, [0], 0x14) == [234]
          and roster(entd, e, [0], 0x15) == [72]
          and roster(entd, e, [0], 0x16) == [254])
    check("439 Chemist sustain kit",
          field16(entd, e, 1, 0x0C) == 441
          and field16(entd, e, 1, 0x0E) == 466
          and field16(entd, e, 1, 0x10) == 486
          and roster(entd, e, [1], 0x12) == [168]
          and roster(entd, e, [1], 0x13) == [198]
          and roster(entd, e, [1], 0x14) == [234]
          and roster(entd, e, [1], 0x15) == [72]
          and roster(entd, e, [1], 0x16) == [254])
    for slot_no in (2, 3, 4, 5):
        check(f"439 s{slot_no} monster unchanged shell",
              field16(entd, e, slot_no, 0x0C) == 510
              and field16(entd, e, slot_no, 0x0E) == 510
              and field16(entd, e, slot_no, 0x10) == 510
              and roster(entd, e, [slot_no], 0x12) == [0]
              and roster(entd, e, [slot_no], 0x13) == [0]
              and roster(entd, e, [slot_no], 0x14) == [0]
              and roster(entd, e, [slot_no], 0x15) == [0]
              and roster(entd, e, [slot_no], 0x16) == [0])
    check("439 no usable gauntlet spoils", roster(entd, e, active, 0x1E) == [0, 0, 0, 0, 0, 0])

    # 058 - Airship Graveyard, phase 1 Hashmal, entry 440.
    # Preserve scripted transition; no unique reward payload inside the final gauntlet.
    e = 440
    active = [0, 1, 2, 3, 4, 5]
    check("440 active/script jobs", roster(entd, e, active, 0x0A) == [36, 44, 64, 44, 44, 44])
    check("440 phase levels", roster(entd, e, active, 0x03) == [105, 105, 105, 104, 104, 104])
    check("440 Brave targets", roster(entd, e, active, 0x06) == [92, 88, 92, 88, 88, 88])
    check("440 Faith targets", roster(entd, e, active, 0x07) == [86, 76, 86, 76, 76, 76])
    check("440 host no Save the Queen leak",
          roster(entd, e, [0], 0x12) == [154]
          and roster(entd, e, [0], 0x13) == [182]
          and roster(entd, e, [0], 0x14) == [213]
          and roster(entd, e, [0], 0x15) == [30]
          and roster(entd, e, [0], 0x16) == [139])
    check("440 named support gear preserved",
          roster(entd, e, [1], 0x12) == [171]
          and roster(entd, e, [1], 0x13) == [206]
          and roster(entd, e, [1], 0x14) == [234]
          and roster(entd, e, [1], 0x15) == [61]
          and roster(entd, e, [1], 0x16) == [255])
    check("440 no usable gauntlet spoils", roster(entd, e, active, 0x1E) == [0, 0, 0, 0, 0, 0])

    # 058 - Airship Graveyard, phase 2 Ultima, entry 441.
    # Ultima is the only level-106 unit; support/form records stay capped at 105.
    e = 441
    active = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    check("441 active/script jobs", roster(entd, e, active, 0x0A) == [49, 49, 20, 154, 154, 154, 154, 65, 73])
    check("441 phase levels", roster(entd, e, active, 0x03) == [105, 105, 106, 105, 105, 105, 105, 105, 105])
    check("441 Brave targets", roster(entd, e, active, 0x06) == [92, 92, 92, 88, 88, 88, 88, 92, 92])
    check("441 Faith targets", roster(entd, e, active, 0x07) == [86, 86, 90, 76, 76, 76, 76, 86, 86])
    check("441 Ultima capstone kit preserved",
          field16(entd, e, 2, 0x0C) == 430
          and roster(entd, e, [2], 0x12) == [171]
          and roster(entd, e, [2], 0x13) == [206]
          and roster(entd, e, [2], 0x14) == [234]
          and roster(entd, e, [2], 0x15) == [61]
          and roster(entd, e, [2], 0x16) == [255])
    for slot_no in (3, 4, 5, 6):
        check(f"441 s{slot_no} Ultima Demon shell",
              roster(entd, e, [slot_no], 0x12) == [255]
              and roster(entd, e, [slot_no], 0x13) == [255]
              and roster(entd, e, [slot_no], 0x14) == [255]
              and roster(entd, e, [slot_no], 0x15) == [255]
              and roster(entd, e, [slot_no], 0x16) == [255])
    check("441 no usable gauntlet spoils", roster(entd, e, active, 0x1E) == [0, 0, 0, 0, 0, 0, 0, 0, 0])

    failed = [name for name, ok in checks if not ok]
    if failed:
        print(f"{len(failed)}/{len(checks)} Chapter 4 v2 checks failed:")
        for name in failed:
            print(f"FAIL {name}")
        return 1

    print(f"All {len(checks)} Chapter 4 v2 checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
