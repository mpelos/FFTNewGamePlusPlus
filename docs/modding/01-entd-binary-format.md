# ENTD binary format (`battle_entd{1-4}_ent.bin`)

The ENTD ("Entry Table Data") files are the primary static unit-roster format for story and
random battles. Each entry describes the up-to-16 units present on one battlefield: their
identity, job, equipment, level, position, and team/control flags. This document covers the
confirmed binary layout, the level relative-encoding scheme, the control-flags byte, and the rule
for telling a guest, an enemy, and a player-controlled unit apart from raw bytes alone.

This format is read at battle-load time by the game's file-read path; this project's own
`src/fftivc.battles.ngplus/Program.cs` hooks that read to apply NG+ level scaling, guest scaling,
and job-swap edits. The offsets below are cross-checked against that shipped, working code.

## File-level structure

The Enhanced version ships four ENTD files, each covering a contiguous range of global entry
numbers:

| File | Global entries |
|---|---|
| `battle_entd1_ent.bin` | `0-127` |
| `battle_entd2_ent.bin` | `128-255` |
| `battle_entd3_ent.bin` | `256-383` |
| `battle_entd4_ent.bin` | `384-511` |

Each file has a flat, headerless layout:

```text
128 entries per file
0x280 bytes per entry   (16 slots x 0x28 bytes/slot)
16 unit slots per entry
0x28 bytes per unit slot
0x14000 bytes total per file (128 x 0x280)
```

A **slot** is one unit record (0x28 bytes). An **entry** is one battle's full roster: 16 slots,
some of which are empty/unused depending on how many units the battle actually has. One ENTD
**entry** generally corresponds to one story or random battle.

### Addressing formula

```text
file number        = global_entry // 128 + 1
local entry         = global_entry % 128
entry file offset   = local_entry * 0x280
unit (slot) offset  = entry file offset + slot * 0x28
field offset        = unit offset + <field offset from the table below>
```

Within this project's own code, the ENTD fftpack indices map to file number as
`fileIndex - 224` (i.e. fftpack index `224` is `battle_entd1_ent.bin`, `227` is
`battle_entd4_ent.bin`); `global_entry = (fileIndex - 224) * 128 + local_entry`.

## Slot (unit record) byte-offset table

All offsets below are relative to the start of a 0x28-byte slot. Confidence notes are given
per-field; fields with no caveat are confirmed both by independent byte-level derivation and by
this project's shipped, in-production code.

