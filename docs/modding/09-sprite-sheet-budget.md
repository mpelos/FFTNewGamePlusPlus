# The per-battle sprite-sheet budget

Every battle has a bounded budget of **unique unit spritesheets** it can load. Exceeding it does not
crash and does not remove units: the over-budget unit stays present, targetable, and fully
functional, but renders with corrupted sprite and portrait (palette garbage over an intact
silhouette). This constraint is inherited from classic FFT's engine and is reproduced by TIC's
enhanced mode. It binds all three unit-addition techniques (job-swap, plain/formation-gated static
slot-add, event-spawned slot-add) because it is about which **sheets** a battle needs, not which
slots it has.

Proven in-game on Zeirchele Falls (entry `405`): with a full 4-unit player deployment, adding two
new generic jobs (Archer + White Mage) to a battle whose vanilla generics are all Knights corrupted
Agrias's sprite and portrait; reverting to one new generic job (White Mage only) fixed her, with the
enemy count unchanged at 7 in both compositions.

## What consumes the budget

A battle's sheet consumption is the number of **unique sprite identities**, not the number of units:

- **Named/special units** — one sheet per character id. A character appearing through two charIds
  (story form + guest/enemy form in the same battle) may or may not share one sheet; treat sharing
  as unverified.
- **Generic units** — one sheet per job (per gender). Five Knights cost one sheet; one Knight + one
  Archer cost two.
- **Story/cutscene actors and corpse placeholders** — they draw, so their sheets count. (Zeirchele's
  intro corpses are Knights, sharing the active Knights' sheet.)
- **Player-side units** — the engine reserves the map's deploy **capacity** up front (classic-engine
  behavior: random battles always reserve 5, even if fewer are brought). Player units are not in the
  ENTD, so ENTD math must add the map's deploy capacity on top.

Allocation order matters for the failure mode: units registered by the event script mid-intro
(`AddUnit` — in Zeirchele, Agrias `0x34` and the Gaffgarion escort form `0x17` via `event129.e`)
allocate **last**, so when a battle goes over budget, an event-added guest is the typical victim.
This is why the corrupted unit was Agrias and not the added enemy itself.

## Known numbers

| Fact | Value | Confidence |
|---|---|---|
| PSX total budget | **9** unique sheets | Community-documented (FFHacktics wiki, "Number of spritesheets limit") |
| PSX limit location | `BATTLE.BIN` offset `0x00118910`, byte `09` | Community-documented; the classic hack raises it to `0x0D` (13) |
| TIC enhanced-mode exact budget | Unknown constant, behavior faithfully reproduced | Bounded empirically (below) |
| TIC empirical rule | **Net +1 unique sheet over vanilla is safe; net +2 on a special-heavy battle corrupts** | Proven in-game on Zeirchele; consistent with every other implemented Ch2 battle (all net +1 or +0, all clean) |

Absolute totals are **not** comparable across battles without the map's deploy capacity: Merchant
Dorter runs 7 non-player sheets cleanly while Zeirchele corrupted at 7, because reserved player
capacity and named-sheet sharing differ per battle. The validated design rule is the per-battle
**net delta against vanilla**, which cancels out both unknowns.

## Checking a battle before a playtest: `tools/sprite_budget.py`

The analyzer computes per-entry unique-sheet counts from the ENTD binaries (vanilla vs. modded) and
flags risk by the net-delta rule:

```powershell
python tools/sprite_budget.py                # default: the implemented Ch2 battle set
python tools/sprite_budget.py 405 403        # specific global entries
python tools/sprite_budget.py --all-vanilla  # survey every entry of all 4 vanilla ENTD files
```

Output per entry: vanilla total, modded total, net delta, plus the exact added/removed sheet
identities (`RED` at net ≥ +2; `watch` at net +1 on a battle with 3+ named sheets). Reference
snapshot of the implemented battles:

| Entry | Vanilla sheets | Modded sheets | Net |
|---|---|---|---|
| 403 Merchant Dorter | 6 | 7 | +1 |
| 404 Araguay Woods | 5 | 6 | +1 (swapped one monster job out) |
| 405 Zeirchele Falls | 5 | 6 | +1 (the +2 composition corrupted Agrias) |
| 407 Zaland / 409 Balias Tor | 5 | 6 | +1 |
| 410 / 415 / 425 | — | — | +0 |

