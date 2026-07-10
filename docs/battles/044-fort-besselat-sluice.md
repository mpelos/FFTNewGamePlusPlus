# 044 - Fort Besselat Sluice Gate (Bethla Garrison Sluice)

Status: ✅ v3 implemented and approved in-game (2026-07-10)
Chapter: 4 — "In the Name of Love"
Battle order: Battle 39 (after Fort Besselat South Wall or North Wall)
Target version: Enhanced v1.5.0
ENTD: global entry **450** (local entry 66, `battle_entd4_ent.bin`)
File: `battle_entd4_ent.bin` (embedded NG+ swap) — `tools/battle_patch.py besselat_sluice`

> **NG++ reward applied (2026-06-27):** Kaiser Shield (s2 reward carrier). Guaranteed Spoils of War (ENTD 0x1e),
> NG+ only, within the 3-cap, no steal needed. Canonical map: `chapter-4-rewards-implementation.md`.

Current v3 implementation (entry 450, vanilla-dump verified):
- s0/s1 Geomancer L102/L101 — former Archer lanes; Shirahadori, Magick Attack Boost, Movement +2,
  Rune Blade/Crystal Shield and MA gear.
- s2/s3 Battle Samurai L101 — mobile screen; no secondary, Dragon's Heart, Magick Attack Boost,
  Movement +3, Masamune/Crystal Shield and Reflect Mail.
- s4/s5 Black Mage L102 — Summoner bucket + Summon, Reflexes, Swiftspell, Movement +2 and full mage kit.
- s6/s7 Lever Knight L102 — confirmed on the lever tiles; main job Knight, Samurai bucket, Aim,
  Reflexes, Defense Boost, Movement +2, Gastrophetes/Crystal Shield and Reflect Mail.
- Lever objective, positions, static flags and event scripting remain untouched. Kaiser Shield stays a
  guaranteed s2 spoil; selectable map treasure remains untouched.

Implemented v3 redesign: the second Black Mage is restored, the Time Mage control engine is removed,
and floodgate pressure comes from two Summon-secondary Black Mages, two lever Knights, two battle
Samurais, and two Geomancers replacing the Archer lane-chip slots.

> Entry 450 and slots s0-s7 are confirmed. This implementation is an ENTD-only retune of existing
> static slots; no event script, objective tile, unit id, control flag, or position was changed.

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
- Vanilla slots are s0/s1 Archer, s2/s3/s6/s7 Knight, and s4/s5 Black Mage.
- Implemented v3 roster: 2 Black Mages + 2 lever Knights with Samurai bucket + 2 battle Samurais + 2
  Geomancers.
- In-game placement confirms s6/s7 are the lever protectors; s2/s3 are the mobile battle screen.
- Lever objective scripting is present and must remain the win condition.
- No active guest, no boss.
- Reward ledger maps this battle to Kaiser Shield guaranteed spoils.
- OverrideEntryData rows 450/0-7 leave the edited fields at `-1`; embedded ENTD is authoritative.
- All eight slots retain vanilla `0x90` static flags, unit ids `0x80`-`0x87`, positions, and facing.
- Sprite budget is vanilla 3 jobs -> v3 4 jobs, net `+1`, inside the documented safe band.
- Selectable treasure (Crystal Shield/Helm/Mail, Lambent Hat) remains vanilla map loot.

STILL NEEDED:
- In-game confirmation that the lever panels/objective behave unchanged.
- Confirm both player lines remain viable: race the levers and clear the screen first.
- Confirm learned Summons and forced crossbow/shield Samurai behavior are acceptable in practice.
```

Job IDs (carry over known, verify the rest in-game):

```text
76 = Knight
77 = Archer (vanilla slot identity; removed in v3)
80 = Black Mage
82 = Summoner (Black Mage bucket / secondary)
86 = Geomancer
88 = Samurai
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
COMBAT ROLE: v3 keeps Kaiser Shield in the reward payload only; both lever Knights use Crystal Shield.
This preserves the gate-wall identity without adding another evasion spike to the objective screen.
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
| n | Geomancer | Geomancer bucket | `102` | `82/45` | Former Archer lane slot; Rune Blade + Crystal Shield pressure. |
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
Secondary: None
Reaction: Dragon's Heart
Support: Magick Attack Boost
Movement: Movement +3
Right hand: Masamune   Left hand: Crystal Shield
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
Right hand: Rune Blade   Left hand: Crystal Shield
Head: Lambent Hat   Body: Wizard's Robe   Accessory: Japa Mala
```

Role: replace Archer lane chip with terrain pressure and magic-leaning durability. Crystal Shield and Japa
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
  iteration-1-results.json
  iteration-1-results.md
  iteration-2-results.json
  iteration-2-results.md
  iteration-results.md
```

