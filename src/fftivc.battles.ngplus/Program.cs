using System;
using System.Diagnostics;

using Reloaded.Hooks.Definitions;
using Reloaded.Memory.SigScan.ReloadedII.Interfaces;
using Reloaded.Mod.Interfaces;
using Reloaded.Mod.Interfaces.Internal;

namespace fftivc.battles.ngplus;

/// <summary>
/// New Game++ conditional code mod.
/// Milestone 1: hook the fftpack file reader and LOG every ENTD read (file indices 224-227),
/// to prove the mod loads alongside the modloader and the signature resolves in-game.
/// No data is changed yet.
/// </summary>
public class Program : IMod
{
    private ILogger _logger = null!;
    private IModLoader _modLoader = null!;
    private IModConfig _modConfig = null!;
    private IReloadedHooks? _hooks;
    private IStartupScanner? _scanner;

    // int fileReadRequestOffset(int fileIndex, long sectorOffset, long size, void* outputPointer)
    // Signature reused from Nenkai/fftivc.utility.modloader FFTPackHooks.cs.
    private unsafe delegate int FileReadRequestOffsetDelegate(int fileIndex, long sectorOffset, long size, void* outputPointer);
    private IHook<FileReadRequestOffsetDelegate>? _entdReadHook;

    // ENTD pack file indices (fftpack.txt): 224=entd1 .. 227=entd4.
    private const int ENTD_INDEX_MIN = 224;
    private const int ENTD_INDEX_MAX = 227;

    private const string SIG_FILE_READ_REQUEST_OFFSET =
        "48 89 5C 24 ?? 48 89 6C 24 ?? 48 89 74 24 ?? 57 48 83 EC ?? 80 3D ?? ?? ?? ?? ?? 4C 89 CE";

    public unsafe void StartEx(IModLoaderV1 loaderApi, IModConfigV1 modConfigV1)
    {
        _modLoader = (IModLoader)loaderApi;
        _modConfig = (IModConfig)modConfigV1;
        _logger = (ILogger)_modLoader.GetLogger();
        _modLoader.GetController<IReloadedHooks>()?.TryGetTarget(out _hooks!);
        _modLoader.GetController<IStartupScanner>()?.TryGetTarget(out _scanner!);

        Log("New Game++ (NG+ conditional) loading [Milestone 1: observe ENTD reads]...");

        if (_hooks is null)
        {
            Log("ERROR: IReloadedHooks unavailable - is reloaded.sharedlib.hooks a dependency?");
            return;
        }
        if (_scanner is null)
        {
            Log("ERROR: IStartupScanner unavailable - is Reloaded.Memory.SigScan.ReloadedII a dependency?");
            return;
        }

        nint baseAddr = Process.GetCurrentProcess().MainModule!.BaseAddress;
        _scanner.AddMainModuleScan(SIG_FILE_READ_REQUEST_OFFSET, result =>
        {
            if (!result.Found)
            {
                Log("ERROR: fileReadRequestOffset signature NOT found. (game update may have shifted it.)");
                return;
            }

            nint addr = baseAddr + result.Offset;
            Log($"Hooked fileReadRequestOffset @ 0x{addr:X}");
            _entdReadHook = _hooks!.CreateHook<FileReadRequestOffsetDelegate>(FileReadRequestOffsetImpl, addr).Activate();
        });
    }

    private unsafe int FileReadRequestOffsetImpl(int fileIndex, long sectorOffset, long size, void* outputPointer)
    {
        if (fileIndex >= ENTD_INDEX_MIN && fileIndex <= ENTD_INDEX_MAX)
            Log($"[observe] ENTD read: index={fileIndex} byteOffset=0x{sectorOffset * 0x800:X} size=0x{size:X}");

        // Observe only for now: always defer to the original (game / modloader).
        return _entdReadHook!.OriginalFunction(fileIndex, sectorOffset, size, outputPointer);
    }

    private void Log(string msg) => _logger.WriteLine($"[{_modConfig.ModId}] {msg}");

    /* Reloaded mod-loader lifecycle (no-ops for now). */
    public void Suspend() { }
    public void Resume() { }
    public void Unload() { }
    public bool CanUnload() => false;
    public bool CanSuspend() => false;
    public Action Disposing => () => { };
}
