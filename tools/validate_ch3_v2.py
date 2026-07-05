#!/usr/bin/env python3
"""Validate implemented Chapter 3 v2 battle data.

This is an objective binary/source validator for docs/battles/025-035. It should grow one battle at
a time as each Chapter 3 redesign is implemented. It does not judge balance; in-game balance remains
a playtest task.
"""

from __future__ import annotations

from pathlib import Path


ENTRY = 0x280
SLOT = 0x28
ENTD = Path("src/fftivc.battles.ngplus/entd/battle_entd4_ent.bin")
RUNTIME = Path("src/fftivc.battles.ngplus/RuntimeGenericStatScaler.cs")


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
    runtime = RUNTIME.read_text(encoding="utf-8")
    checks: list[tuple[str, bool]] = []

    def check(name: str, condition: bool) -> None:
        checks.append((name, condition))

    # 025 - Mining Town of Gollund, entry 417.
    # s0 Orran protected guest; s1/s4/s5 Thief; s2/s3 Chemist; s6 Orator.
    check("417 runtime pass starts at Chapter 3 opener", "FIRST_CHAPTER3_ENTRY = 417" in runtime)
    check("417 runtime target table present", "[417] = Targets(" in runtime)
    check("417 runtime target includes Orran guest", 'GuestUnit(0x15, 0x15, 0x15, "Orran protected guest")' in runtime)
    for uid in (0x80, 0x81, 0x82, 0x83, 0x84, 0x85):
        check(f"417 runtime target includes enemy uid 0x{uid:02X}", f"EnemyUnit(0x{uid:02X}" in runtime)

    check("417 Orran identity preserved", field(entd, 417, 0, 0x00) == 0x15 and field(entd, 417, 0, 0x0A) == 0x15)
    check("417 Orran level/control", field(entd, 417, 0, 0x03) == 100 and (field(entd, 417, 0, 0x18) & 0x08) != 0)
    check("417 Orran Brave/Faith", (field(entd, 417, 0, 0x06), field(entd, 417, 0, 0x07)) == (65, 75))

    enemy_slots = [1, 2, 3, 4, 5, 6]
    check("417 roster jobs", roster(entd, 417, enemy_slots, 0x0A) == [83, 75, 75, 83, 83, 84])
    check("417 roster levels", roster(entd, 417, enemy_slots, 0x03) == [101, 101, 101, 101, 100, 102])
    check("417 roster secondaries", roster(entd, 417, enemy_slots, 0x0B) == [6, 5, 5, 6, 6, 6])
    check("417 roster Brave", roster(entd, 417, enemy_slots, 0x06) == [84, 68, 68, 84, 84, 65])
    check("417 roster Faith", roster(entd, 417, enemy_slots, 0x07) == [42, 64, 64, 42, 42, 72])
    for slot_no in enemy_slots:
        job = field(entd, 417, slot_no, 0x0A)
        check(f"417 s{slot_no} jobrank", field(entd, 417, slot_no, 0x08) == rank(job))
        check(f"417 s{slot_no} JobLevel 8", field(entd, 417, slot_no, 0x09) == 8)

    for slot_no in (1, 4, 5):
        check(f"417 s{slot_no} Thief R/S/M",
              field16(entd, 417, slot_no, 0x0C) == 453
              and field16(entd, 417, slot_no, 0x0E) == 465
              and field16(entd, 417, slot_no, 0x10) == 487)
        check(f"417 s{slot_no} Thief gear",
              roster(entd, 417, [slot_no], 0x12) == [168]
              and roster(entd, 417, [slot_no], 0x13) == [198]
              and roster(entd, 417, [slot_no], 0x14) == [210]
              and roster(entd, 417, [slot_no], 0x15) == [9])

    for slot_no in (2, 3):
        check(f"417 s{slot_no} Chemist R/S/M",
              field16(entd, 417, slot_no, 0x0C) == 441
              and field16(entd, 417, slot_no, 0x0E) == 474
              and field16(entd, 417, slot_no, 0x10) == 486)
        check(f"417 s{slot_no} Chemist gear",
              roster(entd, 417, [slot_no], 0x12) == [167]
              and roster(entd, 417, [slot_no], 0x13) == [198]
              and roster(entd, 417, [slot_no], 0x14) == [218]
              and roster(entd, 417, [slot_no], 0x15) == [72])

    check("417 Orator R/S/M",
          field16(entd, 417, 6, 0x0C) == 453
          and field16(entd, 417, 6, 0x0E) == 465
          and field16(entd, 417, 6, 0x10) == 486)
    check("417 Orator gear",
          roster(entd, 417, [6], 0x12) == [167]
          and roster(entd, 417, [6], 0x13) == [206]
          and roster(entd, 417, [6], 0x14) == [210]
          and roster(entd, 417, [6], 0x15) == [72])

    # 026 - Lesalia Castle Postern, entry 420.
    # s0 Alma support guest; s1 Zalmo retreating Inquisitor; s2/s3/s5 Knight; s4/s6 Monk.
    check("420 runtime target table present", "[420] = Targets(" in runtime)
    check("420 runtime target includes Alma guest", 'GuestUnit(0x30, 0x30, 0x30, "Alma support guest")' in runtime)
    for uid in (0x80, 0x81, 0x82, 0x83, 0x84):
        check(f"420 runtime target includes enemy uid 0x{uid:02X}", f"EnemyUnit(0x{uid:02X}" in runtime)

    check("420 Alma identity preserved", field(entd, 420, 0, 0x00) == 0x30 and field(entd, 420, 0, 0x0A) == 0x30)
    check("420 Alma level/control", field(entd, 420, 0, 0x03) == 100 and (field(entd, 420, 0, 0x18) & 0x08) != 0)
    check("420 Alma Brave/Faith", (field(entd, 420, 0, 0x06), field(entd, 420, 0, 0x07)) == (60, 78))

    check("420 Zalmo identity preserved", field(entd, 420, 1, 0x00) == 0x10 and field(entd, 420, 1, 0x0A) == 0x10)
    check("420 Zalmo level secondary Br/Fa",
          field(entd, 420, 1, 0x03) == 103
          and field(entd, 420, 1, 0x0B) == 6
          and (field(entd, 420, 1, 0x06), field(entd, 420, 1, 0x07)) == (70, 78))
    check("420 Zalmo special R/S/M preserved",
          field16(entd, 420, 1, 0x0C) == 452
          and field16(entd, 420, 1, 0x0E) == 462
          and field16(entd, 420, 1, 0x10) == 493)

    lesalia_enemy_slots = [2, 3, 4, 5, 6]
    check("420 roster jobs", roster(entd, 420, lesalia_enemy_slots, 0x0A) == [76, 76, 78, 76, 78])
    check("420 roster levels", roster(entd, 420, lesalia_enemy_slots, 0x03) == [101, 101, 101, 101, 101])
    check("420 roster secondaries", roster(entd, 420, lesalia_enemy_slots, 0x0B) == [6, 6, 6, 5, 6])
    check("420 roster Brave", roster(entd, 420, lesalia_enemy_slots, 0x06) == [84, 84, 84, 84, 84])
    check("420 roster Faith", roster(entd, 420, lesalia_enemy_slots, 0x07) == [45, 45, 42, 45, 42])
    for slot_no in lesalia_enemy_slots:
        job = field(entd, 420, slot_no, 0x0A)
        check(f"420 s{slot_no} jobrank", field(entd, 420, slot_no, 0x08) == rank(job))
        check(f"420 s{slot_no} JobLevel 8", field(entd, 420, slot_no, 0x09) == 8)

    for slot_no in (2, 3, 5):
        check(f"420 s{slot_no} Knight R/S/M",
              field16(entd, 420, slot_no, 0x0C) == 442
              and field16(entd, 420, slot_no, 0x0E) == 465
              and field16(entd, 420, slot_no, 0x10) == 486)
        check(f"420 s{slot_no} Knight gear",
              roster(entd, 420, [slot_no], 0x12) == [154]
              and roster(entd, 420, [slot_no], 0x13) == [182]
              and roster(entd, 420, [slot_no], 0x14) == [218]
              and roster(entd, 420, [slot_no], 0x15) == [30]
              and roster(entd, 420, [slot_no], 0x16) == [135])

    for slot_no in (4, 6):
        check(f"420 s{slot_no} Monk R/S/M",
              field16(entd, 420, slot_no, 0x0C) == 442
              and field16(entd, 420, slot_no, 0x0E) == 465
              and field16(entd, 420, slot_no, 0x10) == 486)
        check(f"420 s{slot_no} Monk gear",
              roster(entd, 420, [slot_no], 0x12) == [254]
              and roster(entd, 420, [slot_no], 0x13) == [195]
              and roster(entd, 420, [slot_no], 0x14) == [218]
              and roster(entd, 420, [slot_no], 0x15) == [254])

    # 027 - Monastery Vaults 2nd Level, entry 422.
    # s0 Nightblade special is preserved; s1/s2/s3 Dragoon; s4 Chemist; s5/s6 Time Mage.
    check("422 runtime target table present", "[422] = Targets(" in runtime)
    for uid in (0x80, 0x81, 0x82, 0x83, 0x84, 0x85):
        check(f"422 runtime target includes enemy uid 0x{uid:02X}", f"EnemyUnit(0x{uid:02X}" in runtime)

    check("422 Nightblade identity preserved", field(entd, 422, 0, 0x00) == 0x26 and field(entd, 422, 0, 0x0A) == 0x26)
    check("422 Nightblade level Br/Fa",
          field(entd, 422, 0, 0x03) == 102
          and (field(entd, 422, 0, 0x06), field(entd, 422, 0, 0x07)) == (84, 55))

    vaults_enemy_slots = [1, 2, 3, 4, 5, 6]
    check("422 roster jobs", roster(entd, 422, vaults_enemy_slots, 0x0A) == [87, 87, 87, 75, 81, 81])
    check("422 roster levels", roster(entd, 422, vaults_enemy_slots, 0x03) == [102, 101, 100, 101, 101, 101])
    check("422 roster secondaries", roster(entd, 422, vaults_enemy_slots, 0x0B) == [6, 6, 6, 5, 6, 6])
    check("422 roster Brave", roster(entd, 422, vaults_enemy_slots, 0x06) == [84, 84, 84, 68, 60, 60])
    check("422 roster Faith", roster(entd, 422, vaults_enemy_slots, 0x07) == [72, 72, 72, 64, 74, 74])
    for slot_no in vaults_enemy_slots:
        job = field(entd, 422, slot_no, 0x0A)
        check(f"422 s{slot_no} jobrank", field(entd, 422, slot_no, 0x08) == rank(job))

    check("422 all Dragoons Dragonheart",
          [field16(entd, 422, slot_no, 0x0C) for slot_no in (1, 2, 3)] == [427, 427, 427])
    for slot_no in (1, 2, 3):
        check(f"422 s{slot_no} Dragoon JobLevel", field(entd, 422, slot_no, 0x09) == 8)
        check(f"422 s{slot_no} Dragoon R/S/M",
              field16(entd, 422, slot_no, 0x0C) == 427
              and field16(entd, 422, slot_no, 0x0E) == 469
              and field16(entd, 422, slot_no, 0x10) == 492)
        check(f"422 s{slot_no} Dragoon gear",
              roster(entd, 422, [slot_no], 0x12) == [154]
              and roster(entd, 422, [slot_no], 0x13) == [182]
              and roster(entd, 422, [slot_no], 0x14) == [213]
              and roster(entd, 422, [slot_no], 0x15) == [102]
              and roster(entd, 422, [slot_no], 0x16) == [139])

    check("422 Chemist JobLevel", field(entd, 422, 4, 0x09) == 8)
    check("422 Chemist R/S/M",
          field16(entd, 422, 4, 0x0C) == 441
          and field16(entd, 422, 4, 0x0E) == 466
          and field16(entd, 422, 4, 0x10) == 487)
    check("422 Chemist gear",
          roster(entd, 422, [4], 0x12) == [167]
          and roster(entd, 422, [4], 0x13) == [198]
          and roster(entd, 422, [4], 0x14) == [234]
          and roster(entd, 422, [4], 0x15) == [72]
          and roster(entd, 422, [4], 0x16) == [254])

    for slot_no in (5, 6):
        check(f"422 s{slot_no} Time Mage JobLevel cap", field(entd, 422, slot_no, 0x09) == 4)
        check(f"422 s{slot_no} Time Mage R/S/M",
              field16(entd, 422, slot_no, 0x0C) == 445
              and field16(entd, 422, slot_no, 0x0E) == 467
              and field16(entd, 422, slot_no, 0x10) == 494)
        check(f"422 s{slot_no} Time Mage gear",
              roster(entd, 422, [slot_no], 0x12) == [167]
              and roster(entd, 422, [slot_no], 0x13) == [206]
              and roster(entd, 422, [slot_no], 0x14) == [234]
              and roster(entd, 422, [slot_no], 0x15) == [64]
              and roster(entd, 422, [slot_no], 0x16) == [255])

    # 028 - Monastery Vaults 3rd Level, entry 423.
    # s0 Izlude special sub-boss is preserved; s1/s2 Knight; s3 Summoner; s4/s5 Archer.
    check("423 runtime target table present", "[423] = Targets(" in runtime)
    check("423 runtime target excludes Izlude special", "EnemyUnit(0x26" not in runtime)
    for uid in (0x80, 0x81, 0x82, 0x83, 0x84):
        check(f"423 runtime target includes enemy uid 0x{uid:02X}", f"EnemyUnit(0x{uid:02X}" in runtime)

    check("423 Izlude identity preserved", field(entd, 423, 0, 0x00) == 0x26 and field(entd, 423, 0, 0x0A) == 0x26)
    check("423 Izlude level secondary Br/Fa",
          field(entd, 423, 0, 0x03) == 103
          and field(entd, 423, 0, 0x09) == 8
          and field(entd, 423, 0, 0x0B) == 52
          and (field(entd, 423, 0, 0x06), field(entd, 423, 0, 0x07)) == (86, 55))
    check("423 Izlude special R/S/M preserved",
          field16(entd, 423, 0, 0x0C) == 442
          and field16(entd, 423, 0, 0x0E) == 465
          and field16(entd, 423, 0, 0x10) == 492)
    check("423 Izlude Reflect Mail kit",
          roster(entd, 423, [0], 0x13) == [184]
          and roster(entd, 423, [0], 0x14) == [218]
          and roster(entd, 423, [0], 0x15) == [33])

    vaults3_enemy_slots = [1, 2, 3, 4, 5]
    check("423 roster jobs", roster(entd, 423, vaults3_enemy_slots, 0x0A) == [76, 76, 82, 77, 77])
    check("423 roster levels", roster(entd, 423, vaults3_enemy_slots, 0x03) == [101, 101, 101, 101, 100])
    check("423 roster secondaries", roster(entd, 423, vaults3_enemy_slots, 0x0B) == [12, 12, 6, 8, 8])
    check("423 roster Brave", roster(entd, 423, vaults3_enemy_slots, 0x06) == [86, 84, 58, 80, 80])
    check("423 roster Faith", roster(entd, 423, vaults3_enemy_slots, 0x07) == [55, 45, 78, 45, 45])
    for slot_no in vaults3_enemy_slots:
        job = field(entd, 423, slot_no, 0x0A)
        check(f"423 s{slot_no} jobrank", field(entd, 423, slot_no, 0x08) == rank(job))
        check(f"423 s{slot_no} JobLevel 8", field(entd, 423, slot_no, 0x09) == 8)

    for slot_no in (1, 2):
        check(f"423 s{slot_no} Knight R/S/M",
              field16(entd, 423, slot_no, 0x0C) == 453
              and field16(entd, 423, slot_no, 0x0E) == 465
              and field16(entd, 423, slot_no, 0x10) == 487)
        check(f"423 s{slot_no} Knight gear",
              roster(entd, 423, [slot_no], 0x12) == [154]
              and roster(entd, 423, [slot_no], 0x13) == [182]
              and roster(entd, 423, [slot_no], 0x14) == [218]
              and roster(entd, 423, [slot_no], 0x15) == [30]
              and roster(entd, 423, [slot_no], 0x16) == [139])

    check("423 Summoner R/S/M",
          field16(entd, 423, 3, 0x0C) == 449
          and field16(entd, 423, 3, 0x0E) == 482
          and field16(entd, 423, 3, 0x10) == 498)
    check("423 Summoner gear",
          roster(entd, 423, [3], 0x12) == [167]
          and roster(entd, 423, [3], 0x13) == [206]
          and roster(entd, 423, [3], 0x14) == [234]
          and roster(entd, 423, [3], 0x15) == [56]
          and roster(entd, 423, [3], 0x16) == [255])

    for slot_no in (4, 5):
        check(f"423 s{slot_no} Archer R/S/M",
              field16(entd, 423, slot_no, 0x0C) == 449
              and field16(entd, 423, slot_no, 0x0E) == 469
              and field16(entd, 423, slot_no, 0x10) == 490)
        check(f"423 s{slot_no} Archer gear",
              roster(entd, 423, [slot_no], 0x12) == [168]
              and roster(entd, 423, [slot_no], 0x13) == [198]
              and roster(entd, 423, [slot_no], 0x14) == [218]
              and roster(entd, 423, [slot_no], 0x15) == [87]
              and roster(entd, 423, [slot_no], 0x16) == [254])

    # 029 - Monastery Vaults 1st Level, entry 424.
    # s0 Wiegraf special boss flees; s1/s2 Knight; s3/s5 Archer; s4 Black Mage; s6/s7 inactive.
    check("424 runtime target table present", "[424] = Targets(" in runtime)
    check("424 runtime target excludes Wiegraf special", "EnemyUnit(0x28" not in runtime)
    for uid in (0x80, 0x81, 0x82, 0x83, 0x84):
        check(f"424 runtime target includes enemy uid 0x{uid:02X}", f"EnemyUnit(0x{uid:02X}" in runtime)

    check("424 Wiegraf identity preserved", field(entd, 424, 0, 0x00) == 0x28 and field(entd, 424, 0, 0x0A) == 0x28)
    check("424 Wiegraf level secondary Br/Fa",
          field(entd, 424, 0, 0x03) == 104
          and field(entd, 424, 0, 0x09) == 8
          and field(entd, 424, 0, 0x0B) == 5
          and (field(entd, 424, 0, 0x06), field(entd, 424, 0, 0x07)) == (88, 60))
    check("424 Wiegraf disarmable boss kit",
          field16(entd, 424, 0, 0x0C) == 442
          and field16(entd, 424, 0, 0x0E) == 465
          and field16(entd, 424, 0, 0x10) == 486
          and roster(entd, 424, [0], 0x12) == [154]
          and roster(entd, 424, [0], 0x13) == [182]
          and roster(entd, 424, [0], 0x14) == [218]
          and roster(entd, 424, [0], 0x15) == [30]
          and roster(entd, 424, [0], 0x16) == [139])
    check("424 Wiegraf no Safeguard", field16(entd, 424, 0, 0x0E) != 475)

    vaults1_enemy_slots = [1, 2, 3, 4, 5]
    check("424 roster jobs", roster(entd, 424, vaults1_enemy_slots, 0x0A) == [76, 76, 77, 80, 77])
    check("424 roster levels", roster(entd, 424, vaults1_enemy_slots, 0x03) == [101, 101, 101, 101, 100])
    check("424 roster secondaries", roster(entd, 424, vaults1_enemy_slots, 0x0B) == [6, 5, 5, 6, 5])
    check("424 roster Brave", roster(entd, 424, vaults1_enemy_slots, 0x06) == [84, 84, 80, 58, 80])
    check("424 roster Faith", roster(entd, 424, vaults1_enemy_slots, 0x07) == [45, 45, 45, 78, 45])
    for slot_no in vaults1_enemy_slots:
        job = field(entd, 424, slot_no, 0x0A)
        check(f"424 s{slot_no} jobrank", field(entd, 424, slot_no, 0x08) == rank(job))
        check(f"424 s{slot_no} JobLevel 8", field(entd, 424, slot_no, 0x09) == 8)

    for slot_no in (1, 2):
        check(f"424 s{slot_no} Knight R/S/M",
              field16(entd, 424, slot_no, 0x0C) == 442
              and field16(entd, 424, slot_no, 0x0E) == 465
              and field16(entd, 424, slot_no, 0x10) == 486)
        check(f"424 s{slot_no} Knight gear",
              roster(entd, 424, [slot_no], 0x12) == [154]
              and roster(entd, 424, [slot_no], 0x13) == [182]
              and roster(entd, 424, [slot_no], 0x14) == [218]
              and roster(entd, 424, [slot_no], 0x15) == [30]
              and roster(entd, 424, [slot_no], 0x16) == [139])

    check("424 Black Mage R/S/M",
          field16(entd, 424, 4, 0x0C) == 449
          and field16(entd, 424, 4, 0x0E) == 467
          and field16(entd, 424, 4, 0x10) == 486)
    check("424 Black Mage gear",
          roster(entd, 424, [4], 0x12) == [167]
          and roster(entd, 424, [4], 0x13) == [206]
          and roster(entd, 424, [4], 0x14) == [234]
          and roster(entd, 424, [4], 0x15) == [56]
          and roster(entd, 424, [4], 0x16) == [255])

    for slot_no in (3, 5):
        check(f"424 s{slot_no} Archer R/S/M",
              field16(entd, 424, slot_no, 0x0C) == 449
              and field16(entd, 424, slot_no, 0x0E) == 469
              and field16(entd, 424, slot_no, 0x10) == 486)
        check(f"424 s{slot_no} Archer gear",
              roster(entd, 424, [slot_no], 0x12) == [168]
              and roster(entd, 424, [slot_no], 0x13) == [198]
              and roster(entd, 424, [slot_no], 0x14) == [218]
              and roster(entd, 424, [slot_no], 0x15) == [87]
              and roster(entd, 424, [slot_no], 0x16) == [254])

    for slot_no in (6, 7):
        check(f"424 s{slot_no} inactive placeholder preserved", field(entd, 424, slot_no, 0x03) == 254)

    # 030 - Grogh Heights, entry 426.
    # s0 Black Mage; s1/s3 Chemist; s2 Squire; s4 Archer; s5 Thief; s6/s7/s8 inactive.
    check("426 runtime target table present", "[426] = Targets(" in runtime)
    check("426 runtime target excludes inactive Orran placeholder", "EnemyUnit(0x15" not in runtime)
    for uid in (0x80, 0x81, 0x82, 0x83, 0x84, 0x85):
        check(f"426 runtime target includes enemy uid 0x{uid:02X}", f"EnemyUnit(0x{uid:02X}" in runtime)

    grogh_slots = [0, 1, 2, 3, 4, 5]
    check("426 roster jobs", roster(entd, 426, grogh_slots, 0x0A) == [80, 75, 74, 75, 77, 83])
    check("426 roster levels", roster(entd, 426, grogh_slots, 0x03) == [101, 101, 100, 100, 101, 100])
    check("426 roster secondaries", roster(entd, 426, grogh_slots, 0x0B) == [6, 5, 6, 5, 5, 6])
    check("426 roster Brave", roster(entd, 426, grogh_slots, 0x06) == [58, 68, 70, 68, 80, 84])
    check("426 roster Faith", roster(entd, 426, grogh_slots, 0x07) == [78, 64, 50, 64, 45, 42])
    for slot_no in grogh_slots:
        job = field(entd, 426, slot_no, 0x0A)
        check(f"426 s{slot_no} jobrank", field(entd, 426, slot_no, 0x08) == rank(job))
        check(f"426 s{slot_no} JobLevel 8", field(entd, 426, slot_no, 0x09) == 8)

    check("426 Black Mage R/S/M",
          field16(entd, 426, 0, 0x0C) == 449
          and field16(entd, 426, 0, 0x0E) == 467
          and field16(entd, 426, 0, 0x10) == 486)
    check("426 Black Mage gear",
          roster(entd, 426, [0], 0x12) == [167]
          and roster(entd, 426, [0], 0x13) == [206]
          and roster(entd, 426, [0], 0x14) == [234]
          and roster(entd, 426, [0], 0x15) == [56]
          and roster(entd, 426, [0], 0x16) == [255])

    for slot_no in (1, 3):
        check(f"426 s{slot_no} Chemist R/S/M",
              field16(entd, 426, slot_no, 0x0C) == 441
              and field16(entd, 426, slot_no, 0x0E) == 474
              and field16(entd, 426, slot_no, 0x10) == 486)
        check(f"426 s{slot_no} Chemist gear",
              roster(entd, 426, [slot_no], 0x12) == [167]
              and roster(entd, 426, [slot_no], 0x13) == [198]
              and roster(entd, 426, [slot_no], 0x14) == [218]
              and roster(entd, 426, [slot_no], 0x15) == [72]
              and roster(entd, 426, [slot_no], 0x16) == [254])

    check("426 Squire R/S/M",
          field16(entd, 426, 2, 0x0C) == 442
          and field16(entd, 426, 2, 0x0E) == 465
          and field16(entd, 426, 2, 0x10) == 486)
    check("426 Squire gear",
          roster(entd, 426, [2], 0x12) == [163]
          and roster(entd, 426, [2], 0x13) == [195]
          and roster(entd, 426, [2], 0x14) == [218]
          and roster(entd, 426, [2], 0x15) == [29]
          and roster(entd, 426, [2], 0x16) == [255])

    check("426 Archer R/S/M",
          field16(entd, 426, 4, 0x0C) == 449
          and field16(entd, 426, 4, 0x0E) == 469
          and field16(entd, 426, 4, 0x10) == 486)
    check("426 Archer gear",
          roster(entd, 426, [4], 0x12) == [168]
          and roster(entd, 426, [4], 0x13) == [198]
          and roster(entd, 426, [4], 0x14) == [218]
          and roster(entd, 426, [4], 0x15) == [87]
          and roster(entd, 426, [4], 0x16) == [254])

    check("426 Thief R/S/M",
          field16(entd, 426, 5, 0x0C) == 453
          and field16(entd, 426, 5, 0x0E) == 465
          and field16(entd, 426, 5, 0x10) == 487)
    check("426 Thief gear",
          roster(entd, 426, [5], 0x12) == [168]
          and roster(entd, 426, [5], 0x13) == [198]
          and roster(entd, 426, [5], 0x14) == [210]
          and roster(entd, 426, [5], 0x15) == [9]
          and roster(entd, 426, [5], 0x16) == [255])

    for slot_no in (6, 7, 8):
        check(f"426 s{slot_no} inactive placeholder preserved", field(entd, 426, slot_no, 0x03) == 254)

    # 031 - Walled City of Yardrow, entry 428.
    # s0 Rapha protected guest; s1 Marach surviving boss; s2/s4/s6 Ninja; s3/s5 Summoner.
    check("428 runtime target table present", "[428] = Targets(" in runtime)
    check("428 runtime target includes Rapha guest", 'GuestUnit(0x19, 0x19, 0x19, "Rapha protected guest")' in runtime)
    check("428 runtime target excludes Marach boss", "EnemyUnit(0x1A" not in runtime)
    for uid in (0x80, 0x81, 0x82, 0x83, 0x84):
        check(f"428 runtime target includes enemy uid 0x{uid:02X}", f"EnemyUnit(0x{uid:02X}" in runtime)

    check("428 Rapha identity preserved", field(entd, 428, 0, 0x00) == 0x19 and field(entd, 428, 0, 0x0A) == 0x19)
    check("428 Rapha level/control Br/Fa",
          field(entd, 428, 0, 0x03) == 100
          and (field(entd, 428, 0, 0x18) & 0x08) != 0
          and (field(entd, 428, 0, 0x06), field(entd, 428, 0, 0x07)) == (65, 75))
    check("428 Rapha gear preserved",
          roster(entd, 428, [0], 0x12) == [168]
          and roster(entd, 428, [0], 0x13) == [206]
          and roster(entd, 428, [0], 0x14) == [234]
          and roster(entd, 428, [0], 0x15) == [113]
          and roster(entd, 428, [0], 0x16) == [254])

    check("428 Marach identity preserved", field(entd, 428, 1, 0x00) == 0x1A and field(entd, 428, 1, 0x0A) == 0x1A)
    check("428 Marach level setup Br/Fa",
          field(entd, 428, 1, 0x03) == 103
          and field(entd, 428, 1, 0x09) == 8
          and field(entd, 428, 1, 0x0B) == 6
          and (field(entd, 428, 1, 0x06), field(entd, 428, 1, 0x07)) == (78, 72))
    check("428 Marach R/S/M and gear",
          field16(entd, 428, 1, 0x0C) == 449
          and field16(entd, 428, 1, 0x0E) == 467
          and field16(entd, 428, 1, 0x10) == 486
          and roster(entd, 428, [1], 0x12) == [167]
          and roster(entd, 428, [1], 0x13) == [206]
          and roster(entd, 428, [1], 0x14) == [218]
          and roster(entd, 428, [1], 0x15) == [111]
          and roster(entd, 428, [1], 0x16) == [254])

    yardrow_enemy_slots = [2, 3, 4, 5, 6]
    check("428 roster jobs", roster(entd, 428, yardrow_enemy_slots, 0x0A) == [89, 82, 89, 82, 89])
    check("428 roster levels", roster(entd, 428, yardrow_enemy_slots, 0x03) == [102, 101, 101, 101, 101])
    check("428 roster secondaries", roster(entd, 428, yardrow_enemy_slots, 0x0B) == [6, 6, 5, 6, 5])
    check("428 roster Brave", roster(entd, 428, yardrow_enemy_slots, 0x06) == [86, 58, 90, 58, 90])
    check("428 roster Faith", roster(entd, 428, yardrow_enemy_slots, 0x07) == [40, 78, 60, 78, 60])
    for slot_no in yardrow_enemy_slots:
        job = field(entd, 428, slot_no, 0x0A)
        check(f"428 s{slot_no} jobrank", field(entd, 428, slot_no, 0x08) == rank(job))
        check(f"428 s{slot_no} JobLevel 8", field(entd, 428, slot_no, 0x09) == 8)

    for slot_no in (2, 4, 6):
        check(f"428 s{slot_no} Ninja R/S/M",
              field16(entd, 428, slot_no, 0x0C) == 453
              and field16(entd, 428, slot_no, 0x0E) == 465
              and field16(entd, 428, slot_no, 0x10) == 487)
        check(f"428 s{slot_no} Ninja gear",
              roster(entd, 428, [slot_no], 0x12) == [168]
              and roster(entd, 428, [slot_no], 0x13) == [198]
              and roster(entd, 428, [slot_no], 0x14) == [210]
              and roster(entd, 428, [slot_no], 0x15) == [14]
              and roster(entd, 428, [slot_no], 0x16) == [14])

    for slot_no in (3, 5):
        check(f"428 s{slot_no} Summoner R/S/M",
              field16(entd, 428, slot_no, 0x0C) == 449
              and field16(entd, 428, slot_no, 0x0E) == 467
              and field16(entd, 428, slot_no, 0x10) == 486)
        check(f"428 s{slot_no} Summoner gear",
              roster(entd, 428, [slot_no], 0x12) == [167]
              and roster(entd, 428, [slot_no], 0x13) == [206]
              and roster(entd, 428, [slot_no], 0x14) == [234]
              and roster(entd, 428, [slot_no], 0x15) == [56]
              and roster(entd, 428, [slot_no], 0x16) == [255])

    # 032 - The Yuguewood, entry 430.
    # s0 Rapha placeholder inactive; s1/s3 enemy Black Mage; s2/s4 enemy Time Mage; s5-s7 undead.
    check("430 runtime target table present", "[430] = Targets(" in runtime)
    check("430 runtime target includes enemy Black Mage A", 'EnemyUnit(0x80, 0x42, "Enemy Black Mage A")' in runtime)
    check("430 runtime target includes enemy Time Mage A", 'EnemyUnit(0x81, 0x44, "Enemy Time Mage A")' in runtime)
    check("430 runtime target includes enemy Black Mage B", 'EnemyUnit(0x82, 0x42, "Enemy Black Mage B")' in runtime)
    check("430 runtime target includes enemy Time Mage B", 'EnemyUnit(0x83, 0x44, "Enemy Time Mage B")' in runtime)

    check("430 Rapha placeholder inactive", field(entd, 430, 0, 0x03) == 254)
    yuguewood_caster_slots = [1, 2, 3, 4]
    check("430 caster jobs", roster(entd, 430, yuguewood_caster_slots, 0x0A) == [66, 68, 66, 68])
    check("430 caster levels", roster(entd, 430, yuguewood_caster_slots, 0x03) == [101, 101, 100, 101])
    check("430 caster jobrank zero", roster(entd, 430, yuguewood_caster_slots, 0x08) == [0, 0, 0, 0])
    check("430 caster JobLevels", roster(entd, 430, yuguewood_caster_slots, 0x09) == [8, 4, 8, 4])
    check("430 caster secondaries", roster(entd, 430, yuguewood_caster_slots, 0x0B) == [6, 6, 6, 6])
    check("430 caster Brave", roster(entd, 430, yuguewood_caster_slots, 0x06) == [58, 60, 58, 60])
    check("430 caster Faith", roster(entd, 430, yuguewood_caster_slots, 0x07) == [78, 74, 78, 74])

    for slot_no in (1, 3):
        check(f"430 s{slot_no} Black Mage R/S/M",
              field16(entd, 430, slot_no, 0x0C) == 449
              and field16(entd, 430, slot_no, 0x0E) == 467
              and field16(entd, 430, slot_no, 0x10) == 486)
        check(f"430 s{slot_no} Black Mage gear",
              roster(entd, 430, [slot_no], 0x12) == [167]
              and roster(entd, 430, [slot_no], 0x13) == [206]
              and roster(entd, 430, [slot_no], 0x14) == [234]
              and roster(entd, 430, [slot_no], 0x15) == [56]
              and roster(entd, 430, [slot_no], 0x16) == [255])

    for slot_no in (2, 4):
        check(f"430 s{slot_no} Time Mage R/S/M",
              field16(entd, 430, slot_no, 0x0C) == 449
              and field16(entd, 430, slot_no, 0x0E) == 467
              and field16(entd, 430, slot_no, 0x10) == 486)
        check(f"430 s{slot_no} Time Mage gear",
              roster(entd, 430, [slot_no], 0x12) == [167]
              and roster(entd, 430, [slot_no], 0x13) == [206]
              and roster(entd, 430, [slot_no], 0x14) == [234]
              and roster(entd, 430, [slot_no], 0x15) == [64]
              and roster(entd, 430, [slot_no], 0x16) == [255])

    yuguewood_undead_slots = [5, 6, 7]
    check("430 undead jobs", roster(entd, 430, yuguewood_undead_slots, 0x0A) == [112, 113, 114])
    check("430 undead levels", roster(entd, 430, yuguewood_undead_slots, 0x03) == [100, 100, 101])
    check("430 undead JobLevel 8", roster(entd, 430, yuguewood_undead_slots, 0x09) == [8, 8, 8])
    check("430 undead Brave", roster(entd, 430, yuguewood_undead_slots, 0x06) == [86, 86, 86])
    check("430 undead Faith", roster(entd, 430, yuguewood_undead_slots, 0x07) == [35, 35, 35])
    for slot_no in yuguewood_undead_slots:
        check(f"430 s{slot_no} undead no gear",
              roster(entd, 430, [slot_no], 0x12) == [254]
              and roster(entd, 430, [slot_no], 0x13) == [254]
              and roster(entd, 430, [slot_no], 0x14) == [254]
              and roster(entd, 430, [slot_no], 0x15) == [254]
              and roster(entd, 430, [slot_no], 0x16) == [254])

    # 033 - Riovanes Castle Gate, entry 431.
    # s0 Rapha placeholder inactive; s1 Marach named boss excluded from runtime;
    # s2-s4 Archers, s5 Templar, s6-s8 Knights.
    check("431 runtime target table present", "[431] = Targets(" in runtime)
    check("431 runtime target excludes Marach boss", 'GuestUnit(0x1A' not in runtime and 'EnemyUnit(0x1A' not in runtime)
    for uid, label in (
        ("0x80", "High Archer A"),
        ("0x81", "High Archer B"),
        ("0x82", "Flank Archer"),
        ("0x84", "Knight bridge body A"),
        ("0x85", "Knight bridge body B"),
        ("0x86", "Knight bridge body C"),
    ):
        check(f"431 runtime target includes {label}", f'EnemyUnit({uid}, "{label}")' in runtime)
    check("431 runtime target includes Templar explicit job",
          'EnemyUnit(0x83, 0x26, "Templar bridge breaker")' in runtime)

    check("431 Rapha placeholder inactive", field(entd, 431, 0, 0x03) == 254)
    check("431 Marach identity preserved", field(entd, 431, 1, 0x0A) == 26)
    check("431 Marach level/setup",
          field(entd, 431, 1, 0x03) == 103
          and field(entd, 431, 1, 0x09) == 8
          and field(entd, 431, 1, 0x0B) == 6
          and field(entd, 431, 1, 0x06) == 78
          and field(entd, 431, 1, 0x07) == 72)
    check("431 Marach R/S/M and gear",
          field16(entd, 431, 1, 0x0C) == 449
          and field16(entd, 431, 1, 0x0E) == 467
          and field16(entd, 431, 1, 0x10) == 486
          and roster(entd, 431, [1], 0x12) == [167]
          and roster(entd, 431, [1], 0x13) == [206]
          and roster(entd, 431, [1], 0x14) == [218]
          and roster(entd, 431, [1], 0x15) == [111]
          and roster(entd, 431, [1], 0x16) == [254])

    riovanes_slots = [2, 3, 4, 5, 6, 7, 8]
    check("431 roster jobs", roster(entd, 431, riovanes_slots, 0x0A) == [77, 77, 77, 38, 76, 76, 76])
    check("431 roster levels", roster(entd, 431, riovanes_slots, 0x03) == [102, 101, 100, 102, 101, 101, 101])
    check("431 roster JobLevel 8", roster(entd, 431, riovanes_slots, 0x09) == [8, 8, 8, 8, 8, 8, 8])
    check("431 roster Brave", roster(entd, 431, riovanes_slots, 0x06) == [80, 80, 80, 84, 84, 84, 84])
    check("431 roster Faith", roster(entd, 431, riovanes_slots, 0x07) == [45, 45, 45, 45, 45, 45, 45])

    for slot_no in (2, 3, 4):
        check(f"431 s{slot_no} Archer R/S/M",
              field(entd, 431, slot_no, 0x0B) == 5
              and field16(entd, 431, slot_no, 0x0C) == 449
              and field16(entd, 431, slot_no, 0x0E) == 469
              and field16(entd, 431, slot_no, 0x10) == 486)
        check(f"431 s{slot_no} Archer gear",
              roster(entd, 431, [slot_no], 0x12) == [168]
              and roster(entd, 431, [slot_no], 0x13) == [198]
              and roster(entd, 431, [slot_no], 0x14) == [218]
              and roster(entd, 431, [slot_no], 0x15) == [87]
              and roster(entd, 431, [slot_no], 0x16) == [254])

    check("431 Templar Mighty Sword kit",
          field(entd, 431, 5, 0x0B) == 52
          and field16(entd, 431, 5, 0x0C) == 442
          and field16(entd, 431, 5, 0x0E) == 465
          and field16(entd, 431, 5, 0x10) == 486
          and roster(entd, 431, [5], 0x12) == [154]
          and roster(entd, 431, [5], 0x13) == [182]
          and roster(entd, 431, [5], 0x14) == [218]
          and roster(entd, 431, [5], 0x15) == [30]
          and roster(entd, 431, [5], 0x16) == [139])

    check("431 Knight secondaries",
          roster(entd, 431, [6, 7, 8], 0x0B) == [5, 6, 6])
    for slot_no in (6, 7, 8):
        check(f"431 s{slot_no} Knight R/S/M",
              field16(entd, 431, slot_no, 0x0C) == 442
              and field16(entd, 431, slot_no, 0x0E) == 465
              and field16(entd, 431, slot_no, 0x10) == 486)
        check(f"431 s{slot_no} Knight gear",
              roster(entd, 431, [slot_no], 0x12) == [154]
              and roster(entd, 431, [slot_no], 0x13) == [182]
              and roster(entd, 431, [slot_no], 0x14) == [218]
              and roster(entd, 431, [slot_no], 0x15) == [30]
              and roster(entd, 431, [slot_no], 0x16) == [139])

    # 034 - Riovanes Castle Keep, entry 432.
    # Wiegraf and Belias are bosses/transform forms; no generic runtime target is configured here.
    check("432 runtime generic scaler not armed for bosses", "[432] = Targets(" not in runtime)
    check("432 Wiegraf identity preserved", field(entd, 432, 0, 0x00) == 40 and field(entd, 432, 0, 0x0A) == 40)
    check("432 Wiegraf level/setup",
          field(entd, 432, 0, 0x03) == 104
          and field(entd, 432, 0, 0x09) == 8
          and field(entd, 432, 0, 0x0B) == 5
          and field(entd, 432, 0, 0x06) == 88
          and field(entd, 432, 0, 0x07) == 60)
    check("432 Wiegraf disarmable Defender kit",
          field16(entd, 432, 0, 0x0C) == 442
          and field16(entd, 432, 0, 0x0E) == 465
          and field16(entd, 432, 0, 0x10) == 486
          and roster(entd, 432, [0], 0x12) == [154]
          and roster(entd, 432, [0], 0x13) == [182]
          and roster(entd, 432, [0], 0x14) == [218]
          and roster(entd, 432, [0], 0x15) == [33]
          and roster(entd, 432, [0], 0x16) == [139])
    check("432 Wiegraf no Safeguard", field16(entd, 432, 0, 0x0E) != 475)

    placeholder_knights = [1, 2, 3, 4]
    check("432 transform placeholder Knights preserved",
          roster(entd, 432, placeholder_knights, 0x03) == [1, 1, 1, 1]
          and roster(entd, 432, placeholder_knights, 0x09) == [0, 0, 0, 0]
          and roster(entd, 432, placeholder_knights, 0x0A) == [76, 76, 76, 76])
    placeholder_wiegrafs = [9, 10, 11]
    check("432 transform placeholder Wiegrafs preserved",
          roster(entd, 432, placeholder_wiegrafs, 0x03) == [1, 1, 1]
          and roster(entd, 432, placeholder_wiegrafs, 0x09) == [0, 0, 0]
          and roster(entd, 432, placeholder_wiegrafs, 0x0A) == [40, 40, 40])

    check("432 Belias identity and level",
          field(entd, 432, 5, 0x00) == 60
          and field(entd, 432, 5, 0x0A) == 60
          and field(entd, 432, 5, 0x03) == 105
          and field(entd, 432, 5, 0x09) == 8
          and field(entd, 432, 5, 0x06) == 88
          and field(entd, 432, 5, 0x07) == 82)
    check("432 Belias no fake gear",
          roster(entd, 432, [5], 0x12) == [255]
          and roster(entd, 432, [5], 0x13) == [255]
          and roster(entd, 432, [5], 0x14) == [255]
          and roster(entd, 432, [5], 0x15) == [255]
          and roster(entd, 432, [5], 0x16) == [255])

    demon_slots = [6, 7, 8]
    check("432 Archaeodaemon jobs/levels",
          roster(entd, 432, demon_slots, 0x0A) == [153, 153, 153]
          and roster(entd, 432, demon_slots, 0x03) == [103, 103, 102])
    check("432 Archaeodaemon JobLevel and Br/Fa",
          roster(entd, 432, demon_slots, 0x09) == [8, 8, 8]
          and roster(entd, 432, demon_slots, 0x06) == [84, 84, 84]
          and roster(entd, 432, demon_slots, 0x07) == [72, 72, 72])
    for slot_no in demon_slots:
        check(f"432 s{slot_no} Archaeodaemon no gear",
              roster(entd, 432, [slot_no], 0x12) == [254]
              and roster(entd, 432, [slot_no], 0x13) == [254]
              and roster(entd, 432, [slot_no], 0x14) == [254]
              and roster(entd, 432, [slot_no], 0x15) == [254]
              and roster(entd, 432, [slot_no], 0x16) == [254])

    # 035 - Riovanes Castle Roof, entry 433.
    # s0 Rapha protected guest; s1/s2 scripting placeholders; s3 Elmdor; s4 Celia; s5 Lettie.
    check("433 runtime target table present", "[433] = Targets(" in runtime)
    check("433 runtime target includes Rapha guest",
          'GuestUnit(0x29, 0x29, 0x29, "Rapha rooftop protected guest")' in runtime)
    check("433 runtime target excludes fleeing enemies",
          "EnemyUnit(0x1B" not in runtime and "EnemyUnit(0x2D" not in runtime and "EnemyUnit(0x2E" not in runtime)

    check("433 Rapha identity preserved", field(entd, 433, 0, 0x00) == 41 and field(entd, 433, 0, 0x0A) == 41)
    check("433 Rapha level/control Br/Fa",
          field(entd, 433, 0, 0x03) == 100
          and (field(entd, 433, 0, 0x18) & 0x08) == 0x08
          and field(entd, 433, 0, 0x06) == 65
          and field(entd, 433, 0, 0x07) == 75)
    check("433 Rapha support kit",
          field(entd, 433, 0, 0x0B) == 6
          and field16(entd, 433, 0, 0x0C) == 449
          and field16(entd, 433, 0, 0x0E) == 467
          and field16(entd, 433, 0, 0x10) == 486
          and roster(entd, 433, [0], 0x12) == [168]
          and roster(entd, 433, [0], 0x13) == [206]
          and roster(entd, 433, [0], 0x14) == [234]
          and roster(entd, 433, [0], 0x15) == [113]
          and roster(entd, 433, [0], 0x16) == [254])

    check("433 scripting placeholders preserved",
          field(entd, 433, 1, 0x03) == 5
          and field(entd, 433, 1, 0x0A) == 41
          and field(entd, 433, 2, 0x03) == 5
          and field(entd, 433, 2, 0x0A) == 18)

    check("433 Elmdor identity and level",
          field(entd, 433, 3, 0x00) == 27
          and field(entd, 433, 3, 0x0A) == 27
          and field(entd, 433, 3, 0x03) == 104
          and field(entd, 433, 3, 0x09) == 8
          and field(entd, 433, 3, 0x06) == 90
          and field(entd, 433, 3, 0x07) == 65)
    check("433 Elmdor no-Limberry kit",
          field(entd, 433, 3, 0x0B) == 6
          and field16(entd, 433, 3, 0x0C) == 453
          and field16(entd, 433, 3, 0x0E) == 465
          and field16(entd, 433, 3, 0x10) == 498
          and roster(entd, 433, [3], 0x12) == [166]
          and roster(entd, 433, [3], 0x13) == [206]
          and roster(entd, 433, [3], 0x14) == [234]
          and roster(entd, 433, [3], 0x15) == [45]
          and roster(entd, 433, [3], 0x16) == [254]
          and field(entd, 433, 3, 0x1E) == 0)

    check("433 Assassin identities and levels",
          field(entd, 433, 4, 0x00) == 45
          and field(entd, 433, 4, 0x0A) == 45
          and field(entd, 433, 5, 0x00) == 46
          and field(entd, 433, 5, 0x0A) == 46
          and roster(entd, 433, [4, 5], 0x03) == [103, 103]
          and roster(entd, 433, [4, 5], 0x09) == [8, 8]
          and roster(entd, 433, [4, 5], 0x06) == [90, 90]
          and roster(entd, 433, [4, 5], 0x07) == [60, 60])
    for slot_no in (4, 5):
        check(f"433 s{slot_no} Assassin race kit",
              field(entd, 433, slot_no, 0x0B) == 6
              and field16(entd, 433, slot_no, 0x0C) == 453
              and field16(entd, 433, slot_no, 0x0E) == 477
              and field16(entd, 433, slot_no, 0x10) == 498
              and roster(entd, 433, [slot_no], 0x12) == [168]
              and roster(entd, 433, [slot_no], 0x13) == [198]
              and roster(entd, 433, [slot_no], 0x14) == [234]
              and roster(entd, 433, [slot_no], 0x15) == [14]
              and roster(entd, 433, [slot_no], 0x16) == [14]
              and field(entd, 433, slot_no, 0x1E) == 0)

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
