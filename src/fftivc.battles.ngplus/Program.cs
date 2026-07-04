using System;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices;

using Reloaded.Hooks.Definitions;
using Reloaded.Memory.SigScan.ReloadedII.Interfaces;
using Reloaded.Mod.Interfaces;
using Reloaded.Mod.Interfaces.Internal;

using fftivc.utility.modloader.Interfaces;
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
    private unsafe delegate nint EventResolveActorDelegate(int unitId, int* statusOut);
    private delegate int EventGetActorSlotDelegate(int actorIndex);
    private delegate long TransitionIntoBattleDelegate(long a1, long a2, long a3, long a4);
    private IHook<EventResolveActorDelegate>? _eventResolveActorHook;
    private IHook<EventGetActorSlotDelegate>? _eventGetActorSlotHook;
    private IHook<TransitionIntoBattleDelegate>? _transitionIntoBattleHook;

    private const int ENTD_INDEX_MIN = 224;
    private const int ENTD_INDEX_MAX = 227;

    // ENTD file layout: a flat grid of 16 slots/entry x 0x28 bytes, 128 entries -> 0x14000, no header.
    private const long ENTD_FILE_SIZE = 0x14000;
    private const int SLOT_SIZE = 0x28;
    private const int SLOT_CHARID = 0x00; // unit/character id (named chars low; generics 0x80+)
    private const int SLOT_LEVEL = 0x03;  // level (>99 = party level + value-100; 100 = party level)
    private const int SLOT_JOB_UNLOCK = 0x08; // roster job/JP target index; 7 maps to Time Mage, not rank 8
    private const int SLOT_JOB_LEVEL = 0x09;  // level to seed for the job selected by SLOT_JOB_UNLOCK
    private const int SLOT_JOB = 0x0A;    // main job id; ally guests keep job == charId (4/7)
    private const int SLOT_CONTROL_FLAGS = 0x18; // team/control flags; 0x08 makes allied guests controllable
    private const byte LEVEL_PARTY = 100;
    private const byte PLAYER_CONTROL_BIT = 0x08;
    private const byte ENEMY_TEAM_BIT = 0x10;
    private const int PROLOGUE_ORBONNE_ENTRY = 387;
    private const int ZEIRCHELE_FALLS_ENTRY = 405;
    private const int GOLGOLLADA_GALLOWS_ENTRY = 414;

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
    // 0x15=Orran (Chapter 3 — the protected astrologer guest at Gollund; fail-on-death, so he must
    // keep pace with the party. Backline caster, job==charId guard holds: sprite/job both 21).
    // 0x30=Alma (Chapter 3 — guest at Lesalia Postern providing the Aegis buff; scaled so the buff is
    // useful and she survives the wall. job==charId guard holds: sprite/job both 48).
    // 0x19=Rapha (Chapter 3 — the protected NPC guest at Yardow; LOSE-on-death, so she must keep pace
    // with the party or she's one-shot and the fight is unwinnable. job==charId guard holds: sprite/job
    // both 25. 2026-06-27: also re-equipped with best buyable end-game gear in her ENTD slots — Thief's
    // Cap/Luminous Robe/Featherweave Cloak/Eight-fluted Pole — at both Yardow 428 and Riovanes Roof 433).
    // --- Chapter 2 opener guests: Gaffgarion + Agrias join as guests right after Ch1 and were stuck at
    // their vanilla low/default levels. They use SEPARATE charIds for their guest form vs their later
    // boss form, which is exactly what makes this safe:
    // 0x24=Gaffgarion (guest/employer form — the Merchant City of Dorter opener and his early-Ch2 escort
    // appearances; job==charId guard holds: job 0x24). His tuned ENEMY/BOSS fights use DIFFERENT cids
    // (0x05 Zeirchele betrayer, 0x11 Golgollada/Lionel) which are deliberately NOT in this set, so those
    // stay at their designed ~L103 — per the "keep the bosses strong" decision.
    // 0x17 and 0x34 = the two early-Ch2 escort-guest cids (Agrias and Gaffgarion escort forms). BOTH
    // belong in this global set: they are real ally guests at Merchant Dorter (403 s2/s3) and Araguay
    // (404 s7/s8), and 0x34 is the ally guest at Zeirchele (405 s10). At Zeirchele 0x17 carries the
    // enemy-team bit, so the control bit is never applied to it there — no carve-out needed.
    // HISTORY NOTE: 0x34 was briefly removed from this set during the Zeirchele sprite investigation,
    // blamed for a "bugged Agrias-looking unit with wrong portrait". That was a misdiagnosis: the bug
    // was the per-battle sprite-sheet budget (docs/modding/09-sprite-sheet-budget.md) — it persisted
    // with 0x34 removed and was fixed by the ENTD sheet composition with 0x34 still removed. The
    // removal itself broke Agrias's guest control/scaling at 403/404. Do not remove it again.
    // --- Whole-game guest sweep (Ch2-Ch4 stragglers). Derived by scanning every ENTD slot: a cid is
    // SAFE to add iff it has a guest form (named, job==charId, ally) AND NONE of its enemy appearances
    // are real combatants (all at level 254 = disabled cutscene actor). That rule, applied across all 4
    // ENTD files, auto-EXCLUDES every tuned boss (Wiegraf, Elmdor, the 5 Lucavi, Dycedarg, Zalbag,
    // Marach 0x1A, Gaffgarion-boss 0x11, etc.) because bosses always carry real combat levels. Crucially,
    // recruitable characters use SEPARATE cids for their guest vs boss/enemy form, so we scale the guest
    // and leave the boss untouched: Meliadoul guest 0x2A vs boss 0x2F; Reis (human) guest 0x48 vs her
    // dragon boss 0x0F. Safety here does NOT depend on the names being exact — it depends on the verified
    // fact that these cids never appear as a real-level enemy, so scaling them can only help a guest.
    // 0x0C=Ovelia (protected VIP — survives escorts), 0x0D=Orlandeau, 0x16=the Goug ally guest (the
    // doc's "not Mustadio" guest), 0x1F=Beowulf, 0x2A=Meliadoul, 0x32=Cloud, 0x48=Reis.
    private static readonly HashSet<byte> GuestCharIds = new()
    {
        0x04, 0x07, 0x22, 0x1e, 0x15, 0x30, 0x19, 0x24, 0x34, 0x17,
        0x0c, 0x0d, 0x16, 0x1f, 0x2a, 0x32, 0x48,
    };

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
    // Flip this to true when investigating battle-entry ids, event-script slot-adds, or Merchant
    // Dorter actor-table behavior. Keep false for normal playtests; it is intentionally noisy.
    private static readonly bool ENABLE_BATTLE_DIAGNOSTIC_LOGS = false;

    // Diagnostic: log the battle ENTD entry id read from the save.
    private static readonly bool DIAG_LOG_BATTLE_ID = ENABLE_BATTLE_DIAGNOSTIC_LOGS;
    // Diagnostic: trace Merchant Dorter entry 403 after the ENTD read/swap path. This is observe-only
    // and answers whether slot 9 reaches the final buffer the game receives.
    private static readonly bool DIAG_TRACE_MERCHANT_DORTER_ENTD = ENABLE_BATTLE_DIAGNOSTIC_LOGS;
    private static readonly bool DIAG_TRACE_ZEIRCHELE_ENTD = true;
    private const string ZEIRCHELE_DIAG_VARIANT = "guest-control-restore-v1";
    // The intro suspension experiment is retired: the Agrias corruption was sprite-sheet budget
    // (fixed in the ENTD composition — see battle_patch.py zeirchele notes), and suspending the
    // actor before formation froze its idle animation during the deployment screen.
    private static readonly bool DIAG_SUSPEND_ZEIRCHELE_EXTRA87_DURING_INTRO = false;
    private static readonly bool DIAG_TRACE_EVENT_ACTORS = false;
    private static readonly bool DIAG_TRACE_MERCHANT_ACTOR_TABLE = ENABLE_BATTLE_DIAGNOSTIC_LOGS;
    private static readonly bool DIAG_TRACE_TRANSITION_INTO_BATTLE = ENABLE_BATTLE_DIAGNOSTIC_LOGS;
    private static readonly bool DIAG_ACTIVATE_MERCHANT_A9_AFTER_A8 = false;
    private static readonly bool DIAG_TRACE_MODLOADER_FILE_REGISTRATION = ENABLE_BATTLE_DIAGNOSTIC_LOGS;
    private const int MERCHANT_DORTER_ENTRY = 403;
    private const int MERCHANT_DORTER_FILE_INDEX = 227;
    private const long EVENT_RESOLVE_ACTOR_RVA = 0x272684;
    private const long EVENT_GET_ACTOR_SLOT_RVA = 0x273108;
    private const long ACTOR_TABLE_RVA = 0x1853CE0;
    private const int ACTOR_TABLE_ENTRY_SIZE = 0x200;
    private const int ACTOR_TABLE_COUNT = 0x15;
    private const int ACTOR_UNIT_ID_OFFSET = 0x191;
    private const int UNIT_CHAR_ID_OFFSET = 0x00;
    private const int UNIT_JOB_ID_OFFSET = 0x03;
    private const int UNIT_LEVEL_OFFSET = 0x29;
    private const int UNIT_MAX_HP_OFFSET = 0x32;
    private const int UNIT_RAW_PA_OFFSET = 0x38;
    private const int UNIT_EFFECTIVE_PA_OFFSET = 0x3E;
    private const byte GOLGOLLADA_GAFFGARION_CHAR_ID = 0x11;
    private const byte GOLGOLLADA_GAFFGARION_JOB_ID = 17;
    // resume_enwm_main.sav (world-map state of the LOADED game) is the freshest at battle-load time;
    // resume_enbtl_world lags (still the previous battle). Prefer enwm_main.
    private static readonly string[] ResumePreference = { "resume_enwm_main.sav", "resume_enbtl_world.sav" };

    private const string SIG_FILE_READ_REQUEST_OFFSET =
        "48 89 5C 24 ?? 48 89 6C 24 ?? 48 89 74 24 ?? 57 48 83 EC ?? 80 3D ?? ?? ?? ?? ?? 4C 89 CE";
    private const string SIG_TRANSITION_INTO_BATTLE_CALL =
        "E8 ?? ?? ?? ?? 48 8B 0D ?? ?? ?? ?? 48 85 C9 74 ?? E8 ?? ?? ?? ?? 48 8B 0D ?? ?? ?? ?? E8 ?? ?? ?? ?? 84 C0 74";

    private volatile bool _isNgPlus;
    private DateTime _lastMerchantDorterEntdTraceUtc = DateTime.MinValue;
    private long _zeircheleActorTableProbeUntilTicks;
    private long _merchantActorTableProbeUntilTicks;
    private long _golgolladaPaPatchUntilTicks;
    private int _transitionIntoBattleFireCount;
    private int _merchantA9ActivationAttempted;
    private int _zeirchele87Suppressed;
    private int _zeirchele87Restored;
    private int _golgolladaGaffPaPatched;
    private int _golgolladaGaffLastPatchedRawPa = -1;

    // TEST TOGGLE — set true to force the battle ENTD swap (Layer 1) ON for EVERY save, so the NG+
    // battle reworks can be verified on a normal (non-NG+) Chapter-4 save without grinding a full NG+
    // run. Affects ONLY the battle swap (shops/map rewards keep their own level-proxy detection).
    // The [battle-id] diagnostic still logs normally, so endgame entries can be captured either way.
    // MUST be false for any real release.
    // static readonly (not const) on purpose: keeps the compiler from const-folding the `if` branches
    // into "unreachable code" (CS0162) when this is false. Behaviour is identical to a const toggle.
    private static readonly bool DEBUG_FORCE_NGPLUS = false;

    // --- SPOILS-OF-WAR PROBE (DEBUG, observe-only) ---
    // The post-battle "Spoils of War" reward is assembled by engine code: offline RE found NO static
    // (gil,item,item) reward table, and gil has no static xref (it lives at a dynamic-base offset, only
    // stable because the allocation is). So we find WHERE the granted items land and WHICH items they
    // are the GenericChronicle way: a background thread snapshots the persistent game-state region and
    // logs every byte the victory tally changes. The gil global (a known stable address) changing is the
    // event marker, so each capture is a clean before/after DIFF (gil delta + the item-count writes),
    // not frame noise. Pure read + log to spoilsprobe_log.txt next to the exe; never touches gameplay.
    // MUST be false for any release (like DEBUG_FORCE_NGPLUS).
    private static readonly bool DEBUG_SPOILS_PROBE = false;
    private const long PROBE_REGION_RVA = 0xD30000;  // brackets gil(0xD40110) + storyProgress(0xD4021C)
    private const int  PROBE_REGION_LEN = 0x40000;   // 256 KB window of the persistent game-state block
    private const long PROBE_GIL_RVA    = 0xD40110;  // u32 gil; its change is the spoils/gil event marker
    private const int  PROBE_POLL_MS    = 40;
    private const int  PROBE_WINDOW_MS  = 2500;      // keep the event open this long after the last gil tick
    private const int  PROBE_MAX_DIFF   = 8192;      // cap changed-byte records so a noisy region can't flood
    private const int  PROBE_BIG_EVENT  = 1000;      // > this many net changes = save load/shop -> suppress body

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
    // Signature anchors on the first CONCRETE bytes of map 85's entry — item0's rare+common ids
    // (Mandalia, r1/r19/r51/r59). It MUST NOT start with a wildcard: a leading "??" makes Reloaded's
    // sig-scanner skip its fast first-byte search and either scan the whole module byte-by-byte or
    // throw on the scan thread, hanging mod init so the Reloaded launcher times out ("Failed to obtain
    // port") and the game is killed at launch (the exact crash this caused). The two working scans
    // (file-read, item-table) both start concrete; this one now does too. The pattern begins +2 into
    // map 85's entry (skipping the volatile XY+flags byte pair), so tableBase subtracts that offset:
    // tableBase = matchAddr - MAP_SIG_ANCHOR_BYTE_OFFSET - 85*0x18. Interior "??" pairs (later items'
    // XY+flags) are fine — only the LEADING byte must be concrete.
    private const string SIG_MAP_TRAP_TABLE =
        "01 00 F0 00 ?? ?? 13 00 F1 00 ?? ?? 33 00 F6 00 ?? ?? 3B 00 F7 00 " + // map 85 Mandalia (from item0 rare id)
        "?? ?? 1C 00 F3 00 ?? ?? 38 00 FC 00 ?? ?? 40 00 F9 00 ?? ?? 57 00 FD 00 " + // map 86
        "?? ?? 63 00 FA 00 ?? ?? 6C 00 FD 00 ?? ?? 7D 00 F0 00 ?? ?? 7E 00 F1 00";   // map 87
    private const int MAP_SIG_ANCHOR_MAPID = 85;
    private const int MAP_SIG_ANCHOR_BYTE_OFFSET = 2; // pattern starts at item0's rare u16, +2 into the entry
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

    // --- Chapter-4 endgame capstone relics (map Move-Find layer) ---
    // Two Tier-S swords that are otherwise UNOBTAINABLE go on the final maps' hidden treasure tiles.
    // Their bosses can't carry them (Barich is a gunner; Ultima/Lucavi have eq=255), so the reward
    // rides the map layer instead of the ENTD. Map ids cross-verified against FFHacktics/CavesOfNarshe
    // (Mandalia=85 matches our anchor, so TIC's map numbering == the documented FFT numbering).
    // Unlike MapTreasureNgPlus (positional, full 4-slot arrays for maps known to have 4 tiles), these
    // inject the relic into the FIRST REAL tile (first slot whose vanilla rare/common is non-zero) and
    // leave everything else pristine -> no phantom-tile risk even though the tile count is unknown.
    private static readonly Dictionary<int, ushort> MapRelicNgPlus = new()
    {
        [54] = 32, // Lost Sacred Precincts (Lost Halidom, entry 439): Materia Blade
        [55] = 36, // Graveyard of Airships (Ultima, entry 441): Ragnarok
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
        if (DEBUG_FORCE_NGPLUS)
            Log("WARNING: DEBUG_FORCE_NGPLUS=true -> battle swap FORCED ON for ALL saves (TEST BUILD; set false for release).");
        if (_hooks is null) { Log("ERROR: IReloadedHooks unavailable."); return; }
        if (_scanner is null) { Log("ERROR: IStartupScanner unavailable."); return; }

        LoadModdedEntd();
        StartModloaderFileRegistrationTrace();

        _modLoader.GetController<IFFTOItemDataManager>()?.TryGetTarget(out _itemMgr!);
        Log(_itemMgr is null
            ? "WARNING: IFFTOItemDataManager unavailable -> NG+ shops disabled (update the modloader?)."
            : "IFFTOItemDataManager acquired -> NG+ endgame shops enabled.");

        nint baseAddr = Process.GetCurrentProcess().MainModule!.BaseAddress;
        _moduleBase = baseAddr;
        InstallEventActorTraceHooks(baseAddr);
        InstallTransitionIntoBattleTraceHook(baseAddr);
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
            _mapTableBase = baseAddr + result.Offset - MAP_SIG_ANCHOR_BYTE_OFFSET - MAP_SIG_ANCHOR_MAPID * MAP_ENTRY_SIZE;
            Log($"Found MAP_TRAP_FORMATION_DATA table @ 0x{_mapTableBase:X} -> NG+ map rewards enabled.");
        });

        if (DEBUG_SPOILS_PROBE)
        {
            Log("[spoils-probe] DEBUG observe-only memory-diff probe ENABLED -> spoilsprobe_log.txt (set DEBUG_SPOILS_PROBE=false for release).");
            new System.Threading.Thread(SpoilsProbeLoop) { IsBackground = true, Name = "ngplus-spoils-probe" }.Start();
        }
        if (DIAG_TRACE_MERCHANT_ACTOR_TABLE)
        {
            Log("[merchant-actor-table] observe-only memory probe ENABLED -> ngplus_battletrace.log");
            new System.Threading.Thread(MerchantActorTableProbeLoop) { IsBackground = true, Name = "ngplus-merchant-actor-table-probe" }.Start();
        }
        if (DIAG_TRACE_ZEIRCHELE_ENTD)
        {
            Log($"[zeirchele-diag] targeted ENTD + actor-table diagnostics ENABLED variant={ZEIRCHELE_DIAG_VARIANT} -> ngplus_battletrace.log");
            new System.Threading.Thread(ZeircheleActorTableProbeLoop) { IsBackground = true, Name = "ngplus-zeirchele-actor-table-probe" }.Start();
        }
        new System.Threading.Thread(GolgolladaGaffPaPatchLoop) { IsBackground = true, Name = "ngplus-golgollada-gaff-pa-patch" }.Start();

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
            if (DEBUG_FORCE_NGPLUS) _isNgPlus = true; // TEST: force the battle swap on any save
            SyncMapItems(); // re-assert treasures at battle entry (covers a direct battle load w/o world map)

            // Battle entry usually reads the whole ENTD file in one shot, but event/join code can read
            // slices. Delita's pre-Gariland join uses such cached data, so partial reads must receive
            // the same guest scaling or he can still be saved at his vanilla level.
            bool fullRead = sectorOffset == 0 && size == ENTD_FILE_SIZE;
            bool validSlice = IsValidEntdSlice(sectorOffset, size);
            bool haveMod = _moddedEntd.TryGetValue(fileIndex, out byte[]? modded);

            // Layer 1 (NG+ only): swap the modded ENTD bytes for full reads and partial reads.
            if (_isNgPlus && validSlice && haveMod && modded!.Length == ENTD_FILE_SIZE)
            {
                Marshal.Copy(modded!, (int)sectorOffset, (IntPtr)outputPointer, (int)size);
                string kind = fullRead ? "full" : "slice";
                Log($"[swap] ENTD index={fileIndex} off=0x{sectorOffset:X} size=0x{size:X} -> MODDED {kind} [NG+]");
            }
            else
            {
                string why = !_isNgPlus ? "normal play"
                           : !haveMod ? "no modded file"
                           : !validSlice ? $"out-of-range read (off=0x{sectorOffset:X} size=0x{size:X})"
                           : "size mismatch";
                Log($"[pass] ENTD index={fileIndex} size=0x{size:X} -> vanilla enemies ({why})");
            }

            // Layer 2 (ALWAYS except the scripted prologue): scale guests to party level and make allied
            // guest slots controllable. Runs after the swap, so embedded NG++ ENTD and vanilla passthrough
            // both get the same guest policy.
            if (validSlice) TraceZeircheleEntd("before-scale", outputPointer, size, fileIndex, sectorOffset, _isNgPlus, haveMod, fullRead);
            if (validSlice) ScaleGuestsAlways(outputPointer, size, fileIndex, sectorOffset, haveMod ? modded : null);
            if (validSlice) TraceZeircheleEntd("after-scale", outputPointer, size, fileIndex, sectorOffset, _isNgPlus, haveMod, fullRead);
            if (validSlice) TraceMerchantDorterEntd(outputPointer, size, fileIndex, sectorOffset, _isNgPlus, haveMod, fullRead);
            if (_isNgPlus && haveMod && validSlice && SliceCoversEntdEntry(fileIndex, sectorOffset, size, GOLGOLLADA_GALLOWS_ENTRY))
                ArmGolgolladaGaffPaPatch();
        }
        return ret;
    }

    private unsafe void InstallEventActorTraceHooks(nint baseAddr)
    {
        if (!DIAG_TRACE_EVENT_ACTORS) return;
        try
        {
            nint resolveAddr = baseAddr + (nint)EVENT_RESOLVE_ACTOR_RVA;
            nint getSlotAddr = baseAddr + (nint)EVENT_GET_ACTOR_SLOT_RVA;
            _eventResolveActorHook = _hooks!.CreateHook<EventResolveActorDelegate>(EventResolveActorImpl, resolveAddr).Activate();
            _eventGetActorSlotHook = _hooks!.CreateHook<EventGetActorSlotDelegate>(EventGetActorSlotImpl, getSlotAddr).Activate();
            TraceLog($"[event-actor] diagnostic hooks ON resolve=0x{resolveAddr:X} getSlot=0x{getSlotAddr:X} create=OFF");
        }
        catch (Exception ex)
        {
            Log($"ERROR: event actor diagnostic hooks failed: {ex.Message}");
        }
    }

    private void InstallTransitionIntoBattleTraceHook(nint baseAddr)
    {
        if (!DIAG_TRACE_TRANSITION_INTO_BATTLE) return;

        _scanner!.AddMainModuleScan(SIG_TRANSITION_INTO_BATTLE_CALL, result =>
        {
            if (!result.Found)
            {
                Log("ERROR: TransitionIntoBattle call signature NOT found.");
                return;
            }

            try
            {
                nint callSite = baseAddr + result.Offset;
                int rel = Marshal.ReadInt32(callSite + 1);
                nint target = callSite + 5 + rel;
                _transitionIntoBattleHook = _hooks!.CreateHook<TransitionIntoBattleDelegate>(TransitionIntoBattleImpl, target).Activate();
                TraceLog($"[transition] hook ON callSite=0x{callSite:X} target=0x{target:X} rel=0x{rel:X}");
            }
            catch (Exception ex)
            {
                Log($"ERROR: TransitionIntoBattle hook failed: {ex.Message}");
            }
        });
    }

    private long TransitionIntoBattleImpl(long a1, long a2, long a3, long a4)
    {
        long ret = _transitionIntoBattleHook!.OriginalFunction(a1, a2, a3, a4);
        int count = System.Threading.Interlocked.Increment(ref _transitionIntoBattleFireCount);
        TraceLog($"[transition] fired count={count} ret=0x{ret:X} a1=0x{a1:X} a2=0x{a2:X} a3=0x{a3:X} a4=0x{a4:X}");
        return ret;
    }

    private bool ShouldTraceEventActors()
    {
        return DIAG_TRACE_EVENT_ACTORS &&
               (DateTime.UtcNow - _lastMerchantDorterEntdTraceUtc).TotalSeconds <= 120;
    }

    private static bool IsInterestingEventActor(int value) => value >= 0x80 && value <= 0x8F;

    private unsafe nint EventResolveActorImpl(int unitId, int* statusOut)
    {
        nint result = _eventResolveActorHook!.OriginalFunction(unitId, statusOut);
        if (ShouldTraceEventActors() && IsInterestingEventActor(unitId))
        {
            int status = statusOut == null ? int.MinValue : *statusOut;
            TraceLog($"[event-actor] resolve unit=0x{unitId:X2} status={status} ptr=0x{result:X}");
        }
        return result;
    }

    private int EventGetActorSlotImpl(int actorIndex)
    {
        int result = _eventGetActorSlotHook!.OriginalFunction(actorIndex);
        if (ShouldTraceEventActors() && actorIndex >= 0 && actorIndex <= 0x14)
            TraceLog($"[event-actor] get-slot actorIndex={actorIndex} -> {result}");
        return result;
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

    private void StartModloaderFileRegistrationTrace()
    {
        if (!DIAG_TRACE_MODLOADER_FILE_REGISTRATION) return;

        new System.Threading.Thread(() =>
        {
            int[] delaysMs = { 1000, 4000, 9000 };
            int elapsedMs = 0;
            for (int i = 0; i < delaysMs.Length; i++)
            {
                int sleepMs = Math.Max(0, delaysMs[i] - elapsedMs);
                if (sleepMs > 0) System.Threading.Thread.Sleep(sleepMs);
                elapsedMs = delaysMs[i];
                TraceModloaderFileRegistration(i + 1);
            }
        })
        { IsBackground = true, Name = "ngplus-modloader-file-registration-trace" }.Start();
    }

    private void TraceModloaderFileRegistration(int attempt)
    {
        string[] targets = { "script/enhanced/event119.e", "script/enhanced/event298.e" };
        try
        {
            IFFTOModPackManager? packMgr = null;
            var ctrl = _modLoader.GetController<IFFTOModPackManager>();
            if (ctrl is null || !ctrl.TryGetTarget(out packMgr) || packMgr is null)
            {
                TraceLog($"[modloader-files] attempt={attempt} IFFTOModPackManager unavailable");
                return;
            }

            bool baseExists = false;
            string baseExistsNote = "";
            try
            {
                baseExists = targets.All(target => packMgr.FileExists(packMgr.GameMode, target));
            }
            catch (Exception ex)
            {
                baseExistsNote = $" baseExistsError={ex.GetType().Name}:{ex.Message}";
            }

            int totalFiles = 0;
            int scriptFiles = 0;
            var matches = targets.ToDictionary(target => target, _ => new List<string>());
            try
            {
                foreach (var kv in packMgr.ModdedFiles)
                {
                    totalFiles++;
                    var file = kv.Value;
                    string key = kv.Key ?? "";
                    string gamePath = file.GamePath ?? "";
                    string localPath = file.LocalPath ?? "";
                    string owner = file.ModIdOwner ?? "";
                    string mode = Convert.ToString(file.GameMode) ?? "";

                    if (LooksLikeScriptPath(key) || LooksLikeScriptPath(gamePath) || LooksLikeScriptPath(localPath))
                        scriptFiles++;

                    foreach (string target in targets)
                    {
                        if (PathLooksLikeTarget(key, target) || PathLooksLikeTarget(gamePath, target) || PathLooksLikeTarget(localPath, target))
                            matches[target].Add($"key={key} owner={owner} mode={mode} game={gamePath} local={localPath}");
                    }
                }
            }
            catch (Exception ex)
            {
                foreach (string target in targets)
                    matches[target].Add($"moddedFilesError={ex.GetType().Name}:{ex.Message}");
            }

            string matchSummary = string.Join(" ", targets.Select(target => $"{Path.GetFileNameWithoutExtension(target)}Matches={matches[target].Count}"));
            TraceLog($"[modloader-files] attempt={attempt} initialized={packMgr.Initialized} mode={packMgr.GameMode} baseExistsAll={baseExists}{baseExistsNote} total={totalFiles} scripts={scriptFiles} {matchSummary} temp={packMgr.TempFolder} data={packMgr.DataDirectory}");
            foreach (string target in targets)
                foreach (string match in matches[target].Take(8))
                    TraceLog($"[modloader-files] {Path.GetFileNameWithoutExtension(target)} {match}");
        }
        catch (Exception ex)
        {
            TraceLog($"[modloader-files] attempt={attempt} error {ex.GetType().Name}: {ex.Message}");
        }
    }

    private static bool LooksLikeScriptPath(string? path)
    {
        if (string.IsNullOrWhiteSpace(path)) return false;
        string norm = NormalizeModPath(path);
        return norm.Contains("/script/", StringComparison.OrdinalIgnoreCase)
            || norm.StartsWith("script/", StringComparison.OrdinalIgnoreCase);
    }

    private static bool PathLooksLikeTarget(string? path, string target)
    {
        if (string.IsNullOrWhiteSpace(path)) return false;
        string norm = NormalizeModPath(path);
        string fileName = Path.GetFileName(target);
        return norm.Contains(fileName, StringComparison.OrdinalIgnoreCase)
            || norm.Equals(target, StringComparison.OrdinalIgnoreCase)
            || norm.EndsWith("/" + target, StringComparison.OrdinalIgnoreCase);
    }

    private static string NormalizeModPath(string path)
        => path.Replace('\\', '/').TrimStart('/');

    /// <summary>
    /// Force every guest slot (charId in GuestCharIds) to party level (LEVEL_PARTY) and player
    /// control for allied guest slots. The ENTD buffer is a flat grid of 0x28-byte slots, so each
    /// slot-aligned offset's first byte is its charId.
    /// </summary>
    private unsafe void ScaleGuestsAlways(void* buffer, long size, int fileIndex, long sectorOffset, byte[]? reference)
    {
        byte* p = (byte*)buffer;
        int patched = 0;
        long readEnd = sectorOffset + size;
        for (long off = 0; off + SLOT_SIZE <= ENTD_FILE_SIZE; off += SLOT_SIZE)
        {
            if (off >= readEnd || off + SLOT_SIZE <= sectorOffset) continue;

            int globalEntry = ((fileIndex - ENTD_INDEX_MIN) * 128) + (int)(off / (SLOT_SIZE * 16));
            if (globalEntry == PROLOGUE_ORBONNE_ENTRY) continue;

            // Only the genuine ally guest (job == charId). Skips the Ziekden boss (Argath re-jobbed
            // to Knight), so his designed level stands and a normal playthrough's finale isn't broken.
            if (!TryReadEntdByte(p, size, sectorOffset, reference, off + SLOT_CHARID, out byte charId)) continue;
            if (!TryReadEntdByte(p, size, sectorOffset, reference, off + SLOT_JOB, out byte job)) continue;
            TryReadEntdByte(p, size, sectorOffset, reference, off + SLOT_LEVEL, out byte level);
            TryReadEntdByte(p, size, sectorOffset, reference, off + SLOT_CONTROL_FLAGS, out byte flags);

            int slot = (int)((off / SLOT_SIZE) % 16);
            bool isKnownGuest = GuestCharIds.Contains(charId) && job == charId;
            if (DIAG_TRACE_ZEIRCHELE_ENTD && globalEntry == ZEIRCHELE_FALLS_ENTRY &&
                (charId == 0x0C || charId == 0x17 || charId == 0x34))
                TraceLog($"[guest-scaler] CHECK Zeirchele e{globalEntry} s{slot} cid=0x{charId:X2} job=0x{job:X2} lvl=0x{level:X2} flags=0x{flags:X2} known={isKnownGuest}");
            if (!isKnownGuest) continue;

            bool isEnemyTeam = (flags & ENEMY_TEAM_BIT) != 0;

            bool changed = false;
            changed |= PatchEntdByteIfCovered(p, size, sectorOffset, off + SLOT_LEVEL, LEVEL_PARTY);
            if (!isEnemyTeam)
                changed |= OrEntdByteIfCovered(p, size, sectorOffset, off + SLOT_CONTROL_FLAGS, PLAYER_CONTROL_BIT);
            if (changed) patched++;
        }
        if (patched > 0)
            Log($"[guest] scaled/controlled {patched} guest slot(s) in ENTD index={fileIndex} off=0x{sectorOffset:X} size=0x{size:X}");
    }

    private static bool IsValidEntdSlice(long sectorOffset, long size)
        => sectorOffset >= 0 && size > 0 && sectorOffset <= ENTD_FILE_SIZE && size <= ENTD_FILE_SIZE - sectorOffset;

    private static bool SliceCoversEntdEntry(int fileIndex, long sectorOffset, long size, int globalEntry)
    {
        int expectedFileIndex = ENTD_INDEX_MIN + globalEntry / 128;
        if (fileIndex != expectedFileIndex) return false;

        long entryOffset = (globalEntry % 128L) * 16L * SLOT_SIZE;
        long entryEnd = entryOffset + 16L * SLOT_SIZE;
        long readEnd = sectorOffset + size;
        return entryOffset < readEnd && entryEnd > sectorOffset;
    }

    private void ArmGolgolladaGaffPaPatch()
    {
        System.Threading.Interlocked.Exchange(ref _golgolladaGaffPaPatched, 0);
        System.Threading.Volatile.Write(ref _golgolladaPaPatchUntilTicks, DateTime.UtcNow.AddSeconds(90).Ticks);
    }

    private void GolgolladaGaffPaPatchLoop()
    {
        while (true)
        {
            System.Threading.Thread.Sleep(250);
            long untilTicks = System.Threading.Volatile.Read(ref _golgolladaPaPatchUntilTicks);
            if (untilTicks <= DateTime.UtcNow.Ticks) continue;
            if (System.Threading.Volatile.Read(ref _golgolladaGaffPaPatched) != 0) continue;

            try
            {
                if (TryPatchGolgolladaGaffPa())
                    System.Threading.Volatile.Write(ref _golgolladaPaPatchUntilTicks, 0);
            }
            catch (Exception ex)
            {
                Log($"[golgollada-pa] patch error: {ex.Message}");
                System.Threading.Volatile.Write(ref _golgolladaPaPatchUntilTicks, 0);
            }
        }
    }

    private bool TryPatchGolgolladaGaffPa()
    {
        nint table = _moduleBase + (nint)ACTOR_TABLE_RVA;
        int length = ACTOR_TABLE_ENTRY_SIZE * ACTOR_TABLE_COUNT;
        int readable = ReadableExtent(table, length);
        if (readable < length) return false;

        for (int i = 0; i < ACTOR_TABLE_COUNT; i++)
        {
            nint unit = table + i * ACTOR_TABLE_ENTRY_SIZE;
            byte charId = SafeReadByte(unit + UNIT_CHAR_ID_OFFSET);
            byte mirroredId = SafeReadByte(unit + ACTOR_UNIT_ID_OFFSET);
            if (charId != GOLGOLLADA_GAFFGARION_CHAR_ID && mirroredId != GOLGOLLADA_GAFFGARION_CHAR_ID)
                continue;

            byte job = SafeReadByte(unit + UNIT_JOB_ID_OFFSET);
            byte level = SafeReadByte(unit + UNIT_LEVEL_OFFSET);
            if (job != GOLGOLLADA_GAFFGARION_JOB_ID || level is < 1 or > 99)
                continue;

            ushort maxHp = SafeReadU16(unit + UNIT_MAX_HP_OFFSET);
            byte rawPa = SafeReadByte(unit + UNIT_RAW_PA_OFFSET);
            byte effectivePa = SafeReadByte(unit + UNIT_EFFECTIVE_PA_OFFSET);
            if (maxHp < 100 || rawPa == 0 || rawPa > 125 || effectivePa == 0 || effectivePa > 125)
                continue;

            int lastPatchedRaw = System.Threading.Volatile.Read(ref _golgolladaGaffLastPatchedRawPa);
            if (rawPa == lastPatchedRaw)
            {
                System.Threading.Interlocked.Exchange(ref _golgolladaGaffPaPatched, 1);
                return true;
            }

            byte newRawPa = (byte)(rawPa + 2);
            byte newEffectivePa = (byte)(effectivePa + 2);
            Marshal.WriteByte(unit + UNIT_RAW_PA_OFFSET, newRawPa);
            Marshal.WriteByte(unit + UNIT_EFFECTIVE_PA_OFFSET, newEffectivePa);

            System.Threading.Volatile.Write(ref _golgolladaGaffLastPatchedRawPa, newRawPa);
            System.Threading.Interlocked.Exchange(ref _golgolladaGaffPaPatched, 1);
            Log($"[golgollada-pa] patched Gaffgarion a{i} rawPA {rawPa}->{newRawPa} PA {effectivePa}->{newEffectivePa}");
            return true;
        }

        return false;
    }

    private unsafe void TraceMerchantDorterEntd(
        void* buffer,
        long size,
        int fileIndex,
        long sectorOffset,
        bool isNgPlus,
        bool haveMod,
        bool fullRead)
    {
        if (!DIAG_TRACE_MERCHANT_DORTER_ENTD) return;
        if (fileIndex != MERCHANT_DORTER_FILE_INDEX) return;

        long entryOffset = (MERCHANT_DORTER_ENTRY - 384L) * 16L * SLOT_SIZE;
        long entryEnd = entryOffset + 16L * SLOT_SIZE;
        long readEnd = sectorOffset + size;
        if (entryOffset >= readEnd || entryEnd <= sectorOffset) return;

        _lastMerchantDorterEntdTraceUtc = DateTime.UtcNow;
        if (DIAG_TRACE_MERCHANT_ACTOR_TABLE)
            System.Threading.Volatile.Write(ref _merchantActorTableProbeUntilTicks, DateTime.UtcNow.AddSeconds(45).Ticks);
        if (DIAG_ACTIVATE_MERCHANT_A9_AFTER_A8)
            System.Threading.Interlocked.Exchange(ref _merchantA9ActivationAttempted, 0);

        byte* p = (byte*)buffer;
        var sb = new System.Text.StringBuilder();
        sb.Append($"[merchant-entd] file={fileIndex} off=0x{sectorOffset:X} size=0x{size:X} ");
        sb.Append($"full={fullRead} NG+={isNgPlus} haveMod={haveMod} entry={MERCHANT_DORTER_ENTRY}");

        for (int slot = 0; slot <= 9; slot++)
        {
            long slotOffset = entryOffset + slot * SLOT_SIZE;
            if (slotOffset < sectorOffset || slotOffset + SLOT_SIZE > readEnd)
            {
                sb.Append($" | s{slot}=not-covered");
                continue;
            }

            byte cid = p[slotOffset - sectorOffset + SLOT_CHARID];
            byte lvl = p[slotOffset - sectorOffset + SLOT_LEVEL];
            byte jobUnlock = p[slotOffset - sectorOffset + SLOT_JOB_UNLOCK];
            byte jobLevel = p[slotOffset - sectorOffset + SLOT_JOB_LEVEL];
            byte job = p[slotOffset - sectorOffset + SLOT_JOB];
            byte flags = p[slotOffset - sectorOffset + SLOT_CONTROL_FLAGS];
            byte formation = p[slotOffset - sectorOffset + 0x19];
            byte uid = p[slotOffset - sectorOffset + 0x20];

            sb.Append($" | s{slot}:cid=0x{cid:X2} lvl={lvl} ju={jobUnlock} jl={jobLevel} job={job} ");
            sb.Append($"flags=0x{flags:X2} form=0x{formation:X2} uid=0x{uid:X2}");
        }

        TraceLog(sb.ToString());
    }

    private unsafe void TraceZeircheleEntd(
        string stage,
        void* buffer,
        long size,
        int fileIndex,
        long sectorOffset,
        bool isNgPlus,
        bool haveMod,
        bool fullRead)
    {
        if (!DIAG_TRACE_ZEIRCHELE_ENTD) return;
        if (fileIndex != MERCHANT_DORTER_FILE_INDEX) return; // entd4, same file index as Merchant Dorter

        long entryOffset = (ZEIRCHELE_FALLS_ENTRY - 384L) * 16L * SLOT_SIZE;
        long entryEnd = entryOffset + 16L * SLOT_SIZE;
        long readEnd = sectorOffset + size;
        if (entryOffset >= readEnd || entryEnd <= sectorOffset) return;

        if (stage == "before-scale")
        {
            System.Threading.Volatile.Write(ref _zeirchele87Suppressed, 0);
            System.Threading.Volatile.Write(ref _zeirchele87Restored, 0);
        }
        System.Threading.Volatile.Write(ref _zeircheleActorTableProbeUntilTicks, DateTime.UtcNow.AddSeconds(90).Ticks);

        byte* p = (byte*)buffer;
        var sb = new System.Text.StringBuilder();
        sb.Append($"[zeirchele-entd-{stage}] variant={ZEIRCHELE_DIAG_VARIANT} file={fileIndex} off=0x{sectorOffset:X} size=0x{size:X} ");
        sb.Append($"full={fullRead} NG+={isNgPlus} haveMod={haveMod} entry={ZEIRCHELE_FALLS_ENTRY}");

        foreach (int slot in new[] { 0, 1, 7, 8, 9, 10, 11 })
        {
            long slotOffset = entryOffset + slot * SLOT_SIZE;
            if (slotOffset < sectorOffset || slotOffset + SLOT_SIZE > readEnd)
            {
                sb.Append($" | s{slot}=not-covered");
                continue;
            }

            int rel = (int)(slotOffset - sectorOffset);
            byte cid = p[rel + SLOT_CHARID];
            byte name = p[rel + 0x01];
            byte lvl = p[rel + SLOT_LEVEL];
            byte job = p[rel + SLOT_JOB];
            byte flags = p[rel + SLOT_CONTROL_FLAGS];
            byte x = p[rel + 0x19];
            byte y = p[rel + 0x1A];
            byte uid = p[rel + 0x20];
            byte tail35 = p[rel + 0x23];
            byte tail36 = p[rel + 0x24];

            sb.Append($" | s{slot}:cid=0x{cid:X2} name=0x{name:X2} lvl=0x{lvl:X2} job=0x{job:X2} ");
            sb.Append($"flags=0x{flags:X2} pos=({x},{y}) uid=0x{uid:X2} tail23=0x{tail35:X2} tail24=0x{tail36:X2}");
        }

        TraceLog(sb.ToString());
    }

    private static unsafe bool TryReadEntdByte(byte* buffer, long size, long sectorOffset, byte[]? reference, long absoluteOffset, out byte value)
    {
        if (reference is not null && absoluteOffset >= 0 && absoluteOffset < reference.Length)
        {
            value = reference[(int)absoluteOffset];
            return true;
        }

        long rel = absoluteOffset - sectorOffset;
        if (rel >= 0 && rel < size)
        {
            value = buffer[(int)rel];
            return true;
        }

        value = 0;
        return false;
    }

    private static unsafe bool PatchEntdByteIfCovered(byte* buffer, long size, long sectorOffset, long absoluteOffset, byte value)
    {
        long rel = absoluteOffset - sectorOffset;
        if (rel < 0 || rel >= size) return false;

        int index = (int)rel;
        if (buffer[index] == value) return false;

        buffer[index] = value;
        return true;
    }

    private static unsafe bool OrEntdByteIfCovered(byte* buffer, long size, long sectorOffset, long absoluteOffset, byte mask)
    {
        long rel = absoluteOffset - sectorOffset;
        if (rel < 0 || rel >= size) return false;

        int index = (int)rel;
        byte value = (byte)(buffer[index] | mask);
        if (buffer[index] == value) return false;

        buffer[index] = value;
        return true;
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
            foreach (int mapId in MapTreasureNgPlus.Keys.Concat(MapRelicNgPlus.Keys).Distinct())
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

        // Endgame capstone relics: inject ONE Tier-S sword into each final map's first REAL Move-Find
        // tile (first slot with a non-zero vanilla rare/common), preserving its common and all other
        // tiles. In NG+ the slot's rare becomes the relic; otherwise it's restored to the captured value.
        foreach (var (mapId, relic) in MapRelicNgPlus)
        {
            if (!_mapOrig.TryGetValue(mapId, out var orig)) continue;
            int slot = -1;
            for (int i = 0; i < 4; i++)
                if (orig.rare[i] != 0 || orig.common[i] != 0) { slot = i; break; }
            if (slot < 0) continue; // map exposes no real treasure tile -> nothing to ride on
            nint relicBase = _mapTableBase + mapId * MAP_ENTRY_SIZE + slot * MAP_ITEM_SIZE;
            ushort wantRelic = ng ? relic : orig.rare[slot];
            if (SafeReadU16(relicBase + MAP_RARE_OFFSET) != wantRelic)
            { try { Marshal.WriteInt16(relicBase + MAP_RARE_OFFSET, (short)wantRelic); changed++; } catch { } }
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

    private void MerchantActorTableProbeLoop()
    {
        string lastSnapshot = "";
        while (true)
        {
            System.Threading.Thread.Sleep(250);
            long untilTicks = System.Threading.Volatile.Read(ref _merchantActorTableProbeUntilTicks);
            if (untilTicks <= DateTime.UtcNow.Ticks) continue;

            try
            {
                if (DIAG_ACTIVATE_MERCHANT_A9_AFTER_A8)
                    TryActivateMerchantA9AfterA8();

                string snapshot = BuildMerchantActorTableSnapshot();
                if (snapshot.Length > 0 && snapshot != lastSnapshot)
                {
                    TraceLog(snapshot);
                    lastSnapshot = snapshot;
                }
            }
            catch (Exception ex)
            {
                TraceLog($"[merchant-actor-table] probe error: {ex.Message}");
                System.Threading.Volatile.Write(ref _merchantActorTableProbeUntilTicks, 0);
            }
        }
    }

    private void ZeircheleActorTableProbeLoop()
    {
        string lastSnapshot = "";
        while (true)
        {
            System.Threading.Thread.Sleep(250);
            long untilTicks = System.Threading.Volatile.Read(ref _zeircheleActorTableProbeUntilTicks);
            if (untilTicks <= DateTime.UtcNow.Ticks) continue;

            try
            {
                if (DIAG_SUSPEND_ZEIRCHELE_EXTRA87_DURING_INTRO)
                    TrySuspendZeircheleExtraUnitDuringIntro();

                string snapshot = BuildZeircheleActorTableSnapshot();
                if (snapshot.Length > 0 && snapshot != lastSnapshot)
                {
                    TraceLog(snapshot);
                    lastSnapshot = snapshot;
                }
            }
            catch (Exception ex)
            {
                TraceLog($"[zeirchele-actor-table] probe error: {ex.Message}");
                System.Threading.Volatile.Write(ref _zeircheleActorTableProbeUntilTicks, 0);
            }
        }
    }

    private void TryActivateMerchantA9AfterA8()
    {
        if (System.Threading.Volatile.Read(ref _merchantA9ActivationAttempted) != 0) return;

        nint table = _moduleBase + (nint)ACTOR_TABLE_RVA;
        int length = ACTOR_TABLE_ENTRY_SIZE * ACTOR_TABLE_COUNT;
        int readable = ReadableExtent(table, length);
        if (readable < length) return;

        nint a8 = table + 8 * ACTOR_TABLE_ENTRY_SIZE;
        nint a9 = table + 9 * ACTOR_TABLE_ENTRY_SIZE;

        byte a8Uid = SafeReadByte(a8 + ACTOR_UNIT_ID_OFFSET);
        byte a9Uid = SafeReadByte(a9 + ACTOR_UNIT_ID_OFFSET);
        if (a8Uid != 0x85 || a9Uid != 0x86) return;

        byte a8State = SafeReadByte(a8 + 0x01);
        byte a8Aux = SafeReadByte(a8 + 0x1B5);
        byte a9State = SafeReadByte(a9 + 0x01);
        byte a9Aux = SafeReadByte(a9 + 0x1B5);
        if (a8State != 0x08 || a8Aux != 0x01 || a9State != 0xFF || a9Aux != 0x00) return;

        if (System.Threading.Interlocked.CompareExchange(ref _merchantA9ActivationAttempted, 1, 0) != 0) return;

        try
        {
            Marshal.WriteByte(a9 + 0x01, 0x09);
            Marshal.WriteByte(a9 + 0x1B5, 0x01);

            byte postState = SafeReadByte(a9 + 0x01);
            byte postAux = SafeReadByte(a9 + 0x1B5);
            TraceLog($"[merchant-activate-a9] wrote table=0x{table:X} a8=st0x{a8State:X2}/aux0x{a8Aux:X2} a9 0x01:0x{a9State:X2}->0x{postState:X2} 0x1B5:0x{a9Aux:X2}->0x{postAux:X2}");
        }
        catch (Exception ex)
        {
            TraceLog($"[merchant-activate-a9] write failed: {ex.Message}");
        }
    }

    private void TrySuspendZeircheleExtraUnitDuringIntro()
    {
        nint table = _moduleBase + (nint)ACTOR_TABLE_RVA;
        int length = ACTOR_TABLE_ENTRY_SIZE * ACTOR_TABLE_COUNT;
        int readable = ReadableExtent(table, length);
        if (readable < length) return;

        int idx17 = -1, idx34 = -1, idx80 = -1, idx81 = -1, idx87 = -1;
        int active = 0;

        for (int i = 0; i < ACTOR_TABLE_COUNT; i++)
        {
            nint actor = table + i * ACTOR_TABLE_ENTRY_SIZE;
            byte uid = SafeReadByte(actor + ACTOR_UNIT_ID_OFFSET);
            byte state = SafeReadByte(actor + 0x01);
            byte aux = SafeReadByte(actor + 0x1B5);
            if (state != 0xFF && aux == 0x01)
                active++;

            if (uid == 0x17) idx17 = i;
            else if (uid == 0x34) idx34 = i;
            else if (uid == 0x80) idx80 = i;
            else if (uid == 0x81) idx81 = i;
            else if (uid == 0x87) idx87 = i;
        }

        if (idx87 < 0) return;

        nint a87 = table + idx87 * ACTOR_TABLE_ENTRY_SIZE;
        byte wState = SafeReadByte(a87 + 0x01);
        byte wAux = SafeReadByte(a87 + 0x1B5);
        bool wActive = wState != 0xFF && wAux == 0x01;

        bool active17 = IsActorActive(table, idx17);
        bool active34 = IsActorActive(table, idx34);
        bool corpse80Gone = IsActorGone(table, idx80);
        bool corpse81Gone = IsActorGone(table, idx81);

        if (System.Threading.Volatile.Read(ref _zeirchele87Suppressed) == 0 &&
            System.Threading.Volatile.Read(ref _zeirchele87Restored) == 0 &&
            wActive && !active17 && !active34)
        {
            if (System.Threading.Interlocked.CompareExchange(ref _zeirchele87Suppressed, 1, 0) != 0)
                return;

            try
            {
                Marshal.WriteByte(a87 + 0x01, 0xFF);
                Marshal.WriteByte(a87 + 0x1B5, 0x00);
                byte postState = SafeReadByte(a87 + 0x01);
                byte postAux = SafeReadByte(a87 + 0x1B5);
                TraceLog($"[zeirchele-extra87-suspend] variant={ZEIRCHELE_DIAG_VARIANT} table=0x{table:X} a{idx87} active={active} state 0x{wState:X2}->0x{postState:X2} aux 0x{wAux:X2}->0x{postAux:X2} active17={active17} active34={active34}");
            }
            catch (Exception ex)
            {
                TraceLog($"[zeirchele-extra87-suspend] write failed: {ex.Message}");
            }

            return;
        }

        if (System.Threading.Volatile.Read(ref _zeirchele87Suppressed) != 0 &&
            System.Threading.Volatile.Read(ref _zeirchele87Restored) == 0 &&
            !wActive && active17 && corpse80Gone && corpse81Gone)
        {
            if (System.Threading.Interlocked.CompareExchange(ref _zeirchele87Restored, 1, 0) != 0)
                return;

            try
            {
                Marshal.WriteByte(a87 + 0x01, 0x0B);
                Marshal.WriteByte(a87 + 0x1B5, 0x01);
                byte postState = SafeReadByte(a87 + 0x01);
                byte postAux = SafeReadByte(a87 + 0x1B5);
                TraceLog($"[zeirchele-extra87-restore] variant={ZEIRCHELE_DIAG_VARIANT} table=0x{table:X} a{idx87} active={active} state 0x{wState:X2}->0x{postState:X2} aux 0x{wAux:X2}->0x{postAux:X2} active17={active17} active34={active34} corpse80Gone={corpse80Gone} corpse81Gone={corpse81Gone}");
            }
            catch (Exception ex)
            {
                TraceLog($"[zeirchele-extra87-restore] write failed: {ex.Message}");
            }
        }
    }

    private static bool IsActorActive(nint table, int index)
    {
        if (index < 0) return false;
        nint actor = table + index * ACTOR_TABLE_ENTRY_SIZE;
        return SafeReadByte(actor + 0x01) != 0xFF && SafeReadByte(actor + 0x1B5) == 0x01;
    }

    private static bool IsActorGone(nint table, int index)
    {
        if (index < 0) return false;
        nint actor = table + index * ACTOR_TABLE_ENTRY_SIZE;
        return SafeReadByte(actor + 0x01) == 0xFF && SafeReadByte(actor + 0x1B5) == 0x00;
    }

    private string BuildMerchantActorTableSnapshot()
    {
        nint table = _moduleBase + (nint)ACTOR_TABLE_RVA;
        int length = ACTOR_TABLE_ENTRY_SIZE * ACTOR_TABLE_COUNT;
        int readable = ReadableExtent(table, length);
        if (readable < length)
            return $"[merchant-actor-table] unreadable table=0x{table:X} readable=0x{readable:X}/0x{length:X}";

        byte[] data = new byte[length];
        Marshal.Copy(table, data, 0, length);

        var sb = new System.Text.StringBuilder();
        int interesting = 0;
        bool has86 = false;
        bool has87 = false;
        sb.Append($"[merchant-actor-table] table=0x{table:X}");

        for (int i = 0; i < ACTOR_TABLE_COUNT; i++)
        {
            int b = i * ACTOR_TABLE_ENTRY_SIZE;
            byte uid = data[b + ACTOR_UNIT_ID_OFFSET];
            byte state = data[b + 0x01];
            if (uid == 0x86) has86 = true;
            if (uid == 0x87) has87 = true;

            bool nonEmpty = state != 0x00 || uid != 0x00;
            bool focus = uid >= 0x80 && uid <= 0x8F;
            if (!nonEmpty && !focus && i > 10) continue;

            interesting++;
            sb.Append($" | a{i}:uid=0x{uid:X2} st=0x{state:X2}");
            sb.Append($" b0=0x{data[b + 0x00]:X2} f61=0x{data[b + 0x61]:X2} f62=0x{data[b + 0x62]:X2}");
            sb.Append($" c4f=0x{data[b + 0x4F]:X2} c50=0x{data[b + 0x50]:X2} c51=0x{data[b + 0x51]:X2}");
            sb.Append($" p18f=0x{data[b + 0x18F]:X2} p190=0x{data[b + 0x190]:X2}");
            sb.Append($" aux1b5=0x{data[b + 0x1B5]:X2}");
        }

        sb.Append($" | interesting={interesting} has86={has86} has87={has87}");
        return sb.ToString();
    }

    private string BuildZeircheleActorTableSnapshot()
    {
        nint table = _moduleBase + (nint)ACTOR_TABLE_RVA;
        int length = ACTOR_TABLE_ENTRY_SIZE * ACTOR_TABLE_COUNT;
        int readable = ReadableExtent(table, length);
        if (readable < length)
            return $"[zeirchele-actor-table] unreadable table=0x{table:X} readable=0x{readable:X}/0x{length:X}";

        byte[] data = new byte[length];
        Marshal.Copy(table, data, 0, length);

        var sb = new System.Text.StringBuilder();
        int interesting = 0;
        int active = 0;
        bool has17 = false;
        bool active17 = false;
        bool has34 = false;
        bool active34 = false;
        bool has87 = false;
        bool active87 = false;
        sb.Append($"[zeirchele-actor-table] variant={ZEIRCHELE_DIAG_VARIANT} table=0x{table:X}");

        for (int i = 0; i < ACTOR_TABLE_COUNT; i++)
        {
            int b = i * ACTOR_TABLE_ENTRY_SIZE;
            byte uid = data[b + ACTOR_UNIT_ID_OFFSET];
            byte state = data[b + 0x01];
            byte aux = data[b + 0x1B5];
            if (state != 0xFF && aux == 0x01)
                active++;
            if (uid == 0x17)
            {
                has17 = true;
                active17 = state != 0xFF && aux == 0x01;
            }
            if (uid == 0x34)
            {
                has34 = true;
                active34 = state != 0xFF && aux == 0x01;
            }
            if (uid == 0x87)
            {
                has87 = true;
                active87 = state != 0xFF && aux == 0x01;
            }

            bool focus = uid is 0x05 or 0x0C or 0x17 or 0x34 or 0x80 or 0x81 or 0x82 or 0x83 or 0x84 or 0x85 or 0x86 or 0x87;
            bool nonEmpty = state != 0x00 || uid != 0x00;
            if (!focus && !nonEmpty && i > 10) continue;

            interesting++;
            sb.Append($" | a{i}:uid=0x{uid:X2} st=0x{state:X2}");
            sb.Append($" b0=0x{data[b + 0x00]:X2} f61=0x{data[b + 0x61]:X2} f62=0x{data[b + 0x62]:X2}");
            sb.Append($" c4f=0x{data[b + 0x4F]:X2} c50=0x{data[b + 0x50]:X2} c51=0x{data[b + 0x51]:X2}");
            sb.Append($" p18f=0x{data[b + 0x18F]:X2} p190=0x{data[b + 0x190]:X2}");
            sb.Append($" aux1b5=0x{aux:X2}");
        }

        sb.Append($" | active={active} interesting={interesting} has17={has17} active17={active17} has34={has34} active34={active34} has87={has87} active87={active87}");
        return sb.ToString();
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

            // Diagnostic: log the ENTD entry id (u16 @ 0x16C) from EVERY resume file. The enbtl_* files
            // LAG (they show the PREVIOUS battle); resume_enwm_main.sav is the fresh world-map state.
            // Logging all of them lets us pick the current battle's TRUE entry by comparison — needed for
            // template/procedural battles (e.g. Vaults 4th) whose enbtl read is a stale shared value.
            if (DIAG_LOG_BATTLE_ID)
            {
                foreach (var kv in files)
                    if (kv.Key.StartsWith("resume_", StringComparison.OrdinalIgnoreCase)
                        && kv.Value.Length > BATTLE_ENTRY_ID_OFFSET + 1)
                    {
                        int entry = kv.Value[BATTLE_ENTRY_ID_OFFSET] | (kv.Value[BATTLE_ENTRY_ID_OFFSET + 1] << 8);
                        Log($"[battle-id] {kv.Key}: ENTD entry = {entry}");
                    }
                // Hex window around 0x16C of the fresh world-map state — to spot a map/area id when the
                // entry itself is a shared template (the discriminator that picks the OverrideEntryData row).
                if (files.TryGetValue("resume_enwm_main.sav", out var wm) && wm.Length >= 0x180)
                    Log($"[battle-win] enwm_main 0x150-0x17F = {BitConverter.ToString(wm, 0x150, 0x30)}");
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

    private void TraceLog(string msg)
    {
        Log(msg);
        try
        {
            string dir = Path.GetDirectoryName(Process.GetCurrentProcess().MainModule!.FileName!)!;
            File.AppendAllText(Path.Combine(dir, "ngplus_battletrace.log"),
                $"[{DateTime.Now:HH:mm:ss.fff}] [{_modConfig.ModId}] {msg}{Environment.NewLine}");
        }
        catch
        {
            // Reloaded logger already received the line; file logging is best-effort only.
        }
    }

    // ---- SPOILS PROBE IMPLEMENTATION (DEBUG, observe-only) ----

    [DllImport("kernel32.dll")]
    private static extern nuint VirtualQuery(nint lpAddress, out MEMORY_BASIC_INFORMATION lpBuffer, nuint dwLength);

    [StructLayout(LayoutKind.Sequential)]
    private struct MEMORY_BASIC_INFORMATION
    {
        public nint BaseAddress;
        public nint AllocationBase;
        public uint AllocationProtect;
        public ushort PartitionId;
        public nuint RegionSize;
        public uint State;
        public uint Protect;
        public uint Type;
    }

    /// <summary>Committed+readable byte count starting at <paramref name="start"/>, capped at <paramref name="max"/>.</summary>
    private static int ReadableExtent(nint start, int max)
    {
        const uint MEM_COMMIT = 0x1000, PAGE_NOACCESS = 0x01, PAGE_GUARD = 0x100;
        int ok = 0;
        while (ok < max)
        {
            if (VirtualQuery(start + ok, out var mbi, (nuint)Marshal.SizeOf<MEMORY_BASIC_INFORMATION>()) == 0) break;
            if (mbi.State != MEM_COMMIT || (mbi.Protect & PAGE_NOACCESS) != 0 || (mbi.Protect & PAGE_GUARD) != 0) break;
            long regionEnd = (long)mbi.BaseAddress + (long)(ulong)mbi.RegionSize;
            int span = (int)Math.Min(regionEnd - (long)(start + ok), (long)(max - ok));
            if (span <= 0) break;
            ok += span;
        }
        return ok;
    }

    /// <summary>
    /// Observe-only probe: snapshot the persistent game-state region every PROBE_POLL_MS and, whenever the
    /// gil global changes (the spoils/gil tally), log the net before/after DIFF so we can see which inventory
    /// bytes the reward wrote. Reads and logs only; never mutates game memory.
    /// </summary>
    private void SpoilsProbeLoop()
    {
        try
        {
            string dir = Path.GetDirectoryName(Process.GetCurrentProcess().MainModule!.FileName!)!;
            string logPath = Path.Combine(dir, "spoilsprobe_log.txt");
            using var sw = new StreamWriter(logPath, append: false) { AutoFlush = true };
            void P(string s) => sw.WriteLine($"[{DateTime.Now:HH:mm:ss.fff}] {s}");

            nint regionAddr = _moduleBase + (nint)PROBE_REGION_RVA;
            int len = ReadableExtent(regionAddr, PROBE_REGION_LEN);
            int gilOff = (int)(PROBE_GIL_RVA - PROBE_REGION_RVA);
            P($"[SPOILS-PROBE] region=module+0x{PROBE_REGION_RVA:X} readableLen=0x{len:X} gilOff=0x{gilOff:X} poll={PROBE_POLL_MS}ms window={PROBE_WINDOW_MS}ms");
            if (len < gilOff + 4) { P("[SPOILS-PROBE] gil offset is outside the readable region; widen PROBE_REGION_*. Abort."); return; }

            byte[] prev = new byte[len], cur = new byte[len], baseline = new byte[len];
            Marshal.Copy(regionAddr, prev, 0, len);
            Array.Copy(prev, baseline, len);
            uint ReadGil(byte[] buf) => BitConverter.ToUInt32(buf, gilOff);
            uint gilPrev = ReadGil(prev);
            P($"[SPOILS-PROBE] initial gil={gilPrev}");

            bool inEvent = false;
            DateTime eventEnd = DateTime.MinValue, lastBeat = DateTime.Now;

            while (true)
            {
                System.Threading.Thread.Sleep(PROBE_POLL_MS);
                try { Marshal.Copy(regionAddr, cur, 0, len); } catch { continue; }
                uint gilNow = ReadGil(cur);
                bool gilChanged = gilNow != gilPrev;

                if (!inEvent)
                {
                    if (gilChanged)
                    {
                        inEvent = true;
                        Array.Copy(prev, baseline, len); // pre-event snapshot (one tick before the change)
                        eventEnd = DateTime.Now.AddMilliseconds(PROBE_WINDOW_MS);
                        P($"[SPOILS-EVENT-START] gilOld={gilPrev} gilNew={gilNow} delta={(long)gilNow - gilPrev}");
                    }
                    else if ((DateTime.Now - lastBeat).TotalSeconds >= 5)
                    {
                        lastBeat = DateTime.Now;
                        P($"[SPOILS-HEARTBEAT] gil={gilNow}");
                        Array.Copy(cur, baseline, len); // keep the idle baseline fresh
                    }
                }
                else
                {
                    if (gilChanged) eventEnd = DateTime.Now.AddMilliseconds(PROBE_WINDOW_MS);
                    if (DateTime.Now >= eventEnd)
                    {
                        P($"[SPOILS-EVENT-END] gilBaseline={ReadGil(baseline)} gilFinal={gilNow} gilDelta={(long)gilNow - ReadGil(baseline)}");
                        LogDiff(P, baseline, cur, len);
                        inEvent = false;
                        lastBeat = DateTime.Now;
                    }
                }

                (prev, cur) = (cur, prev); // swap; prev now holds this tick's snapshot
                gilPrev = gilNow;
            }
        }
        catch (Exception ex)
        {
            try { _logger.WriteLine($"[spoils-probe] error: {ex.Message}"); } catch { }
        }
    }

    /// <summary>Log every byte that differs between two region snapshots (the net change across an event).
    /// A single battle reward changes only a handful of bytes; a save-load or shop spree changes thousands,
    /// so suppress the body of mass-change events to keep the real reward event readable.</summary>
    private static void LogDiff(Action<string> P, byte[] a, byte[] b, int len)
    {
        int total = 0;
        for (int i = 0; i < len; i++) if (a[i] != b[i]) total++;
        if (total == 0) { P("[SPOILS-SUMMARY] no net change"); return; }
        if (total > PROBE_BIG_EVENT)
        {
            P($"[SPOILS-SUMMARY-BIG changed={total}] likely a save load or shop spree -> body suppressed (not a single battle reward)");
            return;
        }
        var sb = new System.Text.StringBuilder();
        int n = 0;
        for (int i = 0; i < len; i++)
        {
            if (a[i] == b[i]) continue;
            long rva = PROBE_REGION_RVA + i;
            sb.Append($" +0x{i:X}(rva0x{rva:X}):{a[i]:X2}->{b[i]:X2}");
            if (++n >= PROBE_MAX_DIFF) { sb.Append(" ...TRUNCATED"); break; }
        }
        P($"[SPOILS-SUMMARY changed={n}]{sb}");
    }

    public void Suspend() { }
    public void Resume() { }
    public void Unload() { }
    public bool CanUnload() => false;
    public bool CanSuspend() => false;
    public Action Disposing => () => { };
}