| Offset | Size | Name | Meaning / notes |
|---|---|---|---|
| `0x00` | 1 | SpriteSet | Visual spritesheet index. |
| `0x00` | 1 | CharId | Same byte as SpriteSet in practice — this project's code treats `0x00` as the unit/character id. Named characters use a low, stable id (e.g. `0x04` = Delita, `0x07` = Argath); generic/templated enemies use `0xFF` or values in the `0x80+` range. See the CharId vs SpriteSet note below. |
| `0x01` | 1 | Gender/appearance flags | `0x80` = male human, `0x40` = female human, `0x20` = monster. This selects the generic human gender/sprite variant and is distinct from the actor-table gender byte at live offset `+0x06`. Not used by guest/team logic — see ENTD `0x18` for control behavior. |
| `0x02` | 1 | SpecialName | Special-name/portrait id. |
| `0x03` | 1 | Level | Unit level. Uses the **relative-encoding scheme** — see dedicated section below. |
| `0x04` | 1 | Month | Birth month (flavor data). |
| `0x05` | 1 | Day | Birth day (flavor data). |
| `0x06` | 1 | Bravery | Bravery stat. |
| `0x07` | 1 | Faith | Faith stat. |
| `0x08` | 1 | JobUnlock / job-seed target | Selects which roster job-level/JP bucket receives the `0x09` JobLevel seed. It is **not** a visible job rank. For generic jobs, the safe rule is `job_seed_target = mainJob(0x0A) - 0x4A` (`Chemist=1`, `Knight=2`, `Archer=3`, `Monk=4`, `WhiteMage=5`, `BlackMage=6`, `TimeMage=7`, etc.); this is the rule used by the project's patch tooling when re-jobbing generics. Named guests are more delicate and the mapping is not generalized: Delita testing proved `0x08=7, 0x09=8` seeds Time Mage Lv8, not Squire Lv8, while the current Chapter-1 Squire guest patch path uses the known source-record target (`0x08=1`) with `0x09=8`. Do not change a named guest's `0x08` by theory alone; verify the visible job level through a pre-join save or decoded roster cache. |
| `0x09` | 1 | JobLevel | Job level value seeded into the job selected by `0x08`, at the moment the unit is instantiated (join time for guests). Does not retroactively fix a unit already cached into the save — see the save-cache caveat below. |
| `0x0A` | 1 | Job (MainJob) | The unit's main/displayed job id. Central to the guest-detection rule — see below. |
| `0x0B` | 1 | SecondaryAction | Secondary skillset id. |
| `0x0C` | 2 | Reaction | Reaction ability id. **2-byte field** (`short`), not 1 byte — this is the single most common source of an off-by-one miscount in this format; see the Caution section below. |
| `0x0E` | 2 | Support | Support ability id. 2-byte field. |
| `0x10` | 2 | Movement | Movement ability id. 2-byte field. |
| `0x12` | 1 | Head | Head equipment slot. |
| `0x13` | 1 | Body | Body equipment slot. |
| `0x14` | 1 | Accessory | Accessory equipment slot. |
| `0x15` | 1 | RightHand | Right-hand equipment slot. |
| `0x16` | 1 | LeftHand | Left-hand equipment slot. |
| `0x17` | 1 | Palette | Color palette id. Also doubles as a rough "is this a combat-capable slot" signal in practice: in at least one surveyed battle, every actual combatant slot used `0x17 = 0x03`, while purely decorative/non-combat story-unit slots used `0x17 = 0x00`. Not verified as a general rule across all entries. |
| `0x18` | 1 | **Flags2 (control/team flags)** | The control/team flags byte. This is the byte this project's code calls `SLOT_CONTROL_FLAGS`. Full bit breakdown below. |
| `0x19` | 1 | X | Spawn tile X coordinate. |
| `0x1A` | 1 | Y | Spawn tile Y coordinate. |
| `0x1B` | 1 | FacingDirAndUpperLevel | Lower nibble = facing direction; high bit = elevation/upper-level flag. The specific compass-direction-to-nibble-value mapping has not been independently derived by this project; only that the lower nibble is direction and the top bit is a separate elevation flag. |
| `0x1C` | 1 | Experience | Starting experience value. |
| `0x1D` | 1 | SkillSet | Skill set id. |
| `0x1E` | 1 | WarTrophy | Spoils-of-war item slot (same concept as "Spoils of War" elsewhere in this project's reward-system documentation). |
| `0x1F` | 1 | BonusMoney | Bonus gil field. Not independently confirmed beyond its name/position. |
| `0x20` | 1 | UnitID | The unit's **in-battle** id, distinct from CharId/SpriteSet at `0x00`. Generic enemies commonly use `0x80` and up (e.g. a 5-enemy wave uses `0x81`-`0x85`); named/scripted units use small distinct ids. This is the id that event-script opcodes (e.g. the actor-resolve and AddUnit family) reference when they target a specific unit. |
| `0x21` | 1 | TargetX | Target/destination X coordinate (purpose beyond the name not independently verified). |
| `0x22` | 1 | TargetY | Target/destination Y coordinate (purpose beyond the name not independently verified). |
| `0x23` | 1 | Flags3 | Additional flags byte; bits not decoded. |
| `0x24` | 1 | Target | Target-related byte; not decoded further. |
| `0x25` | 1 | Unk25 | Undecoded. |
| `0x26` | 1 | Flags4 | Additional flags byte; bits not decoded. |
| `0x27` | 1 | Unk27 | Undecoded. |

Total: 40 bytes (`0x28`), matching `SLOT_SIZE` exactly with no gaps.

### Gender/appearance flags at `0x01`

Confirmed ENTD values:

```text
0x80 = male generic human
0x40 = female generic human
0x20 = monster
```

Gender recasts must update a coherent two-byte pair, not only `0x01`:

```text
generic male    : +0x00 sprite/CharId 0x80, +0x01 gender 0x80
generic female  : +0x00 sprite/CharId 0x81, +0x01 gender 0x40
generic monster : +0x00 sprite/CharId 0x82, +0x01 gender 0x20
```

Entry 460 (Mullonde Exterior) exposed this distinction in game: changing only `0x01` made s1-s5
female internally but left their visual sprite identity at male `0x80`. The corrected implementation
keeps s0 as `0x80/0x80` and changes s1-s5 to `0x81/0x40`. Jobs, UnitIDs, control flags (`0x18`),
positions, and event delivery remain unchanged. Do not confuse ENTD `0x01` with the live actor table's
gender flags at actor offset `+0x06`; the flag values match, but the structures do not.

### CharId vs SpriteSet at offset `0x00`

Offset `0x00` is referenced under two different names depending on which part of this project's
tooling or documentation is read: "SpriteSet" (visual asset selection) and "CharId" (the
character/unit identity byte the guest-detection and team logic reads). In practice this project
treats them as the same byte — `Program.cs`'s `SLOT_CHARID = 0x00` constant is the one actually
read by the live guest-scaling code. Treat "CharId" as the operative name for this offset when
reasoning about unit identity or guest detection; "SpriteSet" is the same byte under its
classic-FFT-derived name.

### Save-cache caveat for `0x09` (JobLevel) and `0x03` (Level)

Both the Level byte (`0x03`) and the JobLevel seed (`0x09`) are read at the moment a unit is
**instantiated** — for an enemy, that's battle start; for a guest, that's the join cutscene that
adds them to the roster. Once a guest has joined the roster, their visible level, Job Level, and
JP live in the save's roster cache, not in the ENTD slot anymore. Patching the ENTD slot after a
save already has that guest cached has no effect; testing any Level/JobLevel change requires a
save from before the guest's join (or a new game).

### Practical rule for `0x08` / `0x09`

Treat `0x08` as "which job bucket receives the seed" and `0x09` as "the seed value." That rule is
simple for generics and dangerous to over-generalize for named guests:

- **Generic enemy or generic ally:** set `0x08 = mainJob - 0x4A` and set `0x09` to the intended job
  level. Example: generic Knight main job `0x4C` uses `0x08=2`; generic Time Mage main job `0x51`
  uses `0x08=7`.
- **Named guest join data:** preserve the known-good `0x08` target for that specific guest record
  unless an in-game pre-join test proves otherwise. A wrong target can make a different job receive
  Lv8 while the displayed job remains Lv1.
- **Validation:** test from before the unit joins the roster. If the unit is already cached in the
  save, ENTD changes can appear to fail even when the bytes are correct.

#### Ability-learning caveat: one seeded job, random learned skills

`0x08/0x09` does **not** mean "set every job to this level" and does **not** directly write a full
learned-ability list. It seeds one job/unlock bucket. The game then gives enough JP/context for that
job path and spends/assigns learned abilities through the normal enemy generation logic, which can
produce different learned skills between otherwise similar units.

Validated consequence on Outlying Church / entry `445`:

- Setting the three Knights' `0x08` to Monk (`4`) and `0x09=8` did **not** make them Knight Lv8 plus
  guaranteed full Martial Arts. In-game they appeared as Knight Lv3 with several Martial Arts skills.
  The best explanation is that Monk's prerequisite path funds/raises Knight enough to unlock Monk,
  while the seeded bucket and learned skills are resolved separately by the game's JP logic.
- Setting the Mystics' `0x08` to Summoner (`8`) and `0x09=8` left their visible Mystic job at Lv1.
  Their Summon secondary learned different numbers of summons between the two units. This fits the
  same model: Summoner is the seeded bucket, but learned skills are not a deterministic "all skills"
  mask from the ENTD slot.

Operational rule:

```text
If the unit's main/displayed job must be full strength, keep 0x08 pointed at the main job bucket.
Do not point 0x08 at a secondary job expecting both main-job Lv8 and secondary-job Lv8.
ENTD alone currently cannot guarantee a full learned secondary skill list.
```

For battle design, this means a secondary skillset in `0x0B` is safe as a command assignment, but the
exact learned abilities behind that secondary are not guaranteed by `0x08/0x09` unless that same
secondary job is the single seeded bucket and the resulting partial/random learned list is acceptable.
If a design requires precise full secondary skills, use a different design (make that job primary,
choose a secondary whose partial list is acceptable, or implement a future runtime/roster learned-
ability patch once the learned-skill bitfields are mapped).

## The level relative-encoding scheme

The Level byte (`0x03`) does not always hold a literal level. It uses a relative-encoding
scheme:

```text
value <= 99    -> literal/fixed level (the unit's level is exactly this value)
value >= 100   -> relative to the player party's highest-level character:
                  effective level = (highest party member's level) + (value - 100)
                  value == 100 means "exactly match the party's highest level" (offset 0)
```

Worked examples:

```text
value = 1    -> fixed level 1 (a story-locked low-level guest, e.g. Delita at a vanilla Lv2 join)
value = 100  -> effective level = highest party level + 0   (the common "scale to party" case)
value = 102  -> effective level = highest party level + 2
value = 99   -> fixed level 99 (NOT relative — 99 is still in the "literal" range)
value = 254 (0xFE) -> the conventional "use save level" sentinel for a unit whose level is
                       expected to come from elsewhere (typically a player-controlled unit
                       already in the roster, using their saved level instead of this byte)
```

This conversion happens at unit-instantiation time and is **team-agnostic**: the same `>=100`
relative-encoding rule applies whether the slot is read as an enemy or as a guest/ally. Team
membership affects AI control and war-trophy/spoils accounting, not how the Level byte itself is
interpreted.

Important exception: scripted transform/phase bosses may not use the visible ENTD slot as the final
fighting actor. For those battles, the ENTD slot should still carry the intended relative level for
documentation/tooling/rewards, but the post-transform live actor can require a runtime actor-table
level patch. See [11-transform-boss-runtime-scaling.md](11-transform-boss-runtime-scaling.md). Do
not write ENTD syntax (`104`) into the live actor table; live level bytes are already-expanded
`1..99` values.

### Practical consequence for guests specifically

A guest slot's Level byte commonly ships as one of three patterns:

- **`254` (0xFE)** — "use save," the same sentinel a player-controlled unit uses. For a guest who
  has not yet joined the roster, this does not resolve to "party level" the way `100` would; it
  is the pattern most associated with guests that render at an unintended low default level
  (e.g. a vanilla Lv1 fallback) if left unpatched.
- **A fixed low value (`1`-`99`)** — a hardcoded, low, story-appropriate level for that
  appearance (e.g. a vanilla early-game guest fixed at level 2).
- **`>=100`** — already party-relative; no patch needed.

Both the `254` and fixed-low forms are the ones that need a level patch (set to `100`, or
`100 + small offset` to place a guest slightly above party level) to make a guest scale with an
NG+ or late-game party; the `>=100` form already does so by construction.

## Flags/control byte (`0x18`)

`0x18` (named `Flags2` to disambiguate from the unrelated `Flags` byte at `0x01`) is the
control/team flags byte. This project's shipped code calls it `SLOT_CONTROL_FLAGS` and reads/
writes it for every guest-scaling and team decision it makes.

Confirmed bits:

| Bit | Mask | Name | Meaning |
|---|---|---|---|
| 7 | `0x80` | AlwaysPresent (LoadFormation) | Unit is present and visible from the very start of the battle, including any pre-battle tactical-view intro/cutscene. Set on ordinary enemies, on every "guest" pattern surveyed, and on scripted allies. |
| 4 | `0x10` | "Enemy team" bit | See the discriminator caveat immediately below — this bit is **not** a clean enemy/ally signal on its own. |
| 3 | `0x08` | PlayerControl | Unit is player-controlled. This project's `ScaleGuestsAlways()` ORs this bit on for guest slots that are not on the enemy team, making them controllable without disturbing any other bit. |
| 0 | `0x01` | (seen set on some player/ally-initialized slots) | Observed set on the player-controlled init slot and on at least one scripted-ally slot; not independently decoded beyond "appears on player/ally-side units in some configurations." |

Bits `0x20`/`0x40`/`0x02`/`0x04` are not fully decoded for this binary's layout. (Classic PSX-era
FFT documentation describes a richer team scheme at this general position — `0x40` Randomly
Present, team pairs `0x20`/`0x10` for Blue/Green/LightBlue/Red, `0x04` Immortal — but this
project's own empirical byte scans across this binary format have only independently confirmed
`0x80` (AlwaysPresent), `0x10`, `0x08`, and `0x01` as listed above; treat the classic-FFT bit
names beyond those four as an unverified cross-reference, not a confirmed fact about this
specific binary.)

