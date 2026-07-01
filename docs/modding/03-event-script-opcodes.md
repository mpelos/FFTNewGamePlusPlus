# Event-script (`.e`) opcode reference

## What `.e` files are

`.e` files are the bytecode payload for TIC's in-battle event-script virtual machine — the system
that drives cutscene choreography, scripted enemy/ally wave spawns, camera moves, and dialogue
timing during a battle's intro and mid-battle events. They are packed inside the game's `.pac`
archives at paths like `script/enhanced/event119.e` (the enhanced-version `EnhancedBattleEvent`
script set) and `script/classic/event119.e` (a parallel classic-presentation variant), and can be
overridden per-mod by placing a replacement file at the same relative path under
`FFTIVC/data/enhanced/script/enhanced/`.

A script is a flat, sequential stream of **variable-length opcode records**. There is no
instruction-count header, no jump table, and (so far as this project has been able to determine —
see "Insertion safety" below) no global offset/length field anywhere in a script that encodes
absolute byte positions elsewhere in the same file. The interpreter reads one opcode byte, dispatches
on it, consumes that opcode's own fixed or self-describing operand bytes, and advances to whatever
byte immediately follows — i.e. record boundaries are discovered by sequential per-opcode-length
advancement, not looked up in a table. This means inserting a whole, well-formed record at a record
boundary does not desynchronize anything else in the file; every absolute offset after the insertion
point simply shifts forward by the inserted length, which is expected and harmless because nothing
in the file references those later positions as fixed numbers.

Every uid-taking opcode record follows the same general shape:

```text
<opcode byte> <uid byte> 00 <opcode-specific operand bytes...>
```

`<uid>` is a script-local unit handle, not a raw ENTD `cid` — `event298.e`'s wave enemies use uids
`0x80`-`0x86`, which do not correspond to any ENTD table index. Named story characters use a
different uid range entirely (`0x17`, `0x24`, `0x34` observed) and are handled by the same opcode
families as ordinary wave enemies.

## The unit-registration idiom: `AddUnitStart` / `AddUnit` / `AddUnitEnd`

Adding a unit to a script's active roster and giving that unit its on-screen presentation are two
separate, independently-required mechanisms:

1. **Registration** — a bare `AddUnitStart` (`0x49`) opcode, followed by one `AddUnit` (`0x45`)
   record per uid being introduced, followed by a bare `AddUnitEnd` (`0x4A`) opcode. This bracket is
   what makes a uid an active, targetable battle participant. A uid that never appears in an
   `AddUnit` record inside one of these brackets never activates, regardless of what choreography
   records exist for it elsewhere in the file — its position/animation data can be written and even
   observed changing live, but the unit's activation state stays unset.
2. **Choreography** — a separate family of per-uid records (`WarpUnit`, `SpriteMove`, `ColorUnit`,
   `Draw`, `UnitAnim`, `WaitSpriteMove`, `EVTCHRPalette`, `UnitShadow`, and others below) that
   position the unit on the grid, animate its walk-in, tint/palette it, and time its reveal. These
   records can sit anywhere in the file relative to the registration bracket — in practice they are
   often hundreds of bytes later, in a dedicated choreography region that runs after all
   `AddUnitStart…AddUnitEnd` brackets in the script have already closed.

A single script can contain more than one registration bracket. `event119.e` (pristine, 1845 bytes)
contains two: one early bracket registering `0x80,0x81,0x82,0x83,0x17,0x34`, and a second, later
bracket registering `0x84,0x85`. A uid omitted from every bracket in the file is never registered, no
matter how complete its choreography records are.

## Confirmed opcode table

Confidence categories used below:

- **LIVE-CONFIRMED** — this project directly observed the opcode's effect change real, in-game
  behavior under a controlled test (a live actor-table field changing, a unit's activation state
  flipping, a visible on-screen result), in TIC specifically. This is the strongest category.
