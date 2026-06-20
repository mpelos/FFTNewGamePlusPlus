#!/usr/bin/env python3
"""
FFT: The Ivalice Chronicles - save decoder (offline).

Decodes the PNG-wrapped saves (enhanced.png = manual slots, autoenhanced.png = autosave/resume)
into their inner files. Format is the Faith/FF16 engine save:
  PNG -> 'ffTo' chunk -> UMIF TOC -> per-file: XOR(key) + zlib(preset dict).

Crypto/format reference: Nenkai/FF16Tools FF16Tools.Files/Save/FaithSaveFile.cs + CompressDict.cs.
XOR key: 0x0F3F80FE5F1FC4F3. zlib uses a 0x8000-byte preset dictionary (work/CompressDict.cs).

NG+ FLAG (manual save 'fftsave.bin', per-slot, slot aligned so 'Arthur' marker sits at +0x85C,
slot stride 0x9CE4): byte at slot offset 0x08AFB == 1 for New Game+, 0 for a normal playthrough.
(0x0972C is a second robust alternate; 0x08CA7/0x08DFB are NOT reliable.) Validated across all
7 used slots: flag==1 for the 3 NG+ saves, ==0 for the 4 normal saves (incl. an Arthur-less NG+).

Usage:
  python fft_save_decode.py <enhanced.png|autoenhanced.png> [--dump-dir OUT]
"""
import sys, os, re, struct, zlib, argparse

XOR_KEY = 0x0F3F80FE5F1FC4F3
PNG_SIG = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
SLOT_SIZE = 0x9CE4
ARTHUR_IN_SLOT = 0x85C          # offset of the 'Arthur' roster marker inside a manual slot
NGPLUS_FLAG_OFF = 0x08AFB       # per-slot: 1 = NG+, 0 = normal


def _zdict():
    """Load the 0x8000 zlib preset dictionary from a local copy of FF16Tools CompressDict.cs."""
    here = os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(here, "..", "work", "CompressDict.cs"),
              os.path.join(here, "CompressDict.cs")):
        if os.path.exists(p):
            blk = re.search(r"new byte\[0x8000\]\s*\{(.*?)\}", open(p, encoding="utf-8").read(), re.S).group(1)
            return bytes(int(v, 16) for v in re.findall(r"0x([0-9A-Fa-f]{2})", blk))
    raise FileNotFoundError("CompressDict.cs not found (work/ or tools/). Grab it from Nenkai/FF16Tools.")


def crypt(b):
    """In-place-style XOR (returns new bytes). Matches FaithSaveFile.Crypt."""
    b = bytearray(b); n = len(b); i = 0
    while n - i >= 8:
        b[i:i+8] = (int.from_bytes(b[i:i+8], "little") ^ XOR_KEY).to_bytes(8, "little"); i += 8
    if n - i >= 4:
        b[i:i+4] = (int.from_bytes(b[i:i+4], "little") ^ (XOR_KEY & 0xFFFFFFFF)).to_bytes(4, "little"); i += 4
    if n - i >= 2:
        b[i:i+2] = (int.from_bytes(b[i:i+2], "little") ^ (XOR_KEY & 0xFFFF)).to_bytes(2, "little"); i += 2
    if n - i >= 1:
        b[i] ^= XOR_KEY & 0xFF
    return bytes(b)


def decode_png(path, zdict=None):
    """Return {innerFileName: decompressedBytes} for a PNG save container."""
    if zdict is None:
        zdict = _zdict()
    d = open(path, "rb").read()
    assert d[:8] == PNG_SIG, "not a PNG"
    o = 8; sd = None
    while o + 8 <= len(d):
        ln = struct.unpack_from(">I", d, o)[0]; typ = d[o+4:o+8]
        if typ == b"ffTo":
            sd = d[o+8:o+8+ln]; break
        o += 12 + ln
    if sd is None:
        raise KeyNotFoundError("no ffTo chunk")
    num = struct.unpack_from("<I", sd, 0xC)[0]
    out = {}
    for i in range(num):
        base = 0x10 + i * 0x20
        name_len, data_len = struct.unpack_from("<II", sd, base)
        name_ptr, decomp_len, data_ptr = struct.unpack_from("<qqq", sd, base + 8)
        name = crypt(sd[name_ptr:name_ptr+name_len]).split(b"\x00")[0].decode("utf-8", "replace")
        comp = crypt(sd[data_ptr:data_ptr+data_len])
        do = zlib.decompressobj(15, zdict=zdict)
        out[name] = do.decompress(b"\x78\xF9" + comp) + do.flush()
    return out


def manual_slots(fftsave_bin):
    """Split decompressed fftsave.bin into per-slot byte blobs, aligned by the 'Arthur' marker."""
    slots = []; i = fftsave_bin.find(b"Arthur")
    while i != -1:
        s = i - ARTHUR_IN_SLOT
        slots.append(fftsave_bin[s:s+SLOT_SIZE]); i = fftsave_bin.find(b"Arthur", i + 1)
    return slots


def is_ngplus(slot_bytes):
    return slot_bytes[NGPLUS_FLAG_OFF] != 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("png")
    ap.add_argument("--dump-dir")
    args = ap.parse_args()
    files = decode_png(args.png)
    print(f"{args.png}: {len(files)} inner file(s)")
    for name, data in files.items():
        print(f"  {name}: {len(data)} bytes")
        if args.dump_dir:
            os.makedirs(args.dump_dir, exist_ok=True)
            open(os.path.join(args.dump_dir, name), "wb").write(data)
    if "fftsave.bin" in files:
        for idx, sl in enumerate(manual_slots(files["fftsave.bin"])):
            print(f"  slot {idx}: NG+={is_ngplus(sl)} (byte@0x{NGPLUS_FLAG_OFF:X}={sl[NGPLUS_FLAG_OFF]})")
