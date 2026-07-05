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
