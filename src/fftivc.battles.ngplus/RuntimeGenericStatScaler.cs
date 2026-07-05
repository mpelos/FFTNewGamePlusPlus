using System.Runtime.InteropServices;

namespace fftivc.battles.ngplus;

public partial class Program
{
    private const int FIRST_CHAPTER3_ENTRY = 417;
    private const byte GENDER_MALE_BIT = 0x80;
    private const byte GENDER_FEMALE_BIT = 0x40;
    private const byte GENDER_MONSTER_BIT = 0x20;
    private const byte FOE_TEAM_BIT = 0x10;
    private const int STAT_FIXED_POINT_SCALE = 100_000;
    private static readonly bool DIAG_TRACE_GENERIC_RUNTIME_STATS = false;

    private readonly object _genericRuntimeStatPatchLock = new();
    private readonly HashSet<int> _genericRuntimeStatPatchedKeys = new();
    private long _genericRuntimeStatPatchUntilTicks;
    private int _genericRuntimeStatActiveEntry = -1;

    // Chapter 3+ human runtime stat targets.
    //
    // Add entries here as battle docs are implemented. Use the ENTD global entry and the runtime
    // UnitID (+0x191), not an actor-table index. Generic enemies use enemy-side + job 74-93 guards.
    // Active allied guests use expected char/job + allied-side guards and the same live growth bytes.
    //
    // [426] = Targets(
    //     EnemyUnit(0x80, "frontline Knight"),
    //     GuestUnit(0x15, 0x15, 0x15, "Orran"));
    private static readonly Dictionary<int, RuntimeGenericStatTarget[]> GenericRuntimeStatTargetsByEntry = new()
    {
        [417] = Targets(
            GuestUnit(0x15, 0x15, 0x15, "Orran protected guest"),
            EnemyUnit(0x80, "Thief charm left"),
            EnemyUnit(0x81, "Chemist sustain A"),
            EnemyUnit(0x82, "Chemist sustain B"),
            EnemyUnit(0x83, "Thief charm mid"),
            EnemyUnit(0x84, "Thief charm right"),
            EnemyUnit(0x85, "Orator anchor")),
        [420] = Targets(
            GuestUnit(0x30, 0x30, 0x30, "Alma support guest"),
            EnemyUnit(0x80, "Knight wall A"),
            EnemyUnit(0x81, "Knight wall B"),
            EnemyUnit(0x82, "Monk bruiser A"),
            EnemyUnit(0x83, "Knight wall C"),
            EnemyUnit(0x84, "Monk bruiser B")),
        [422] = Targets(
            EnemyUnit(0x80, "Dragoon lead"),
            EnemyUnit(0x81, "Dragoon diver A"),
            EnemyUnit(0x82, "Dragoon diver B"),
            EnemyUnit(0x83, "Chemist sustain"),
            EnemyUnit(0x84, "Time Mage tempo A"),
            EnemyUnit(0x85, "Time Mage tempo B")),
        [423] = Targets(
            EnemyUnit(0x80, "Knight Rend screen"),
            EnemyUnit(0x81, "Knight bodyguard"),
            EnemyUnit(0x82, "Archer shelf cover"),
            EnemyUnit(0x83, "Archer lane cover"),
            EnemyUnit(0x84, "Summoner shelling")),
        [424] = Targets(
            EnemyUnit(0x80, "Knight disarm-lane screen"),
            EnemyUnit(0x81, "Knight gate body"),
            EnemyUnit(0x82, "Archer gate cover"),
            EnemyUnit(0x83, "Black Mage clump punish"),
            EnemyUnit(0x84, "Archer flank cover")),
    };

    private enum RuntimeStatTargetKind
    {
        EnemyGenericHuman,
        AlliedGuest,
    }

    private readonly record struct RuntimeGenericStatTarget(
        byte UnitId,
        RuntimeStatTargetKind Kind,
        byte ExpectedCharId,
        byte ExpectedJobId,
        string Label);

    private static RuntimeGenericStatTarget EnemyUnit(byte unitId, string label)
        => new(unitId, RuntimeStatTargetKind.EnemyGenericHuman, 0, 0, label);

    private static RuntimeGenericStatTarget GuestUnit(byte unitId, byte expectedCharId, byte expectedJobId, string label)
        => new(unitId, RuntimeStatTargetKind.AlliedGuest, expectedCharId, expectedJobId, label);