One empirical fact about `0x40` IS confirmed (in-game, Zaland entry 407 s8, 2026-07-02): **a
MODDED, newly-added slot whose flags carry `0x40` never materializes in battle** — the same slot
byte-identical except flags `0xD0 → 0x90` spawns normally. The best-supported reading of WHY
(supersedes the classic "Randomly Present" cross-reference, which the data initially resembled) is
**script-managed presence**: every `0xD0` unit in Zaland (407) is `AddUnit`-registered and
choreographed by that battle's intro script `event140.e` (two registration brackets, warp →
fade-in → pose records), so a `0x40`-flagged unit exists only if the battle's `.e` file registers
its uid — which a modded uid never is until the script is patched. Vanilla distribution fits:
`0xD0` is a minority value on units with staged entrances (385 s4–s6, 397 s5, 401 s6–s7);
Tchigolith 410's uid-sharing variant slots are `0x50`. Consequence for adds: either avoid `0x40`
entirely (a `0x90` static add — spawns, but stands outside any intro choreography), or match the
siblings' `0xD0` AND register/choreograph the new uid in the right `.e`
(the full-parity route; Zaland implementation pending playtest). See
[10-event-scripts-and-the-e-files.md](10-event-scripts-and-the-e-files.md).

### Caution: `0x10` ("enemy team bit") is not a clean enemy/ally discriminator

