# 049 - Limberry Castle Undercroft

Status: 🧪 v3 implemented — direct in-game playtest pending
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
CURRENT V3 IMPLEMENTATION (verified from embedded entd4 dump, entry 457):
  slot 0 = Elmdor cameo/script record
           job 27, level 43, JobLevel 8, eq=255 no gear.
           Preserve until in-game testing proves whether he is active; do not treat as a reward carrier.

  slot 1 = Zalera / Death Seraph
           job 62, level 102, JobLevel 8, secondary 108, eq=255 no normal equipment.
           Spoils byte = 0x88 (Aegis Shield).

  slots 2,3 = Archaeodaemon, job 153, level 100, JobLevel 8.
              Innate monster equipment/ability shape preserved; no human equipment.
              Slot 2 retains spoils byte 0x41 (Zeus Mace).

  slots 4,5,6 = Undead Knight, job 61, level 101, Monk bucket L8.
              Martial Arts / Counter / Dual Wield / Movement +3.
              Dual Rune Blades, Crystal Helm, Crystal Mail, Bracers.

  slots 8,9 = duplicate job-111 records visible in the raw ENTD dump, but not active in the observed
              battle. Preserve as inactive/script records until their gating is understood.

  slot 7 = Meliadoul join/post-battle record
           job 42, level 254, gear includes Save the Queen + Aegis Shield.
           Public battle shape has no active guest. Treat this as a join/post-battle record unless
           playtest proves it is active; if active, NG++ guest-control rule applies immediately.

Preserved v3 data:
  Win condition and Zalera mass-status identity.
  Original control flags, positions, UnitIDs, reward bytes, slot 0 cameo, and slot 7 join record.
  Inactive raw slots 8/9 remain byte-identical.
```

Implemented v3 redesign: replace the active s2-s6 guard with two Archaeodaemons and three Undead
Knights. All three copy the Martial Arts Knight build from Fort Besselat North Wall with Counter
replacing First Strike. Sharing one Knight sprite identity keeps the observed battle sprite budget
safe. Zalera remains s1 and the sole headline mass-status engine.
The player should resist/cleanse Zalera's curses, manage the dead, and focus the Death Seraph before the
end of the Limberry chain collapses into item/status debt.

> The embedded ENTD is implemented and mechanically validated. Direct playtest must still verify the
> special-job equipment, innate Undead behavior, active roster, slot 0/7 behavior, and boss cadence.
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

In-game roster correction:

```text
The raw ENTD contains five skeleton-family records, including three job-111 records, but direct in-game
observation confirms that only three skeleton-family units are active:
  one Skeleton (job 109) + one Bonesnatch (job 110) + one Skeletal Fiend (job 111).

Active enemy roster:
  Zalera + two job-61 Undead Knights + one of each skeleton-family unit = six enemies total.

Design consequence: preserve the observed six-enemy roster. Do not activate the duplicate job-111
records from slots 8/9. Positioning must still leave at least one
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
V3 IMPLEMENTATION CONFIRMED:
- Entry 457 is the playable Limberry Undercroft battle data.
- Slot 1 is Zalera, level 102, no normal equipment, reward payload Aegis Shield.
- Slots 2/3 are Archaeodaemons job `153`, level 100, with innate monster kits and no equipment.
- Slot 2 retains Zeus Mace as reward payload after the job swap.
- Slots 4/5/6 are job `61` Undead Knights with the adapted North Wall build at level 101.
- Slots 8/9 are duplicate job-111 records in the raw dump but do not appear in the observed battle;
  the patch leaves them byte-identical and outside the v3 active composition.
- Slot 7 is a Meliadoul join/post-battle record in the data and should not be used as a guest-AI check.
- No active guest is expected from the public battle shape.
- Reward ledger maps this battle to Aegis Shield + Zeus Mace guaranteed spoils.
- The patch changes only entry 457; positions, control flags, UnitIDs, objective/event data, and rewards
  are preserved. Sprite-sheet delta is `-1`; the Mystic sheet was removed to respect the observed
  in-game budget.

STILL NEEDED IN GAME:
- In-game verify whether slot 0 Elmdor and slot 7 Meliadoul are active, hidden, or join/script records.
- If slot 7 is active, set player control per global guest rule.
- Confirm job `61` preserves innate Undead while accepting the copied Monk job bucket, abilities, and
  explicit equipment fields in slots 4/5/6.
- Confirm s2/s3 accept Archaeodaemon job `153` with the innate monster kit and no human equipment.
- Confirm s4 matches the s5/s6 Undead Knight identity and build without sprite/palette corruption.
- Confirm duplicate slots 8/9 remain inactive.
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
  - Two Archaeodaemons create undead/reraise and drain pressure without equipment.
  - Three Undead Knights adapted from the North Wall Martial Arts Knight create the physical screen:
    Arts of War primary, Martial Arts secondary, Counter, Dual Wield, and dual Rune Blades.
  - Slot 7 Meliadoul is not a difficulty lever; she is join/post-battle data unless proven active.

