# 026 - Lesalia Castle Postern (Lesalia Imperial Capital — Postern Gate)

Status: ✅ implemented (v1, entry 420) — NG+ only; Alma partial endgame gear 2026-06-27; pending playtest. **v2 redesign documented only** (implementation pending).
Chapter: 3 — "The Valiant"
Battle order: Battle 23 (after Mining Town of Gollund)
Target version: Enhanced v1.5.0
ENTD: global entry **420** (entd4 local 36) — Zalmo boss + 3 Knight + 2 Monk + Alma guest; see 024
File: `battle_entd*_ent.bin` (TBD) / `OverrideEntryData` rows (TBD)

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `024-chapter-3-overview.md`.

**Guest gear upgrade (NG+ survivability, 2026-06-27):** Alma (s0) — **body Black Garb 198** (HP 42→100)
and **weapon Golden Staff 64** upgraded to best buyable. **Head Barrette 170 KEPT** (no buyable
HairAdornment exists — all are reserved; Barrette already grants KO/Stone/Stop/Charm immunity, better
for survival than any buyable Hat) and **accessory Red Shoes 214 KEPT** (already the best buyable shoe).
Level from the scaler.

For v2, Alma must be player-controlled in NG+. Her Aegis support is part of the player's tactical
toolkit, not a guest-AI variable.

## Original Battle

Objective:

```text
Defeat Zalmour!  (Zalmo is a named boss who RETREATS once he takes enough damage — he does NOT
  die here, and the fight ends when he withdraws even if his allies still stand.)
```

Player deployment:

```text
Up to 5 units, including Ramza. Guest: ALMA (present; provides an Aegis buff to the party).
  Keep her alive — do not alter her guest scripting.
```

Original enemy composition:

```text
1x Zalmour   (Inquisitor BOSS — constantly HEALS and REVIVES his allies; holy/status; retreats)
3x Knight
2x Monk
ALL enemies carry FLAME SHIELDS: Fire nullified, Ice halved -> THUNDER is the effective element.
```

Public walkthrough details:

```text
Recommended level: ~26.
Small map; enemies cluster at the far side and line up on STAIRS as they advance — ideal for
  line / area attacks (Thunder line, Shockwave).
Zalmo CONSTANTLY revives + heals his Knights/Monks — a sustain wall. Silence him (e.g. Agrias'
  Hallowed Bolt) or burst him down; the fight ENDS when he retreats.
Flame Shields on the whole band null Fire and halve Ice — bring THUNDER.
Alma provides an Aegis buff.
```

Design reading:

Lesalia Postern is **the reviving-healer-boss puzzle** — a twist on Chapter 1's Brigands' Den
("kill the healers first"). Here the healer IS the boss: Zalmo, an Inquisitor, endlessly heals and
revives his Knight/Monk wall, so killing the minions is futile — the player must **silence or
burst Zalmo himself**, at which point he retreats and the fight ends. Layered on top is an
**elemental lock**: the whole band's Flame Shields null Fire and halve Ice, funnelling the player
toward **Thunder**, and the stair-cluster terrain rewards **line/AoE**. It teaches target priority
(go for the boss, not his wall), build adaptation (bring Thunder), and terrain exploitation.

For New Game++ the identity must stay: **a sustain wall anchored by a reviving Inquisitor boss who
must be silenced or burst before his retreat, against a Fire-immune band on stair terrain that
rewards Thunder line-AoE — priority and element are the whole fight.**

## Local Data Confirmed

```text
ENTD entry 420 confirmed in `024-chapter-3-overview.md` and v1 implementation.
Roster: Zalmo + 3 Knight + 2 Monk, plus the player slots and Alma guest slot.
DO NOT touch Zalmo's RETREAT scripting (he must withdraw at his HP threshold; the fight ends on
  his retreat). He does NOT die here — his death (and any rare loot) is a Chapter 4 matter.
Preserve Alma's guest scripting/Aegis buff, and verify/apply player control in NG+.
Keep the FLAME SHIELDS on the whole band (the Fire-immune / Thunder puzzle is the design).
Keep the stair / far-cluster terrain (line-AoE counterplay depends on it).
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
```

