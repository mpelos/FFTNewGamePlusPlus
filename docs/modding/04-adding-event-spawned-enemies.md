# Adding a new enemy unit to an event-scripted battle wave

This document is the validated recipe for adding a brand-new enemy unit to a story battle whose
enemies are delivered by an event script mid-battle (a cutscene/wave trigger), as opposed to a
unit that is simply present in the ENTD from turn 1. It includes a byte-exact worked example from
the battle that validated the technique end-to-end: Merchant Dorter (Chapter 2 opener, ENTD entry
403, `entd/battle_entd4_ent.bin`).

For battles that are **not** event-scripted — the new unit just needs to be present at battle
start — do not use this recipe. Use the plain ENTD job-swap/new-slot technique described in
[06-job-swap-fallback-and-battle-inventory.md](06-job-swap-fallback-and-battle-inventory.md)
instead; it is simpler and carries none of the risk discussed below.

## The core fact: three coherent layers, not one

An event-spawned enemy unit is not produced by a single edit. It requires **three separate things
to exist together, consistently, pointing at the same unit id**:

1. **An ENTD slot** for the unit — job, stats, equipment, team/control flags. See
   [01-entd-binary-format.md](01-entd-binary-format.md) for the binary layout.
2. **A choreography block in the event-script file that actually drives that battle's wave** —
   the sequence of opcodes that positions, animates, and releases the new unit id. Built by
   copying a real, already-working neighbor unit's own block verbatim and retargeting every
   occurrence of the neighbor's id to the new unit's id (see "Authoring the choreography block"
   below).
3. **An explicit registration entry for the new unit's id** in that same script's unit-creation
   bracket (the `AddUnit` list bracketed by `AddUnitStart`/`AddUnitEnd`).

**Layer 2 alone is not sufficient.** A unit can have its position and visual fields actively driven
by the script — its tile coordinates can visibly update, exactly as commanded — while the unit
remains permanently inactive in the live battle-actor table. Only layer 3 flips the unit from
"data present" to "real, active combatant." This is a direct consequence of the two-stage
activation model described in
[02-battle-actor-table.md](02-battle-actor-table.md): a unit's actor-table entry has fields that
script-driven choreography opcodes can write to regardless of whether the unit is active, and a
separate state/flag pair that marks the unit as a live participant. Writing the former does not
imply the latter. Do not assume that a choreography block "doing something visible" (e.g. a tile
position field changing) means the unit is live — check the activation fields specifically (see
Verification below).

All three layers must reference the same unit id and must be internally consistent (ENTD slot's
unit id == choreography block's retargeted id == registration bracket's new entry). Missing any one
of the three, or mismatching the id across them, produces a unit that is either entirely absent or
a permanently-inactive ghost entry.

## Warning: identifying the correct script file

A battle's event script is not reliably found by following an NXD-table join (for example, a
mapping from a battle/event key to a script number). These joins can be — and have been — wrong.
A join that looks structurally correct (consistent key, consistent naming, no obvious off-by-one)
can still point at a script that is never actually loaded at the moment the battle's wave
activates. Treating such a join as ground truth and patching the script it names, without
independent confirmation, can produce a long sequence of correctly-built, correctly-deployed,
completely inert patches — every edit lands in a real file, builds cleanly, deploys cleanly, and
changes nothing in-game, because the file was never read at the relevant moment.

**The reliable way to confirm which file actually drives a specific battle's wave-trigger moment is
direct file-access logging**, not inference from a database join. Reloaded-II's general file-access
logging feature is built for exactly this:

```json
"LogGeneralFileAccesses": true,
"GeneralFileAccessType": "AllFiles"
```

With this enabled, the Reloaded-II log records every file the game opens, in order, with a
timestamp. Trigger the battle's wave (e.g. let the intro cutscene play through to the point where
the delayed enemies appear) and search the log for the script load that occurs at that exact
moment:

