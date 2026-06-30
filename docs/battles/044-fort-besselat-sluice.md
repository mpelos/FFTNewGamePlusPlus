# 044 - Fort Besselat Sluice Gate (Bethla Garrison Sluice)

Status: 📝 redesign v2 planned (docs-only) — v1 implementation exists for entry 450
Chapter: 4 — "In the Name of Love"
Battle order: Battle 39 (after the Fort Besselat Wall, S or N)
Target version: Enhanced v1.5.0
ENTD: global entry **450** (local entry 66, `battle_entd4_ent.bin`)
File: `battle_entd4_ent.bin` (embedded NG+ swap) — `tools/battle_patch.py besselat_sluice`

> **NG++ reward applied (2026-06-27):** Kaiser Shield (s2, Knight). Guaranteed Spoils of War (ENTD 0x1e),
> NG+ only, within the 3-cap, no steal needed. Canonical map: `chapter-4-rewards-implementation.md`.

Current implementation (entry 450, vanilla-dump verified) — slots: s0,s1 Archer; s2,s3,s6,s7 Knight; s4,s5 Black Mage:
- s4 Black Mage L102 — AoE on high ground (priority); Mage Hat/shop Robe/Featherweave/shop Rod.
- s5 Black Mage→**Time Mage** L102 — Slows the lever-runner; **jl4** (Haste/Slow/Float only); shop Staff.
- s2,s3 Knight L102, s6,s7 Knight L101 — gate wall; Heavy gear/Runeblade/shop Shield; Rend innate.
- s0 Archer L102, s1 Archer L101 — lane chip (Windslash, two-hand).
- Lever objective + tiles (scripting) untouched; no boss; low Ch4 band. Kaiser Shield reward is applied
  through spoils; selectable map treasure (other layer) untouched.

Planned v2 redesign (docs-only in this pass): keep the one-Time-Mage lever-race engine, make every
active human complete, cap Rend at two Knights, and allow Kaiser Shield to be visible on one gate
Knight as role-fitting pressure while the reward remains guaranteed spoils.

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `037-chapter-4-overview.md`. Both Wall paths (`043`) converge HERE.

## Design Goal

```text
Make Bethla Sluice a hard objective-race map: the player can still rush the floodgate levers, but the
lever-runner is taxed by Slow, high-ground AoE, lane chip, and a limited-Rend Knight wall. Clearing
first must be safer; racing must remain viable. No Stop, no four-Rend gate, no objective conversion.
```

No active guests appear here. No guest-control implementation is needed for this battle.

## Original Battle

Objective:

```text
Open the water gate at Fort Besselat!   (pull the floodgate levers — the gate-open objective)
```

Player deployment:

```text
Up to 5 units, including Ramza. No guests.
```

Original enemy composition (verified via Game8, Battle 39):

```text
4x Knight       (heavy melee wall guarding the gate)
2x Archer       (ranged chip)
2x Black Mage   (AoE on the high ground near the levers — the priority threat)
```

Public walkthrough details:

```text
Recommended level: ~45.  Difficulty: 3/5 stars.  Deploy up to 5.
OBJECTIVE map: the mission completes by PULLING THE FLOODGATE LEVERS to open the water gate. You CAN
  win by operating the levers, but the walkthrough says it is "easier and safer to DEFEAT ALL ENEMIES
  FIRST" — clearing prevents counterattacks during the lever-pull.
THE THREAT — BLACK MAGES on HIGH GROUND near the gate: heavy AoE; the walkthrough says kill them first.
  A 4-Knight wall + 2 Archers screen the approach to the levers.
Outdoor fort terrain with elevation; levers positioned in the battlefield.
Rewards: 37,600 Gil; selectable treasure (Crystal Shield, Crystal Helm, Crystal Mail, Lambent Hat).
```

Design reading:

The Sluice is **the objective map**: not a kill-box but a **race to operate the floodgate levers**,
contested by a heavy Knight wall and AoE Black Mages dug in on the high ground above the gate. Its
identity is the **tension between the two valid lines** — sprint the levers (fast, risky: you eat
counterattacks) or clear the screen first (safe, slow). The lesson is *objective control under a
caster screen*: neutralize the AoE on the height, hold the chokepoint, then work the levers. After the
Wall (`043`), it's the payoff of the Bethla assault — the moment you flood the garrison.

For New Game++ the identity must stay: **a floodgate-lever objective map — race the gate or clear the
screen — defined by AoE Black Mages on the high ground and a Knight wall guarding the levers; the
objective is the demand, sharpened by one tempo wrinkle that makes the lever-race genuinely tense.**

## Local Data Confirmed / Data Still Needed

```text
CONFIRMED:
- Entry 450 is the Bethla Sluice ENTD entry.
- Current slots are 4 Knights + 2 Archers + 1 Black Mage + 1 Time Mage (swapped from Black Mage).
- Lever objective scripting is present and must remain the win condition.
- No active guest, no boss.
- Reward ledger maps this battle to Kaiser Shield guaranteed spoils.

STILL NEEDED FOR V2 IMPLEMENTATION:
- Confirm exact slot order before patching complete v2 kits.
- Confirm floodgate lever panels/event tiles remain untouched.
- Confirm whether OverrideEntryData carries level for this battle or leaves it at runtime scale.
- Preserve high-ground caster placement and Knight wall geometry.
- Preserve selectable treasure (Crystal Shield/Helm/Mail, Lambent Hat) as vanilla map loot.
```

Job IDs (carry over known, verify the rest in-game):

```text
77 = Archer            (confirmed)
Knight job id          (TBD - verify)
Black Mage job id      (TBD - verify)
Time Mage job id       (TBD - verify; the single swapped-in escalation slot)
```

## Enemy Party Escalation (Chapter 4 rule)

```text
CHANGE: swap ONE of the two Black Mages -> a TIME MAGE that SLOWS the player (and may Haste the Knights)
  to pressure the LEVER-RACE, while every active human receives a complete Chapter-4 kit.
WHY: the fight's identity is "race the floodgate vs. a caster screen." The single, fitting escalation is
  to tax the RACE itself: a Time Mage that Slows the player's lever-runner makes the "sprint the gate"
  line genuinely risky and rewards clearing the screen first — INTENSIFYING the existing objective
  tension without changing it. The other Black Mage keeps the AoE-on-high-ground threat the walkthrough
  is built around, so the "kill the casters first" read survives.
CONSTRAINT: Time Mage uses Haste/Slow/Float ONLY (no Stop/Immobilize/Don't Act) — sharpen the race,
  never hard-lock the runner (carried Ch2-Ch4 Time-Mage precedent, 038).
REJECTED DEFAULTS: no second Time Mage, no Stop/Don't Act, no four-Rend gate, no overlevelled screen,
  and no removal of the Time Mage. The objective tension needs one tempo lever, not a lockdown stack.
WHAT IS NOT CHANGED: the floodgate-lever objective, the 4-Knight wall, the Archers, and the remaining
  AoE Black Mage on the height remain. No brand-new caste, no boss.
```

## Sanctioned exceptions (carried precedents)

```text
TIME MAGE CONTROL — Haste/Slow/Float only, normal cast cadence; no hard lock (038 precedent).
BLACK MAGE AoE — boosted elemental on the high ground; the priority kill; race-able by reaching it.
KNIGHT REND / BREAK — limit to ≤2 of the 4 Knights (carried ≤2-break-source cap); telegraphed,
  Safeguard/Steal answers. (A 4-Knight wall must NOT be a 4-source break-lock.)
OBJECTIVE TILES (floodgate levers) — preserved as the win condition; not an exception, the core puzzle.
ROLE-FITTING KAISER SHIELD — allowed on one Knight as visible Chapter-4 gear because it fits the gate
  wall role; reward still pays through spoils.
```

