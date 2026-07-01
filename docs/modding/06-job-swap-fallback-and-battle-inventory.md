# Job-swap, plain ENTD slot-adds, and the current battle inventory

This document covers the **job-swap** technique — re-theming an existing ENTD slot's job, equipment,
and identity instead of allocating a new slot — the **plain new ENTD slot** technique for static
rosters, and the project's current inventory of battles that want an additional or different-feeling
enemy unit, with the applicable technique for each.

For the technique that adds a genuinely new ENTD slot to an event-scripted wave, see
[04-adding-event-spawned-enemies.md](04-adding-event-spawned-enemies.md). For the static-roster case
where a high ENTD slot is ignored until `OverrideEntryData` is expanded, see
[08-adding-formation-gated-static-enemies.md](08-adding-formation-gated-static-enemies.md). For the
ENTD slot layout itself (offsets, flags, the fields job-swap edits), see
[01-entd-binary-format.md](01-entd-binary-format.md).

## Technique 1: job-swap

Job-swap re-themes an existing ENTD slot rather than allocating a new one. Given a slot already
present in a battle's roster, the technique changes:

- **Job** (`SLOT_JOB`, offset `0x0A`) — the unit's main job id, which also drives its sprite/portrait.
- **Equipment** — head, body, accessory, and weapon slot ids, set to match the new job's intended kit.
- **Job level seed** (`SLOT_JOB_LEVEL`, offset `0x09`) and the roster job-unlock target
  (`SLOT_JOB_UNLOCK`, offset `0x08`), so the unit's abilities (reaction, support, movement, innate
  job commands) match its new identity.
- **Level** (`SLOT_LEVEL`, offset `0x03`) and any reaction/support/movement ability ids, tuned to the
  new role the slot is meant to play in the redesigned encounter.
- **Identity/framing in documentation** — the slot is described and balanced as the new unit (e.g.
  "Street Captain — Knight") even though its underlying slot index, character id, and unit id are
  unchanged.

Job-swap deliberately leaves alone:

- **Slot allocation** — no new slot is added to the entry; the entry's total slot count is unchanged.
- **Team/control flags** (`SLOT_CONTROL_FLAGS`, offset `0x18`) — enemy/ally team membership and
  player-control bits stay whatever they were for that slot.
- **Position** — starting coordinates and the LoadFormation-vs-reinforcement flag distinction are
  untouched, so the slot's existing intro/spawn timing behavior carries over unchanged.
- **Character id and unit id** — the slot keeps its original identifiers; only the job/equipment/
  level fields layered on top of them change.

This is what makes job-swap safe in every case: it is a pure ENTD-byte edit confined to a single
slot's existing fields. It never touches the event-script/activation layer — no choreography block,
no `AddUnit`-family registration entry, no interaction with the two-stage actor-activation model.
Whatever spawn timing and activation path the slot already had (present-from-start or
script-triggered reinforcement) continues to work exactly as before, because none of the bytes that
control that path are part of the edit. This is the structural reason job-swap carries zero risk of
the failure modes that a true slot-add must account for (see
[04-adding-event-spawned-enemies.md](04-adding-event-spawned-enemies.md) and
[05-ruled-out-techniques.md](05-ruled-out-techniques.md) for what a slot-add has to get right that
job-swap simply never encounters).

## Technique 2: plain new ENTD slot for static rosters

A plain new ENTD slot is the correct way to increase enemy count when the battle's roster is loaded
statically from the ENTD and the new unit is meant to be present from battle start. In that case the
edit is still only an ENTD edit: allocate a free 0x28-byte slot in the battle entry, assign a unique
UnitID, fill job/equipment/level/ability bytes, choose valid coordinates, and set flags consistent
with the rest of that static enemy roster.

Plain slot-add deliberately does **not** add event-script records:

- No copied choreography block is needed, because the unit is not arriving through a scripted wave.
- No `AddUnit` registration entry is needed, because there is no wave-registration bracket gating
  the unit's activation.
- No runtime actor-table hook is needed, because the normal battle-load path creates the static
  formation.