Job IDs (carry over known, verify the rest in-game):

```text
Knight job id          (TBD - verify)
Monk job id            (TBD - verify)
Inquisitor job id      (TBD - verify; Zalmo — heal/revive holy boss; FIRST Inquisitor in the mod)
Flame Shield item id   (TBD - verify; equipped on all enemies)
```

## Enemy Party Escalation (Chapter 3 redesign)

```text
VANILLA SPIRIT: a reviving Inquisitor turns the enemy wall into a sustain puzzle, while Flame
  Shields push the player toward Thunder and line/AoE on stairs.
CHAPTER-3 UPGRADE: keep the exact Zalmo + 3 Knight + 2 Monk roster, but complete every active human
  setup with secondary/reaction/support/movement. Alma must be player-controlled.
WHY: the sustain boss and elemental lock are already the headline. Adding Dragoon/Ninja here would
  steal later debuts and overpressure the pre-Vault fight.
WHAT IS NOT CHANGED: the answer remains silence/burst Zalmo, use Thunder/non-Fire damage, and exploit
  the stair cluster.
```

Chapter 3 requirements applied:

```text
- Every active human enemy has full equipment.
- Every active human enemy has secondary, reaction, support, and movement.
- The party has real synergy: Zalmo sustains/revives, Knights screen and threaten gear, Monks
  pressure with Martial Arts, and Flame Shields create a shared element rule.
- Alma is scaled, geared, and player-controlled in NG+.
- No hard-lock Zalmo and no extra caste.
```

## Sanctioned exceptions (carried precedents)

```text
HEALER SUSTAIN / REVIVE on a boss — allowed and intended: Zalmo's heal/revive IS the puzzle; the
  counter is SILENCE or focus-burst (telegraphed, fair). Constrain his offense to holy/soft status
  — NO hard lock (no Stop/Don't Act spam) on an endgame party.
KNIGHT Rend (break) — allowed on up to 2 of the 3 Knights (Ch2 Balias Tor 016 / Lionel precedent):
  shop-tier breakable gear, Safeguard remains the counter.
ELEMENTAL-RESIST gear (Flame Shield) — allowed band-wide here as the deliberate build puzzle; it is
  telegraphed and counterable (use Thunder / non-Fire). Not a status effect, so no lock concerns.
```

## Boss rare loot

```text
None HERE. Zalmo RETREATS — he does not die at Lesalia, so there is nothing to drop (Gallows
precedent, 020: a retreating boss carries no rare; the rare is paid out where the boss dies). If
Zalmo reappears as a killable boss in Chapter 4, assign his rare there.
Generics stay shop-tier (their Flame Shields are a mechanic, not a reward). The map's BURIED
TREASURE (Brigandine / Diamond Bracelet / Ancient Sword / Ninja Blade) is existing map treasure,
not boss loot; leave it as-is.
```

## Guest handling

```text
Alma is an active guest and must be player-controlled in NG+. Her Aegis buff remains helpful, but
the fight's difficulty comes from Zalmo's sustain wall and element puzzle, not from Alma AI.
```

## Proposed Composition (New Game++ Lesalia Postern v2)

Keep the exact roster; Zalmo is the sub-boss spike (retreats). Zalmo `103`; Knights `101`;
Monks `101`. Whole band keeps Flame Shields.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Zalmo (SUB-BOSS) | Inquisitor | `103` | Heals + revives the wall; silence/burst him → he retreats, ending the fight. |
| n | Knight (Rend) | Knight | `101` | Front wall, kept alive by Zalmo; screens him on the stairs. |
| n | Knight (Rend) | Knight | `101` | Second wall; contests the line/AoE approach. |
| n | Knight | Knight | `101` | Third body; pressures the player / Alma. |
| n | Monk | Monk | `101` | Bare-fist bruiser (Chakra/Aurablast); durable, revived if downed. |
| n | Monk | Monk | `101` | Second Monk; sustained melee pressure. |

