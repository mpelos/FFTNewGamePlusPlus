# 057 - Lost Halidom

Status: designed (not yet implemented)
Chapter: 4 — "In the Name of Love"
Battle order: Battle 52 (ENDGAME GAUNTLET 4 of 5 — NO resupply across 49→50→51→52→53)
Target version: Enhanced v1.5.0
ENTD: global entry **TBD** — confirm on Windows game data
File: `battle_entd*_ent.bin` (TBD) / `OverrideEntryData` rows (TBD)

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `037-chapter-4-overview.md`. ENDGAME GAUNTLET: 49 (`054`) → 50 (`055`) → 51 (`056`) →
> 52 (`057`) → 53 (`058`), ONE loadout, no outfitter. THIS is the 5★ peak before the FINAL.

## Original Battle

Objective:

```text
Defeat Barich!   (the fight ends the instant Barich falls — the dragons/monsters are OPTIONAL. This is
                  the BARICH REMATCH — last seen at Bed Desert, 042; here he makes his final stand and DIES.)
```

Player deployment:

```text
Up to 5 units, including Ramza. No outfitter (gauntlet 4/5 — the hardest fight of the run).
```

Original enemy composition (verified via Game8, Battle 52):

```text
Barich Fendsor   (BOSS — Machinist/gunner; DISABLE + IMMOBILIZE status-locks; controls from range)
2x Hydra          (multi-headed dragons; LIGHTNING breath; up to 3 attacks/turn)
1x Tiamat          (apex dragon; elemental breath; up to 3 attacks/turn)
1x Dark Behemoth   (high-HP bruiser; heavy melee)
1x Chemist         (sustain — heals/revives the monster line)
```

Public walkthrough details:

```text
Recommended level: 60+.  Difficulty: 5/5 stars (the HARDEST fight of the endgame gauntlet).  Deploy up to 5.
Win: "Defeat Barich!" — the dragons/monsters are OPTIONAL (kill only Barich to end it).
TERRAIN: the Lost Halidom (a forsaken holy ground — the lost sanctuary).
THE THREAT — a DRAGON-BREATH CROSSFIRE under a CONTROL BOSS: 2 Hydra + 1 Tiamat each unleash ELEMENTAL
  BREATH up to THREE times per turn (multi-target AoE), a Dark Behemoth bruises the front, and a Chemist
  keeps the monster line alive — while BARICH locks your units with DISABLE / IMMOBILIZE from range.
WALKTHROUGH TIPS: DISABLE the monsters first (Mustadio's Arm Shot / break their attack) to blunt the
  3x-per-turn breath; answer Barich's Disable/Immobilize (status immunity — RIBBON now available from 053);
  then burst Barich. Do NOT try to out-trade the dragons.
Spoils: 41,900 Gil; buried treasure (Elixirs).
```

Design reading:

The Lost Halidom is **the dragon-pit peak** of the gauntlet — a **5/5★ multi-monster breath crossfire
under a control boss**, and the **Barich rematch** (Bed Desert, `042`); here he makes his last stand and
**dies**. Its identity is **survive the elemental breath storm while answering the boss's status control**:
two Hydras and a Tiamat fire **multi-target breath up to three times a turn**, a Dark Behemoth pins the
front, a Chemist sustains them, and **Barich Disables/Immobilizes** to freeze your answers. Because the
win condition is *defeat Barich*, it rewards **disabling the monsters, breaking the status lock, and
bursting the gunner** rather than grinding the dragon line.

For New Game++ the identity must stay: **the hardest fight of the run — a 3x-per-turn dragon-breath
crossfire (2 Hydra + Tiamat + Dark Behemoth) sustained by a Chemist, under Barich's Disable/Immobilize
control; win the instant Barich falls — the 5★ peak before the FINAL, on no resupply.** And because this
is the **Lost Halidom** — a forsaken holy ground — its Tier-S is **the enshrined relic, the Materia
Blade**, recovered by clearing the sanctuary.

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm slots: Barich (gunner) + 2 Hydra + 1 Tiamat + 1 Dark Behemoth + 1 Chemist. NO outfitter (gauntlet 4/5).
Confirm the win condition: fight ENDS when Barich falls (monsters optional).
Keep the 3x-per-turn dragon BREATH crossfire + the Dark Behemoth bruiser + the Chemist sustain +
  Barich's DISABLE/IMMOBILIZE control. These ARE the fight (the hardest of the gauntlet).
