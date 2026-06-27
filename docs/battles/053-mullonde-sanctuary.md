# 053 - Mullonde Cathedral Sanctuary (Murond Holy Place)

Status: ✅ implemented (v1, entry 462) — TIER-S (Ribbon)
Chapter: 4 — "In the Name of Love"
Battle order: Battle 48 (Mullonde chain 3 of 3 — NO resupply across 46→47→48)
Target version: Enhanced v1.5.0
ENTD: global entry **462** (local 78, entd4)
File: `battle_entd4_ent.bin`

## Implemented (v1, entry 462)

```text
DATA (story order 459->460->461->462; verified from dump):
  slot 0 = Folmarv (name 36, eq=255, lvl 254) -> INACTIVE cutscene placeholder (left untouched).
  slot 1 = Zalbaag (name 51, job 51 Ark-Knight-class; jl8; eq head154/body182/acc210/rh30 Runeblade/
           lh139 shield) -> the ACTIVE vampire boss + Tier-S carrier. Has real equip slots.
  slots 2,3 = Archaeodaemon (job 153, undead) -> reraise + HP-drain screen.
  slot 4 = Ultima Demon (job 154) -> telegraphed Ultima pressure (optional target).
  slot 5 = job 51 clone (name255, eq=255, lvl 254) -> scripting placeholder (left untouched).
  NOTE: TIC names Zalbaag's undead boss form name_id 51 (not the standard low-range id); confirmed by
  the active Ark-Knight+Runeblade profile + the demon screen + win="Defeat Zalbaag".

CHANGE: scale + Tier-S reward. Zalbaag 105, accessory set to RIBBON (171) = the Tier-S steal/drop on
  the named kill target (he DIES as the win condition -> guaranteed). Kept his Runeblade (the equip-break
  weapon) + vampirism/undead flags + scripting (only level + acc changed). Archaeodaemons & Ultima Demon
  103. Win-on-Zalbaag-falls, vampirism (sole source), Runeblade break, and undead reraise all preserved.
  No buried treasure (vanilla) -> Gil + Elixir spoils unchanged.
```

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `037-chapter-4-overview.md`. MULLONDE CHAIN: 46 (`051`) → 47 (`052`) → 48 (`053`), one loadout.

## Original Battle

Objective:

```text
Defeat Zalbaag!   (the fight ends the instant Zalbaag falls — the Ultima Demon / Archaeodaemons are
                   OPTIONAL. Zalbaag is Ramza's second brother, raised as an undead vampire.)
```

Player deployment:

```text
Up to 5 units, including Ramza. No outfitter (chain 3/3 — last of the Mullonde gauntlet).
```

Original enemy composition (verified via Game8, Battle 48):

```text
Zalbaag Beoulve   (BOSS — Ark Knight; VAMPIRE / undead; Runeblade equip-break + vampirism/HP-drain)
2x Archaeodaemon  (undead demons — HP-drain, reraise/undead pressure)
1x Ultima Demon   (Chapter-4 demon caste — body double; Ultima / self-destruct threat)
```

Public walkthrough details:

```text
Recommended level: ~60.  Difficulty: 4/5 stars.  Deploy up to 5.
Win: "Defeat Zalbaag!" — the Ultima Demon and Archaeodaemons are OPTIONAL (kill only Zalbaag to end it).
TERRAIN: the cathedral SANCTUARY — the holy inner chamber (the Mullonde climax).
THE THREAT — ZALBAAG, the VAMPIRE Ark Knight: he inflicts VAMPIRISM on your units (HP-drain / turn),
  and wields a RUNEBLADE (Ark-Knight powerful-sword) that breaks gear. His demon screen (2 Archaeodaemon
  + 1 Ultima Demon) drains HP and threatens Ultima; the Archaeodaemons are UNDEAD (reraise pressure).
WALKTHROUGH TIPS: equip JAPA MALA / HOLY WATER to counter vampirism; use REND / CRUSH WEAPON to
  permanently disable his Runeblade; holy damage answers the undead demons. Ultima Demons cannot be
  tamed or poached — pure threats.
Spoils: 32,800 Gil, 1x Elixir. NO buried treasure here.
```

Design reading:

The Sanctuary is **the tragic undead-brother climax** of the Mullonde gauntlet: **Zalbaag Beoulve**,
Ramza's second brother, raised as a **vampire Ark Knight**, flanked by **undead demons and an Ultima
Demon** in the holy inner chamber. Its identity is **a release-the-cursed-brother boss fight under two
attrition threats** — his **vampirism** (HP-drain / turn-your-units, answered by Holy Water / Japa
Mala) and his **Runeblade equip-break** (answered by Rend / Crush), while an **undead demon screen**
(reraise + HP-drain + an Ultima Demon's Ultima) grinds the party on **no resupply**. Because the win
condition is *defeat Zalbaag*, it rewards cutting through the demons to **free the brother**, not
clearing the room.

For New Game++ the identity must stay: **the vampiric undead-brother boss whose vampirism and Runeblade
equip-break are answerable-but-real, screened by undead demons + an Ultima Demon, win the instant
Zalbaag falls — the tragic climax of the Mullonde chain on no resupply.** And because Zalbaag **dies**
(the win condition), this is a clean Tier-S payout: **Zalbaag carries the Ribbon** — the crown that
would have warded the curse, taken from the brother freed in death.

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm slots: Zalbaag (Ark Knight, vampire/undead) + 2 Archaeodaemon + 1 Ultima Demon. NO outfitter (chain 3/3).
Confirm the win condition: fight ENDS when Zalbaag falls (demons optional).
Keep Zalbaag's VAMPIRISM (HP-drain / turn) + the RUNEBLADE equip-break + the undead-demon screen
  (reraise + Ultima Demon). These ARE the fight.
Confirm whether OverrideEntryData carries Level / equipment / Undead flag, or leaves them at -1.
Set Zalbaag's drop/steal = the Tier-S RIBBON (see Boss rare loot). Demons drop nothing rare (untameable).
NO buried treasure here (vanilla) — leave as-is.
```

Job IDs (carry over known, verify the rest in-game):

```text
Zalbaag      — Ark Knight job id        (TBD - verify; vampire/undead; Runeblade; cf. Elmdore 048)
Archaeodaemon — undead demon job id     (TBD - verify; reraise/undead; HP-drain)
Ultima Demon — Ch4 demon caste job id   (TBD - verify; Ultima / self-destruct; cf. 048/049)
```

## Job Escalation (Chapter 4 rule)

```text
CHANGE: keep the tragic boss-and-demons shape (no generic padding — it would cheapen the brother's
  climax), but make the DUAL attrition the demand: Zalbaag as a genuine VAMPIRE (vampirism status +
  HP-drain) AND Runeblade equip-breaker, screened by an UNDEAD demon line (Archaeodaemon reraise) and
  the Ch4 ULTIMA DEMON caste. Two recoverable threats (status + equip-break) layered on undead reraise.
WHY: the chapter wants more challenge via jobs WITHOUT breaking strategy. Here the escalation is the
  STATUS+DRAIN+UNDEAD stack — you must bring anti-undead/anti-vampire answers and disarm the Runeblade,
  then cut to Zalbaag. The Ultima Demon caste IS the new-job content; padding with generics would dull
  the tragedy. Consistent with prior tragic-boss docs (Wiegraf, Elmdore).
CONSTRAINTS (carried): VAMPIRISM CAPPED — Zalbaag is the SOLE vampirism source; cleansable (Holy Water /
  Esuna), counter-gear (Japa Mala / anti-undead), telegraphed — NOT a permanent hard lock; it does NOT
  chain-spread uncontrollably (the demons HP-drain but do not vampirize). RUNEBLADE equip-break = ONE
  source, answerable (Rend / Crush / break-resist), recoverable (039/052 precedent). ULTIMA DEMON Ultima
  = telegraphed, race-able/space-able, no instant party-wipe (048/049 precedent). UNDEAD reraise on the
  demon line = put down with holy / finish while down (049 precedent).
WHAT IS NOT CHANGED: Zalbaag the vampire Ark Knight, the demon screen, and the "Defeat Zalbaag" win
  rule remain. No generics added.
```

## Sanctioned exceptions (carried precedents)

```text
VAMPIRISM (Zalbaag, SOLE source) — HP-drain / turn-a-unit; cleansable (Holy Water / Esuna), countered
  by Japa Mala / anti-undead gear, telegraphed, NON-spreading — NOT a hard lock.
RUNEBLADE EQUIP-BREAK (Zalbaag, ONE source) — Ark-Knight powerful-sword break; answer = Rend / Crush /
  break-resist (039 Bervenia, 048 Elmdore, 052 Nave precedents). Capped, recoverable.
UNDEAD RERAISE (2 Archaeodaemon) — undead demons reraise; answer = holy damage / Holy Water / finish
  while downed (049 Undercroft precedent). HP-drain, no vampirism.
ULTIMA DEMON (1) — Ch4 demon caste; Ultima / self-destruct telegraphed, race-able/space-able, no instant
  wipe (048/049 precedent). Untameable / unpoachable (vanilla).
WIN-ON-ZALBAAG-FALLS — defeating Zalbaag ends the fight; the demons are optional (vanilla rule).
```

## Boss rare loot — TIER-S

> **Updated (2026-06-27 rebalance):** Zalbaag now ALSO drops **Ragnarok (s1)**, relocated here from the
> Ultima fight so the player holds the best sword before the no-resupply gauntlet. Ribbon (s2) unchanged;
> the Elixir spoil moves to s3. Canonical: `chapter-4-rewards-implementation.md`.

```text
ZALBAAG BEOULVE → RIBBON (Tier-S — the ultimate accessory: all-status immunity).
  Steal-or-drop on Zalbaag, who DIES as the win condition (guaranteed obtainable on a focus kill).
  THEMATIC: the crown that would have warded the vampiric curse — taken from Ramza's brother, freed in
  death. A fitting best-of-best for the chain's tragic climax.
  The Archaeodaemons / Ultima Demon drop NOTHING rare (untameable, unpoachable — vanilla).
  NO buried treasure here (vanilla) — only the 32,800 Gil + Elixir spoils stay.
```

> Tier-S ledger (per 037 / 052): Chaos Blade (Folmarv, 052) · **Ribbon (Zalbaag, 053)** · Robe of Lords
> (Loffrey, 055) · Materia Blade (Cletienne, 056) · Escutcheon (Lost Halidom, 057) · Ragnarok (FINAL
> capstone, 058). Excalibur stays with Orlandeau (player) — never on an enemy.

## Proposed Composition (New Game++ Mullonde Sanctuary v1)

Keep the boss + demon screen; no generics. Zalbaag (tragic climax) `105`; Ultima Demon `103`;
Archaeodaemons `103`.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Zalbaag (BOSS, objective) | Ark Knight (vampire/undead) | `105` | Vampirism + Runeblade equip-break; carries Tier-S Ribbon; the intended kill. |
| n | Archaeodaemon | Undead demon | `103` | Undead reraise + HP-drain; screen Zalbaag; holy answers it. |
| n | Archaeodaemon | Undead demon | `103` | Second undead; reraise pressure; finish while down. |
| n | Ultima Demon | Demon caste | `103` | Ultima / self-destruct (telegraphed, race-able); optional but punishing. |

Reasoning:

The faithful move is **the brother and his demons, no padding** — the pressure is the **status+drain+
undead stack**, not numbers. Zalbaag (`105`) brings two answerable threats (vampirism → Holy Water /
Japa Mala; Runeblade break → Rend / Crush); the **undead demon screen** (2 Archaeodaemon `103`) reraises
and drains, demanding holy damage to keep down; the **Ultima Demon `103`** threatens a telegraphed
Ultima you must space around. Win-on-Zalbaag-falls preserves the original's *cut to the brother and
free him* tactics — on no resupply, the climax of Mullonde. A 4/5★ tragic boss fight, harder than the
Nave by virtue of the undead/drain attrition.

## Builds (boss-tier; cursed-Beoulve flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Zalbaag Beoulve (Lv 105) — BOSS, objective, Tier-S carrier

```text
Job: Ark Knight (id TBD)   JobLevel: 8   Primary: Runeblade / Unyielding Blade (equip-break + drain)
  + VAMPIRISM (HP-drain / turn — SOLE source, cleansable, telegraphed, NON-spreading)
Reaction: Damage Split / Reflexes (id TBD)   Support: break-resist / Defense Boost (id TBD)   Movement: Move +2 (id TBD)
Head: Genji Helm-tier (id TBD)   Body: heavy boss armor (id TBD)
Accessory: RIBBON (Tier-S steal/drop, id TBD)   Right hand: Runeblade (id TBD)   Left: shield (id TBD)
The intended kill; answer vampirism (Holy Water / Japa Mala) + disarm the Runeblade (Rend/Crush), then burst.
```

Role: the tragic vampire brother; two answerable threats + the Tier-S Ribbon; the focus target.

### Archaeodaemon x2 (Lv 103) — undead screen

```text
Job: Archaeodaemon / undead demon (id TBD)   JobLevel: 8   Undead (RERAISE) + HP-drain.
Reaction: Counter (442)   Support: Defense Boost (id TBD)   Movement: Move +2 (id TBD)
Undead — answered by holy damage / Holy Water / finishing while downed. No vampirism (drain only).
```

Role: reraise pressure + HP-drain; the screen between the party and Zalbaag.

### Ultima Demon (Lv 103) — demon caste

```text
Job: Ultima Demon / demon caste (id TBD)   JobLevel: 8   Ultima / self-destruct (telegraphed, race/space-able).
Reaction: Reflexes (449)   Support: MA-boost (id TBD)   Movement: Move +2 (id TBD)
Untameable / unpoachable (vanilla). Optional target — pressure, not the objective.
```

Role: a telegraphed Ultima threat you space around; punishes clustering.

## Positioning Plan

```text
The cathedral SANCTUARY (holy inner chamber): place Zalbaag at the altar / back-center as the climax;
  the 2 Archaeodaemon forward as the undead screen; the Ultima Demon to one flank (forcing the party to
  avoid clustering near its Ultima). Keep the holy-chamber elevation. The player must punch through the
  undead screen (holy damage) and answer vampirism/break to reach Zalbaag.
Preserve: boss + demon screen (no generics), the dual attrition (status + equip-break) on undead reraise,
  and the win-on-Zalbaag-falls rule. The Ribbon rides on Zalbaag, the intended target.
```

The sanctuary should say: "the last of the Knights Templar's puppets is your own brother, cursed to
undeath — break the blade, lift the curse, and free him; the Ribbon is what should have saved him."

## Implementation Checklist

- [ ] Identify Mullonde Sanctuary `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify Zalbaag + 2 Archaeodaemon + 1 Ultima Demon, and the Undead/vampire flags.
- [ ] Confirm win condition: fight ENDS when Zalbaag falls (demons optional).
- [ ] Keep vampirism on Zalbaag ONLY (sole source, cleansable, telegraphed, non-spreading); Runeblade
      equip-break ONE source (Rend / Crush / break-resist answerable).
- [ ] Keep undead reraise on the 2 Archaeodaemon (holy answer); Ultima Demon Ultima telegraphed/race-able.
- [ ] Set levels: Zalbaag `105`; Ultima Demon & Archaeodaemons `103`. JobLevel `8` on all slots.
- [ ] Set Zalbaag's steal/drop = Tier-S **Ribbon**; demons carry NO rare (untameable). NO buried treasure.
- [ ] Patch via the correct layer; keep the diff inside the Mullonde Sanctuary window only.
- [ ] Re-dump and diff; confirm small, intentional changes; verify roster + win rule + Ribbon.
- [ ] Install mod, test from a New Game+ save; confirm vampirism/break are answerable (not hard locks),
      undead reraise demands holy, and killing Zalbaag yields the Ribbon.

## Test Questions

- Is it a focus kill on the tragic brother — win the instant Zalbaag falls (demons optional)?
- Are BOTH boss threats answerable (vampirism → Holy Water / Japa Mala / Esuna; Runeblade → Rend / Crush)
  and NOT hard locks; does vampirism stay single-source and non-spreading?
- Does the undead screen demand holy damage (reraise / finish-while-down), and is the Ultima Demon's
  Ultima telegraphed and space-able (no instant wipe)?
- Is Zalbaag clearly the rewarded target (win condition + Tier-S Ribbon)?
- Is it survivable on ONE loadout (no resupply, chain 3/3 — the longest sustained stretch yet)?
- Does it read as freeing a cursed brother in the holy chamber, not a designed mob?

## Sources

- Game8, "Mullonde Cathedral Sanctuary Walkthrough (Battle 48)": roster (Zalbaag Ark Knight + 2
  Archaeodaemon + 1 Ultima Demon), "Defeat Zalbaag!" (demons optional), rec ~60, 4/5 stars, vampire/
  vampirism threat + Japa Mala / Holy Water counter, Runeblade + Rend/Crush advice, untameable Ultima
  Demons, spoils 32,800 Gil + Elixir, no buried treasure.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553208
- Final Fantasy Wiki, "Zalbaag Beoulve": Ark Knight, undead/vampire raising, the Beoulve tragedy.
  https://finalfantasy.fandom.com/wiki/Zalbaag_Beoulve
- Local: `037-chapter-4-overview.md` (Tier-S tiering), `048-limberry-keep.md` (Elmdore Ark Knight),
  `049-limberry-undercroft.md` (undead reraise guard), `052-mullonde-nave.md` (chain 2/3; equip-break),
  `051-mullonde-exterior.md` (chain 1/3).
```