    private static RuntimeGenericStatTarget[] Targets(params RuntimeGenericStatTarget[] targets) => targets;

    private void CaptureCurrentBattleEntry(Dictionary<string, byte[]> files)
    {
        if (TryReadBattleEntry(files, out int entry))
            System.Threading.Volatile.Write(ref _currentBattleEntry, entry);
    }

    private static bool TryReadBattleEntry(Dictionary<string, byte[]> files, out int entry)
    {
        entry = -1;
        foreach (string name in new[]
                 {
                     "resume_enwm_main.sav",
                     "resume_enbtl_main.sav",
                     "resume_enbtl_attack.sav",
                     "resume_enbtl_fturn.sav",
                     "resume_enbtl_world.sav",
                 })
        {
            if (!files.TryGetValue(name, out byte[]? data) || data.Length <= BATTLE_ENTRY_ID_OFFSET + 1)
                continue;

            int candidate = data[BATTLE_ENTRY_ID_OFFSET] | (data[BATTLE_ENTRY_ID_OFFSET + 1] << 8);
            if (candidate is >= 0 and <= 511)
            {
                entry = candidate;
                return true;
            }
        }

        return false;
    }

    private void ArmGenericRuntimeStatPatchIfNeeded(int fileIndex, long sectorOffset, long size)
    {
        int entry = System.Threading.Volatile.Read(ref _currentBattleEntry);
        if (entry < FIRST_CHAPTER3_ENTRY)
            return;

        if (!GenericRuntimeStatTargetsByEntry.TryGetValue(entry, out RuntimeGenericStatTarget[]? targets) ||
            targets.Length == 0)
            return;

        if (!SliceCoversEntdEntry(fileIndex, sectorOffset, size, entry))
            return;

        lock (_genericRuntimeStatPatchLock)
        {
            if (_genericRuntimeStatActiveEntry != entry)
            {
                _genericRuntimeStatPatchedKeys.Clear();
                _genericRuntimeStatActiveEntry = entry;
            }
        }

        System.Threading.Volatile.Write(ref _genericRuntimeStatPatchUntilTicks, DateTime.UtcNow.AddSeconds(90).Ticks);
        if (DIAG_TRACE_GENERIC_RUNTIME_STATS)
            TraceLog($"[generic-stats] armed entry={entry} targets={targets.Length}");
    }

    private void GenericRuntimeStatPatchLoop()
    {
        while (true)
        {
            System.Threading.Thread.Sleep(250);
            long untilTicks = System.Threading.Volatile.Read(ref _genericRuntimeStatPatchUntilTicks);
            if (untilTicks <= DateTime.UtcNow.Ticks)
                continue;

            int entry = System.Threading.Volatile.Read(ref _genericRuntimeStatActiveEntry);
            if (!GenericRuntimeStatTargetsByEntry.TryGetValue(entry, out RuntimeGenericStatTarget[]? targets) ||
                targets.Length == 0)
            {
                System.Threading.Volatile.Write(ref _genericRuntimeStatPatchUntilTicks, 0);
                continue;
            }

            try
            {
                if (TryPatchGenericRuntimeStats(entry, targets))
                    System.Threading.Volatile.Write(ref _genericRuntimeStatPatchUntilTicks, 0);
            }
            catch (Exception ex)
            {
                if (DIAG_TRACE_GENERIC_RUNTIME_STATS)
                    TraceLog($"[generic-stats] patch error entry={entry}: {ex.Message}");
                System.Threading.Volatile.Write(ref _genericRuntimeStatPatchUntilTicks, 0);
            }
        }
    }

    private bool TryPatchGenericRuntimeStats(int entry, RuntimeGenericStatTarget[] targets)
    {
        nint table = _moduleBase + (nint)ACTOR_TABLE_RVA;
        int length = ACTOR_TABLE_ENTRY_SIZE * ACTOR_TABLE_COUNT;
        int readable = ReadableExtent(table, length);
        if (readable < length)
            return false;

        int complete = 0;
        foreach (RuntimeGenericStatTarget target in targets)
        {
            int key = (entry << 8) | target.UnitId;
            lock (_genericRuntimeStatPatchLock)
            {
                if (_genericRuntimeStatPatchedKeys.Contains(key))
                {
                    complete++;
                    continue;
                }
            }

            if (TryPatchGenericRuntimeStatTarget(table, target, out string? logLine))
            {
                lock (_genericRuntimeStatPatchLock)
                    _genericRuntimeStatPatchedKeys.Add(key);
                complete++;

                if (DIAG_TRACE_GENERIC_RUNTIME_STATS && logLine is not null)
                    TraceLog($"[generic-stats] entry={entry} {logLine}");
            }
        }

        return complete == targets.Length;
    }

