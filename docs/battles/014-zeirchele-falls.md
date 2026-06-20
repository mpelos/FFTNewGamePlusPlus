# 014 - Zeirchele Falls (Zirekile Falls)

Status: designed (not yet implemented)
Chapter: 2 — "The Manipulator and the Subservient"
Battle order: Battle 13 (after Araguay Woods)
Target version: Enhanced v1.5.0
ENTD: global entry **TBD** — confirm on Windows game data
File: `battle_entd*_ent.bin` (TBD) / `OverrideEntryData` rows (TBD)

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `011-chapter-2-overview.md`.

## Original Battle

Objective:

```text
Save Princess Ovelia!  (she must survive the battle — her death is a failure/Game Over)
```

Player deployment:

```text
Up to 4 units, including Ramza.
Allies: Agrias joins here and fights alongside the party. Ovelia hangs back and casts
  defensive magic (Aegis/Shell-type); she is the unit the player must protect.
Note: Gaffgarion starts as a party ally, then BETRAYS mid-battle and turns enemy.
```

Original enemy composition:

```text
1x Gaffgarion (Dark Knight / Fell Knight — betrayer; RETREATS at low HP, not killed here)
5x Knight
```

Public walkthrough details:

```text
Recommended level: ~13.
Riverside map: a bridge crossing water, with elevation changes on the banks.
Gaffgarion's betrayal is the story beat; he uses HP-draining dark sword skills (Drain/
  Shadowblade-type) and his power lives in his weapon.
Canonical tip: STRIP Gaffgarion's equipment while he is still your ally (formation screen)
  so his attacks are far weaker once he turns — his threat is gear-dependent.
He retreats after taking enough damage — you do NOT have to defeat him outright.
The Knights press toward Ovelia; protecting her is the whole battle.
```

Design reading:

Zeirchele is **the betrayal fight and the chapter's first big escort-defense**. The drama is
Gaffgarion flipping from ally to enemy, but the *mechanics* are: keep **Ovelia** alive while a
Knight wall pushes toward her and a draining Dark Knight pressures your line. It teaches the
player to **defend a fixed, fragile VIP** across a bridge chokepoint, and rewards prep (stripping
Gaffgarion's gear neuters him). Agrias arriving gives the player a strong sword-skill ally to
offset the loss of Gaffgarion.

For New Game++ the identity must stay: **a tense VIP-defense on a riverbank where a betraying,
gear-dependent Dark Knight and his Knight escort drive at Princess Ovelia — protect her, exploit
the strip-his-gear counter, and lean on Agrias.**

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm slots: Gaffgarion (named/boss unit) + 5 Knight, plus the player, Agrias, and OVELIA slots.
DO NOT touch Ovelia's protected-VIP scripting, Agrias's ally slot, or Gaffgarion's
  ally-then-betray + auto-retreat scripting. Only the enemy Knight pack (and one job swap) is edited.
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
```

Job IDs (verify all in-game):

```text
Gaffgarion boss job id (TBD - verify; named Dark Knight; handle the betray/retreat link with care)
Knight job id          (TBD - verify; shares with other Ch2 battles)
Archer job id = 77     (confirmed; added below)
```

## Job Escalation (Chapter 2 rule)

```text
CHANGE: swap ONE Knight -> an Archer (keep the count at 6).
WHY: the original escort threat is all melee Knights, which a player can wall off at the bridge
  to shield a hanging-back Ovelia. Adding a ranged Archer means Ovelia can be threatened from
  across the water / from elevation, so the player must actually cover her line of sight, not
  just block the bridge. This is the single new wrinkle; the strategy ("defend Ovelia, weather
  Gaffgarion, use Agrias") is unchanged — only harder.
WHAT IS NOT CHANGED: Gaffgarion's gear-dependent threat and the four remaining Knights keep the
  betrayal-and-press identity intact.
```

## Boss rare loot

```text
NONE here. Gaffgarion RETREATS (he is not defeated at Zeirchele), so there is no drop, and the
canonical counter is to strip his gear anyway. His rare, non-buyable signature item is granted
at Lionel Castle Gate (doc 021 / Battle 20), where he actually falls. Keeping his Zeirchele kit
strong-but-non-unique also keeps the strip-his-gear tactic meaningful.
```

## Proposed Composition (New Game++ Zeirchele v1)

Keep Gaffgarion + the Knight escort, swapping one Knight for an Archer (6 enemies). Gaffgarion
at sub-boss tier (`103`); the Archer and lead Knight at `101`; the rest at `100`–`101`.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | **Gaffgarion (betrayer)** | Dark Knight / Fell Knight | `103` | Draining sword-skill pressure; retreats at low HP. Strip-his-gear neuters him. |
| n | Knight | Knight | `101` | Lead wall; drives toward Ovelia. |
| n | Knight | Knight | `101` | Second wall; contests the bridge. |
| n | Knight | Knight | `100` | Body; flanks along the bank. |
| n | Knight | Knight | `100` | Body; reinforces the push on Ovelia. |
| n | Archer (NEW) | Archer | `101` | Ranged threat to Ovelia from across the water / elevation — the new escort wrinkle. |

Reasoning:

The faithful move is to **scale the escort, elevate Gaffgarion to a real sub-boss, and add one
ranged threat to Ovelia**. Gaffgarion at `103` with draining dark sword skills is a genuine
menace — but, true to the original, his power is in his (strippable, non-unique) weapon, so the
counter survives. Four Knights keep the bridge-push identity; the swapped-in Archer means the
player can't simply block the bridge and ignore Ovelia's line of sight. Agrias (ally) offsets
the difficulty, as intended.

## Builds (final-shop quality; Gaffgarion gear-dependent and strippable)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Gaffgarion - Betrayer sub-boss (Lv 103)

```text
Job: Dark Knight / Fell Knight (id TBD — preserve the ally->betray + auto-retreat link)
JobLevel: 8
Primary/Secondary: his dark sword skillset (Drain/Shadowblade-type, id TBD) — keep it
  WEAPON-dependent so stripping his sword (the canonical counter) truly weakens him
Reaction: Counter or Damage Split (id TBD) — punishes dogpiling
Support: Attack Boost (465)   Movement: Movement +1 (486)

Head: shop heavy helm (id TBD)        Body: shop heavy armor (id TBD)
Accessory: Bracers (218)
Right hand: a strong shop sword (Runeblade 30 / Icebrand 29) — NON-unique and STRIPPABLE
Left hand: shop shield (id TBD)
```

Role: the betrayer. Drains HP off the party with his sword skills, but a player who stripped
his gear (or breaks it) defangs him — exactly the original lesson. NON-unique kit (his rare
drop is reserved for Lionel Gate).

### Knight x4 (Lv 101 / 101 / 100 / 100)

```text
Job: Knight (id TBD)   JobLevel: 8   Secondary: none (NO Break)
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head/Body: shop heavy helm + heavy armor (ids TBD)
Accessory: Bracers (218)
Right hand: Runeblade (30) or Icebrand (29)   Left hand: shop shield (id TBD)
```

Role: the wall that drives at Ovelia. Forces the player to hold the bridge/bank chokepoint.

### Archer (Lv 101) — NEW (job swap)

```text
Job: Archer (77)   JobLevel: 8   Secondary: none
Reaction: Reflexes (449)   Support: Concentration (469)   Movement: Movement +1 (486)
Head: Thief's Cap (168)   Body: Black Garb (198)   Accessory: Bracers (218)
Right hand: Windslash Bow (87)   Left hand: none / two-hand marker (254)
```

Role: the ranged escort threat. Positioned to draw a line on Ovelia from across the water or
from elevation, so the player must screen her, not just block the melee.

## Positioning Plan

```text
Gaffgarion starts on the party's side or the bridge (per his betray scripting) — when he turns,
  he pressures the player's line and drives toward Ovelia.
The four Knights start across/at the bridge, pushing toward Ovelia's hang-back position.
The Archer starts on elevation or the far bank with a sightline to Ovelia's area — the threat
  the player must screen.
Preserve Ovelia's protected position, Agrias's ally slot, and Gaffgarion's betray/retreat link.
```

The map should read: "a draining traitor and a Knight wall drive across the bridge at the
princess, with an archer drawing a bead on her from afar." Screen Ovelia, strip the traitor,
hold the crossing.

## Implementation Checklist

- [ ] Identify Zeirchele `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify Gaffgarion + 5 Knight + player + Agrias + Ovelia slots.
- [ ] Confirm Gaffgarion's named-unit + betray/auto-retreat link; DO NOT break it.
- [ ] Keep Gaffgarion's sword skills WEAPON-dependent and his gear strippable + non-unique.
- [ ] Swap one Knight -> Archer (re-job a Knight slot); confirm Archer build.
- [ ] Set levels: Gaffgarion `103`; lead Knights + Archer `101`; the other two Knights `100`.
- [ ] Set JobLevel `8` on all active enemy slots; Knights have NO Break.
- [ ] Do NOT touch Ovelia/Agrias/ally scripting; preserve positions.
- [ ] Patch via the correct layer; keep the diff inside the Zeirchele window only.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify all named links intact.
- [ ] Install mod, test from a New Game+ save; confirm Ovelia-protect + Gaffgarion-retreat work.

## Test Questions

- Is protecting Ovelia genuinely tense at scale (Knight push + the new Archer threat) without
  being an unavoidable loss?
- Does Gaffgarion feel like a dangerous betrayer, while the strip-his-gear counter still defangs him?
- Does his auto-retreat-at-low-HP still trigger (he must NOT be killable here)?
- Does the swapped-in Archer change the escort math (must the player screen Ovelia's LoS)?
- Does Agrias as an ally offset the difficulty as intended?
- Is it harder than Araguay but not yet a Gaffgarion/Cúchulainn-tier boss wall, per the curve?
- Does it still read as the riverbank betrayal, not a designed arena?

## Sources

- Game8, "Zeirchele Falls Walkthrough (Battle 13)": roster (Gaffgarion + 5 Knight), objective
  "Save Princess Ovelia!", deploy 4, recommended level ~13, riverside/bridge terrain,
  Gaffgarion betrayal + strip-his-gear tip + auto-retreat-at-low-HP, Ovelia defensive-magic VIP.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553174
- Final Fantasy Wiki, "Zirekile Falls" / "Gaffgarion": story context (betrayal, Agrias joins).
  https://finalfantasy.fandom.com/wiki/Zirekile_Falls
- Local: `docs/battles/011-chapter-2-overview.md` (job-escalation + boss-loot rules),
  `008-fovoham-windflats.md` (gear-dependent sword-skill boss handling),
  `021-lionel-castle-gate.md` (where Gaffgarion falls and gets his rare drop — to be written).
</content>