A bit-level survey of documented flags-byte values across multiple battles found `0x10` set on
both enemy slots and on shipped, documented **friendly** guest slots:

| Unit | Flags (`0x18`) | Bits set | Team in practice |
|---|---|---|---|
| Argath (guest, before a level patch) | `0x84` | `0x80`, `0x04` | guest/ally |
| Argath (guest, after a level/control patch) | `0x8C` | `0x80`, `0x08`, `0x04` | guest/ally, player-controlled |
| Agrias (scripted ally) | `0x89` | `0x80`, `0x08`, `0x01` | ally |
| Mustadio (guest) | `0x91` | `0x80`, `0x10`, `0x01` | **ally**, despite `0x10` set |
| Unidentified Goug ally guest | `0x91` | `0x80`, `0x10`, `0x01` | **ally**, despite `0x10` set |
| A failed always-present clone attempt | `0x90` | `0x80`, `0x10` | (intended enemy; visually broken for unrelated sprite-preload reasons) |
| Generic wave-reinforcement enemies | `0x10` | `0x10` only, no `0x80` | enemy |
| Generic always-present enemy | `0x80` | `0x80` only | enemy |

`0x10` is set on at least two shipped, documented friendly guest slots (Mustadio, the Goug ally)
in addition to ordinary enemy slots. **Do not use `(flags & 0x10) != 0` in isolation as "this
slot is an enemy."** This project's own shipped code does not make that mistake: its guest/team
logic decides guest-ness from the CharId/MainJob signature first (see the detection rule below),
and only consults `0x10` afterward, to decide whether to also grant player control to an
already-identified guest — never to decide team membership for an arbitrary slot.