    private bool TryPatchGenericRuntimeStatTarget(nint table, RuntimeGenericStatTarget target, out string? logLine)
    {
        logLine = null;

        for (int i = 0; i < ACTOR_TABLE_COUNT; i++)
        {
            nint unit = table + i * ACTOR_TABLE_ENTRY_SIZE;
            byte unitId = SafeReadByte(unit + ACTOR_UNIT_ID_OFFSET);
            if (unitId != target.UnitId)
                continue;

            if (!TryReadGenericRuntimeStatInputs(unit, target, out GenericRuntimeStatInputs inputs))
                return false;

            GenericRuntimeStats stats = CalculateGenericRuntimeStats(inputs);
            WriteGenericRuntimeStats(unit, inputs, stats);

            logLine =
                $"target=0x{target.UnitId:X2}/{target.Kind}/{target.Label} a{i} char=0x{inputs.CharId:X2} job={inputs.JobId} lv={inputs.Level} " +
                $"HP {inputs.CurrentHp}/{inputs.MaxHp}->{stats.CurrentHp}/{stats.MaxHp} " +
                $"MP {inputs.CurrentMp}/{inputs.MaxMp}->{stats.CurrentMp}/{stats.MaxMp} " +
                $"rawPA {inputs.RawPa}->{stats.RawPa} rawMA {inputs.RawMa}->{stats.RawMa} " +
                $"rawSpd {inputs.RawSpeed}->{stats.RawSpeed}";
            return true;
        }

        return false;
    }