```text
[FFT File Logger] loaded: script/enhanced/event119.e (0x735 bytes)
```

This line — not any NXD join — is what identifies the correct target file. Before committing to a
script file as the patch target, confirm independently (via this logging, not via a table lookup)
that it is the file actually opened when the wave activates. If a previous patch attempt against a
"mapped" script produced no visible effect at all (no crash, no change, nothing), that is itself a
signal worth treating seriously: it is consistent both with "the technique is wrong" and with "the
file is wrong," and only file-access logging distinguishes the two. Do not spend further patch
iterations against a script file whose load has not been independently confirmed at the relevant
moment.

A second, weaker but free corroborating signal: also confirm that the mod's file override is
actually being registered by the modloader (e.g. by logging `IFFTOModPackManager.ModdedFiles` at
startup and checking the override path appears with a match count > 0). This rules out "the
override was never registered" as a confound, but it does **not** by itself prove you have the
right file — a correctly-registered override of the wrong file is still inert. Both checks are
complementary; file-access logging at the trigger moment is the one that actually answers "is this
the file that matters."

This logging mode is intentionally temporary. It is noisy enough to obscure the normal console while
playtesting, so turn `LogGeneralFileAccesses` back to `false` once the target script file is
identified. See [07-diagnostics-and-logging.md](07-diagnostics-and-logging.md) for the exact config
path and the other project-level diagnostic switches.

## Procedure

This procedure is generalized for any event-scripted battle that needs a new wave-spawned enemy
unit. Substitute the battle's own ENTD file, script file, and unit ids.

1. **Choose a free unit id** for the new unit, distinct from every id already used by that battle's
   ENTD entry and by its event script (check both — an id can be "free" in the ENTD's own roster
   while still appearing in the script for an unrelated purpose, e.g. a camera marker or a named
   character; reusing such an id will collide).

2. **Add an ENTD slot** for the new unit: job, level, equipment, reaction/support/movement, and the
   correct flags byte for a wave reinforcement (not a `LoadFormation`/always-present unit — see the
   caution below). See [01-entd-binary-format.md](01-entd-binary-format.md) for field offsets and
   flag semantics.

   **Caution**: cloning an existing slot that has the `LoadFormation` bit set produces a unit that
   is present during the intro cutscene itself, before the wave's sprites are loaded — this can
   manifest as the wrong sprite/portrait (falling back to whatever is already loaded for the
   intro), backward facing, and the unit being visible before the ambush/reveal is supposed to
   happen. The real wave-delivered enemies in a delayed-wave battle are reinforcement-flagged, not
   `LoadFormation`-flagged. Clone an existing reinforcement slot's flags byte, not an
   always-present one's.

3. **Identify the event-script file that actually drives this battle's wave activation**, per the
   warning above. Extract it from the game's packed data archive (the relevant `.pac` file under
   the game's `data/enhanced/` directory) using the project's archive-extraction tooling, and hash
   the extracted file so later diffs against it are exact.

4. **Locate the unit-creation bracket(s)** in the script: a single byte opcode that opens a
   unit-list (`AddUnitStart`), one or more 4-byte `AddUnit` records (`<opcode> <uid> 00 01`, one per
   unit being added), and a single byte opcode that closes it (`AddUnitEnd`). A script can contain
   **more than one** such bracket — do not assume there is exactly one. If there are multiple
   brackets, determine which one the existing late-wave units (the ones the new unit is being added
   alongside) are registered in; the new unit's registration entry belongs in that same bracket, not
   a new one and not the other existing bracket.

5. **Locate the existing choreography block for the last real unit in the same wave family** — the
   sequence of opcodes that sets the unit's final tile, moves/colors/draws its sprite, waits for the
   sprite move to finish, and plays an animation. This is the neighbor block you will copy.

