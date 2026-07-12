# 053 - Mullonde Cathedral Sanctuary (Murond Holy Place)

Status: 🧪 v3 implemented/deployed — direct playtest pending
Chapter: 4 — "In the Name of Love"
Battle order: Battle 48 (Mullonde chain 3 of 3 — NO resupply across 46→47→48)
Target version: Enhanced v1.5.0
ENTD: global entry **462** (local 78, entd4)
File: `battle_entd4_ent.bin`

> **NG++ rewards applied (2026-06-27):** Ragnarok + Ribbon + Elixir/minor spoil through guaranteed
> Spoils of War (`0x1e`), NG+ only, within the 3-item cap, no stealing required. Ragnarok is both
> Zalbaag's active weapon and a guaranteed reward payload. Canonical map:
> `chapter-4-rewards-implementation.md`.

> **V3 implementation (2026-07-11):** Zalbaag received the complete equipment set from his Eagrose
> guest version. Entry 462 was patched in the embedded ENTD and deployed through a clean Release build;
> the installed DLL resource matches the source binary byte-for-byte.

## Current Implementation / Data Reality

```text
DATA REALITY (verified from current embedded entd4 dump, entry 462):
  slot 0 = Folmarv cutscene placeholder
           level 254, no gear; preserve untouched.

  slot 1 = Zalbaag
           job 51, level 105, JobLevel 8, complete setup, Eagrose guest equipment set.
           Secondary 63, reaction 424, support 466, movement 493.
           Spoils payload = 0x24 (Ragnarok).

  slots 2,3 = Archaeodaemons
              job 153, level 103, undead monster/fixed bodies.
              slot 2 spoils payload = 0xAB (Ribbon).
              slot 3 spoils payload = 0xF5 (Elixir/minor spoil).

  slot 4 = Ultima Demon
           job 154, level 103, monster/fixed body.

  slot 5 = job-51 script placeholder
           level 254; preserve untouched.

Current v3 implementation:
  Zalbaag = 105.
  Archaeodaemons and Ultima Demon = 103.
  Zalbaag carries Ragnarok / Venetian Shield / Grand Helm / Maximillian / Bracers.
  Ragnarok + Ribbon + Elixir are guaranteed reward payloads.
  Win-on-Zalbaag-falls must be preserved.
```

Locked v3 revision: preserve the complete v2 battle and change only Zalbaag's equipment. His undead
version uses the same loadout as guest Zalbaag in Eagrose. Levels, Brave/Faith, abilities, demon screen,
positions, placeholders, objective and guaranteed spoils remain unchanged.

```text
ZALBAAG V3 EQUIPMENT:
  Right hand: Ragnarok
  Left hand: Venetian Shield
  Head: Grand Helm
  Body: Maximillian
  Accessory: Bracers
```

> MULLONDE CHAIN: 46 (`051`) → 47 (`052`) → 48 (`053`), one loadout. This is the chain closer and the
> last reward payout before the no-resupply endgame gauntlet.

## Design Goal

```text
Make Mullonde Sanctuary the tragic chain closer: Zalbaag is the sole vampirism source and a Ragnarok
break threat, demons screen him with undead/reraise and Ultima pressure, and the player wins by freeing
the brother rather than clearing the room. Ragnarok + Ribbon are guaranteed spoils; the fight must not
become spreading vampire lock or sealed demon cleanup.
```

No active guests appear here. No guest-control implementation is needed for this battle.

## Original Battle

Objective:

```text
Defeat Zalbaag!   (the fight ends when Zalbaag falls; demons are optional)
```

Player deployment:

```text
Up to 5 units, including Ramza. No outfitter (chain 3/3).
```

Original enemy composition:

```text
Zalbaag Beoulve   (undead/vampire Ark Knight; Runeblade/equip-break; vampirism)
2x Archaeodaemon  (undead demon screen; reraise/HP-drain)
1x Ultima Demon   (Ultima pressure; optional target)
```

Public walkthrough details:

