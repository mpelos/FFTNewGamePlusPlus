# The live battle-actor table

`FFT_enhanced.exe` tracks active battle participants in a fixed-size, fixed-stride array in process
memory, allocated once a battle loads. This table is what the event-script interpreter's actor-resolve
opcode (`0x45`, see [03-event-script-opcodes.md](03-event-script-opcodes.md)) consults when a script
references a unit by ID, and what the engine's turn-order/render/AI systems read to know which slots
hold a live, in-play combatant. It is a different structure from the on-disk ENTD slot format
([01-entd-binary-format.md](01-entd-binary-format.md)) and from the persistent 54-entry save-data
roster array (`UnitData`, stride `0x258`, fields like `Exp`/`JobLevels`/`CombatSet`) — those describe a
unit's static template and campaign-long progression; this table describes a unit's *current,
in-battle* runtime state.

## Location and shape

| Property | Value |
|---|---|
| Base address | `module + 0x1853CE0` (`module` = `FFT_enhanced.exe`'s loaded base address) |
| Entry stride | `0x200` bytes (512 bytes per slot) |
| Entry count | Unresolved exact upper bound — see note below |
| Empty-slot sentinel | State byte (`+0x01`) `== 0xFF` |

The base address and stride are confirmed by two fully independent derivation methods that converge on
the identical address:

1. **Live disassembly of the actor-resolve call chain.** The event interpreter's actor-resolve
   trampoline (`module + 0x272684`) jumps to a function outside the main module that scans this table.
   A live trace of a resolve call (`resolve unit=0x81 status=-2 ptr=0x1418544E0`) lands exactly on
   entry index 4 of this table: `0x1418544E0 - 4*0x200 == 0x141853CE0`, matching the base address
   directly.
2. **Static AOB-pattern resolution against a third-party mod's own reverse engineering.** The
   open-source Reloaded-II mod `dicene/fftivc.unitcontrol` independently locates the same array (its
   own name for it: `BattleUnitsBaseAddress`) via a signature scan anchored to an unrelated function's
   embedded `mov rax, [rip+disp32]` instruction, with no reference to or dependency on this project's
   code. Resolving that mod's AOB pattern against the locally-installed `FFT_enhanced.exe` (static file
   scan, no process attached) produces a single hit whose RIP-relative target is `module + 0x1853CE0` —
   byte-for-byte the same address found by method 1.

Two unrelated methods (one live in-memory disassembly, one independent third-party mod's own shipped,
released reverse-engineering) arriving at the identical base address and stride (`0x200`) is strong
identity confirmation: this is the same array both systems operate on, not a coincidentally similar
structure.

**Entry count discrepancy (unresolved, does not affect field-layout confidence).** Two read methods
disagree on the table's upper bound:

- The live disassembly of the actor-resolve function's loop bound reads `0x15` (21) entries.
- `dicene/fftivc.unitcontrol`'s independent AOB-based read uses a hardcoded loop bound of `23` entries,
  with no in-memory count field backing either number — both are compile-time/disassembly-time
  constants, not values read from a header.

Neither source documents a count field anywhere in or near the table. The discrepancy (21 vs. 23) is
unresolved — it may reflect two different consumers using different sub-ranges of one larger
allocation, or two different fixed caps for different purposes — but it does not cast doubt on the
table's identity, base address, or per-entry field layout, all of which are independently confirmed by
both methods.

## Field layout

All offsets are relative to the start of an entry (`base + index * 0x200`).

