# Scripted transform bosses and runtime level scaling

Some boss battles do not use the visible ENTD boss slot as the final combatant for the whole fight.
The battle script can register, reveal, transform, or replace an actor during the intro or phase
transition. In those cases, setting the static ENTD Level byte to `100 + offset` can be necessary
for documentation and rewards, but it may not be sufficient to scale the unit that actually fights.

Use this document when a battle has a scripted transformation or phase change, such as:

- Lionel Castle Oratory: Cardinal Draclau -> Cuchulainn.
- Riovanes Castle Keep: Wiegraf -> Belias/Velius.
- Limberry Castle Keep: Celia/Lettie -> Ultima Demon forms.
- Eagrose Castle: Dycedarg -> Adrammelech.
- Airship Graveyard: Hashmal/Ultima phase records.

## Core rule

ENTD relative levels and live actor-table levels are different representations:

```text
ENTD Level byte 104       = highest party level + 4
Live actor table +0x29 84 = already-expanded real level 84
```

Do not write `104` into the live actor table. The live table stores the resolved `1..99` battle
level after ENTD expansion. If the target is "highest + 4", compute the party highest level at
runtime and write `min(99, highest + 4)` to actor-table offset `+0x29`.

## When ENTD-only scaling is not enough

ENTD-only scaling works for ordinary static enemies because the combatant is instantiated directly
from that slot. A transform boss can differ in at least one of these ways:

- the script registers a different UnitID than the ENTD slot that looks like the boss;
- the visible pre-transform actor is a template, corpse, cutscene, or reveal actor;
- the final combatant has a different runtime CharId/UnitID or JobId after transformation;
- the transform happens after the normal ENTD relative-level expansion point.

If the status panel shows the transformed boss at its vanilla level while the ENTD slot is already
`104`, treat the battle as a runtime-scaling case.

## Confirmed example: Lionel Castle Oratory, entry 425

Static ENTD facts:

```text
entry 425, slot s9
CharId/SpriteSet 0x3c
UnitID 0x3c
Job 60 (Gigas/Demon)
Level 104
JobLevel 8
Brave/Faith 88/82
Spoils byte 0x1e = item 226 (108 Gems / Japa Mala)
```

Those bytes remain valuable: they document the intended boss band, keep the slot's reward, and
preserve the Lucavi template. However, Oratory's event script also registers a runtime actor id
`0x43`:

```text
tmp/pac0005/script/enhanced/event197.e
0x00B3: 45 43 00 01              AddUnit/registration for uid 0x43
0x045E: 5F 43 00 04 06 00 00     Warp/position record for uid 0x43
```

The fighting Cuchulainn can therefore be observed in the live battle actor table under the transform
identity, not just the static ENTD slot identity. The working runtime patch treats both ids as valid
for this battle:

```text
static ENTD identity:     0x3c
runtime transform id:     0x43
known Lucavi jobs:        60, 67
live level offset:        +0x29
```

The important result: the boss level scaling is applied to the live actor-table entry after battle
load, not by trying to write a second ENTD slot that does not exist.

## Runtime patch pattern

Use this pattern only for a confirmed transform/phase boss whose final actor does not inherit the
static ENTD relative level.

1. Keep the documented ENTD slot at its intended relative level (`104`, `105`, etc.) unless there is
   a specific reason not to. This preserves the data record, reward, Brave/Faith, and tooling checks.
2. Arm a short-lived runtime scan only when the relevant NG+ ENTD entry is read. Do not run a global
   always-on scanner for every battle.
3. Match the live actor by identity and job, not by actor-table index:
   - accepted CharId/UnitID values for that boss or phase;
   - accepted JobId values for the boss form;
   - `state != 0xFF`;
   - plausible HP range (`maxHp` nonzero, current HP not above max).
4. Compute the target level from the current live player party. Use player-side actor-table entries,
   sane HP, and real levels `1..99`; ignore empty entries and enemies.
5. Write only the live level byte (`unit + 0x29`) unless a separate, explicit stat-tuning task has
   been requested and tested.
6. Make the patch idempotent. A second ENTD read or repeated scan must not apply a delta twice.
7. Log only behind a diagnostic flag and turn the flag off for normal testing.

The level-only path is the default. Manual HP or Speed writes are separate balance experiments, not
part of the transform scaling rule. They should not be left on unless the design explicitly calls
for hidden stat tuning and the in-game result has been accepted.

## What to test

Test from a save before the battle load or before the transform trigger. For Oratory, use a save
before entering the Lionel Castle Oratory battle from the Gate chain.

Check these in-game facts:

- the status panel shows the transformed boss at `highest + offset`;
- the boss still has the correct job/skill identity after transformation;
- the boss reward/spoils path still works;
- the phase transition, death/flee/win condition still fires;
- no manual HP/Speed patch remains unless that is intentionally being tested.

An intro trace may see the boss template before the visible transformation. That is not a failure by
itself. The success criterion is the fighting actor's final status once the battle is active.

## Diagnostics

For Cuchulainn, the project has two diagnostic switches in
`src/fftivc.battles.ngplus/Program.cs`:

```csharp
private static readonly bool DIAG_TRACE_CUCHULAINN_RUNTIME = false;
private static readonly bool DIAG_TRACE_CUCHULAINN_DAMAGE = false;
```

`DIAG_TRACE_CUCHULAINN_RUNTIME` logs the actor-table scan and the level write. It is the normal
first diagnostic for this problem.

`DIAG_TRACE_CUCHULAINN_DAMAGE` installs a pre-damage trace hook that can identify attacker/defender
and HP around damage resolution. It is for targeted investigation only. Keep it off during ordinary
playtesting.

## Common mistakes

| Mistake | Why it is wrong |
|---|---|
| Writing `104` into actor-table `+0x29` | `104` is ENTD-relative syntax. The live table needs the expanded real level. |
| Matching only by ENTD slot or actor-table index | Transform scripts can register a different runtime UnitID. |
| Assuming the script-visible intro actor is the final combatant | Transform/reveal battles can show a template before the fighting form exists. |
| Patching HP/Speed as part of "level scaling" | Those are separate live stats. They may hide the real behavior of a high-level boss. |
| Leaving damage hooks on | They are diagnostic native hooks, not normal mod behavior. |
