# 056 - Necrohol of Mullonde

Status: designed (not yet implemented)
Chapter: 4 — "In the Name of Love"
Battle order: Battle 51 (ENDGAME GAUNTLET 3 of 5 — NO resupply across 49→50→51→52→53)
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
Defeat Cletienne!   (the fight ends the instant Cletienne falls — the elite screen is optional. This is
                     the payoff for the boss who RETREATED at the Mullonde Nave, 052; here he DIES.)
```

Player deployment:

```text
Up to 5 units, including Ramza. No outfitter (gauntlet 3/5).
```

Original enemy composition (verified via Game8, Battle 51):

```text
Cletienne Duroi   (BOSS — Sorcerer / caster; "MAGICK SURGE" — Magick rises each time he takes damage)
2x Samurai         (the Chapter-4 SAMURAI debut — Draw Out: AoE elemental / break, katana-consumed)
2x Ninja            (fast dual-wield flankers + Throw)
2x Time Mage        (Slow / Haste — tempo control)
```

Public walkthrough details:

```text
Recommended level: 60+.  Difficulty: 3/5 stars.  Deploy up to 5.  Win: "Defeat Cletienne!"
TERRAIN: the Necrohol of Mullonde (the dead holy city — ruined, tiered ground).
THE THREAT — CLETIENNE'S MAGICK SURGE: his Magick stat RISES every time he takes damage, so slow chip
  makes him DEADLIER the longer he lives. The walkthrough's answer: SILENCE him (shut his casting) and/or
  BURST him down fast — do NOT trade a long fight. His elite screen (2 Samurai Draw Out + 2 Ninja flank +
  2 Time Mage Slow) keeps you busy while the surge stacks.
SUPPORT: Samurai Draw Out (AoE elemental); Ninja fast flank/Throw; Time Mages Slow your tempo.
Spoils: 47,600 Gil; buried treasure (four spots — Elixirs).
```

Design reading:

The Necrohol is **the escalating-mage boss fight** and the **payoff for Cletienne**, who retreated at
the Nave (`052`) — here he stands and **dies**. Its identity is **a race against a comeback mechanic**:
Cletienne's **Magick Surge** makes him stronger the longer the fight runs, so the player must **Silence
his casting and burst him**, not slow-chip — all while an **elite fast screen** (the **Samurai job
debut** with Draw Out AoE, **Ninja** flank-tempo, **Time Mage** Slow) tries to stall the kill and let the
surge stack. Because the win condition is *defeat Cletienne*, it rewards decisive focus over attrition.

For New Game++ the identity must stay: **an escalating Magick-Surge mage (answer: Silence-or-burst) behind
an elite Samurai/Ninja/Time-Mage screen; win the instant Cletienne falls — the gauntlet's tempo-race on
no resupply, and the canonical home of the Chapter-4 Samurai debut.** And because Cletienne **dies** here,
this is the perfect Tier-S payout: **Cletienne carries the Robe of Lords** — the best caster robe.

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm slots: Cletienne (Sorcerer, Magick Surge) + 2 Samurai + 2 Ninja + 2 Time Mage. NO outfitter (gauntlet 3/5).
Confirm the win condition: fight ENDS when Cletienne falls (elite screen optional).
Keep Cletienne's MAGICK SURGE (comeback mechanic) + the Samurai Draw-Out / Ninja / Time-Mage screen.
  These ARE the fight. The 2 SAMURAI are the canonical Ch4 Samurai debut (per directive) — keep them.
Confirm whether OverrideEntryData carries Level / equipment, or leaves them at -1.
Set Cletienne's drop/steal = the Tier-S ROBE OF LORDS (see Boss rare loot). Screen drops nothing rare.
Leave the four buried Elixir spots as-is — existing loot.
```

Job IDs (carry over known, verify the rest in-game):

```text
Cletienne — Sorcerer job id   (TBD - verify; Magick Surge; cf. 052 Nave)
Samurai job id   (TBD - verify; the Ch4 DEBUT caste; Draw Out command)
Ninja job id     (TBD - verify; cf. 045 Mount Germinas)
Time Mage job id (TBD - verify; Slow; cf. 044 / 055)
```

## Job Escalation (Chapter 4 rule)

```text
CHANGE: this battle IS the chapter's SAMURAI debut — the 2 Samurai (Draw Out) are vanilla here, so the
  new-caste content is canonical, not invented. Bring the whole elite screen to endgame strength
  (Samurai 104, Ninja/Time Mage 103, Cletienne full boss 105) and let the SURGE be the demand.
WHY: the chapter wants more challenge via jobs while keeping strategy. The Samurai (Draw Out AoE/break)
  add a NEW pressure vector alongside Ninja tempo and Time-Mage Slow — three distinct elite roles
  screening a comeback-mechanic mage. The escalation is the surge-race forcing Silence/burst, sharpened
  by the elite mix. No generic padding.
CONSTRAINTS (carried): MAGICK SURGE is a comeback mechanic answered by SILENCE (shut casting) or BURST
  (kill fast) — telegraphed, NOT an unavoidable wipe; his retaliation is MAGIC, which Silence stops.
  SAMURAI DRAW OUT = AoE elemental / break, race-able, no hard lock (NEW caste, capped). NINJA = physical
  tempo, no status lock (045). TIME-MAGE SLOW = soft, ONE-disruptor cap across the two, cleansable (044).
WHAT IS NOT CHANGED: Cletienne the Magick-Surge mage, the Samurai/Ninja/Time-Mage screen, and the
  "Defeat Cletienne" win rule remain.
```