## Rare/reward handling

```text
Guaranteed spoils for entry 450: KAISER SHIELD.
This is delivered by the Spoils of War reward channel; the player must never be required to Steal.
COMBAT ROLE: Kaiser Shield may be equipped by one gate Knight as visible, role-fitting defensive
pressure. If playtest turns the wall into a slog, move it to reward payload only and resimulate.
PRESERVE: selectable map treasure (Crystal Shield/Helm/Mail, Lambent Hat) remains vanilla map loot and
is not the NG++ reward channel.
```

## Proposed Composition (New Game++ Bethla Sluice v2)

Keep the count (8) and the objective-map shape; one Black Mage becomes the Slow Time Mage. Every active
human has a complete but constrained kit. Modest Ch4 levels — no `103` spike (no boss; large screen).
Casters `102`; Knights `102`/`102`/`101`/`101`; Archers `102`/`101`.

| Slot | Role | Job | Level | Br/Fa | Purpose |
| ------ | ------ | ----- | ------- | --- | --------- |
| n | Black Mage | Black Mage | `102` | `60/84` | AoE on the high ground near the levers — priority kill. |
| n | Time Mage (NEW) | Time Mage | `102` | `62/80` | Slows the player's lever-runner — the objective-tempo wrinkle. |
| n | Kaiser Knight | Knight | `102` | `88/42` | Gate wall; Rend source 1; visible Kaiser Shield pressure. |
| n | Knight | Knight | `102` | `88/42` | Gate wall; Rend (break source 2 — cap reached). |
| n | Knight | Knight | `101` | `88/42` | Gate wall; NO Rend (cap kept). |
| n | Knight | Knight | `101` | `88/42` | Gate wall; NO Rend (cap kept). |
| n | Archer | Archer | `102` | `82/45` | Ranged chip over the approach to the levers. |
| n | Archer | Archer | `101` | `82/45` | Second archer; covers the lever lanes. |

Reasoning:

The faithful move is to **keep the floodgate objective central and tax the race by one degree**. One
Black Mage stays as the AoE-on-the-height threat (kill it first); the swapped-in Time Mage Slows the
runner so "just sprint the levers" is risky and clearing the screen first is rewarded — exactly the
tension the original is built on, raised a notch. The 4-Knight wall (Rend capped to two) guards the
gate; two Archers cover the lanes. Levels stay low Ch4 band (`101`–`102`, no `103`) because this is a
large boss-less screen on an objective map, not a spike.

Rejected variants:

```text
- v1 partial setup: correct objective engine, but incomplete for Chapter 4 humans.
- No Time Mage: too little lever tension for Chapter 4.
- Double Time Mage: turns the race into tempo control rather than objective choice.
- Four-Rend gate wall: violates the two-break-source cap.
- Hard-control runner trap: invalidates the lever race.
- Overlevelled gate: makes the objective map a spike before Limberry.
- Spoils-only shield: acceptable fallback, but too soft in the paper model if active Kaiser tests fair.
```

## Builds (Chapter-4 quality; garrison-floodgate flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Black Mage (Lv 102) — AoE on the height

```text
Job: Black Mage (id TBD)   JobLevel: 8
High-tier AoE (Fire/Bolt/Ice 3-tier). Black-Robe-equivalent body. Starts on the high ground by the gate.
Secondary: Item, limited to Ether/Remedy/self-care; no Time Magic or hard control.
Reaction: Reflexes (449)   Support: MA/Magick-boost (id TBD)   Movement: Movement +1 (486)
Head: mage hat (id TBD)   Body: Black Robe-equivalent (id TBD)
Accessory: Featherweave Cloak (234)   Right hand: magic-boost rod (id TBD)   Left: none (255)
```

Role: the priority kill — AoE over the levers; reaching/killing it is the safe line.

### Time Mage (Lv 102) — NEW (objective tempo)

