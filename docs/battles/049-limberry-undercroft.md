# 049 - Limberry Castle Undercroft

Status: 📝 redesign v2 planned (docs-only) — v1 implementation exists for entry 457
Chapter: 4 — "In the Name of Love"
Battle order: Battle 44 (Limberry chain 3 of 3 — NO resupply across 42→43→44)
Target version: Enhanced v1.5.0
ENTD: global entry **457** (local 73, entd4)
File: `battle_entd4_ent.bin`

> **NG++ rewards applied (2026-06-27):** Aegis Shield + Zeus Mace through guaranteed Spoils of War
> (`0x1e`), NG+ only, within the 3-item cap, no stealing required. Zalera has no normal equipment slots,
> so these are reward payloads, not fake boss gear. Canonical map: `chapter-4-rewards-implementation.md`.

## Current Implementation / Data Reality

```text
DATA REALITY (verified from current embedded entd4 dump, entry 457):
  slot 0 = Elmdor cameo/script record
           job 27, level 43, JobLevel 8, eq=255 no gear.
           Preserve until in-game testing proves whether he is active; do not treat as a reward carrier.

  slot 1 = Zalera / Death Seraph
           job 62, level 105, JobLevel 8, secondary 108, eq=255 no normal equipment.
           Spoils byte = 0x88 (Aegis Shield).

  slots 2,3 = job 61 undead knight-like monster/fixed bodies
              type=monster, level 103, JobLevel 8, eq=254 fixed/no normal gear.
              slot 2 spoils byte = 0x41 (Zeus Mace).

  slots 4,5,6,8,9 = skeleton-family undead monsters
                    jobs 111/110/109/111/111, level 103, no normal human equipment setup.

  slot 7 = Meliadoul join/post-battle record
           job 42, level 254, gear includes Save the Queen + Aegis Shield.
           Public battle shape has no active guest. Treat this as a join/post-battle record unless
           playtest proves it is active; if active, NG++ guest-control rule applies immediately.

Current v1 implementation:
  Zalera = 105
  undead guard = 103
  Win condition, Zalera mass-status identity, undead/reraise identity, slot 0 cameo, and slot 7 join
  record are preserved.
```

Planned v2 redesign (docs-only in this pass): keep the local ENTD reality and make the fight a **status
Lucavi capstone with a dense undead screen but a real boss-focus lane**. The player should resist/cleanse
Zalera's curses, use Holy/Phoenix Down/Seal Evil to manage the dead, and focus the Death Seraph before
the end of the Limberry chain collapses into item/status debt.

> Data-layer fields are known for entry 457, but final implementation still needs a fresh dump/diff and
> in-game verification of slot 0 and slot 7 behavior. This pass updates documentation only.
> LIMBERRY CHAIN: 42 (`047`) → 43 (`048`) → 44 (`049`), one loadout.

## Design Goal

```text
Make Limberry Undercroft the chain capstone: Zalera is the single visible mass-status engine, the undead
guard creates action-economy and permakill pressure, and the player must keep enough units acting to
burst the Lucavi. The fight is severe, but never an unavoidable Stop/Doom/Confuse lock, never a guest-AI
failure, and never a reward path that depends on Steal or Meliadoul's join gear.
```

No active guest is expected in the playable battle. Slot 7 must be treated as join/post-battle data. If
implementation or playtest proves Meliadoul is active, she must be player-controlled in NG++.

## Original Battle

Objective:

```text
Defeat Zalera!   (defeating Zalera ends the battle)
```

Player deployment:

```text
Up to 5 units, including Ramza. No active guests expected. NO outfitter access (chain 3/3 capstone).
```

Public-guide enemy composition:

```text
Zalera (Death Seraph)   (Lucavi boss; mass status)
2x undead Knight        (undead screen)
Skeleton / Bonesnatch / Skeletal Fiend
```

Local ENTD correction:

```text
The embedded data exposes a denser undead guard than the public guide lists:
  Zalera + two job-61 undead/fixed knight-like monster bodies + five skeleton-family undead monsters.

Design consequence: preserve the local roster, but positioning/scripting must leave at least one
boss-focus lane. The undead are a screen and resource tax, not mandatory full cleanup before Zalera.
```

Public walkthrough details:

```text
Recommended level: ~60. Difficulty: 3/5 stars. Deploy up to 5. No resupply.
Zalera repeatedly casts mass status such as Stop, Doom, Sleep, Confuse, and Toad. The guard is undead,
so Phoenix Down, Holy, and Seal Evil style answers matter. Meliadoul joins after the battle.
Buried map treasure includes Gastrophetes, Obelisk, and Eight-Fluted Pole.
```

