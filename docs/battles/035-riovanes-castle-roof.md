# 035 - Riovanes Castle Roof — Elmdor & the Assassins

Status: designed (not yet implemented)
Chapter: 3 — "The Valiant" — **CHAPTER FINALE**
Battle order: Battle 32 (after Riovanes Castle Keep) — **Riovanes chain 3 of 3 (close)**
Target version: Enhanced v1.5.0
ENTD: global entry **TBD** — confirm on Windows game data
File: `battle_entd*_ent.bin` (TBD) / `OverrideEntryData` rows (TBD)

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `024-chapter-3-overview.md`.

## Original Battle

Objective:

```text
Save Rapha!  (protect the NPC — the mission fails if Rapha is defeated.)
WIN CONDITION: force the enemy to FLEE. The moment ONE assassin (Celia or Lettie) reaches CRITICAL
  HP, ALL THREE enemies retreat and the fight ends instantly. You do NOT defeat them — you drive
  them off. Elmdor and both assassins ESCAPE (Elmdor reappears at Limberry in Chapter 4).
```

Player deployment:

```text
Up to 4 units, including Ramza (a SMALLER squad than usual). Protected NPC: RAPHA (fail on death).
On completion, MARACH and RAPHA are recruited.
CHAIN: arrives from the Keep on one loadout (closes the no-resupply Riovanes chain).
```

Original enemy composition:

```text
1x Elmdore   (Arc Knight — draw-out/Iaido; debuffs; teleport)
1x Celia     (Assassin — high mobility / teleport; nasty status / instant-death tools)
1x Lettie    (Assassin — high mobility / teleport; nasty status / instant-death tools)
```

Public walkthrough details:

```text
Recommended level: ~36.  Difficulty: 2/5 stars (it is a RACE, not a slugfest).
Rooftop arena. Protect Rapha — her death fails the mission.
The intended play: IGNORE Elmdor's debuffs and focus ALL damage on ONE assassin (Celia or Lettie).
  As soon as one hits critical, all three flee and the fight ends — so it is a RACE to a threshold.
The assassins are fast and teleport, with dangerous status/instant-death; Elmdor adds debuffs.
```

Design reading:

