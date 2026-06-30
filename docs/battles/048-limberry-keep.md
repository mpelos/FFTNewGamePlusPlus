# 048 - Limberry Castle Keep

Status: 📝 redesign v2 planned (docs-only) — v1 implementation exists for entry 456
Chapter: 4 — "In the Name of Love"
Battle order: Battle 43 (Limberry chain 2 of 3 — NO resupply between 42→43→44)
Target version: Enhanced v1.5.0
ENTD: global entry **456** (local 72, entd4)
File: `battle_entd4_ent.bin`

> **NG++ rewards applied (2026-06-27):** Masamune + Genji Armor + Chirijiraden through guaranteed
> Spoils of War (`0x1e`), NG+ only, within the 3-item cap, no stealing required. Masamune and Genji
> Armor are also Elmdor's active story gear in the local data; Chirijiraden is the added reward payload.
> Canonical map: `chapter-4-rewards-implementation.md`.

## Current Implementation / Data Reality

```text
DATA REALITY (verified from entd4 dump):
  Entry 455 ([27,27,45,46], all lvl/eq 254) is an event/cutscene formation.
  Entry 456 is the PLAYABLE Limberry Keep battle.

  slot 0 = Elmdor (job 27 Ark Knight, name 0x1b)
           eq=(155, 183, 216, 46, 140)
           active story gear includes MASAMUNE (rh=46) + GENJI ARMOR (body=183).
           Shirahadori parry, Vampire drain, katana/Draw Out behavior, and boss AI are preserved.
  slot 1 = Celia  (job 45 Assassin) eq=254 fixed boss kit
  slot 2 = Lettie (job 46 Assassin) eq=254 fixed boss kit
  slots 3,4 = job 154, name-linked to Celia/Lettie -> scripted ULTIMA DEMON transform forms.

Current v1 implementation:
  Elmdor = 104
  Celia/Lettie = 104
  Ultima Demon transform forms = 105
  Win condition, Shirahadori, Vampire drain, fixed Assassin kits, transform scripting, and keep terrain
  are preserved. Rewards are guaranteed spoils, not steal-dependent.
```

Planned v2 redesign (docs-only in this pass): keep the exact scripted roster and turn the fight into
a sharper Chapter 4 puzzle: **crack Elmdor's Shirahadori and burst the objective while Celia/Lettie's
transform pressure acts as the timer**. Do not add bodies, do not make rewards steal-dependent, and do
not force normal generic gear/secondary planning onto fixed Assassin/transform slots.

> Data-layer fields are already known for entry 456, but final implementation still needs a fresh
> dump/diff on the Windows game data before patching. This pass updates documentation only.
> LIMBERRY CHAIN: 42 (`047`) → 43 (`048`) → 44 (`049`), one loadout.

## Design Goal

```text
Make Limberry Keep the hard middle fight of the Limberry chain: Elmdor is a parry-puzzle objective,
Celia/Lettie's Ultima Demon transform is the timer, and the player must solve the boss instead of
turning the map into a clear-all slog. The reward is guaranteed Masamune + Genji Armor + Chirijiraden,
never a Steal check through Shirahadori.
```

No active guests appear here. No guest-control implementation is needed for this battle.

## Original Battle

Objective:

```text
Defeat Elmdor!   (defeating Elmdor ends the battle)
```

Player deployment:

```text
Up to 5 units, including Ramza. No guests. NO outfitter access (chain 2/3).
```

Original enemy composition:

```text
Elmdor  (Ark Knight boss; Shirahadori parry, Vampire sustain, katana pressure)
Celia   (Assassin; returns from Gate, then transforms into Ultima Demon)
Lettie  (Assassin; returns from Gate, then transforms into Ultima Demon)
```

Public walkthrough details:

```text
Recommended level: ~60. Difficulty: 5/5 stars. Deploy up to 5. No resupply.
Win: "Defeat Elmdor!" Plain physical/sword attacks are punished by Shirahadori, while magic and
magic-sword style answers can get through. Celia and Lettie return and transform into Ultima Demons
after defeat, but the player does not need to clear them if Elmdor falls.
Buried map treasure: Muramasa, Vampire Cape, Icebrand, Spellbinder.
```