Model scope:

```text
Coarse deterministic objective-pressure model over the first five rounds.
It scores pressure, lever tension, clear-first viability, race viability, break fairness, answerability,
and hard-lock risk. It does not simulate exact FFT formulas.
```

Result summary:

| Candidate | Pressure | Lever control | Clear-first | Race | Answer | Hard lock | Verdict |
|---|---:|---:|---:|---:|---:|---:|---|
| v3 uniform L102 | 19.69 | 22.46 | 70.0 | 53.8 | 71.9 | 0 | Rejected: race below threshold |
| v3 L101-102, crossbow/Aim Samurais | 19.09 | 21.89 | 71.2 | 55.3 | 73.2 | 0 | Historical baseline; Samurai kit superseded |

Iteration decision:

```text
The historical coarse model accepted the L101-102 band before the final Samurai equipment revision.
The first uniform-L102 pass made the mobile screen slightly too sharp and dropped race viability below
the model threshold. The final Battle Samurai kit — no secondary, Masamune, Magick Attack Boost — is not
re-simulated by request; it will be validated directly in game. Required playtest questions are whether
Masamune/Iaido pressure remains readable and whether the Crystal Shield screen creates cleanup drag.
```

## Implementation Checklist

- [x] Confirm entry 450 vanilla slot order: 4 Knight + 2 Archer + 2 Black Mage.
- [x] Preserve lever objective tiles/event scripting; no script or position bytes were edited.
- [x] Keep the "open the water gate" lever objective intact (do NOT convert to plain defeat-all).
- [x] Remove the Time Mage and restore the slot to Black Mage.
- [x] Give both Black Mages Summoner JobLevel 8 bucket data, Summon secondary, Reflexes, Swift Spell,
  Movement +2, Lambent Hat, Black Robe, Featherweave Cloak, and Wizard's Rod.
- [x] Set s6/s7 on the levers as Knights with Samurai bucket, Aim, Reflexes, Defense Boost,
  Movement +2, Gastrophetes, Crystal Shield, Crystal Helm, Reflect Mail, Bracers.
- [x] Convert s2/s3 battle Knights to Samurais with Samurai bucket, no secondary, Dragon's Heart,
  Magick Attack Boost, Movement +3, Masamune, Crystal Shield, Crystal Helm, Reflect Mail, Bracers.
- [x] Convert both Archer slots to Geomancer JobLevel 8 units with no secondary, Shihadori, Magic
  Attack Boost, Movement +2, Rune Blade, Crystal Shield, Lambent Hat, Wizard's Robe, and Japa Mala.
- [x] Give every active human complete equipment plus secondary/reaction/support/movement.
- [x] Keep secondaries constrained; no Phoenix Down loops, Stop, Don't Act, or hard control.
- [x] Preserve guaranteed spoils: Kaiser Shield; preserve selectable map treasure.
- [x] Set levels low Ch4 band (`101`-`102`, no `103`); JobLevel `8` on all active slots.
- [x] Patch through the embedded ENTD; diff is confined to entry 450.
- [x] Re-dump and validate the entry; flags, unit ids, positions and reward payload are preserved.
- [x] Install the mod and approve the final v3 setup in game.

In-game validation (2026-07-10): final v3 approved after correcting the lever-guard slot mapping,
changing the Battle Samurais to Masamune/Magick Attack Boost, and replacing the Geomancers' Aegis
Shields with Crystal Shields. Keep the race-vs-clear routes and reward delivery in the regression list.

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