Confirm whether OverrideEntryData carries Level / monster stats, or leaves them at -1.
Set the Tier-S MATERIA BLADE as the ENSHRINED RELIC of the Lost Halidom — a GUARANTEED special treasure
  recovered on victory (a sacred blade of the holy ground), NOT on Barich (a gunner wields no sword).
  Barich carries no separate rare (his Glacial Gun was already the Bed Desert reward, 042).
Leave the buried Elixir spots as-is — existing loot.
```

Job / unit IDs (carry over known, verify the rest in-game):

```text
Barich  — Machinist/gunner job id   (TBD - verify; Disable/Immobilize; cf. 042 Bed Desert)
Hydra unit id        (TBD - verify; lightning breath; 3 attacks/turn)
Tiamat unit id       (TBD - verify; apex; elemental breath; 3 attacks/turn)
Dark Behemoth unit id (TBD - verify; high-HP melee)
Chemist job id       (TBD - verify; Item sustain)
```

## Job Escalation (Chapter 4 rule)

```text
CHANGE: keep the packed 5★ monster pit (2 Hydra + Tiamat + Dark Behemoth + Chemist + Barich) — it is
  already the chapter's apex roster; no padding. Bring it to endgame strength (Barich full boss 105,
  Tiamat/Dark Behemoth 104, Hydra 103, Chemist 103) and let the 3x-BREATH crossfire + status control be
  the demand. The "new content" is the SCALE of the monster crossfire, not a new generic job.
WHY: the chapter wants more challenge while keeping strategy. Here the escalation is the sheer multi-
  target breath density (up to 9+ breath hits/turn across three dragons) plus a control boss — answered by
  disabling the monsters (Arm Shot / break) and breaking the status lock, exactly the vanilla tactics at
  endgame intensity. Adding generics would dilute the monster-pit identity.
CONSTRAINTS (carried): BARICH DISABLE/IMMOBILIZE — ONE source, telegraphed, RESISTABLE/cleansable; the
  player has earned status immunity (RIBBON, 053) and Esuna-tier cleanses, so it is NOT a permanent hard
  lock; Barich does not chain-lock the whole party. DRAGON BREATH = ELEMENTAL (resistable with elemental
  gear/absorb), spaceable, and the monsters are DISABLE-able (Arm Shot / break) — dangerous but answerable.
  CHEMIST sustain = race-able (kill it or out-damage). DARK BEHEMOTH = a melee bruiser (no status).
WHAT IS NOT CHANGED: the monster pit, the breath crossfire, the Chemist sustain, Barich's control, and the
  "Defeat Barich" win rule remain.
```

## Sanctioned exceptions (carried precedents)

```text
BARICH DISABLE/IMMOBILIZE (ONE source) — status control; telegraphed, RESISTABLE/cleansable, immunity-
  answerable (RIBBON earned at 053); NOT a permanent hard lock, no full-party chain-lock.
DRAGON BREATH (2 Hydra + Tiamat, 3x/turn) — ELEMENTAL multi-target AoE; resistable (elemental gear/absorb),
  spaceable, and the monsters are DISABLE-able (Arm Shot / break). The 5★ core threat — dangerous but fair.
DARK BEHEMOTH — high-HP melee bruiser; no status; a damage sponge to space around.
CHEMIST SUSTAIN — heals/revives the monster line; race-able (kill it or out-damage).
WIN-ON-BARICH-FALLS — defeating Barich ends the fight; the monsters are optional (vanilla rule).
```

## Boss rare loot — TIER-S (the enshrined relic)

```text
LOST HALIDOM RELIC → MATERIA BLADE (Tier-S — the sacred blade enshrined at the holy ground; enables
  sword-skill / advanced abilities on its wielder).
  A GUARANTEED special treasure recovered on VICTORY (a relic of the forsaken sanctuary), NOT a boss
  drop — Barich is a gunner and wields no sword, so the blade is the holy ground's own relic. THEMATIC:
  "Lost Halidom" = a lost holy relic/sanctuary; the legendary blade is exactly what was lost here.
  Barich carries NO separate rare (his Glacial Gun was the Bed Desert reward, 042). The monsters drop
  nothing rare (untameable apex beasts). Buried Elixirs stay as-is.
