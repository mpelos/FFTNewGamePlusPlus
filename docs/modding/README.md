# Modding reference — FFT: The Ivalice Chronicles Enhanced

Technical reference documentation for this project's reverse-engineered understanding of TIC's data
formats, runtime structures, and event-scripting system. Each file below covers one self-contained
topic.

**These documents are factual reference material, not investigation logs.** They describe what is
proven true about the game today — confirmed byte layouts, confirmed mechanisms, confirmed working
techniques, confirmed dead ends — without narrating how or when it was discovered, what was tried and
failed first, or which tool/session found it. For the historical investigation record (chronological,
includes process and dead ends as they were hit), see `tmp/work/` — that material is session-scoped
and not durable documentation.

## Topics

| File | Covers |
|---|---|
| [01-entd-binary-format.md](01-entd-binary-format.md) | The `battle_entd{1-4}_ent.bin` file format: entry/slot structure, every confirmed byte offset and its meaning, team/control flag semantics, relative level encoding, the guest-vs-enemy detection rule. |
| [02-battle-actor-table.md](02-battle-actor-table.md) | The live, in-memory runtime structure the game uses to track battle participants: base address, stride, confirmed field layout, runtime stat offsets such as Raw PA/Effective PA, and the two-stage unit-activation model. |
| [03-event-script-opcodes.md](03-event-script-opcodes.md) | The `.e` event-script bytecode format: file conventions and a confirmed opcode reference table (names, parameter shapes, byte structures) for the opcodes this project has decoded. |
| [04-adding-event-spawned-enemies.md](04-adding-event-spawned-enemies.md) | The proven recipe for adding a brand-new enemy unit to an event-scripted battle wave (as opposed to a static always-present slot), with a fully worked example. |
| [05-ruled-out-techniques.md](05-ruled-out-techniques.md) | Approaches that were tested and confirmed **not** to work for adding a new event-spawned unit, and why — so they aren't re-attempted. Includes native runtime-hooking constraints. |
| [06-job-swap-fallback-and-battle-inventory.md](06-job-swap-fallback-and-battle-inventory.md) | The job-swap technique (re-theming an existing slot), plain new ENTD slots for static rosters, and the current inventory of battles that want an extra body. |
| [07-diagnostics-and-logging.md](07-diagnostics-and-logging.md) | How to temporarily enable the project's diagnostic logs and Reloaded-II file-access logging, where to read the logs, and when to turn each signal back off. |
| [08-adding-formation-gated-static-enemies.md](08-adding-formation-gated-static-enemies.md) | The Zeirchele Falls technique for adding a new enemy to a static roster whose high ENTD slot is ignored until `OverrideEntryData` and `root.nxl` are expanded. |
| [09-sprite-sheet-budget.md](09-sprite-sheet-budget.md) | The per-battle unique-spritesheet budget: the palette-corruption symptom, what counts against the budget, the `tools/sprite_budget.py` pre-playtest analyzer, design mitigations, and the future path to raising the engine limit. |
| [10-event-scripts-and-the-e-files.md](10-event-scripts-and-the-e-files.md) | **The enemy-add playbook — start here.** Decision tree (job-swap / static add / script-managed add), the full paths + tools maps, how to find a battle's `.e` file (uid-profile scan → numbering shortlist → authoritative file-access log), both recipes with validation status, the verify-and-deploy block, failure triage, and the per-battle track record. |
| [11-transform-boss-runtime-scaling.md](11-transform-boss-runtime-scaling.md) | How to scale scripted transform/phase bosses whose final fighting actor is not fully controlled by the visible ENTD slot; confirmed on Lionel Castle Oratory / Cuchulainn. |

## State of the world

**For any new enemy add, start at the playbook:
[10-event-scripts-and-the-e-files.md](10-event-scripts-and-the-e-files.md).** It classifies the
battle up front (static vs script-managed vs wave, decided by the siblings' flags byte and
`tools/scan_event_units.py`), maps every tool and path, and ends in the mechanical pre-playtest
gate `python tools/audit_slot_adds.py`. The key engine fact behind it: a slot whose flags carry
bit `0x40` is script-managed — its existence comes from the battle's `.e` event script
(`AddUnit` registration + choreography), so an added slot must either avoid `0x40` (static `0x90`
add) or be registered/choreographed in the right script file.