Design reading:

The Undercroft is **the status-Lucavi capstone** of Limberry. Gate was a flee race; Keep was a parry
race; Undercroft is the moment where the player must prove their chain loadout can still function while
Zalera attacks action economy directly. The undead guard matters because killing is not clean unless
the player spends the right actions, but the tactical lesson is still boss focus: do not get hypnotized
by the screen while the Death Seraph keeps rolling status.

For New Game++ the identity must stay: **resist, cleanse, permakill selectively, and burst Zalera**.

## Local Data Confirmed / Data Still Needed

```text
CONFIRMED:
- Entry 457 is the playable Limberry Undercroft battle data.
- Slot 1 is Zalera, level 105, no normal equipment, reward payload Aegis Shield.
- Slot 2 carries Zeus Mace as reward payload.
- Slots 2/3 are undead/fixed monster-type knight bodies, not editable full human Knight kits.
- Slots 4/5/6/8/9 are skeleton-family undead monsters.
- Slot 7 is a Meliadoul join/post-battle record in the data and should not be used as a guest-AI check.
- No active guest is expected from the public battle shape.
- Reward ledger maps this battle to Aegis Shield + Zeus Mace guaranteed spoils.

STILL NEEDED FOR V2 IMPLEMENTATION:
- In-game verify whether slot 0 Elmdor and slot 7 Meliadoul are active, hidden, or join/script records.
- If slot 7 is active, set player control per global guest rule.
- Confirm Zalera's status cadence allows cleanse/resist windows and does not chain-lock the party.
- Confirm undead/reraise behavior and Phoenix Down/Holy/Seal Evil answers.
- Confirm the map has or can preserve a boss-focus lane through the dense undead screen.
- Confirm Aegis Shield + Zeus Mace land as guaranteed spoils without using Meliadoul join gear.
- Preserve buried map treasure as vanilla map loot.
```

## Enemy Party Escalation (Chapter 4 rule)

```text
Headline engine: Zalera's mass-status Lucavi pressure.
Supporting roles:
  - Undead/fixed knight-like bodies create the first screen and punish careless physical routing.
  - Skeleton-family undead bodies widen the screen and tax permakill resources.
  - Slot 7 Meliadoul is not a difficulty lever; she is join/post-battle data unless proven active.

WHY: this is the Limberry capstone. The enemy party can be dense and punishing, but it must remain one
readable puzzle: stop the status engine while managing undead bodies.

CONSTRAINTS:
  - Zalera is the one mass-status source.
  - Status must be resistable, cleansable, and non-locking.
  - Undead bodies must not seal every route to the boss.
  - No extra support caster, healer, or additional status engine.
  - No fake equipment on Zalera's no-equip Lucavi slot.
  - No guest AI survival test.
```

## Sanctioned Exceptions

```text
LUCAVI MASS STATUS:
  Allowed as Zalera's signature. Guardrail: visible, resistable, cleansable, and non-locking. Doom is a
  race-able countdown; Stop/Sleep/Confuse/Toad must never become an unavoidable party-wide chain lock.

UNDEAD RERAISE / PERMAKILL:
  Allowed as the guard's identity. The player answers with Phoenix Down, Holy, Seal Evil, or selective
  focus fire while downed. The undead are not all mandatory kills because Zalera is the win condition.

DENSE LOCAL ENTD ROSTER:
  Allowed because the embedded data proves more undead slots than the public guide lists. Guardrail:
  preserve or create at least one boss-focus lane.

JOIN/POST-BATTLE MELIADOUL RECORD:
  Preserve the slot without making guest AI part of the challenge. If she appears active in battle,
  player control is mandatory.
```

## Rare/reward handling

```text
Guaranteed spoils for entry 457: AEGIS SHIELD + ZEUS MACE.
These are delivered by the Spoils of War reward channel; the player must never be required to Steal.

COMBAT ROLE:
  - Zalera cannot equip normal gear (`eq=255`), so Aegis Shield is reward payload only.
  - Zeus Mace is reward payload on the undead screen, not a required active caster weapon.
  - Meliadoul's join gear is not the canonical reward path.

PRESERVE:
  - Buried map treasure remains vanilla map loot.
  - Slot 7 join gear remains a separate recruitment/script concern.
```

## Proposed Composition (New Game++ Limberry Undercroft v2)

Keep the local roster and levels. The redesign is positioning/guardrail clarity: dense undead screen,
one status engine, and at least one route to focus Zalera.