The main checks are local to the ENTD and the map: free slot, free UnitID, legal job/equipment,
enemy-side flags, non-overlapping coordinates, and a visual test that the unit renders correctly.
If the battle has a pre-battle tactical-view intro, also check the sprite preload behavior described
in [05-ruled-out-techniques.md](05-ruled-out-techniques.md#a-static-always-present-extra-entd-slot).
For a fully static battle this is still much simpler than the event-spawned recipe; the extra
caution only matters when the intro tries to render a job sprite the battle has not preloaded.

Some static rosters have an additional NXD formation gate: the ENTD high slot is valid, but the game
ignores it because `OverrideEntryData` rows for that battle stop before the new slot. In that case,
the correct fix is not event scripting; add the ENTD slot and expand the NXD table as described in
[08-adding-formation-gated-static-enemies.md](08-adding-formation-gated-static-enemies.md).

## Decision guide

When a battle's design calls for an additional or different-feeling enemy unit, the deciding factor
is **whether the enemy count changes** and **how that battle's roster is delivered**:

| Design need | Roster delivery | Technique |
|---|---|---|
| Same count, different role/job | Static roster or event-scripted wave | **Job-swap** an existing slot. This is the safest option because the slot already participates in the battle through the correct path. |
| True count increase | Static roster, present from battle start | **Plain new ENTD slot.** Add the slot in the battle entry and validate flags, UnitID, position, and sprite preload behavior. |
| True count increase | Static roster, but high ENTD slot is ignored and `OverrideEntryData` rows stop before it | **Formation-gated static slot-add** in [08-adding-formation-gated-static-enemies.md](08-adding-formation-gated-static-enemies.md): ENTD slot + matching `OverrideEntryData` row + matching `root.nxl` row count. |
| True count increase | Event-scripted wave or delayed arrival | **Event-spawned recipe** in [04-adding-event-spawned-enemies.md](04-adding-event-spawned-enemies.md): ENTD slot + copied/retargeted choreography block + matching `AddUnit` registration entry in the runtime-confirmed script file. |
| Decorative story/cutscene figure only | Event-scripted scene, not combat roster | Presentation-layer scripting such as `AddGhostUnit`; this does not create a targetable combatant. |

A scripted **exit** (a unit fleeing, retreating, or betraying mid-battle) is not the same as a
scripted **arrival**, and does not by itself put a battle in the event-scripted row above — it only
matters whether new enemy *presence* is gated by the script. A battle with dormant, never-activated
"placeholder" ENTD slots (leftover vanilla data with no script ever waking them) is also not
event-scripted in the relevant sense; those slots are inert data, not a delayed-wave mechanic.

When the roster is event-scripted, job-swap is the lower-effort, zero-new-failure-mode option and
should be preferred unless the design specifically requires raising the enemy headcount rather than
re-casting an existing body.

## Track record

Job-swap is the technique used for every unit-identity change shipped across this project's
implemented battles to date except explicit enemy-count increases: Merchant Dorter's 7th-enemy Knight, which was delivered as a
genuine new ENTD slot via the three-layer event-spawned-enemy recipe once that recipe was worked out
(see [04-adding-event-spawned-enemies.md](04-adding-event-spawned-enemies.md)), and Zeirchele Falls's
7th-enemy White Mage, which was delivered through the formation-gated static recipe (see
[08-adding-formation-gated-static-enemies.md](08-adding-formation-gated-static-enemies.md)). Every other
implemented battle that escalated, re-cast, or re-themed a unit's identity — across all four chapters
— did so by re-tuning an existing slot rather than adding one. Examples include Mount Germinas's "2nd
Ninja," Poeskas Lake's "2nd Mystic," Fort Besselat Sluice's "Time Mage," and Dugeura Pass's "Time
Mage": each is a 1-for-1 job-swap of an existing slot (the surrounding battle text specifies "keep
the count (N)"), not a new slot, despite carrying a "(NEW)" tag in their composition tables — that
tag denotes a job newly cast onto an existing slot, not a newly allocated slot.

## Battle inventory: battles wanting a new or additional enemy unit

The following battles have a documented composition table or design note explicitly calling for an
additional enemy unit (an enemy-count increase, not a same-slot re-cast). This list reflects a
full-text survey of `docs/battles/*.md`; the event-scripted classification for Merchant Dorter is
independently verified against `event119.e` and the live actor table (see
[04-adding-event-spawned-enemies.md](04-adding-event-spawned-enemies.md)). The classification for the
other entries is based on each battle's own documented deployment description (static roster, no
mid-battle arrival trigger noted) and was not independently re-verified against each battle's raw
event-script bytes the way Merchant Dorter's was.

