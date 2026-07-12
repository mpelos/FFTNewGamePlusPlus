# 051 - Mullonde Cathedral Exterior (Murond Holy Place)

Status: 🧪 v3 implemented and deployed — in-game playtest pending
Chapter: 4 — "In the Name of Love"
Battle order: Battle 46 (Mullonde chain 1 of 3 — NO resupply across 46→47→48)
Target version: Enhanced v1.5.0
ENTD: global entry **460** (local 76, entd4)
File: `battle_entd4_ent.bin`

> **NG++ rewards applied (2026-06-27):** Staff of the Magi + Faerie Harp + kept minor spoil through
> guaranteed Spoils of War (`0x1e`), NG+ only, within the 3-item cap, no stealing required. Dragon Rod
> remains optional steal flavor only. Canonical map: `chapter-4-rewards-implementation.md`.

> **V3 gender correction (2026-07-12):** the original implementation changed only gender flags at
> ENTD `0x01`, leaving the generic sprite identity at male `0x80`. The corrected pair is s0 male
> `0x80/0x80` and s1-s5 female `0x81/0x40` at `0x00/0x01`. Positions, UnitIDs, control flags, jobs,
> equipment, and Spoils remain preserved.

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

Historical v2 redesign: preserve the six-caster opener and make the hidden roof White Mage the single
sustain engine. V3 now locks complete builds for all six slots, changes s1-s5 to female while keeping
the White Mage male, and preserves the healer-priority puzzle.

> V3 is implemented in the ENTD patch path and deployed to Reloaded-II. The single `Geomancer Female`
> build applies to both s2 and s3 so the original two-Geomancer composition remains intact. Direct
> in-game validation remains pending.

## V3 Locked Decisions

```text
GENDER:
  s0 White Mage: male.
  s1 Summoner: female.
  s2/s3 Geomancers: female.
  s4/s5 Orators: female.

LEVELS:
  s0: 102.  s1: 101.  s2/s3: 100.  s4/s5: 101.

BRAVE/FAITH:
  Preserve v2 targets: s0/s1 60/84; s2-s5 68/78.

REWARDS:
  Preserve guaranteed Staff of the Magi + Faerie Harp + minor spoil.
  Dragon Rod is no longer active steal flavor; s1 equips Rod of Faith.
```

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

STILL NEEDED FOR V3 IMPLEMENTATION:
- Verify hidden rooftop White Mage placement and at least two answers: reach, Silence, height-ignoring
  damage, or fast ranged pressure.
- Apply the locked v3 gender, level, ability, and equipment setup for s0-s5.
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
  - Staff of the Magi is visible on the White Mage and also remains in the guaranteed reward ledger.
  - Faerie Harp is reward payload only unless a future implementation intentionally creates a Bard role,
    which this design does not require.
  - Summoner equips Rod of Faith; Dragon Rod is removed from the v3 active loadout.

PRESERVE:
  - Buried map treasure remains vanilla map loot.
```

## Proposed Composition (New Game++ Mullonde Exterior v3)

Keep the local six-caster roster and positions. White Mage remains the hidden sustain priority target;
the Summoner and Orators sit at `101`, while the two Geomancers form the level-`100` floor.

| Slot | Role | Job | Level | Br/Fa | Purpose |
| ------ | ------ | ----- | ------- | --- | --------- |
| s0 | Male sustain engine / reward payload | White Mage | `102` | `60/84` | Hidden roof healer; Staff of the Magi; Ribbon + Sortilège protection. |
| s1 | Female charged AoE | Summoner | `101` | `60/84` | Rod of Faith summon pressure; Dragon's Heart safety. |
| s2 | Female terrain bruiser / reward payload | Geomancer | `100` | `68/78` | Martial Arts secondary; Faerie Harp spoil payload. |
| s3 | Female terrain bruiser | Geomancer | `100` | `68/78` | Second copy of the same Geomancer build. |
| s4 | Female ranged disruptor | Orator | `101` | `68/78` | Stoneshooter + Mana Shield/Manafont pressure. |
| s5 | Female ranged utility | Orator; Mime bucket Lv8 | `101` | `68/78` | Mythril Gun + Items utility; Speechcraft remains primary. |

Reasoning:

V3 preserves the reachable hidden-healer screen while making every caste distinct. The White Mage is
a protected fast sustain anchor; the Summoner is a Rod-of-Faith AoE threat; the Geomancers combine
Geomancy with Martial Arts; s4 is the Mana-Shield Stoneshooter battery, while s5 uses Mythril Gun and
Items through a Mime Lv8 bucket. The unchanged
six-body roster and low `100-102` band keep this as the chain opener rather than the Mullonde spike.

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

## Builds (v3 locked)

```text
White Mage s0 — male:
  - Level: 102.  Brave/Faith: 60/84.
  - Job bucket: White Mage; JobLevel: 8.
  - Primary: White Magicks.
  - Secondary: Items.
  - Reaction: Dragon's Heart.
  - Support: Swiftness (Swiftspell).
  - Movement: Movement +2.
  - Right hand: Staff of the Magi.  Left hand: None.
  - Head: Ribbon.  Body: Luminous Robe.  Accessory: Sortilège.
  - Ivalice Chronicles allows male units to equip Ribbon and perfumes; this loadout is legal and
    requires no gender-restriction exception or special verification.