## Sanctioned exceptions (carried precedents)

```text
MAGICK SURGE (Cletienne) — Magick rises as he takes damage; answer = SILENCE (shut casting) or BURST
  (kill fast). Telegraphed comeback mechanic, NOT an unavoidable wipe; magic-only retaliation.
SAMURAI DRAW OUT (2, NEW Ch4 caste) — AoE elemental / break via consumed katana; race-able, spaceable,
  no hard lock. The chapter's sanctioned job debut.
NINJA TEMPO (2) — fast dual-wield flankers + Throw; physical, no status lock (045 precedent).
TIME-MAGE SLOW (2) — soft tempo denial; ONE-disruptor cap across the pair, cleansable / immunity (044).
WIN-ON-CLETIENNE-FALLS — defeating Cletienne ends the fight; the screen is optional (vanilla rule).
```

## Boss rare loot — TIER-S

> **Superseded (2026-06-27 rebalance):** the no-resupply gauntlet drops nothing usable. Robe of Lords now
> pays at Cletienne's FIRST appearance at **Nave (461 s2)**; this battle is restored to standard loot
> (Cletienne back to his vanilla Black Garb, no spoil). Canonical: `chapter-4-rewards-implementation.md`.

```text
CLETIENNE DUROI → ROBE OF LORDS (Tier-S — the best caster robe: top magic defense + stat bonuses).
  Steal-or-drop on Cletienne, who DIES as the win condition (guaranteed on a focus kill). THEMATIC: the
  Sorcerer's own master-robe — a perfect archetype fit (the ledger was rebalanced at 055 to put the robe
  on the actual caster rather than the Divine Knight Loffrey).
  The Samurai / Ninja / Time-Mage screen drops nothing rare. Buried Elixirs stay as-is.
```

> Tier-S ledger: Chaos Blade (Folmarv, 052) · Ribbon (Zalbaag, 053) · Escutcheon (Loffrey, 055) ·
> **Robe of Lords (Cletienne, 056)** · Materia Blade (Lost Halidom relic, 057) · Ragnarok (FINAL, 058).
> Excalibur stays with Orlandeau (player) — never on an enemy.

## Proposed Composition (New Game++ Necrohol v1)

Keep Cletienne + the elite screen; no padding. Cletienne (full boss, he dies) `105`; Samurai `104`;
Ninja & Time Mage `103`.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Cletienne (BOSS, objective) | Sorcerer | `105` | Magick Surge comeback mage; carries Tier-S Robe of Lords; the intended kill. |
| n | Samurai | Samurai | `104` | Ch4 debut; Draw Out AoE/break; new pressure vector. |
| n | Samurai | Samurai | `104` | Second Samurai; widens the Draw-Out threat. |
| n | Ninja | Ninja | `103` | Fast dual-wield flanker; punishes a stalled kill. |
| n | Ninja | Ninja | `103` | Second Ninja; tempo + Throw reach. |
| n | Time Mage | Time Mage | `103` | Slow (one-disruptor cap across the pair); stalls to let surge stack. |

Reasoning:

The faithful move is **a tempo race against a comeback mage behind an elite screen**. Cletienne (`105`)
**surges** the longer he lives, so the party must **Silence and burst** him — the screen (2 Samurai `104`
Draw-Out AoE, 2 Ninja `103` flank, 2 Time Mage `103` Slow — only one effectively Slowing at a time)
exists to **stall** that kill and let the surge stack. Win-on-Cletienne-falls preserves the original's
*commit and finish him fast* tactics — on no resupply, gauntlet 3/5. A clean 3/5★ tempo test that
**debuts the Samurai** as the chapter's new caste. The Robe of Lords drops from the Sorcerer who wore it.

## Builds (boss-tier mage + elite screen)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Cletienne Duroi (Lv 105) — BOSS, objective, Tier-S carrier

```text
Job: Sorcerer (id TBD)   JobLevel: 8   Primary: Black/area magic + MAGICK SURGE (Magick rises on damage taken)
Reaction: Reflexes / Damage Split (id TBD)   Support: MA-boost (id TBD)   Movement: Move +2 (id TBD)
Head: mage hat (id TBD)   Body: ROBE OF LORDS (Tier-S steal/drop, id TBD)
Accessory: Featherweave Cloak (234)   Right hand: magic-boost rod (id TBD)   Left: none (255)
The intended kill; SILENCE him (or burst fast), then finish for the Robe of Lords. Surge = comeback, not a wipe.
```

Role: the escalating comeback mage + the Tier-S robe; the focus target.

### Samurai x2 (Lv 104) — Ch4 debut

