# Chapter 2 — "The Manipulator and the Subservient": New Game++ Design Overview

Master plan for rescaling and redesigning every **Chapter 2** story battle of *FINAL FANTASY
TACTICS - The Ivalice Chronicles* (Enhanced v1.5.0) for New Game++.

Chapter 2 is where the mod's ambition steps up. The scaling mechanic and the "preserve each
fight's identity" philosophy from Chapter 1 still apply (see `000-chapter-1-overview.md`), but
two new design goals are layered on top:

```text
1. JOB ESCALATION — start adding or swapping enemy jobs to raise the challenge, WITHOUT
   breaking each battle's original strategy. One new wrinkle per fight, not a redesign.
2. RARE BOSS LOOT — important (boss) battles equip the boss with a RARE, non-buyable item as
   a signature reward/threat. NOT best-in-slot: the very best gear is reserved for Chapter 4.
```

## Story framing (why the difficulty rises)

After Ziekden, Delita is gone and time has passed. Ramza is now a **sellsword** working
alongside the Dark Knight **Gaffgarion** under the Order, drawn into the plot around Princess
**Ovelia**. Over the chapter he gains **Agrias** and **Mustadio** as allies, is betrayed by
Gaffgarion, and finally faces the first **Lucavi demon, Cúchulainn**. The enemies stop being
ragged deserters and become professional knights, hired assassins, **Summoners**, the undead,
a Dark Knight, and a Zodiac demon. The curve should reflect that: Chapter 2 is meaningfully
harder than Chapter 1, with real magic, real bosses, and the first non-human horror.

## Chapter 2 battle list

"Battle N" follows in-game/Game8 numbering. Doc numbers continue the flat sequence from
Chapter 1 (doc `001` = Battle 2, so the offset is the same established pattern: doc = battle + 1).

| Doc | Battle | Location | Role in story | New element | Status |
|-----|--------|----------|---------------|-------------|--------|
| `012` | 11 | Merchant City of Dorter | Mercenary work; "kill them all" | revisit Dorter, tougher mix | ✅ Implemented (v1, entry 403; Knight add deferred) |
| `013` | 12 | Araguay Woods | Rescue Boco the chocobo vs Goblins | escort + monster pack | ✅ Implemented (v1, entry 404; Panther add + Boco scaling deferred) |
| `014` | 13 | Zeirchele Falls | Protect Ovelia; **Gaffgarion betrays** | Agrias ally; Gaffgarion turns | ✅ Implemented (v1, entry 405; Knight→Archer swap inline) |
| `015` | 14 | Castled City of Zaland | Save Mustadio from bounty hunters | ranged/urban + Dragoon (vertical) | ✅ Implemented (v1, entry 407; Knight→Dragoon inline; Mustadio auto-scaled) |
| `016` | 15 | Balias Tor | Defeat enemy **Summoners** + support | **Summoner** (new job) | ✅ Implemented (v1, entry 409; Summoner = built-in escalation) |
| `017` | 16 | Tchigolith Fenlands | Swamp; **undead / dark** enemies | undead + swamp terrain | ✅ Implemented (v1, entry 410; undead = built-in escalation) |
| `018` | 17 | Goug Lowtown | Summoners; Mustadio guest | Summoner + Time-Mage tempo | ✅ Implemented (v1, entry 411; Thief→Time Mage inline) |
| `019` | 18 | Balias Swale | Split-team; rain-boosted Thunder | split + weather + Geomancer | ✅ Implemented (v1, entry 413; Geomancer add deferred; Agrias auto-scaled) |
| `020` | 19 | Golgollada Gallows | **Gaffgarion** as a major threat | Dark Knight sub-boss (Drain/disarm) | ✅ Implemented (v1, entry 414; Gaffgarion sub-boss L103) |
| `021` | 20 | Lionel Castle Gate | Two-part; **Gaffgarion boss** (dies) | boss + rare loot (Blood Sword) | ✅ Implemented (v1, entry 415; first rare boss loot) |
| `022` | 21 | Lionel Castle Oratory | **Cúchulainn**, first Lucavi demon | demon boss + rare loot (108 Gems) | ✅ Implemented (v1, entry 425; L104, rare loot deferred) |
| `023` | — | Chapter 2 Balance Review | Cross-battle curve + consistency audit | — | ✅ Done (all 11) |

## Carried-over rules (from Chapter 1)

Still in force — see `000-chapter-1-overview.md` for the full text:

```text
- Scale to party: enemy Level = 100 + offset. Offsets stay small; bosses are the spikes.
- Preserve each battle's identity (theme, archetypes, terrain, what it teaches).
- Respect job equipment rules (mages wear robes, monsters wear nothing, etc.).
- Keep the curve readable: at most ONE new meaningful demand per fight.
- Document any rule exception per-battle (as we did for Time Mage / equipment-break in Ch1).
```

## NEW rule 1 — Job escalation

Chapter 2 starts evolving the enemy roster. The goal is **more challenge through variety**,
not through bigger numbers — and never at the cost of the fight's original strategy.

