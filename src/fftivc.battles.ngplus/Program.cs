using System;
using System.Diagnostics;
using System.Runtime.InteropServices;

using Reloaded.Hooks.Definitions;
using Reloaded.Memory.SigScan.ReloadedII.Interfaces;
using Reloaded.Mod.Interfaces;
using Reloaded.Mod.Interfaces.Internal;

namespace fftivc.battles.ngplus;

/// <summary>
/// New Game++ conditional code mod.
/// SAFE build: only observes. (The CloseHandle hook from M2c crashed the CLR — CloseHandle is on
/// the GC/runtime hot path, so we must never hook it.) Hooks here are limited to the fftpack
/// reader (ENTD observe) and CreateFileW (save-file open observe). No autosave decoding (the
/// autosave/resume format has no cleanly-locatable NG+ flag with the data we have).
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

    private delegate nint CreateFileWDelegate(nint name, uint access, uint share, nint sa, uint disp, uint flags, nint tmpl);
    private IHook<CreateFileWDelegate>? _createFileHook;

    private const int ENTD_INDEX_MIN = 224;
    private const int ENTD_INDEX_MAX = 227;
    private const uint GENERIC_WRITE = 0x40000000;
    private const uint GENERIC_READ = 0x80000000;

    private const string SIG_FILE_READ_REQUEST_OFFSET =
        "48 89 5C 24 ?? 48 89 6C 24 ?? 48 89 74 24 ?? 57 48 83 EC ?? 80 3D ?? ?? ?? ?? ?? 4C 89 CE";

    [DllImport("kernel32", CharSet = CharSet.Ansi)] private static extern nint GetModuleHandleA(string name);
    [DllImport("kernel32", CharSet = CharSet.Ansi)] private static extern nint GetProcAddress(nint module, string name);

    public unsafe void StartEx(IModLoaderV1 loaderApi, IModConfigV1 modConfigV1)
    {
        _modLoader = (IModLoader)loaderApi;
        _modConfig = (IModConfig)modConfigV1;
        _logger = (ILogger)_modLoader.GetLogger();
        _modLoader.GetController<IReloadedHooks>()?.TryGetTarget(out _hooks!);
        _modLoader.GetController<IStartupScanner>()?.TryGetTarget(out _scanner!);

        Log("loading [SAFE observe build]...");
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

        nint k32 = GetModuleHandleA("kernel32.dll");
        nint createFileW = k32 != 0 ? GetProcAddress(k32, "CreateFileW") : 0;
        if (createFileW != 0) { _createFileHook = _hooks.CreateHook<CreateFileWDelegate>(CreateFileWImpl, createFileW).Activate(); Log($"Hooked CreateFileW @ 0x{createFileW:X}"); }
        else Log("ERROR: could not resolve CreateFileW.");
    }

    private nint CreateFileWImpl(nint name, uint access, uint share, nint sa, uint disp, uint flags, nint tmpl)
    {
        nint handle = _createFileHook!.OriginalFunction(name, access, share, sa, disp, flags, tmpl);
        try
        {
            string? path = name != 0 ? Marshal.PtrToStringUni(name) : null;
            if (path != null && path.Contains("enhanced.png", StringComparison.OrdinalIgnoreCase))
            {
                string mode = (access & GENERIC_WRITE) != 0 ? "WRITE" : (access & GENERIC_READ) != 0 ? "READ" : $"0x{access:X}";
                Log($"[fileopen] {mode}: {path}");
            }
        }
        catch { }
        return handle;
    }

    private unsafe int FileReadRequestOffsetImpl(int fileIndex, long sectorOffset, long size, void* outputPointer)
    {
        if (fileIndex >= ENTD_INDEX_MIN && fileIndex <= ENTD_INDEX_MAX)
            Log($"[observe] ENTD read: index={fileIndex} byteOffset=0x{sectorOffset * 0x800:X} size=0x{size:X}");

        return _entdReadHook!.OriginalFunction(fileIndex, sectorOffset, size, outputPointer);
    }

    private void Log(string msg) => _logger.WriteLine($"[{_modConfig.ModId}] {msg}");

    public void Suspend() { }
    public void Resume() { }
    public void Unload() { }
    public bool CanUnload() => false;
    public bool CanSuspend() => false;
    public Action Disposing => () => { };
}
