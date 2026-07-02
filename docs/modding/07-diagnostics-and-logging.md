# Diagnostics and logging

Diagnostics are a temporary investigation tool, not the normal playtest mode. Keep them off by
default, enable only the signal needed for the current question, capture the evidence, then turn the
signal back off before ordinary testing. The file-access logger in particular is intentionally noisy.

## Default state

Use this as the default baseline:

```text
Reloaded-II file-access logging: off
Project battle diagnostic logs: off
Hot event-actor native hooks: off
Mutating runtime experiments: off
```

This keeps Reloaded's console readable and avoids touching fragile native code paths during normal
testing.

## Reloaded-II file-access logging

Use this when the question is: **which game file did the engine actually open at this exact moment?**
It is the reliable way to identify the real `.e` script file driving an event-scripted wave. Do not
trust an NXD join alone for that purpose.

Config file:

```text
C:\Reloaded-II\User\Mods\fftivc.utility.modloader\Config.json
```

Temporary investigative setting:

```json
{
  "LogGeneralFileAccesses": true,
  "GeneralFileAccessType": "AllFiles"
}
```

Then trigger the relevant moment in-game and search the Reloaded log for lines like:

```text
[FFT File Logger] loaded: script/enhanced/event119.e (0x735 bytes)
```

Turn it back off immediately after the file is identified:

```json
{
  "LogGeneralFileAccesses": false,
  "GeneralFileAccessType": "AllFiles"
}
```

Leaving `GeneralFileAccessType` at `AllFiles` is fine; `LogGeneralFileAccesses=false` is the switch
that stops the spam.

## Project battle diagnostic logs

Project-side logging lives in:

```text
src/fftivc.battles.ngplus/Program.cs
```

The master switch is:

```csharp
private static readonly bool ENABLE_BATTLE_DIAGNOSTIC_LOGS = false;
```

Set it to `true` only when investigating battle-load behavior. The master switch gates ordinary
project diagnostics such as battle-id tracing, ENTD trace points, actor-table snapshots around the
Merchant Dorter slot-add work, transition-into-battle logging, and modloader file-registration
checks.

The game trace file is:

```text
D:\SteamLibrary\steamapps\common\FINAL FANTASY TACTICS - The Ivalice Chronicles\ngplus_battletrace.log
```

Reloaded's own logs are under:

```text
%APPDATA%\Reloaded-Mod-Loader-II\Logs\
```

Use project diagnostics for these questions:

| Question | Useful signal |
|---|---|
| Which battle entry/file is being patched? | Battle-id / ENTD trace logs |
| Did the modloader register our override file? | Modded-file registration trace |
| Did an event-spawned unit activate or remain dormant? | Actor-table state (`st`) and activation flag (`aux1b5`) |
| Did choreography run without activation? | Actor-table position fields (`c4f`/`c50`) changed while `st=0xFF` |
| Is a safe once-per-battle native hook firing? | Transition-into-battle trace |
| What are a specific battle's ENTD bytes before/after the guest-scaling pass, and its live actor states? | Targeted battle trace (`DIAG_TRACE_ZEIRCHELE_ENTD` pattern: ENTD slot dump on read + a time-boxed observe-only actor-table probe) |

The targeted-battle trace pattern carries a `variant=` label in every log line; the label is
compiled into the DLL, so after data-only (loose-file) changes the logs keep reporting the label of
the last DLL build, not the current experiment.

After changing `Program.cs`, rebuild and deploy the DLL before expecting the switch to affect the
game. If `FFT_enhanced.exe` is running, Windows will usually lock the deployed DLL under
`C:\Reloaded-II\Mods\fftivc.battles.ngplus\`, so close the game before a normal deploy.

## Dangerous switches stay off

These are intentionally not part of normal diagnostics:

```csharp
private static readonly bool DIAG_TRACE_EVENT_ACTORS = false;
private static readonly bool DIAG_ACTIVATE_MERCHANT_A9_AFTER_A8 = false;
private static readonly bool DIAG_SUSPEND_ZEIRCHELE_EXTRA87_DURING_INTRO = false;
```

`DIAG_TRACE_EVENT_ACTORS` touches the hot event actor/native dispatch neighborhood that has
reproducibly crashed even under observe-only hooks. `DIAG_ACTIVATE_MERCHANT_A9_AFTER_A8` is a
mutating experiment, not a passive log. `DIAG_SUSPEND_ZEIRCHELE_EXTRA87_DURING_INTRO` is a retired
mutating experiment that temporarily deactivated a unit's actor-table state during the battle
intro; it proved irrelevant to its target problem (sprite corruption is sheet-budget pressure, see
[09-sprite-sheet-budget.md](09-sprite-sheet-budget.md)), and suspending an actor before the
formation screen freezes that unit's idle animation during deployment. Do not enable any of these
during routine battle work.

## File-only script overrides

External script overrides, such as:

```text
C:\Reloaded-II\Mods\fftivc.battles.ngplus\FFTIVC\data\enhanced\script\enhanced\event119.e
```

can be copied directly without rebuilding the DLL, because the modloader serves them as files. The
game still has to reload the relevant battle/script before the change is observed. If the script is
already loaded in the current battle instance, return to a state before that battle load and enter it
again.

## What not to infer from logs

Do not treat a registered file override as proof that it is the **right** file for a battle moment. A
wrong script can be registered perfectly and still do nothing in-game. The only reliable proof that a
script matters to a wave is a file-access log showing that script being opened at the wave trigger.

Do not treat a unit's position fields changing as proof that the unit is active. For event-spawned
units, activation is the `st`/`aux1b5` pair in the live battle-actor table; choreography fields can
move even when the unit remains permanently inactive.
