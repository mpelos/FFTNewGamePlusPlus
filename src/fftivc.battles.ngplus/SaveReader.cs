using System;
using System.Collections.Generic;
using System.IO;
using System.Reflection;
using System.Runtime.InteropServices;

using Ionic.Zlib;

namespace fftivc.battles.ngplus;

/// <summary>
/// Minimal, self-contained reader for FFT: The Ivalice Chronicles PNG saves.
/// Reads with FileShare.ReadWrite and disposes the handle immediately, so it NEVER blocks the
/// game's own save writes (the FF16Tools FaithSaveGameData.Open leaks the handle -> game autosave
/// fails with "file used by another process"; this avoids that).
/// Format: PNG 'ffTo' chunk -> UMIF TOC -> per-file XOR(0x0F3F80FE5F1FC4F3) + zlib(preset dict).
/// </summary>
public static class SaveReader
{
    private const ulong XOR_KEY = 0x0F3F80FE5F1FC4F3;
    private static readonly byte[] PngSig = { 0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A };
    private static byte[]? _dict;

    private static byte[] Dict => _dict ??= LoadDict();

    private static byte[] LoadDict()
    {
        Assembly asm = typeof(SaveReader).Assembly;
        using Stream s = asm.GetManifestResourceStream("fftivc.battles.ngplus.zlibdict.bin")
            ?? throw new InvalidOperationException("embedded zlibdict.bin missing");
        using var ms = new MemoryStream();
        s.CopyTo(ms);
        return ms.ToArray();
    }

    /// <summary>Read a save PNG without locking it, return all inner files decompressed.</summary>
    public static Dictionary<string, byte[]> Decode(string path)
    {
        byte[] data = ReadShared(path);
        var result = new Dictionary<string, byte[]>(StringComparer.OrdinalIgnoreCase);

        if (data.Length < 8 || !AsSpan(data, 0, 8).SequenceEqual(PngSig))
            throw new InvalidDataException("not a PNG save");

        // Walk PNG chunks for the 'ffTo' data chunk.
        int o = 8;
        ReadOnlySpan<byte> sd = default;
        while (o + 8 <= data.Length)
        {
            int len = ReadU32BE(data, o);
            string type = System.Text.Encoding.ASCII.GetString(data, o + 4, 4);
            if (type == "ffTo") { sd = new ReadOnlySpan<byte>(data, o + 8, len); break; }
            o += 12 + len;
        }
        if (sd.IsEmpty) throw new InvalidDataException("no ffTo chunk");

        uint numFiles = ReadU32LE(sd, 0xC);
        for (uint i = 0; i < numFiles; i++)
        {
            int b = (int)(0x10 + i * 0x20);
            uint nameLen = ReadU32LE(sd, b);
            uint dataLen = ReadU32LE(sd, b + 4);
            long namePtr = ReadI64LE(sd, b + 8);
            long decompLen = ReadI64LE(sd, b + 16);
            long dataPtr = ReadI64LE(sd, b + 24);

            byte[] nameBytes = sd.Slice((int)namePtr, (int)nameLen).ToArray();
            Crypt(nameBytes);
            string name = CStr(nameBytes);

            byte[] comp = sd.Slice((int)dataPtr, (int)dataLen).ToArray();
            Crypt(comp);
            result[name] = Inflate(comp, decompLen);
        }
        return result;
    }

    private static byte[] ReadShared(string path)
    {
        using var fs = new FileStream(path, FileMode.Open, FileAccess.Read, FileShare.ReadWrite);
        byte[] buf = new byte[fs.Length];
        int read = 0;
        while (read < buf.Length)
        {
            int n = fs.Read(buf, read, buf.Length - read);
            if (n == 0) break;
            read += n;
        }
        return buf;
    }

    private static byte[] Inflate(byte[] encrypted, long decompLen)
    {
        // zlib stream = 0x78 0xF9 header (FDICT set) + the (decrypted) deflate body w/ DICTID.
        byte[] input = new byte[2 + encrypted.Length];
        input[0] = 0x78; input[1] = 0xF9;
        Buffer.BlockCopy(encrypted, 0, input, 2, encrypted.Length);

        var cod = new ZlibCodec(CompressionMode.Decompress);
        cod.InitializeInflate(15, true);
        cod.InputBuffer = input; cod.NextIn = 0; cod.AvailableBytesIn = input.Length;
        byte[] output = new byte[decompLen];
        cod.OutputBuffer = output; cod.NextOut = 0; cod.AvailableBytesOut = output.Length;

        int r = cod.Inflate(FlushType.Finish);
        if (r == ZlibConstants.Z_NEED_DICT)
        {
            cod.SetDictionary(Dict);
            cod.Inflate(FlushType.Finish);
        }
        cod.EndInflate();
        return output;
    }

    private static void Crypt(byte[] data)
    {
        int n = data.Length, i = 0;
        while (n - i >= 8)
        {
            ulong v = BitConverter.ToUInt64(data, i) ^ XOR_KEY;
            BitConverter.GetBytes(v).CopyTo(data, i); i += 8;
        }
        if (n - i >= 4)
        {
            uint v = BitConverter.ToUInt32(data, i) ^ (uint)(XOR_KEY & 0xFFFFFFFF);
            BitConverter.GetBytes(v).CopyTo(data, i); i += 4;
        }
        if (n - i >= 2)
        {
            ushort v = (ushort)(BitConverter.ToUInt16(data, i) ^ (ushort)(XOR_KEY & 0xFFFF));
            BitConverter.GetBytes(v).CopyTo(data, i); i += 2;
        }
        if (n - i >= 1) data[i] ^= (byte)(XOR_KEY & 0xFF);
    }

    private static ReadOnlySpan<byte> AsSpan(byte[] d, int o, int l) => new ReadOnlySpan<byte>(d, o, l);
    private static int ReadU32BE(byte[] d, int o) => (d[o] << 24) | (d[o + 1] << 16) | (d[o + 2] << 8) | d[o + 3];
    private static uint ReadU32LE(ReadOnlySpan<byte> d, int o) => (uint)(d[o] | (d[o + 1] << 8) | (d[o + 2] << 16) | (d[o + 3] << 24));
    private static long ReadI64LE(ReadOnlySpan<byte> d, int o) { long v = 0; for (int k = 7; k >= 0; k--) v = (v << 8) | d[o + k]; return v; }
    private static string CStr(byte[] b) { int e = Array.IndexOf(b, (byte)0); return System.Text.Encoding.UTF8.GetString(b, 0, e < 0 ? b.Length : e); }
}