```text
Recommended level: ~60. Difficulty: 4/5 stars. Sanctuary interior.
The player is advised to counter vampirism with Holy Water/Japa Mala style answers, break or manage
Zalbaag's Runeblade, and use Holy/anti-undead tools against the demon screen. No buried treasure.
```

Design reading:

The Sanctuary is **the undead brother release fight**. The emotional center is not the demon screen; it
is Zalbaag, a Beoulve brother turned into an undead weapon. The player should feel pressure from two
recoverable boss demands: vampirism and Runeblade break. The demons matter because they make reaching
him costly, but they must not become the real objective.

For New Game++ the identity must stay: **cleanse or resist vampirism, answer Zalbaag's break threat, open the
demon screen, and defeat Zalbaag.**

## Local Data Confirmed / Data Still Needed

```text
CONFIRMED:
- Entry 462 is Mullonde Sanctuary.
- Slot 1 is active Zalbaag at level 105 with complete setup and the Eagrose guest equipment set.
- Slots 2/3 are Archaeodaemon undead monster/fixed bodies at level 103.
- Slot 4 is an Ultima Demon at level 103.
- Slots 0/5 are placeholders and should be preserved unless playtest proves active.
- Rewards are Ragnarok + Ribbon + Elixir/minor spoil guaranteed spoils.
- No active guests.

STILL NEEDED FOR V3 PLAYTEST:
- Verify win-on-Zalbaag-falls and optional demon cleanup.
- Confirm vampirism is sourced only from Zalbaag and is cleansable/non-spreading.
- Confirm Zalbaag's Ragnarok pressure remains answerable.
- Confirm demons screen without sealing Zalbaag behind mandatory cleanup.
- Confirm Ultima pressure is telegraphed/spaceable.
- Confirm Ragnarok + Ribbon + Elixir/minor spoil land as guaranteed spoils.
```

## Enemy Party Escalation (Chapter 4 rule)

```text
Headline engine: undead brother focus fight.
Supporting roles:
  - Zalbaag brings vampirism and Ragnarok pressure as the sole boss engine.
  - Archaeodaemons create undead/reraise pressure and drain tax.
  - Ultima Demon punishes clustering and slow play with telegraphed Ultima pressure.

WHY: adding generic guards or making every demon part of the objective would dull the tragedy. The
Chapter 4 escalation is the layered undead/break/status stack around one named brother.

CONSTRAINTS:
  - Win-on-Zalbaag remains.
  - Vampirism is one source only.
  - The Eagrose guest equipment set is reused exactly.
  - Ragnarok is active equipment and remains a guaranteed reward payload.
  - Demons screen, but do not seal, the boss.
  - No generic padding.
```

## Sanctioned Exceptions

```text
VAMPIRISM:
  Allowed as Zalbaag's identity. Guardrail: sole source, cleansable, non-spreading, and never a hard lock.

RUNEBLADE BREAK:
  Allowed as one answerable gear-break source. Guardrail: disarm/break protection/burst must work.

UNDEAD DEMON SCREEN:
  Allowed as reraise/anti-undead pressure. Guardrail: demons are optional because the objective is
  Zalbaag; at least one focus route must remain.

ULTIMA DEMON:
  Allowed as Chapter 4 demon pressure. Guardrail: Ultima is telegraphed and spaceable.

PRE-GAUNTLET REWARD PAYOUT:
  Ragnarok + Ribbon pay here through guaranteed spoils so the player has them before the final gauntlet.
```

## Rare/reward handling

```text
Guaranteed spoils for entry 462: RAGNAROK + RIBBON + ELIXIR/minor spoil.
These are delivered by the Spoils of War reward channel; the player must never be required to Steal.

COMBAT ROLE:
  - Zalbaag actively carries Ragnarok and the complete defensive equipment set copied from his Eagrose guest.
  - Ragnarok and Ribbon remain guaranteed reward payloads regardless of the active equipment.

PRESERVE:
  - No buried map treasure.
  - No Excalibur. Excalibur stays Orlandeau's.
```

