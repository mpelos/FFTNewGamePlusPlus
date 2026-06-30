# Scaling guests (Delita & co.) to the player's level

Date: 2026-06-19

## Problem

In New Game+, guest/ally units (Delita early on, later story guests) show up at their
original fixed low levels, making them useless next to a carried-over high-level roster.
Goal: make guests enter at the player's highest character level the moment they appear.

## Core finding: controlled vs guest vs enemy

The ENTD Level byte uses the relative encoding (`>99` = highest party level + (value-100)).
That conversion happens when the unit is instantiated from ENTD and is **team-agnostic** —
team only decides AI control / war-trophy counting, not how the Level byte is read.

BUT there is a split that matters:

| Unit kind | Level source | Patch needed? |
|-----------|--------------|---------------|
| Player-controlled story unit (forced Ramza, units already in your roster) | your SAVE | No — already your level |
| Guest / AI ally (Green team) | ENTD Level byte (fixed) | YES — this is what stays low |
| Enemy (Red team) | ENTD Level byte | already handled |

So the fix for a guest = set that guest slot's Level byte to `100` (= party level), same tool
and same encoding as enemies. Must confirm with one in-game test on a real guest.

## Gariland (entry 388) inspection — important

Vanilla entry 388 raw dump shows only:

```
slot 0: charId 0x04, level 1, flags 0x89 (Always Present 0x80 | Control 0x08 | Ramza-init 0x01), Blue team
slots 1-5: charId 0xFF (generic), enemies
slots 6-15: empty
```

- Slot 0 is the **player-controlled Ramza** (Control + Blue), so its level 1 byte is ignored;
  it uses the save. Leaving it untouched was correct.
- **Delita (guest) is NOT a slot in entry 388.** In the remaster the Gariland guest is injected
  by something other than this ENTD entry (event/scenario script, or a separate guest/entry
  table). We must locate where guests are defined before we can scale them.

## ENTD flag/team semantics (classic FFT reference)

Flags byte: `0x80` Always Present · `0x40` Randomly Present · team bits `0x20`/`0x10`
(none = Blue/player, `0x20` = Green/guest-AI, `0x20|0x10` = Light Blue, `0x10` = Red/enemy)
· `0x08` Control · `0x04` Immortal · `0x01` set by Ramza on init.

NOTE: the TIC `battle_entd*_ent.bin` binary does NOT lay out bytes the same as classic PSX.
In our dumps, byte1 is not the classic Flags byte (enemies show 0x80/0x40 = looks like
gender, not team). The reliable per-unit markers we DID see in TIC:
- byte 0x02 = character/name id (`0xFF` = generic, low value = named special/guest/boss)
- byte 0x21 = in-battle unit id (`0x04` for the controlled story unit, `0x80..0x85` for the
  five generic enemies — high bit looks tied to enemy side)
- byte 0x03 = Level (validated in-game)

The exact TIC team byte still needs to be pinned down by comparing a battle that has a known
guest.

## Plan to scale guests systematically

1. **Find where guests live.** Two candidates:
   - Scan all ENTD entries for slots with a named charId (byte 0x02 not 0xFF/0x00) that are
     allies (not the controlled protagonist, not enemies) → surfaces guests + named bosses.
   - Check `OverrideEntryData` and the event/scenario tables (`EventId`, `ScenarioId`,
     `Chapter`, `GameProgress`) in `enhanced_0004.sqlite` for guest unit definitions.
2. **Pin the TIC team byte** by diffing a confirmed-guest battle against Gariland.
3. **Confirm the mechanic on one guest** (set its Level byte to 100, test in-game that it
   scales like the enemies did).
4. **Roll out**: for every battle a guest appears in, set the guest slot Level to 100
   (or `100 + small offset` if we want guests slightly above party).
5. **Permanent joiners** (Agrias, Mustadio, etc.) become player-controlled when they JOIN —
   they then use save level, but they may JOIN at a low level. That join level is a separate
   mechanism (recruit/join routine) and is tracked as a follow-up, distinct from guest scaling.

## Tooling

`tools/entd_tool.py patch-levels` already patches any slot's Level byte, so once we know the
guest's entry+slot, scaling a guest is identical to scaling an enemy. A future helper could
auto-scan ENTD for guest slots.

## CONFIRMED FINDINGS (data scan, 2026-06-19)

Ran a full scan of all 4 ENTD files (`tools/guest_scan.py`). Results:

### Team byte (TIC binary)
- **Byte `0x18`, bit `0x10`**: SET = enemy (Red team); CLEAR = ally/guest/player.
  Verified: in entry 384 allies show `0x84`, enemies `0x90`; consistent across entries.
- Char id is byte `0x02` (`0xFF` = generic enemy, low value = named character).
- In-battle unit id is byte `0x20` (`0x80+` for generic enemies).

