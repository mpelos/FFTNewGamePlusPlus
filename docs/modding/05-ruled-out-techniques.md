# Ruled-out techniques and native-hooking constraints

This document covers approaches that do **not** work for adding a new event-spawned enemy unit to a
story battle, plus one approach that works for a different purpose entirely, plus native
runtime-hooking constraints for `FFT_enhanced.exe` that bear on any future hooking-based feature, not
just this one. The goal these techniques were evaluated against is the same one
[04-adding-event-spawned-enemies.md](04-adding-event-spawned-enemies.md) solves: introducing a
genuinely new unit that appears mid-battle, after an intro cutscene, inside an event-scripted wave —
not a job-swap of an existing slot, and not a unit present from turn 1.

Each section below states what the technique is, why it does not achieve that goal, and — where
applicable — what it is actually proven to do instead, so the underlying fact stays useful even
though the original application doesn't work.

## Native hooking of the unit-creation code path

Three native functions sit in the event-script interpreter's hot per-instruction dispatch loop, all
reached from the same call site cluster (relative to image base `0x140000000`):

```text
0x140272684   RESOLVE   — resolves a script-given unit id to a live actor-table entry
0x140273108   GET-SLOT  — checks whether a given table slot index is free (-1) or occupied
0x1402731B4   CREATE    — creates a new actor at a free slot (best-supported signature:
                          int CreateActorAtSlot(int slotIndex, int bpOperand), RCX=slotIndex,
                          RDX=sign-extended bp operand, return value ignored by every known caller)
```

Hooking any subset of these three — including a pure pass-through, observe-only hook that calls the
original function, logs its arguments and return value, and alters nothing — crashes the game at an
identical point during a battle's intro, every time. The crash signature is the same regardless of
which functions are hooked:

```text
[event-actor] resolve unit=0x81 status=-2 ptr=0x1418544E0
[event-actor] get-slot actorIndex=4 -> -1
(crash, no further log output)
```

This was confirmed with all three functions hooked, and reproduced again with only RESOLVE and
GET-SLOT hooked and CREATE left completely untouched — i.e., the crash is not a property of
intercepting the creation call specifically. The instability is a property of placing a detour
anywhere in this function neighborhood, not of any one function's calling convention or argument
handling. A "wrong CREATE signature" explanation cannot be the primary cause, since CREATE was never
called in the build that still crashed.

### Why static disassembly of this region is unreliable

`FFT_enhanced.exe`'s PE header shows concrete anti-tamper/obfuscation characteristics:

```text
IMAGE_FILE_RELOCS_STRIPPED = true
DllCharacteristics.DYNAMIC_BASE = false     (fixed image base, no ASLR, no relocation table)
Linker version 14.29                         (an ordinary modern MSVC linker — not itself unusual)
Unusual section layout: .xcode, .sbss, .00cfg, .impdata, .udata, .xtls,
  plus a .edata section with a virtual size of ~5.4 GB (nonsensical for real export data)
```

All five functions in the RESOLVE/GET-SLOT/CREATE neighborhood (plus the two adjacent helper calls,
a slot-precondition check at `0x1402411A0` and an occupied-slot-only touch function at `0x140273260`)
show, on disk, a short run of `int3` (`0xCC`) padding immediately followed by a 5-byte `jmp` to an
address far outside the executable's `SizeOfImage` — consistent with a virtualization-style wrapper
that replaces selected function prologues on disk with VM-entry stubs, where only a running,
unwrapped process shows the real prologue. The RVA-to-file-offset math itself was verified correct by
cross-checking the dispatch loop's own entry point, which is plain, unencrypted, on-disk code and
matches a live capture byte-for-byte. Static on-disk disassembly of the three target functions
specifically cannot currently confirm or refute anything about their argument count, stack frame, or
internal behavior — only live, in-process capture (call-site disassembly, or a hooked function's own
observed register/stack state at runtime) is trustworthy evidence for this region of the binary. This
is a binary-wide property of however the protection layer selects functions to wrap, not something
specific to these three functions.

### Leading explanation for the crash

