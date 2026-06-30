# 051 - Mullonde Cathedral Exterior (Murond Holy Place)

Status: 📝 redesign v2 planned (docs-only) — v1 implementation exists for entry 460
Chapter: 4 — "In the Name of Love"
Battle order: Battle 46 (Mullonde chain 1 of 3 — NO resupply across 46→47→48)
Target version: Enhanced v1.5.0
ENTD: global entry **460** (local 76, entd4)
File: `battle_entd4_ent.bin`

> **NG++ rewards applied (2026-06-27):** Staff of the Magi + Faerie Harp + kept minor spoil through
> guaranteed Spoils of War (`0x1e`), NG+ only, within the 3-item cap, no stealing required. Dragon Rod
> remains optional steal flavor only. Canonical map: `chapter-4-rewards-implementation.md`.

## Current Implementation / Data Reality

```text
DATA REALITY (verified from current embedded entd4 dump, entry 460):
  slot 0 = White Mage
           job 79, level 103, JobLevel 8, full mage gear, reaction 449, support 465, movement 486.
           Spoils payload = 0x42 (Staff of the Magi reward slot).

  slot 1 = Summoner
           job 82, level 102, JobLevel 8, Dragon Rod, full mage gear, reaction 449, support 465,
           movement 486. Spoils payload = 0xF2 (kept minor/consumable spoil).

  slots 2,3 = Geomancers
              job 86, level 102, JobLevel 8, rods, full gear, Counter (442), support 465, movement 486.
              slot 2 spoils payload = 0x5E (Faerie Harp reward slot).

  slots 4,5 = Orators
              job 84, level 102, JobLevel 8, guns, full gear, reaction 449, support 465, movement 486.

Current v1 implementation:
  White Mage = 103.
  Summoner, Geomancers, Orators = 102.
  All six have full equipment and R/S/M.
  Secondary is currently unset/fixed in the dump, so v2 documentation requires intentional secondary
  planning before any future implementation pass.
```

Planned v2 redesign (docs-only in this pass): preserve the six-caster opener and make the hidden roof
White Mage the single sustain engine. The enemy side gets complete Chapter 4 caster kits, but the
secondaries must support the healer-priority puzzle rather than adding another headline engine.

> MULLONDE CHAIN: 46 (`051`) → 47 (`052`) → 48 (`053`), one loadout. This opener may tax actions and
> items, but it must leave enough resources for the triple-Templar Nave and Zalbaag Sanctuary.

## Design Goal

```text
Make Mullonde Exterior a complete but controlled chain opener: split deployment and rooftops reveal a
hidden White Mage sustain engine, the caster screen pressures both flanks, and the player must reach or
silence the healer before cleanup. It pays Staff of the Magi + Faerie Harp through guaranteed spoils,
but it must stay lighter than the two boss fights that follow.
```

No active guests appear here. No guest-control implementation is needed for this battle.

## Original Battle

Objective:

```text
Defeat all enemies!
```

Player deployment:

```text
Up to 5 units, including Ramza, split into two groups. No outfitter (chain 1/3).
```

Original enemy composition:

```text
1x White Mage   (hidden on the roof; heal/Raise sustain)
1x Summoner     (AoE caster; Dragon Rod steal flavor)
2x Geomancer    (terrain attacks)
2x Orator       (speech/status pressure)
```

Public walkthrough details:

```text
Recommended level: ~60. Difficulty: 3/5 stars. Cathedral exterior with rooftops and split deployment.
The hidden White Mage heals and raises enemies, so the player is told to find and kill that unit first.
The rest of the caster band pressures the split groups with terrain, speech/status, and summons.
Buried map treasure can include Elixir.
```

Design reading:

The Exterior is **the hidden-healer caster screen** that opens the Mullonde chain. Its job is not to
spike like Nave or Sanctuary; it is to make the player solve a priority target while already thinking
about resources for the next two fights. A tuned NG++ party can erase ordinary casters, so the healer
must matter. But if the healer is unreachable, or if both Orators become hard control, the opener drains
the chain before the actual bosses.

For New Game++ the identity must stay: **find the hidden healer, reach or silence it, then collapse the
caster screen.**

## Local Data Confirmed / Data Still Needed

```text
CONFIRMED:
- Entry 460 is Mullonde Cathedral Exterior.
- Six active human caster enemies occupy slots 0-5.
- Levels are White Mage `103`, all supports `102`.
- Every active enemy currently has full equipment and R/S/M.
- Current secondary fields are not yet an intentional complete-kit plan.
- Reward ledger maps this battle to Staff of the Magi + Faerie Harp + minor/Hi-Ether spoil.
- No active guests.

STILL NEEDED FOR V2 IMPLEMENTATION:
- Verify hidden rooftop White Mage placement and at least two answers: reach, Silence, height-ignoring
  damage, or fast ranged pressure.
- Give every active human an intentional secondary that supports the role without creating a second
  headline engine.
- Confirm Orator status remains soft and limited.
- Confirm Summoner charge times remain intact and race-able.
- Confirm Staff of the Magi + Faerie Harp + minor spoil land as guaranteed spoils.
- Preserve buried map treasure as vanilla map loot.
```