WHY: this is the Limberry capstone. The six-enemy party is punishing, but it must remain one
readable puzzle: stop the status engine while managing undead bodies.

CONSTRAINTS:
  - Zalera is the one mass-status source.
  - Status must be resistable, cleansable, and non-locking.
  - Undead bodies must not seal every route to the boss.
  - No extra support caster, healer, or additional status engine.
  - Exactly three Arts of War sources: the s4/s5/s6 Undead Knights.
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

INACTIVE DUPLICATE ENTD RECORDS:
  Slots 8/9 are present in the raw data but absent from the observed battle. They are not active v3
  enemies and must remain inactive; the playable v3 roster is limited to s1-s6.

THREE ARTS OF WAR SOURCES:
  Allowed because all three job-61 bodies are Undead Knights. This raises equipment-break pressure,
  but removes the separate Mystic sprite sheet that exceeded the battle's observed sprite budget.

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
  - Zeus Mace remains reward payload on s2 after that slot becomes an Archaeodaemon; it is not equipped.
  - Meliadoul's join gear is not the canonical reward path.

PRESERVE:
  - Buried map treasure remains vanilla map loot.
  - Slot 7 join gear remains a separate recruitment/script concern.
```

## Proposed Composition (New Game++ Limberry Undercroft v3)

Use exactly the requested active s1-s6 roster. Zalera is the only `102`; all three Knights are `101`;
both Archaeodaemons are `100`. Do not activate raw duplicate records s8/s9.

| Slot | Role | Unit type | Level | Br/Fa | Purpose |
| ------ | ------ | ----------- | ------- | --- | --------- |
| s1 | Boss / objective | Zalera, Death Seraph Lucavi | `102` | `92/86` | Single mass-status engine; defeat ends fight; Aegis Shield spoil. |
| s2 | Demon / reward payload | Archaeodaemon, job 153 | `100` | `88/76` | Innate undead demon kit; reraise/drain pressure; Zeus Mace spoil remains payload only. |
| s3 | Demon | Archaeodaemon, job 153 | `100` | `88/76` | Second innate undead demon body on the opposite approach. |
| s4 | Bruiser | Job 61 Undead Knight, Monk bucket | `101` | `88/40` | Same adapted North Wall build; shares the Knight sprite sheet. |
| s5 | Bruiser | Job 61 Undead Knight, Monk bucket | `101` | `88/40` | Adapted North Wall Martial Arts Knight build; first Arts of War source. |
| s6 | Bruiser | Job 61 Undead Knight, Monk bucket | `101` | `88/40` | Same adapted build; second and final Arts of War source. |

Non-combat/script records to preserve and verify:

| Slot | Record | Handling |
|------|--------|----------|
| s0 | Elmdor cameo/script record | Preserve untouched unless playtest proves active; if active, redesign separately before implementation. |
| s7 | Meliadoul join/post-battle record | Preserve as join data; if active, make player-controlled in NG++. |
| s8/s9 | Duplicate job-111 raw records | Preserve inactive; do not include in the v3 enemy party. |

Reasoning:

The v3 design preserves the status-Lucavi objective while replacing the vanilla skeleton-family line.
Archaeodaemons provide innate undead/drain pressure, while the three Undead Knights provide capped
break and melee pressure on one shared sprite identity. All five
adds amplify the boss race instead of replacing Zalera as the priority target.

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

## Builds (Lucavi + Archaeodaemons + Undead Knights)

```text
Zalera:
  - Job: Death Seraph / Lucavi (job 62), JobLevel 8.
  - Preserve no-equipment Lucavi slot (`eq=255`).
  - Preserve mass-status identity through secondary/status kit.
  - Status is the one headline engine: visible, resistable, cleansable, non-locking.
  - Reward payload: Aegis Shield via spoils, not equipped gear.

Archaeodaemon x2 (slots 2/3, Lv 100):
  - Main job: Archaeodaemon (job 153); JobLevel 8.
  - Equipment: none; preserve the innate monster kit.
  - Preserve Undead/reraise and HP-drain pressure.
  - Brave/Faith: 88/76.
  - Slot 2 keeps Zeus Mace as reward payload only; it is not active equipment.

Undead Knight x3 (slots 4/5/6, Lv 101):
  - Main job: Undead Knight (job 61); preserve innate Undead and primary Arts of War.
  - Job bucket: Monk; JobLevel: 8.
  - Secondary: Martial Arts.
  - Reaction: Counter.
  - Support: Dual Wield.
  - Movement: Movement +3.
  - Right hand: Rune Blade.   Left hand: Rune Blade.
  - Head: Crystal Helm.   Body: Crystal Mail.   Accessory: Bracers.
  - Brave/Faith: 88/40.
  - This adapts the North Wall Martial Arts Knight build onto both bodies. The intentional differences
    are the Undead Knight main job and Counter in place of First Strike.