Design reading:

Limberry Keep is **the Elmdor reckoning**. The original designers made the objective Elmdor, not the
assassins, because the lesson is focus: identify why plain melee fails, use a different damage channel
or disarm route, and end the fight before the transform pressure turns the room into a resource sink.

For New Game++ the identity must stay: **a parry-race boss puzzle on no resupply**. The player should
feel smart for solving Shirahadori and committing to the objective, not punished for failing to clear
every demon form.

## Local Data Confirmed / Data Still Needed

```text
CONFIRMED:
- Entry 456 is the playable Limberry Keep battle.
- Entry 455 is a separate event/cutscene formation and is not the playable fight.
- Slot 0 is Elmdor, job 27 Ark Knight, with active Masamune and Genji Armor in local data.
- Slots 1/2 are Celia/Lettie fixed Assassin boss kits (eq=254).
- Slots 3/4 are the Celia/Lettie Ultima Demon transform forms.
- Win condition is "Defeat Elmdor."
- No active guests.
- Reward ledger maps this battle to Masamune + Genji Armor + Chirijiraden guaranteed spoils.

STILL NEEDED FOR V2 IMPLEMENTATION:
- Confirm exact Shirahadori counter behavior in TIC Enhanced: magic, sword-skill, disarm, and other
  reliable anti-parry lines.
- Confirm transform forms still trigger and do not need normal equipment setup.
- Confirm all three spoils land in the first three awarded `0x1e` slots.
- Confirm the chain transition into `049` stays intact.
- Preserve buried map treasure as vanilla map loot.
```

## Enemy Party Escalation (Chapter 4 rule)

```text
Headline engine: Elmdor's Shirahadori parry-race.
Supporting roles:
  - Elmdor is the objective and rare-gear story carrier.
  - Celia and Lettie force the player to act quickly.
  - Their Ultima Demon forms punish slow clear-first play.

WHY: the fight already has a complete Chapter 4 identity in the data: boss parry plus transform timer.
The correct escalation is not extra bodies or hidden immunity; it is making those scripted pieces matter
against a tuned NG++ party.

CONSTRAINTS:
  - Preserve "Defeat Elmdor" as the focus race.
  - Preserve fixed/scripted boss kits.
  - Keep Shirahadori readable and answerable, not a hard wall.
  - Keep Ultima Demon pressure telegraphed/spaceable.
  - Do not add a second headline engine such as hard status spam.
  - Do not make Masamune/Genji/Chirijiraden steal-dependent.
```

## Sanctioned Exceptions

```text
SHIRAHADORI PARRY:
  Allowed as Elmdor's signature. It pressures physical burst and forces alternate answers. Guardrail:
  at least two fair lines must remain live, such as magic, faith-independent sword skills, disarm/break,
  or objective burst after opening a timing window.

VAMPIRE SUSTAIN:
  Allowed as boss sustain. It rewards fast focus and denial; it must not become an infinite loop.

ULTIMA DEMON TRANSFORM:
  Allowed as the timer. It creates chain tax if the player spends too long, but it is not the objective.

FIXED BOSS KITS:
  Celia/Lettie and their transform forms are scripted/fixed slots. Do not invent normal equipment,
  secondary, reaction, support, or movement planning for those fixed slots unless future data proves the
  fields are safely editable.
```

## Rare/reward handling

```text
Guaranteed spoils for entry 456: MASAMUNE + GENJI ARMOR + CHIRIJIRADEN.
These are delivered by the Spoils of War reward channel; the player must never be required to Steal.

COMBAT ROLE:
  - Masamune and Genji Armor are active Elmdor gear in the local data and should remain visible story
    pressure where implementation preserves the existing equipment.
  - Chirijiraden is reward payload, not a required active combat item.

PRESERVE:
  - Celia/Lettie do not add separate equipment rewards.
  - Buried map treasure remains vanilla map loot, not the NG++ reward channel.
```