## Enemy Party Escalation (Chapter 4 rule)

```text
Headline engine: hidden rooftop White Mage sustain.
Supporting roles:
  - Summoner punishes clumped regrouping with charged AoE.
  - Geomancers pressure both split flanks through terrain.
  - Orators add soft disruption without becoming a hard-control engine.

WHY: this is a chain opener, not the chain spike. The full party can be complete and synergistic, but
the puzzle must remain "reach the healer" rather than "survive every caster engine at once."

CONSTRAINTS:
  - One sustain engine only.
  - Healer must be reachable or silenceable.
  - Orator status soft and limited.
  - Summoner charge windows intact.
  - No extra body, no boss, no hard lock.
```

## Sanctioned Exceptions

```text
HIDDEN-HEALER SUSTAIN:
  Allowed as the fight identity. Guardrail: reachable/silenceable, not a permanent revive lock.

SPLIT DEPLOYMENT:
  Preserved because it turns the opener into a route puzzle instead of a flat caster cleanup.

SOFT ORATOR STATUS:
  Allowed as harassment. Guardrail: no double hard-control lock and no Invitation/Charm-style collapse
  without counterplay.

GUARANTEED NON-BOSS SPOILS:
  Allowed by the Chapter 4 reward ledger. No named boss exists here, but Staff of the Magi and Faerie
  Harp are still guaranteed battle rewards.
```

## Rare/reward handling

```text
Guaranteed spoils for entry 460: STAFF OF THE MAGI + FAERIE HARP + kept minor/Hi-Ether spoil.
These are delivered by the Spoils of War reward channel; the player must never be required to Steal.

COMBAT ROLE:
  - Staff of the Magi may be visible on the White Mage only if legal and playtest-safe.
  - Faerie Harp is reward payload only unless a future implementation intentionally creates a Bard role,
    which this design does not require.
  - Dragon Rod stays optional steal flavor, not the canonical reward.

PRESERVE:
  - Buried map treasure remains vanilla map loot.
```

## Proposed Composition (New Game++ Mullonde Exterior v2)

Keep the local six-caster roster. White Mage is the priority target at `103`; the rest sit at `102`.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| s0 | Sustain engine / reward payload | White Mage | `103` | Hidden roof heal/Raise engine; Staff of the Magi spoil. |
| s1 | Charged AoE | Summoner | `102` | Punishes clumping/regrouping; Dragon Rod steal flavor; minor spoil. |
| s2 | Terrain pressure / reward payload | Geomancer | `102` | Flank pressure; Faerie Harp spoil payload. |
| s3 | Terrain pressure | Geomancer | `102` | Second flank pressure piece. |
| s4 | Soft disruptor | Orator | `102` | Speech/status harassment, not hard lock. |
| s5 | Soft disruptor | Orator | `102` | Second Orator, still under soft-status cap. |

Reasoning:

The accepted design is **v2 reachable hidden-healer screen**. Iteration 1 flagged raw caster pressure
above the original opener budget, but chain tax and hard-lock risk were controlled, so iteration 2
accepts the local six-caster roster as long as the healer is reachable and the Orators/Summoner do not
become a second hard engine.

Rejected variants:

```text
- Unreachable roof healer: hidden sustain becomes a lock.
- Hard-status Orator opener: steals turns instead of testing priority.
- Instant summon crossfire: removes charge-window counterplay.
- Double sustain roof: turns opener into revive slog.
- Extra caster body: adds cleanup to chain 1/3.
- Overlevelled opener: spends Nave/Sanctuary boss budget too early.
- Old no-rare/steal reward: contradicts Staff/Faerie guaranteed spoils.
- Weak healer screen: loses the original tactical lesson.
```

## Builds (complete caster kits)

```text
White Mage:
  - Level 103, JobLevel 8.
  - Primary: White Magic with real Cure/Raise sustain.
  - Secondary: limited Time Magic or Item, if legal; no Stop/hard control.
  - Reaction: Reflexes or current reaction 449.
  - Support: caster support if legal; avoid turning sustain into invulnerability.
  - Movement: Movement +1 or roof-appropriate mobility.
  - Gear: mage gear; Staff of the Magi visible only if legal/playtest-safe.

Summoner:
  - Level 102, JobLevel 8.
  - Primary: Summon with intact charge times.
  - Secondary: Item or light White Magic; no second sustain engine.
  - Reaction/Support/Move: complete caster setup.
  - Gear: Dragon Rod may remain optional steal flavor.

Geomancers x2:
  - Level 102, JobLevel 8.
  - Primary: Geomancy.
  - Secondary: Item/Fundaments/light utility.
  - Reaction/Support/Move: complete role setup.
  - Role: flank terrain pressure, not status lock.

Orators x2:
  - Level 102, JobLevel 8.
  - Primary: speech/status pressure.
  - Secondary: Item or light utility.
  - Reaction/Support/Move: complete role setup.
  - Guardrail: soft disruption only; no hard-control pile-up.
```