- **NAME-CONFIRMED, structure cross-checked** — the opcode's hex value, name, and parameter count
  are cross-referenced against an independent external reference for vanilla PSX-era FFT, *and* this
  project's own raw-byte records from real TIC `.e` files match that reference's declared
  byte-shape exactly (record length, parameter count, parameter widths). High confidence in the name
  and in the byte layout; the specific runtime *semantics* (what the bytes do mechanically inside
  TIC's executable) are inferred from the external reference's documentation of vanilla PSX FFT, not
  independently disassembled or behaviorally tested in TIC itself for every field.
- **NAME-CONFIRMED ONLY** — the opcode's hex value and name are cross-referenced against an external
  reference by hex value (high confidence in the name), but this project has not independently
  verified the byte-shape against enough real TIC records to call it a structural match, and has not
  observed its effect live in TIC.

| Hex | Name | Params | Confirmed byte structure | Confidence / source |
|---|---|---|---|---|
| `0x45` | AddUnit | 1 (`Unit`, 2 bytes) + 1 (`Draw`, 1 byte) | `45 <uid> 00 <draw>`, 4 bytes total. `<draw>` is a 0/1 flag. | LIVE-CONFIRMED. The presence/absence of a unit's `45 <uid> 00 01` record inside an `AddUnitStart…AddUnitEnd` bracket was directly observed to control whether that unit's live actor-table entry reaches the active state (`st` field equal to its own table index, `aux1b5=0x01`) versus staying inert (`st=0xFF`, `aux1b5=0x00`) — see worked example below. Name/param shape independently cross-checked against `Glain/FFTPatcher`'s `EventCommands.xml` (`Unit` + `Draw` parameters) and against `adamrt/heretic`'s `vm_opcode.h` (3 one-byte params). |
| `0x47` | AddGhostUnit | 7 named (`Spritesheet` 2 bytes, `Index` 1, `X` 1, `Y` 1, `Z` 1, `Facing` 1, `Draw` 1) | `47 <spritesheet_lo> <spritesheet_hi> <index> <x> <y> <z> <facing> <draw>`, 9 bytes total. Takes **no `Unit`/roster-table parameter** — it constructs and places a sprite from a spritesheet index and explicit screen/grid coordinates rather than referencing an existing unit handle. | NAME-CONFIRMED, structure cross-checked. Parameter schema sourced from `Glain/FFTPatcher`'s `EntryEdit/EntryData/PSX/EventCommands.xml` (`Add Ghost Unit`, hex `47`), confirmed byte-for-byte identical between that file's vanilla and "Event Instruction Upgrade" variants. Confirmed real usage in this project's own script corpus (`event298.e`, `event300.e`, `event327.e`) — see worked example below. The uids it introduces (`0x64`, `0x65` in `event298.e`) were confirmed, by tracing their later opcode references, to never appear in `AddUnit`, `WarpUnit`, `UnitShadow`, or `MirrorSprite` records anywhere in the same file — i.e. ghost-unit entities are presentation-layer only and structurally separate from the combat-roster registration idiom above. |
| `0x49` | AddUnitStart | 0 | Bare opcode byte, no operand. Opens a registration bracket. | LIVE-CONFIRMED (as part of the bracket idiom — see `0x45` and the worked example below). Name cross-checked against `Glain/FFTPatcher`'s `EventCommands.xml` and `adamrt/heretic`'s `vm_opcode.h` (both list it as a zero-parameter opcode). |
| `0x4A` | AddUnitEnd | 0 | Bare opcode byte, no operand. Closes a registration bracket opened by `0x49`. | LIVE-CONFIRMED (as part of the bracket idiom). Name cross-checked identically to `0x49`. |
| `0x4B` | WaitAddUnitEnd | 0 | Bare opcode byte, no operand. Observed immediately following an `0x4A` in `event298.e`. | NAME-CONFIRMED ONLY. Cross-referenced against `Glain/FFTPatcher`'s `EventCommands.xml` (`Wait Add Unit End`, hex `4B`, zero parameters) and `adamrt/heretic`. Not observed in every registration bracket in this project's corpus (`event119.e`'s two brackets do not have an `0x4B` immediately following their `0x4A`), so its presence appears situational rather than a mandatory part of every bracket. |
| `0x48` | WaitAddUnit | 0 | Bare opcode byte, no operand. Observed immediately following `0x47 AddGhostUnit` records in `event298.e`, and once preceding a registration bracket in `event119.e`. | NAME-CONFIRMED ONLY. Cross-referenced against `Glain/FFTPatcher`'s `EventCommands.xml` (`Wait Add Unit`, hex `48`, zero parameters). |
| `0x3D` | RemoveUnit | 1 (`Unit`, 2 bytes) | `3d <uid> 00`, 3 bytes total. | NAME-CONFIRMED, structure cross-checked. Cross-referenced against `Glain/FFTPatcher`'s `EventCommands.xml` (`Unit` parameter) and `adamrt/heretic`'s `vm_opcode.h` (`PARAMS(1,1), 2`). Observed in real records in `event119.e` (`3d 24 00`, removing a named-character uid before a later registration bracket opens) and `event327.e` (five consecutive `RemoveUnit` records clearing a prior wave before a new one is set up). |
| `0x5F` | WarpUnit | 6 named | `5f <uid> 00 <operand bytes...>`. Confirmed final-tile usage: `5f <uid> 00 <X> <Y> 00 00` sets the unit's destination tile — directly cross-checked against the live actor table, where the unit's `c4f`/`c50` fields took on exactly the `X`/`Y` values given in this record. | LIVE-CONFIRMED for the tile-target meaning of its first two operand bytes. Name cross-checked against `Glain/FFTPatcher` (`WarpUnit`) and `adamrt/heretic` (6 params). The full 6-parameter operand layout beyond the X/Y tile pair has not been individually field-tested. |
| `0x11` | UnitAnim | 5 named | `11 <uid> 00 <pose/anim id> 02 00`, 6 bytes total. The third operand byte is a small enumerated value (observed values `0x58`/`0x59`/`0x5a` across different units), not a continuously-varying coordinate; the trailing `02 00` is constant across every observed record. | NAME-CONFIRMED ONLY for the "pose/anim id" reading of the varying byte. Hex/name cross-referenced against `Glain/FFTPatcher` and `adamrt/heretic` (`UnitAnim`, 5 params) — the small-enumerated, non-monotonic, reused-across-units behavior of the varying byte is consistent with an animation/pose-index parameter, but no individual pose value has been live-tested to confirm which specific pose each numeric id selects. |
| `0x3B` | SpriteMove | 8 named | `3b <uid> 00 <u16 field> <s16 deltaA> <s16 deltaB> 00 01 01 00`, 13 bytes total. `field`, `deltaA`, `deltaB` vary per unit with no derived formula relating them to ENTD spawn position; the trailing `00 01 01 00` is constant across every observed record. Absent for always-present (non-wave-spawned) units. | NAME-CONFIRMED, structure cross-checked. Hex/name/param-count cross-referenced against `Glain/FFTPatcher` and `adamrt/heretic` (`SpriteMove`, 8 params) and independently corroborated by a second source (an FFHacktics wiki search snippet explicitly pairing `{3B}` with `SpriteMove`). The opcode family's purpose (a unit's intro walk-in positioning/timing) is well supported by its shape and by-absence behavior; the individual meaning of `field`/`deltaA`/`deltaB` has not been live-tested field-by-field. |
| `0x32` | ColorUnit | 7 (each 1 byte) | `32 <uid> 00 <5 operand bytes>`, 8 bytes total. Observed examples: `32 85 00 01 00 00 00 00`, `32 85 00 08 00 00 00 02`. | NAME-CONFIRMED, structure cross-checked. Hex/name/param-count cross-referenced against `adamrt/heretic`'s `vm_opcode.h` (`PARAMS(1,1,1,1,1,1,1), 7`) and independently corroborated by a second source (a wiki search snippet grouping `{32}` with other RGB/color-related event instructions). Every occurrence found in `event119.e` (11 of 11) matches the 8-byte total length exactly, with zero exceptions. Individual operand-byte meanings (plausibly R/G/B/duration/flags) have not been live-tested. |
| `0x44` | Draw | 2 (each 1 byte) | `44 <uid> 00`, 3 bytes total. | NAME-CONFIRMED, structure cross-checked. Hex/name/param-count cross-referenced against `Glain/FFTPatcher` (`Draw Unit`, `Unit` parameter) and `adamrt/heretic` (`PARAMS(1,1), 2`). Every occurrence found in `event119.e` (14 of 14) matches the 3-byte total length exactly, with zero exceptions. |
| `0x4E` | UnitShadow | 3 (1 named `Unit` + further params) | `4e <uid> 00 01`, 4 bytes total. The trailing byte is constant `0x01` across every observed record for every uid, including always-present units. | NAME-CONFIRMED ONLY. Hex/name cross-referenced against `adamrt/heretic`'s `vm_opcode.h`. The simplest, least ambiguous family observed in this project's corpus — only the uid byte varies at all. |
| `0x68` | MirrorSprite | 3 (each 1 byte) | `68 <uid> 00 01`, 4 bytes total. Observed only for a minority of units in a given wave (e.g. 2 of 6 in `event298.e`), not for every unit — consistent with a horizontal sprite-flip flag that is only needed for units whose spawn-side/facing requires mirroring a directional sprite, not a property every unit needs a record for. | NAME-CONFIRMED ONLY. Hex/name cross-referenced against `adamrt/heretic`'s `vm_opcode.h`. Not safe to assume every unit needs a record in this family — its selective presence has no derived gating rule. |
| `0x6F` | WaitSpriteMove | 2 (each named) | `6f <uid> 00`, 3 bytes total. Observed immediately following the last `SpriteMove` (`0x3b`) record in a unit's choreography block — consistent with a block-until-animation-finishes synchronization point keyed to a specific uid. | NAME-CONFIRMED, structure cross-checked. Hex/name cross-referenced against `adamrt/heretic`'s `vm_opcode.h` (`PARAMS(1,1), 2`) and `Glain/FFTPatcher`. The terminator/sync-point role is well supported by its consistent file position (always immediately after a `SpriteMove` family's last record) but the precise wait condition has not been live-tested. |
| `0x7F` | EVTCHRPalette | 4 (each 1 byte) | `7f <uid> 00 <b3> <b4>`, 5 bytes total. `b3` is constant `0x01` across every observed record. `b4` is constant `0x03` for ordinary wave enemies and `0x01` for the always-present (non-wave) unit — a palette-variant byte distinguishing reference classes. | NAME-CONFIRMED, structure cross-checked. Hex/name/param-count cross-referenced against `adamrt/heretic`'s `vm_opcode.h` (`PARAMS(1,1,1,1), 4`) and independently corroborated by a second source (a wiki search snippet explicitly pairing `{7F}` with `EVTCHRPalette`). "EVTCHR" is the classic-PSX term for a battle's special pre-rendered cutscene-portrait sprite bank, making a palette-select opcode for it a plausible fit for the wave-enemy-vs-boss palette split observed in the data. |
| `0xF1` | Wait | 1 (`numFrames`, 2 bytes) | `f1 <LL> <HH>`, 3 bytes total. `<LL HH>` is a little-endian 16-bit frame count (at 60 fps) the script pauses for before executing the next instruction. This is a real, standalone, fixed-shape opcode — **not** a length-prefix or sub-block marker; the bytes immediately following an `0xF1` record are simply the next instruction in the sequential stream. | NAME-CONFIRMED, structure cross-checked. Hex/name/param-shape cross-referenced against `adamrt/heretic`'s `vm_opcode.h` (`PARAMS(2), 1`) and independently corroborated by a second source (a wiki page on the same opcode describing it as "pauses the event for a given number of frames before resuming," with documented examples of `60`/`120`/`300` corresponding to 1/2/5 seconds). Every occurrence found in `event119.e` (100 of 101; the one exception lands inside an unrelated, undecoded marker-block record rather than being a real `Wait`) matches the 3-byte total length exactly. |

## Worked example: a full `AddUnitStart…AddUnit…AddUnitEnd` registration bracket

From `event298.e` (pristine, offset `0x14`), registering all 7 of that script's uids in one bracket:

```text
0x14: 49                  AddUnitStart
0x15: 45 80 00 00         AddUnit  uid=0x80  draw=0
0x19: 45 81 00 00         AddUnit  uid=0x81  draw=0
0x1d: 45 82 00 00         AddUnit  uid=0x82  draw=0
0x21: 45 83 00 00         AddUnit  uid=0x83  draw=0
0x25: 45 84 00 00         AddUnit  uid=0x84  draw=0
0x29: 45 85 00 00         AddUnit  uid=0x85  draw=0
0x2d: 45 86 00 01         AddUnit  uid=0x86  draw=1
0x31: 4a                  AddUnitEnd
0x32: 4b                  WaitAddUnitEnd
```

A second example, from `event119.e` (pristine, offset `0x3c9`) — a script can use more than one
bracket; this one registers only two of the script's later-introduced uids:

```text
0x3c9: 49                 AddUnitStart
0x3ca: 45 84 00 01        AddUnit  uid=0x84  draw=1
0x3ce: 45 85 00 01        AddUnit  uid=0x85  draw=1
0x3d2: 4a                 AddUnitEnd
```

`event119.e`'s first, earlier bracket (offset `0x1e9`) registers a different uid set in the same
script:

```text
0x1e9: 49                 AddUnitStart
0x1ea: 45 80 00 01        AddUnit  uid=0x80  draw=1
0x1ee: 45 81 00 01        AddUnit  uid=0x81  draw=1
0x1f2: 45 82 00 01        AddUnit  uid=0x82  draw=1
0x1f6: 45 83 00 01        AddUnit  uid=0x83  draw=1
0x1fa: 45 17 00 01        AddUnit  uid=0x17  draw=1  (named character)
0x1fe: 45 34 00 01        AddUnit  uid=0x34  draw=1  (named character)
0x202: 4a                 AddUnitEnd
```

This pair of `event119.e` brackets is the live-confirmed basis for the `0x45` row's LIVE-CONFIRMED
rating above: a uid choreographed in full (every `WarpUnit`/`SpriteMove`/`ColorUnit`/`Draw`/
`WaitSpriteMove`/`UnitAnim` record present and correct) but **absent** from both of these brackets
was directly observed, via the live actor table, to receive its position update (`c50` field moved
from `0x00` to `0x0A`, matching its `WarpUnit` record's operand) but never flip to the active state
(`st` stayed `0xFF`, `aux1b5` stayed `0x00`). Adding a third `AddUnit` record for that same uid —
`45 86 00 01` — immediately before the second bracket's `4a`, with no other change, was directly
observed to flip that unit to the active state (`st=0x09`, matching its own table index;
`aux1b5=0x01`) in the same live actor-table log, and the unit appeared in-battle as a fully
functional 7th combatant with correct sprite and portrait.

## Worked example: a per-unit choreography sequence

From `event119.e`, the native choreography block for uid `0x85` (the last of that script's five
vanilla wave enemies), confirmed present at the file's wave-choreography region:

```text
5f 85 00 ...              WarpUnit         uid=0x85  (sets final tile; observed c4f/c50 match)
3b 85 00 ...               SpriteMove       uid=0x85
32 85 00 ...               ColorUnit        uid=0x85
44 85 00                   Draw             uid=0x85
3b 85 00 ...               SpriteMove       uid=0x85
32 85 00 ...               ColorUnit        uid=0x85
6f 85 00                   WaitSpriteMove   uid=0x85
11 85 00 ...                UnitAnim         uid=0x85
```

A fully decoded, byte-exact clone of this same family for a newly-registered uid `0x86` (the first
deployed variant, final tile changed from `(5,10)` to `(7,10)`):

```text
5f 86 00 07 0a 00 00                              WarpUnit        uid=0x86  tile=(7,10)
3b 86 00 00 00 00 00 12 00 00 01 01 00            SpriteMove      uid=0x86
32 86 00 01 00 00 00 00                           ColorUnit       uid=0x86
44 86 00                                          Draw            uid=0x86
3b 86 00 00 00 00 00 00 00 00 01 1c 00            SpriteMove      uid=0x86
f1 08 00                                          Wait            8 frames
32 86 00 08 00 00 00 02                           ColorUnit       uid=0x86
6f 86 00                                          WaitSpriteMove  uid=0x86
11 86 00 02 00 00                                 UnitAnim        uid=0x86
```

This exact block (including the `(7,10)` tile) is what the registration-bracket worked example above
validates: that adding the matching `45 86 00 01` record is what flips this uid from inert to active.
The block's non-tile bytes (`SpriteMove`/`ColorUnit`/`Draw`/`WaitSpriteMove`/`UnitAnim`) are
confirmed correct as-is. The `WarpUnit` tile operand is a separate, independently-tunable value —
`(7,10)` itself was subsequently found to be a rooftop tile, invalid for this unit's intended
street-level role, and was revised; see the closing note on spawn placement in
[04-adding-event-spawned-enemies.md](04-adding-event-spawned-enemies.md) for the current tile and why
the choreography/registration validation above is unaffected by that revision.

This block alone — choreography with no corresponding `AddUnit` record in any registration bracket —
was live-tested and confirmed **insufficient** for a working unit (see the registration-bracket
worked example above for the actor-table evidence). Choreography and registration are independent,
both-required layers; neither alone produces an active combatant.

## Insertion safety

Inserting a whole, well-formed record at an existing record boundary (immediately after the last byte
of one record, immediately before the opcode byte of the next) has been checked, and observed, not to
corrupt unrelated parts of a script:

- No `0xF1`-prefixed record anywhere in the checked corpus (`event298.e`, `event119.e`) has an
  operand value that spans or references a position outside its own 3-byte record — `0xF1` is a
  standalone fixed-shape `Wait` opcode (see table above), not a length-prefixed sub-block header, so
  there is no length field at risk of desynchronization from a nearby insertion.
- No global header field in either checked script matches the file's total byte length, or the
  offset of any internal sub-script/marker region, as a 16- or 32-bit value at any position — i.e. no
  evidence of a file-length or absolute-offset field that an insertion would invalidate.
- No sibling script that invokes a given `.e` file by script ID embeds that file's byte length or any
  absolute offset into it; the link between scripts is by script ID through the enhanced-battle-event
  table, not a byte-offset reference.
- A live, in-game test of a two-site, length-changing insertion (a new `AddUnit` record plus an
  entire new choreography block, growing `event119.e` from 1845 to 1913 bytes) produced no crash and
  the correct visual result, which is direct empirical confirmation — not just static analysis — that
  this category of edit is safe for this file format.

## Sourcing and provenance

The opcode names and parameter shapes in this reference are sourced from two independent,
open-source community projects that reverse-engineer or reimplement vanilla 1997 PSX-era Final
Fantasy Tactics' event-script virtual machine — neither project has any connection to TIC (this 2025
remaster) itself:

- **`adamrt/heretic`** (https://github.com/adamrt/heretic) — a from-scratch C reimplementation of
  PSX FFT's event-script VM that reads `EVENT/TEST.EVT` directly out of an unmodified North American
  PSX disc image. Its opcode table (`src/vm_opcode.h`) is the primary source for most hex/name/
  parameter-count pairings in this document. It is a parser/catalog, not a full behavioral
  reimplementation — it does not itself execute most opcodes' game logic, so it can confirm an
  opcode's name and operand byte-widths but not its in-game effect.
- **`Glain/FFTPatcher`** (https://github.com/Glain/FFTPatcher) — the GitHub mirror of the long-running
  FFTPatcher modding-tool suite. Its `EntryEdit/EntryData/PSX/EventCommands.xml` data file is the
  machine-readable command schema the tool's own GUI event editor reads, with named (not just
  counted) parameters for each opcode. Cross-checked against the same file's "Event Instruction
  Upgrade" variant (a separate, later community ASM-hack opcode set) and confirmed byte-for-byte
  identical for every opcode used in this document's table, supporting the reading that these are
  genuine 1997 vanilla opcode definitions, not upgrade-hack-only additions.

Where a hex/name pairing from one of these sources was also independently found in FFHacktics
community wiki content (via search-indexed snippets, since the wiki's own domain is not directly
fetchable from this project's tooling), that second-source agreement is noted in the table's
confidence column.

**What this sourcing does and does not establish.** TIC's `.e` files reuse the exact same opcode hex
values, and — everywhere this project has been able to check a record's byte length against an
external source's declared parameter shape — the same record shapes, as these vanilla PSX-era
sources describe. This is strong circumstantial evidence that TIC's remaster engine inherited the
same event-script bytecode format rather than designing a new one, but it is not formal proof that
every opcode's runtime behavior is byte-for-byte identical across the roughly 28-year platform and
engine difference. Opcodes marked LIVE-CONFIRMED in the table above have had their effect on TIC's
own actor-table/runtime state directly observed under a controlled test; opcodes marked
NAME-CONFIRMED (with or without "structure cross-checked") have not — for those, the *name* and
*byte shape* rest on agreement with an external vanilla-PSX reference, while the precise in-TIC
runtime semantics of individual operand fields remain an inference from that external documentation,
not an independently verified fact about this remaster's executable.