## Proposed Composition (New Game++ Limberry Keep v2)

Keep the five scripted enemy records: Elmdor, Celia, Lettie, and the two transform forms. No extra
bodies. Elmdor and assassins sit at `104`; transform forms sit at `105`.

| Slot | Role | Unit type | Level | Purpose |
|------|------|-----------|-------|---------|
| s0 | Boss / objective | Elmdor, Ark Knight | `104` | Shirahadori parry puzzle; Vampire sustain; active Masamune + Genji Armor; objective. |
| s1 | Timer phase 1 | Celia, Assassin fixed kit | `104` | Teleport/status/pressure; not the win condition. |
| s2 | Timer phase 1 | Lettie, Assassin fixed kit | `104` | Second assassin pressure; not the win condition. |
| s3 | Timer phase 2 | Celia-linked Ultima Demon | `105` | Transform pressure if the player spends too long. |
| s4 | Timer phase 2 | Lettie-linked Ultima Demon | `105` | Second transform pressure; chain tax, not required cleanup. |

Reasoning:

The accepted design is **v2 parry-race with demon timer**. Elmdor must be dangerous enough that plain
physical burst is the wrong first answer, but not so protected that the player needs a hidden solution.
Celia/Lettie keep the fight from becoming a static boss duel: if the player wastes turns clearing or
misroutes the parry answer, the transform forms tax HP/MP/items before the Zalera fight. Because the
win condition is Elmdor, the skill test is target priority under pressure.

Rejected variants:

```text
- Hard parry wall: turns Shirahadori into fake invulnerability.
- Extra demon body: adds cleanup tax before the chain's Lucavi capstone.
- Steal-required Genji payout: contradicts guaranteed reward policy and punishes physical Steal into
  the parry mechanic.
- Editable Assassin kits: violates fixed boss-kit data reality.
- Status pile-up Keep: adds an unrelated second headline engine.
- Demon-lite boss duel: removes the transform timer and makes the map too flat.
- Overlevelled Elmdor: replaces puzzle pressure with raw stats.
- Clear-all transform slog: breaks the "Defeat Elmdor" focus race.
```

## Builds (scripted boss fight — preserve fixed data)

```text
Elmdor:
  - Job: Ark Knight (job 27), JobLevel 8.
  - Preserve Shirahadori, Vampire sustain, katana/Draw Out behavior, and AI.
  - Preserve active Masamune + Genji Armor unless a future implementation pass proves the data must
    change for technical reasons.
  - Do not add blanket immunities or anti-magic protection that erase the parry answers.

Celia/Lettie:
  - Fixed Assassin boss kits (`eq=254`).
  - Preserve teleport/status/Ultima behavior and scripted links to transform forms.
  - Do not assign normal equipment or complete generic setups to these fixed slots.

Ultima Demon transform forms:
  - Preserve scripted transform behavior and demon kits.
  - Level `105` is the pressure spike, but the demons remain a timer/support threat because Elmdor is
    the objective.
```

## Positioning Plan

```text
Keep interior: Elmdor starts central/back as the objective the player must solve. Celia and Lettie
start split enough to threaten different approach lines and punish a slow setup. The transform forms
must preserve their scripted spawn/activation behavior.

The board should make the intended answer readable:
  1. Identify that plain physical attacks are failing into Shirahadori.
  2. Switch to magic, sword-skill, disarm/break, or other anti-parry answer.
  3. Burst Elmdor before Celia/Lettie's transform pressure consumes too many chain resources.
```

The keep should say: "the lord parries every blade; solve the parry and end him before the knives
become demons."

## Simulation Plan and Results

Simulation artifact:

```text
tmp/fft-level-design-048-limberry-keep/
  assumptions.md
  simulate.py
  iteration-results.json
  iteration-results.md
```

Model scope:

```text
Coarse deterministic parry-race and chain-tax model over the first six rounds.
It scores pressure, parry clarity, focus-race integrity, answerability, chain tax, hard-wall risk,
reward correctness, and scripting fidelity. It does not simulate exact FFT formulas.
```

Result summary:

| Candidate | Pressure | Parry clarity | Focus race | Answer | Chain tax | Hard wall | Reward | Scripting | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| v2 parry-race with demon timer | 236 | 94 | 91 | 91 | 54 | 8 | 100 | 100 | **Accepted** |
| hard parry wall | 270 | 64 | 91 | 61 | 62 | 52 | 100 | 100 | Rejected: hard wall |
| extra demon body | 260 | 84 | 73 | 79 | 68 | 8 | 100 | 100 | Rejected: cleanup tax |
| steal-required Genji payout | 236 | 94 | 91 | 75 | 54 | 16 | 22 | 100 | Rejected: reward policy |
| editable assassin kits | 236 | 94 | 91 | 91 | 54 | 8 | 100 | 65 | Rejected: fixed-kit violation |
| status pile-up keep | 278 | 94 | 91 | 69 | 70 | 28 | 100 | 100 | Rejected: second engine |
| demon-lite boss duel | 198 | 94 | 75 | 91 | 34 | 8 | 100 | 100 | Rejected: loses timer |
| overlevelled Elmdor | 262 | 94 | 91 | 81 | 64 | 8 | 100 | 100 | Rejected: raw-stat pressure |
| clear-all transform slog | 236 | 94 | 42 | 66 | 54 | 8 | 100 | 55 | Rejected: breaks objective |

Iteration decision:

```text
ACCEPT v2 parry-race with demon timer.
Keep the scripted roster, objective, fixed kits, and rewards. The fight becomes harder by making
Elmdor's parry answer and the transform timer matter, not by adding bodies, hard status, or hidden
immunity.
```

## Implementation Checklist

- [ ] Re-dump entry 456 and verify slot order: Elmdor, Celia, Lettie, two transform forms.
- [ ] Preserve entry 455 as event/cutscene formation unless a future implementation task proves it is active.
- [ ] Preserve win condition: defeating Elmdor ends the fight.
- [ ] Keep Elmdor at `104`; Celia/Lettie at `104`; transform forms at `105`.
- [ ] Preserve Elmdor's Shirahadori, Vampire sustain, katana behavior, Masamune, and Genji Armor.
- [ ] Preserve Celia/Lettie fixed boss kits and transform scripting.
- [ ] Do not add extra bodies, hard status, blanket anti-magic, or clear-all requirement.
- [ ] Author/verify spoils: Masamune + Genji Armor + Chirijiraden, all within the first 3 awarded items.
- [ ] Preserve buried map treasure as map treasure.
- [ ] Test as Limberry chain 2/3 with resources carried from `047` and into `049`.

## Test Questions

- Does Shirahadori read as a fair puzzle with at least two reliable answers?
- Can Elmdor be killed before the transform pressure becomes a slog?
- Does "Defeat Elmdor" reliably end the battle without requiring demon cleanup?
- Do Celia/Lettie and their transform forms tax the chain without becoming an unrelated hard-lock layer?
- Do Masamune + Genji Armor + Chirijiraden appear as guaranteed spoils without requiring Steal?
- Does the party enter the Undercroft meaningfully taxed but not crippled?

## Sources

- Game8, "Limberry Castle Keep Walkthrough (Battle 43)": roster, objective, Shirahadori/parry note,
  assassin transform context, no-resupply chain, and buried treasure.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553203
- Final Fantasy Wiki, "Elmdor" / "Limberry Castle": story/terrain context.
  https://finalfantasy.fandom.com/wiki/Elmdor
- Local: `037-chapter-4-overview.md`, `035-riovanes-castle-roof.md`,
  `047-limberry-gate.md`, `049-limberry-undercroft.md`, `chapter-4-rewards-implementation.md`,
  `spoils-of-war-reward-system.md`.
