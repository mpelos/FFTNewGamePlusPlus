# 044 - Fort Besselat Sluice Gate (Bethla Garrison Sluice)

Status: ✅ implemented (v1, entry 450)
Chapter: 4 — "In the Name of Love"
Battle order: Battle 39 (after the Fort Besselat Wall, S or N)
Target version: Enhanced v1.5.0
ENTD: global entry **450** (local entry 66, `battle_entd4_ent.bin`)
File: `battle_entd4_ent.bin` (embedded NG+ swap) — `tools/battle_patch.py besselat_sluice`

Implemented (entry 450, vanilla-dump verified) — slots: s0,s1 Archer; s2,s3,s6,s7 Knight; s4,s5 Black Mage:
- s4 Black Mage L102 — AoE on high ground (priority); Mage Hat/shop Robe/Featherweave/shop Rod.
- s5 Black Mage→**Time Mage** L102 — Slows the lever-runner; **jl4** (Haste/Slow/Float only); shop Staff.
- s2,s3 Knight L102, s6,s7 Knight L101 — gate wall; Heavy gear/Runeblade/shop Shield; Rend innate.
- s0 Archer L102, s1 Archer L101 — lane chip (Windslash, two-hand).
- Lever objective + tiles (scripting) untouched; no boss/no rare; low Ch4 band. Selectable map treasure (other layer) untouched.

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `037-chapter-4-overview.md`. Both Wall paths (`043`) converge HERE.

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

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm slots: 4 Knight + 2 Archer + 2 Black Mage, plus the player slots, AND the floodgate LEVER
  panels / event tiles (the win-objective). Keep the "open the water gate" objective intact — it IS
  the fight (do NOT silently convert to plain defeat-all).
Keep the Black Mages on the HIGH GROUND near the levers (the AoE-over-the-gate threat) and the Knight
  wall guarding the approach.
This is a no-boss, no-rare OBJECTIVE skirmish: modest Ch4 levels (100-103), NOT a spike.
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
Leave the selectable treasure (Crystal Shield/Helm/Mail, Lambent Hat) as-is — map loot, not boss loot.
```

Job IDs (carry over known, verify the rest in-game):

```text
77 = Archer            (confirmed)
Knight job id          (TBD - verify)
Black Mage job id      (TBD - verify)
Time Mage job id       (TBD - verify; the single swapped-in escalation slot)
```

## Job Escalation (Chapter 4 rule)

```text
CHANGE: swap ONE of the two Black Mages -> a TIME MAGE that SLOWS the player (and may Haste the Knights)
  to pressure the LEVER-RACE.
WHY: the fight's identity is "race the floodgate vs. a caster screen." The single, fitting escalation is
  to tax the RACE itself: a Time Mage that Slows the player's lever-runner makes the "sprint the gate"
  line genuinely risky and rewards clearing the screen first — INTENSIFYING the existing objective
  tension without changing it. The other Black Mage keeps the AoE-on-high-ground threat the walkthrough
  is built around, so the "kill the casters first" read survives.