    private static bool TryReadGenericRuntimeStatInputs(
        nint unit,
        RuntimeGenericStatTarget target,
        out GenericRuntimeStatInputs inputs)
    {
        inputs = default;

        byte state = SafeReadByte(unit + UNIT_STATE_OFFSET);
        if (state == 0xFF)
            return false;

        byte charId = SafeReadByte(unit + UNIT_CHAR_ID_OFFSET);
        byte jobId = SafeReadByte(unit + UNIT_JOB_ID_OFFSET);
        byte team = SafeReadByte(unit + UNIT_TEAM_OFFSET);
        byte foeFlags = SafeReadByte(unit + UNIT_FOE_FLAGS_OFFSET);
        bool isEnemySide = team != 0 && (foeFlags & FOE_TEAM_BIT) != 0;

        if (target.Kind == RuntimeStatTargetKind.EnemyGenericHuman)
        {
            if (!isEnemySide || jobId is < 74 or > 93)
                return false;
        }
        else
        {
            if (isEnemySide ||
                team == 0 ||
                charId != target.ExpectedCharId ||
                jobId != target.ExpectedJobId)
                return false;
        }

        byte genderFlags = SafeReadByte(unit + UNIT_GENDER_FLAGS_OFFSET);
        if ((genderFlags & GENDER_MONSTER_BIT) != 0)
            return false;

        bool isMale = (genderFlags & GENDER_MALE_BIT) != 0;
        bool isFemale = (genderFlags & GENDER_FEMALE_BIT) != 0;
        if (isMale == isFemale)
            return false;

        byte level = SafeReadByte(unit + UNIT_LEVEL_OFFSET);
        if (level is < 1 or > 99)
            return false;

        ushort currentHp = SafeReadU16(unit + UNIT_CURRENT_HP_OFFSET);
        ushort maxHp = SafeReadU16(unit + UNIT_MAX_HP_OFFSET);
        ushort currentMp = SafeReadU16(unit + UNIT_CURRENT_MP_OFFSET);
        ushort maxMp = SafeReadU16(unit + UNIT_MAX_MP_OFFSET);
        if (maxHp is 0 or > 9999 || currentHp > maxHp || maxMp > 9999 || currentMp > maxMp)
            return false;

        byte hpGrowth = SafeReadByte(unit + UNIT_HP_GROWTH_OFFSET);
        byte hpMultiplier = SafeReadByte(unit + UNIT_HP_MULTIPLIER_OFFSET);
        byte mpGrowth = SafeReadByte(unit + UNIT_MP_GROWTH_OFFSET);
        byte mpMultiplier = SafeReadByte(unit + UNIT_MP_MULTIPLIER_OFFSET);
        byte speedGrowth = SafeReadByte(unit + UNIT_SPEED_GROWTH_OFFSET);
        byte speedMultiplier = SafeReadByte(unit + UNIT_SPEED_MULTIPLIER_OFFSET);
        byte paGrowth = SafeReadByte(unit + UNIT_PA_GROWTH_OFFSET);
        byte paMultiplier = SafeReadByte(unit + UNIT_PA_MULTIPLIER_OFFSET);
        byte maGrowth = SafeReadByte(unit + UNIT_MA_GROWTH_OFFSET);
        byte maMultiplier = SafeReadByte(unit + UNIT_MA_MULTIPLIER_OFFSET);

        if (hpGrowth == 0 || hpMultiplier == 0 ||
            mpGrowth == 0 || mpMultiplier == 0 ||
            speedGrowth == 0 || speedMultiplier == 0 ||
            paGrowth == 0 || paMultiplier == 0 ||
            maGrowth == 0 || maMultiplier == 0)
            return false;

        inputs = new GenericRuntimeStatInputs(
            CharId: charId,
            IsMale: isMale,
            JobId: jobId,
            Level: level,
            CurrentHp: currentHp,
            MaxHp: maxHp,
            CurrentMp: currentMp,
            MaxMp: maxMp,
            RawPa: SafeReadByte(unit + UNIT_RAW_PA_OFFSET),
            RawMa: SafeReadByte(unit + UNIT_RAW_MA_OFFSET),
            RawSpeed: SafeReadByte(unit + UNIT_RAW_SPEED_OFFSET),
            EffectivePa: SafeReadByte(unit + UNIT_EFFECTIVE_PA_OFFSET),
            EffectiveMa: SafeReadByte(unit + UNIT_EFFECTIVE_MA_OFFSET),
            EffectiveSpeed: SafeReadByte(unit + UNIT_EFFECTIVE_SPEED_OFFSET),
            HpGrowth: hpGrowth,
            HpMultiplier: hpMultiplier,
            MpGrowth: mpGrowth,
            MpMultiplier: mpMultiplier,
            SpeedGrowth: speedGrowth,
            SpeedMultiplier: speedMultiplier,
            PaGrowth: paGrowth,
            PaMultiplier: paMultiplier,
            MaGrowth: maGrowth,
            MaMultiplier: maMultiplier);
        return true;
    }

    private static GenericRuntimeStats CalculateGenericRuntimeStats(GenericRuntimeStatInputs inputs)
    {
        GenericLevelOneBases bases = inputs.IsMale
            ? new GenericLevelOneBases(30, 15, 6, 4, 3)
            : new GenericLevelOneBases(28, 16, 6, 3, 4);

        ushort maxHp = CalculateVisibleWordStat(bases.Hp, inputs.HpGrowth, inputs.HpMultiplier, inputs.Level, 1);
        ushort maxMp = CalculateVisibleWordStat(bases.Mp, inputs.MpGrowth, inputs.MpMultiplier, inputs.Level, 0);
        byte rawSpeed = CalculateVisibleByteStat(bases.Speed, inputs.SpeedGrowth, inputs.SpeedMultiplier, inputs.Level, 1);
        byte rawPa = CalculateVisibleByteStat(bases.Pa, inputs.PaGrowth, inputs.PaMultiplier, inputs.Level, 1);
        byte rawMa = CalculateVisibleByteStat(bases.Ma, inputs.MaGrowth, inputs.MaMultiplier, inputs.Level, 1);

        return new GenericRuntimeStats(
            CurrentHp: PreserveCurrentPool(inputs.CurrentHp, inputs.MaxHp, maxHp),
            MaxHp: maxHp,
            CurrentMp: PreserveCurrentPool(inputs.CurrentMp, inputs.MaxMp, maxMp),
            MaxMp: maxMp,
            RawPa: rawPa,
            RawMa: rawMa,
            RawSpeed: rawSpeed,
            EffectivePa: ApplyEffectiveDelta(inputs.RawPa, inputs.EffectivePa, rawPa),
            EffectiveMa: ApplyEffectiveDelta(inputs.RawMa, inputs.EffectiveMa, rawMa),
            EffectiveSpeed: ApplyEffectiveDelta(inputs.RawSpeed, inputs.EffectiveSpeed, rawSpeed));
    }