| Offset | Name | Type | Confirmed semantics | Notes |
|---|---|---|---|---|
| `+0x00` | SpriteSet | byte | Sprite-set ID. Constant per entry once populated. | Never observed to change after initial population, including across full activation. |
| `+0x01` | State (`st`) | byte | **Occupancy/activation state.** `0xFF` = free/inactive sentinel. When active, equals the entry's own table index (e.g. index 4 → `0x04`, index 8 → `0x08`). | Core activation signal — see "Two-stage activation model" below. |
| `+0x05` | Control flags | byte | Bit `0x8` = player-controllable/human-control flag. Bits `0x30` = team marker (`0x10`/`0x20` distinguish the two enemy-team values). | Documented by `dicene/fftivc.unitcontrol`'s source, not independently re-derived or logged by this project's own probes. Listed here for completeness; treat as externally sourced. |
| `+0x4F`–`+0x51` | `c4f`/`c50`/`c51` | byte ×3 | **Final tile position.** `c4f` = final tile X, `c50` = final tile Y. `c51`'s role is less certain (observed to change independently and later than `c4f`/`c50` in some entries). | See "Two-stage activation model" — these are the confirmed stage-2 fields. Directly correlated with a script-issued position-set opcode operand (worked example below). |
| `+0x61` | Discard flag 1 | byte | Observed always `0x00` across every occupied slot in every snapshot taken, including a slot that never activates. | No variance observed; role not exhaustively tested — zero-variance data is consistent with "doesn't matter for this case" as much as "is a real discard flag that simply was never set." |
| `+0x62` | Discard flag 2 | byte | Same as `+0x61`: observed always `0x00`, no exceptions. | Same caveat as `+0x61`. |
| `+0x18F`–`+0x190` | Pre-populated identity data | byte ×2 | Set once, at or before the entry first becomes observable, and never changes afterward — independent of either activation stage. | Immediately precedes `UnitID` at `+0x191`; this byte range reads as identity/template data copied in from the ENTD source at table-population time, before any activation logic runs. |
| `+0x191` | UnitID | byte | The unit's identifier as referenced by event-script opcodes (e.g. the `XX` operand in `45 XX 00 ZZ`). Matches the source ENTD slot's UID. | Constant for the lifetime of the entry. This is the field the actor-resolve opcode compares against a script's unit-ID operand. |
| `+0x1B5` | Secondary activation flag (`aux1b5`) | byte | Moves together with the state byte: `0x00` when inactive, `0x01` when active. Always observed to flip in the same write as `+0x01`. | Paired with `+0x01` as the confirmed stage-1 activation signal. Distinct from the `+0x1EE` shadow-copy field documented by `dicene/fftivc.unitcontrol` (see below) — the two are not the same field; no evidence ties them together beyond both being "redundant flag copy" style fields in a large struct. |
| `+0x1EE` | Control-flag shadow copy | byte | A second, redundant copy of the `+0x5` control-flag bit, kept in sync with it. | Documented by `dicene/fftivc.unitcontrol`'s source, not independently re-derived or logged by this project's own probes. Listed for completeness; treat as externally sourced, not cross-validated against this project's own field set. |

Fields not in this table (the remainder of each `0x200`-byte entry) have not been probed.

## The two-stage activation model

A unit occupying a table entry with valid, plausible data (SpriteSet, UnitID, pre-populated identity
fields all correctly set) is **not** the same thing as a unit that is fully active and visible in
battle. Becoming a live, rendered, turn-order-participating combatant is a confirmed two-stage process,
and the two stages are driven by separate mechanisms and can occur independently of each other.

### Stage 1 — occupancy/activation flip

The state byte (`+0x01`) transitions from the `0xFF` sentinel to the entry's own table index, and the
secondary flag (`+0x1B5`) transitions from `0x00` to `0x01`, in the same write. This is the signal that
marks a slot as occupied/active from the perspective of the actor-resolve and get-slot routines.

This flip is driven by the event script's own unit-registration opcode family — explicit inclusion of
the unit's ID in the script's `0x45` (`AddUnit`) registration list, inside the `0x49`/`0x4A`
(`AddUnitStart`/`AddUnitEnd`) bracket. A unit whose ID is never named in this registration list never
receives the stage-1 flip, regardless of what other script opcodes reference that same unit ID
elsewhere in the file. (See [03-event-script-opcodes.md](03-event-script-opcodes.md) for the opcode
reference and [04-adding-event-spawned-enemies.md](04-adding-event-spawned-enemies.md) for the full
recipe this drives.)

### Stage 2 — position/visual field write

The position fields (`+0x4F`/`+0x50`, and sometimes `+0x51`) are written separately, by separate script
opcodes (the `0x5f` position-set family, alongside `0x3b`/`0x32`/`0x44`/`0x11` choreography opcodes that
configure movement, color, draw state, and animation). This write is not necessarily simultaneous with
stage 1 — across observed activation sequences, stage 2 for a given unit lands anywhere from roughly 2
to over 12 seconds after that unit's own stage-1 flip, and the exact values written are unit-specific
(no formula relating them to table index or UID has been derived).

