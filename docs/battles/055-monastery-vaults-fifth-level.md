# 055 - Monastery Vaults, Fifth Level (Orbonne descent / Murond Death City)

Status: designed (not yet implemented)
Chapter: 4 — "In the Name of Love"
Battle order: Battle 50 (ENDGAME GAUNTLET 2 of 5 — NO resupply across 49→50→51→52→53)
Target version: Enhanced v1.5.0
ENTD: global entry **TBD** — confirm on Windows game data
File: `battle_entd*_ent.bin` (TBD) / `OverrideEntryData` rows (TBD)

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `037-chapter-4-overview.md`. ENDGAME GAUNTLET: 49 (`054`) → 50 (`055`) → 51 (`056`) →
> 52 (`057`) → 53 (`058`), ONE loadout, no outfitter.

## Original Battle

Objective:

```text
Defeat Loffrey!   (the fight ends the instant Loffrey falls — the caster screen is optional. This is the
                   payoff for the boss who RETREATED at the Mullonde Nave, 052; here he DIES.)
```

Player deployment:

```text
Up to 5 units, including Ramza. No outfitter (gauntlet 2/5).
```

Original enemy composition (verified via Game8, Battle 50):

```text
Loffrey Wodring   (BOSS — Knights Templar / Divine Knight; "Unyielding Blade" equip-break; wields Save the Queen)
2x Black Mage      (heavy AoE magic)
2x Summoner         (AoE summon damage)
1x Time Mage        (Slow / tempo denial)
```

Public walkthrough details:

```text
Recommended level: 60+.  Difficulty: 3/5 stars.  Deploy up to 5.  Win: "Defeat Loffrey!"
TERRAIN: a WIDE area with the enemies SCATTERED across the field (a caster crossfire — open sightlines).
THE THREAT — LOFFREY + a CASTER CROSSFIRE: Loffrey wields "UNYIELDING BLADE" (Divine-Knight equip-break)
  and a strong sword (Save the Queen); his SCATTERED caster squad (2 Black Mage + 2 Summoner) rains heavy
  AoE while a Time Mage SLOWS your units to keep you in the kill-zone. You must cross open ground under
  fire to reach him.
WALKTHROUGH TIPS: DISARM Loffrey first (Steal Weapon / Rend / Crush) to neuter Unyielding Blade; spread
  out vs the AoE; answer Slow (cleanse / immunity); then burst the boss.
Spoils: 40,300 Gil; buried treasure (four spots — Elixirs).
```

Design reading:

The Vaults Fifth Level is **the caster-crossfire boss fight** and the **payoff for Loffrey**, who
retreated at the Nave (`052`) — here he stands and **dies**. Its identity is **a cross-the-killzone race
to a disarmable equip-break boss**: Loffrey's Unyielding Blade can strip your gear (disarm him first),
while a **scattered squad of two Black Mages, two Summoners, and a Time Mage** punishes clustering with
**AoE** and locks your tempo with **Slow** — across a wide, open field. Because the win condition is
*defeat Loffrey*, it rewards spreading out, answering Slow, disarming the knight, and **bursting the
boss** rather than trading with the casters.

For New Game++ the identity must stay: **a disarmable equip-break boss (Loffrey) behind a scattered AoE-
plus-Slow caster crossfire on a wide field; win the instant Loffrey falls — the gauntlet's caster-screen
test on no resupply.** And because Loffrey **dies** here, this is a clean Tier-S payout: **Loffrey carries
the Escutcheon** — the best shield, the corrupted Templar's guard.

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm slots: Loffrey (Divine Knight) + 2 Black Mage + 2 Summoner + 1 Time Mage. NO outfitter (gauntlet 2/5).
Confirm the win condition: fight ENDS when Loffrey falls (caster screen optional).
Keep Loffrey's equip-break (ONE source, disarmable) + the SCATTERED caster crossfire (AoE) + Time-Mage
  Slow + the WIDE open field. These ARE the fight.
SWAP Loffrey's weapon OFF "Save the Queen" → a strong generic/Tier-A knight sword (Save the Queen is the
  Ch4 Bervenia unlock, 039; keep it singular). Loffrey's Tier-S reward here is the ESCUTCHEON (shield).
