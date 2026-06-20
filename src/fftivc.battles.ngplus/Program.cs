using System;
using System.Diagnostics;
using System.IO;
using System.Runtime.InteropServices;

using FF16Tools.Files.Save;

using Reloaded.Hooks.Definitions;
using Reloaded.Memory.SigScan.ReloadedII.Interfaces;
using Reloaded.Mod.Interfaces;
using Reloaded.Mod.Interfaces.Internal;

namespace fftivc.battles.ngplus;

/// <summary>
/// New Game++ conditional code mod.
/// Milestone 1 (done): hook the fftpack reader, observe ENTD reads (the game reads the whole
///   entd file 0x14000 at once -> a single overwrite will suffice for the swap).
/// Milestone 2 (this): also hook faith ResourceManager::OpenFileAndCache and log .png file
///   accesses, to learn whether/when the save files (enhanced.png / autoenhanced.png) are read
///   through this path (the basis for NG+ detection).
/// </summary>
public class Program : IMod
{
    private ILogger _logger = null!;
    private IModLoader _modLoader = null!;
    private IModConfig _modConfig = null!;
    private IReloadedHooks? _hooks;
    private IStartupScanner? _scanner;

    // int fileReadRequestOffset(int fileIndex, long sectorOffset, long size, void* outputPointer)
    private unsafe delegate int FileReadRequestOffsetDelegate(int fileIndex, long sectorOffset, long size, void* outputPointer);
    private IHook<FileReadRequestOffsetDelegate>? _entdReadHook;

    // void faith::Resource::ResourceManager::OpenFileAndCache(void* a1, FileResult* a2)
    private unsafe delegate void OpenFileAndCacheDelegate(void* a1, FileResult* a2);
    private IHook<OpenFileAndCacheDelegate>? _openFileHook;

    private const int ENTD_INDEX_MIN = 224;
    private const int ENTD_INDEX_MAX = 227;

    // Signatures reused from Nenkai/fftivc.utility.modloader (open source).
    private const string SIG_FILE_READ_REQUEST_OFFSET =
        "48 89 5C 24 ?? 48 89 6C 24 ?? 48 89 74 24 ?? 57 48 83 EC ?? 80 3D ?? ?? ?? ?? ?? 4C 89 CE";
    private const string SIG_OPEN_FILE_AND_CACHE =
        "48 8B C4 48 89 58 ?? 48 89 68 ?? 48 89 70 ?? 48 89 78 ?? 41 56 48 83 EC ?? 33 ED 48 8B F2";

    public unsafe void StartEx(IModLoaderV1 loaderApi, IModConfigV1 modConfigV1)
    {
        _modLoader = (IModLoader)loaderApi;
        _modConfig = (IModConfig)modConfigV1;
        _logger = (ILogger)_modLoader.GetLogger();
        _modLoader.GetController<IReloadedHooks>()?.TryGetTarget(out _hooks!);
        _modLoader.GetController<IStartupScanner>()?.TryGetTarget(out _scanner!);

        Log("New Game++ (NG+ conditional) loading [Milestone 2: observe ENTD reads + .png file loads]...");

        if (_hooks is null) { Log("ERROR: IReloadedHooks unavailable - is reloaded.sharedlib.hooks a dependency?"); return; }
        if (_scanner is null) { Log("ERROR: IStartupScanner unavailable - is Reloaded.Memory.SigScan.ReloadedII a dependency?"); return; }

        nint baseAddr = Process.GetCurrentProcess().MainModule!.BaseAddress;

        _scanner.AddMainModuleScan(SIG_FILE_READ_REQUEST_OFFSET, result =>
        {
            if (!result.Found) { Log("ERROR: fileReadRequestOffset signature NOT found."); return; }
            nint addr = baseAddr + result.Offset;
            Log($"Hooked fileReadRequestOffset @ 0x{addr:X}");
            _entdReadHook = _hooks!.CreateHook<FileReadRequestOffsetDelegate>(FileReadRequestOffsetImpl, addr).Activate();
        });

        _scanner.AddMainModuleScan(SIG_OPEN_FILE_AND_CACHE, result =>
        {
            if (!result.Found) { Log("ERROR: OpenFileAndCache signature NOT found."); return; }
            nint addr = baseAddr + result.Offset;
            Log($"Hooked OpenFileAndCache @ 0x{addr:X}");
            _openFileHook = _hooks!.CreateHook<OpenFileAndCacheDelegate>(OpenFileAndCacheImpl, addr).Activate();
        });
    }