The most defensible statement supported by the evidence: a detour placed anywhere in this specific
RESOLVE/GET-SLOT/CREATE neighborhood reproducibly destabilizes the game during a battle's intro,
independent of which of the three functions is hooked or whether the hook is a pure pass-through.
Two explanations remain consistent with all available evidence and are not distinguished from each
other by anything tested so far:

1. **Hook-induced re-entrancy or timing shift on a hot per-instruction path.** The dispatch loop runs
   once per 4-byte instruction record, many times per frame during an intro. A detour adds a
   trampoline jump and a managed/native transition on every call; if anything downstream is sensitive
   to call latency (a stack-depth-sensitive recursive call, a same-frame state machine, or an
   SEH/vectored-exception interaction with the protection layer), added cycles per call could matter.
2. **The protection layer reacts to a foreign detour planted in or near a function it specifically
   wrapped**, independent of whether the hook is logically correct — i.e. it doesn't care whether the
   hook's arguments and return value are right, only that the bytes at the protected address changed.

Both explanations predict exactly what was observed: pure pass-through hooks crash identically to a
hook that alters behavior, and the crash always lands at the same log line regardless of which
function combination is hooked.

### A confirmed-stable, different hook point

A separate, unrelated function — `TransitionIntoBattle`, the once-per-battle-load "enter combat"
transition point, not part of the per-instruction dispatch loop — is a confirmed-safe location for a
passive, pass-through hook. Evidence:

- A pure pass-through hook (calls the original function first, increments a counter, logs that it
  fired, touches no unit memory) was deployed and tested in-game: no crash, the hook fires reliably
  across multiple calls, and it fires at a timing point that precedes the delayed wave's own
  activation sequence completing — i.e. it is both stable and well-timed relative to battle setup.
- A third-party, independently-developed and publicly released Reloaded-II mod
  (`dicene/fftivc.unitcontrol`) hooks this same function with no special crash-handling code, in a
  shipped release — independent evidence this hook point does not sit in the same fragile
  neighborhood as RESOLVE/GET-SLOT/CREATE.
- `TransitionIntoBattle`'s address was located the same way as the live battle-actor table's base
  address (an AOB signature pattern, statically resolved against the locally-installed executable,
  no process attached) and resolved to a single hit, landing in the `.xcode` section.

**Forward-looking guidance**: if a future feature needs to hook native code in `FFT_enhanced.exe` for
any purpose, `TransitionIntoBattle` is the known-safe hook point — once-per-battle-load timing, no
observed instability, third-party precedent. The RESOLVE/GET-SLOT/CREATE neighborhood (and by
extension, the entire hot per-script-instruction dispatch loop) is not a safe place to hook anything,
observe-only or otherwise, until a future isolation test (hooking exactly one of the three functions
alone, never combined with the others) narrows down whether the failure is per-function or
neighborhood-wide. No such isolation test has been run; the current evidence only supports "this
neighborhood as a whole is unsafe to hook," not a finer-grained verdict.

## Reusing the guest-arrival ENTD pattern for an enemy unit

"Guest" status in this codebase is not a mid-battle materialization mechanism — it is a narrative and
ownership label applied to an ordinary ENTD slot that is present on the map from turn 1, exactly like
any other ally or enemy slot. There is no runtime mechanism anywhere in this project, vanilla FFT, or
this mod's own code that makes a guest unit appear partway through a battle the way an event-scripted
enemy wave does.