The one bit that consistently correlates with "this is a recognized ally/guest unit the runtime
guest-scaler will touch" is the combination of `0x80` (AlwaysPresent) plus the CharId/MainJob
signature described below — not `0x10` in isolation, and not `0x80` in isolation either (`0x80`
alone is also set on ordinary always-present enemies).

## Guest vs. enemy vs. player-controlled detection rule

Three distinct kinds of slot exist, and they are told apart by different signals — no single byte
answers "what kind of unit is this":

```text
Player-controlled unit (uses the save, not this slot's Level byte):
  Level byte is conventionally 254 (0xFE), a "use save" sentinel.
  Typically the slot initialized for the protagonist/roster member already under player control.

Guest (named ally, level/control determined by this slot but not a permanent roster member yet):
  CharId (0x00) is a known named-character id, AND
  MainJob (0x0A) == CharId (0x00)
  i.e. "a unit in GUEST form has MainJob == CharId."
  This is the operative, code-confirmed rule: this project's shipped guest scaler computes
  isKnownGuest = (charId is in the known-guest-id set) && (job == charId), and only ever
  touches a slot when both hold.

Enemy (including a named character's enemy/boss form):
  Either CharId is a generic/non-named value, OR
  CharId is a named id whose MainJob has been re-jobbed away from CharId (MainJob != CharId).
  Example: a named character who is a guest ally earlier in the game can return later as a
  boss with the SAME CharId but a re-jobbed MainJob (e.g. re-jobbed to Knight) — that
  MainJob != CharId mismatch is what correctly excludes the boss form from guest-scaling logic
  while still scaling the earlier guest-form appearances of the identical CharId.
```

