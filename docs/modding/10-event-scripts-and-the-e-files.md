# Adding an enemy — the playbook (start HERE)

The single entry point for adding a unit to a battle: the decision tree, every tool and path, how
to find the battle's event script, and the validated recipes. Deep references: `01` (ENTD bytes),
`03` (opcodes), `04` (event-spawn recipe), `08` (OverrideEntryData), `09` (sprite budget).

Validation status is marked per claim: **[VALIDATED]** = confirmed in-game; **[PENDING]** =
implemented, awaiting playtest; **[HYPOTHESIS]** = best reading of the data.

## The mental model (what gates a unit's existence)

A battle unit can be delivered by one of two mechanisms, chosen per-slot by the ENTD flags byte
(offset 0x18):

| Slot flags | Delivery | Who makes it exist | Example |
|---|---|---|---|
| `0x80` set, `0x40` clear (`0x90`, `0x80`, `0x84`…) | **Static** | The engine, directly from the ENTD at load | Gariland/Zeirchele enemies |
| `0x40` set (`0xD0`, `0x50`, `0xC4`…) | **Script-managed** [HYPOTHESIS, strong] | The battle's `.e` event script: `AddUnit` registration + choreography | Zaland/Balias Swale enemies, Dorter Slums s4-s6 |
| `0x10` only, no `0x80` | **Delayed wave** (script-managed subtype) | Same as above, revealed mid-scene | Merchant Dorter ambush |

**[VALIDATED]** consequences of getting this wrong:
- An added slot cloned with `0x40` in its flags **never materializes** — the script doesn't know
  the new uid (Zaland 407 s8 as `0xD0`: absent, even with its OverrideEntryData row).
- Forcing that slot to `0x90` makes it spawn, but **outside the intro choreography**: visible from
  frame 0, playing its default walk animation while the scripted units hold poses (Zaland, user
  rejected as final state).
- A wave add without script registration is a ghost: its fields update but it never activates
  (Merchant, actor-table proof — doc `04`).
- Full parity for a `0xD0`-convention battle = `0xD0` + `AddUnit` registration + entrance
  choreography in the right `.e` [PENDING — Zaland `zaland-script-parity-v1`].

## Decision tree

```text
Want a different role, same enemy count?
└── JOB-SWAP an existing slot (doc 06). No script work, no new uid. Done.

Want one MORE enemy?
├── 1. Dump the entry (see Paths). Note: sibling flags convention, free uid,
│      story slots (lvl 254 — never repurpose), sprite budget headroom.
├── 2. Sprite budget: python tools/sprite_budget.py <entry>   (net +1 sheet max, doc 09)
├── 3. Are the siblings 0x40-flagged (0xD0/0x50) or 0x10-wave?
│      python tools/scan_event_units.py <sibling uids>  → which .e registers them
│   ├── NO (0x90/0x80 static, uids in no AddUnit bracket)
│   │   └── RECIPE A (static): ENTD-only. [VALIDATED 4x]
│   └── YES (uids registered in a .e)
│       └── RECIPE B (script-managed): ENTD + .e patch. [Merchant VALIDATED; Zaland PENDING]
└── 4. Either way: finish with the Verify & deploy block, then ONE playtest.
```

## Paths map