### Stage 2 can occur without stage 1 — confirmed, not hypothetical

A unit's position fields can be written by script while the unit remains completely inactive at the
table-state level. This was directly observed: a script choreography block (`0x5f`/`0x3b`/`0x32`/
`0x44`/`0x6f`/`0x11`) targeting a unit's ID executed and successfully wrote that unit's `+0x50` field,
while the same unit's `+0x01`/`+0x1B5` pair remained stuck at the inactive sentinel (`0xFF`/`0x00`) for
the entire battle — because that unit's ID was absent from the script's `0x45` registration list. The
choreography family and the registration list are independent gates; satisfying one does not satisfy
the other.

This rules out treating "the unit's position got set" as evidence of activation, or treating
"choreography opcodes target this unit" as sufficient on its own to bring it into active play. Both
layers — registration (stage 1) and choreography (stage 2) — must be present and correctly targeted for
a unit to become a fully active, visible combatant.

## Worked example

### A fully active unit

Table entry for a unit after both activation stages have completed, table index 9, the unit's own
index value mirrored into the state byte:

```text
a9: uid=0x86  st=0x09  c4f=0x07  c50=0x0A  aux1b5=0x01
```

`st=0x09` matches the entry's own table index (stage 1 complete). `aux1b5=0x01` confirms the paired
secondary flag (stage 1 complete). `c4f=0x07`/`c50=0x0A` are the final tile X/Y (stage 2 complete).

The `c4f`/`c50` = final tile X/Y reading is confirmed by direct correlation with the position-set
opcode that wrote them. The script's position-set instruction for this unit was:

```text
5f 86 00 07 0a 00 00
```

The operand bytes `07 0a` match `c4f=0x07`/`c50=0x0A` exactly. The same correlation was independently
observed for a different unit in the same script family: a position-set instruction
`5f 85 00 05 0a 00 00` (operand `05 0a`) corresponds to that unit's table fields reading
`c4f=0x05`/`c50=0x0A`. Two independent instances of operand-to-field correlation, for two different
units, is the basis for the `c4f`/`c50` = tile X/Y field identification.

### An inactive, pre-populated-but-dormant slot

The same unit's table entry before either activation stage runs, immediately after the table is first
populated from ENTD source data:

```text
a9: uid=0x86  st=0xFF  b0=0x80  f61=0x00  f62=0x00  c4f=0x07  c50=0x00  c51=0x00
    p18f=0x64  p190=0x00  aux1b5=0x00
```

Every field here is plausible, correctly-typed data — `uid`, sprite set (`b0`), and pre-populated
identity bytes (`p18f`/`p190`) all match what an equivalent active enemy slot shows. Only the
activation-stage fields differ: `st` sits at the `0xFF` sentinel instead of the table index, `aux1b5`
sits at `0x00` instead of `0x01`, and `c50`/`c51` sit at their pre-activation baseline (`0x00`) rather
than a script-written tile coordinate. This state — data present and correct, activation fields never
flipped — is what a unit whose ID was never named in the script's `0x45` registration list looks like
for the entire duration of a battle: it does not revert or get cleaned up, it simply never transitions
out of this state. A slot in this state is functionally invisible: not rendered, not part of turn
order, not interactive — despite holding entirely valid identity data.

### Mid-transition: stage 2 without stage 1

An intermediate state, captured for the same unit during an earlier version of its registration that
included full choreography targeting but not list inclusion:

```text
a9: uid=0x86  st=0xFF  aux1b5=0x00  c50=0x0A   (c50 changed from 0x00 baseline; st/aux1b5 unchanged)
```

`c50` moved from its `0x00` baseline to `0x0A`, exactly matching the targeted choreography block's
position-set operand — proving the script's per-unit instructions executed against this entry — while
`st`/`aux1b5` remained at the inactive sentinel the entire time neighboring, correctly-registered units
transitioned to active. This is the direct, in-game-observed confirmation that stage 2 can complete
independently of stage 1.
