# 048 - Limberry Castle Keep

Status: designed (not yet implemented)
Chapter: 4 — "In the Name of Love"
Battle order: Battle 43 (Limberry chain 2 of 3 — NO resupply between 42→43→44)
Target version: Enhanced v1.5.0
ENTD: global entry **TBD** — confirm on Windows game data
File: `battle_entd*_ent.bin` (TBD) / `OverrideEntryData` rows (TBD)

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `037-chapter-4-overview.md`. LIMBERRY CHAIN: 42 (`047`) → 43 (`048`) → 44 (`049`), one loadout.

## Original Battle

Objective:

```text
Defeat Elmdore!   (defeating Elmdore ends the battle — he dies here for good)
```

Player deployment:

```text
Up to 5 units, including Ramza. No guests. NO outfitter access (chain 2/3).
```

Original enemy composition (verified via Game8, Battle 43):

```text
Elmdore (Ark Knight)   (BOSS — the objective; Shirahadori parry + Vampire drain + Draw Out/katana)
Celia (Assassin)       (transforms into an ULTIMA DEMON after initial defeat)
Lettie (Assassin)      (transforms into an ULTIMA DEMON after initial defeat)
```

Public walkthrough details:

```text
Recommended level: ~60.  Difficulty: 5/5 stars.  Deploy up to 5.  NO resupply (Limberry chain 2/3).
WIN: "Defeat Elmdore!" — killing ELMDORE ends the fight (the assassins do NOT have to be fully cleared).
ELMDORE — the parry boss: SHIRAHADORI auto-evades physical/normal sword attacks, so plain melee whiffs.
  The walkthrough's tip: "Sword attacks like DIVINE RUINATION ignore Shirahadori" — i.e. MAGIC and
  magic-based sword arts get through; also Vampire DRAIN sustain.
CELIA & LETTIE — they RETURN here (from the Gate, 047) and, after their initial defeat, TRANSFORM into
  ULTIMA DEMONS (the "won't stay down" pressure, with Ultima) — but they are not the win condition.
THE READ: crack Elmdore's parry (magic / Divine-Ruination-type / break it) and BURST HIM before the
  assassins' Ultima + demon-transform grind you down. The fight ends the moment Elmdore falls.
Keep interior terrain. Buried (map) treasure: Muramasa, Vampire Cape, Icebrand, Spellbinder.
```

Design reading:

Limberry Keep is **the Elmdor reckoning** — the Arc Knight who fled Riovanes (Ch3 Roof, `035`) is
killed here for good, and his iconic loot finally pays out. Its identity is a **parry-puzzle boss
race**: Elmdore's **Shirahadori** turns plain melee into a whiff, so the player must answer with magic
or magic-based sword arts (Divine Ruination) and burst him — *while* Celia & Lettie return and
transform into **Ultima Demons** that won't stay down and threaten Ultima. Because the win is *defeat
Elmdore*, it rewards cracking the parry and focusing the boss over chasing the resurrecting assassins.
It is the centerpiece of the Limberry gauntlet and the home of the long-deferred **Masamune + Genji**.

For New Game++ the identity must stay: **a 5★ parry-puzzle boss race — beat Elmdore's Shirahadori with
magic/magic-sword-arts and burst him to win — under the pressure of two assassins who transform into
Ultima Demons; on no resupply; and the long-deferred Masamune + Genji finally drop here.**

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm slots: Elmdore (Ark Knight) + Celia + Lettie (Assassins, demon-transform), plus player slots.
  NO outfitter (chain 2/3).
Keep the win condition = "Defeat Elmdore" (his death ends the fight) and the keep-interior geometry.
Keep Elmdore's SHIRAHADORI (physical-parry) + Vampire drain + katana Draw Out; keep the assassins'
  Ultima-Demon TRANSFORM-after-defeat (the 2-phase "won't stay down" pressure).
