#!/usr/bin/env python3
"""Apply the NG+ level band to every optional Chapter 4 battle.

Only the level byte (+0x03) is changed.  The fixed sidequest encounters live in
ENTD4; Midlight's Deep random formations live in ENTD1.  Allies, recruitment
scenes, and unused/debug formations are deliberately excluded.
"""
from pathlib import Path

ENTRY = 0x280
SLOT = 0x28
ROOT = Path(__file__).resolve().parents[1]
VANILLA = ROOT / "extracted/enhanced_0002_selected/fftpack"
MOD = ROOT / "src/fftivc.battles.ngplus/entd"

# EntryNo -> MapId, recovered from enhanced_0004 EntryNo/SortieConfirm.
# Maps 78-82 are the five map assets used by Midlight's Deep's ten floors.
MIDLIGHT_ENTRIES = (
    list(range(73, 81))
    + list(range(85, 93))
    + [94]
    + list(range(97, 105))
    + [107, 108]
    + list(range(109, 128))
)


def slot_offset(entry: int, slot: int) -> int:
    return entry * ENTRY + slot * SLOT


def set_level(data: bytearray, entry: int, slot: int, level: int) -> None:
    offset = slot_offset(entry, slot)
    if data[offset] == 0:
        raise ValueError(f"entry {entry} slot {slot} is empty")
    data[offset + 3] = level


def patch_entd1() -> None:
    source = VANILLA / "battle_entd1_ent.bin"
    target = MOD / "battle_entd1_ent.bin"
    data = bytearray(source.read_bytes())
    patched = 0
    for entry in MIDLIGHT_ENTRIES:
        ordinal = 0
        for slot in range(16):
            offset = slot_offset(entry, slot)
            if data[offset] == 0:
                continue
            set_level(data, entry, slot, 100 + (ordinal & 1))
            ordinal += 1
            patched += 1
    target.write_bytes(data)
    print(f"ENTD1: {patched} Midlight formation slots -> levels 100-101")


def patch_entd4() -> None:
    target = MOD / "battle_entd4_ent.bin"
    data = bytearray(target.read_bytes())

    # Global ENTD entries 463-466: Colliery Underground Third, Second,
    # First, and Underground Passage. s0 is Beowulf; entry 466 s1 is Reis.
    fixed_enemies = {
        79: range(1, 6),
        80: range(1, 6),
        81: range(1, 6),
        82: range(2, 8),
        # Global 475: Zarghidas. s0 is Cloud.
        91: range(1, 8),
    }
    patched = 0
    for entry, slots in fixed_enemies.items():
        for ordinal, slot in enumerate(slots):
            set_level(data, entry, slot, 100 + (ordinal & 1))
            patched += 1

    # Global 468: Nelveska Temple. Construct 7 is the encounter leader.
    set_level(data, 84, 0, 102)
    patched += 1
    for ordinal, slot in enumerate(range(1, 6)):
        set_level(data, 84, slot, 100 + (ordinal & 1))
        patched += 1

    target.write_bytes(data)
    print(f"ENTD4: {patched} fixed sidequest slots -> 100-101; leaders -> 102")


def patch_entd3() -> None:
    """Patch the dedicated Midlight END encounter, stored in ENTD3."""
    source = VANILLA / "battle_entd3_ent.bin"
    target = MOD / "battle_entd3_ent.bin"
    data = bytearray(source.read_bytes())
    set_level(data, 90, 0, 102)  # Elidibus
    patched = 1
    ordinal = 0
    for slot in range(1, 16):
        offset = slot_offset(90, slot)
        if data[offset] == 0:
            continue
        set_level(data, 90, slot, 100 + (ordinal & 1))
        ordinal += 1
        patched += 1
    target.write_bytes(data)
    print(f"ENTD3: {patched} Midlight END slots -> 100-101; Elidibus -> 102")


if __name__ == "__main__":
    patch_entd1()
    patch_entd3()
    patch_entd4()