| Slot | Role | Unit type | Level | Br/Fa | Purpose |
| ------ | ------ | ----------- | ------- | --- | --------- |
| s1 | Boss / objective | Zalera, Death Seraph Lucavi | `105` | `92/86` | Single mass-status engine; defeat ends fight; Aegis Shield spoil. |
| s2 | Screen / reward payload | Job 61 undead/fixed knight-like monster | `103` | `86/35` | First undead body; Zeus Mace spoil; screens a direct route. |
| s3 | Screen | Job 61 undead/fixed knight-like monster | `103` | `86/35` | Second undead body; forces route choice. |
| s4 | Undead pressure | Skeleton-family monster job 111 | `103` | `86/35` | Reraise/permakill action tax. |
| s5 | Undead pressure | Skeleton-family monster job 110 | `103` | `86/35` | Second skeleton-family pressure body. |
| s6 | Undead pressure | Skeleton-family monster job 109 | `103` | `86/35` | Lower-route undead body. |
| s8 | Undead pressure | Skeleton-family monster job 111 | `103` | `86/35` | Outer screen body; must not seal boss access. |
| s9 | Undead pressure | Skeleton-family monster job 111 | `103` | `86/35` | Outer screen body; cleanup risk control. |

Non-combat/script records to preserve and verify:

| Slot | Record | Handling |
|------|--------|----------|
| s0 | Elmdor cameo/script record | Preserve untouched unless playtest proves active; if active, redesign separately before implementation. |
| s7 | Meliadoul join/post-battle record | Preserve as join data; if active, make player-controlled in NG++. |

Reasoning:

The accepted design is **v2 status-Lucavi with undead screen** after one iteration. The first simulation
flagged the dense local undead roster as too much if the bodies formed a sealed wall. The revised design
keeps the data-faithful roster but requires a boss-focus lane: the player may need to permakill or push
through part of the screen, but does not have to clear every undead body while Zalera rolls status.

Rejected variants:

```text
- Hard-lock Death Seraph: turns mass status into unavoidable lost turns.
- Living support engine: adds a second puzzle behind Zalera.
- Clear-all undead slog: breaks the boss focus objective.
- Active AI Meliadoul risk: uses guest AI as a skill check.
- Fake-equipped Zalera reward: violates no-equip Lucavi data.
- Steal-or-join reward: contradicts guaranteed spoils.
- Downplayed status exhale: loses the chain capstone.
- Overlevelled crypt: replaces puzzle pressure with raw stats.
- Extra undead body: adds cleanup tax to an already dense roster.
- Sealed undead wall: ignores the required boss-focus lane.
```

## Builds (Lucavi + monster/fixed undead screen)

```text
Zalera:
  - Job: Death Seraph / Lucavi (job 62), JobLevel 8.
  - Preserve no-equipment Lucavi slot (`eq=255`).
  - Preserve mass-status identity through secondary/status kit.
  - Status is the one headline engine: visible, resistable, cleansable, non-locking.
  - Reward payload: Aegis Shield via spoils, not equipped gear.

Job 61 undead/fixed knight-like bodies:
  - Type is monster in the dump; equipment is fixed/no normal gear.
  - Preserve undead/fixed body identity and level 103.
  - Do not promise complete human Knight equipment or ability slots unless future data proves these are
    editable active humans instead of monster/fixed bodies.
  - Slot 2 carries Zeus Mace as reward payload only.

Skeleton-family monsters:
  - Preserve innate undead monster kits and level 103.
  - No human equipment, secondary, reaction, support, or movement planning.
  - Use placement to create pressure without sealing the boss.

Meliadoul slot:
  - Treat as join/post-battle record.
  - If active, set player control and document her as an active guest before implementation.
```

## Positioning Plan

```text
Undercroft: Zalera starts central/back with clear mass-status sightlines. Undead bodies form a dense
screen in two clusters, but at least one route must let a prepared party reach or target Zalera without
full undead cleanup.

The player should see three valid lines:
  1. Resist/cleanse enough status to keep turns.
  2. Permakill selected undead bodies that block the boss-focus lane.
  3. Commit burst onto Zalera before Doom/status/item debt overwhelms the chain.
```

The crypt should say: "the dead crowd the way while the Seraph steals your turns; keep your people
acting, open one lane, and end the status engine."

## Simulation Plan and Results

Simulation artifact:

```text
tmp/fft-level-design-049-limberry-undercroft/
  assumptions.md
  simulate.py
  iteration-results.json
  iteration-results.md
```

Model scope:

