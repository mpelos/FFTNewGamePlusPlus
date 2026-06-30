# Spoils of War — the per-battle reward system (and how to mod it)

**Status:** mechanism SOLVED, fix implemented, and validated end-to-end in-game (2026-06-26): the
modded Brigands' Den (entry 395) now drops authored spoils instead of vanilla. Also discovered a
**hard cap of 3 spoils per battle** (see "Hard cap" below).

## TL;DR

The post-battle **"Spoils of War"** items are **not** a separate reward table, **not** Move-Find
treasures, and **not** the enemy's live equipment. Each unit slot in the ENTD carries a **1-byte
"spoils item" field at slot offset `0x1e`**. The battle's spoils = **the set of all non-zero `0x1e`
bytes across the entry's 16 slots**. It is deterministic and **kill-independent** (you receive every
slot's `0x1e` item just by winning; you do not have to kill that unit — the boss slot is usually `0`).

Our code mod swaps the whole ENTD file in NG+ but only edits the **equipment** bytes (`0x12`–`0x16`).
It never wrote `0x1e`, which is why NG+ spoils stayed vanilla even though enemies fight with modded gear.

**The fix:** write the desired spoils into `0x1e` of occupied slots in the modded ENTD. No new hook,
no new file, NG+-only for free, and fully **decoupled from difficulty** (`0x12`–`0x16` = what the
enemy fights with; `0x1e` = what it drops).

**Hard limit:** a battle awards **at most 3 spoils items**. The engine takes the first 3 non-zero
`0x1e` bytes in slot order and silently drops the rest, so authoring more than 3 is wasted. Project
rule: never put more than 3 (see "Hard cap").

## The field

ENTD record = 128 entries/file × 16 slots/entry × `0x28` bytes/slot (files `battle_entd1-4_ent.bin`
in `0002.pac` → `fftpack/`). The spoils byte lives inside the per-slot tail our `entd_tool.py` had
left undecoded as `raw_tail`.

```
slot byte 0x1c = 0xFE          (sentinel)
slot byte 0x1d = 0xFF          (sentinel)
slot byte 0x1e = SPOILS ITEM   <-- item id of this slot's reward, 0 = none
slot byte 0x1f = ?             (unconfirmed; possibly base gil / 100 — see Open items)
slot byte 0x20 = unit instance id (0x80+, present on every slot)
```

Absolute file offset of a slot's spoils byte:

```
file       = global_entry // 128 + 1          # 1..4  -> battle_entd{file}_ent.bin
local      = global_entry %  128
offset_1e  = local * 0x280 + slot * 0x28 + 0x1e
```

## Hard cap: at most 3 spoils per battle

The engine awards **at most 3 spoils items per battle.** It scans the 16 slots in order, takes the
first 3 non-zero `0x1e` bytes, and **silently drops** any beyond that.