```

> Tier-S ledger: Chaos Blade (Folmarv, 052) · Ribbon (Zalbaag, 053) · Escutcheon (Loffrey, 055) · Robe of
> Lords (Cletienne, 056) · **Materia Blade (Lost Halidom relic, 057)** · Ragnarok (FINAL, 058). Excalibur
> stays with Orlandeau (player) — never on an enemy.

## Proposed Composition (New Game++ Lost Halidom v1)

Keep the apex pit; no padding. Barich (full boss, he dies) `105`; Tiamat & Dark Behemoth `104`; Hydras &
Chemist `103`.

| Slot | Role | Job / Unit | Level | Purpose |
|------|------|-----------|-------|---------|
| n | Barich (BOSS, objective) | Machinist/gunner | `105` | Disable/Immobilize control; the intended kill; ends the fight. |
| n | Tiamat | Apex dragon | `104` | Elemental breath, 3x/turn; the heaviest crossfire source. |
| n | Hydra | Dragon | `103` | Lightning breath, 3x/turn; disable-able (Arm Shot). |
| n | Hydra | Dragon | `103` | Second Hydra; widens the breath storm. |
| n | Dark Behemoth | Bruiser | `104` | High-HP melee; pins the front; space around it. |
| n | Chemist | Chemist | `103` | Sustain — heals/revives the monster line; race-able. |

Reasoning:

The faithful move is **the apex monster pit kept brutal but fair**. Three dragons (Tiamat `104` + 2 Hydra
`103`) fire **breath up to 3x/turn** — the 5★ core threat — but it's **elemental** (resistable) and the
monsters are **disable-able** (Arm Shot / break); the Dark Behemoth (`104`) is a sponge to space around;
the Chemist (`103`) sustains them (race-able). **Barich `105`** controls with **Disable/Immobilize**, now
answerable because the player earned **Ribbon at 053** and carries cleanses. Win-on-Barich-falls preserves
the original's *disable the beasts, break the lock, burst the gunner* tactics — on no resupply, the
hardest fight before the FINAL. The Materia Blade is recovered as the sanctuary's enshrined relic.

## Builds (apex monster pit + control boss)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Barich Fendsor (Lv 105) — BOSS, objective

```text
Job: Machinist/gunner (id TBD)   JobLevel: 8   Primary: gun + DISABLE / IMMOBILIZE (ONE source, resistable)
Reaction: Reflexes / Damage Split (id TBD)   Support: break-resist / Defense Boost (id TBD)   Movement: Move +2 (id TBD)
Head: Genji Helm-tier (id TBD)   Body: heavy boss armor (id TBD)
Accessory: status-resist accessory (id TBD)   Right hand: strong gun (id TBD; NOT the Glacial Gun — looted at 042)
The intended kill; answer his control (Ribbon/cleanse), then burst. Status NOT a permanent hard lock.
```

Role: the control boss; ends the fight; no separate rare (gun looted at 042).

### Tiamat (Lv 104) — apex dragon

```text
Unit: Tiamat (id TBD)   Elemental BREATH (multi-target AoE), up to 3 attacks/turn.
Reaction: Counter-tier (id TBD)   Movement: Move +2 / fly (id TBD)
Breath is ELEMENTAL (resistable); DISABLE-able via Arm Shot / break. The heaviest crossfire source.
```

Role: the apex breath threat; spaceable and disable-able.

### Hydra x2 (Lv 103) — dragons

```text
Unit: Hydra (id TBD)   LIGHTNING breath (multi-target), up to 3 attacks/turn.
Reaction: Counter-tier (id TBD)   Movement: Move +2 (id TBD)
Resistable (lightning gear/absorb); disable-able (Arm Shot / break).
```

Role: widen the breath storm; answerable with elemental defense + disable.

### Dark Behemoth (Lv 104) — bruiser

```text
Unit: Dark Behemoth (id TBD)   High-HP heavy melee; no status.
Reaction: Counter (442)   Movement: Move +1 (id TBD)
A damage sponge to space around — not the objective.
```

Role: front-line pressure; soak, don't trade.

### Chemist (Lv 103) — sustain

```text
Job: Chemist (id TBD)   JobLevel: 8   Primary: Item (X-Potion / Phoenix Down — heals/revives the monsters)
Reaction: Reflexes (449)   Support: Move-Find Item / Defense Boost (id TBD)   Movement: Move +1 (486)
Race-able — kill it or out-damage its sustain.
```

Role: keeps the monster line alive; a priority secondary target.

## Positioning Plan

```text
The Lost Halidom (forsaken holy ground): place Barich at range/back (the control boss you must reach and
  burst); the Tiamat + 2 Hydra spread across the field for overlapping breath crossfire; the Dark Behemoth
  forward as a wall; the Chemist behind the monsters to sustain them. Keep open sightlines (the breath
  crossfire IS the fight) and any sacred elevation of the halidom.