Meliadoul slot:
  - Treat as join/post-battle record.
  - If active, set player control and document her as an active guest before implementation.
```

## Positioning Plan

```text
Undercroft: Zalera starts central/back with clear mass-status sightlines. Archaeodaemons s2/s3 take
separate approaches, while Undead Knights s4/s5/s6 form the physical screen. At least one route must
let a prepared party reach or target Zalera
without full add cleanup. Slots 8/9 remain inactive.

The player should see three valid lines:
  1. Resist/cleanse enough status to keep turns.
  2. Permakill selected undead bodies that block the boss-focus lane.
  3. Commit burst onto Zalera before Doom/status/item debt overwhelms the chain.
```

The crypt should say: "the dead crowd the way while the Seraph steals your turns; keep your people
acting, open one lane, and end the status engine."

## Historical Simulation Record / v3 Test Plan

No new simulation was run for v3. Per the current workflow, this docs-only build will be validated by
direct in-game playtest after implementation. The artifact below records the older v2 screen/positioning
analysis only; it does not validate the v3 Archaeodaemons, copied Mystic, relocated Knights, or the
`100`-`102` level distribution. It also modeled raw duplicate skeleton records as active, an assumption
disproved by direct in-game observation; its roster-pressure numbers therefore remain historical only.

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
HISTORICAL RESULT: accept v2 status-Lucavi with undead screen as the structural base only.
Iteration 1 rejected the dense roster as too high-pressure if the undead form a sealed wall. Iteration 2
required at least one boss-focus lane. The old simulation assumed the two raw duplicate job-111 records
were active. The corrected v3 roster instead uses two Archaeodaemons and three Undead Knights sharing
one sprite identity. Zalera remains the sole headline engine, rewards stay guaranteed, and Meliadoul's slot
is never a guest-AI skill check.
```

## Implementation Checklist

- [x] Re-dump entry 457 and verify slot order, levels, spoils bytes, and slot 7 record bytes.
- [x] Preserve win condition data: defeating Zalera ends the fight; no event/script patch.
- [x] Set exact active composition: s1 Zalera; s2/s3 Archaeodaemon; s4/s5/s6 Undead Knight.
- [x] Set Zalera to `102`; all three Knights to `101`; both Archaeodaemons to `100`.
- [x] Move the two Undead Knight identities from s2/s3 to s5/s6.
- [x] Preserve duplicate job-111 slots 8/9 byte-identically; verify they remain inactive in game.
- [x] Keep slots 4/5/6 as job `61` Undead Knights with Arts of War primary.
- [x] Adapt the North Wall Martial Arts Knight build to all three: Monk bucket/JobLevel 8, Martial Arts,
  Counter, Dual Wield, Movement +3, dual Rune Blades, Crystal Helm, Crystal Mail, and Bracers.
- [ ] Verify explicit abilities/equipment work on the job-61 monster-type records without removing Undead.
- [x] Preserve Zalera's original mass-status kit; verify no hard-lock cadence in game.
- [x] Preserve innate undead/reraise jobs; verify Phoenix Down/Holy/Seal Evil answers in game.
- [x] Preserve original positions and boss-focus routes; verify their practical accessibility in game.
- [x] Do not fake-equip Aegis Shield or Zeus Mace on no-equip/fixed slots.
- [x] Preserve spoils: Aegis Shield + Zeus Mace, guaranteed and within the 3-item cap.
- [ ] Verify slot 7 Meliadoul is not active; if active, make her player-controlled and update this doc.
- [x] Preserve buried map treasure by leaving map/event data untouched.
- [ ] Test as Limberry chain 3/3 with resources carried from `047` and `048`.

## Test Questions

- Does Zalera's status cadence allow cleanse/resist windows and avoid unavoidable party-wide lock?
- Are all three job-61 units visibly Undead Knights—not Samurai or normal Knights—with innate Undead and
  Arts of War primary?
- Do s4/s5/s6 have the adapted North Wall build—including Counter, dual Rune Blades, and
  Martial Arts secondary—while slot 2 still awards Zeus Mace only as spoils?
- Is the three-source Arts of War pressure fair without creating an equipment-break wall?
- Can the player reach or target Zalera without clearing every undead body?
- Do undead bodies force real Phoenix Down/Holy/Seal Evil decisions without becoming a cleanup slog?
- Are s2/s3 Archaeodaemons using only their innate monster kit, with s2 still awarding Zeus Mace?
- Does s4 match the other Undead Knights and render without sprite/palette corruption?
- Does the active roster contain exactly Zalera, two Archaeodaemons, and three Undead Knights, with
  slots 8/9 inactive?
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
