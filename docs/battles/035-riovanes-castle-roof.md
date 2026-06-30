# 035 - Riovanes Castle Roof — Elmdor & the Assassins

Status: ✅ implemented (v1, entry 433) — redesign plan v2 docs-only
Chapter: 3 — "The Valiant" — **CHAPTER FINALE**
Battle order: Battle 32 (after Riovanes Castle Keep) — **Riovanes chain 3 of 3 (close)**
Target version: Enhanced v1.5.0
ENTD: global entry **433** (local entry 49, `battle_entd4_ent.bin`)
File: `battle_entd4_ent.bin` (embedded NG+ swap)

Implemented composition (entry 433, vanilla-dump verified):

- s0 **Rapha** (job 41 Skyseer — protected guest, current control `00 84`) — L100 via direct ENTD
  level. v2 requirement: Rapha must be **player-controlled in NG+** while preserving the
  fail-on-death objective. Current gear is best-buyable/end-game support gear: Thief's Cap (168),
  Luminous Robe (206), Featherweave Cloak (234), Eight-fluted Pole (113).
- s3 **Elmdor** (job 27 Ark Knight) — L104; flees, no loot.
- s4 **Celia** (job 45 Assassin) — L103; flees, no loot.
- s5 **Lettie** (job 46 Assassin) — L103; flees, no loot.
- s1 (job-41 L5 Rapha clone) + s2 (job-18 L5 Netherseer/Marach-class) are scripting placeholders;
  leave untouched.

The v2 redesign keeps the race and flee trigger, but upgrades Elmdor/Celia/Lettie from level-only
enemies to complete Chapter 3 human setups. It does **not** add bodies, loot, or hard-lock status.

## Original Battle

Objective:

```text
Save Rapha! (protect objective; mission fails if Rapha is defeated.)
WIN CONDITION: force the enemy to flee. The moment Celia or Lettie reaches critical HP, Elmdor,
Celia, and Lettie retreat and the fight ends instantly. You drive them off; you do not kill them.
```

Player deployment:

```text
Up to 4 units, including Ramza. Protected NPC: Rapha.
On completion, Marach and Rapha are recruited.
CHAIN: arrives from the Keep on one loadout, closing the no-resupply Riovanes chain.
```

Original enemy composition:

```text
1x Elmdor  (Arc Knight — Iaido/draw-out style pressure, debuffs, teleport)
1x Celia   (Assassin — high mobility / teleport; dangerous status and instant-death tools)
1x Lettie  (Assassin — high mobility / teleport; dangerous status and instant-death tools)
```

Public walkthrough details:

```text
Recommended level: ~36. Difficulty: 2/5 stars. It is a race, not a slugfest.
Rooftop arena. Protect Rapha.
The intended play is to ignore Elmdor's noise and focus all damage on one assassin. As soon as one
assassin hits critical, all three enemies flee.
```

Design reading:

The Roof is **the chapter's coda: a race-to-flee under assassin pressure**. The player has just beaten
the hardest fight in the chapter, so this should not exceed Keep in attrition. Its challenge comes
from tempo and focus: control Rapha, keep her alive, pick Celia or Lettie, and burst one assassin to
critical before teleporting killers can punish the exposed objective. Elmdor is dangerous atmosphere
and debuff noise, not the target.

For New Game++ the identity is: **a 4-unit rooftop sprint where Rapha is protected but
player-controlled, Celia and Lettie showcase complete-but-fair Assassin builds, and the fight ends the
moment one assassin is pushed to critical. Nobody dies and nobody drops loot.**

## Local Data Confirmed

```text
Entry 433 / local entry 49 / battle_entd4_ent.bin:
  s0  Rapha       job 41 Skyseer      L100   protected guest; v2 requires player control in NG+
  s3  Elmdor      job 27 Ark Knight   L104   active enemy; flees
  s4  Celia       job 45 Assassin     L103   active enemy; flees
  s5  Lettie      job 46 Assassin     L103   active enemy; flees
  s1  Rapha clone job 41              L5     scripting placeholder
  s2  Netherseer  job 18              L5     scripting placeholder

Preserve: 4-unit deploy cap, protected-Rapha fail condition, flee-on-critical trigger, all-three-flee
escape behavior, rooftop geometry, and no-resupply chain close.
```

Job IDs:

```text
Skyseer / Rapha job id:     41
Arc Knight / Elmdor job id: 27
Celia Assassin job id:      45
Lettie Assassin job id:     46
```

## Enemy Party Escalation (Chapter 3 redesign)

