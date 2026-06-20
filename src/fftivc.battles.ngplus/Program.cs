using System;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices;

using Reloaded.Hooks.Definitions;
using Reloaded.Memory.SigScan.ReloadedII.Interfaces;
using Reloaded.Mod.Interfaces;
using Reloaded.Mod.Interfaces.Internal;

namespace fftivc.battles.ngplus;

/// <summary>
/// New Game++ conditional code mod.
/// Detection SOLVED: the NG+ flag in the autosave resume format is byte 0x3F (==1 for NG+, ==0 for
/// normal), validated across 8 captures (4 NG+ / 4 normal) in both resume_enbtl_world.sav and
/// resume_enwm_main.sav. At battle entry the game writes the autosave ~2s before reading the ENTD,
/// so reading it in the ENTD hook is race-free and current.
/// This build: read the autosave at ENTD time, log the NG+ verdict (validation before the swap).
/// </summary>
public class Program : IMod
{
    private ILogger _logger = null!;
    private IModLoader _modLoader = null!;
    private IModConfig _modConfig = null!;
    private IReloadedHooks? _hooks;
    private IStartupScanner? _scanner;

    private unsafe delegate int FileReadRequestOffsetDelegate(int fileIndex, long sectorOffset, long size, void* outputPointer);
    private IHook<FileReadRequestOffsetDelegate>? _entdReadHook;

    private const int ENTD_INDEX_MIN = 224;
    private const int ENTD_INDEX_MAX = 227;

    // NG+ flag in the autosave resume format: byte 0x3F == 1 -> New Game+, == 0 -> normal.
    private const int NGPLUS_FLAG_OFFSET = 0x3F;
    private static readonly string[] ResumePreference = { "resume_enbtl_world.sav", "resume_enwm_main.sav" };

    private const string SIG_FILE_READ_REQUEST_OFFSET =
        "48 89 5C 24 ?? 48 89 6C 24 ?? 48 89 74 24 ?? 57 48 83 EC ?? 80 3D ?? ?? ?? ?? ?? 4C 89 CE";

    private volatile bool _isNgPlus;

    public unsafe void StartEx(IModLoaderV1 loaderApi, IModConfigV1 modConfigV1)
    {
        _modLoader = (IModLoader)loaderApi;
        _modConfig = (IModConfig)modConfigV1;
        _logger = (ILogger)_modLoader.GetLogger();
        _modLoader.GetController<IReloadedHooks>()?.TryGetTarget(out _hooks!);
        _modLoader.GetController<IStartupScanner>()?.TryGetTarget(out _scanner!);

        Log("loading [detect NG+ from autosave @0x3F, log verdict]...");
        if (_hooks is null) { Log("ERROR: IReloadedHooks unavailable."); return; }
        if (_scanner is null) { Log("ERROR: IStartupScanner unavailable."); return; }

        nint baseAddr = Process.GetCurrentProcess().MainModule!.BaseAddress;
        _scanner.AddMainModuleScan(SIG_FILE_READ_REQUEST_OFFSET, result =>
        {
            if (!result.Found) { Log("ERROR: fileReadRequestOffset signature NOT found."); return; }
            nint addr = baseAddr + result.Offset;
            Log($"Hooked fileReadRequestOffset @ 0x{addr:X}");
            _entdReadHook = _hooks!.CreateHook<FileReadRequestOffsetDelegate>(FileReadRequestOffsetImpl, addr).Activate();
        });
    }

    private unsafe int FileReadRequestOffsetImpl(int fileIndex, long sectorOffset, long size, void* outputPointer)
    {
        if (fileIndex >= ENTD_INDEX_MIN && fileIndex <= ENTD_INDEX_MAX)
        {
            DetectNgPlus();
            Log($"[observe] ENTD read: index={fileIndex} size=0x{size:X} | NG+={_isNgPlus}");
        }
        return _entdReadHook!.OriginalFunction(fileIndex, sectorOffset, size, outputPointer);
    }

    /// <summary>Decode the live autosave (non-locking) and read the NG+ flag (byte 0x3F).</summary>
    private void DetectNgPlus()
    {
        try
        {
            string? path = FindAutosavePath();
            if (path is null) { Log("[ngdetect] autosave not found"); return; }

            Dictionary<string, byte[]> files = SaveReader.Decode(path);

            // Diagnostic: log every resume file's flag byte so we can see which is fresh/current.
            foreach (var kv in files)
                if (kv.Key.StartsWith("resume_", StringComparison.OrdinalIgnoreCase) && kv.Value.Length > NGPLUS_FLAG_OFFSET)
                    Log($"[ngdetect] {kv.Key}: 0x3F={kv.Value[NGPLUS_FLAG_OFFSET]}");

            byte[]? resume = null;
            foreach (string name in ResumePreference)
                if (files.TryGetValue(name, out resume) && resume.Length > NGPLUS_FLAG_OFFSET) break;
                else resume = null;
            resume ??= files.Values.FirstOrDefault(b => b.Length > NGPLUS_FLAG_OFFSET);

            if (resume is null) { Log("[ngdetect] no resume file"); return; }
            _isNgPlus = resume[NGPLUS_FLAG_OFFSET] != 0;
        }
        catch (Exception ex) { Log($"[ngdetect] error: {ex.Message}"); }
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

    private void Log(string msg) => _logger.WriteLine($"[{DateTime.Now:HH:mm:ss.fff}] [{_modConfig.ModId}] {msg}");

    public void Suspend() { }
    public void Resume() { }
    public void Unload() { }
    public bool CanUnload() => false;
    public bool CanSuspend() => false;
    public Action Disposing => () => { };
}