6. **Copy the neighbor's choreography block verbatim, then retarget every occurrence of the
   neighbor's unit id within that copy to the new unit's id.** Do not hand-author a new block from
   first principles or attempt to derive per-field values analytically — every non-uid byte in a
   real working block is, by construction, already known to produce a working result for that
   opcode family; the only correctness requirement is that every id reference inside the copied
   block is consistently retargeted. Insert the retargeted copy immediately after the original
   block it was copied from (or at any point in the script after the relevant `AddUnit` bracket
   closes and before the rest of the wave's choreography runs — exact placement within that range
   has not been shown to matter, but placement immediately adjacent to the source block is the
   simplest to verify by inspection).

7. **Insert an explicit registration entry for the new unit's id into the unit-creation bracket
   identified in step 4** — a new `AddUnit`-family record for the new id, inserted immediately
   before that bracket's closing opcode (i.e., after the last existing entry in the list, not
   appended after the bracket closes). This is the step most likely to be skipped, because the
   choreography block alone (step 6) can appear to work — the unit's fields visibly update — while
   this registration entry is still missing. Do not treat a partially-successful test (fields
   moving, unit still inactive) as a dead end; it is the expected signature of having completed step
   6 without step 7, and the fix is to add this entry, not to revisit the choreography block.

8. **Build and deploy.** Confirm the patched script's resulting file size matches the original size
   plus the exact byte count of everything inserted (the choreography block's byte length plus the
   registration entry's byte length). A mismatch indicates a build/deploy that did not pick up the
   intended source file, not a problem with the bytes themselves.

9. **Test in-game and verify activation**, per the Verification section below. If the unit appears
   but its final position is wrong (e.g. on a rooftop, overlapping another unit, off the playable
   map), that is a separate placement issue, not a re-opening of the activation question — see the
   closing note on spawn placement.

### Insertion-safety notes

Before inserting bytes into an existing script file (as opposed to overwriting same-length bytes in
place), check the file for any mechanism that an insertion could desync:

- **Length-prefixed sub-blocks.** Some opcodes in this format carry a small fixed-shape duration/
  count parameter that can superficially resemble a sub-block length field. Confirm, by direct
  inspection, that any such field's value never extends across your insertion point — i.e., that it
  is a small, self-contained, fixed-shape operand (e.g. a frame-count duration for a `Wait`-class
  opcode), not a length field describing a variable-size region of the file.
- **A global header length/offset field.** Scan the file's header region for any value that equals
  the file's total length or the offset of a later section. If no such value exists, ordinary
  sequential opcode dispatch (each instruction's length determined by its own opcode, with the next
  instruction immediately following) is not at risk from a length-changing insertion.
- **A sibling file referencing this file's byte length.** Check whether any caller/index script
  that references this file by id also embeds an absolute byte length or offset into it. If the
  link between files is by id through a table (not an embedded byte offset), insertion is safe with
  respect to that link.

If all three checks come back negative for the specific region you are inserting into, a
length-changing insertion at that point is safe to deploy and test. This does not eliminate all
risk (it does not constitute a disassembly of the script interpreter's own instruction-fetch loop),
but it is the practical standard this technique has been validated against, and a real in-game test
with a length-changing, two-site insertion has confirmed no crash and a fully correct visual result
when these three checks pass.

## Verification: how to confirm it worked

Do not rely on a visual count of enemies alone as the only signal — confirm via the underlying
battle-actor-table fields described in
[02-battle-actor-table.md](02-battle-actor-table.md):

- **The unit is present in the actor table at all** — its slot shows the correct unit id.
- **Choreography fields are moving** — the unit's tile-position fields change during the cutscene,
  matching the values your copied/retargeted choreography block commands. This alone is **not**
  sufficient evidence of success — see the core fact above.
- **The activation fields specifically are set, not just present** — the unit's state byte equals
  its own table index (the same pattern every genuinely active unit in the table shows, not a
  sentinel/free value), and the accompanying activation flag is set. This is the field pair that
  distinguishes "real, active combatant" from "data present, permanently inactive."

A unit showing moved choreography fields but a state byte still at the inactive/free sentinel value
is the exact signature of a missing registration entry (layer 3) — return to step 7, not step 6.

A unit showing the correct active state byte and flag, with the correct sprite/portrait and no
crash, but standing on an unintended tile, is a successful activation with a separate, cosmetic
placement issue — see the closing note below.

## Worked example: Merchant Dorter's 7th enemy (the Knight captain)

Merchant Dorter's NG+ redesign (see
[`docs/battles/012-merchant-dorter.md`](../battles/012-merchant-dorter.md)) calls for a 7th enemy —
a Knight captain anchoring the street — added to the original 6-enemy band (2 Archer, 2 Black Mage,
2 Thief) without disturbing that band's identity. The 6 original enemies are wave-delivered:
present from the ENTD but not visible until an intro cutscene plays out and releases them.

### Layer 1 — ENTD slot

The new unit occupies **s9** of ENTD entry 403 (`entd/battle_entd4_ent.bin`, local entry 19),
unit id `0x86` — the next free id after the existing wave's `0x81`–`0x85`. It is flagged as a
reinforcement (matching the existing wave enemies' flags), not `LoadFormation` — an earlier attempt
that cloned a `LoadFormation`-flagged slot produced a unit with the wrong sprite (fell back to an
already-loaded Thief portrait), backward facing, and visible during the intro itself; that attempt
is why this flag distinction is called out explicitly in step 2 above.

### Layer 2, step one — identifying the correct script file

Merchant's enemy-to-event-script relationship is reachable via an NXD join (an `EnhancedBattleEvent`
key mapped to a script number) that names `event298.e`. Multiple independently-built, independently
byte-verified patches against `event298.e` — including a full second `AddUnit`-family choreography
block for `uid=0x86`, cloned from `uid=0x85`'s own block — built cleanly, deployed cleanly, and
produced **no change in-game whatsoever**: no crash, no 7th enemy, still 6.

Direct file-access logging (`LogGeneralFileAccesses=true`, `GeneralFileAccessType=AllFiles`) during
the actual wave-trigger moment showed the file the game opens at that instant is not `event298.e`:

```text
[FFT File Logger] loaded: script/enhanced/event119.e (0x735 bytes)
```

`event119.e` is the correct target. The `EnhancedBattleEvent`-key join to `event298.e` was a real,
correctly-registered mapping for some purpose, but not the one that gates this battle's wave
activation — every `event298.e` patch had been a correctly-deployed edit of a file that was never
the activation gate to begin with. This is the concrete case the warning above is written from.

`event119.e`, pristine, extracted from the game's `0005.pac` archive:

```text
size:   1845 bytes (0x735)
SHA256: F03EAEF91C46BB9524DDB1A8BB5E7D17E622240D7531695E5B9229F0F1A6AEBE
```

Structural facts about this file, confirmed by a full sequential opcode-stream walk:

- It contains **two** separate unit-creation brackets (`AddUnitStart`/`AddUnit`/`AddUnitEnd`,
  opcodes `0x49`/`0x45`/`0x4a`), not one:
  - **Bracket 1**, offsets `0x1E9`–`0x202`, registers `0x80, 0x81, 0x82, 0x83, 0x17, 0x34`.
  - **Bracket 2**, offsets `0x3C9`–`0x3D2`, registers `0x84, 0x85`:
    ```text
    0x3c9: 49                AddUnitStart
    0x3ca: 45 84 00 01       AddUnit uid=0x84
    0x3ce: 45 85 00 01       AddUnit uid=0x85
    0x3d2: 4a                AddUnitEnd
    ```
- `uid=0x86` appears **zero times anywhere** in the pristine file (confirmed by a brute-force
  whole-file byte search, not just an opcode-aware scan) — it is registered in neither bracket and
  has no choreography of its own.
- The last real wave unit, `uid=0x85`, has a complete per-unit choreography family late in the
  file (well after both brackets close):
  ```text
  5f 85 00 ...      final tile position
  3b 85 00 ...       sprite move
  32 85 00 ...        color/tint
  44 85 00 ...        draw
  3b 85 00 ...       sprite move
  32 85 00 ...        color/tint
  6f 85 00            wait for sprite move
  11 85 00 ...        unit animation
  ```
  `0x5f`'s operand correlates exactly with the live actor table's final-tile fields for that unit
  (`5f 85 00 05 0a 00 00` matches the table's recorded tile `(0x05, 0x0A)`), confirming `0x5f` sets
  final tile position.

### Layer 2, step two — authoring and inserting the choreography block

`uid=0x85`'s complete block was copied verbatim and every `85` byte retargeted to `86`. The final
tile was changed from `0x85`'s own `(5,10)` to `(7,10)` to avoid spawning on top of the existing
unit (this initial value was later revised again — see the closing note on spawn placement):

```text
5f 86 00 07 0a 00 00
3b 86 00 00 00 00 00 12 00 00 01 01 00
32 86 00 01 00 00 00 00
44 86 00
3b 86 00 00 00 00 00 00 00 00 01 1c 00
f1 08 00
32 86 00 08 00 00 00 02
6f 86 00
11 86 00 02 00 00
```

(The `f1 08 00` mid-sequence is a standalone `Wait` opcode — pause 8 frames — not a length-prefixed
sub-block; it is part of the copied block's own internal pacing and requires no special handling
during insertion.)

Inserted immediately after the source `uid=0x85` block, in the deployed file:

```text
5f 86 00 @ 0x679
3b 86 00 @ 0x680, 0x698
32 86 00 @ 0x68D, 0x6A8
44 86 00 @ 0x695
6f 86 00 @ 0x6B0
11 86 00 @ 0x6B3
```

Result (choreography insertion only — this is the v1 patch, **not yet sufficient on its own**):

```text
original: 1845 bytes (0x735), SHA256 F03EAEF91C46BB9524DDB1A8BB5E7D17E622240D7531695E5B9229F0F1A6AEBE
v1:       1909 bytes (0x775), SHA256 0ECDE03190898C1B0CBDD8B16491F97CFB2EEDD479CC4CF27395991C35BA37F8
```

**v1 test result, in-game**: no crash, nothing visually wrong during the cutscene, but still 6
enemies. The actor-table log was the decisive signal:

```text
a9 (uid=0x86): c50 changed 0x00 -> 0x0A, exactly matching the inserted 5f 86 00 07 0a 00 00 command
a9 (uid=0x86): st remained 0xFF, aux1b5 remained 0x00, the entire time
a7, a8 (the neighboring real wave units): both transitioned to active during the same scene
```

This is the exact signature described under "the core fact" above: the choreography block executed
and moved the unit's tile-position field, while the unit itself never activated. It directly
diagnoses a missing registration entry, not a defective choreography block — confirming step 7 of
the procedure is not optional.

### Layer 3 — the registration entry

`45 86 00 01` was inserted into **Bracket 2**, immediately after the existing `45 85 00 01` entry
and immediately before that bracket's closing `4a`:

```text
before (pristine):  ... 45 84 00 01  45 85 00 01  4a ...
after (v2 patch):   ... 45 84 00 01  45 85 00 01  45 86 00 01  4a ...
```

at offset `0x3d2` in the pristine file's addressing (i.e., the insertion point is the byte position
of the bracket's closing `4a`, which the new 4-byte record displaces forward). The choreography
block from v1 was kept unchanged.

```text
v2: 1913 bytes (0x779), SHA256 691BC1B13C4022A640E2E8201EB8F703ECB34ABC6AAADC7691E1A5D036543351
```

File-size accounting: `1845 + 64 (choreography block) + 4 (45 86 00 01) = 1913` — confirms no other
bytes were inadvertently touched.

The current placement-test variant keeps the same 1913-byte structure and the same registration
entry, but changes the first `5f 86` tile operand from the activation-proof `(7,10)` rooftop value
to `(5,7)`. This changes only where the already-working unit stands; it does not change the
three-layer activation mechanism. Current source and deployed script hash:

```text
current: 1913 bytes (0x779), SHA256 F36F4772D32B4D1D97E06A8779DBDD3E09656C983DA368D11D0F109686E65498
```

**v2 test result, in-game — confirmed success.** Merchant Dorter appeared with 7 enemies. The new
Knight rendered with the correct sprite and portrait. Actor-table log:

```text
a9:uid=0x86 st=0x09 ... c4f=0x07 c50=0x0A ... aux1b5=0x01
```

`st=0x09` is the unit's own table index — the same "state equals table index" signature every
genuinely active unit in the table shows — and `aux1b5=0x01` is the accompanying activation flag.
Both are now set, where v1 left them at the inactive sentinel (`st=0xFF`, `aux1b5=0x00`). This is
the confirmation criterion described in Verification above, satisfied end-to-end.

### Summary of the three layers for this example

| Layer | What | Where |
|---|---|---|
| 1. ENTD slot | s9, `uid=0x86`, Knight, reinforcement flags (not `LoadFormation`) | `entd/battle_entd4_ent.bin`, entry 403 |
| 2. Choreography block | `uid=0x85`'s block copied verbatim, retargeted to `0x86` | `event119.e`, inserted after the native `0x85` block (~`0x679`) |
| 3. Registration entry | `45 86 00 01` | `event119.e`, Bracket 2, before `4a` (~`0x3d2`) |

Without layer 3, layer 2 alone produced a unit with correct, script-driven tile data that was
permanently invisible and inactive. With all three layers present and mutually consistent, the unit
is a real, fully active 7th combatant.

## Closing note: spawn placement is a separate, mandatory check

Copying a neighbor's choreography block also copies that neighbor's final-position tile. That tile
is valid **for the neighbor**, in the neighbor's own spawn context — it is not guaranteed to be a
valid tile for the new unit, even after retargeting every id reference in the block.

In the worked example, the first deployed version of the new Knight's block used final tile
`(7,10)` — one tile past `uid=0x85`'s own `(5,10)`/`(6,10)`-adjacent position, chosen to avoid
overlapping the existing unit. The unit activated correctly (sprite, portrait, `st`/`aux1b5` all
correct) but visually landed on the map's rooftop — an inaccessible, clearly-wrong position for a
street-level frontline unit, despite the unit being otherwise fully functional. Fixing this requires
no change to the choreography or registration logic — only the `0x5f` final-tile operand needs to
change, by iterating toward a tile that is actually valid ground in the target map's geometry:

```text
(7,10)  — rooftop, invalid for this unit's intended role (deployed, confirmed wrong in-game)
(6,9)   — valid ground (deployed and confirmed in-game: lands correctly on grass, height 6.5)
(5,9)   — valid ground/height band, but still placed behind or lateral to the nearby Archer in
          the intended composition, so it was rejected as the final design tile
(5,7)   — current candidate: intended to put the Knight in front of the nearby Archer at `(5,8)`,
          same height band; deployed for the next visual confirmation
```

**Always verify the copied final-position tile against the actual map geometry for the new unit's
intended spawn context, rather than assuming a copied tile — or the first replacement tile tried — is
safe.** A wrong tile does not produce a crash, a build error, or any other diagnostic signal
distinguishing it from a correct one — the unit is fully active and otherwise indistinguishable from
a successful spawn in every log field. The only way to catch it is a visual in-game check of where
the unit actually stands once the wave activates, and placement may take more than one iteration to
land on a tile that is both unoccupied and valid ground — and a further iteration may follow even
after valid ground is confirmed, if the design calls for a more specific position (e.g. relative to
another unit) rather than merely any legal tile.