## Positioning Plan

```text
Cathedral exterior: White Mage starts hidden on the roof with healing sightlines, but at least two common
NG++ answers must reach it: height-ignoring damage, Silence, fast ranged pressure, Teleport/Ignore Height,
or a split-team route.

Summoner and Geomancers punish clumping as the party regroups. Orators occupy side lanes where they can
harass without hard-locking either deployment group. The player should feel the intended sequence:
identify the sustain, solve the roof, then clean the casters while preserving resources for Nave.
```

The cathedral steps should say: "the choir will not fall while the hidden healer keeps singing; reach
the roof, stop the sustain, and save strength for the altar."

## Simulation Plan and Results

Simulation artifact:

```text
tmp/fft-level-design-051-mullonde-exterior/
  assumptions.md
  simulate.py
  iteration-results.json
  iteration-results.md
```

Model scope:

```text
Coarse deterministic hidden-healer and chain-opener model over the first five rounds.
It scores pressure, sustain clarity, answerability, chain tax, hard-lock risk, reward correctness, and
chain pacing. It does not simulate exact FFT formulas.
```

Result summary:

| Candidate | Pressure | Sustain clarity | Answer | Chain tax | Hard lock | Reward | Chain pace | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| v2 reachable hidden-healer screen | 264 | 94 | 94 | 44 | 6 | 100 | 92 | **Accepted** |
| unreachable roof healer | 264 | 42 | 56 | 44 | 14 | 100 | 92 | Rejected: unreachable sustain |
| hard-status orator opener | 282 | 94 | 74 | 58 | 40 | 100 | 92 | Rejected: hard control |
| instant summon crossfire | 286 | 94 | 76 | 56 | 16 | 100 | 80 | Rejected: instant AoE wall |
| double sustain roof | 298 | 76 | 80 | 56 | 6 | 100 | 72 | Rejected: sustain slog |
| extra caster body | 290 | 94 | 82 | 56 | 6 | 100 | 76 | Rejected: cleanup |
| overlevelled opener | 290 | 94 | 84 | 58 | 6 | 100 | 70 | Rejected: overbudget |
| old no-rare/steal reward | 264 | 94 | 94 | 44 | 6 | 15 | 92 | Rejected: reward policy |
| weak healer screen | 204 | 76 | 94 | 28 | 6 | 100 | 82 | Rejected: loses puzzle |

Iteration decision:

```text
ACCEPT v2 reachable hidden-healer screen.
The opener can run six complete Chapter 4 caster kits because chain tax and hard-lock risk stay low.
The required guardrails are: reachable healer, soft status, charged summons, no extra bodies, and
guaranteed Staff/Faerie spoils.
```

## Implementation Checklist

- [ ] Re-dump entry 460 and verify slot order, rewards, and rooftop placement.
- [ ] Preserve split deployment and roof/height puzzle.
- [ ] Keep levels: White Mage `103`; all other enemies `102`.
- [ ] Add/verify intentional secondaries for every active human caster.
- [ ] Keep hidden White Mage sustain reachable/silenceable.
- [ ] Keep Orator status soft; no hard-control pile-up.
- [ ] Keep Summoner charge times intact.
- [ ] Author/verify spoils: Staff of the Magi + Faerie Harp + minor/Hi-Ether spoil.
- [ ] Preserve Dragon Rod steal flavor and buried map treasure separately from guaranteed rewards.
- [ ] Test as Mullonde chain 1/3 with resources carried into `052` and `053`.

## Test Questions

- Is the White Mage discoverable and reachable by at least two common NG++ answers?
- Does the caster band fold once the healer is stopped?
- Does split deployment create route pressure without isolating one group into hard status?
- Are Orator status and Summoner AoE answerable, with no hard lock?
- Do Staff of the Magi + Faerie Harp appear as guaranteed spoils?
- Does the party enter Nave taxed but not drained?

## Sources

- Game8, "Mullonde Cathedral Walkthrough (Battle 46)": public roster, split deployment, hidden White
  Mage priority, rooftop/height advice, Dragon Rod steal, and buried treasure.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553206
- Final Fantasy Wiki, "Mullonde" / "Murond Holy Place": story/terrain context.
  https://finalfantasy.fandom.com/wiki/Mullonde
- Local: `037-chapter-4-overview.md`, `052-mullonde-nave.md`, `053-mullonde-sanctuary.md`,
  `chapter-4-rewards-implementation.md`, `spoils-of-war-reward-system.md`.
