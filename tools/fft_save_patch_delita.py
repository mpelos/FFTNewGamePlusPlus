#!/usr/bin/env python3
"""
Patch the current Delita roster-cache bug in a FFT: The Ivalice Chronicles save PNG.

This is intentionally narrow:
- It only edits resume_* inner files.
- It only patches records with the confirmed Delita fingerprint from the Ch1 NG++ test save:
  Brave/Faith 71/55, Squire below Lv8, Time Mage Lv8, and Time Mage JP >= 1000.
- It moves the mistakenly-seeded Time Mage JP package onto Squire, then returns Time Mage to Lv1.

Usage:
  python tools/fft_save_patch_delita.py autoenhanced.png --output patched.png
  python tools/fft_save_patch_delita.py autoenhanced.png --in-place
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import struct
import sys
import time
import zlib
from dataclasses import dataclass
from pathlib import Path


XOR_KEY = 0x0F3F80FE5F1FC4F3
PNG_SIG = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])

BRAVE_FAITH = b"\x47\x37"  # Delita current fingerprint: Bravery 71 / Faith 55.
JOB_LEVELS_FROM_BRFA = 0x56
JOB_JP_FROM_BRFA = 0x62

JOB_SQUIRE = 0
JOB_BLACK_MAGE = 6
JOB_TIME_MAGE = 7


@dataclass
class InnerFile:
    name: str
    data: bytearray
    original_name_bytes: bytes


@dataclass
class Candidate:
    file_name: str
    br_fa: int
    squire_level: int
    squire_jp: int
    time_mage_level: int
    time_mage_jp: int


def zdict() -> bytes:
    here = Path(__file__).resolve().parent
    for path in (here.parent / "work" / "CompressDict.cs", here / "CompressDict.cs"):
        if path.exists():
            text = path.read_text(encoding="utf-8")
            match = re.search(r"new byte\[0x8000\]\s*\{(.*?)\}", text, re.S)
            if not match:
                continue
            return bytes(int(v, 16) for v in re.findall(r"0x([0-9A-Fa-f]{2})", match.group(1)))
    raise FileNotFoundError("CompressDict.cs not found under work/ or tools/")


def crypt(data: bytes) -> bytes:
    b = bytearray(data)
    n = len(b)
    i = 0
    while n - i >= 8:
        b[i:i + 8] = (int.from_bytes(b[i:i + 8], "little") ^ XOR_KEY).to_bytes(8, "little")
        i += 8
    if n - i >= 4:
        b[i:i + 4] = (int.from_bytes(b[i:i + 4], "little") ^ (XOR_KEY & 0xFFFFFFFF)).to_bytes(4, "little")
        i += 4
    if n - i >= 2:
        b[i:i + 2] = (int.from_bytes(b[i:i + 2], "little") ^ (XOR_KEY & 0xFFFF)).to_bytes(2, "little")
        i += 2
    if n - i >= 1:
        b[i] ^= XOR_KEY & 0xFF
    return bytes(b)


def read_png_chunks(png: bytes) -> list[tuple[bytes, bytes]]:
    if png[:8] != PNG_SIG:
        raise ValueError("not a PNG save")
    chunks: list[tuple[bytes, bytes]] = []
    o = 8
    while o + 12 <= len(png):
        length = struct.unpack_from(">I", png, o)[0]
        typ = png[o + 4:o + 8]
        data = png[o + 8:o + 8 + length]
        chunks.append((typ, data))
        o += 12 + length
        if typ == b"IEND":
            break
    return chunks


def write_png_chunks(chunks: list[tuple[bytes, bytes]]) -> bytes:
    out = bytearray(PNG_SIG)
    for typ, data in chunks:
        out += struct.pack(">I", len(data))
        out += typ
        out += data
        out += struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)
    return bytes(out)


def inflate(stored: bytes, decomp_len: int, zd: bytes) -> bytes:
    dec = zlib.decompressobj(15, zdict=zd)
    out = dec.decompress(b"\x78\xF9" + stored) + dec.flush()
    if len(out) != decomp_len:
        raise ValueError(f"decompressed length mismatch: got {len(out)}, expected {decomp_len}")
    return out


def deflate(data: bytes, zd: bytes) -> bytes:
    comp = zlib.compressobj(level=9, wbits=15, zdict=zd)
    out = comp.compress(data) + comp.flush()
    if not out.startswith(b"\x78\xF9"):
        raise ValueError(f"unexpected zlib header: {out[:2].hex()}")
    return out[2:]


def decode_ffto(ffto: bytes, zd: bytes) -> tuple[bytearray, list[InnerFile]]:
    if ffto[8:12] != b"UMIF":
        raise ValueError("ffTo chunk does not contain UMIF")
    num_files = struct.unpack_from("<I", ffto, 0xC)[0]
    files: list[InnerFile] = []
    for i in range(num_files):
        base = 0x10 + i * 0x20
        name_len, data_len = struct.unpack_from("<II", ffto, base)
        name_ptr, decomp_len, data_ptr = struct.unpack_from("<qqq", ffto, base + 8)
        raw_name = crypt(ffto[name_ptr:name_ptr + name_len])
        name = raw_name.split(b"\x00", 1)[0].decode("utf-8", "replace")
        stored = crypt(ffto[data_ptr:data_ptr + data_len])
        files.append(InnerFile(name=name, data=bytearray(inflate(stored, decomp_len, zd)), original_name_bytes=raw_name))
    return bytearray(ffto[:0x10]), files


def encode_ffto(header: bytearray, files: list[InnerFile], zd: bytes) -> bytes:
    num_files = len(files)
    toc_len = 0x10 + num_files * 0x20
    header = bytearray(header)
    struct.pack_into("<I", header, 0, toc_len)
    struct.pack_into("<I", header, 0xC, num_files)

    entries = bytearray(toc_len - 0x10)
    names = bytearray()
    compressed: list[bytes] = []

    for f in files:
        names += crypt(f.original_name_bytes)
        compressed.append(crypt(deflate(bytes(f.data), zd)))

    data_start = toc_len + len(names)
    name_cursor = toc_len
    data_cursor = data_start
    for i, f in enumerate(files):
        base = i * 0x20
        comp = compressed[i]
        struct.pack_into("<IIqqq", entries, base, len(f.original_name_bytes), len(comp),
                         name_cursor, len(f.data), data_cursor)
        name_cursor += len(f.original_name_bytes)
        data_cursor += len(comp)

    return bytes(header + entries + names + b"".join(compressed))


def packed_job_level(data: bytearray, base: int, job_index: int) -> int:
    value = data[base + job_index // 2]
    return value >> 4 if job_index % 2 == 0 else value & 0x0F


def set_packed_job_level(data: bytearray, base: int, job_index: int, level: int) -> None:
    idx = base + job_index // 2
    old = data[idx]
    if job_index % 2 == 0:
        data[idx] = ((level & 0x0F) << 4) | (old & 0x0F)
    else:
        data[idx] = (old & 0xF0) | (level & 0x0F)


def read_u16(data: bytearray, off: int) -> int:
    return data[off] | (data[off + 1] << 8)


def write_u16(data: bytearray, off: int, value: int) -> None:
    data[off] = value & 0xFF
    data[off + 1] = (value >> 8) & 0xFF


def find_delita_bug_records(file_name: str, data: bytearray) -> list[Candidate]:
    if not file_name.lower().startswith("resume_"):
        return []

    found: list[Candidate] = []
    start = 0
    while True:
        br_fa = data.find(BRAVE_FAITH, start)
        if br_fa < 0:
            break
        start = br_fa + 1

        level_base = br_fa + JOB_LEVELS_FROM_BRFA
        jp_base = br_fa + JOB_JP_FROM_BRFA
        if jp_base + 2 * (JOB_TIME_MAGE + 1) > len(data) or level_base + 11 > len(data):
            continue

        squire_level = packed_job_level(data, level_base, JOB_SQUIRE)
        time_mage_level = packed_job_level(data, level_base, JOB_TIME_MAGE)
        squire_jp = read_u16(data, jp_base + JOB_SQUIRE * 2)
        time_mage_jp = read_u16(data, jp_base + JOB_TIME_MAGE * 2)

        # The real bug shape from the active Delita roster cache is:
        # Squire still low with low JP, while the wrong Time Mage slot carries the Lv8 seed package.
        # Other resume snapshots may contain unrelated 71/55 records with huge JP values; skip those.
        if squire_level < 8 and squire_jp < 500 and time_mage_level == 8 and 1000 <= time_mage_jp <= 5000:
            found.append(Candidate(file_name, br_fa, squire_level, squire_jp, time_mage_level, time_mage_jp))

    return found


def patch_candidate(data: bytearray, c: Candidate) -> None:
    level_base = c.br_fa + JOB_LEVELS_FROM_BRFA
    jp_base = c.br_fa + JOB_JP_FROM_BRFA

    # Move the misplaced "Lv8 job seed" from Time Mage to Squire.
    set_packed_job_level(data, level_base, JOB_SQUIRE, 8)
    set_packed_job_level(data, level_base, JOB_TIME_MAGE, 1)
    write_u16(data, jp_base + JOB_SQUIRE * 2, c.time_mage_jp)
    write_u16(data, jp_base + JOB_TIME_MAGE * 2, c.squire_jp)


def decode_png_files(path: Path) -> tuple[list[tuple[bytes, bytes]], bytearray, list[InnerFile], bytes]:
    png = path.read_bytes()
    chunks = read_png_chunks(png)
    zd = zdict()
    for typ, data in chunks:
        if typ == b"ffTo":
            header, files = decode_ffto(data, zd)
            return chunks, header, files, zd
    raise ValueError("no ffTo chunk found")


def rebuild_png(chunks: list[tuple[bytes, bytes]], header: bytearray, files: list[InnerFile], zd: bytes) -> bytes:
    ffto = encode_ffto(header, files, zd)
    replaced = False
    out_chunks: list[tuple[bytes, bytes]] = []
    for typ, data in chunks:
        if typ == b"ffTo":
            out_chunks.append((typ, ffto))
            replaced = True
        else:
            out_chunks.append((typ, data))
    if not replaced:
        raise ValueError("no ffTo chunk found")
    return write_png_chunks(out_chunks)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("save_png", type=Path)
    ap.add_argument("--output", type=Path)
    ap.add_argument("--in-place", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    if not args.dry_run and args.in_place == bool(args.output):
        ap.error("choose exactly one of --output or --in-place")

    chunks, header, files, zd = decode_png_files(args.save_png)
    candidates: list[Candidate] = []
    for f in files:
        candidates.extend(find_delita_bug_records(f.name, f.data))

    if not candidates:
        print("no Delita Squire/Time Mage bug records found")
        return 1

    print("records to patch:")
    for c in candidates:
        print(f"  {c.file_name}: br_fa=0x{c.br_fa:X} Squire Lv{c.squire_level} JP{c.squire_jp} "
              f"TimeMage Lv{c.time_mage_level} JP{c.time_mage_jp}")

    if args.dry_run:
        return 0

    by_file = {(c.file_name, c.br_fa): c for c in candidates}
    for f in files:
        for c in [v for (name, _), v in by_file.items() if name == f.name]:
            patch_candidate(f.data, c)

    patched_png = rebuild_png(chunks, header, files, zd)

    target = args.save_png if args.in_place else args.output
    assert target is not None

    if args.in_place:
        stamp = time.strftime("%Y%m%d_%H%M%S")
        backup = args.save_png.with_name(f"{args.save_png.stem}.bak_delita_{stamp}{args.save_png.suffix}")
        shutil.copy2(args.save_png, backup)
        print(f"backup: {backup}")

    target.write_bytes(patched_png)
    print(f"wrote: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