## Proposed Composition (New Game++ Mullonde Sanctuary v3)

Keep the local boss + demon screen roster. Zalbaag is `105`; demons are `103`.

| Slot | Role | Unit type | Level | Br/Fa | Purpose |
| ------ | ------ | ----------- | ------- | --- | --------- |
| s1 | Boss / objective / reward payload | Zalbaag, undead Ark Knight | `105` | `90/78` | Sole vampirism source; Ragnarok pressure; defeat ends fight; Ragnarok spoil. |
| s2 | Undead screen / reward payload | Archaeodaemon | `103` | `88/76` | Reraise/drain pressure; Ribbon spoil. |
| s3 | Undead screen / minor reward | Archaeodaemon | `103` | `88/76` | Second undead screen body; Elixir/minor spoil. |
| s4 | Demon pressure | Ultima Demon | `103` | `88/76` | Telegraphed Ultima pressure; optional target. |

Script placeholders to preserve:

| Slot | Record | Handling |
|------|--------|----------|
| s0 | Folmarv cutscene placeholder | Preserve untouched unless proven active. |
| s5 | job-51 placeholder | Preserve untouched unless proven active. |

Reasoning:

The accepted design is **v2 undead-brother focus**. The simulation rejects spreading vampirism, clear-all
demon walls, generic padding, overleveling, and unspaceable Ultima. The battle is
hard because it layers vampire status, one gear-break source, undead reraise, and demon AoE on a chained
party, but it stays fair because the objective is still Zalbaag.

Rejected variants:

```text
- Spreading vampire lock: turns a curse into lost-turn collapse.
- Clear-all demon rite: breaks the brother focus objective.
- Sealed demon wall: makes demons mandatory cleanup.
- Chaos Blade Zalbaag: superseded; both Zalbaag encounters now use Ragnarok.
- Old Ribbon-only reward: contradicts current reward map.
- Steal-required Ribbon/Ragnarok: contradicts guaranteed spoils.
- Generic-padded Sanctuary: dulls the tragic boss fight.
- Overlevelled tragedy: replaces puzzle pressure with raw stats.
- Unspaceable Ultima Demon: removes positioning counterplay.
```

## Builds (boss + demon screen)

```text
Zalbaag:
  - Level 105, JobLevel 8.
  - Right hand: Ragnarok.
  - Left hand: Venetian Shield.
  - Head: Grand Helm.
  - Body: Maximillian.
  - Accessory: Bracers.
  - Vampirism: sole source, cleansable, non-spreading.
  - Reaction/Support/Move: complete boss setup already present.
  - Role: tragic focus target; defeat ends fight.

Archaeodaemons x2:
  - Level 103.
  - Preserve undead/reraise and drain pressure.
  - No human equipment setup; monster/fixed bodies.
  - Role: screen and anti-undead resource test.

Ultima Demon:
  - Level 103.
  - Preserve demon kit and telegraphed Ultima pressure.
  - Role: punish clumping/slow play, not the objective.
```

## Positioning Plan

```text
Sanctuary interior: Zalbaag anchors the altar/back-center. Archaeodaemons form a partial screen, not a
sealed wall. Ultima Demon sits on a flank where Ultima pressure is visible and spaceable.

The player should see the intended line:
  1. Prevent or cleanse vampirism.
  2. Disarm/protect against Ragnarok pressure.
  3. Open one lane through undead demons.
  4. Focus Zalbaag and end the chain.
```

The sanctuary should say: "your brother is the curse at the altar; quiet the demons only enough to
reach him, break the blade, and free him."

## Historical v2 Simulation / v3 Test Plan

Simulation artifact:

```text
tmp/fft-level-design-053-mullonde-sanctuary/
  assumptions.md
  simulate.py
  iteration-results.json
  iteration-results.md
```

Model scope:

```text
Coarse deterministic undead-brother focus model over the first six rounds.
It scores pressure, focus clarity, vampirism fairness, break fairness, demon cleanup risk, answerability,
reward correctness, and scripting fidelity. It does not simulate exact FFT formulas.
```