```text
The new caste is built in: Celia and Lettie are the Assassin debut. The escalation is not "more
enemies"; it is a complete named trio whose kits create a short, dangerous race. Keep exactly
Elmdor + Celia + Lettie.
```

All three active human enemies get Chapter 3 complete setups: secondary, reaction, support, movement,
full legal equipment, and JobLevel 8. Because the fight is a coda, their instant-death/status tools
must be constrained: resistable, non-spam, and never a permanent lock.

## Sanctioned Exceptions

```text
PROTECTED GUEST:
  Rapha remains a fail condition, but she must be player-controlled in NG+. The skill check is player
  routing and tempo, not guest AI.

ASSASSIN status / instant-death:
  Celia and Lettie may use signature Assassin pressure, but it must be resistable and non-spam.
  No Stop/Don't Act/death chain that removes the race answer.

TELEPORT / high mobility:
  Allowed and intended. The assassins must threaten Rapha quickly, but the flee-on-critical trigger
  gives the player a short, clear escape route.

ELMDOR debuffs:
  Allowed as ignorable pressure. He should make the roof feel unsafe without becoming the win target.
```

## Boss Rare Loot

```text
None. Elmdor, Celia, and Lettie all flee, so this battle must not pay out enemy loot.
Masamune and the Genji set are best-tier Chapter 4 Limberry rewards, not Roof rewards.
```

The map's rare treasure (Jade Armlet / Elven Cloak / Orichalcum Dirk / Kodachi) is existing map
treasure, not boss loot; leave it as-is.

## Proposed Composition (New Game++ Riovanes Roof v2)

Keep the exact trio. Elmdor `104`; Celia/Lettie `103`; Rapha controlled by the player.

| Slot | Role | Job | Level | Br/Fa | Purpose |
| ------ | ------ | ----- | ------- | --- | --------- |
| s0 | Rapha (protected ally) | Skyseer (41) | `100` | `65/75` | Player-controlled objective; survive and help create the burst line. |
| s3 | Elmdor | Ark Knight (27) | `104` | `90/65` | Debuff/teleport noise; ignore unless he blocks the race. Escapes. |
| s4 | Celia | Assassin (45) | `103` | `90/60` | Teleporting killer; one valid focus target. Critical HP ends fight. |
| s5 | Lettie | Assassin (46) | `103` | `90/60` | Second teleporting killer; other valid focus target. Critical HP ends fight. |

Reasoning:

The faithful v2 move is to make the named trio complete without changing the objective. Celia and
Lettie become real Assassin showcases through mobility, dual-pressure, and resistable status/death;
Elmdor gets a complete but non-loot, non-Masamune setup; Rapha is controlled by the player so the
protect condition rewards positioning instead of punishing AI behavior. The difficulty sits in
choosing one assassin and ending the fight before the rooftop collapses, not in grinding down Elmdor.

Simulation result (`tmp/fft-level-design-035-riovanes-castle-roof/iteration-results.md`):

```text
v2 controlled-Rapha complete assassin race: Accepted.
Threat 161.0; Rapha survival 68.1; focus-race answer 72.7; answerability 100.0;
finale exhale 88.0.

Rejected: AI-Rapha race shell, third Assassin, hard-lock Assassin showcase, Elmdor loot slugfest,
and low-threat escort cleanup.
```

## Builds (complete human setup; no loot because all flee)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Rapha — Skyseer Protected Ally (Lv 100) — player-controlled in NG+

```text
Job: Skyseer (41)
Control: player-controlled in NG+ while preserving protected/fail-on-death objective
Gear: Thief's Cap (168), Luminous Robe (206), Featherweave Cloak (234), Eight-fluted Pole (113)
Behavior target: reposition, survive, and contribute to the burst line when safe.
```

Role: the objective. The player can save her by playing well, not by hoping the guest AI behaves.

### Elmdor — Ark Knight (Lv 104) — escapes, no drop

```text
Job: Ark Knight (27)   JobLevel: 8
Primary: Iaido / Arc-Knight pressure; soft debuffs only
Secondary: Item or low-commitment command, if legal
Reaction: defensive/evasion reaction
Support: Attack Boost (465) or legal offensive support
Movement: Teleport / Move +1 legal equivalent
Head/Body/Accessory: best legal non-Genji gear
Right hand: non-rare, non-Masamune katana

Guardrails: no Masamune, no Genji, no hard lock, no rare loot. He escapes.
```

Role: the intimidating noise. He should pressure the roof, but focusing him is usually wrong.

### Celia — Assassin (Lv 103) — escapes