Adding a genuinely new, event-spawned enemy unit to a story battle — not just a job-swap of an
existing slot — **is a solved, proven technique**, validated end-to-end in-game on Merchant
Dorter (Chapter 2 opener). See [04-adding-event-spawned-enemies.md](04-adding-event-spawned-enemies.md)
for the full recipe. The technique requires three coherent layers (an ENTD slot, a correctly-targeted
event-script choreography block, and an explicit unit-registration entry in that same script) — all
three are necessary; any one alone leaves the unit either absent or a permanently-inactive ghost
entry in the live actor table. Final spawn-tile placement for a newly added unit is a separate,
cosmetic concern layered on top of this technique — see the closing note in
[04-adding-event-spawned-enemies.md](04-adding-event-spawned-enemies.md).

For battles that want a new unit but are **not** event-scripted (the unit should simply be present
from battle start), choose between a job-swap and a plain new ENTD slot: job-swap is the lowest-risk
choice when the design only needs a different role in an existing body; a plain new ENTD slot is the
right tool when the design truly needs one more body and the battle is not script-gating that unit's
arrival. See [06-job-swap-fallback-and-battle-inventory.md](06-job-swap-fallback-and-battle-inventory.md).
If a plain high-slot ENTD add is ignored and the battle's `OverrideEntryData` rows stop before that
slot, use the Zeirchele formation-gated static recipe in
[08-adding-formation-gated-static-enemies.md](08-adding-formation-gated-static-enemies.md).
That path is still a static-roster solution: it expands the NXD formation layer and does not use
event-script choreography or `AddUnit` registration.

One constraint cuts across all of these techniques: the per-battle **sprite-sheet budget**
([09-sprite-sheet-budget.md](09-sprite-sheet-budget.md)). Any edit that makes a battle need a
spritesheet it did not already load — a new generic job, a new named unit — spends budget, and going
over corrupts the sprite/portrait of the last-allocated unit (typically an event-added guest) while
leaving it fully functional. The validated design rule is net +1 unique sheet over vanilla per
battle; check with `python tools/sprite_budget.py <entry>` before playtesting.

## Technique selection quick reference

| Situation | Use | Why |
|---|---|---|
| Same enemy count, but a different job/role is desired | Job-swap an existing ENTD slot | Keeps the battle's existing spawn timing, event-script activation, sprite preload, team flags, and unit ids intact. |
| Static roster, true enemy-count increase | Plain new ENTD slot | No mid-battle registration/choreography layer exists, so the ENTD slot itself is enough once the position, flags, and visual preload constraints are valid. |
| Static roster, high ENTD slot ignored, `OverrideEntryData` rows stop before the new slot | Formation-gated static slot-add | Add the ENTD slot and expand `OverrideEntryData`/`root.nxl`; no event choreography or `AddUnit` registration is needed. |
| Event-scripted wave, same enemy count | Job-swap one of the existing scripted wave slots | The existing slot is already registered and choreographed by the correct script. |
| Event-scripted wave, true enemy-count increase | Full three-layer event-spawned recipe | The new unit needs an ENTD slot, a copied/retargeted choreography block, and a matching `AddUnit` registration entry in the script actually loaded at the wave trigger. |
| Unsure whether an enemy add needs script editing at all | `python tools/scan_event_units.py <uids>` | If the battle's enemy uids appear in an `AddUnit` bracket they are event-delivered (doc `04`); otherwise the roster is static and the add is ENTD-only work — see [10-event-scripts-and-the-e-files.md](10-event-scripts-and-the-e-files.md). |
| An added unit never appears despite correct ENTD (and NXD row) | Check the added slot's flags for bit `0x40` | `clone_slot` copies the sibling's flags; `0x40` = script-managed presence — the battle's `.e` must `AddUnit`-register the new uid (Recipe B), or clear the bit to `0x90` for a plain static add — validated on Zaland. See [10-event-scripts-and-the-e-files.md](10-event-scripts-and-the-e-files.md) and `tools/audit_slot_adds.py`. |
| Unsure which `.e` file drives a wave | Temporary Reloaded-II file-access logging | NXD joins can point at a real but irrelevant script; the runtime file-open log is the reliable source. |
| Need only a decorative cutscene sprite, not a combatant | `AddGhostUnit`/presentation-layer work | `AddGhostUnit` creates a display entity, not a targetable unit with turns, HP, AI, or victory-condition participation. |
| A unit renders with palette-garbage sprite/portrait but plays normally | Sprite-sheet budget check (`tools/sprite_budget.py`) | The battle exceeds its unique-spritesheet budget; reduce or reuse sheets — see [09-sprite-sheet-budget.md](09-sprite-sheet-budget.md). |
| A transformed boss stays at vanilla level even though its ENTD slot is `104+` | Runtime transform-boss scaling | The final combatant may be a script-registered actor with a different runtime id; patch actor-table `+0x29` with the expanded real level, not ENTD syntax. See [11-transform-boss-runtime-scaling.md](11-transform-boss-runtime-scaling.md). |