```text
Job: Time Mage (id TBD)   JobLevel: 8
Cast SLOW on the player's lever-runner (and Haste on the Knights). Haste/Slow/Float ONLY — no hard lock.
Secondary: Item, limited to Ether/Remedy/self-care; no Stop/Don't Act/Petrify/Death.
Reaction: Reflexes (449)   Support: MA/Magick-boost (id TBD)   Movement: Movement +1 (486)
Head: mage hat (id TBD)   Body: shop robe (id TBD)
Accessory: Featherweave Cloak (234)   Right hand: magic-boost rod (id TBD)   Left: none (255)
```

Role: taxes the lever-race; makes "sprint the gate" risky and "clear first" rewarding.

### Knight x4 (Lv 102/102/101/101) — gate wall

```text
Job: Knight (id TBD)   JobLevel: 8   Primary: basic + Rend (ONLY 2 of 4 — cap)
Secondary: Item, limited to Potion/Hi-Potion/Remedy style stabilization; no Phoenix Down/Elixir.
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head: shop helm (id TBD)   Body: shop heavy armor (id TBD)   Accessory: Bracers (218)
Right hand: shop knight sword (id TBD)   Left: Kaiser Shield on one Lv102 Knight; shop shield on others
```

Role: the body wall guarding the levers; Rend on at most two (cap) — never a 4-source break-lock.
The two Lv101 Knights have complete equipment/reaction/support/movement but no Rend enabled.

### Archer x2 (Lv 102/101) — lane chip

```text
Job: Archer (77)   JobLevel: 8   Secondary: Item, limited to Potion/Remedy utility; no Phoenix Down loop.
Reaction: Reflexes (449)   Support: Concentration (469)   Movement: Movement +1 (486)
Head: Thief's Cap (168)   Body: Black Garb (198)   Accessory: Bracers (218)
Right hand: shop high-tier bow (id TBD)   Left: none / two-hand marker (254)
```

Role: ranged chip covering the approach to the levers.

## Positioning Plan

```text
Outdoor fort, elevation: the floodgate LEVERS sit in/near the contested ground; the Black Mage starts
  on the HIGH GROUND with AoE sightlines over the levers; the Time Mage tucked behind it (Slow range on
  the lever approach); the 4 Knights form the wall between the player's start and the levers; the 2
  Archers on the flanking parapets.
Preserve the LEVER objective tiles and the height (the Black-Mage-over-the-gate threat is the puzzle).
Place the wall so the player must either fight through to the levers or accept counterattacks for a
  fast pull — keep BOTH lines viable (do not make the rush impossible or trivial).
Modest levels — a large boss-less objective screen, not a spike.
```

The gate should say: "open the floodgate and drown Bethla's advance — but the mages own the high
ground over the levers, so clear them or race the water under fire."

## Simulation Plan and Results

Simulation artifact:

```text
tmp/fft-level-design-044-fort-besselat-sluice/
  assumptions.md
  simulate.py
  iteration-results.json
  iteration-results.md
```

Model scope:

```text
Coarse deterministic objective-pressure model over the first five rounds.
It scores pressure, lever tension, clear-first viability, race viability, break fairness, answerability,
and hard-lock risk. It does not simulate exact FFT formulas.
```

Result summary:

| Candidate | Pressure | Lever tension | Clear-first | Race | Break fairness | Answer | Hard lock | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| v1 partial lever screen | 183 | 100 | 84 | 76 | 74 | 82 | 0 | Rejected: incomplete setup |
| v2 complete lever siege | 192 | 100 | 84 | 76 | 74 | 82 | 0 | **Accepted** |
| no time mage clear map | 198 | 59 | 84 | 69 | 74 | 82 | 0 | Rejected: too little objective tension |
| double time lock | 204 | 37 | 68 | 51 | 74 | 62 | 0 | Rejected: too much tempo control |
| four-rend gate wall | 218 | 100 | 40 | 40 | 0 | 34 | 0 | Rejected: break cap violation |
| hard-control runner trap | 257 | 68 | 52 | 40 | 74 | 42 | 60 | Rejected: hard control |
| overlevelled gate | 216 | 100 | 76 | 68 | 66 | 74 | 0 | Rejected: too spiky |
| spoils-only shield | 185 | 98 | 84 | 86 | 74 | 82 | 0 | Rejected: too soft |