Confirm whether OverrideEntryData carries Level / equipment, or leaves them at -1.
Leave the four buried Elixir spots as-is — existing loot.
```

Job IDs (carry over known, verify the rest in-game):

```text
Loffrey  — Divine Knight job id   (TBD - verify; Unyielding Blade equip-break; cf. 052 Nave)
Black Mage job id   (TBD - verify; AoE)
Summoner job id     (TBD - verify; AoE; cf. 028)
Time Mage job id    (TBD - verify; Slow; cf. 044 Sluice)
```

## Job Escalation (Chapter 4 rule)

```text
CHANGE: keep Loffrey + the caster squad (2 Black Mage + 2 Summoner + 1 Time Mage), but bring the whole
  crossfire to ENDGAME strength (casters 103, Loffrey full boss 105). The "changed job" content is the
  DENSITY of the caster crossfire at endgame — five casters' worth of AoE + Slow over a wide field — plus
  Loffrey now standing to DIE (he fled at the Nave). No generic padding beyond the vanilla screen.
WHY: the chapter wants more challenge via jobs without breaking strategy. Here the escalation is the
  AoE-plus-Slow crossfire forcing dispersal + tempo answers BEFORE you can disarm and burst Loffrey —
  the original tactics, sharpened to endgame. Padding with melee adds would dull the caster identity.
CONSTRAINTS (carried): EQUIP-BREAK ONE source (Loffrey), disarmable (Steal / Rend / Crush), recoverable,
  NOT a hard lock (039/052 precedent). CASTER AoE = INTACT charge times, race-able (028). TIME-MAGE SLOW
  = soft, ONE-disruptor cap, cleansable / immunity-answerable, NOT a hard lock (044 precedent).
WHAT IS NOT CHANGED: Loffrey the equip-break boss, the scattered caster crossfire, the wide field, and
  the "Defeat Loffrey" win rule remain.
```

## Sanctioned exceptions (carried precedents)

```text
UNYIELDING BLADE (Loffrey, ONE source) — Divine-Knight equip-break; answer = Steal Weapon / Rend / Crush
  (disarm first). Capped, recoverable, NOT a hard lock (039 / 048 / 052 precedents).
CASTER AoE (2 Black Mage + 2 Summoner) — heavy area magic; INTACT charge times, race-able, spaceable (028).
TIME-MAGE SLOW (1) — tempo denial; soft, ONE-disruptor cap, cleansable / immunity-answerable (044 precedent).
WIN-ON-LOFFREY-FALLS — defeating Loffrey ends the fight; the casters are optional (vanilla rule).
```

## Boss rare loot — TIER-S (ledger reassigned thematically)

> **Superseded (2026-06-27 rebalance):** the no-resupply gauntlet drops nothing usable. Escutcheon now pays
> at Loffrey's FIRST appearance at **Nave (461 s1)**, before the point of no return; this battle is restored
> to standard loot (Loffrey back to his vanilla Crystal Shield, no spoil). Canonical: `chapter-4-rewards-implementation.md`.

```text
LOFFREY WODRING → ESCUTCHEON (Tier-S — the best shield; auto-Protect/Shell-tier guard).
  Steal-or-drop on Loffrey, who DIES as the win condition (guaranteed on a focus kill). THEMATIC: the
  corrupted Templar's own shield — a Divine Knight carries a shield, so the best-in-game shield fits him
  far better than a caster's robe.
  LEDGER NOTE (reassignment): the overview pencilled Robe of Lords here, assuming Loffrey was a caster.
  Game8 confirms he is a DIVINE KNIGHT, so the Tier-S ledger is rebalanced to fit each boss's archetype:
    • Loffrey (Divine Knight, 055) → ESCUTCHEON (shield)  ← here
    • Cletienne (Sorcerer/caster, Necrohol 056) → ROBE OF LORDS (caster robe)  ← moved here (perfect fit)
    • Lost Halidom (holy relic, 057) → MATERIA BLADE (the holy blade left at the holy ground)
    • Airship Graveyard FINAL (058) → RAGNAROK (capstone)
  The caster screen drops nothing rare. Save the Queen stays singular to Bervenia (039) — swap Loffrey's
  weapon to a generic/Tier-A knight sword. Buried Elixirs stay as-is.