### Character ids (inferred from appearance pattern)
- `0x01` = Ramza (later chapters), `0x04` = Ramza (Chapter 1), **`0x07` = Delita (Chapter 1)**.
- These appear together as allies in the early entd4 entries (384-395 = early Chapter 1 area).

### Level encoding for ally/guest slots — the key nuance
Each ally slot's Level byte (0x03) is one of:
- **`254` (0xFE) = default/use-save.** Player-controlled units (Ramza, joined roster chars)
  use the save level here — correct, no fix needed. BUT guests with `254` appear to fall back
  to a low default in NG+ (this is likely why Delita shows up weak).
- **`1`-`99` = fixed low level.** e.g. entry 389 slot 1 = Delita at **level 2** (likely
  Mandalia). These are the clearest "stuck low" guests.
- **`>=100` = already party-relative** (rare in story data).

Delita (0x07) histogram: 18× default(254), 1× fixed(level 2 @ entry 389).
So the guest problem has TWO forms to handle: fixed-low (set to 100) AND default-254 guests
(need an in-game test to see whether 254 must be overridden to 100 to scale).

### Important: Gariland (388) has NO Delita
Entry 388 = Ramza (0x04, controlled, level byte ignored) + 5 generic enemies only. Delita is
NOT in the Gariland battle in this version. He first appears as a fixable guest in entry 389.

### Master list
`tools/guest_scan.py` prints all 125 named-ally occurrences with fixed levels — the candidate
list for systematic guest scaling. (Note: list also includes named bosses temporarily on the
ally side and special joinable characters; filter by intent when rolling out.)

## NEXT: isolated in-game test (Delita)
Created `work/battle_entd4_ent.delita389-test.bin` — ONE byte changed vs original
(offset 0x00CAB: Delita level 2 -> 100, entry 389 slot 1). Deploy this single-change file and
start the entry-389 battle (likely Mandalia) with a high-level NG+ party:
- If Delita enters near party level -> guest scaling via the Level byte is CONFIRMED, and we
  roll it out (fixed-low first, then test a 254 guest).
- If not -> guests use a different mechanism (event/recruit routine) and we investigate that.

