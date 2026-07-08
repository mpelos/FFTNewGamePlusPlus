# 044 - Fort Besselat Sluice Gate (Bethla Garrison Sluice)

Status: 📝 redesign v3 planned (docs-only) — v1 implementation exists for entry 450
Chapter: 4 — "In the Name of Love"
Battle order: Battle 39 (after Fort Besselat South Wall or North Wall)
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

Planned v3 redesign (docs-only in this pass): restore the second Black Mage, remove the Time Mage
lever-control engine, and make the floodgate pressure come from two Summon-secondary Black Mages, two
Knight lever guards with Samurai bucket data, two battle Knights upgraded into Samurai, and two Geomancers
that replace the Archer lane-chip slots.

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `037-chapter-4-overview.md`. Both Wall paths (`043`) converge HERE.

## Design Goal

```text
Make Bethla Sluice a hard objective-race map: the player can still rush the floodgate levers, but the
lever-runner is taxed by high-ground AoE, Summon pressure, crossbow gate guards, and a stronger melee
screen. Clearing first must be safer; racing must remain viable. No Stop, no four-Rend gate, no objective
conversion.
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
objective is the demand, sharpened by stronger high-ground magic and lever guards that make the race
genuinely tense.**

## Local Data Confirmed / Data Still Needed

```text
CONFIRMED:
- Entry 450 is the Bethla Sluice ENTD entry.
- Current slots are 4 Knights + 2 Archers + 1 Black Mage + 1 Time Mage (swapped from Black Mage).
- Planned v3 roster: 2 Black Mages + 2 lever Knights with Samurai bucket + 2 battle Samurais + 2
  Geomancers.
- Lever objective scripting is present and must remain the win condition.
- No active guest, no boss.
- Reward ledger maps this battle to Kaiser Shield guaranteed spoils.

STILL NEEDED FOR V3 IMPLEMENTATION:
- Confirm exact slot order before patching complete v3 kits.
- Confirm floodgate lever panels/event tiles remain untouched.
- Confirm whether OverrideEntryData carries level for this battle or leaves it at runtime scale.
- Preserve high-ground caster placement and Knight wall geometry.
- Confirm the former Archer slots can be converted to Geomancer with the documented gear.
- Preserve selectable treasure (Crystal Shield/Helm/Mail, Lambent Hat) as vanilla map loot.
```

Job IDs (carry over known, verify the rest in-game):

```text
77 = Archer            (confirmed)
Knight job id          (TBD - verify)
Black Mage job id      (TBD - verify)
Samurai job id         (TBD - verify)
Geomancer job id       (TBD - verify)
Summoner job id        (TBD - verify; Black Mage job bucket / secondary)
```

## Enemy Party Escalation (Chapter 4 rule)

```text
CHANGE: restore the second Black Mage and remove the Time Mage. Both Black Mages become Summoner-bucket
  casters with Summon secondary, while the four Knight slots split into two lever Knights and two battle
  Samurais.
WHY: the fight's identity is "race the floodgate vs. a caster screen." The v3 escalation keeps pressure
  on the objective through high-ground magic and stronger gate defenders instead of Slow control.
CONSTRAINT: no Time Mage hard-control layer here; Black Mage + Summon pressure must remain charge-time
  raceable. Lever Knights stay Knights with Samurai bucket data, while battle Knights become Samurais.
REJECTED DEFAULTS: no Time Mage, no Stop/Don't Act, no four-Rend gate, no overlevelled screen. The
  objective tension needs readable damage pressure, not tempo lockdown.
WHAT IS NOT CHANGED: the floodgate-lever objective, the 4 former-Knight wall footprint, and the two
  Black Mage caster slots remain. No boss.
```

## Sanctioned exceptions (carried precedents)

```text
BLACK MAGE AoE — boosted elemental on the high ground; the priority kill; race-able by reaching it.
SUMMON SECONDARY — allowed on the Black Mages as charge-time AoE pressure; no instant summons or hard
  status engine.
KNIGHT/SAMURAI WALL — lever guards remain Knights with Samurai bucket data; battle Knights become
  Samurais. Rend/break is removed from the v3 wall plan.
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