```text
HOW TO ESCALATE A FIGHT:
- Upgrade or swap at most 1-2 generic slots to a more advanced / more thematic job that
  INTENSIFIES the existing challenge.
  e.g. Dorter's rooftop pressure -> swap one Archer for a Geomancer or add an Oracle for a new
       ranged/utility angle, but keep "control the high ground" as the core read.
- Prefer jobs the chapter canonically introduces: Summoner (Balias Tor, Goug), undead
  (Tchigolith), Dark Knight (Gaffgarion), plus order-knights, Geomancer, Oracle, Dragoon.
- The new job must ADD a wrinkle to the existing plan, not force a different plan. If the
  original fight was "kill the healers first," the escalated fight is still "kill the healers
  first, but now one of them also Hastes" — the strategy survives, the execution gets harder.

DO NOT:
- Stack multiple brand-new mechanics in one fight (one new wrinkle at a time).
- Introduce hard lockdown (Stop/Don't Act/Petrify spam) on an endgame party.
- Replace a fight's identity with a different fight.
```

A short **"job escalation"** section in each battle doc states exactly which slot(s) changed
job and why, and confirms the original strategy still holds.

## NEW rule 2 — Rare, non-buyable boss loot (the reward escalation)

Chapter 1 bosses used strong but non-unique shop gear. Starting in Chapter 2, **bosses in
important (boss) battles carry one RARE, non-buyable item** — the kind obtained in vanilla via
steal / poach / rare drop / treasure — as a signature piece. This makes the bosses feel
special and seeds the loot-progression arc. **But not best-in-slot.** The very best equipment
(Excalibur, Ragnarok, Chaos Blade, Masamune, Genji set, Save the Queen, etc.) is held back for
**Chapter 4**.

```text
CHAPTER 2 RARE-LOOT TIER (examples — verify exact ids/availability in ItemData.xml):
  Weapons:    Blood Sword, Mythril/Platinum-tier swords, a non-best katana, Hidden Knife,
              Mage Masher, a mid-tier bow/gun above shop level.
  Armor:      Platinum-tier armor, a non-best robe (e.g. Wizard/Silk-tier above shop),
              a rare hat above shop level.
  Accessory:  Sprint Shoes, 108 Gems, Defense Ring, Magic Ring, Feather Boots, Cursed Ring
              (flavor), or a rare cloak above shop tier.

RESERVED FOR CHAPTER 4 (do NOT use in Ch2):
  Excalibur, Ragnarok, Chaos Blade, Masamune, Materia/Mythril-best, Genji set, Save the Queen,
  Escutcheon II / best shields, Ribbon, best robes. These are the "best" gear.

RULE OF THUMB:
- Each boss battle's boss gets ONE rare item as its highlight (occasionally a sub-boss gets one
  too if the fight has two notable foes). Generics stay on shop-tier gear.
- The rare item should fit the boss's identity AND be a real in-fight threat or a tempting
  steal target — not just a trophy.
```

Each battle doc with a boss includes a **"Boss rare loot"** line naming the item, why it fits,
and confirming it is mid-tier (not reserved-for-Ch4).

## Difficulty budget per battle (Chapter 2)

Level bands creep slightly above Chapter 1; bosses are the spikes. Generics `100–102`,
sub-bosses `102–103`, major bosses `103–104`.

| Battle | Target feel | Level band | New wrinkle / boss loot |
|--------|-------------|------------|--------------------------|
| Merchant Dorter (11) | Harder Dorter rematch | 100–102 | tougher mage/archer/thief mix; revisit the rooftops |
| Araguay Woods (12) | Escort a chocobo through a pack | 100–101 | monster pack + protect Boco |
| Zeirchele Falls (13) | Defend Ovelia; betrayal turn | 100–103 | Agrias ally; Gaffgarion turncoat pressure |
| Zaland (14) | Save Mustadio under fire | 100–102 | urban assassins; ranged escort |
| Balias Tor (15) | First Summoner fight | 100–102 | **Summoner** AoE pressure |
| Tchigolith Fenlands (16) | Swamp of the dead | 100–102 | **undead** (reraise) + bog terrain |
| Goug Lowtown (17) | Summoners + guest escort | 100–102 | Summoner + protect Mustadio |
| Balias Swale (18) | Split-team in the rain | 100–102 | split + rain-Thunder synergy |
| Golgollada Gallows (19) | Gaffgarion looms | sub-boss 103, adds 100–102 | Dark Knight sub-boss (Drain) |
| Lionel Gate (20) | Gaffgarion boss, two-part | boss 103, adds 100–102 | **boss + rare loot**; disarm him |
| Lionel Oratory (21) | First Lucavi demon | boss 104, adds 100–103 | **Cúchulainn + rare loot**; Holy weakness |

## Workflow per battle (same as Chapter 1)

```text
1. Read this overview + the battle doc.
2. On Windows: identify the BattleId / ENTD entry (cross-ref SortieConfirm, EventId, Map,
   scenario tables; sanity-check with FFTIvaliceEditor).
3. Dump the entry; confirm the original roster matches the doc's "Original Battle".
4. Apply the New Game++ composition: levels, JOB ESCALATION swaps, gear, RARE BOSS LOOT,
   skills, placement.
5. Patch via the right layer (.bin or OverrideEntryData); keep the diff inside the battle window.
6. Copy into the mod, install to Reloaded-II, test from a New Game+ save.
7. Record results back in the battle doc.
```

## Sources

- Game8, "Chapter 2: The Manipulator and the Subservient Walkthrough":
  https://game8.co/games/Final-Fantasy-Tactics/archives/543020
- Game8 per-battle walkthroughs (rosters) — linked in each battle doc.
- Local: `000-chapter-1-overview.md` (carried-over rules), `010-chapter-1-balance-review.md`
  (the boss-loot escalation was seeded there: Ch1 bosses non-unique, Ch2 begins rare items).
</content>