Deploy command (replaces the active mod bin — note this reverts the Gariland finalshop edit,
so it's a clean isolated test):
```
Copy-Item work\battle_entd4_ent.delita389-test.bin mod\fftivc.battles.rescale\FFTIVC\data\enhanced\fftpack\battle_entd4_ent.bin -Force
# then copy mod into C:\Reloaded-II\Mods and launch via Reloaded-II
```

## DEAD END: guest level is NOT in editable unit tables (2026-06-19, in-game verified)

Tested in-game: Gariland (entry 388) enemy edits DO load (enemies changed), but the guest
**Delita still shows Lv 1**. Investigation:

- Gariland is confirmed = ENTD entry **388** (enemies changed in-game).
- Base ENTD 388 = Ramza (controlled) + 5 generic enemies. **No Delita slot.**
- `OverrideEntryData` Key=388 = 6 rows (slots 0-5), ALL `Level=-1` (no override), no Delita.
- Across the ENTIRE NXD database, only `GeneralJob` and `OverrideEntryData` have a Level
  column. `Chara` has NO level field.
- `OverrideEntryData` uses a real Level override in only **6 rows total** (battles 387, 419) —
  never for Gariland's guest.

**Therefore: the Gariland guest (Delita) is injected and leveled by the EVENT/SCENARIO system,
not by the battle's unit data (ENTD / OverrideEntryData).** Editing the ENTD level byte cannot
reach this guest. (Note: entry 389's Delita is a different, real ENTD guest slot — that patch
is still valid for whatever battle 389 actually is, but it is NOT the Gariland guest.)

### Where to look next for guest levels
- Event/scenario data — likely in a different `.pac` than 0002(fftpack)/0004(nxd) we extracted,
  or in event script files. Need to extract & search for the Gariland event that spawns Delita.
- Possibly hardcoded in `FFT_enhanced.exe`.
- Research whether the community (FFHacktics / Nexus) has cracked guest/event unit leveling in
  TIC.

## BREAKTHROUGH: guests live in `event_btlevt_bin_entrydata_add_ent.bin` (2026-06-19)

The Gariland event (EventId 9) only has 4 trigger opcodes in `EnhancedBattleEvent` — none place
units; they point to an external battle-event script. The units that EVENTS ADD to battles
(i.e. guests) are in a separate fftpack file we already had extracted:

**`fftpack/event_btlevt_bin_entrydata_add_ent.bin`** — 49280 bytes, SAME structure as ENTD
(0x28-byte unit records, 16 per 0x280 "entry", **level byte at 0x03, same `>99 = party level`
encoding**). This is the "entry data ADD" layer = event-injected units.

Proof the mechanic works here: later-battle guest records in this file ALREADY use relative
levels (102, 105) and fixed (99) — the game itself scales guests via this file. The early ones
(e.g. Ch1 Delita) are left at `254` (default) → render as level 1 in NG+.

### Delita records in the add-file
| rec | off | entry/slot | sprite | level | note |
|-----|-----|-----------|--------|-------|------|
| 98 | 0x00F50 | e6 s2 | 0x07 | **254** | Ch1 squire Delita (Gariland/early) — the stuck-at-1 guest |
| 112 | 0x01180 | e7 s0 | 0xA5 | 40 | Ch2+ Holy Knight Delita |
| 931 | 0x09178 | e58 s3 | 0x07 | 99 | later |
| 1216| 0x0BE00 | e76 s0 | 0x07 | 99 | later |

### Test deployed (clean, isolated)
- entd4 bin reverted to Gariland-finalshop-only (enemies only; no ENTD Delita experiments).
- add-file: rec 98 level byte `0x00F53` set `254 -> 100` (1 byte).
- Mod must now ship BOTH fftpack files: `battle_entd4_ent.bin` + `event_btlevt_bin_entrydata_add_ent.bin`.
- If Gariland's Delita now enters at party level -> THIS FILE is the guest source, and we scale
  all guests by editing it (map each add-file entry to its battle, set level to `100 + offset`).

### How to map add-file entries to battles (next, if test passes)
Need to correlate the 77 add-file entries to events/battles (likely via the external battle-event
script `event_btlevt_bin.bin`, or by testing). Then build a guest-scaling pass over the add-file
analogous to `guest_scan.py`.

## BREAKTHROUGH #2: the fingerprint method + corrected identities (2026-06-19)

The add-file (rec 98) change had NO in-game effect (verified inside the live modded.pac).
So I searched ALL fftpack bins for Delita's on-screen stats as a fingerprint:
**Bravery 71 (0x47) + Faith 55 (0x37)** adjacent (ENTD layout: bravery@+0x06, faith@+0x07).

Exactly ONE match in the whole fftpack:
**`battle_entd4_ent.bin`, entry 392, slot 1, charId 0x04, level 1, bravery 0x47, faith 0x37.**

This is the on-screen Delita. Consequences:
- **Identities were swapped:** `charId 0x01 = Ramza`, **`charId 0x04 = Delita`** (not the
  reverse as earlier assumed).
- **The real Gariland-with-Delita battle is ENTD entry 392**, NOT 388. Entry 392 =
  Ramza(0x01) + Delita(0x04) + generic squire/chemist enemies (jobs 0x4A/0x4B/0x4C) — the
  classic Gariland shape. Entry 388 (Delita-controlled + 5 enemies) is likely a different
  battle (prologue/cutscene); the old "388 = Gariland" mapping is suspect.
- The guest level WAS in the base ENTD all along — just in a different entry. No event/save
  decoding needed.

### Fingerprint method (reusable)
To locate any on-screen unit's data record: read its Bravery/Faith from the status screen,
convert to hex, search the ENTD bins for that adjacent byte pair; the level byte is 3 bytes
before bravery (record+0x03).

### Fix deployed (mod v0.5.0)
- entd4: entry 388 finalshop (kept) + **entry 392 slot 1 (Delita) level 1 -> 100** (offset 0x0142B).
- add-file removed from the mod (it was not the source).
- PENDING in-game test: does Delita now scale at the entry-392 battle?
- Also to confirm: which entry holds the real enemies the player sees (388 vs 392).

## ✅ CONFIRMED SOLUTION (2026-06-19) — guest scaling WORKS

Setting **entry 392 slot 1 (Delita, charId 0x04) level 1 -> 100** made Delita enter at the
party's level. Guest scaling via the base ENTD level byte is CONFIRMED.

### CRITICAL GOTCHA: guests are cached in the SAVE on join
A guest joins (and is written to the save) in a cutscene BEFORE his first battle. If your save
already has the guest, he keeps the OLD level — our ENTD edit only affects him at the moment he
JOINS. **To test/apply guest changes you need a save from BEFORE the join (or a new game).**
This is why earlier edits "did nothing": the test save already had Delita at level 1.

### The confirmed method to scale any guest
1. From the status screen, read the guest's Bravery + Faith (e.g. 71 / 55).
2. Fingerprint-search the ENTD bins for that adjacent byte pair (bravery@rec+0x06, faith@+0x07).
3. The match is the guest's record; level byte = record+0x03. Set to `100 + offset`.
   If the guest should have the full primary kit, job level byte = record+0x09. Set to `8`.
4. Test with a save from before the guest joins (or new game).

`tools/entd_tool.py patch-levels --entry <N> --slots <S> --level 100` applies it.
`tools/entd_tool.py patch-job-levels --entry <N> --slots <S> --job-level 8` applies the
companion JobLevel patch.

### Corrected identities
charId `0x01` = Ramza, `0x04` = Delita. (Use the fingerprint method, not charId guesses, to be sure.)

## Chapter 1 guests scaled (mod v0.6.0)

Reliable guest-vs-enemy rule discovered: **a special character in GUEST form has
`MainJob (slot+0x0A) == charId (slot+0x02)`**; the same character as an ENEMY uses a generic
combat job (e.g. Argath-enemy at Ziekden has job 0x4C, not 0x07). So filter guests by
`charId not in {0,0xFF} AND MainJob == charId`.

Chapter 1 human guests = **Delita (charId 0x04)** and **Argath/Algus (charId 0x07)**.
Scaled ALL their guest-form appearances across entd4 entries 384-401 to level 100 (27 records;
both fixed-level joins like e389 Argath L2, e392 Delita L1, and the 254/default appearances —
robust against the save-cache-on-join behavior regardless of which entry is the true join).
Argath-as-enemy (e401, job 0x4C) correctly excluded.

2026-06-29 follow-up: Delita's pre-Gariland join record also needs the full guest-job kit.
Patched **entry 392 slot 1 JobLevel `1 -> 8`** at byte `0x01431`. This follows the same
save-cache rule as the level patch: verify from a save before Delita joins, or from a fresh NG+
start.

NOT scaled: Ramza (0x01) — he is the player's main (uses save level), not a guest.
TODO: Boco (Ch1 chocobo guest) not found as a named job==charId record in the ENTD — likely
joins via event or as a generic monster; investigate if guest chocobo scaling is wanted.

## Sources
- ENTD flags/team bits: FFHacktics wiki (Extra Battle Stats / ENTD).
  https://ffhacktics.com/wiki/Extra_Battle_Stats , https://ffhacktics.com/wiki/ENTD
- Story battles use fixed levels; guests predetermined: community + walkthroughs.
  https://gamefaqs.gamespot.com/boards/197339-final-fantasy-tactics/52397740
- Level relative encoding (>99 = party level + value-100): https://ffhacktics.com/wiki/ENTD
- Local data: extracted/enhanced_0002_selected/fftpack/battle_entd4_ent.bin (entry 388),
  work/enhanced_0004.sqlite

## ROOT CAUSE of the wrong-job JobLevel seed (2026-06-29) — byte 0x08 = job-seed INDEX

The join JobLevel (byte **0x09**) is paired with byte **0x08 = the GENERIC JOB INDEX** it applies to.
Proven by the generic-enemy data across entd4: a generic unit's `0x08 == (mainJob 0x0A) - 0x4A`, i.e.
Squire(0x4A)=0, Chemist=1, Knight=2, Archer=3, Monk=4, WhiteMage=5, BlackMage=6, TimeMage=7 … — the
SAME indexing as the save's per-job level/JP arrays (see `tools/fft_save_patch_delita.py`).

For a NAMED guest, `0x08 = 0` makes the JobLevel apply to the unit's **main/displayed job**. EVERY
working named guest uses `0x08 = 0`: Ovelia `0x08=0 / 0x09=6` → "Princess Lv6" (confirmed in-game);
Gaffgarion, Agrias, Mustadio all `0x08=0`. **Delita was the lone exception** — his `0x08` had been set
to `1` (Chemist) [earlier `7` = Time Mage], so the Lv8 seed landed on Chemist/Time Mage, never Squire.

**FIX (Claude, 2026-06-29):** Delita join records (entries **388 s0, 389 s0, 392 s1**) byte `0x08`
set `1 → 0` (keep `0x09 = 8`). His JobLevel 8 now applies to his main Squire job (`0x0A = 4`), like
Ovelia's. ✅ CONFIRMED in-game 2026-06-29 (tested from a pre-join save / new game — Delita joins **Squire Lv8**); originally written as PENDING playtest from a **pre-join save / new game** (save-cache-on-join: a Delita already
in the save keeps the old bugged data — this is why the autosave-edit test "did nothing").

**Open items:**
- **NG+-only.** The seed rides the Layer-1 `.bin` swap (incl. the slice reads for Delita's join),
  which is NG+-gated. The always-on `ScaleGuestsAlways` sets level + control bit but NOT the job seed
  (the `Program.cs` constants `SLOT_JOB_UNLOCK=0x08` / `SLOT_JOB_LEVEL=0x09` are defined but UNUSED).
  To give Delita Squire Lv8 in normal play too, wire those into `ScaleGuestsAlways` (set 0x08=0,
  0x09=8 for the ally guest), same as the level/control patch.
- **Argath (charId 0x07 @ entry 389 s1) has the identical `0x08=1` bug** — not yet fixed.
- The `tools/fft_save_patch_delita.py` band-aid (retro-fix an already-joined Delita in the save PNG)
  is moot for new playthroughs once the join seed is correct.