Known limitations of the analyzer: it does not split generic sheets by gender, does not know each
map's deploy capacity (add it manually when judging absolute headroom), cannot tell whether two
charIds of the same character share a sheet, and its name annotations come from the PSX-era
FFTPatcher `SpecialNames.xml`, which TIC in-game evidence has already contradicted at least once —
treat names as hints, charId counts as the data.

## Designing within the budget

Ordered by cost, when a design wants more unit variety than the budget allows:

1. **Reuse an existing sheet.** Make the added unit a job the battle already fields (Zeirchele's
   added 7th enemy is a Knight for exactly this reason), or move the new job into a vanilla slot
   and backfill the vanilla job into the added slot — slot position does not change sheet math, but
   it lets the design keep the new role.
2. **Deliver the role through equipment instead of a job.** ENTD-forced gear works on any job, so
   ranged pressure can come from a crossbow on a Knight (one-handed, shield-compatible) rather than
   an Archer sheet. Untested in this project as of this writing, but it is a plain ENTD gear byte
   with no new failure mode.
3. **Swap a sheet out to fund a sheet in.** Net-zero job substitutions (Araguay dropped one vanilla
   monster job while adding two others, landing at net +1) keep totals flat.
4. **`OverrideEntryData.Spriteset` (research lead).** The formation-layer table has a per-slot
   `Spriteset` column, used by vanilla in exactly 4 rows (values 2, 12, 25, 48). If it does what its
   name says, it could dissociate a unit's sheet from its job (e.g., an Archer job wearing the
   already-loaded Knight sheet — classic FFT generic sheets share one animation frame layout, so
   cross-assignments render). Semantics and id space unverified; requires reverse-engineering the 4
   vanilla usages plus at least one playtest.
5. **Reduce player-side pressure.** Fewer deploy slots or duplicate-job deployments lower the total,
   but the player controls this, so it is not a design guarantee.

## Raising the limit itself (future work)

The budget is **not data-driven** — no NXD table carries it (searched), so raising it means patching
the engine. On PSX this is a proven one-byte change; TIC almost certainly has an analogous constant
in `FFT_enhanced.exe`, and unlike the PSX original there is no hardware VRAM reason for the value,
so a raised limit plausibly just works. Candidate approaches, cheapest first:

1. **Pin the TIC constant empirically first.** Bisection playtests on a controlled battle (add one
   unique sheet at a time until corruption appears, with a fixed player deployment) establish the
   exact value in 2–4 tests. Knowing the value (e.g., whether TIC already raised 9) both informs
   design and gives the byte value to hunt for.
2. **AOB-scan the sprite-loading path.** Precedent: this project located the live battle-actor
   table via third-party AOB patterns when static disassembly of the obfuscated exe failed. The
   equivalent here is scanning for small-immediate comparisons (`cmp`-with-9-family encodings) in
   code reachable from battle setup, then validating candidates by runtime byte-patching (a static
   in-place constant patch, unlike the function hooks that reproducibly crashed this exe, does not
   redirect control flow).
3. **Locate the runtime counter, then its writers.** Cheat Engine-style: enter battles with known
   sheet counts (5, 6, 7 …), scan for a matching counter, then hardware-watch what compares against
   it. The comparison site reveals the limit constant's address.
4. **Community channels.** The FearLess Cheat Engine thread for TIC and the Nexus sprite-toolkit
   authors work in exactly this layer; the classic-hack lineage (the PSX `09 → 0D` patch) is
   well-known enough that a TIC port may already exist or be in progress.

Risks to test for if the constant is raised: downstream fixed-size arrays sized to the same
assumption (palette/CLUT slots, portrait cache, formation-view rendering). The PSX hack history says
13 was safe there; TIC's internals differ, so raise incrementally (one step, then a
maximum-pressure battle like Zeirchele with full varied deployment as the regression test).

## Failure signatures

| Symptom | Meaning | Fix |
|---|---|---|
| A unit (typically an event-added guest) has palette-garbage sprite AND portrait but plays normally | Battle is over the sheet budget; this unit's sheet allocated last | Reduce unique sheets (see "Designing within the budget"); verify with `tools/sprite_budget.py` |
| Corruption appears only with full/varied player deployment | Player capacity + ENTD sheets together cross the budget | Same as above; the ENTD-side count must leave headroom for the map's full deploy capacity |
| Corruption appeared after adding a 2nd new job to one battle | Net +2 over vanilla | Fund the new sheet by removing another, or reuse an existing sheet |
