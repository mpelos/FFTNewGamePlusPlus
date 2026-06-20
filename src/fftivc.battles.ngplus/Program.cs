using System;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices;

using Reloaded.Hooks.Definitions;
using Reloaded.Memory.SigScan.ReloadedII.Interfaces;
using Reloaded.Mod.Interfaces;
using Reloaded.Mod.Interfaces.Internal;

using fftivc.utility.modloader.Interfaces.Tables;
using fftivc.utility.modloader.Interfaces.Tables.Models;
using fftivc.utility.modloader.Interfaces.Tables.Structures;

namespace fftivc.battles.ngplus;

/// <summary>
/// New Game++ conditional code mod.
/// Detection SOLVED: the NG+ flag in the autosave resume format is byte 0x3F (==1 for NG+, ==0 for
/// normal), validated across 8 captures (4 NG+ / 4 normal) in both resume_enbtl_world.sav and
/// resume_enwm_main.sav. At battle entry the game writes the autosave ~2s before reading the ENTD,
/// so reading it in the ENTD hook is race-free and current.
///
/// Two layers, applied in the ENTD read hook:
///  - Layer 1 (NG+ ONLY): swap the whole modded ENTD (enemies + composition + guests) from our
///    embedded entd\battle_entdN_ent.bin. Normal play keeps vanilla enemies -> first playthrough
///    unaffected. Makes the mod self-contained: the old data-only file-replacement mod
///    (fftivc.battles.rescale) is superseded and MUST be disabled or it would replace ENTD always.
///  - Layer 2 (ALWAYS): scale guests (named ally charIds) to party level whether NG+ or not. A
///    guest at party level never hardens a first playthrough, and patching every ENTD read removes
///    the dependency on detecting NG+ at the exact join cutscene (when the level bakes into the save).
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

    // ENTD file layout: a flat grid of 16 slots/entry x 0x28 bytes, 128 entries -> 0x14000, no header.
    private const long ENTD_FILE_SIZE = 0x14000;
    private const int SLOT_SIZE = 0x28;
    private const int SLOT_CHARID = 0x00; // unit/character id (named chars low; generics 0x80+)
    private const int SLOT_LEVEL = 0x03;  // level (>99 = party level + value-100; 100 = party level)
    private const int SLOT_JOB = 0x0A;    // main job id; ally guests keep job == charId (4/7)
    private const byte LEVEL_PARTY = 100;

    // Guests scale UNCONDITIONALLY (NG+ or not): a guest at party level never makes a first
    // playthrough harder (the party is low level early, so the guest just matches the team). This
    // also dodges the join-timing problem: the level bakes into the save at the join cutscene, and
    // patching every ENTD read means we don't depend on detecting NG+ at that exact moment.
    // charId set (extend as later-chapter guests are added). 0x04=Delita, 0x07=Argath (Chapter 1).
    // CRITICAL: Argath (0x07) also appears as the ENEMY BOSS at Ziekden (end of Ch1), where his slot
    // is re-jobbed to Knight (job 76). An ALLY guest always keeps job == charId (Delita job 4, Argath
    // job 7) across every appearance in the ENTD; only the Ziekden boss breaks that. So we scale a
    // guest slot ONLY when job == charId. This (a) lets the Ziekden boss keep his designed boss level
    // instead of being clamped to party level, and (b) fixes a real bug: in NORMAL play the scaler
    // would otherwise force vanilla boss-Argath (lvl 10) to 100, making the finale unwinnable on a
    // first playthrough — the exact thing the mod promises never to do.
    private static readonly HashSet<byte> GuestCharIds = new() { 0x04, 0x07 };

    // fftpack index -> modded ENTD bytes (embedded). Only populated for files we actually ship a
    // modded version of; an index with no entry passes through vanilla even in NG+.
    private readonly Dictionary<int, byte[]> _moddedEntd = new();

    // NG+ flag in the autosave resume format: byte 0x3F == 1 -> New Game+, == 0 -> normal.
    private const int NGPLUS_FLAG_OFFSET = 0x3F;
    // The current battle's ENTD GLOBAL entry number is stored as a u16 at 0x16C in the battle-state
    // resume files (resume_enbtl_main/attack/fturn.sav). Verified offline: 388=Gariland, 389=Mandalia.
    // Logging this at battle entry maps each story battle -> its ENTD entry with zero guesswork.
    private const int BATTLE_ENTRY_ID_OFFSET = 0x16C;
    private static readonly string[] BattleIdResumeFiles =
        { "resume_enbtl_main.sav", "resume_enbtl_attack.sav", "resume_enbtl_fturn.sav" };
    // Diagnostic: log the battle ENTD entry id read from the save. Set false once Ch1 is mapped.
    private const bool DIAG_LOG_BATTLE_ID = true;
    // resume_enwm_main.sav (world-map state of the LOADED game) is the freshest at battle-load time;
    // resume_enbtl_world lags (still the previous battle). Prefer enwm_main.
    private static readonly string[] ResumePreference = { "resume_enwm_main.sav", "resume_enbtl_world.sav" };

    private const string SIG_FILE_READ_REQUEST_OFFSET =
        "48 89 5C 24 ?? 48 89 6C 24 ?? 48 89 74 24 ?? 57 48 83 EC ?? 80 3D ?? ?? ?? ?? ?? 4C 89 CE";

    private volatile bool _isNgPlus;

    // --- NG+ SHOPS ---
    // The store inventory is two STATIC in-memory exe tables (parsed by the modloader): which shops
    // sell each item (ITEM_SHOPS_DATA), and each item's ShopAvailability (ITEM_COMMON_DATA) = the
    // story-progress milestone it unlocks at (1=Chapter1_Start .. 16=Chapter4_KillZalbag, 0=never).
    // An item shows iff availability <= currentProgress AND its shop bit is set. In NG+ progress
    // resets -> only availability=1 items show. Fix: in NG+, lower every normally-sold item's
    // availability to Chapter1_Start so the full endgame stock is available immediately; restore
    // originals in normal play. We patch via the modloader's IFFTOItemDataManager controller.
    private IFFTOItemDataManager? _itemMgr;
    private const int ITEM_COUNT = 256;
    // world_* files (fftpack indices 765-772) load on world-map/town entry, BEFORE any shop opens.
    private const int WORLD_INDEX_MIN = 765;
    private const int WORLD_INDEX_MAX = 772;
    // menu_bk_shop / shop2 / shop3 (741-743) are read EVERY time the Outfitter opens -> the reliable
    // per-open trigger (world_* files get cached within a session and don't re-fire on save switch,
    // which left endgame stock stuck when loading a normal save after an NG+ one).
    private const int SHOP_UI_INDEX_MIN = 741;
    private const int SHOP_UI_INDEX_MAX = 743;
    private enum ShopState { Unknown, EndgameApplied, VanillaRestored }
    private ShopState _shopState = ShopState.Unknown;
    private DateTime _lastShopSync = DateTime.MinValue;
    private readonly List<int> _patchedItemIds = new();

    // DIAGNOSTIC (shop discovery): log each fftpack file index the first time it is read this
    // session, so newly-read indices when entering a town / opening a shop reveal the store-data
    // file. Set false to disable. globalIndex - 223 = line number in 0002_files.txt (if in 0002.pac).
    private const bool DIAG_LOG_READS = true;
    private readonly HashSet<int> _seenReadIndices = new();

    // --- RAM SAVE DUMP DIAGNOSTIC (locate the live NG+ flag in g_WorkMem) ---
    // Nenkai's RE notes: the live save data sits inside the 0x400440-byte g_WorkMem buffer. We resolve
    // the g_WorkMem pointer via the documented ref `add rbx,[rip+g_WorkMem]; test r8,r8`, then dump the
    // whole buffer to disk when a shop opens. Comparing a matched NG+ vs normal save (same story point)
    // reveals the NG+ flag byte by diff (same method that found autosave 0x3F) -> reliable at-any-time
    // detection that survives restart and needs no battle.
    private const bool DIAG_DUMP_WORKMEM = true;
    private const string SIG_WORKMEM = "48 03 1D ?? ?? ?? ?? 4D 85 C0";
    private const long WORKMEM_SIZE = 0x400440;
    private nint _workMemPtrAddr;          // address of the g_WorkMem pointer variable (module data)
    private int _dumpSeq;
    private DateTime _lastDump = DateTime.MinValue;

    [DllImport("kernel32.dll")] private static extern bool ReadProcessMemory(nint hProcess, nint lpBaseAddress, byte[] lpBuffer, nint dwSize, out nint lpNumberOfBytesRead);
    [DllImport("kernel32.dll")] private static extern nint GetCurrentProcess();

    public unsafe void StartEx(IModLoaderV1 loaderApi, IModConfigV1 modConfigV1)
    {
        _modLoader = (IModLoader)loaderApi;
        _modConfig = (IModConfig)modConfigV1;
        _logger = (ILogger)_modLoader.GetLogger();
        _modLoader.GetController<IReloadedHooks>()?.TryGetTarget(out _hooks!);
        _modLoader.GetController<IStartupScanner>()?.TryGetTarget(out _scanner!);

        Log("loading [M3: conditional ENTD swap in NG+]...");
        if (_hooks is null) { Log("ERROR: IReloadedHooks unavailable."); return; }
        if (_scanner is null) { Log("ERROR: IStartupScanner unavailable."); return; }

        LoadModdedEntd();

        _modLoader.GetController<IFFTOItemDataManager>()?.TryGetTarget(out _itemMgr!);
        Log(_itemMgr is null
            ? "WARNING: IFFTOItemDataManager unavailable -> NG+ shops disabled (update the modloader?)."
            : "IFFTOItemDataManager acquired -> NG+ endgame shops enabled.");

        nint baseAddr = Process.GetCurrentProcess().MainModule!.BaseAddress;
        _scanner.AddMainModuleScan(SIG_FILE_READ_REQUEST_OFFSET, result =>
        {
            if (!result.Found) { Log("ERROR: fileReadRequestOffset signature NOT found."); return; }
            nint addr = baseAddr + result.Offset;
            Log($"Hooked fileReadRequestOffset @ 0x{addr:X}");
            _entdReadHook = _hooks!.CreateHook<FileReadRequestOffsetDelegate>(FileReadRequestOffsetImpl, addr).Activate();
        });

        if (DIAG_DUMP_WORKMEM)
            _scanner.AddMainModuleScan(SIG_WORKMEM, r =>
            {
                if (!r.Found) { Log("[ramdump] g_WorkMem signature NOT found."); return; }
                nint instr = baseAddr + r.Offset;
                int rel32 = Marshal.ReadInt32(instr + 3);     // disp of `add rbx,[rip+disp]` (7-byte instr)
                _workMemPtrAddr = instr + 7 + rel32;           // address of the g_WorkMem pointer variable
                Log($"[ramdump] g_WorkMem ptr-var @ 0x{_workMemPtrAddr:X} (instr @ 0x{instr:X})");
            });
    }

    /// <summary>Dump the whole g_WorkMem buffer to disk so NG+ vs normal can be diffed for the flag.</summary>
    private void DumpWorkMem(string tag)
    {
        if (!DIAG_DUMP_WORKMEM || _workMemPtrAddr == 0) return;
        if (_dumpSeq >= 8) return;                                   // cap disk usage
        if ((DateTime.Now - _lastDump).TotalSeconds < 8) return;     // throttle
        long workMemBase = Marshal.ReadInt64(_workMemPtrAddr);       // pointer var is committed module data
        if (workMemBase <= 0x10000) { Log($"[ramdump] g_WorkMem not allocated yet (0x{workMemBase:X})"); return; }

        var buf = new byte[WORKMEM_SIZE];
        if (!ReadProcessMemory(GetCurrentProcess(), (nint)workMemBase, buf, (nint)WORKMEM_SIZE, out nint read) || read == 0)
        {
            Log($"[ramdump] ReadProcessMemory failed (base=0x{workMemBase:X}, read={read})");
            return;
        }
        _lastDump = DateTime.Now;
        int seq = ++_dumpSeq;
        string dir = Path.Combine(_modLoader.GetDirectoryForModId(_modConfig.ModId), "ramdumps");
        Directory.CreateDirectory(dir);
        string path = Path.Combine(dir, $"workmem_{DateTime.Now:HHmmss}_{seq:D2}.bin");
        try
        {
            File.WriteAllBytes(path, read == (nint)WORKMEM_SIZE ? buf : buf[..(int)read]);
            Log($"[ramdump] #{seq} [{tag}] base=0x{workMemBase:X} size=0x{(long)read:X} -> {path}");
        }
        catch (Exception ex) { Log($"[ramdump] write failed: {ex.Message}"); }
    }

    private unsafe int FileReadRequestOffsetImpl(int fileIndex, long sectorOffset, long size, void* outputPointer)
    {
        // Let the original read happen first: it fills outputPointer with the vanilla file bytes and
        // returns whatever status/byte-count the game expects. We only mutate the buffer afterwards.
        int ret = _entdReadHook!.OriginalFunction(fileIndex, sectorOffset, size, outputPointer);

        // Diagnostic: first time we see each index, log it (size+offset help spot the small store table).
        if (DIAG_LOG_READS && _seenReadIndices.Add(fileIndex))
            Log($"[read-new] index={fileIndex} size=0x{size:X} off=0x{sectorOffset:X}");

        // Sync shops on world-map/town entry (world_* 765-772) AND on every Outfitter open
        // (menu_bk_shop* 741-743). The latter is the reliable per-open trigger that catches save
        // switches within a session (where world_* are cached and don't re-fire).
        if ((fileIndex >= WORLD_INDEX_MIN && fileIndex <= WORLD_INDEX_MAX) ||
            (fileIndex >= SHOP_UI_INDEX_MIN && fileIndex <= SHOP_UI_INDEX_MAX))
            SyncShops();

        // RAM dump diagnostic: capture the live save buffer when the Outfitter opens (shop UI reads).
        if (DIAG_DUMP_WORKMEM && fileIndex >= SHOP_UI_INDEX_MIN && fileIndex <= SHOP_UI_INDEX_MAX)
            DumpWorkMem("shop-open");

        if (fileIndex >= ENTD_INDEX_MIN && fileIndex <= ENTD_INDEX_MAX && outputPointer != null)
        {
            DetectNgPlus();

            // The game reads the whole ENTD file in one shot (sectorOffset 0, size == file length).
            bool fullRead = sectorOffset == 0 && size == ENTD_FILE_SIZE;
            bool haveMod = _moddedEntd.TryGetValue(fileIndex, out byte[]? modded);

            // Layer 1 (NG+ only): swap the whole modded file (enemies + composition + guests).
            if (_isNgPlus && fullRead && haveMod && modded!.Length == size)
            {
                Marshal.Copy(modded!, 0, (IntPtr)outputPointer, modded!.Length);
                Log($"[swap] ENTD index={fileIndex} -> MODDED ({modded.Length} bytes) [NG+]");
            }
            else
            {
                string why = !_isNgPlus ? "normal play"
                           : !haveMod ? "no modded file"
                           : !fullRead ? $"partial read (off=0x{sectorOffset:X} size=0x{size:X})"
                           : "size mismatch";
                Log($"[pass] ENTD index={fileIndex} size=0x{size:X} -> vanilla enemies ({why})");
            }

            // Layer 2 (ALWAYS): scale guests to party level, in NG+ and normal alike. Runs after the
            // swap so it's a no-op on a modded file (guests already 100) and the fix on vanilla.
            if (fullRead) ScaleGuestsAlways(outputPointer, size);
        }
        return ret;
    }

    /// <summary>Load every embedded modded ENTD (entd\battle_entdN_ent.bin) into the index map.</summary>
    private void LoadModdedEntd()
    {
        var asm = typeof(Program).Assembly;
        // Map each fftpack ENTD index to its filename.
        var indexToName = new (int idx, string file)[]
        {
            (224, "battle_entd1_ent.bin"),
            (225, "battle_entd2_ent.bin"),
            (226, "battle_entd3_ent.bin"),
            (227, "battle_entd4_ent.bin"),
        };
        foreach (var (idx, file) in indexToName)
        {
            string res = $"fftivc.battles.ngplus.entd.{file}";
            using Stream? s = asm.GetManifestResourceStream(res);
            if (s is null) continue;
            using var ms = new MemoryStream();
            s.CopyTo(ms);
            _moddedEntd[idx] = ms.ToArray();
            Log($"[init] loaded modded {file} (index {idx}, {_moddedEntd[idx].Length} bytes)");
        }
        if (_moddedEntd.Count == 0) Log("[init] WARNING: no modded ENTD embedded; will pass through vanilla.");
    }

    /// <summary>
    /// Force every guest slot (charId in GuestCharIds) to party level (LEVEL_PARTY). The ENTD buffer
    /// is a flat grid of 0x28-byte slots, so each slot-aligned offset's first byte is its charId.
    /// </summary>
    private unsafe void ScaleGuestsAlways(void* buffer, long size)
    {
        byte* p = (byte*)buffer;
        int patched = 0;
        for (long off = 0; off + SLOT_SIZE <= size; off += SLOT_SIZE)
        {
            // Only the genuine ally guest (job == charId). Skips the Ziekden boss (Argath re-jobbed
            // to Knight), so his designed level stands and a normal playthrough's finale isn't broken.
            if (GuestCharIds.Contains(p[off + SLOT_CHARID]) && p[off + SLOT_JOB] == p[off + SLOT_CHARID]
                && p[off + SLOT_LEVEL] != LEVEL_PARTY)
            {
                p[off + SLOT_LEVEL] = LEVEL_PARTY;
                patched++;
            }
        }
        if (patched > 0) Log($"[guest] scaled {patched} guest slot(s) to party level");
    }

    /// <summary>
    /// Re-detect NG+ and bring the in-memory shop tables to the desired state: endgame stock in NG+,
    /// vanilla otherwise. Throttled (the world_* burst triggers this several times) and idempotent.
    /// </summary>
    private void SyncShops()
    {
        if (_itemMgr is null) return;
        if ((DateTime.Now - _lastShopSync).TotalSeconds < 0.5) return; // collapse read bursts only
        _lastShopSync = DateTime.Now;

        DetectNgPlus();
        if (_isNgPlus && _shopState != ShopState.EndgameApplied)
        {
            ApplyEndgameShops();
            _shopState = ShopState.EndgameApplied;
        }
        else if (!_isNgPlus && _shopState != ShopState.VanillaRestored)
        {
            RestoreVanillaShops();
            _shopState = ShopState.VanillaRestored;
        }
    }

    /// <summary>NG+: lower every normally-sold item's availability to Chapter1_Start (everything in stock now).</summary>
    private void ApplyEndgameShops()
    {
        _patchedItemIds.Clear();
        for (int id = 0; id < ITEM_COUNT; id++)
        {
            ItemShopAvailability? avail = _itemMgr!.GetOriginalItem(id).ShopAvailability;
            // Only items that are EVER sold (availability != Blank). Leave never-sold (0) items unsold.
            if (avail is null || avail == ItemShopAvailability.Blank) continue;
            _itemMgr.ApplyTablePatch(_modConfig.ModId, new Item { Id = id, ShopAvailability = ItemShopAvailability.Chapter1_Start });
            _patchedItemIds.Add(id);
        }
        Log($"[shops] NG+ -> endgame stock: {_patchedItemIds.Count} items unlocked from Chapter 1.");
    }

    /// <summary>Normal play: restore the original availability of every item we lowered.</summary>
    private void RestoreVanillaShops()
    {
        int n = 0;
        foreach (int id in _patchedItemIds)
        {
            ItemShopAvailability? orig = _itemMgr!.GetOriginalItem(id).ShopAvailability;
            _itemMgr.ApplyTablePatch(_modConfig.ModId, new Item { Id = id, ShopAvailability = orig });
            n++;
        }
        _patchedItemIds.Clear();
        Log($"[shops] normal play -> restored vanilla availability for {n} items.");
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

            // Diagnostic: log the current battle's ENTD entry id (u16 @ 0x16C) so we can map each
            // story battle to its ENTD entry just by entering it in-game.
            if (DIAG_LOG_BATTLE_ID)
                foreach (string name in BattleIdResumeFiles)
                    if (files.TryGetValue(name, out byte[]? b) && b.Length > BATTLE_ENTRY_ID_OFFSET + 1)
                    {
                        int entry = b[BATTLE_ENTRY_ID_OFFSET] | (b[BATTLE_ENTRY_ID_OFFSET + 1] << 8);
                        Log($"[battle-id] {name}: ENTD entry = {entry}");
                    }

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