| What | Where |
|---|---|
| Modded ENTD (story battles, entries 384-511) | `src/fftivc.battles.ngplus/entd/battle_entd4_ent.bin` — **EMBEDDED in the DLL**: every edit needs `dotnet build` |
| Vanilla ENTD extract (diff baseline) | `extracted/enhanced_0002_selected/fftpack/battle_entd4_ent.bin` |
| Vanilla event scripts (560 files, extracted from `0005.pac`) | `tmp/pac0005/script/enhanced/event<NNN>.e` |
| Mod's loose overrides — event scripts | `src/fftivc.battles.ngplus/FFTIVC/data/enhanced/script/enhanced/` (shipped: `event119.e` Merchant, `event140.e` Zaland; `event129.e` intentionally vanilla) |
| Mod's loose overrides — NXD tables | `src/fftivc.battles.ngplus/FFTIVC/data/enhanced/nxd/` (`overrideentrydata.nxd` + `root.nxl` — row count in both MUST match) |
| Deployed mod (build output target) | `C:\Reloaded-II\Mods\fftivc.battles.ngplus\` (same relative layout; loose files need no DLL rebuild but the build copies them too) |
| Vanilla NXD as SQLite (inspection) | `work/enhanced_0004.sqlite` (table `overrideentrydata`) |
| Investigation journals (pre-validation notes — never in docs/) | `work/YYYYMMDD-*.md` |

## Tools map

| Tool | Use it to |
|---|---|
| `tools/battle_patch.py <battle>` | Author every ENTD change (`set_slot`, `clone_slot`, `set_control_flags`, `set_position`, `restore_vanilla_slot`). Deterministic; prints the byte-diff containment. |
| `tools/scan_event_units.py <uids...>` | Find which `.e` files register given uids in `AddUnit` brackets — the static-vs-script classifier and the first step of finding a battle's script. `--all` dumps every bracket. |
| `tools/audit_slot_adds.py` | The mechanical gate before any playtest: diffs modded-vs-vanilla ENTD and ERRORs on added slots carrying `0x40`, root.nxl/NXD count mismatch, uid collisions; warns on missing NXD rows / wave adds. |
| `tools/sprite_budget.py <entry>` | Net-new-spritesheet count vs vanilla (doc 09 rule: max +1). |
| `tools/validate_ch2_v2.py` | Chapter regression suite (ENTD bytes + patched script markers + root.nxl). Add checks for every new change. |
| `tools/patch_event140_zaland.py` | Deterministic, hash-guarded `.e` patcher — **the template for every future script patch**: pristine-hash guard, context-guard bytes at each insertion offset, end-first insertion, fixed output size. |
| `tools/FF16Tools.CLI-…/FF16Tools.CLI.exe` | `nxd-to-sqlite` / `sqlite-to-nxd -t OverrideEntryData` (case-sensitive `-t`). Roundtrip is byte-faithful — prove it by hashing a no-op roundtrip first. |

## How to find a battle's event script (in confidence order)

1. **Offline uid-profile match (minutes, usually enough):** the battle's `.e` references its exact
   cast. Scan for the ENTD uid set (generics `0x80+` AND the named cids like `0x22`/`0x34`):
   `python tools/scan_event_units.py 0x80 0x81 0x82 0x83 0x84 0x85`, then profile the hits — the
   right file references (nearly) ALL of the battle's uids and no foreign ones. Zaland: only
   `event140.e` matches 0x22+0x02+0x34+0x80-0x85 (with 0x22 doing a 10-record chase — the intro).
2. **Numbering shortlist:** story-battle scripts run roughly linearly — confirmed anchors:
   `403 → event119`, `405 → event129`, `407 → event140` (~5 files per battle step). Use only to
   shortlist candidates for method 1, never as proof.
3. **Authoritative proof — runtime file-access log:** Reloaded-II `LogGeneralFileAccesses: true`,
   `GeneralFileAccessType: "AllFiles"` (config path + how-to in doc `07`), load the battle / let
   the trigger moment play, and grep the log for `script/enhanced/event<NNN>.e` at that timestamp.
   **This is the only proof.** The Merchant NXD join named `event298.e` and every patch to it was
   silently inert; the real file (`event119.e`) was found only this way. If a script patch
   produces zero visible change, assume wrong-file until this log says otherwise.

## Recipe A — static add (siblings are `0x90`/`0x80`) [VALIDATED: Gariland 388 s6, Araguay 404 s9, Zeirchele 405 s11, Zaland-as-0x90]

1. `clone_slot(data, E, <active sibling>, <free slot>, unitid=<next free uid>, x=…, y=…)` in
   `battle_patch.py`, then `set_slot` to retune job/level/gear.
2. Flags: keep/force `0x90` (`set_control_flags`) — never let a `0x40` bit through.
3. OverrideEntryData row `(entry, slot)` cloned from one of THAT battle's active-enemy rows
   (match `Unknown64`; `Unknown9C=0`) + `root.nxl` count +1 (doc `08` steps 5-8). Current shipped
   practice; necessity never isolated [HYPOTHESIS] — keep shipping it until a row-removal test.
4. Verify & deploy block below.

Cosmetic cost in intro battles: the unit stands outside the intro choreography (visible early,
default animation). Acceptable for battles without a staged entrance; for full parity in a
choreographed intro, use Recipe B.

## Recipe B — script-managed add (siblings carry `0x40`, or wave `0x10`) [Merchant VALIDATED end-to-end; Zaland parity PENDING]

Everything in Recipe A steps 1/3/4, PLUS:

1. Flags: **match the siblings** (`0xD0` for a script-managed always-present battle; wave flags
   for a wave) — the script, not the flags, makes the unit exist.
2. Find the real `.e` (section above). Extract pristine copy, record size + sha256.
3. Patch the `.e` with a deterministic tool cloned from `tools/patch_event140_zaland.py`:
   - **Registration**: `45 <uid> 00 01` inserted inside the bracket that registers the unit's own
     wave-siblings, immediately before that bracket's closing `4A`. (A script can have several
     brackets — pick the wave-mates', doc `04` step 4.)
   - **Choreography**: mirror the siblings' entrance for the new uid. Two validated shapes:
     per-unit block copied verbatim and uid-retargeted (Merchant, doc `04` step 6), or phase-
     interleaved scripts (Zaland): insert a compact block (WarpUnit to the unit's tile +
     ColorUnit prep + Draw + ColorUnit fade + UnitAnim pose) at a record boundary right after the
     siblings' Draw records, plus the final idle `11 <uid> 00 02 00 00` next to a sibling's idle
     record. Opcode shapes/lengths: doc `03` table.
   - Insertion safety: whole records at record boundaries only; the format has no length/offset
     fields to desync (doc `03`); guard every insertion with pristine-hash + context bytes.
4. WarpUnit tile doubles as the unit's battle-start position (Merchant precedent) — pick valid
   ground that also works tactically; iterate visually if needed (doc `04` closing note).

## Verify & deploy (every change, before any playtest)

```powershell
python tools\battle_patch.py <battle>        # byte-diff must be contained to the intended entry
python tools\<script patcher>.py             # if Recipe B
python tools\audit_slot_adds.py              # zero ERRORs
python tools\validate_ch2_v2.py              # all checks pass (add checks for the new change)
$env:RELOADEDIIMODS='C:\Reloaded-II\Mods'; dotnet build .\src\fftivc.battles.ngplus\fftivc.battles.ngplus.csproj -c Release
```

Then verify the DEPLOYED artifacts, not the intent: read the entry back from the deployed DLL's
embedded resource (`GetManifestResourceStream`), hash the deployed loose files against source.
Playtest once, from a save BEFORE the battle, with full player deployment (doc `09`).
Document results in `work/` first; `docs/` only after the playtest confirms.

## Failure triage

| Symptom | First suspect | Validated by |
|---|---|---|
| Added unit absent; siblings `0xD0`/`0x50` | Script doesn't register the uid (or flags carry `0x40` without Recipe B) | Zaland |
| Added unit absent; battle static | DLL not rebuilt (embedded ENTD stale); then NXD row/root.nxl mismatch | multiple |
| Script patch changes nothing at all | Wrong `.e` file — go to file-access logging | Merchant (`event298` trap) |
| Unit present but fields-only ghost (never gets a turn) | Choreography without `AddUnit` registration | Merchant v1 |
| Unit visible from frame 0, walk-animating through the intro | Static-flagged unit in a choreographed intro | Zaland `0x90` state |
| Wrong sprite/portrait during intro only | `LoadFormation` preload fallback — sprite not loaded yet | Dorter early attempt |
| Guest palette-garbage after the add | Sprite budget exceeded | Zeirchele (doc `09`) |
| Unit on a roof/odd tile, otherwise fine | Warp/position operand | Merchant `(7,10)` |
| "Defeat all enemies" won't end / count off | Unit exists but shouldn't (or vice versa) — recount vs design | — |

## Per-battle track record (adds only)

| Battle (entry) | Add | Mechanism | State |
|---|---|---|---|
| Gariland (388) | s6 Thief `0x90` | static, no NXD row | ✅ shipped |
| Merchant Dorter (403) | s9 Knight `0x10` | wave: ENTD + NXD row + `event119.e` (registration + block) | ✅ shipped |
| Araguay (404) | s9 Coeurl `0x90` | static, no NXD row | ✅ shipped |
| Zeirchele (405) | s11 Knight `0x90` | static + NXD row `(405,11)` | ✅ shipped |
| Zaland (407) | s8 Dragoon `0xD0` | script-managed: ENTD + NXD row + `event140.e` parity patch | 🟡 PENDING playtest |
| Balias Tor (409) | s8 Chemist `0x90` | static (siblings `0x90`) | 🟡 not yet playtested |
| Tchigolith (410) | s9 monster `0x90` | ⚠ siblings include `0x50` variant slots; battle has ZERO NXD rows — classify via scanner before trusting | 🟡 audit flags it |
| Balias Swale (413) | s7 Geomancer `0xD0` | ⚠ same as Zaland: needs Recipe B (script patch) or it will not appear | 🔴 known-broken until treated |

## Open questions

- OverrideEntryData row necessity (never isolated — remove `(407,8)` or `(405,11)` on a green
  battle to settle it).
- `0x40` = "script-managed presence" is the best reading but rests on Zaland; the PENDING parity
  playtest is also its confirmation test.
- Whether an `AddUnit` bracket accepts more than one inserted uid per bracket (all patches so far
  added exactly one).
