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
    # Six-body Chapter 4 opener: Knight screen, 2 Black Mages, Haste/Slow/Float Time Mage, 2 Dragoons.
    e = 442
    active = [0, 1, 2, 3, 4, 5]
    check("442 active jobs", roster(entd, e, active, 0x0A) == [76, 80, 81, 80, 87, 87])
    check("442 active levels", roster(entd, e, active, 0x03) == [101, 102, 101, 102, 102, 101])
    check("442 active job ranks", roster(entd, e, active, 0x08) == [2, 6, 7, 6, 13, 13])
    check("442 active job levels", roster(entd, e, active, 0x09) == [8, 8, 4, 8, 8, 8])
    check("442 active secondaries", roster(entd, e, active, 0x0B) == [6, 6, 6, 6, 6, 6])
    check("442 Brave targets", roster(entd, e, active, 0x06) == [88, 60, 62, 60, 86, 86])
    check("442 Faith targets", roster(entd, e, active, 0x07) == [42, 84, 80, 84, 40, 40])

    check("442 s0 Knight R/S/M",
          field16(entd, e, 0, 0x0C) == 442
          and field16(entd, e, 0, 0x0E) == 465
          and field16(entd, e, 0, 0x10) == 486)
    check("442 s0 Knight gear",
          roster(entd, e, [0], 0x12) == [154]
          and roster(entd, e, [0], 0x13) == [182]
          and roster(entd, e, [0], 0x14) == [218]
          and roster(entd, e, [0], 0x15) == [30]
          and roster(entd, e, [0], 0x16) == [139])

    for slot_no in (1, 3):
        check(f"442 s{slot_no} Black Mage R/S/M",
              field16(entd, e, slot_no, 0x0C) == 449
              and field16(entd, e, slot_no, 0x0E) == 467
              and field16(entd, e, slot_no, 0x10) == 486)
        check(f"442 s{slot_no} Black Mage gear",
              roster(entd, e, [slot_no], 0x12) == [167]
              and roster(entd, e, [slot_no], 0x13) == [206]
              and roster(entd, e, [slot_no], 0x14) == [234]
              and roster(entd, e, [slot_no], 0x15) == [56]
              and roster(entd, e, [slot_no], 0x16) == [255])

    check("442 s2 Time Mage R/S/M",
          field16(entd, e, 2, 0x0C) == 449
          and field16(entd, e, 2, 0x0E) == 482
          and field16(entd, e, 2, 0x10) == 486)
    check("442 s2 Time Mage gear",
          roster(entd, e, [2], 0x12) == [167]
          and roster(entd, e, [2], 0x13) == [206]
          and roster(entd, e, [2], 0x14) == [234]
          and roster(entd, e, [2], 0x15) == [64]
          and roster(entd, e, [2], 0x16) == [255])

    for slot_no in (4, 5):
        check(f"442 s{slot_no} Dragoon R/S/M",
              field16(entd, e, slot_no, 0x0C) == 449
              and field16(entd, e, slot_no, 0x0E) == 465
              and field16(entd, e, slot_no, 0x10) == 486)
        check(f"442 s{slot_no} Dragoon gear",
              roster(entd, e, [slot_no], 0x12) == [154]
              and roster(entd, e, [slot_no], 0x13) == [182]
              and roster(entd, e, [slot_no], 0x14) == [210]
              and roster(entd, e, [slot_no], 0x15) == [102]
              and roster(entd, e, [slot_no], 0x16) == [139])

    check("442 reward spoils preserved", roster(entd, e, active, 0x1E) == [0, 58, 179, 0, 0, 0])

    # 039 - Free City of Bervenia, entry 443.
    # Meliadoul is the only break source; support screen is complete but does not add hard control.
    e = 443
    active = [0, 1, 2, 3, 4, 5]
    check("443 active jobs", roster(entd, e, active, 0x0A) == [47, 82, 77, 77, 82, 89])
    check("443 active levels", roster(entd, e, active, 0x03) == [104, 102, 102, 101, 102, 102])
    check("443 active job levels", roster(entd, e, active, 0x09) == [8, 8, 8, 8, 8, 8])
    check("443 active secondaries", roster(entd, e, active, 0x0B) == [6, 6, 5, 5, 6, 6])
    check("443 Brave targets", roster(entd, e, active, 0x06) == [88, 60, 88, 82, 60, 90])
    check("443 Faith targets", roster(entd, e, active, 0x07) == [42, 84, 55, 45, 84, 35])

    check("443 Meliadoul boss R/S/M and weapon",
          field16(entd, e, 0, 0x0C) == 442
          and field16(entd, e, 0, 0x0E) == 465
          and field16(entd, e, 0, 0x10) == 486
          and field(entd, e, 0, 0x15) == 34)

    for slot_no in (1, 4):
        check(f"443 s{slot_no} Summoner R/S/M",
              field16(entd, e, slot_no, 0x0C) == 449
              and field16(entd, e, slot_no, 0x0E) == 467
              and field16(entd, e, slot_no, 0x10) == 486)
        check(f"443 s{slot_no} Summoner gear",
              roster(entd, e, [slot_no], 0x12) == [167]
              and roster(entd, e, [slot_no], 0x13) == [206]
              and roster(entd, e, [slot_no], 0x14) == [234]
              and roster(entd, e, [slot_no], 0x15) == [56]
              and roster(entd, e, [slot_no], 0x16) == [255])

    for slot_no in (2, 3):
        check(f"443 s{slot_no} Archer R/S/M",
              field16(entd, e, slot_no, 0x0C) == 449
              and field16(entd, e, slot_no, 0x0E) == 469
              and field16(entd, e, slot_no, 0x10) == 486)
        check(f"443 s{slot_no} Archer gear",
              roster(entd, e, [slot_no], 0x12) == [168]
              and roster(entd, e, [slot_no], 0x13) == [198]
              and roster(entd, e, [slot_no], 0x14) == [218]
              and roster(entd, e, [slot_no], 0x15) == [87]
              and roster(entd, e, [slot_no], 0x16) == [254])

    check("443 s5 Ninja R/S/M",
          field16(entd, e, 5, 0x0C) == 453
          and field16(entd, e, 5, 0x0E) == 465
          and field16(entd, e, 5, 0x10) == 487)
    check("443 s5 Ninja gear",
          roster(entd, e, [5], 0x12) == [168]
          and roster(entd, e, [5], 0x13) == [198]
          and roster(entd, e, [5], 0x14) == [210]
          and roster(entd, e, [5], 0x15) == [14]
          and roster(entd, e, [5], 0x16) == [14])
    check("443 reward spoils preserved", roster(entd, e, active, 0x1E) == [0, 0, 0, 225, 252, 34])

    # 040 - Finnath Creek, entry 444.
    # De-randomized six-body flock: 2 Black Chocobo, 2 yellow Chocobo, 1 Red Chocobo, 1 Pig.
    e = 444
    cleared = [0, 1, 2, 3, 4, 5]
    active = [6, 7, 8, 9, 10, 11]
    check("444 old variant records cleared", roster(entd, e, cleared, 0x20) == [255, 255, 255, 255, 255, 255])
    check("444 fixed flock jobs", roster(entd, e, active, 0x0A) == [95, 95, 94, 94, 96, 121])
    check("444 fixed flock levels", roster(entd, e, active, 0x03) == [102, 102, 101, 101, 101, 100])
    check("444 fixed flock job levels", roster(entd, e, active, 0x09) == [8, 8, 8, 8, 8, 8])
    check("444 fixed flock Brave", roster(entd, e, active, 0x06) == [90, 90, 90, 90, 90, 60])
    check("444 fixed flock Faith", roster(entd, e, active, 0x07) == [30, 30, 30, 30, 30, 40])
    check("444 fixed flock control flags", roster(entd, e, active, 0x18) == [0x90, 0x90, 0x90, 0x90, 0x90, 0x90])
    check("444 fixed flock unit ids", roster(entd, e, active, 0x20) == [0x80, 0x81, 0x82, 0x83, 0x84, 0x85])
    check("444 no equipment spoils", roster(entd, e, active, 0x1E) == [0, 0, 0, 0, 0, 0])

    # 041 - Outlying Church, entry 445.
    # Zalmo focus fight with two full Rend Knights and one lower-JL bodyguard Knight.
    e = 445
    active = [1, 2, 3, 4, 5, 6]
    check("445 inactive placeholder preserved",
          field(entd, e, 0, 0x03) == 254
          and field(entd, e, 0, 0x0A) == 5
          and field(entd, e, 0, 0x18) == 0x84)
    check("445 active jobs", roster(entd, e, active, 0x0A) == [16, 85, 85, 76, 76, 76])
    check("445 active levels", roster(entd, e, active, 0x03) == [104, 102, 102, 102, 102, 101])
    check("445 active job levels", roster(entd, e, active, 0x09) == [8, 8, 8, 8, 8, 1])
    check("445 active secondaries", roster(entd, e, active, 0x0B) == [10, 10, 10, 6, 6, 6])
    check("445 Brave targets", roster(entd, e, active, 0x06) == [72, 68, 72, 88, 88, 88])
    check("445 Faith targets", roster(entd, e, active, 0x07) == [82, 78, 82, 42, 42, 42])

    check("445 Zalmo R/S/M and robe",
          field16(entd, e, 1, 0x0C) == 449
          and field16(entd, e, 1, 0x0E) == 467
          and field16(entd, e, 1, 0x10) == 486
          and field(entd, e, 1, 0x13) == 206)

    for slot_no in (2, 3):
        check(f"445 s{slot_no} Mystic R/S/M",
              field16(entd, e, slot_no, 0x0C) == 449
              and field16(entd, e, slot_no, 0x0E) == 467
              and field16(entd, e, slot_no, 0x10) == 486)
        check(f"445 s{slot_no} Mystic gear",
              roster(entd, e, [slot_no], 0x12) == [167]
              and roster(entd, e, [slot_no], 0x13) == [206]
              and roster(entd, e, [slot_no], 0x14) == [234]
              and roster(entd, e, [slot_no], 0x15) == [56]
              and roster(entd, e, [slot_no], 0x16) == [255])

    for slot_no in (4, 5, 6):
        check(f"445 s{slot_no} Knight R/S/M",
              field16(entd, e, slot_no, 0x0C) == 442
              and field16(entd, e, slot_no, 0x0E) == 465
              and field16(entd, e, slot_no, 0x10) == 486)
        check(f"445 s{slot_no} Knight gear",
              roster(entd, e, [slot_no], 0x12) == [154]
              and roster(entd, e, [slot_no], 0x13) == [182]
              and roster(entd, e, [slot_no], 0x14) == [218]
              and roster(entd, e, [slot_no], 0x15) == [30]
              and roster(entd, e, [slot_no], 0x16) == [139])
    check("445 reward spoils preserved", roster(entd, e, active, 0x1E) == [223, 206, 0, 0, 0, 0])

    # 042 - Beddha Sandwaste / Bed Desert, entry 447.
    # Six active enemies plus two Barich script placeholders. Keep the gun duel focused on Barich.
    e = 447
    active = [0, 1, 2, 3, 4, 5]
    check("447 active jobs", roster(entd, e, active, 0x0A) == [43, 76, 76, 80, 77, 77])
    check("447 active levels", roster(entd, e, active, 0x03) == [104, 102, 102, 102, 102, 101])
    check("447 active job levels", roster(entd, e, active, 0x09) == [8, 8, 8, 8, 8, 8])
    check("447 active secondaries", roster(entd, e, active, 0x0B) == [6, 6, 6, 6, 6, 6])
    check("447 Brave targets", roster(entd, e, active, 0x06) == [84, 88, 88, 60, 82, 82])
    check("447 Faith targets", roster(entd, e, active, 0x07) == [55, 42, 42, 84, 45, 45])

    check("447 Barich boss R/S/M and Glacial Gun",
          field16(entd, e, 0, 0x0C) == 449
          and field16(entd, e, 0, 0x0E) == 469
          and field16(entd, e, 0, 0x10) == 486
          and field(entd, e, 0, 0x15) == 74)

    for slot_no in (1, 2):
        check(f"447 s{slot_no} Knight R/S/M",
              field16(entd, e, slot_no, 0x0C) == 442
              and field16(entd, e, slot_no, 0x0E) == 465
              and field16(entd, e, slot_no, 0x10) == 486)
        check(f"447 s{slot_no} Knight gear",
              roster(entd, e, [slot_no], 0x12) == [154]
              and roster(entd, e, [slot_no], 0x13) == [182]
              and roster(entd, e, [slot_no], 0x14) == [218]
              and roster(entd, e, [slot_no], 0x15) == [30]
              and roster(entd, e, [slot_no], 0x16) == [139])

    check("447 s3 Black Mage R/S/M",
          field16(entd, e, 3, 0x0C) == 449
          and field16(entd, e, 3, 0x0E) == 467
          and field16(entd, e, 3, 0x10) == 486)
    check("447 s3 Black Mage gear",
          roster(entd, e, [3], 0x12) == [167]
          and roster(entd, e, [3], 0x13) == [206]
          and roster(entd, e, [3], 0x14) == [234]
          and roster(entd, e, [3], 0x15) == [56]
          and roster(entd, e, [3], 0x16) == [255])

    for slot_no in (4, 5):
        check(f"447 s{slot_no} Archer R/S/M",
              field16(entd, e, slot_no, 0x0C) == 449
              and field16(entd, e, slot_no, 0x0E) == 469
              and field16(entd, e, slot_no, 0x10) == 486)
        check(f"447 s{slot_no} Archer gear",
              roster(entd, e, [slot_no], 0x12) == [168]
              and roster(entd, e, [slot_no], 0x13) == [198]
              and roster(entd, e, [slot_no], 0x14) == [218]
              and roster(entd, e, [slot_no], 0x15) == [87]
              and roster(entd, e, [slot_no], 0x16) == [254])

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
    check("448 South active jobs", roster(entd, e, active, 0x0A) == [76, 76, 76, 77, 77, 89, 83])
    check("448 South active levels", roster(entd, e, active, 0x03) == [102, 102, 101, 102, 101, 102, 101])
    check("448 South job levels", roster(entd, e, active, 0x09) == [8, 8, 1, 8, 8, 8, 8])
    check("448 South secondaries", roster(entd, e, active, 0x0B) == [6, 6, 6, 6, 6, 6, 6])
    check("448 South Brave targets", roster(entd, e, active, 0x06) == [88, 88, 88, 82, 82, 90, 88])
    check("448 South Faith targets", roster(entd, e, active, 0x07) == [42, 42, 42, 45, 45, 35, 38])

    for slot_no in (0, 1, 2):
        check(f"448 s{slot_no} Knight R/S/M",
              field16(entd, e, slot_no, 0x0C) == 442
              and field16(entd, e, slot_no, 0x0E) == 465
              and field16(entd, e, slot_no, 0x10) == 486)
        check(f"448 s{slot_no} Knight gear",
              roster(entd, e, [slot_no], 0x12) == [154]
              and roster(entd, e, [slot_no], 0x13) == [182]
              and roster(entd, e, [slot_no], 0x14) == [218]
              and roster(entd, e, [slot_no], 0x15) == [30]
              and roster(entd, e, [slot_no], 0x16) == [139])

    for slot_no, bow in ((3, 90), (4, 91)):
        check(f"448 s{slot_no} Archer R/S/M and bow",
              field16(entd, e, slot_no, 0x0C) == 449
              and field16(entd, e, slot_no, 0x0E) == 469
              and field16(entd, e, slot_no, 0x10) == 486
              and field(entd, e, slot_no, 0x15) == bow)
        check(f"448 s{slot_no} Archer gear",
              roster(entd, e, [slot_no], 0x12) == [168]
              and roster(entd, e, [slot_no], 0x13) == [198]
              and roster(entd, e, [slot_no], 0x14) == [218]
              and roster(entd, e, [slot_no], 0x16) == [254])

    check("448 s5 Ninja R/S/M and gear",
          field16(entd, e, 5, 0x0C) == 453
          and field16(entd, e, 5, 0x0E) == 465
          and field16(entd, e, 5, 0x10) == 487
          and roster(entd, e, [5], 0x12) == [168]
          and roster(entd, e, [5], 0x13) == [198]
          and roster(entd, e, [5], 0x14) == [210]
          and roster(entd, e, [5], 0x15) == [14]
          and roster(entd, e, [5], 0x16) == [14])
    check("448 s6 Thief R/S/M and gear",
          field16(entd, e, 6, 0x0C) == 453
          and field16(entd, e, 6, 0x0E) == 465
          and field16(entd, e, 6, 0x10) == 487
          and roster(entd, e, [6], 0x12) == [168]
          and roster(entd, e, [6], 0x13) == [198]
          and roster(entd, e, [6], 0x14) == [210]
          and roster(entd, e, [6], 0x15) == [9]
          and roster(entd, e, [6], 0x16) == [255])
    check("448 bow spoils preserved",
          field(entd, e, 3, 0x1E) == 90
          and field(entd, e, 4, 0x1E) == 91)

    e = 449
    active = [0, 1, 2, 3, 4, 5]
    check("449 North active jobs", roster(entd, e, active, 0x0A) == [77, 87, 87, 77, 82, 78])
    check("449 North active levels", roster(entd, e, active, 0x03) == [102, 102, 101, 101, 102, 102])
    check("449 North job levels", roster(entd, e, active, 0x09) == [8, 8, 8, 8, 8, 8])
    check("449 North secondaries", roster(entd, e, active, 0x0B) == [6, 6, 6, 6, 10, 6])
    check("449 North Brave targets", roster(entd, e, active, 0x06) == [82, 86, 86, 82, 60, 88])
    check("449 North Faith targets", roster(entd, e, active, 0x07) == [45, 40, 40, 45, 84, 40])

    for slot_no, bow in ((0, 90), (3, 91)):
        check(f"449 s{slot_no} Archer R/S/M and bow",
              field16(entd, e, slot_no, 0x0C) == 449
              and field16(entd, e, slot_no, 0x0E) == 469
              and field16(entd, e, slot_no, 0x10) == 486
              and field(entd, e, slot_no, 0x15) == bow)
        check(f"449 s{slot_no} Archer gear",
              roster(entd, e, [slot_no], 0x12) == [168]
              and roster(entd, e, [slot_no], 0x13) == [198]
              and roster(entd, e, [slot_no], 0x14) == [218]
              and roster(entd, e, [slot_no], 0x16) == [254])

    for slot_no in (1, 2):
        check(f"449 s{slot_no} Dragoon R/S/M",
              field16(entd, e, slot_no, 0x0C) == 449
              and field16(entd, e, slot_no, 0x0E) == 465
              and field16(entd, e, slot_no, 0x10) == 486)
        check(f"449 s{slot_no} Dragoon gear",
              roster(entd, e, [slot_no], 0x12) == [154]
              and roster(entd, e, [slot_no], 0x13) == [182]
              and roster(entd, e, [slot_no], 0x14) == [210]
              and roster(entd, e, [slot_no], 0x15) == [102]
              and roster(entd, e, [slot_no], 0x16) == [139])

    check("449 s4 Summoner R/S/M and gear",
          field16(entd, e, 4, 0x0C) == 449
          and field16(entd, e, 4, 0x0E) == 467
          and field16(entd, e, 4, 0x10) == 486
          and roster(entd, e, [4], 0x12) == [167]
          and roster(entd, e, [4], 0x13) == [206]
          and roster(entd, e, [4], 0x14) == [234]
          and roster(entd, e, [4], 0x15) == [56]
          and roster(entd, e, [4], 0x16) == [255])
    check("449 s5 Monk R/S/M and gear",
          field16(entd, e, 5, 0x0C) == 442
          and field16(entd, e, 5, 0x0E) == 465
          and field16(entd, e, 5, 0x10) == 486
          and roster(entd, e, [5], 0x13) == [195]
          and roster(entd, e, [5], 0x14) == [218])
    check("449 bow spoils preserved",
          field(entd, e, 0, 0x1E) == 90
          and field(entd, e, 3, 0x1E) == 91)

    # 044 - Fort Besselat Sluice Gate, entry 450.
    # Lever objective race: one Slow/Haste/Float Time Mage, one Black Mage, two Rend Knights, two bodyguards.
    e = 450
    active = [0, 1, 2, 3, 4, 5, 6, 7]
    check("450 active jobs", roster(entd, e, active, 0x0A) == [77, 77, 76, 76, 80, 81, 76, 76])
    check("450 active levels", roster(entd, e, active, 0x03) == [102, 101, 102, 102, 102, 102, 101, 101])
    check("450 active job levels", roster(entd, e, active, 0x09) == [8, 8, 8, 8, 8, 4, 1, 1])
    check("450 active secondaries", roster(entd, e, active, 0x0B) == [6, 6, 6, 6, 6, 6, 6, 6])
    check("450 Brave targets", roster(entd, e, active, 0x06) == [82, 82, 88, 88, 60, 62, 88, 88])
    check("450 Faith targets", roster(entd, e, active, 0x07) == [45, 45, 42, 42, 84, 80, 42, 42])

    for slot_no in (0, 1):
        check(f"450 s{slot_no} Archer R/S/M",
              field16(entd, e, slot_no, 0x0C) == 449
              and field16(entd, e, slot_no, 0x0E) == 469
              and field16(entd, e, slot_no, 0x10) == 486)
        check(f"450 s{slot_no} Archer gear",
              roster(entd, e, [slot_no], 0x12) == [168]
              and roster(entd, e, [slot_no], 0x13) == [198]
              and roster(entd, e, [slot_no], 0x14) == [218]
              and roster(entd, e, [slot_no], 0x15) == [87]
              and roster(entd, e, [slot_no], 0x16) == [254])

    for slot_no, shield in ((2, 141), (3, 139), (6, 139), (7, 139)):
        check(f"450 s{slot_no} Knight R/S/M",
              field16(entd, e, slot_no, 0x0C) == 442
              and field16(entd, e, slot_no, 0x0E) == 465
              and field16(entd, e, slot_no, 0x10) == 486)
        check(f"450 s{slot_no} Knight gear",
              roster(entd, e, [slot_no], 0x12) == [154]
              and roster(entd, e, [slot_no], 0x13) == [182]
              and roster(entd, e, [slot_no], 0x14) == [218]
              and roster(entd, e, [slot_no], 0x15) == [30]
              and roster(entd, e, [slot_no], 0x16) == [shield])

    check("450 s4 Black Mage R/S/M and gear",
          field16(entd, e, 4, 0x0C) == 449
          and field16(entd, e, 4, 0x0E) == 467
          and field16(entd, e, 4, 0x10) == 486
          and roster(entd, e, [4], 0x12) == [167]
          and roster(entd, e, [4], 0x13) == [206]
          and roster(entd, e, [4], 0x14) == [234]
          and roster(entd, e, [4], 0x15) == [56]
          and roster(entd, e, [4], 0x16) == [255])
    check("450 s5 Time Mage R/S/M and gear",
          field16(entd, e, 5, 0x0C) == 449
          and field16(entd, e, 5, 0x0E) == 467
          and field16(entd, e, 5, 0x10) == 486
          and roster(entd, e, [5], 0x12) == [167]
          and roster(entd, e, [5], 0x13) == [206]
          and roster(entd, e, [5], 0x14) == [234]
          and roster(entd, e, [5], 0x15) == [64]
          and roster(entd, e, [5], 0x16) == [255])
    check("450 Kaiser Shield spoil preserved", field(entd, e, 2, 0x1E) == 141)

    # 045 - Mount Germinas, entry 452.
    # Vertical mobility skirmish: two Ninjas, one Thief, three Archers; ninja arsenal paid via spoils.
    e = 452
    active = [0, 1, 2, 3, 4, 5]
    check("452 active jobs", roster(entd, e, active, 0x0A) == [89, 89, 83, 77, 77, 77])
    check("452 active levels", roster(entd, e, active, 0x03) == [103, 102, 101, 102, 101, 101])
    check("452 active job levels", roster(entd, e, active, 0x09) == [8, 8, 8, 8, 8, 8])
    check("452 active secondaries", roster(entd, e, active, 0x0B) == [6, 6, 6, 6, 6, 6])
    check("452 Brave targets", roster(entd, e, active, 0x06) == [90, 90, 88, 82, 82, 82])
    check("452 Faith targets", roster(entd, e, active, 0x07) == [35, 35, 38, 45, 45, 45])

    check("452 s0 Apex Ninja R/S/M and visible Ninja Gear",
          field16(entd, e, 0, 0x0C) == 453
          and field16(entd, e, 0, 0x0E) == 465
          and field16(entd, e, 0, 0x10) == 487
          and roster(entd, e, [0], 0x12) == [168]
          and roster(entd, e, [0], 0x13) == [197]
          and roster(entd, e, [0], 0x14) == [210]
          and roster(entd, e, [0], 0x15) == [14]
          and roster(entd, e, [0], 0x16) == [14])
    check("452 s1 Ninja R/S/M and visible Koga",
          field16(entd, e, 1, 0x0C) == 453
          and field16(entd, e, 1, 0x0E) == 465
          and field16(entd, e, 1, 0x10) == 487
          and roster(entd, e, [1], 0x12) == [168]
          and roster(entd, e, [1], 0x13) == [198]
          and roster(entd, e, [1], 0x14) == [210]
          and roster(entd, e, [1], 0x15) == [18]
          and roster(entd, e, [1], 0x16) == [14])
    check("452 s2 Thief R/S/M and legal gear",
          field16(entd, e, 2, 0x0C) == 453
          and field16(entd, e, 2, 0x0E) == 465
          and field16(entd, e, 2, 0x10) == 487
          and roster(entd, e, [2], 0x12) == [168]
          and roster(entd, e, [2], 0x13) == [198]
          and roster(entd, e, [2], 0x14) == [210]
          and roster(entd, e, [2], 0x15) == [9]
          and roster(entd, e, [2], 0x16) == [255])

    for slot_no in (3, 4, 5):
        check(f"452 s{slot_no} Archer R/S/M",
              field16(entd, e, slot_no, 0x0C) == 449
              and field16(entd, e, slot_no, 0x0E) == 469
              and field16(entd, e, slot_no, 0x10) == 486)
        check(f"452 s{slot_no} Archer gear",
              roster(entd, e, [slot_no], 0x12) == [168]
              and roster(entd, e, [slot_no], 0x13) == [198]
              and roster(entd, e, [slot_no], 0x14) == [218]
              and roster(entd, e, [slot_no], 0x15) == [87]
              and roster(entd, e, [slot_no], 0x16) == [254])

    check("452 ninja arsenal spoils preserved",
          field(entd, e, 0, 0x1E) == 197
          and field(entd, e, 1, 0x1E) == 18
          and field(entd, e, 2, 0x1E) == 17)

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