Summoner s1 — female:
  - Level: 101.  Brave/Faith: 60/84.
  - Job bucket: Summoner; JobLevel: 8.
  - Primary: Summon.
  - Secondary: None.
  - Reaction: Dragon's Heart.
  - Support: Magic Attack Boost.
  - Movement: Movement +2.
  - Right hand: Rod of Faith.  Left hand: None.
  - Head: Ribbon.  Body: Black Robe.  Accessory: Sortilège.

Geomancers s2/s3 — female, identical builds:
  - Level: 100.  Brave/Faith: 68/78.
  - Job bucket: Geomancer; JobLevel: 8.
  - Primary: Geomancy.
  - Secondary: Martial Arts.
  - Reaction: Nature's Wrath.
  - Support: Magic Attack Boost.
  - Movement: Movement +3.
  - Right hand: Rune Blade.  Left hand: None.
  - Head: Lambent Hat.  Body: Power Garb.  Accessory: Japa Mala.

Orator s4 — female Stoneshooter disruptor:
  - Level: 101.  Brave/Faith: 68/78.
  - Job bucket: Orator; JobLevel: 8.
  - Primary: Speechcraft.
  - Secondary: None.
  - Reaction: Mana Shield.
  - Support: Arcane Strength (Magic Attack Boost).
  - Movement: Manafont.
  - Right hand: Stoneshooter.  Left hand: None.
  - Head: Lambent Hat.  Body: Wizard's Robe.  Accessory: Septième Sens.

Orator s5 — female Items utility:
  - Level: 101.  Brave/Faith: 68/78.
  - Main job: Orator; primary Speechcraft.
  - Job bucket: Mime; JobLevel: 8.
  - Secondary: Items.
  - Reaction: Mana Shield.
  - Support: Arcane Strength (Magic Attack Boost).
  - Movement: Manafont.
  - Right hand: Mythril Gun.  Left hand: None.
  - Head: Lambent Hat.  Body: Wizard's Robe.  Accessory: Septième Sens.
```

## Positioning Plan

```text
Cathedral exterior: White Mage starts hidden on the roof with healing sightlines, but at least two common
NG++ answers must reach it: height-ignoring damage, Silence, fast ranged pressure, Teleport/Ignore Height,
or a split-team route.

Preserve the vanilla ENTD tiles: s0 `(2,5)`, s1 `(2,7)`, s2 `(3,7)`, s3 `(6,7)`, s4 `(2,11)`,
and s5 `(3,11)`.

Summoner and Geomancers punish clumping as the party regroups. Orators occupy side lanes where they can
harass without hard-locking either deployment group. The player should feel the intended sequence:
identify the sustain, solve the roof, then clean the casters while preserving resources for Nave.
```

The cathedral steps should say: "the choir will not fall while the hidden healer keeps singing; reach
the roof, stop the sustain, and save strength for the altar."

## Historical v2 Simulation / v3 Test Plan

The results below describe the historical v2 caster screen. They do not validate v3's gender changes,
Rod-of-Faith Summoner, Martial Arts Geomancers, or the two
distinct Stoneshooter and Mythril-Gun/Items Orators. No new simulation is requested; direct in-game validation follows
implementation.

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

- [x] Re-dump entry 460 and verify slot order, rewards, and rooftop placement.
- [x] Preserve split deployment, positions, control flags, UnitIDs, and roof/height puzzle data.
- [x] Set coherent sprite/gender pairs at ENTD `0x00/0x01`: s0 male `0x80/0x80`; s1-s5 female
      `0x81/0x40`.
- [x] Set levels: s0 `102`; s1/s4/s5 `101`; s2/s3 `100`.
- [x] Preserve Br/Fa targets: s0/s1 `60/84`; s2-s5 `68/78`.
- [x] Apply the complete v3 abilities and equipment documented for every slot.
- [ ] Keep hidden White Mage sustain reachable/silenceable.
- [ ] Keep Orator status soft; no hard-control pile-up.
- [ ] Keep Summoner charge times intact.
- [x] Verify spoils: Staff of the Magi + Faerie Harp + minor spoil.
- [x] Equip s1 with Rod of Faith, removing the old Dragon Rod active steal flavor.
- [x] Keep s4 with Stoneshooter; give s5 Mythril Gun, Items secondary, and Mime bucket JobLevel 8.
- [x] Preserve buried map treasure by leaving map/event data untouched.
- [ ] Test as Mullonde chain 1/3 with resources carried into `052` and `053`.

## Test Questions

- Is the White Mage discoverable and reachable by at least two common NG++ answers?
- Are s1-s5 female while s0 remains male?
- Does the caster band fold once the healer is stopped?
- Does split deployment create route pressure without isolating one group into hard status?
- Does s4 retain Stoneshooter while s5 uses Mythril Gun, Items, and Mime bucket Lv8?
- Are both Mana-Shield/Manafont Orators answerable without becoming a ranged sustain lock?
- Does the Rod-of-Faith Summoner remain raceable with normal Summon charge times?
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