Result summary:

| Candidate | Pressure | Focus clarity | Vamp fair | Break fair | Cleanup risk | Answer | Reward | Scripting | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| v2 undead-brother focus | 316 | 96 | 92 | 90 | 34 | 98 | 100 | 100 | **Accepted** |
| spreading vampire lock | 432 | 96 | 8 | 90 | 34 | 76 | 100 | 100 | Rejected: hard vampirism |
| clear-all demon rite | 378 | 22 | 92 | 90 | 60 | 30 | 100 | 55 | Rejected: breaks focus |
| sealed demon wall | 350 | 40 | 92 | 90 | 42 | 74 | 100 | 100 | Rejected: sealed screen |
| active Ragnarok Zalbaag (historical) | 312 | 96 | 92 | 50 | 34 | 98 | 82 | 100 | Superseded by locked v3 equipment |
| old ribbon-only reward | 316 | 96 | 92 | 90 | 34 | 98 | 75 | 100 | Rejected: reward ledger |
| steal-required ribbon | 316 | 96 | 92 | 80 | 34 | 98 | 47 | 100 | Rejected: reward policy |
| generic-padded sanctuary | 342 | 82 | 92 | 90 | 46 | 86 | 100 | 82 | Rejected: padding |
| overlevelled tragedy | 344 | 96 | 92 | 90 | 34 | 86 | 100 | 100 | Rejected: raw levels |
| unspaceable ultima demon | 340 | 96 | 92 | 90 | 44 | 82 | 100 | 100 | Rejected: unspaceable Ultima |

Iteration decision:

```text
ACCEPT v2 undead-brother focus.
Zalbaag remains the objective and sole vampirism/break engine. Demons are pressure, not mandatory
cleanup. Ragnarok and Ribbon are guaranteed rewards, with Ragnarok also used as his active weapon.
The historical simulation rejected active Ragnarok, but the locked v3 equipment decision supersedes
that weapon-only verdict; direct in-game testing is the validation source for the revised loadout.
```

The v3 equipment-only revision is not re-simulated. Its combat impact will be validated directly
in-game; the v2 simulation above remains historical design context.

## Implementation Checklist

- [x] Re-dump entry 462 and verify slots, rewards, and placeholder data.
- [x] Preserve win-on-Zalbaag-falls data.
- [x] Keep Zalbaag at `105`; demons at `103`.
- [x] Equip Zalbaag: Ragnarok / Venetian Shield / Grand Helm / Maximillian / Bracers.
- [x] Preserve vampirism setup.
- [x] Preserve the demon screen.
- [x] Preserve Ultima Demon setup.
- [x] Preserve spoils: Ragnarok + Ribbon + Elixir, guaranteed and within the 3-item cap.
- [x] Preserve no buried treasure data.
- [ ] Test as Mullonde chain 3/3 after `051` and `052`.

## Test Questions

- Does the fight end immediately when Zalbaag falls?
- Is vampirism cleansable, single-source, and non-spreading?
- Does Ragnarok pressure remain fair without becoming a gear lock?
- Can the player reach Zalbaag without clearing every demon?
- Is Ultima pressure spaceable?
- Do Ragnarok + Ribbon appear as guaranteed spoils?
- Does the Mullonde chain end with the party taxed but ready for the point of no return?

## Sources

- Game8, "Mullonde Cathedral Sanctuary Walkthrough (Battle 48)": public roster, win condition, vampirism
  counterplay, Runeblade/break advice, demon screen, and no buried treasure.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553208
- Final Fantasy Wiki, "Zalbaag Beoulve": story context.
  https://finalfantasy.fandom.com/wiki/Zalbaag_Beoulve
- Local: `037-chapter-4-overview.md`, `051-mullonde-exterior.md`, `052-mullonde-nave.md`,
  `chapter-4-rewards-implementation.md`, `spoils-of-war-reward-system.md`.