This MainJob == CharId guard is load-bearing in practice: several named characters use the
**same** CharId for both their guest and enemy/boss appearances, distinguished only by whether
MainJob has been changed away from CharId for the boss fight. A detection rule based on CharId
alone, without the MainJob comparison, would incorrectly classify a boss fight as a guest
appearance (or vice versa).

The `0x18` AlwaysPresent bit (`0x80`) does not distinguish guest from enemy — it is set on both,
since both are commonly present from turn 1. The `0x10` "enemy team" bit does not reliably
distinguish them either, per the caution above. The CharId/MainJob comparison is the rule that
this project's shipped code actually relies on.

### Known guest CharId set (as shipped)

The specific CharId values this project's code recognizes as guests (subject to the
MainJob == CharId guard above) include `0x04`, `0x07`, `0x0c`, `0x0d`, `0x15`, `0x16`, `0x17`,
`0x19`, `0x1e`, `0x1f`, `0x22`, `0x24`, `0x2a`, `0x30`, `0x32`, `0x34`, `0x48`. This list is
specific to which characters this project has identified and chosen to scale; it is a curated
set, not a derivation of "every guest in the game," and battles using a named-guest CharId outside
this set would not be recognized by the shipped code as-is.

## Caution: a recurring one-byte miscounting trap in this format

A specific, easy-to-repeat mistake when re-deriving this slot layout from a struct definition
(e.g. a third-party tool's field list) is **silently undercounting a multi-byte field as a single
byte**, which shifts every subsequent field's reported offset by one and produces a layout that
is wrong in a way that is hard to notice by inspection.

The concrete failure mode: `Reaction` (`0x0C`), `Support` (`0x0E`), and `Movement` (`0x10`) are
each **2-byte** fields (`short`), not 1-byte fields. A field list that treats all three as 1 byte
each undercounts by 3 bytes total across that span. If a *second*, unrelated error elsewhere in
the same field list happens to add a byte back (for example, mistakenly treating a later 1-byte
field as 2 bytes), the cumulative offset can drift back into alignment by coincidence — meaning
some downstream fields (e.g. `UnitID` and beyond) land back on their correct absolute offset even
though the offsets in between are wrong. This makes the bug easy to miss on a quick sanity check
that only spot-checks a few fields rather than re-deriving the whole struct from scratch.

The concrete, previously-observed consequence of this exact miscount: a field list affected by it
mislabels `Flags2` (`0x18`, the real control/team flags byte) as `X` (a position coordinate), and
correspondingly mislabels `X` (`0x19`, the real position byte) as `Y`. Anyone re-deriving this
struct from a third-party source and arriving at "the control/team byte is actually at `0x18`-1"
or "`0x18` is a position coordinate, not flags" has, with very high probability, reproduced this
exact one-byte miscount rather than found a genuine correction — this exact wrong reading has
recurred independently at least twice in this project's own research history, each time traced
back to the same root cause (a struct field list that silently treats a 2-byte field as 1 byte).

The reliable check against this trap: re-derive the field list's cumulative offsets by hand from
field sizes (not by trusting a tool's reported offsets directly), and confirm the struct's total
size matches the known slot size (`0x28` bytes) with zero unaccounted gap. A struct that
"normally" sums to `0x28` only because two separate errors happened to cancel is not a sufficient
check — verify every multi-byte field individually.