This is a Tier-A BOSS fight + chain 2/3: Elmdore 104, assassins 104 → demon form 105. Two Tier-A items
  on Elmdore (the deferred Masamune + a Genji piece).
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
Leave the buried map treasure (Muramasa, Vampire Cape, etc.) as-is — map loot, not boss loot.
```

Job IDs (carry over known, verify the rest in-game):

```text
Ark Knight id          (TBD - verify; Elmdore's boss job)
Assassin id            (TBD - verify; Celia/Lettie — 035/047)
Ultima Demon id        (TBD - verify; the assassins' transformed form)
```

## Job Escalation (Chapter 4 rule)

```text
CHANGE: NO new generic caste. The escalation is the BOSS KIT — Elmdore's SHIRAHADORI parry is the new
  demand (plain melee whiffs; you must use magic / magic-based sword arts / break it), and the two
  assassins' demon-TRANSFORM is the 2-phase pressure. These are the established Limberry foes delivered
  at full, lethal endgame power.
WHY: the fight's identity is already "crack the parry boss and burst him while the assassins harass."
  The faithful Ch4 escalation is the parry puzzle + the demon transform — NOT bolting on a third
  mechanic. The Shirahadori read IS the one new demand vs the Gate's (047) flee-race.
CONSTRAINTS (carried): Shirahadori is a PARRY with a clear counter (magic / Divine-Ruination-type /
  break) — telegraphed, NOT a hard lock (he is killable). Ultima = ONE telegraphed, spaceable AoE per
  demon (boss mass-AoE cap). Assassin status resistable + non-spam (035/047). Vampire drain = self-
  sustain answered by burst, not a lock.
WHAT IS NOT CHANGED: the "defeat Elmdore to win" shape, the assassins' return/transform, and the keep
  interior remain.
```

## Sanctioned exceptions (carried precedents)

```text
SHIRAHADORI (physical parry, Elmdore) — allowed as his signature: plain melee/normal sword attacks
  auto-evade. COUNTER: magic, magic-based sword arts (Divine Ruination/Holy Sword spell-hits), or
  breaking the reaction. Telegraphed, killable — NOT a hard lock. The puzzle, not a wall.
VAMPIRE DRAIN (Elmdore) — boss self-sustain; answered by bursting him / denying hits. Not a lock.
ULTIMA-DEMON TRANSFORM (Celia/Lettie) — the 2-phase "won't stay down" pressure; Ultima = ONE
  telegraphed, spaceable AoE per demon (boss mass-AoE cap). Not the win condition (Elmdore is).
ASSASSIN STATUS — resistable + non-spam (035/047 precedent); no hard lock.
```

## Boss rare loot

```text
ELMDORE (boss, DIES here) drops/carries the long-DEFERRED Tier-A loot: MASAMUNE (katana) + GENJI ARMOR
  (a Genji-set piece).
WHY IT FITS: Elmdore is the iconic wielder of the Masamune and wearer of Genji gear; this is the payout
  the Ch3 Roof (035) explicitly DEFERRED (he fled there → no drop). Both are top-tier UNIQUES — a clear
  best-non-ultimate prize — paid where he finally dies.
TIER: A (mid-Chapter-4 best non-ultimate). NOT Tier-S: the absolute best (Ragnarok/Chaos Blade/Ribbon/
  Robe of Lords/Escutcheon/Materia Blade) stays on the endgame sequence (47-53). Masamune is iconic but
  not the single best weapon; Genji ARMOR (not the full set) keeps it Tier-A.
STEAL NOTE: Elmdore's Shirahadori complicates a physical Steal — the player may need to break the parry
  or use a non-physical steal; the DROP pays on his death regardless. Celia/Lettie do NOT drop (their
  reckoning is the transform, not a death-loot — consistent with the assassins' flee/transform handling).
```

## Proposed Composition (New Game++ Limberry Keep v1)

Keep the 3-foe boss-race shape; deliver Elmdore's parry kit + the assassins' demon transform at full
5★ power. Elmdore `104`; assassins `104` → Ultima-Demon `105`. No resupply (chain 2/3) — tune lethality
to one loadout.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Elmdore (BOSS) | Ark Knight | `104` | Shirahadori parry + Vampire drain + katana; the objective; Masamune + Genji Armor. |
| n | Celia | Assassin → Ultima Demon | `104` → `105` | Returns; transforms after defeat; Ultima pressure. |
| n | Lettie | Assassin → Ultima Demon | `104` → `105` | Second assassin/demon; the "won't stay down" grind. |

Reasoning:

The faithful move is to **make Elmdore's parry the puzzle and the assassins the timer**. Elmdore at
`104` with Shirahadori forces the player off plain melee and onto magic / Divine-Ruination-type arts to
land damage, then burst him to win; his Vampire drain rewards quick kills. Celia & Lettie return and
transform into Ultima Demons (`105`) — the "they keep coming back, and now they nuke" pressure — but
since the win is Elmdore, the smart line ignores/CCs them and focuses the boss. No resupply means
lethality is tuned to one loadout (no guaranteed-kill combo; Ultima telegraphed). Elmdore's death pays
the deferred Masamune + Genji Armor (Tier-A).

## Builds (Chapter-4 boss quality; Arc-Knight + demon flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Elmdore (Lv 104) — BOSS (Ark Knight)

```text
Job: Ark Knight (id TBD)   JobLevel: 8   Primary: Draw Out (katana spirits) + melee; Vampire drain
Reaction: SHIRAHADORI (physical-parry, id TBD)   Support: Attack Boost (465) / MA-boost
  Movement: Teleport (id TBD) or Movement +2 (487)
Head: Genji Helm-equivalent / Tier-A (id TBD)   Body: GENJI ARMOR (Tier-A, id TBD)
Accessory: Tier-A accessory (id TBD)   Right hand: MASAMUNE (Tier-A katana, id TBD)   Left: none (255)
```

Role: the parry-puzzle objective — beat Shirahadori with magic/Divine-Ruination, deny his drain, burst
him to win. His death drops Masamune + Genji Armor. Keep Shirahadori a counterable parry, not a lock.

### Celia & Lettie (Lv 104 → Ultima Demon 105)

```text
Job: Assassin (id TBD) → Ultima Demon (id TBD)   JobLevel: 8
Phase 1 (Assassin): teleport killer; resistable, non-spam status.
Phase 2 (Ultima Demon, after initial defeat): demon kit + ULTIMA (one telegraphed, spaceable AoE).
Reaction: (mobility) Reflexes / First Strike   Movement: Teleport / Movement +2 (487)
```

Role: the timer/pressure — they return and transform; threaten Ultima — but are not the win condition.
Keep Ultima telegraphed and status resistable; do not let them hard-lock the party.

## Positioning Plan

```text
Keep interior: Elmdore starts central/back (parry boss the player must reach and crack), the two
  assassins flanking with teleport range onto the back-line. Keep sightlines so Ultima (once they
  transform) is a telegraphed, spaceable threat — not an ambush nuke.
Preserve the "defeat Elmdore = win" trigger, his Shirahadori parry, and the assassins' demon transform.
Tune for NO resupply: survivable on one loadout; parry has a clear magic counter; Ultima spaceable;
  status resistable.
```

The keep should say: "the immortal lord parries every blade — strike him with spell and sword-light,
and cut him down before his knife-women rise as demons."

## Implementation Checklist

- [ ] Identify Limberry Keep `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify Elmdore + Celia + Lettie (+ transform) + player slots.
- [ ] Keep win = "Defeat Elmdore" (his death ends it); keep the keep-interior geometry.
- [ ] Set Elmdore `104` with Shirahadori (counterable parry) + Vampire drain + katana Draw Out.
- [ ] Equip Elmdore with MASAMUNE + GENJI ARMOR (Tier-A) as his death drop; note Shirahadori complicates Steal.
- [ ] Keep assassins `104` → Ultima-Demon `105` transform; Ultima telegraphed/spaceable; status resistable.
- [ ] Tune lethality to ONE loadout (chain 2/3, no resupply); no guaranteed-kill combo.
- [ ] Set JobLevel `8` on boss/assassin slots.
- [ ] Patch via the correct layer; keep the diff inside the Limberry Keep window only.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify parry counter + win-cond + drop.
- [ ] Install mod, test from a New Game+ save (chain-realistic resources); confirm the parry has a
      working magic counter, Elmdore is killable, Ultima is spaceable, and Masamune+Genji drop.

## Test Questions

- Is Shirahadori a fair PUZZLE (magic / Divine-Ruination / break it answers it) and NOT a hard lock —
  is Elmdore reliably killable by a prepared party?
- Does "Defeat Elmdore ends the fight" keep it a focus race over chasing the resurrecting assassins?
- Do Celia & Lettie transform into Ultima Demons as pressure, with Ultima telegraphed/spaceable and
  status resistable (no hard lock)?
- Do the deferred MASAMUNE + GENJI ARMOR (Tier-A) drop on Elmdore's death — and is that NOT Tier-S?
- Is the fight survivable on ONE loadout (no resupply, chain 2/3)?
- Does it read as the long-awaited reckoning of Elmdore, the heart of the Limberry gauntlet?

## Sources

- Game8, "Limberry Castle Keep Walkthrough (Battle 43)": roster (Elmdore Ark Knight + Celia + Lettie,
  assassins transform into Ultima Demons), objective "Defeat Elmdore!", rec ~60, 5/5 stars, deploy 5,
  Shirahadori parry (Divine Ruination ignores it) + Vampire drain, no resupply (Limberry chain), buried
  treasure (Muramasa, Vampire Cape, Icebrand, Spellbinder).
  https://game8.co/games/Final-Fantasy-Tactics/archives/553203
- Final Fantasy Wiki, "Elmdor" / "Limberry Castle": story/terrain context.
  https://finalfantasy.fandom.com/wiki/Elmdor
- Local: `037-chapter-4-overview.md` (rules + Elmdor deferral), `035-riovanes-castle-roof.md` (Ch3 Roof —
  where Elmdor fled and the Masamune/Genji were deferred), `047-limberry-gate.md` (chain 1/3 — the
  assassins' first appearance), `049-limberry-undercroft.md` (chain 3/3 — to be designed).
```
</content>