## Proposed Composition (New Game++ Bethla Sluice v3)

Keep the count (8) and the objective-map shape. Restore both Black Mages; split the old Knight wall into
two lever Knights and two battle Samurais; replace both Archers with Geomancers. Modest Ch4 levels — no
`103` spike (no boss; large screen). Casters `102`; front line `102`/`102`/`101`/`101`; Geomancers
`102`/`101`.

| Slot | Role | Job | Level | Br/Fa | Purpose |
| ------ | ------ | ----- | ------- | --- | --------- |
| n | Black Mage | Black Mage, Summoner bucket | `102` | `60/84` | High-ground AoE + Summon pressure near the levers. |
| n | Black Mage | Black Mage, Summoner bucket | `102` | `60/84` | Restored from Time Mage; second caster threat. |
| n | Lever Knight | Knight, Samurai bucket | `102` | `88/42` | On/near lever; Gastrophetes + Reflexes defensive guard. |
| n | Lever Knight | Knight, Samurai bucket | `102` | `88/42` | Second lever guard; mirrors the first. |
| n | Battle Samurai | Samurai bucket | `101` | `88/42` | Mobile battle screen; Dragon's Heart pressure sink. |
| n | Battle Samurai | Samurai bucket | `101` | `88/42` | Second battle Samurai; pushes the approach. |
| n | Geomancer | Geomancer bucket | `102` | `82/45` | Former Archer lane slot; Rune Blade + Aegis pressure. |
| n | Geomancer | Geomancer bucket | `101` | `82/45` | Second former Archer; terrain pressure and magic-boosted chip. |

Reasoning:

The faithful move is to **keep the floodgate objective central and tax the race through board pressure**.
Both Black Mages are restored as the AoE-on-the-height threats; Summon secondary makes ignoring them
costly without adding Time Mage control. The former Knight wall splits into lever guards and battle
Samurais, while the former Archers become Geomancers that make terrain and magic mitigation matter on the
approach. The player must decide between racing the levers under fire or clearing the screen first. Levels
stay low Ch4 band (`101`–`102`, no `103`) because this is a large boss-less screen on an objective map,
not a spike.

Rejected variants:

```text
- v1 partial setup: correct objective engine, but incomplete for Chapter 4 humans.
- v2 Time Mage: removed in v3; lever pressure now comes from damage, Summon, and stronger defenders.
- Double Time Mage: turns the race into tempo control rather than objective choice.
- Four-Rend gate wall: superseded; v3 removes Rend/break from the wall plan.
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

### Black Mage x2 (Lv 102) — AoE on the height

```text
Job: Black Mage (id TBD)   JobLevel: 8
Job bucket: Summoner   JobLevel: 8
High-tier AoE (Fire/Bolt/Ice 3-tier). Black-Robe-equivalent body.
Secondary: Summon
Reaction: Reflexes (449)   Support: Swift Spell   Movement: Movement +2
Head: Lambent Hat   Body: Black Robe
Accessory: Featherweave Cloak (234)   Right hand: Wizard's Rod
```

Role: priority kills — AoE and Summon pressure over the levers; reaching/killing them is the safe line.

### Lever Knight x2 (on the levers, Lv 102/102)

```text
Job: Knight
Job bucket: Samurai   JobLevel: 8
Secondary: Aim
Reaction: Reflexes
Support: Defense Boost
Movement: Movement +2
Right hand: Gastrophetes   Left hand: Crystal Shield
Head: Crystal Helm   Body: Reflect Mail   Accessory: Bracers
```

Role: hold the lever tiles from above/near the objective. They remain Knights, but use Samurai bucket data.

### Battle Samurai x2 (former battle Knights, Lv 101/101)

```text
Job: Samurai
Job bucket: Samurai   JobLevel: 8
Secondary: Aim
Reaction: Dragon's Heart
Support: Attack Boost
Movement: Movement +3
Right hand: Gastrophetes   Left hand: Crystal Shield
Head: Crystal Helm   Body: Reflect Mail   Accessory: Bracers
```

Role: active battle screen pushing the approach while the lever Knights and casters hold the objective.

### Geomancer x2 (former Archer slots, Lv 102/101)

```text
Job bucket: Geomancer   JobLevel: 8
Secondary: None
Reaction: Shihadori
Support: Magic Attack Boost
Movement: Movement +2
Right hand: Rune Blade   Left hand: Aegis Shield
Head: Lambent Hat   Body: Wizard's Robe   Accessory: Japa Mala
```

Role: replace Archer lane chip with terrain pressure and magic-leaning durability. Aegis Shield and Japa
Mala give them a defensive identity while Magic Attack Boost makes Geomancy matter.

## Positioning Plan

```text
Outdoor fort, elevation: the floodgate LEVERS sit in/near the contested ground; the two Black Mages start
  on the HIGH GROUND with AoE/Summon sightlines over the levers; the 2 lever Knights hold the lever tiles;
  the 2 battle Samurais form the mobile wall between the player's start and the levers; the 2 Geomancers
  take the former Archer lanes on the flanking parapets.
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