The mechanism, read directly from `src/fftivc.battles.ngplus/Program.cs`'s `ScaleGuestsAlways()`: for
every ENTD slot, if the slot's CharId is a known guest id AND its MainJob equals that CharId (the
guest-detection signature — see
[01-entd-binary-format.md](01-entd-binary-format.md#guest-vs-enemy-vs-player-controlled-detection-rule)),
the function forces the slot's Level byte to party level and, if the slot is not on the enemy team,
ORs in the player-control flag bit. This is a pure data rewrite applied to the static ENTD buffer at
file-read time, before the battle loads. It does not hook the event-script interpreter, does not
touch the live battle-actor table, and runs once, not "later" — the guest's slot is a completely
ordinary, always-present ENTD slot from the instant the ENTD entry is read, identical in kind to the
already-ruled-out always-present-slot approach (see below). A guest's documented "joins after this
battle" phrasing means the character becomes recruitable on the world map after victory, not that
they materialize mid-fight.

A bit-level survey of 8 documented flags-byte (`0x18`) values across multiple battles confirms every
guest uses the same AlwaysPresent (`0x80`) pattern as ordinary always-present enemies and scripted
allies — there is no separate guest-specific bit or mechanism that distinguishes "appears later" from
"present from the start." Reusing this pattern for a new enemy slot reduces to the same approach
already confirmed not to work (wrong sprite during the intro, since the new unit's job is outside the
battle's small intro-time sprite preload set — see the always-present-slot section below for the full
mechanism).

### Side finding: the "enemy team" flag bit is not a clean discriminator

`Program.cs`'s `ENEMY_TEAM_BIT` (`0x10`) is not a reliable "this slot is hostile" signal in isolation.
It is set on at least two shipped, documented **friendly** guest slots (a guest at Zaland, an
unidentified ally at Goug Lowtown) in addition to ordinary enemy slots. The shipped code does not
make this mistake — it determines guest status from the CharId/MainJob signature first, and only
consults `0x10` afterward, to decide whether to also grant player control to an already-identified
guest, never to decide team membership for an arbitrary slot. Any other reasoning about this flags
byte should follow the same order: identify guest/ally status by the CharId/MainJob signature, not by
`(flags & 0x10) != 0` alone. Full bit table in
[01-entd-binary-format.md](01-entd-binary-format.md#flagscontrol-byte-0x18).

## The event-injected "add" data file as a larger-roster precedent

`fftpack/event_btlevt_bin_entrydata_add_ent.bin` contains entries with up to 13 occupied unit slots
(true maximum: entry 60, 13 units; several others have 10-12) — more than any single event-scripted
enemy wave in this game uses. This is not usable as precedent for delivering a larger enemy roster,
because the file's confirmed, in-game-proven function is something else entirely.

The file shares its record structure with the base ENTD format (`0x28`-byte unit records, 16 slots
per `0x280`-byte "entry," level byte at the same relative offset, same `>99 = party-relative` level
encoding — see [01-entd-binary-format.md](01-entd-binary-format.md)). Its actual, confirmed purpose is
**event-injected guest/ally unit data** — the mechanism behind the already-shipped fix for guest
units (e.g. a Chapter 1 squire guest) entering NG+ battles at their original fixed low level instead
of scaling with the player's party. See `notes/03-guests-scaling.md` for the full in-game-validated
investigation that established this: a guest's level and job-level seed are read from a record in
this file at the moment the guest joins the story, not from the base ENTD, and not from a runtime
event-script mechanism. That fix is live in the shipped mod.

The file's larger entries (10-13 units) are not single-battle enemy rosters. They are reusable
per-event templates that mix recurring monster and named-character archetypes across multiple,
otherwise-unrelated battles. For example, the largest entry (60, 13 units) combines three named
characters from one story chain with a 6-unit cluster of one monster job (independently confirmed
elsewhere in this project's documentation as the reinforcement wave for a specific castle-keep
battle) and a 2-unit cluster of a different monster job (confirmed elsewhere as a boss's transform
encounter) — three unrelated battles' worth of data sharing one entry index. Both monster job ids
recur in other entries in the same file under different slot counts, confirming these are
template-reuse buckets indexed by an internal slot-role convention, not a transcription of any single
battle's deploy screen. There is no header field anywhere in the file's record structure encoding "N
units for this battle" — occupancy is purely implicit from which of 16 fixed slot positions are
non-empty, the same convention the base ENTD format uses everywhere.

**Standing fact for future use**: this file and its proven guest/ally-injection mechanism is the
right starting point for any future feature that needs to inject an ally or guest unit at a
story-event trigger point (for example, a chocobo-guest mechanic). It is not applicable to
mid-battle enemy-wave delivery, which is a structurally different consumption path (the live
battle-actor table and event-script registration described in
[02-battle-actor-table.md](02-battle-actor-table.md) and
[03-event-script-opcodes.md](03-event-script-opcodes.md)), not this file's event-injected-guest path.

## The `AddGhostUnit` event-script opcode (`0x47`)

`0x47 AddGhostUnit` is a real, vanilla (not upgrade-hack-only) event-script opcode, confirmed used by
this game's own scripts, but its parameter schema rules it out for adding a combat-roster enemy. Its
parameters, per the authoritative FFTPatcher command schema:

```text
Spritesheet  (2 bytes)
Index        (1 byte)
X            (1 byte, unsigned)
Y            (1 byte, unsigned)
Z            (1 byte, unsigned)
Facing       (1 byte, hex)
Draw         (1 byte, hex)
```

There is no `Unit`-typed parameter anywhere in this schema — unlike `0x45 AddUnit`, `0x5f WarpUnit`,
`0x3b SpriteMove`, and every other opcode in the combat-roster family, which all take a `Unit`
parameter referencing an existing ENTD/roster entry. `AddGhostUnit` instead constructs and places a
sprite from scratch, addressed by a spritesheet index and explicit screen coordinates, with no
reference to the unit/roster addressing system combat units use.

Five genuine usages exist across this project's own event scripts (confirmed via a record-boundary-
aware scan, not a raw byte search, to exclude false-positive byte matches inside unrelated opcode
parameters), each immediately followed by the same choreography opcode family
(`0x3b`/`0x6f`/`0x11`/`0x7f`) real combat units also receive. Every uid introduced by one of these
five `AddGhostUnit` records is structurally absent from every confirmed combat-roster opcode family
(`0x45 AddUnit`, `0x5f WarpUnit`, `0x4e UnitShadow`, `0x68 MirrorSprite`) anywhere in the scripts that
contain it — checked exhaustively, zero overlap. The two `AddGhostUnit` records in Merchant Dorter's
own intro script introduce uids that correspond positionally to two already-known named scripted
allies visible in the same establishing shot, consistent with this opcode's role: presenting a
non-combatant figure who is already present in the battle through a separate mechanism (an ordinary
ENTD ally slot), not spawning a new combatant.

**What this opcode is actually for**: a coordinate-addressed, spritesheet-driven cutscene display
entity. It receives full presentation-layer treatment (movement, pose, palette, an explicit `Draw`
flag) identical in shape to what real combat units receive, which is why it could be mistaken for an
alternate unit-creation path — but presentation-layer choreography and combat-roster registration are
confirmed to be two separate systems in this engine (see the two-stage activation model in
[02-battle-actor-table.md](02-battle-actor-table.md)), and `AddGhostUnit` only ever reaches the
former. Using it to add a 7th enemy would place a non-combatant decorative sprite, not a unit that can
be targeted, take a turn, or be defeated.

## Chained multi-stage battle restructuring as a level-design alternative

Unlike every other entry in this document, this is not a technical dead end — it is a real, working
technique with genuine tradeoffs that make it situational rather than a default choice for adding a
new enemy.

This project ships several multi-phase chained battles (for example, a castle Gate → Keep → Roof
sequence), where each stage is its own complete, independent ENTD entry with its own map, own deploy
screen, and own win condition. The transition between stages is vanilla FFT's own story-event
sequencing — clearing one stage's win condition advances the story script, which loads the next
battle. A grep across `src/fftivc.battles.ngplus/Program.cs` confirms zero chain, transition, or
sequencing code for this pattern: it is entirely vanilla game behavior, configured only through which
existing ENTD entries and story events the data points at. A new, genuinely new (not job-swapped)
enemy slot in the second or third stage of such a chain is just an ordinary ENTD slot in a freshly-
loaded battle — there is no wave-spawn or event-script materialization problem to solve, because
there is no mid-script appearance involved at all.

**Mechanically viable, confirmed by precedent**: every existing chain in this project retunes a link
that already existed in vanilla FFT's own story sequence (the mod adjusts levels, gear, and loadouts
inside an already-existing chain; it does not invent the chain itself). Authoring a brand-new chain
link from scratch — inserting an additional battle into a sequence where vanilla FFT did not already
have one — is a different, unattempted problem. The "battle complete → load next battle" sequencing
mechanism is confirmed to exist and work (used in every shipped chain), but how to author a wholly new
link into it, as opposed to reusing one vanilla FFT already had, has not been derived from a read-only
pass over this codebase.