Preserve: the 3x-breath monster pit + Chemist sustain + Barich's control, and the win-on-Barich-falls
  rule. The Materia Blade is the enshrined relic, recovered on victory.
```

The lost sanctuary should say: "the holy ground is a dragons' den now, and Barich would freeze you in
their fire — disable the beasts, break his hold, and end him; the blade enshrined here is your reward."

## Implementation Checklist

- [ ] Identify Lost Halidom `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify Barich + 2 Hydra + 1 Tiamat + 1 Dark Behemoth + 1 Chemist.
- [ ] Confirm win condition: fight ENDS when Barich falls (monsters optional).
- [ ] Keep dragon 3x-breath (elemental, resistable, disable-able); Barich Disable/Immobilize ONE source,
      resistable/cleansable (NOT a permanent hard lock); Chemist sustain race-able.
- [ ] Set levels: Barich `105`; Tiamat & Dark Behemoth `104`; Hydras & Chemist `103`.
- [ ] Set the Tier-S **Materia Blade** as a GUARANTEED relic recovered on victory (not on Barich); swap
      Barich's gun OFF the Glacial Gun (looted at 042).
- [ ] Patch via the correct layer; keep the diff inside the Lost Halidom window only.
- [ ] Re-dump and diff; confirm small, intentional changes; verify roster + win rule + Materia Blade relic.
- [ ] Install mod, test from a New Game+ save; confirm it plays as the 5★ peak — breath is survivable with
      elemental defense + disable, the status lock is answerable, and victory yields the Materia Blade.

## Test Questions

- Is it the hardest fight of the run (5★) — a genuine 3x-per-turn dragon-breath crossfire under a control boss?
- Is the breath answerable (elemental resist/absorb + disable the monsters via Arm Shot/break), not an
  unavoidable wipe?
- Is Barich's Disable/Immobilize ONE resistable/cleansable source (Ribbon from 053 / Esuna), NOT a
  permanent party-wide hard lock?
- Is Barich clearly the rewarded target (win condition), with the Materia Blade recovered as the
  sanctuary's relic (not on the gunner)?
- Is it survivable on ONE loadout as the 4th of five no-resupply fights — brutal but fair before the FINAL?
- Does it read as a desecrated holy ground turned dragon den, not a designed arena?

## Sources

- Game8, "Lost Halidom Walkthrough (Battle 52)": roster (Barich + 2 Hydra + 1 Tiamat + 1 Dark Behemoth +
  1 Chemist), "Defeat Barich!" (monsters optional), rec 60+, 5/5 stars, dragon breath 3x/turn + Barich
  Disable/Immobilize, Arm-Shot-the-monsters advice, spoils 41,900 Gil + buried Elixirs.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553228
- Local: `037-chapter-4-overview.md` (gauntlet + Tier-S tiering), `042-bed-desert.md` (Barich first
  fight; Glacial Gun reward), `053-mullonde-sanctuary.md` (Ribbon — the status-immunity answer earned
  before this fight), `058-airship-graveyard.md` (the FINAL — to be designed).
```