```

> Tier-S ledger (updated): Chaos Blade (Folmarv, 052) · Ribbon (Zalbaag, 053) · **Escutcheon (Loffrey,
> 055)** · Robe of Lords (Cletienne, 056) · Materia Blade (Lost Halidom relic, 057) · Ragnarok (FINAL,
> 058). Excalibur stays with Orlandeau (player) — never on an enemy.

## Proposed Composition (New Game++ Vaults Fifth Level v1)

Keep Loffrey + the caster squad; no padding. Loffrey (full boss, he dies) `105`; casters `103`.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Loffrey (BOSS, objective) | Divine Knight | `105` | Equip-break (disarm-first); carries Tier-S Escutcheon; the intended kill. |
| n | Black Mage | Black Mage | `103` | Heavy AoE; punishes clustering. |
| n | Black Mage | Black Mage | `103` | Second AoE caster; crossfire from the far flank. |
| n | Summoner | Summoner | `103` | AoE summon damage (intact charge times). |
| n | Summoner | Summoner | `103` | Second summoner; widens the kill-zone. |
| n | Time Mage | Time Mage | `103` | Slow / tempo denial (one-disruptor cap). |

Reasoning:

The faithful move is **a wide-field caster crossfire guarding a disarmable equip-break boss**. Loffrey
(`105`) brings the **disarm-first** wrinkle (Steal / Rend / Crush answers Unyielding Blade); the four
damage casters (2 Black Mage + 2 Summoner, `103`) punish clustering with **AoE** so the party must
**spread** as it crosses; the Time Mage (`103`) **Slows** to hold you in the kill-zone (soft, cleansable,
one-disruptor). Win-on-Loffrey-falls preserves the original's *disperse, disarm, and burst the boss*
tactics — on no resupply, gauntlet 2/5. A clean 3/5★ caster test, the payoff for the man who fled the
Nave. The Escutcheon (best shield) drops from the Divine Knight who carried it.

## Builds (boss-tier knight + endgame casters)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Loffrey Wodring (Lv 105) — BOSS, objective, Tier-S carrier

```text
Job: Divine Knight (id TBD)   JobLevel: 8   Primary: Unyielding Blade / Divine Sword (equip-break + drain)
Reaction: Damage Split / Reflexes (id TBD)   Support: break-resist / Defense Boost (id TBD)   Movement: Move +2 (id TBD)
Head: Genji Helm-tier (id TBD)   Body: heavy boss armor (id TBD)
Accessory: break-resist accessory (id TBD)   Right hand: strong generic/Tier-A knight sword (id TBD; NOT Save the Queen)
Left: ESCUTCHEON (Tier-S steal/drop, id TBD)
The intended kill; disarm him (Steal / Rend / Crush), then burst for the Escutcheon.
```

Role: the disarmable equip-break boss + the Tier-S shield; the focus target.

### Black Mage x2 (Lv 103) — AoE crossfire

```text
Job: Black Mage (id TBD)   JobLevel: 8   Primary: Black Magic (heavy AoE; INTACT charge times)
Reaction: Reflexes (449)   Support: MA-boost (id TBD)   Movement: Move +1 (486)
Head: mage hat (id TBD)   Body: shop robe (id TBD)   Accessory: Featherweave Cloak (234)
Right hand: magic-boost rod (id TBD)   Left: none (255)
```

Role: punishes clustering from open sightlines; race-able.

### Summoner x2 (Lv 103) — AoE

```text
Job: Summoner (id TBD)   JobLevel: 8   Primary: mid/high summons (INTACT charge times, race-able)
Reaction: Reflexes (449)   Support: MA-boost (id TBD)   Movement: Move +1 (486)
Body: shop robe (id TBD)   Accessory: Featherweave Cloak (234)   Right hand: magic-boost rod (id TBD)
```

Role: widens the kill-zone with summon AoE; spaceable.

### Time Mage (Lv 103) — Slow

```text
Job: Time Mage (id TBD)   JobLevel: 8   Primary: Time Magic — SLOW (soft, one-disruptor cap) + Haste-self
Reaction: Reflexes (449)   Support: MA-boost (id TBD)   Movement: Move +1 (486)
Accessory: Featherweave Cloak (234)   Right hand: magic-boost rod (id TBD)
No hard CC — Slow only (cleansable / immunity-answerable).
```

Role: tempo denial; holds the party in the kill-zone; soft.

## Positioning Plan

```text
A WIDE open vault floor with the enemies SCATTERED: Loffrey forward-center as the objective; the 2 Black
  Mages and 2 Summoners spread to the flanks/back for crossfire AoE (open sightlines force dispersal);
  the Time Mage mid-back to Slow advancing units. Keep the open field (the crossfire IS the fight).