Result summary (v2 baseline; v3 needs refreshed simulation):

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

V3 note: this simulation is now stale. The Time Mage was removed, both Black Mages now carry Summon,
the Knight wall split into lever Knights + battle Samurais, and the Archers became Geomancers. Re-simulate
the completed v3 setup.
```

## Implementation Checklist

- [ ] Confirm current entry 450 slot order: 4 Knight + 2 Archer + 2 Black Mage + player slots, with one
  current Black Mage currently implemented as Time Mage in v1.
- [ ] Confirm lever objective tiles/event scripting remain untouched.
- [ ] Keep the "open the water gate" lever objective intact (do NOT convert to plain defeat-all).
- [ ] Remove the Time Mage and restore the slot to Black Mage.
- [ ] Give both Black Mages Summoner JobLevel 8 bucket data, Summon secondary, Reflexes, Swift Spell,
  Movement +2, Lambent Hat, Black Robe, Featherweave Cloak, and Wizard's Rod.
- [ ] Set the two Knights on the levers as Knights with Samurai bucket, Aim, Reflexes, Defense Boost,
  Movement +2, Gastrophetes, Crystal Shield, Crystal Helm, Reflect Mail, Bracers.
- [ ] Convert the two battle Knights to Samurais with Samurai bucket, Aim, Dragon's Heart, Attack Boost,
  Movement +3, Gastrophetes, Crystal Shield, Crystal Helm, Reflect Mail, Bracers.
- [ ] Convert both Archer slots to Geomancer JobLevel 8 units with no secondary, Shihadori, Magic
  Attack Boost, Movement +2, Rune Blade, Aegis Shield, Lambent Hat, Wizard's Robe, and Japa Mala.
- [ ] Give every active human complete equipment plus secondary/reaction/support/movement.
- [ ] Keep secondaries constrained; no Phoenix Down loops, Stop, Don't Act, or hard control.
- [ ] Preserve guaranteed spoils: Kaiser Shield; preserve selectable map treasure.
- [ ] Set levels low Ch4 band (`101`-`102`, no `103`); JobLevel `8` on all active slots.
- [ ] Patch via the correct layer; keep the diff inside the Sluice window only.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify levers + objective intact.
- [ ] Install mod, test from a New Game+ save; confirm BOTH lines (race the gate / clear first) work.

## Test Questions

- Does the floodgate-LEVER objective still define the fight (both "race the gate" and "clear first"
  lines viable)?
- Are the two Black Mages on the high ground still priority threats over the levers?
- Does removing the Time Mage keep the lever-race tense through damage/Summon pressure rather than Slow?
- Are the lever Knights and battle Samurais a fair screen without Rend/break-lock?
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
- Local: `037-chapter-4-overview.md` (rules), `043a-fort-besselat-south-wall.md` /
  `043b-fort-besselat-north-wall.md` (the converging Wall battles),
  `038-dugeura-pass.md` (Black Mage AoE precedent),
  `chapter-4-rewards-implementation.md` (Kaiser Shield guaranteed spoils).