    private static ushort CalculateVisibleWordStat(int baseValue, int growth, int multiplier, int level, int min)
        => (ushort)CalculateVisibleStat(baseValue, growth, multiplier, level, min, 9999);

    private static byte CalculateVisibleByteStat(int baseValue, int growth, int multiplier, int level, int min)
        => (byte)CalculateVisibleStat(baseValue, growth, multiplier, level, min, 127);

    private static int CalculateVisibleStat(int baseValue, int growth, int multiplier, int level, int min, int max)
    {
        long rawScaled = (long)baseValue * STAT_FIXED_POINT_SCALE;
        for (int currentLevel = 1; currentLevel < level; currentLevel++)
            rawScaled += rawScaled / (growth + currentLevel);

        long value = rawScaled * multiplier / 100 / STAT_FIXED_POINT_SCALE;
        return (int)Math.Clamp(value, min, max);
    }

    private static ushort PreserveCurrentPool(ushort current, ushort oldMax, ushort newMax)
    {
        if (current >= oldMax)
            return newMax;
        return current > newMax ? newMax : current;
    }

    private static byte ApplyEffectiveDelta(byte oldRaw, byte oldEffective, byte newRaw)
    {
        int delta = oldEffective - oldRaw;
        return (byte)Math.Clamp(newRaw + delta, 1, 127);
    }

    private static void WriteGenericRuntimeStats(nint unit, GenericRuntimeStatInputs inputs, GenericRuntimeStats stats)
    {
        if (inputs.MaxHp != stats.MaxHp)
            Marshal.WriteInt16(unit + UNIT_MAX_HP_OFFSET, unchecked((short)stats.MaxHp));
        if (inputs.CurrentHp != stats.CurrentHp)
            Marshal.WriteInt16(unit + UNIT_CURRENT_HP_OFFSET, unchecked((short)stats.CurrentHp));
        if (inputs.MaxMp != stats.MaxMp)
            Marshal.WriteInt16(unit + UNIT_MAX_MP_OFFSET, unchecked((short)stats.MaxMp));
        if (inputs.CurrentMp != stats.CurrentMp)
            Marshal.WriteInt16(unit + UNIT_CURRENT_MP_OFFSET, unchecked((short)stats.CurrentMp));

        Marshal.WriteByte(unit + UNIT_RAW_PA_OFFSET, stats.RawPa);
        Marshal.WriteByte(unit + UNIT_RAW_MA_OFFSET, stats.RawMa);
        Marshal.WriteByte(unit + UNIT_RAW_SPEED_OFFSET, stats.RawSpeed);
        Marshal.WriteByte(unit + UNIT_EFFECTIVE_PA_OFFSET, stats.EffectivePa);
        Marshal.WriteByte(unit + UNIT_EFFECTIVE_MA_OFFSET, stats.EffectiveMa);
        Marshal.WriteByte(unit + UNIT_EFFECTIVE_SPEED_OFFSET, stats.EffectiveSpeed);
    }

    private readonly record struct GenericLevelOneBases(int Hp, int Mp, int Speed, int Pa, int Ma);

    private readonly record struct GenericRuntimeStatInputs(
        byte CharId,
        bool IsMale,
        byte JobId,
        byte Level,
        ushort CurrentHp,
        ushort MaxHp,
        ushort CurrentMp,
        ushort MaxMp,
        byte RawPa,
        byte RawMa,
        byte RawSpeed,
        byte EffectivePa,
        byte EffectiveMa,
        byte EffectiveSpeed,
        byte HpGrowth,
        byte HpMultiplier,
        byte MpGrowth,
        byte MpMultiplier,
        byte SpeedGrowth,
        byte SpeedMultiplier,
        byte PaGrowth,
        byte PaMultiplier,
        byte MaGrowth,
        byte MaMultiplier);

    private readonly record struct GenericRuntimeStats(
        ushort CurrentHp,
        ushort MaxHp,
        ushort CurrentMp,
        ushort MaxMp,
        byte RawPa,
        byte RawMa,
        byte RawSpeed,
        byte EffectivePa,
        byte EffectiveMa,
        byte EffectiveSpeed);
}