**Why this is situational, not a default choice**:

- Every existing chain in this project sits at its chapter's **climax** — explicitly framed in this
  project's own battle docs as a chapter's defining trial or finale, where multiple consecutive
  battles with no resupply between them is itself part of the intended difficulty statement. None
  sits at a chapter's **opener**.
- A chained second stage changes the experience from "a new enemy reveals itself mid-fight" to "two
  separate skirmishes presented back-to-back" — a battle-end/battle-start screen transition replaces
  an in-fight surprise. This is a structurally different kind of payoff, not merely a smaller version
  of the original one.
- It costs real design scope: a new narrative beat not implied by existing source material (unlike
  every shipped chain, which retunes a beat the original game's story already had), a new map/
  positioning/builds section roughly doubling a battle doc's footprint for one additional enemy, and
  — if inserted as a genuinely new slot in a chapter's existing battle order — renumbering every
  subsequent battle in that chapter.

**When to reach for this technique**: a battle that is already a chapter's climax and could credibly
support a two-act structure on its own narrative merits. Not a battle explicitly designed to stay
small or to function as a low-stakes chapter opener — forcing the pattern onto a battle in that
position trades an unsolved engine question for a narrative-invention and chapter-pacing cost, which
is not obviously a better trade.

## A static, always-present extra ENTD slot

A new ENTD slot flagged AlwaysPresent (`0x18` bit `0x80` set — see
[01-entd-binary-format.md](01-entd-binary-format.md#flagscontrol-byte-0x18)) does not require any
event-script involvement at all — it is simply part of the battle's roster from the moment the ENTD
entry loads, the same as any ordinary enemy or guest slot. This sidesteps the entire event-script
materialization problem by construction. It can deliver a visually-correct unit, but only under a
narrow, easy-to-violate constraint.

**The constraint**: a battle's pre-battle tactical-view intro cutscene only loads a small subset of
sprites into memory — the "intro preload set" — which is typically much smaller than the full roster
of jobs that battle eventually uses (a battle with 9 total roster slots may have an intro preload set
of as few as 4 distinct visuals, covering only the slots that are themselves AlwaysPresent). A new
AlwaysPresent slot whose job is **not** already in that battle's intro preload set has no sprite
resolved for it during the intro and silently falls back to whatever generic sprite is already
resident — producing a wrong-looking unit (for example, a unit intended to display as one job
rendering as a completely different, already-loaded generic job instead).

A new AlwaysPresent slot only renders correctly if it reuses a sprite/job that is **already part of
that specific battle's own intro preload set** — concretely, the job of one of that battle's existing
AlwaysPresent slots. Reusing the job of a unique, named character produces a visually duplicated named
character (a second copy of an existing story figure standing in the intro), which is a more
obviously broken result than a generic-job fallback. Reusing a generic job already used by an existing
AlwaysPresent slot is the only sound choice, and it constrains the new unit to look like that same
generic job — it cannot deliver a distinct job identity (for example, a Knight) if no AlwaysPresent
slot in that specific battle already uses a Knight sprite. This is a real per-battle constraint, not a
portable rule: which job is "safe" to reuse must be checked fresh for each battle's own intro preload
set, and a battle with no scripted intro cutscene at all has no such constraint to dodge in the first
place.

A second, unconditional cost applies regardless of which job is reused: the unit is visible from the
very start of the intro cutscene, not as a mid-battle reveal. For a battle whose design specifically
wants a new enemy to appear as a surprise once the fight is already underway, this technique cannot
deliver that beat — it can only deliver an extra unit who is already standing there from frame one.

Whether a unit's rendered sprite re-resolves once the full battle sprite set loads after the intro
completes (as opposed to staying cached on whatever the intro resolved) has not been established by
any in-game test in this codebase. This question only matters if a design insists on a job that is
**not** in the intro preload set despite the constraint above; reusing a job already in the preload
set sidesteps the question entirely, since there is no fallback-then-possible-correction sequence to
observe in that case.

## Three refuted structural hypotheses

Three narrower hypotheses about where enemy-roster size might be encoded, or where a second example
of Merchant Dorter's own delayed-wave mechanism might exist, were tested directly against this
project's data and refuted.

**No other vanilla battle in this project's documented scope shares Merchant Dorter's specific
delayed-wave mechanism, so none is usable as an independent comparison or precedent for it.** Two
separate checks converged on this. First, an ENTD-flags-byte scan across all four
`battle_entd{1-4}_ent.bin` files for any other contiguous run of present, non-empty slots sharing
Merchant's own reinforcement-flag signature (`0x18` = `0x10`, not the `0x80` AlwaysPresent bit)
returns entries outside this project's documented chapters (almost certainly generic/non-story
battles) plus a handful of documented entries — Goug Lowtown, Riovanes Castle Keep, Eagrose Castle —
that each turn out, on reading their own battle docs, to be a static full roster or a scripted-
transform-boss artifact, never a genuine intro-then-wave structure. A separate, similarly-shaped
roster (Ziekden Fortress, entry 401, 11 used slots including slots 9-10) is not a counter-example
either: its two highest slots are 2 Black Mages that are simply part of one large static roster, with
no intro-cutscene-gated reveal, and its own wave-adjacent scripts (`event031.e`/`event032.e`) contain
none of the per-unit choreography opcodes (`0x7f`/`0x11`/`0x3b`/`0x4e`) that mark Merchant's
mechanism. Second, and more fundamentally: the `EnhancedBattleEvent` template family that ultimately
routes into Merchant's own choreography file (the `UnkType4=37` "position block" pattern feeding a
shared call to script 298) is used by exactly 9 keys in the entire event table, of which Merchant is
the only one this project has identified against a real, documented battle — the other 8 keys' own
unique intro scripts are not present in this project's locally extracted script set, so even if one of
them does use a differently-sized wave, that is not currently checkable. Net effect: a true,
independently-checkable second example of this mechanism is not known to exist in this project's
current data, so no other battle can currently serve as a "does the wave size generalize" test case
for the recipe in [04-adding-event-spawned-enemies.md](04-adding-event-spawned-enemies.md).

**`EnhancedBattleEvent` row count does not track enemy roster size per battle.** This NXD table's
position-block row count (rows where the per-row opcode field equals `37`) is constant at exactly 5
for every one of the 9 distinct battle keys that use this opcode anywhere in the entire table —
including the one key independently confirmed to correspond to a real battle with 5 documented
delayed enemies, which is what originally made the row count look like a per-battle record. No key
in this 9-key cluster deviates from 5, and no other key in the table uses this opcode at all. Multiple
keys in the same cluster share the identical map-id reference and an identical per-instance selector
constant that increments by exactly 1 across the cluster, and several keys in the cluster have no
sortie-launch link at all — both facts consistent with a single shared, reusable deploy-position
template reused across a family of similarly-shaped battles, not 9 independently-sized enemy rosters
that coincidentally all equal 5. Inserting an additional row into this table to add a 6th position
record was evaluated and is not recommended: it risks desyncing the row count's expectations for
every other battle sharing the same template shape, for an effect on the actual roster that has no
confirmed mechanism (the per-battle script, not this table, is what's confirmed to drive how many
actors get created).

**An event-key-to-script-number NXD join exists but is unreliable and must not be trusted without
independent confirmation.** A table join chain in this project's NXD data nominally maps a battle's
event key to the specific event-script file that drives it. This mapping has been found to not
correspond to the script the game actually loads at runtime for at least one battle, in a way only
detected after the fact via direct file-access logging at runtime. Do not treat this join as
authoritative on its own for identifying which script file actually drives a given battle's wave —
confirm the target file through the runtime-verification approach described in
[04-adding-event-spawned-enemies.md](04-adding-event-spawned-enemies.md) before relying on an NXD-join
result for this purpose.
