# Chapter 2 — "The Manipulator and the Subservient": New Game++ Design Overview

Master plan for rescaling and redesigning every **Chapter 2** story battle of *FINAL FANTASY
TACTICS - The Ivalice Chronicles* (Enhanced v1.5.0) for New Game++.

Chapter 2 is where the mod's ambition steps up. The scaling mechanic and the "preserve each
fight's identity" philosophy from Chapter 1 still apply (see `000-chapter-1-overview.md`), but
two new design goals are layered on top:

```text
1. ENEMY PARTY ESCALATION — start building full enemy parties to raise the challenge, WITHOUT
   breaking each battle's original strategy. One headline demand per fight; the whole enemy side
   may support that demand.
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
| `012` | 11 | Merchant City of Dorter | Mercenary work; "kill them all" | revisit Dorter, rooftop pressure + charm | ✅ v1 implemented; **v2 documented only** |
| `013` | 12 | Araguay Woods | Rescue Boco the chocobo vs Goblins | controlled Boco + faster monster route pressure | ✅ v1 implemented; **v2 documented only** |
| `014` | 13 | Zeirchele Falls | Protect Ovelia; **Gaffgarion betrays** | controlled Ovelia/Agrias + betrayal bridge control | ✅ v1 implemented; **v2 documented only** |
| `015` | 14 | Castled City of Zaland | Save Mustadio from bounty hunters | controlled Mustadio + vertical assassin pressure | ✅ v1 implemented; **v2 documented only** |
| `016` | 15 | Balias Tor | Defeat enemy **Summoners** + support | first Summoner race + sustain screen | ✅ v1 implemented; **v2 documented only** |
| `017` | 16 | Tchigolith Fenlands | Swamp; **undead / dark** enemies | undead attrition + one status monster | ✅ v1 implemented; **v2 documented only** |
| `018` | 17 | Goug Lowtown | Summoners; active guest slot | second Summoner fight + Time-Mage tempo/charm | ✅ v1 implemented; **v2 documented only** |
| `019` | 18 | Balias Swale | Split-team; rain-boosted Thunder | controlled Agrias + route-biased storm cell | ✅ v1 implemented; **v2 documented only** |
| `020` | 19 | Golgollada Gallows | **Gaffgarion** as a major threat | Dark Knight sub-boss (Drain/disarm) | ✅ v1 implemented; **v2 documented only** |
| `021` | 20 | Lionel Castle Gate | Two-part; **Gaffgarion boss** (dies) | boss + Blood Sword rare loot | ✅ v1 implemented; **v2 documented only** |
| `022` | 21 | Lionel Castle Oratory | **Cúchulainn**, first Lucavi demon | solo Lucavi `104`, chain-aware + 108 Gems reward | ✅ v1 implemented; **v2 documented only** |
| `023` | — | Chapter 2 Balance Review | Cross-battle curve + consistency audit | — | ✅ Done (all 11) |

## Carried-over rules (from Chapter 1)

Still in force — see `000-chapter-1-overview.md` for the full text:

```text
- Scale to party: enemy Level = 100 + offset. Offsets stay small; bosses are the spikes.
- Preserve each battle's identity (theme, archetypes, terrain, what it teaches).
- Respect job equipment rules (mages wear robes, monsters wear nothing, etc.).
- Keep the curve readable: one headline demand per fight, with the whole enemy side supporting it.
- Guest-control rule: from Chapter 1 onward, every active guest is player-controlled in NG+,
  whether or not the objective says to save them. Guest AI is not a skill check.
- Document any rule exception per-battle (as we did for Time Mage / equipment-break in Ch1).
```

## NEW rule 1 — Enemy party escalation

Chapter 2 starts evolving the enemy roster into real New Game+ opposition. The goal is **more
challenge through higher-skill party construction**, not bigger numbers alone — and never at the
cost of the fight's original strategy.

```text
HOW TO ESCALATE A FIGHT:
- First diagnose the vanilla spirit: what feeling and difficulty did the original designers want?
  Rooftop pressure, betrayal, crossing a river, undead dread, caster priority, boss duel, etc.