CONSTRAINT: Time Mage uses Haste/Slow/Float ONLY (no Stop/Immobilize/Don't Act) — sharpen the race,
  never hard-lock the runner (carried Ch2-Ch4 Time-Mage precedent, 038).
WHAT IS NOT CHANGED: the floodgate-lever objective, the 4-Knight wall, the Archers, and the remaining
  AoE Black Mage on the height remain. No brand-new caste, no boss, no rare.
```

## Sanctioned exceptions (carried precedents)

```text
TIME MAGE CONTROL — Haste/Slow/Float only, normal cast cadence; no hard lock (038 precedent).
BLACK MAGE AoE — boosted elemental on the high ground; the priority kill; race-able by reaching it.
KNIGHT REND / BREAK — limit to ≤2 of the 4 Knights (carried ≤2-break-source cap); telegraphed,
  Safeguard/Steal answers. (A 4-Knight wall must NOT be a 4-source break-lock.)
OBJECTIVE TILES (floodgate levers) — preserved as the win condition; not an exception, the core puzzle.
```

## Boss rare loot

```text
None. No named boss here — no rare boss item (per the Chapter 4 overview tiering). Generics stay
Chapter-4 shop-tier. The selectable map treasure (Crystal Shield/Helm/Mail, Lambent Hat) is EXISTING
map loot — leave it as-is.
```

## Proposed Composition (New Game++ Bethla Sluice v1)

Keep the count (8) and the objective-map shape; swap one Black Mage for a Slow Time Mage. Modest Ch4
levels — no `103` spike (no boss; large screen). Casters `102`; Knights `102`/`102`/`101`/`101`;
Archers `102`/`101`.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Black Mage | Black Mage | `102` | AoE on the high ground near the levers — priority kill. |
| n | Time Mage (NEW) | Time Mage | `102` | Slows the player's lever-runner — the objective-tempo wrinkle. |
| n | Knight | Knight | `102` | Gate wall; Rend (break source 1). |
| n | Knight | Knight | `102` | Gate wall; Rend (break source 2 — cap reached). |
| n | Knight | Knight | `101` | Gate wall; NO Rend (cap kept). |
| n | Knight | Knight | `101` | Gate wall; NO Rend (cap kept). |
| n | Archer | Archer | `102` | Ranged chip over the approach to the levers. |
| n | Archer | Archer | `101` | Second archer; covers the lever lanes. |

Reasoning:

The faithful move is to **keep the floodgate objective central and tax the race by one degree**. One
Black Mage stays as the AoE-on-the-height threat (kill it first); the swapped-in Time Mage Slows the
runner so "just sprint the levers" is risky and clearing the screen first is rewarded — exactly the
tension the original is built on, raised a notch. The 4-Knight wall (Rend capped to two) guards the
gate; two Archers cover the lanes. Levels stay low Ch4 band (`101`–`102`, no `103`) because this is a
large boss-less screen on an objective map, not a spike.

## Builds (Chapter-4 quality; garrison-floodgate flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Black Mage (Lv 102) — AoE on the height

```text
Job: Black Mage (id TBD)   JobLevel: 8   Secondary: none
High-tier AoE (Fire/Bolt/Ice 3-tier). Black-Robe-equivalent body. Starts on the high ground by the gate.
Reaction: Reflexes (449)   Support: MA/Magick-boost (id TBD)   Movement: Movement +1 (486)
Head: mage hat (id TBD)   Body: Black Robe-equivalent (id TBD)
Accessory: Featherweave Cloak (234)   Right hand: magic-boost rod (id TBD)   Left: none (255)
```

Role: the priority kill — AoE over the levers; reaching/killing it is the safe line.

### Time Mage (Lv 102) — NEW (objective tempo)

```text
Job: Time Mage (id TBD)   JobLevel: 8   Secondary: none
Cast SLOW on the player's lever-runner (and Haste on the Knights). Haste/Slow/Float ONLY — no hard lock.
Reaction: Reflexes (449)   Support: MA/Magick-boost (id TBD)   Movement: Movement +1 (486)
Head: mage hat (id TBD)   Body: shop robe (id TBD)
Accessory: Featherweave Cloak (234)   Right hand: magic-boost rod (id TBD)   Left: none (255)
```

Role: taxes the lever-race; makes "sprint the gate" risky and "clear first" rewarding.

### Knight x4 (Lv 102/102/101/101) — gate wall

```text
Job: Knight (id TBD)   JobLevel: 8   Primary: basic + Rend (ONLY 2 of 4 — cap)
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head: shop helm (id TBD)   Body: shop heavy armor (id TBD)   Accessory: Bracers (218)
Right hand: shop knight sword (id TBD)   Left: shop shield (id TBD)
```

Role: the body wall guarding the levers; Rend on at most two (cap) — never a 4-source break-lock.

### Archer x2 (Lv 102/101) — lane chip

```text
Job: Archer (77)   JobLevel: 8   Secondary: none
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

## Implementation Checklist

- [ ] Identify Bethla Sluice `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify 4 Knight + 2 Archer + 2 Black Mage + the lever objective tiles + player slots.
- [ ] Keep the "open the water gate" lever objective intact (do NOT convert to plain defeat-all).
- [ ] Swap ONE Black Mage -> Time Mage (Slow the runner); Haste/Slow/Float only, no hard lock.
- [ ] Keep the other Black Mage on the high ground (AoE over the levers).
- [ ] Limit Rend to 2 of the 4 Knights (≤2-break-source cap).
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
  `038-dugeura-pass.md` (Black Mage AoE + Time-Mage tempo precedent).
```
</content>