```text
Coarse deterministic status-Lucavi and chain-tax model over the first six rounds.
It scores pressure, status clarity, answerability, chain tax, hard-lock risk, undead cleanup risk,
reward correctness, scripting fidelity, and guest safety. It does not simulate exact FFT status formulas.
```

Result summary:

| Candidate | Pressure | Status clarity | Answer | Chain tax | Hard lock | Cleanup | Reward | Scripting | Guest | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| v2 status-Lucavi with undead screen | 301 | 94 | 93 | 60 | 14 | 28 | 100 | 100 | 100 | **Accepted** |
| hard-lock Death Seraph | 355 | 68 | 61 | 72 | 66 | 28 | 100 | 100 | 100 | Rejected: hard lock |
| living support engine | 329 | 80 | 79 | 70 | 26 | 36 | 100 | 100 | 100 | Rejected: second engine |
| clear-all undead slog | 349 | 94 | 48 | 70 | 14 | 62 | 100 | 60 | 100 | Rejected: breaks objective |
| active AI Meliadoul risk | 301 | 94 | 93 | 60 | 14 | 28 | 100 | 100 | 30 | Rejected: guest AI |
| fake-equipped Zalera reward | 301 | 94 | 93 | 60 | 14 | 28 | 75 | 75 | 100 | Rejected: no-equip violation |
| steal-or-join reward | 301 | 94 | 93 | 60 | 14 | 28 | 21 | 100 | 100 | Rejected: reward policy |
| downplayed status exhale | 263 | 58 | 93 | 46 | 14 | 28 | 100 | 100 | 100 | Rejected: loses capstone |
| overlevelled crypt | 331 | 94 | 83 | 68 | 14 | 28 | 100 | 100 | 100 | Rejected: raw levels |
| extra undead body | 314 | 94 | 85 | 66 | 14 | 40 | 100 | 100 | 100 | Rejected: cleanup tax |
| sealed undead wall | 325 | 94 | 93 | 60 | 14 | 34 | 100 | 100 | 100 | Rejected: no focus lane |

Iteration decision:

```text
ACCEPT v2 status-Lucavi with undead screen.
Iteration 1 rejected the dense roster as too high-pressure if the undead form a sealed wall. Iteration 2
keeps the local ENTD roster but requires at least one boss-focus lane. Zalera remains the sole headline
engine, rewards stay guaranteed, and Meliadoul's slot is never a guest-AI skill check.
```

## Implementation Checklist

- [ ] Re-dump entry 457 and verify slot order, levels, spoils bytes, and slot 7 behavior.
- [ ] Preserve win condition: defeating Zalera ends the fight.
- [ ] Keep Zalera at `105`; undead guard at `103`.
- [ ] Preserve Zalera as the single mass-status source; no hard-lock cadence.
- [ ] Preserve undead/reraise identity and Phoenix Down/Holy/Seal Evil answers.
- [ ] Preserve or create at least one boss-focus lane through the undead screen.
- [ ] Do not fake-equip Aegis Shield or Zeus Mace on no-equip/fixed slots.
- [ ] Author/verify spoils: Aegis Shield + Zeus Mace, guaranteed and within the 3-item cap.
- [ ] Verify slot 7 Meliadoul is not active; if active, make her player-controlled and update this doc.
- [ ] Preserve buried map treasure as map treasure.
- [ ] Test as Limberry chain 3/3 with resources carried from `047` and `048`.

## Test Questions

- Does Zalera's status cadence allow cleanse/resist windows and avoid unavoidable party-wide lock?
- Can the player reach or target Zalera without clearing every undead body?
- Do undead bodies force real Phoenix Down/Holy/Seal Evil decisions without becoming a cleanup slog?
- Is Meliadoul inactive/join-only, or controllable if she appears active?
- Do Aegis Shield + Zeus Mace appear as guaranteed spoils without Steal or join-gear dependency?
- Does the full Limberry chain feel like Gate race -> Keep parry -> Undercroft status spike?

## Sources

- Game8, "Limberry Castle Undercroft Walkthrough (Battle 44)": public roster, objective, Zalera status
  identity, no-resupply chain, buried treasure, and Meliadoul recruitment context.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553204
- Final Fantasy Wiki, "Zalera" / "Limberry Castle": story/terrain context.
  https://finalfantasy.fandom.com/wiki/Zalera
- Local: `037-chapter-4-overview.md`, `046-poeskas-lake.md`, `047-limberry-gate.md`,
  `048-limberry-keep.md`, `chapter-4-rewards-implementation.md`, `spoils-of-war-reward-system.md`.