| Battle | Wants new unit? | Event-scripted wave? | Applicable technique |
|---|---|---|---|
| Merchant Dorter (Ch2 opener, `012`) | Yes — Knight captain, 7th enemy | Yes — `event119.e` delayed wave | Event-spawned-enemy recipe (`04`). Implemented: ENTD slot `s9`/uid `0x86` + retargeted choreography block + `45 86 00 01` registration entry. |
| Balias Swale (Ch2, `019`) | Yes — Geomancer, 7th enemy | No — fully static roster | Plain new ENTD slot. Implemented in entry `413`, slot `s7`, UnitID `0x86`. |
| Araguay Woods (Ch2, `013`) | Yes — Coeurl, 7th monster; vanilla monster tiers promoted | No — fully static roster | Plain new ENTD slot. Implemented in entry `404`, slot `s9`, UnitID `0x87`. |
| Zeirchele Falls (Ch2, `014`) | Yes — White Mage field medic, 7th enemy | Formation-gated static roster; high-slot `s11` requires an `OverrideEntryData` row | Formation-gated static slot-add (`08`). Implemented in entry `405`, slot `s11`, UnitID `0x87`; `OverrideEntryData` row `405/11` added; vanilla corpse placeholders `s2/s3` remain untouched. |
| Balias Tor (Ch2, `016`) | Yes — Chemist, 7th enemy (tagged "(NEW)" in the composition table) | No — fully static roster | Plain new ENTD slot. Implemented in entry `409`, slot `s8`, UnitID `0x86`. |
| Tchigolith Fenlands (Ch2, `017`) | Yes — 2nd Bonesnatch, 8th monster | No — fully static roster (the in-combat teleport some enemies use is movement, not a scripted arrival) | Plain new ENTD slot. Implemented in entry `410`, slot `s9`, UnitID `0x86`. |

Most non-Merchant entries are Chapter 2 battles implemented with plain ENTD slot-adds. Zeirchele is
the exception: the battle is not a delayed wave like Merchant Dorter, but its `OverrideEntryData`
rows originally ended at `s10`, so an ENTD-only `s11` add was ignored. The working path keeps the
vanilla intro corpse placeholders (`s2/s3`) untouched, adds the White Mage in `s11`, and adds a
matching `OverrideEntryData` `Key=405, Key2=11` row while moving Zeirchele's end marker
`Unknown9C=150` from `s10` to `s11`. Merchant Dorter remains the only entry in this table whose
roster delivery is event-scripted and needs the full three-layer recipe.

### Battles with dormant placeholder slots (excluded from the table above)

Several battles carry unused, inactive ENTD slots in their data (for example
`029-monastery-vaults-1st.md` slots 6-7 at level `0xFE`, `030-grogh-heights.md` slots 6-8,
`032-yuguewood.md` slot 0, `033-riovanes-castle-gate.md` slot 0, `035-riovanes-castle-roof.md` slots
1-2, `042-bed-desert.md` slots 6-7, and similar slots in `051-mullonde-exterior.md` and
`053-mullonde-sanctuary.md`). These are leftover vanilla data with no script ever activating them —
not a delayed-wave mechanic, and not a documented want for a new unit. They are excluded from the
inventory above.

### Transform/scripted-boss battles (excluded from the table above)

A separate set of battles has genuine event-script-gated or scripted-transform enemy mechanics
(Riovanes Castle Keep's Wiegraf-to-Belias transform, Lionel Castle Oratory's Cardinal Draclau-to-
Cúchulainn transform, Limberry Castle Keep's Celia/Lettie-to-Ultima Demon transform, Eagrose Castle's
Dycedarg-to-Adrammelech transform/summon, and Airship Graveyard's two-entry Hashmal/Ultima chain).
Each of these already has a working scripted-spawn or transform mechanism, but none of their design
docs calls for pushing an additional slot through it — each explicitly declines extra bodies for
design reasons (boss-identity dilution, escalation-chain cost) rather than citing a technical
limitation. They are excluded from the inventory above because they are not a documented want for a
new unit, not because the technique wouldn't apply; if a future design pass wants to add a body to
one of these fights, the event-spawned-enemy recipe is the applicable technique, since all five are
event-scripted.