Iteration decision:

```text
ACCEPT v2 complete lever siege.
One Slow/Haste/Float Time Mage is enough to pressure the objective without deleting turns. Kaiser Shield
may be visible on one Knight because it fits the gate-wall role; rewards still pay through guaranteed
spoils. The two valid player lines remain: race the levers under fire, or clear the screen first.
```

## Implementation Checklist

- [ ] Confirm current entry 450 slot order: 4 Knight + 2 Archer + 1 Black Mage + 1 Time Mage + player slots.
- [ ] Confirm lever objective tiles/event scripting remain untouched.
- [ ] Keep the "open the water gate" lever objective intact (do NOT convert to plain defeat-all).
- [ ] Swap ONE Black Mage -> Time Mage (Slow the runner); Haste/Slow/Float only, no hard lock.
- [ ] Keep the other Black Mage on the high ground (AoE over the levers).
- [ ] Limit Rend to 2 of the 4 Knights (≤2-break-source cap).
- [ ] Give every active human complete equipment plus secondary/reaction/support/movement.
- [ ] Keep secondaries constrained to utility/self-care; no Phoenix Down loops, Stop, Don't Act, or hard control.
- [ ] Preserve guaranteed spoils: Kaiser Shield; preserve selectable map treasure.
- [ ] Set levels low Ch4 band (`101`-`102`, no `103`); JobLevel `8` on all active slots.
- [ ] Patch via the correct layer; keep the diff inside the Sluice window only.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify levers + objective intact.
- [ ] Install mod, test from a New Game+ save; confirm BOTH lines (race the gate / clear first) work.

## Test Questions

- Does the floodgate-LEVER objective still define the fight (both "race the gate" and "clear first"
  lines viable)?
- Is the AoE Black Mage on the high ground still the priority threat over the levers?
- Does the swapped-in Time Mage make the lever-race tense (Slow the runner) WITHOUT hard-locking it
  (Haste/Slow only)?
- Is the 4-Knight wall a fair screen with Rend capped to two (no break-lock)?
- Do all active humans have complete equipment plus secondary/reaction/support/movement?
- Does Kaiser Shield pay through guaranteed spoils, without requiring Steal?
- If Kaiser Shield is visible on a Knight, does it add gate-wall identity without making the wall a slog?
- Are levels kept low Ch4 band so this large objective skirmish isn't a spike before Limberry?
- Does it read as the Bethla floodgate — a tense objective map, not a kill-box?

## Sources

- Game8, "Fort Besselat Sluice Walkthrough (Battle 39)": roster (4 Knight + 2 Archer + 2 Black Mage),
  objective "Open the water gate at Fort Besselat!" (pull floodgate levers; safer to defeat all first),
  rec ~45, 3/5 stars, deploy 5, Black-Mage-on-high-ground priority, rewards (37,600 Gil; Crystal Shield/
  Helm/Mail, Lambent Hat). https://game8.co/games/Final-Fantasy-Tactics/archives/553071
- Final Fantasy Wiki, "Bethla Garrison": story/terrain context (the floodgate).
  https://finalfantasy.fandom.com/wiki/Bethla_Garrison
- Local: `037-chapter-4-overview.md` (rules), `043-fort-besselat-wall.md` (the converging Wall battle),
  `038-dugeura-pass.md` (Black Mage AoE + Time-Mage tempo precedent),
  `chapter-4-rewards-implementation.md` (Kaiser Shield guaranteed spoils).