Confirmed in-game (2026-06-26): entry 395 (Brigands' Den) was authored with 5 spoils on slots 3-7
(Runeblade, Crystal Shield, Crystal Helm, Crystal Mail, Bracers). The Spoils of War screen showed
only the **three lowest slots**: Runeblade (s3), Crystal Shield (s4), Crystal Helm (s5). Slots 6-7
(Crystal Mail, Bracers) were dropped. This also explains the vanilla scan: **no vanilla battle ever
exceeds 3 spoils** (distribution 1:24, 2:13, 3:5).

**Design rule (project-wide): never author more than 3 spoils on a battle.** Put the 3 intended
items on the battle's 3 lowest-indexed occupied slots so none are lost. Gil is separate and not
subject to this cap. (Entry 395 was then consolidated to its best 3: Runeblade / Crystal Mail /
Bracers on slots 3-5.)

## Proof (the two in-game data points)

Both fought in NG+ on the current modded build (enemies confirmed modded: Milleuda was level 102 with
Runeblade + Crystal Shield in battle 1).

**Battle 1 — Brigands' Den, entry 395 (first Milleuda).** Vanilla `0x1e` per slot:

```
slot 2 (Milleuda, named boss)  0x1e = 0     -> no spoils token on the boss herself
slot 3 (generic)               0x1e = 21    -> Iron Sword
slot 4 (generic)               0x1e = 130   -> Bronze Shield
```

Reported spoils: **Iron Sword + Bronze Shield.** Match. The player killed only Milleuda, yet received
slots 3 and 4's items — proof the spoils are collected battle-wide, not per kill.

**Battle 2 — Lenalian Plateau, entry 399 (Milleuda falls).** Vanilla `0x1e` per slot:

```
slot 1 (Milleuda)              0x1e = 0
slot 2 (wears Longsword)       0x1e = 201   -> Silken Robe
slot 3 (wears Leather Cap)     0x1e = 208   -> Battle Boots
```

Reported spoils: **Silken Robe + Battle Boots + ~1000 gil.** Match. **No unit in the battle wears
Battle Boots** — the killer clue that broke the "enemy equipment" theory: `0x1e` is a reward token
attached to the slot, independent of what the unit equips.

## Current vanilla spoils table — Chapter 1

| Entry | Battle | Spoils (`0x1e` per slot) |
|------:|--------|--------------------------|
| 388 | Gariland | Mythril Knife, Phoenix Down, Potion |
| 389 | Mandalia | Potion, Potion |
| 384 | Siedge Weald (Sweegy) | (none) |
| 385 | Dorter Slums | Iron Sword, Hempen Robe, Ether |
| 386 | Sand Rat Sietch | High Potion, Blind Knife |
| 395 | Brigands' Den (Milleuda 1) | Iron Sword, Bronze Shield |
| 399 | Lenalian Plateau (Milleuda 2) | Silken Robe, Battle Boots |
| 400 | Fovoham Windflats | High Potion |
| 401 | Ziekden Fortress | (none) |

NG++ override now applied for Gariland (`388`): Mythril Knife + Phoenix Down + Potion becomes
**Air Knife + Phoenix Down + X-Potion**, preserving the original categories while moving the reward
to the Chapter-1 post-game floor.

Across all four ENTD files: **42 of 512 entries** carry at least one spoils item
(items-per-battle distribution: 1 item → 24 battles, 2 → 13, 3 → 5). The table mixes consumables
(Potion 240 / High Potion 241 / Ether 243 / Phoenix Down 253) with low-tier gear — clearly an
authored "battle completion reward" list. Some story battles (Sweegy, Ziekden) have none.

## What it is NOT (do not re-investigate)

All of these were checked and disproven this session:

- **A Nex/NXD reward table** — swept all 192 base tables in `0004.pac`; no per-battle item-reward table.
- **Move-Find / `MAP_TRAP_FORMATION_DATA`** — vanilla map 91 (Brigands) treasures = {53,54,60,83};
  map 77 (Lenalia) = {129,146,159,174}. Neither matches the spoils. (Move-Find is a *separate* reward
  channel the mod already upgrades; see the rewards memory.)
- **The unit's live equipment (`0x12`–`0x16`)** — modded Milleuda fights with Runeblade + Crystal
  Shield but the spoils were the vanilla Iron Sword + Bronze Shield.
- **A second ENTD copy baked into `FFT_enhanced.exe`** — byte-search for the unit's record signature
  returned 0 hits.
- **`fftpack/event_btlevt_bin_entrydata_add_ent.bin` and `event_win001_bin.bin`** — items absent.
- **`OverrideEntryData` (NXD)** — no `RightHand=21` / `LeftHand=130` anywhere; Milleuda's equipment
  is not overridden there.

## Why the mod's NG+ spoils were vanilla

`src/fftivc.battles.ngplus` swaps the entire ENTD file (fftpack indices 224–227) in NG+ via the
`fileReadRequestOffset` hook, so enemies you fight are modded. But the data we author in the modded
ENTD only changes level/job/equipment (`0x12`–`0x16`) and never `0x1e`. The swap *does* carry `0x1e`
through — it just carries the **vanilla** bytes because we copied them unchanged. Verified by reading
the embedded ENTD out of the deployed DLL: entry 395 slots 3/4 still hold `0x1e = 21 / 130`.

## The fix

Write the intended spoils into `0x1e` of occupied slots in the modded ENTD. Properties:

- **No new hook or file.** The mod already swaps the exact file that contains `0x1e`.
- **NG+-only automatically.** First playthrough reads the vanilla ENTD → vanilla spoils. The mod's
  swap is gated on NG+, so the reward change rides that gate.
- **Decoupled from difficulty.** Set `0x12`–`0x16` for how the enemy fights and `0x1e` for what it
  drops, independently. A perfectly balanced boss can hand out an otherwise-inaccessible item.

### Implementation notes

- Put spoils on slots that have a **present unit** in the (modded) battle. Vanilla always attaches
  them to occupied slots; do the same. The boss slot is a fine carrier even though vanilla leaves it 0.
- A battle awards **at most 3 spoils items** (engine cap, see "Hard cap"). Never author more than
  3: extra `0x1e` bytes on higher slots are silently dropped. Put the 3 intended items on the
  battle's 3 lowest-indexed occupied slots.
- Tooling: extend `tools/entd_tool.py` — its `patch-levels` already writes a fixed slot offset
  (`LEVEL_OFFSET = 0x03`); add an analogous writer for `0x1e` (e.g. `patch-spoils`). Or write the
  bytes directly when assembling the modded ENTD.
- Inspect any battle's current spoils with `entd_tool.py dump-entry --entry <N>` and read byte `0x1e`
  of each slot (it is inside the `raw_tail` column).

### Validation (do this before scaling to every battle)

Set one battle's `0x1e` to a distinctive, unmistakable item (e.g. on Brigands/entry 395), rebuild the
mod, deploy, and fight it in NG+. If the Spoils screen shows the new item, the end-to-end path is
confirmed and we can author the full per-chapter reward tables.

**Done (2026-06-26):** entry 395 now drops Runeblade + Crystal Mail + Bracers in NG+ (authored on
slots 3-5). The end-to-end path is confirmed, and the 3-item cap was discovered in the process.

## Chapter 4 application (best / inaccessible gear)

Chapter 4's design goal is to hand the player the best equipment as the story climaxes, including items
that are normally inaccessible. Because spoils are decoupled from combat gear, the recipe is:

1. Identify each Chapter 4 battle's ENTD entry (see `docs/battles/037-chapter-4-overview.md` and the
   ENTD-entry-ID method).