Preserve: Loffrey the equip-break boss (disarm-first), the scattered AoE+Slow crossfire, and the
  win-on-Loffrey-falls rule. The Escutcheon rides on Loffrey, the intended target.
```

The vault floor should say: "Loffrey makes his stand in the open, his casters spread to catch you in
the crossfire — scatter, weather the Slow, strike the blade from his hand, and take his shield."

## Implementation Checklist

- [ ] Identify Vaults Fifth Level `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify Loffrey + 2 Black Mage + 2 Summoner + 1 Time Mage.
- [ ] Confirm win condition: fight ENDS when Loffrey falls (casters optional).
- [ ] Keep Loffrey's equip-break ONE source (disarmable); casters' charge times intact; Slow soft (one-disruptor).
- [ ] Swap Loffrey's weapon OFF Save the Queen → strong generic/Tier-A knight sword (keep StQ singular to 039).
- [ ] Set levels: Loffrey `105`; casters `103`. JobLevel `8` on all slots.
- [ ] Set Loffrey's steal/drop = Tier-S **Escutcheon**; casters carry NO rare.
- [ ] Update the Tier-S ledger downstream: Robe of Lords → Cletienne (056); Materia Blade → Lost Halidom (057).
- [ ] Patch via the correct layer; keep the diff inside the Vaults Fifth Level window only.
- [ ] Re-dump and diff; confirm small, intentional changes; verify roster + win rule + Escutcheon.
- [ ] Install mod, test from a New Game+ save; confirm disperse-disarm-burst play, AoE+Slow answerable,
      and killing Loffrey yields the Escutcheon.

## Test Questions

- Is it a disperse-disarm-burst race — cross the open field under AoE, answer Slow, disarm Loffrey, win
  the instant he falls (casters optional)?
- Is the equip-break disarmable/answerable (one source; Steal / Rend / Crush) and the Slow soft (one
  disruptor, cleansable) — neither a hard lock?
- Does the scattered caster crossfire genuinely demand dispersal (heavy AoE, open sightlines)?
- Is Loffrey clearly the rewarded target (win condition + Tier-S Escutcheon), and does the ledger now fit
  each boss's archetype (shield→knight, robe→caster)?
- Is it survivable on ONE loadout (no resupply, gauntlet 2/5)?
- Does it read as Loffrey's last stand in the open vault, not a designed arena?

## Sources

- Game8, "Monastery Vaults: Fifth Level Walkthrough (Battle 50)": boss Loffrey (Divine Knight; Unyielding
  Blade; Save the Queen), support 2 Black Mage + 2 Summoner + 1 Time Mage, "Defeat Loffrey!", rec 60+,
  3/5 stars, wide scattered field, disarm-first + spread-vs-AoE + Slow advice, spoils 40,300 Gil + buried
  Elixirs.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553226
- Final Fantasy Wiki, "Loffrey Wodring": Knights Templar / Divine Knight.
  https://finalfantasy.fandom.com/wiki/Loffrey_Wodring
- Local: `037-chapter-4-overview.md` (gauntlet + Tier-S tiering), `052-mullonde-nave.md` (Loffrey retreats
  there), `044-fort-besselat-sluice.md` (Time-Mage Slow precedent), `028` (Summoner precedent),
  `056-necrohol-of-mullonde.md` (Cletienne + Robe of Lords — to be designed).
```