- Any normal job tier is legal starting now — except Mime and Calculator/Arithmetician — if it
  translates that spirit into a harder NG+ version.
  e.g. Dorter's rooftop pressure can become Archer/Gunner/Geomancer/Time-supported ranged control,
       but it must still read as "control the high ground."
- Chapter 2 is the preview chapter for Chapter 3. It may use advanced jobs and extra enemies, but
  it should teach one or two clear knobs rather than become a dense synergy puzzle.
- Every active human enemy gets complete equipment. Reaction/support/movement should also be set
  intentionally. Secondary is allowed but optional: use it when it clarifies the role or previews a
  Chapter 3 system, not as automatic filler.
- The enemy party may add bodies if the map needs action economy, flanks, bodyguards, or route
  pressure. Extra enemies must sharpen the original feeling, not create cleanup.

DO NOT:
- Stack multiple unrelated puzzle engines in one fight.
- Introduce hard lockdown (Stop/Don't Act/Petrify spam) on an endgame party.
- Replace a fight's identity with a different fight.
```

A short **"enemy party escalation"** section in each battle doc states the original battle spirit,
the upgraded party roles, full equipment plan, R/S/M setup, optional secondary choices, which jobs
changed or were added, why any extra enemies exist, and how the original strategy still survives at
a higher difficulty.

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
- If a monster/Lucavi ENTD slot cannot equip the rare, the item moves to a guaranteed reward/table
  path instead of being faked onto the unit.
```

Each battle doc with a boss includes a **"Boss rare loot"** line naming the item, why it fits,
and confirming it is mid-tier (not reserved-for-Ch4).

## Difficulty budget per battle (Chapter 2)

Level bands creep slightly above Chapter 1; bosses are the spikes. Generics `100–102`,
sub-bosses `102–103`, major bosses `103–104`. The solo Lucavi capstone stays at `104`;
its v2 difficulty is validated by testing the Gate -> Oratory no-resupply chain, not by
raising the chapter cap.

| Battle | Target feel | Level band | New wrinkle / boss loot |
|--------|-------------|------------|--------------------------|
| Merchant Dorter (11) | Harder Dorter rematch | 100–102 | tougher mage/archer/thief mix; revisit the rooftops |
| Araguay Woods (12) | Controlled Boco through a pack | 100–101 | monster pack + route pressure |
| Zeirchele Falls (13) | Defend Ovelia; betrayal turn | 100–103 | Agrias ally; Gaffgarion turncoat pressure |
| Zaland (14) | Save Mustadio under fire | 100–102 | controlled Mustadio + vertical/ranged pressure |
| Balias Tor (15) | First Summoner fight | 100–102 | **Summoner** AoE pressure |
| Tchigolith Fenlands (16) | Swamp of the dead | 100–102 | **undead** (reraise) + bog terrain |
| Goug Lowtown (17) | Summoners + active ally slot | 100–102 | Summoner + Time Mage tempo + charm |
| Balias Swale (18) | Split-team in the rain | 100–102 | controlled Agrias + route-biased rain-Thunder |
| Golgollada Gallows (19) | Gaffgarion looms | sub-boss 103, adds 100–102 | Dark Knight sub-boss (Drain) |
| Lionel Gate (20) | Gaffgarion boss, two-part | boss 103, adds 100–102 | **boss + rare loot**; disarm him |
| Lionel Oratory (21) | First Lucavi demon | boss 104 | **Cúchulainn + reward-table rare**; Holy weakness |

## Workflow per battle (same as Chapter 1)

```text
1. Read this overview + the battle doc.
2. On Windows: identify the BattleId / ENTD entry (cross-ref SortieConfirm, EventId, Map,
   scenario tables; sanity-check with FFTIvaliceEditor).
3. Dump the entry; confirm the original roster matches the doc's "Original Battle".
4. Apply the New Game++ composition: levels, ENEMY PARTY ESCALATION, gear, RARE BOSS LOOT,
   skills, placement, and guest-control flags for every active guest.
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