    private unsafe int FileReadRequestOffsetImpl(int fileIndex, long sectorOffset, long size, void* outputPointer)
    {
        if (fileIndex >= ENTD_INDEX_MIN && fileIndex <= ENTD_INDEX_MAX)
        {
            Log($"[observe] ENTD read: index={fileIndex} byteOffset=0x{sectorOffset * 0x800:X} size=0x{size:X}");
            LogNgPlusFlagFromAutosave();
        }

        return _entdReadHook!.OriginalFunction(fileIndex, sectorOffset, size, outputPointer);
    }

    // Resume-file NG+ flag offset in the autosave (manual 0x08AFB + 0x154 header).
    private const int NGPLUS_FLAG_OFFSET_RESUME = 0x8C4F;

    /// <summary>
    /// Reads the live autosave (autoenhanced.png), decodes it, and logs the NG+ flag from each
    /// resume_* inner file. The autosave is rewritten on entering a battle, so it reflects the
    /// game we're about to fight in. Diagnostic for Milestone 2.
    /// </summary>
    private void LogNgPlusFlagFromAutosave()
    {
        try
        {
            string? autosave = FindAutosavePath();
            if (autosave is null) { Log("[ngdetect] autosave path not found"); return; }

            FaithSaveGameData sav = FaithSaveGameData.Open(autosave);
            foreach (var kv in sav.Files)
            {
                if (kv.Key.StartsWith("resume_", StringComparison.OrdinalIgnoreCase)
                    && kv.Value.Length > NGPLUS_FLAG_OFFSET_RESUME)
                {
                    Log($"[ngdetect] {kv.Key}: flag@0x{NGPLUS_FLAG_OFFSET_RESUME:X}={kv.Value[NGPLUS_FLAG_OFFSET_RESUME]}");
                }
            }
        }
        catch (Exception ex)
        {
            Log($"[ngdetect] error reading autosave: {ex.Message}");
        }
    }

    private static string? FindAutosavePath()
    {
        string docs = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments);
        string baseDir = Path.Combine(docs, "My Games", "FINAL FANTASY TACTICS - The Ivalice Chronicles", "Steam");
        if (!Directory.Exists(baseDir)) return null;
        foreach (string steamDir in Directory.GetDirectories(baseDir))
        {
            string p = Path.Combine(steamDir, "autoenhanced.png");
            if (File.Exists(p)) return p;
        }
        return null;
    }

    private unsafe void OpenFileAndCacheImpl(void* a1, FileResult* a2)
    {
        _openFileHook!.OriginalFunction(a1, a2);

        if (a2 != null && a2->PathPtr != null)
        {
            string? path = Marshal.PtrToStringAnsi((nint)a2->PathPtr);
            if (path != null && path.Contains(".png", StringComparison.OrdinalIgnoreCase))
                Log($"[observe] file loaded: {path} (0x{a2->FileSize:X} bytes)");
        }
    }

    private void Log(string msg) => _logger.WriteLine($"[{_modConfig.ModId}] {msg}");

    // Layout from Nenkai/fftivc.utility.modloader ResourceManagerHooks.FileResult ("stolen from ff16").
    public unsafe struct FileResult
    {
        public void* VTable;
        public uint field_0x08;
        public uint handleId;
        public ulong field_0x10;
        public char* PathPtr;
        public ushort field_0x20;
        public ushort field_0x22;
        public ushort field_0x24;
        public ushort field_0x26;
        public void* field_0x28;
        public void* field_0x30;
        public ulong Empty;
        public ulong FileSize;
        public ulong Field_0x48;
        public uint field_0x50;
        public uint field_0x54;
    }

    /* Reloaded mod-loader lifecycle (no-ops for now). */
    public void Suspend() { }
    public void Resume() { }
    public void Unload() { }
    public bool CanUnload() => false;
    public bool CanSuspend() => false;
    public Action Disposing => () => { };
}