```text
Job: Samurai (id TBD)   JobLevel: 8   Primary: Draw Out (Iaido — AoE elemental / break via consumed katana)
Reaction: Reflexes (449)   Support: Attack/MA-boost (id TBD)   Movement: Move +1 (486)
Head/Body: samurai gear (id TBD)   Accessory: Featherweave Cloak (234)   Right hand: katana (id TBD)
NEW caste — Draw Out is race-able/spaceable, no hard lock.
```

Role: the chapter's Samurai debut; AoE/break pressure screening Cletienne.

### Ninja x2 (Lv 103) — tempo

```text
Job: Ninja (id TBD)   JobLevel: 8   Primary: dual-wield strikes (+ Throw)
Reaction: Reflexes (449)   Support: Dual Wield (id TBD)   Movement: Move +2 (id TBD)
Right/Left hand: ninja blades (id TBD)   Accessory: Featherweave Cloak (234)
```

Role: fast flankers; punish a stalled kill; physical, no status lock.

### Time Mage x2 (Lv 103) — Slow (capped)

```text
Job: Time Mage (id TBD)   JobLevel: 8   Primary: Time Magic — SLOW (soft; ONE-disruptor cap across the pair) + Haste-self
Reaction: Reflexes (449)   Support: MA-boost (id TBD)   Movement: Move +1 (486)
Accessory: Featherweave Cloak (234)   Right hand: magic-boost rod (id TBD)
No hard CC — Slow only (cleansable / immunity-answerable); the pair does not double-lock.
```

Role: tempo denial to stall the kill and let surge stack; soft.

## Positioning Plan

```text
The Necrohol of Mullonde (dead holy city): ruined tiered ground. Place Cletienne back-center (the surge
  mage you must reach and Silence/burst); the 2 Samurai mid-field for Draw-Out AoE; the 2 Ninja on the
  flanks for fast pressure; the 2 Time Mages mid-back to Slow your advance. Keep the ruined elevation.
Preserve: Cletienne the surge mage (Silence/burst answer), the elite Samurai/Ninja/Time-Mage screen, and
  the win-on-Cletienne-falls rule. The Robe of Lords rides on Cletienne, the intended target.
```

The dead city should say: "Cletienne grows stronger with every wound you give him — do not bleed him
slowly; silence his tongue and end him, then take the master's robe from the last of the Templars' mages."

## Implementation Checklist

- [ ] Identify Necrohol `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify Cletienne + 2 Samurai + 2 Ninja + 2 Time Mage.
- [ ] Confirm win condition: fight ENDS when Cletienne falls (screen optional).
- [ ] Keep Magick Surge (comeback; Silence/burst answer, not a wipe); Samurai Draw-Out race-able; Time-Mage
      Slow soft (one-disruptor across the pair).
- [ ] Confirm the 2 Samurai as the Ch4 debut caste (Draw Out command present).
- [ ] Set levels: Cletienne `105`; Samurai `104`; Ninja & Time Mage `103`. JobLevel `8` on all slots.
- [ ] Set Cletienne's steal/drop = Tier-S **Robe of Lords**; screen carries NO rare.
- [ ] Patch via the correct layer; keep the diff inside the Necrohol window only.
- [ ] Re-dump and diff; confirm small, intentional changes; verify roster + win rule + Robe of Lords.
- [ ] Install mod, test from a New Game+ save; confirm Silence/burst beats the surge, the Samurai debut
      reads cleanly, and killing Cletienne yields the Robe of Lords.

## Test Questions

- Is it a tempo race — Silence/burst the surge mage, win the instant Cletienne falls (screen optional)?
- Is Magick Surge a fair comeback mechanic (Silence shuts it / burst beats it) and NOT an unavoidable wipe?
- Do the Samurai read as a clean Ch4 debut (Draw Out AoE/break, race-able), with Ninja tempo and a
  single effective Slow (no double-lock)?
- Is Cletienne clearly the rewarded target (win condition + Tier-S Robe of Lords)?
- Is it survivable on ONE loadout (no resupply, gauntlet 3/5)?
- Does it read as Cletienne's last stand in the dead city, not a designed mob?

## Sources

- Game8, "Necrohol of Mullonde Walkthrough (Battle 51)": boss Cletienne (Magick Surge), support 2 Samurai
  + 2 Ninja + 2 Time Mage, "Defeat Cletienne!", rec 60+, 3/5 stars, Silence-the-surge advice, spoils
  47,600 Gil + buried Elixirs.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553227
- Final Fantasy Wiki, "Cletienne Duroi": Knights Templar Sorcerer.
  https://finalfantasy.fandom.com/wiki/Cletienne_Duroi
- Local: `037-chapter-4-overview.md` (gauntlet + Tier-S tiering; Samurai as Ch4 caste), `052-mullonde-nave.md`
  (Cletienne retreats there), `055-monastery-vaults-fifth-level.md` (ledger reassignment), `044`/`045`
  (Time-Mage Slow / Ninja precedents), `057-lost-halidom.md` (gauntlet 4/5 — to be designed).
```