```text
Job: Assassin (45)   JobLevel: 8
Primary: Assassin tools; resistable, non-spam status/death
Secondary: Item / Fundaments / legal utility command
Reaction: First Strike (453), Vanish, or legal evasion reaction
Support: Dual Wield if legal, otherwise legal speed/offense support
Movement: Teleport / high-mobility legal movement
Head/Body/Accessory: best legal non-rare speed/evasion gear
Weapons: non-rare knives/ninja blades; no Chapter 4 best loot
```

Role: primary focus option. If Celia hits critical, the trio flees.

### Lettie — Assassin (Lv 103) — escapes

```text
Job: Assassin (46)   JobLevel: 8
Primary: Assassin tools; resistable, non-spam status/death
Secondary: Item / Fundaments / legal utility command
Reaction: First Strike (453), Vanish, or legal evasion reaction
Support: Dual Wield if legal, otherwise legal speed/offense support
Movement: Teleport / high-mobility legal movement
Head/Body/Accessory: best legal non-rare speed/evasion gear
Weapons: non-rare knives/ninja blades; no Chapter 4 best loot
```

Role: second focus option and the crossfire threat. If Lettie hits critical, the trio flees.

## Positioning Plan

```text
Rapha starts exposed, but player control lets the player route her first safe move.
Elmdor anchors as debuff pressure and should not body-block the single-focus answer.
Celia and Lettie begin with teleport/high-mobility access to Rapha's side of the roof.
Preserve the 4-unit deploy cap, rooftop geometry, protected-Rapha fail condition, and
flee-on-critical trigger.
```

The Roof should say: "you cannot win by fighting everyone. Move Rapha, pick one assassin, and hit
hard enough that they vanish before the knives reach her."

## Implementation Checklist

- [x] Confirm entry 433 active slots and placeholder slots in the doc.
- [x] Confirm job IDs: Rapha 41, Elmdor 27, Celia 45, Lettie 46.
- [ ] Make Rapha player-controlled in NG+ while preserving protected/fail-on-death behavior.
- [ ] Preserve the 4-unit deploy cap and no-resupply chain close.
- [ ] Preserve the flee-on-critical trigger: either assassin critical -> all three enemies retreat.
- [ ] Give Elmdor complete setup without Masamune, Genji, rare loot, or hard lock.
- [ ] Give Celia and Lettie complete Assassin setups with constrained, resistable status/death.
- [ ] Preserve exact trio: no third Assassin, no generic reinforcements, no defeat-all conversion.
- [ ] Set/verify levels: Rapha `100`; Elmdor `104`; Celia/Lettie `103`.
- [ ] Set JobLevel `8` on Elmdor, Celia, and Lettie where the slots support it.
- [ ] Confirm no enemy rare loot here; Elmdor's iconic rewards stay in Chapter 4.
- [ ] Patch only through the correct future implementation layer; keep this redesign docs-only for now.
- [ ] Re-dump and diff after implementation; verify control, flee trigger, trio, 4-unit cap, and no loot.
- [ ] Test from a New Game+ save: a focused 4-unit squad can keep Rapha alive and end the fight by
      pushing one assassin to critical.

## Test Questions

- Is Rapha player-controlled in NG+ while still protected by the fail condition?
- Does pushing either Celia or Lettie to critical immediately end the battle?
- Are the assassins dangerous enough to force urgency without hard-locking the small squad?
- Is ignoring Elmdor still the correct read most of the time?
- Is there no enemy loot, with Masamune/Genji deferred to Chapter 4?
- Does the fight feel like a sharp coda after Keep, not a harder attrition wall?
- Does it close the Riovanes chain cleanly and set up the Chapter 4 Elmdor rematch?

## Sources

- Game8, "Riovanes Castle Roof Walkthrough (Battle 32)": roster, Save Rapha objective, recommended
  level, 4-unit deploy, flee-on-critical rule, focus-one-assassin plan, and treasure context.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553192
- Final Fantasy Wiki, "Elmdor" / "Celia and Lettie": story context, Assassin/Arc-Knight context, and
  Limberry rematch loot.
  https://finalfantasy.fandom.com/wiki/Elmdor
- Local: `docs/battles/024-chapter-3-overview.md` (chapter rules and guest-control requirement),
  `031-walled-city-yardrow.md` (Rapha protected-guest precedent), `034-riovanes-castle-keep.md`
  (Riovanes chain), and `tmp/fft-level-design-035-riovanes-castle-roof/` (coarse simulation and
  rejected variants).