Reasoning:

The faithful move is to **make Zalmo the priority and keep the sustain + element puzzle**. With
Zalmo reviving and healing at `103`, attriting his Knight/Monk wall is pointless — the player must
silence him or focus him through the screen until he retreats. The band-wide Flame Shields force a
Thunder pivot, while the stair cluster rewards line/AoE. The Knights and Monks now have complete
setups, so the wall pressures rather than simply stalls. Alma's controlled Aegis helps the player
weather the wall. He retreats with no rare, preserving any later payoff.

## Builds (final-shop quality; Church guard + Inquisitor flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Zalmo — Inquisitor SUB-BOSS (Lv 103)

```text
Job: Inquisitor (id TBD)   JobLevel: 8   Primary: heal/revive + holy/soft-status
Secondary: White Magic / Item support equivalent if legal; keep to heal/revive/cleanse, no hard lock
Skillset limit: heal, revive (Raise), holy damage, soft status ONLY — NO hard lock.
Reaction: a defensive/MP reaction (id TBD)   Support: MA/Magick-boost (id TBD)
Movement: Movement +1 (486)
Head: cloth/clergy hat (id TBD)   Body: shop robe (id TBD)
Accessory: Flame Shield (id TBD — band gimmick) or a magic-def accessory
Right hand: shop magic-boost rod/staff (id TBD)   Left: none (255)
RETREATS at HP threshold — do NOT let him die here; no rare loot at Lesalia.
```

Role: the reviving heart of the wall. Silence or burst him; everything else is a stalling screen.

### Knight x3 (Lv 101) — 2x Rend, Flame Shield

```text
Job: Knight (id TBD)   JobLevel: 8
Secondary: Item on the wall captain; Fundaments/limited support on the third; Rend/Battle Skill
  remains the primary Knight pressure and is capped to two meaningful break sources.
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head/Body: shop heavy helm + heavy armor (ids TBD)
Accessory: Bracers (218)   Right hand: Runeblade (30) / Icebrand (29)   Left: FLAME SHIELD (id TBD)
```

Role: the front wall Zalmo keeps reviving; Flame Shield makes Fire useless against them.

### Monk x2 (Lv 101) — Flame Shield-equivalent resistance

```text
Job: Monk (id TBD)   JobLevel: 8   Primary: Martial Arts (Chakra self-sustain, Aurablast range)
Secondary: Item or Fundaments equivalent; no status lock
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head: Headband (163)   Body: Power Garb (195)   Accessory: a Fire-resist accessory (id TBD)
(Monks cannot hold a shield; give them a Fire-null/halve accessory to keep the band's element puzzle.)
```

Role: durable bruisers, revived if downed; Chakra/Aurablast keep them a sustained threat.

## Positioning Plan

```text
Zalmo starts at the FAR side behind his Knight/Monk wall, healing/reviving from safety; the player
  must punch through or silence/snipe him.
The 3 Knights screen the stairs; the 2 Monks flank/advance. Enemies LINE UP on the stairs as they
  come — preserve that cluster so Thunder line-AoE is rewarded.
Alma starts with the player, buffing (Aegis). Keep her guest start.
Preserve Zalmo's retreat trigger and the band-wide Flame Shields.
```

The gate should say: "their priest raises the dead faster than you can drop them — silence him,
strike with Thunder, and he'll flee."

## Simulation Plan and Results

Simulation artifact:

```text
tmp/fft-level-design-026-lesalia-castle-postern/
```

Model scope:

```text
First four rounds only; compares Zalmo sustain pressure, wall pressure, and the fairness of the
silence/burst answer. It assumes Alma is player-controlled in v2 and rejects hard-lock Zalmo or an
extra Dragoon caste.
```

Iteration results:

| Candidate | Enemies | Action ratio | Sustain pressure | Wall pressure | Total pressure | Answer window | Answer fairness | Result |
|-----------|---------|--------------|------------------|---------------|----------------|---------------|-----------------|--------|
| v1 sustain wall | 6 | 0.85 | 60.0 | 68.9 | 128.9 | 2.8 | 28.6 | Rejected: Zalmo answer too poor |
| v2 complete sustain wall | 6 | 0.89 | 67.2 | 75.7 | 142.9 | 2.6 | 39.7 | Accepted |
| Hard-lock Inquisitor | 6 | 0.90 | 74.8 | 75.7 | 150.5 | 3.2 | 26.2 | Rejected: hard-lock/too high |
| Add Dragoon flanker | 7 | 1.01 | 67.2 | 94.0 | 161.2 | 3.1 | 30.7 | Rejected: extra caste/too high |

Decision:

```text
Keep the exact six-enemy roster. Complete every setup and make Alma player-controlled. Zalmo's
sustain gets stronger, but hard-lock status and extra Dragoon pressure are rejected.
```

## Current Implementation (v1, entry 420 — superseded by v2 design)

The shipped v1 scales the fight, keeps Zalmo's retreat scripting, and gives Alma stronger gear.
The v2 redesign above is **documentation only** in this pass; it requires a later implementation
pass to apply Alma player control and complete secondary setups for every active enemy.

## Future Implementation Checklist (v2)

- [x] Identify Lesalia Postern ENTD entry 420; fill "Local Data Confirmed".
- [x] Dump original entry; verify Zalmo + 3 Knight + 2 Monk + player + Alma guest slots.
- [ ] Confirm Inquisitor / Knight / Monk job ids; keep Zalmo's heal/revive + holy/soft-status only.
- [ ] Keep FLAME SHIELDS (or Fire-null/halve accessory on Monks) band-wide; verify Thunder is the answer.
- [ ] Put Rend on TWO of the three Knights; shop-tier breakable gear only.
- [ ] Set levels: Zalmo `103`; Knights + Monks `101`.
- [ ] Set JobLevel `8` on all active enemy slots.
- [ ] Give every active human enemy full equipment plus secondary/reaction/support/movement.
- [ ] PRESERVE Zalmo's RETREAT threshold scripting (he must NOT die here; no drop).
- [ ] Apply/verify Alma player control in NG+ while preserving Aegis and guest scripting.
- [ ] Keep the stair/far-cluster terrain.
- [ ] Patch via the correct layer in a later implementation pass; no binary/data change in this doc pass.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify retreat + Flame Shields.
- [ ] Install mod, test from a New Game+ save; confirm silencing/bursting Zalmo ends the fight.

## Test Questions

- Is attriting the wall genuinely futile until Zalmo is silenced or burst (revive sustain real)?
- Does Zalmo RETREAT at threshold and end the fight, with no lootable rare (Ch4 deferral)?
- Do the band-wide Flame Shields clearly push the player to Thunder (and punish Fire)?
- Does the stair cluster reward line/AoE the way the original taught?
- Is Zalmo's offense holy/soft-status only — annoying, not a hard lock on an endgame party?
- With Alma player-controlled, does Aegis help without trivializing the wall?
- Is it a step up from Gollund but below the Vaults bosses (Izlude/Wiegraf)?
- Does it still read as a Church gate ambush, not a designed arena?

## Sources

- Game8, "Lesalia Castle Postern Walkthrough (Battle 23)": roster (Zalmour + 3 Knight, 2 Monk),
  objective "Defeat Zalmour!", recommended level ~26, deploy 5, Zalmo constantly heals/revives and
  RETREATS at enough damage, band-wide Flame Shields (null Fire / halve Ice → Thunder), small
  stair-cluster map, Alma's Aegis buff, buried treasure.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553183
- Final Fantasy Wiki, "Zalmo Rusnada" / "Lesalia": story/terrain context.
  https://finalfantasy.fandom.com/wiki/Zalmo_Rusnada
- Local: `docs/battles/024-chapter-3-overview.md` (Chapter 3 complete-party rules),
  `006-brigands-den.md` (kill-the-healers precedent, here inverted), `020-golgollada-gallows.md`
  (retreating boss → no drop), `016-balias-tor.md` (Knight Rend exception).
