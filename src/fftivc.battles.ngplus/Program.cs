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
    // charId set (extend as later-chapter guests are added). 0x04=Delita, 0x07=Argath (Chapter 1);
    // 0x22=Mustadio (Chapter 2 — reckless guest at Zaland/Goug; uncontrolled, charges in, and his
    // death is a Game Over on the protect path, so he MUST keep pace with the party);
    // 0x1e=Agrias (Chapter 2 — the "Save Agrias!" VIP at Balias Swale, isolated/outnumbered, whose
    // death FAILS the battle + recruit; she becomes a permanent party member right after, so she must
    // be at party level to survive the rescue).
    // CRITICAL: Argath (0x07) also appears as the ENEMY BOSS at Ziekden (end of Ch1), where his slot
    // is re-jobbed to Knight (job 76). An ALLY guest always keeps job == charId (Delita job 4, Argath
    // job 7, Mustadio job 34 == 0x22) across every appearance in the ENTD; only the Ziekden boss
    // breaks that. So we scale a guest slot ONLY when job == charId. This (a) lets the Ziekden boss
    // keep his designed boss level instead of being clamped to party level, and (b) fixes a real bug:
    // in NORMAL play the scaler would otherwise force vanilla boss-Argath (lvl 10) to 100, making the
    // finale unwinnable on a first playthrough — the exact thing the mod promises never to do.
    private static readonly HashSet<byte> GuestCharIds = new() { 0x04, 0x07, 0x22, 0x1e };

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
    private DateTime _lastShopSync = DateTime.MinValue;

    // We write ShopAvailability DIRECTLY into the live ITEM_COMMON_DATA table instead of via the
    // modloader's ApplyTablePatch. ApplyTablePatch tracks changes per (id, field) and re-applies them
    // when the item table is (re)read; that tracking locks the FIRST value we set in a session, so a
    // later "restore" never sticks (endgame stock stayed after switching NG+ -> normal). A direct write
    // fully under our control, re-asserted every sync, sidesteps that entirely. We locate the table by
    // the SAME signature the modloader uses (its literal item-0/1/2 bytes). Each entry is 0x0C bytes;
    // ShopAvailability is the byte at +0x0A. We snapshot the pristine availability once (from the live
    // table, before our first write, so it respects other mods) and restore to it in normal play.
    private const string SIG_ITEM_TABLE = "00 00 00 80 00 00 00 00 00 00 00 00 00 01 01 80 01 01 00 00 64 00 01 00 00 02 03 80 02 01 00 00";
    private const int ITEM_ENTRY_SIZE = 0x0C;
    private const int ITEM_SHOPAVAIL_OFFSET = 0x0A;
    private const byte AVAIL_BLANK = 0;          // never sold
    private const byte AVAIL_CHAPTER1_START = 1; // buyable from the very start
    private nint _itemTableBase;
    private readonly byte[] _origAvail = new byte[ITEM_COUNT];
    private bool _origCaptured;

    // NG+ DETECTION FOR SHOPS — LEVEL PROXY (found via Cheat Engine).
    // There is NO reliable "is NG+" byte in RAM: every flag-shaped candidate we found was noise that
    // did NOT reset when loading a normal save in the same session (the 0xD8D91C "flag" was a false
    // positive — it reads 0 even in a fresh NG+ process). What IS reliable and refreshes on every
    // save-load are the live gameplay globals (Gil is one, at module+0xD40110). So we detect NG+
    // INDIRECTLY: NG+ carries the prior playthrough's levels, so Ramza's level is high while story
    // progress is reset to chapter 1. A normal first playthrough has a low-level Ramza early; the only
    // false positive is normal mid/late game, where shops already sell most things anyway -> harmless.
    // NG+ proxy = Ramza's level in the live static globals (refreshes on save-load, so reliable at shop
    // time, unlike the stale autosave). Found via a Byte scan on the NG+ world map (so the Units-screen
    // int32 display buffers, which read 1 off that screen, don't match) plus 74->1->74 narrowing across
    // save switches, yielding 5 static copies. Across 6 test saves (Ramza 74/1/55/64/55/74), module+
    // 0x2C81D93 was correct 6/6, so we DECIDE on it alone. The other 4 are lazy mirrors that lag at the
    // previous save's level (seen sticking at 37 and 1; which lag depends on load order) -> logged only
    // as diagnostics so that IF a bug surfaces we already have the data to switch to a more robust rule
    // (e.g. median of the copies that agree). SEE the memory note [[fft-tic-shop-ngplus]]: the strategy
    // MUST change if 0x2C81D93 is ever observed wrong. The autosave 0x3F flag stays the source for
    // BATTLE context (fresh at battle entry); only shops use this proxy. There is NO reliable raw "is
    // NG+" RAM byte (every flag-shaped candidate was noise that failed to reset on a same-session load).
    private const long RAMZA_LEVEL_RVA = 0x2C81D93;
    private static readonly long[] RamzaLevelDiagRvas = { 0x11A7D2D, 0x2C81D93, 0x11AF25D, 0x2C821B5, 0x2C896E5 };

    // Live currentStoryProgress (1..16, the ItemShopAvailability milestone scale; 0=prologue,
    // 1=Chapter1_Start, ... 16=Chapter4_KillZalbag = end of Cap 4). Found by reverse-engineering the
    // manual save (slot+0x87F0 reads 16 at end-game, 1 at Cap1) then a known-value CE scan (Cap1=1,
    // Cap4=16). Two static copies track identically: 0xD4021C sits next to the reliable Gil global
    // (0xD40110) in the global game-state block -> PRIMARY; 0x2C8A470 is in the 0x2C8xxxx unit region,
    // the same neighbourhood as the LAGGY Ramza-level mirrors -> diagnostic only. Both logged; switch
    // the primary if it is ever observed to lag (mirrors the level strategy). NOTE: the adjacent byte
    // 0x2C81D94 is Ramza's JOB, not progress (an early red herring) -> do not use it.
    private const long STORY_PROGRESS_RVA = 0xD4021C;
    private static readonly long[] StoryProgressDiagRvas = { 0xD4021C, 0x2C8A470 };

    // Per-progress NG+ level threshold (user's rule): the Cap 1 threshold = the minimum level to finish
    // the game normally (~30), rising linearly to 45 at end-game (progress 16). A normal playthrough's
    // level never crosses it (level and progress climb together); NG+'s carried-over level (55+) always
    // does. threshold(p) = FLOOR + (p-1)*(TOP-FLOOR)/15. See [[fft-tic-shop-ngplus]].
    private const int NGPLUS_THRESHOLD_FLOOR = 30; // progress 1 (Chapter1_Start)
    private const int NGPLUS_THRESHOLD_TOP = 45;   // progress 16 (Chapter4_KillZalbag)
    private nint _moduleBase;

    // --- NG+ MAP TREASURES (Move-Find Items = "battle rewards") ---
    // Each map has up to 4 hidden treasure tiles (MAP_TRAP_FORMATION_DATA, 0x18 bytes/map, 128 maps).
    // Per item (6 bytes): XY(1) TrapFlags(1) RareItemId(u16 @+2) CommonItemId(u16 @+4). The hardcoded
    // in-memory table is the same one the modloader's MapTrapData.xml overwrites. In NG+ we upgrade
    // each Chapter-1 treasure to the strongest NON-reserved item in its ORIGINAL category (endgame-best
    // gear stays reserved for later), and bump the consolation consumable to a post-game tier; in normal
    // play we restore the captured vanilla values so a first playthrough is untouched. We DIRECT-WRITE
    // the live table (NOT the modloader's ApplyTablePatch, which locks the first value per field and so
    // can't restore on an NG+->normal save switch — the exact problem the shops hit). Detection reuses
    // the same NG+ level proxy as the shops (fresh on every save-load); see [[fft-tic-shop-ngplus]].
    // Signature anchors at the START of map 85's entry (Mandalia, r1/r19/r51/r59) and runs through maps
    // 86-87; XY+flags bytes are wildcarded (volatile / not needed), rare+common u16s are the literal
    // fingerprint. tableBase = matchAddr - 85*0x18.
    private const string SIG_MAP_TRAP_TABLE =
        "?? ?? 01 00 F0 00 ?? ?? 13 00 F1 00 ?? ?? 33 00 F6 00 ?? ?? 3B 00 F7 00 " + // map 85 Mandalia
        "?? ?? 1C 00 F3 00 ?? ?? 38 00 FC 00 ?? ?? 40 00 F9 00 ?? ?? 57 00 FD 00 " + // map 86
        "?? ?? 63 00 FA 00 ?? ?? 6C 00 FD 00 ?? ?? 7D 00 F0 00 ?? ?? 7E 00 F1 00";   // map 87
    private const int MAP_SIG_ANCHOR_MAPID = 85;
    private const int MAP_ENTRY_SIZE = 0x18;     // 24 bytes per map
    private const int MAP_ITEM_SIZE = 6;         // XY + flags + rare(u16) + common(u16)
    private const int MAP_RARE_OFFSET = 2;       // u16 within an item
    private const int MAP_COMMON_OFFSET = 4;     // u16 within an item
    private nint _mapTableBase;
    private DateTime _lastMapSync = DateTime.MinValue;

    // Per Chapter-1 map: the NG+ targets. rare[i] = upgraded equipment (best non-reserved in the slot's
    // original category); common[i] = post-game consumable. Index 0..3 maps to item tiles 1..4. All 8
    // maps have exactly 4 full treasure tiles, so every slot here is real (no phantom-tile risk). The
    // upgrade table was generated from ItemData.xml (strongest item per category with availability not
    // Unknown20/Blank and id<256) — see docs/battles/010 for the per-battle reward rationale.
    private static readonly Dictionary<int, (ushort[] rare, ushort[] common)> MapTreasureNgPlus = new()
    {
        [85] = (new ushort[]{9,30,56,64},    new ushort[]{242,242,252,252}), // Mandalia: Knife/Sword/Rod/Staff
        [74] = (new ushort[]{82,139,153,168},new ushort[]{252,253,242,242}), // Sweegy: Crossbow/Shield/Helmet/Hat
        [32] = (new ushort[]{184,198,9,30},  new ushort[]{252,252,252,253}), // Dorter: Armor/Clothing/Knife/Sword
        [34] = (new ushort[]{153,168,184,198},new ushort[]{242,242,252,252}),// Sand Rat: Helmet/Hat/Armor/Clothing
        [72] = (new ushort[]{30,50,82,89},   new ushort[]{252,252,252,253}), // Fovoham: Sword/Axe/Crossbow/Bow
        [77] = (new ushort[]{139,153,168,184},new ushort[]{242,242,252,252}),// Lenalian: Shield/Helmet/Hat/Armor
        [91] = (new ushort[]{56,56,64,89},   new ushort[]{252,252,252,253}), // Brigands: Rod/Rod/Staff/Bow
        [49] = (new ushort[]{139,184,198,206},new ushort[]{242,242,252,252}),// Ziekden: Shield/Armor/Clothing/Robe
        // --- Chapter 2 --- baseline = best non-reserved per category; deserving battles add ONE early
        // NON-buyable signature rare (Unknown20 but low-tier, never endgame): Invisibility Cloak 235,
        // Chantage 236, Cursed Ring 222, Septieme Sens 238, Elixir 245. See docs/battles/023.
        [31] = (new ushort[]{89,124,139,153},new ushort[]{242,242,244,252}), // Merchant Dorter: Bow/Throwing/Shield/Helmet
        [80] = (new ushort[]{168,184,198,212},new ushort[]{252,253,242,242}),// Araguay: Hat/Armor/Clothing/Shoes
        [83] = (new ushort[]{235,9,30,56},   new ushort[]{244,252,252,253}), // Zeirchele: SIG Invisibility Cloak + Knife/Sword/Rod
        [35] = (new ushort[]{64,113,139,153},new ushort[]{245,242,244,252}), // Zaland: Staff/Pole/Shield/Helmet + SIG Elixir (common)
        [84] = (new ushort[]{168,184,198,218},new ushort[]{252,253,242,242}),// Balias Tor: Hat/Armor/Clothing/Armguard
        [78] = (new ushort[]{45,45,50,72},   new ushort[]{244,252,252,253}), // Tchigolith: Katana/Katana/Axe/Gun
        [40] = (new ushort[]{82,89,93,97},   new ushort[]{242,242,244,252}), // Goug Lowtown: Crossbow/Bow/Instrument/Book
        [87] = (new ushort[]{103,113,127,236},new ushort[]{252,253,242,242}),// Balias Swale: Polearm/Pole/Bomb + SIG Chantage
        [63] = (new ushort[]{222,139,153,168},new ushort[]{244,252,252,253}),// Golgollada: SIG Cursed Ring + Shield/Helmet/Hat
        [12] = (new ushort[]{184,198,206,212},new ushort[]{245,242,244,252}),// Lionel Gate: Armor/Clothing/Robe/Shoes + SIG Elixir (common)
        [13] = (new ushort[]{219,224,238,45},new ushort[]{242,242,244,252}), // Lionel Oratory: Ring/Armlet + SIG Septieme Sens + Katana
        // --- Chapter 3 --- baseline = best buyable per category; deserving battles add ONE MID-HIGH
        // non-buyable "otimo" highlight (a tier above Ch2's early non-buyables): Ninja Gear 197, Kaiser
        // Shield 141, Septieme Sens 238, Grand Helm 156, Rubber Suit 199, Invisibility Cloak 235. Final-
        // game best (rl90+ weapons, Genji set, Maximillian, best robes/shields, Ribbon) stays Ch4. Boss
        // rares (Reflect Mail, Defender, Defense Ring) live in the ENTD, applied per battle. See docs/036.
        [27] = (new ushort[]{64,69,103,153}, new ushort[]{253,252,242,242}), // Gollund: Staff/Flail/Polearm/Helmet
        [2]  = (new ushort[]{197,224,15,30}, new ushort[]{244,252,253,252}), // Lesalia Postern: SIG Ninja Gear + Armlet/NinjaBlade/Sword
        [58] = (new ushort[]{45,82,89,113},  new ushort[]{242,242,244,252}), // Vaults 2nd: Katana/Crossbow/Bow/Pole
        [59] = (new ushort[]{118,141,139,168},new ushort[]{253,252,242,242}),// Vaults 3rd: Bag + SIG Kaiser Shield + Shield/Hat
        [57] = (new ushort[]{212,218,219,224},new ushort[]{244,252,253,252}),// Vaults 1st: Shoes/Armguard/Ring/Armlet (Wiegraf loot deferred)
        [81] = (new ushort[]{9,15,30,45},    new ushort[]{242,242,244,252}), // Grogh Heights: Knife/NinjaBlade/Sword/Katana
        [25] = (new ushort[]{50,69,72,238},  new ushort[]{253,252,242,242}), // Yardrow: Axe/Flail/Gun + SIG Septieme Sens (Rapha)
        [79] = (new ushort[]{97,103,113,120},new ushort[]{244,252,253,252}), // Yuguewood: Book/Polearm/Pole/Cloth
        [6]  = (new ushort[]{124,139,156,168},new ushort[]{242,242,244,252}),// Riovanes Gate: Throwing/Shield + SIG Grand Helm + Hat
        [7]  = (new ushort[]{184,199,206,212},new ushort[]{242,242,244,252}),// Riovanes Keep: Armor + SIG Rubber Suit + Robe/Shoes
        [5]  = (new ushort[]{224,235,9,15},  new ushort[]{252,253,242,242}), // Riovanes Roof: Armlet + SIG Invisibility Cloak + Knife/NinjaBlade
    };
    // Captured vanilla rare+common per target map (lazy, before our first write) -> restore in normal play.
    private readonly Dictionary<int, (ushort[] rare, ushort[] common)> _mapOrig = new();
    private bool _mapOrigCaptured;

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
        _moduleBase = baseAddr;
        _scanner.AddMainModuleScan(SIG_FILE_READ_REQUEST_OFFSET, result =>
        {
            if (!result.Found) { Log("ERROR: fileReadRequestOffset signature NOT found."); return; }
            nint addr = baseAddr + result.Offset;
            Log($"Hooked fileReadRequestOffset @ 0x{addr:X}");
            _entdReadHook = _hooks!.CreateHook<FileReadRequestOffsetDelegate>(FileReadRequestOffsetImpl, addr).Activate();
        });

        // Locate the live ITEM_COMMON_DATA table for direct ShopAvailability writes (NG+ endgame shops).
        _scanner.AddMainModuleScan(SIG_ITEM_TABLE, result =>
        {
            if (!result.Found) { Log("ERROR: ITEM_COMMON_DATA signature NOT found -> NG+ shops disabled."); return; }
            _itemTableBase = baseAddr + result.Offset;
            Log($"Found ITEM_COMMON_DATA table @ 0x{_itemTableBase:X} -> NG+ endgame shops enabled.");
        });

        // Locate the live MAP_TRAP_FORMATION_DATA table for direct treasure writes (NG+ map rewards).
        _scanner.AddMainModuleScan(SIG_MAP_TRAP_TABLE, result =>
        {
            if (!result.Found) { Log("ERROR: MAP_TRAP_FORMATION_DATA signature NOT found -> NG+ map rewards disabled."); return; }
            _mapTableBase = baseAddr + result.Offset - MAP_SIG_ANCHOR_MAPID * MAP_ENTRY_SIZE;
            Log($"Found MAP_TRAP_FORMATION_DATA table @ 0x{_mapTableBase:X} -> NG+ map rewards enabled.");
        });
    }

    private unsafe int FileReadRequestOffsetImpl(int fileIndex, long sectorOffset, long size, void* outputPointer)
    {
        // Let the original read happen first: it fills outputPointer with the vanilla file bytes and
        // returns whatever status/byte-count the game expects. We only mutate the buffer afterwards.
        int ret = _entdReadHook!.OriginalFunction(fileIndex, sectorOffset, size, outputPointer);

        // Sync shops on world-map/town entry (world_* 765-772) AND on Outfitter open (menu_bk_shop*
        // 741-743). The world_* read fires when you enter a town — BEFORE the Outfitter builds its item
        // list from the table — so the patch/restore lands in time for the shop you're about to open
        // (the shop-UI read alone is too late: the list is already built, so a restore only shows up on
        // the NEXT open). We can use world_* now because detection switched to the stable Ramza-level
        // proxy (the old NG+ static flag bounced during the load transition, which is why world_* was
        // dropped before). The shop-UI read stays as a catch-up for same-screen re-opens.
        if ((fileIndex >= WORLD_INDEX_MIN && fileIndex <= WORLD_INDEX_MAX) ||
            (fileIndex >= SHOP_UI_INDEX_MIN && fileIndex <= SHOP_UI_INDEX_MAX))
        {
            SyncShops();
            SyncMapItems(); // world-map entry lands the treasure patch before the next battle's map loads
        }

        if (fileIndex >= ENTD_INDEX_MIN && fileIndex <= ENTD_INDEX_MAX && outputPointer != null)
        {
            DetectNgPlus();
            SyncMapItems(); // re-assert treasures at battle entry (covers a direct battle load w/o world map)

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
        if (_itemTableBase == 0 || _moduleBase == 0) return;
        if ((DateTime.Now - _lastShopSync).TotalSeconds < 0.5) return; // collapse read bursts only
        _lastShopSync = DateTime.Now;

        // Snapshot the pristine availability once, from the live table BEFORE our first write (so it
        // reflects vanilla + any other mod's edits). Lazy, at first sync, when game data is initialized.
        if (!_origCaptured)
        {
            for (int id = 0; id < ITEM_COUNT; id++)
                _origAvail[id] = SafeReadByte(_itemTableBase + id * ITEM_ENTRY_SIZE + ITEM_SHOPAVAIL_OFFSET);
            _origCaptured = true;
        }

        // NG+ = Ramza's level is abnormally high for the current story progress (per-progress threshold).
        // Decide on the primary copies (RAMZA_LEVEL_RVA + STORY_PROGRESS_RVA); log all copies as
        // diagnostics so a future bug report already carries the data to pick a better rule.
        var dbg = new System.Text.StringBuilder();
        foreach (long rva in RamzaLevelDiagRvas) dbg.Append($" lvl@0x{rva:X}={ReadStaticByte(rva)}");
        foreach (long rva in StoryProgressDiagRvas) dbg.Append($" prog@0x{rva:X}={ReadStaticByte(rva)}");

        int rawLvl = ReadStaticByte(RAMZA_LEVEL_RVA);
        int lvl = rawLvl is >= 1 and <= 99 ? rawLvl : 0;
        int rawProg = ReadStaticByte(STORY_PROGRESS_RVA);
        // Clamp to the valid milestone range. 0 = prologue -> treat as 1 (same low threshold). Garbage
        // (read failure / out of range) -> 16, the highest threshold, so we never wrongly flag NG+.
        int prog = rawProg switch { >= 1 and <= 16 => rawProg, 0 => 1, _ => 16 };
        int threshold = NgThreshold(prog);
        bool ng = lvl >= threshold;

        int changed = WriteShopAvailability(ng); // re-asserted every sync (idempotent: only writes diffs)
        Log($"[nglevel]{dbg} -> lvl={lvl} prog={prog} threshold={threshold} NG+={ng} | shop writes={changed}");
    }

    /// <summary>Write each sold item's ShopAvailability directly into the live ITEM_COMMON_DATA table:
    /// Chapter1_Start (all in stock) in NG+, the captured original otherwise. Returns the number of bytes
    /// actually changed. Direct write bypasses the modloader's ApplyTablePatch change-tracking (which
    /// locked the first value and made a later restore impossible).</summary>
    private int WriteShopAvailability(bool ng)
    {
        int changed = 0;
        for (int id = 0; id < ITEM_COUNT; id++)
        {
            byte orig = _origAvail[id];
            if (orig == AVAIL_BLANK) continue; // never sold -> leave untouched
            byte target = ng ? AVAIL_CHAPTER1_START : orig;
            nint addr = _itemTableBase + id * ITEM_ENTRY_SIZE + ITEM_SHOPAVAIL_OFFSET;
            if (SafeReadByte(addr) != target)
            {
                try { Marshal.WriteByte(addr, target); changed++; } catch { /* ignore */ }
            }
        }
        return changed;
    }

    /// <summary>
    /// Bring the live MAP_TRAP_FORMATION_DATA table to the desired state: upgraded Chapter-1 treasures
    /// in NG+, captured vanilla otherwise. Same shape as SyncShops (throttled, idempotent direct write).
    /// </summary>
    private void SyncMapItems()
    {
        if (_mapTableBase == 0 || _moduleBase == 0) return;
        if ((DateTime.Now - _lastMapSync).TotalSeconds < 0.5) return; // collapse read bursts
        _lastMapSync = DateTime.Now;

        // Snapshot pristine rare+common per target map once, from the live table BEFORE our first write.
        if (!_mapOrigCaptured)
        {
            foreach (int mapId in MapTreasureNgPlus.Keys)
            {
                var rare = new ushort[4];
                var common = new ushort[4];
                for (int i = 0; i < 4; i++)
                {
                    nint itemBase = _mapTableBase + mapId * MAP_ENTRY_SIZE + i * MAP_ITEM_SIZE;
                    rare[i] = SafeReadU16(itemBase + MAP_RARE_OFFSET);
                    common[i] = SafeReadU16(itemBase + MAP_COMMON_OFFSET);
                }
                _mapOrig[mapId] = (rare, common);
            }
            _mapOrigCaptured = true;
        }

        bool ng = ComputeNgPlusProxy(out int lvl, out int prog, out int threshold);
        int changed = WriteMapTreasures(ng);
        Log($"[mapitems] lvl={lvl} prog={prog} threshold={threshold} NG+={ng} | treasure writes={changed}");
    }

    /// <summary>Write each target map's rare+common ids: upgraded in NG+, captured original otherwise.
    /// Returns the number of u16 fields actually changed (idempotent: only writes diffs). Leaves XY and
    /// TrapFlags bytes untouched, so treasure tile positions/traps are preserved.</summary>
    private int WriteMapTreasures(bool ng)
    {
        int changed = 0;
        foreach (var (mapId, target) in MapTreasureNgPlus)
        {
            if (!_mapOrig.TryGetValue(mapId, out var orig)) continue;
            for (int i = 0; i < 4; i++)
            {
                nint itemBase = _mapTableBase + mapId * MAP_ENTRY_SIZE + i * MAP_ITEM_SIZE;
                ushort wantRare = ng ? target.rare[i] : orig.rare[i];
                ushort wantCommon = ng ? target.common[i] : orig.common[i];
                if (SafeReadU16(itemBase + MAP_RARE_OFFSET) != wantRare)
                { try { Marshal.WriteInt16(itemBase + MAP_RARE_OFFSET, (short)wantRare); changed++; } catch { } }
                if (SafeReadU16(itemBase + MAP_COMMON_OFFSET) != wantCommon)
                { try { Marshal.WriteInt16(itemBase + MAP_COMMON_OFFSET, (short)wantCommon); changed++; } catch { } }
            }
        }
        return changed;
    }

    /// <summary>NG+ decision via the level-vs-progress proxy (same rule the shops use; fresh on every
    /// save-load, unlike the autosave flag). NG+ when Ramza's level exceeds the per-progress threshold.</summary>
    private bool ComputeNgPlusProxy(out int lvl, out int prog, out int threshold)
    {
        int rawLvl = ReadStaticByte(RAMZA_LEVEL_RVA);
        lvl = rawLvl is >= 1 and <= 99 ? rawLvl : 0;
        int rawProg = ReadStaticByte(STORY_PROGRESS_RVA);
        prog = rawProg switch { >= 1 and <= 16 => rawProg, 0 => 1, _ => 16 };
        threshold = NgThreshold(prog);
        return lvl >= threshold;
    }

    /// <summary>Read a little-endian u16 from an absolute address, 0 on failure.</summary>
    private static ushort SafeReadU16(nint addr)
    {
        try { return (ushort)Marshal.ReadInt16(addr); }
        catch { return 0; }
    }

    /// <summary>Read one byte from a static module-relative address (the live game-state globals).</summary>
    private int ReadStaticByte(long rva)
    {
        try { return Marshal.ReadByte((nint)((long)_moduleBase + rva)); }
        catch { return -1; }
    }

    /// <summary>NG+ level threshold for a story progress (1..16): FLOOR at progress 1, rising linearly
    /// to TOP at progress 16. NG+ when Ramza's level is >= this.</summary>
    private static int NgThreshold(int progress)
    {
        int p = Math.Clamp(progress, 1, 16);
        return NGPLUS_THRESHOLD_FLOOR + (p - 1) * (NGPLUS_THRESHOLD_TOP - NGPLUS_THRESHOLD_FLOOR) / 15;
    }

    /// <summary>Read one byte from an absolute address, 0 on failure.</summary>
    private static byte SafeReadByte(nint addr)
    {
        try { return Marshal.ReadByte(addr); }
        catch { return 0; }
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