The Roof is **the chapter's coda — a race-to-flee under assassin pressure**. Unlike every prior
boss, you cannot win by killing: the enemy is built to **escape the instant you hurt one assassin
enough**, so the fight is a sprint — **burst one assassin to critical before the teleporting killers
(and Elmdor's debuffs) can put down the fragile Rapha**. It introduces the **Assassin** caste — the
most mobile, most lethal generic in the game — as a pair of named threats who flicker around the
roof toward the protected NPC. The lesson is **focus and tempo under a protect condition**: pick a
target, ignore the noise (Elmdor), and end it fast. Nobody dies here — Elmdor and the assassins
slip away to return in Chapter 4 — so it is a *threat* finale, not a kill, and a deliberate
exhale (2/5★) after the Velius spike, gated only by the protect-Rapha condition and the smaller
4-unit squad.

For New Game++ the identity must stay: **a small-squad rooftop race to drive off two teleporting
assassins (and Elmdor) by bursting ONE to critical, before they kill the protected Rapha — focus
and tempo, not a defeat-all; everyone escapes.**

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm slots: Elmdore + Celia + Lettie, plus the (max 4) player slots and RAPHA's protected NPC slot.
CRITICAL: preserve the FLEE-ON-CRITICAL scripting (one assassin to critical -> all three retreat,
  fight ends) and the "Save Rapha" fail-on-death objective. Preserve the 4-unit deploy cap.
ALL THREE ENEMIES ESCAPE — none die here; Elmdor's best loot (Masamune / Genji) is a Chapter 4
  (Limberry) matter, NOT here.
Preserve the rooftop geometry and the assassins' teleport/high-mobility.
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
```

Job IDs (carry over known, verify the rest in-game):

```text
Arc Knight job id   (TBD - verify; Elmdore — draw-out/Iaido; teleport)
Assassin job id     (TBD - verify; Celia & Lettie — FIRST Assassins in the mod; teleport + status/death)
```

## Job Escalation (Chapter 3 rule)

```text
THE NEW CASTE IS BUILT IN: this finale debuts the ASSASSIN (Celia & Lettie) — the most mobile,
most lethal generic, with teleport and status/instant-death tools — as named threats to the
protected Rapha, alongside Elmdor's Arc-Knight debuffs. The Assassin caste IS this fight's
escalation; per "one new wrinkle per fight," NO additional generic job is added. Keep the
Elmdor + Celia + Lettie shape.
WHY: teleporting killers that race a protect target, in a flee-on-critical sprint, is a genuinely
  new tactical problem (focus one, ignore the rest, beat the clock). Nothing else is needed.
```

## Sanctioned exceptions (carried + new precedent)

```text
ASSASSIN status / instant-death — allowed as a BOSS-tier threat, CONSTRAINED (new precedent, in the
  spirit of the Cúchulainn 022 / Velius 034 caps):
  ALLOWED: the assassins' signature status / instant-death tools on Celia & Lettie.
  GUARDRAILS: NOT unavoidable and NOT spammed — instant-death/status must be RESISTABLE (accessory
    immunity, Faith/positioning) and not land every turn; NO permanent hard lock (no Stop/Don't Act
    chain) that makes the race impossible. The flee-on-critical win condition is itself the pressure
    valve: the player can END the fight quickly, so the danger window is short by design — keep it that way.
TELEPORT / high mobility — allowed and intended (it is the Assassin's identity); preserve it so the
  threat to Rapha is real, but keep the fight endable by focusing one assassin.
ELMDOR debuffs — allowed, soft/ignorable (the guide says ignore them); NO hard lock from Elmdor either.
```

## Boss rare loot

```text
None. All three enemies FLEE — none die here, so there is nothing to drop (retreat = no rare, per
Gallows 020 / Zalmo 026 / Wiegraf-Vaults 029 / Marach 031&033). ELMDOR's iconic best loot — the
MASAMUNE and the GENJI set — is BEST-tier and RESERVED for Chapter 4, obtained at his LIMBERRY
rematch where he can actually be fought for it. Do NOT place any rare here.
The map's rare TREASURE (Jade Armlet / Elven Cloak / Orichalcum Dirk / Kodachi) is existing map
treasure, not boss loot; leave it as-is.
```

## Proposed Composition (New Game++ Riovanes Roof v1)

Keep the exact trio; this is a race, not a slugfest. Elmdor `104`; assassins `103`. Smaller (4-unit)
player squad preserved.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Elmdore | Arc Knight | `104` | Debuffs + teleport; the "noise" to ignore. Escapes. |
| n | Celia (assassin, NEW caste) | Assassin | `103` | Teleporting killer; threatens Rapha. Burst HER to critical to end it. |
| n | Lettie (assassin, NEW caste) | Assassin | `103` | Second teleporting killer; the other valid focus target. Escapes. |

Reasoning:

The faithful move is to **preserve the flee-on-critical race and the protect-Rapha pressure, and
keep the assassins lethal-but-resistable**. Elmdor at `104` piles on ignorable debuffs; the two
Assassins at `103` flicker around the roof toward Rapha with status/instant-death — but because the
fight ENDS the moment one of them is bursted to critical, the player has a clear, fast out: focus
one assassin, shield Rapha, beat the clock. Constraining the instant-death to resistable, non-spam,
no-hard-lock keeps the small 4-unit squad's race fair. Nobody dies (all flee), so there is no loot —
the iconic Elmdor rewards wait for Chapter 4. A deliberate 2/5★ exhale after the Velius spike, gated
by the protect condition, that still showcases the new Assassin caste.

## Builds (final-shop quality; Elmdor's assassins flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Elmdore — Arc Knight (Lv 104) — escapes, no drop

```text
Job: Arc Knight (id TBD)   JobLevel: 8   Primary: Draw Out / Iaido (soft debuffs) — NO hard lock
Reaction: a defensive reaction (id TBD)   Support: Attack Boost (465)   Movement: Teleport / Move +1 (id TBD)
Head/Body: shop gear his job allows (ids TBD)
Accessory: Bracers (218)   Right hand: a shop-tier / NON-RARE katana (id TBD — NOT Masamune; he escapes,
  nothing drops; Masamune/Genji are his Chapter 4 Limberry loot)
ESCAPES — no rare here.
```

Role: the ignorable debuffer; teleports around but is not the win target.

### Celia & Lettie — Assassins (Lv 103) — NEW caste; escape

```text
Job: Assassin (id TBD)   JobLevel: 8   Primary: assassin status/instant-death tools (RESISTABLE, non-spam)
Support: Dual Wield or Martial-arts-tier (id TBD)
Reaction: First Strike (453) or Vanish (id TBD)   Movement: Teleport / Move +3 (id TBD — high mobility)
Head: Thief's Cap (168)   Body: Black Garb (198)   Accessory: a fast/evasion accessory (id TBD)
Right/Left hand: shop ninja blades / knives (ids TBD; NON-RARE — they escape, nothing drops)
GUARDRAILS: instant-death/status must be resistable and not every-turn; NO hard lock. Bursting EITHER
  to critical ends the fight (all flee) — preserve that trigger.
```

Role: the teleporting killers and the win condition — focus one to critical to drive the trio off.

## Positioning Plan

```text
The trio starts on the rooftop with teleport access to Rapha's vicinity, so the threat to the NPC
  is immediate; Rapha starts exposed (story placement).
Elmdor anchors as the debuff "noise"; Celia & Lettie flank/teleport toward Rapha.
Preserve the rooftop geometry, the assassins' teleport, the 4-unit deploy cap, the protect-Rapha
  fail condition, and the FLEE-ON-CRITICAL trigger (one assassin critical -> all retreat).
```

The roof should say: "you can't kill them — they'll vanish the moment you draw blood — so put all
your force on ONE knife-hand, fast, before they reach the girl."

## Implementation Checklist

- [ ] Identify Riovanes Roof `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify Elmdore + Celia + Lettie + (max 4) player slots + Rapha NPC slot.
- [ ] Confirm Arc Knight / Assassin job ids; keep teleport + status/death (RESISTABLE, non-spam, no lock).
- [ ] PRESERVE the flee-on-critical trigger, the protect-Rapha fail condition, and the 4-unit deploy cap.
- [ ] Give Elmdor a NON-RARE katana (no drop); assassins NON-RARE blades (no drop) — all escape.
- [ ] Set levels: Elmdor `104`; Celia & Lettie `103`.
- [ ] Set JobLevel `8` on all three.
- [ ] Confirm NO rare loot here; Masamune/Genji are deferred to Elmdor's Ch4 Limberry rematch.
- [ ] Patch via the correct layer; keep the diff inside the Riovanes Roof window only.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify flee trigger + Rapha + cap.
- [ ] Install mod, test from a New Game+ save; confirm bursting one assassin to critical ends the fight
      and that Rapha can be kept alive by a focused 4-unit squad.

## Test Questions

- Does bursting ONE assassin to critical end the fight (all flee), preserving the race identity?
- Are the teleporting assassins a real threat to Rapha while still being out-raced by focus fire?
- Is their instant-death/status resistable and non-spam (fair), with no hard lock on the small squad?
- Is ignoring Elmdor's debuffs the right read (he's noise, not the win target)?
- Does NOBODY die / nothing drop here, with Elmdor's Masamune+Genji correctly deferred to Ch4?
- Is the 4-unit cap + protect-Rapha the real constraint, with levels kept race-appropriate?
- Is it a deliberate 2/5★ exhale after the Velius spike, still showcasing the Assassin caste?
- Does it faithfully close the Riovanes chain and set up the Chapter 4 Elmdor rematch?

## Sources

- Game8, "Riovanes Castle Roof Walkthrough (Battle 32)": roster (Elmdore + Celia + Lettie), objective
  "Save Rapha!", recommended level ~36, 2/5 stars, deploy 4, flee-on-critical (one assassin critical
  -> all three retreat), focus one assassin / ignore Elmdor's debuffs, Marach & Rapha recruited on
  completion, rewards/treasure.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553192
- Final Fantasy Wiki, "Elmdor" / "Celia and Lettie": story + Assassin/Arc-Knight context, Limberry rematch loot.
  https://finalfantasy.fandom.com/wiki/Elmdor
- Local: `docs/battles/024-chapter-3-overview.md` (job-escalation + rare-loot rules; Elmdor deferral),
  `031-walled-city-yardrow.md` & `025-mining-town-gollund.md` (protect-NPC handling),
  `034-riovanes-castle-keep.md` (no-resupply chain; Lucavi status caps), `022-lionel-castle-oratory.md`
  (boss status constraint precedent).
</content>