2. Choose the reward items per battle (**at most 3**, the engine cap), escalating with the story
   (Excalibur, Ragnarok, Genji set, etc.).
3. Write them into `0x1e` of occupied slots in the modded ENTD for those entries.
4. Keep the enemies' own `0x12`–`0x16` tuned for difficulty separately.

## Open items

- **`0x1f` may be the base gil.** Entry 399 slot 2 has `0x1f = 10` and the battle paid ~1000 gil
  (×100). Unconfirmed with a second data point; if true we control gil per battle too. (An earlier
  note claimed plundered gil scales with enemy level — reconcile these once tested.)
- **Exact slot-presence requirement** for a spoils byte to register (does an empty slot's `0x1e`
  still drop?). Assume "needs a present unit" until tested.
- **End-to-end fix validation** in NG+ (see Validation above).

## How this was found (reproducibility)

- Extract ENTD from the game: `FF16Tools.CLI.exe unpack -i 0002.pac -f fftpack/battle_entdN_ent.bin -o <dir> -g fft`
  (every FFT command needs `-g fft`).
- Dump an entry: `python tools/entd_tool.py dump-entry --input battle_entd4_ent.bin --entry 395 --include-empty`.
- Verify what's actually deployed by reading the embedded ENTD out of the built DLL
  (`C:\Reloaded-II\Mods\fftivc.battles.ngplus\fftivc.battles.ngplus.dll`) and checking byte `0x1e`.
- Item id ↔ name via the localized `Item-en` table (FF16Tools `nxd-to-sqlite` on `0004.en.pac`).

See also: `docs/battles/010-chapter-1-balance-review.md` (reward rationale), the Move-Find reward
memory (a separate channel), and `notes/04-ngplus-conditioning.md` (the ENTD swap mechanism).
