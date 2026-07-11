# Chapter 4 — "In the Name of Love": New Game++ Design Overview

Master plan for rescaling and redesigning every **Chapter 4** story battle of *FINAL FANTASY
TACTICS - The Ivalice Chronicles* (Enhanced v1.5.0) for New Game++.

Chapter 4 is the **endgame**: the Church's conspiracy is laid bare, the Lucavi reveal themselves one
after another (Zalera, Adramelk, Hashmal), Ramza's own brothers fall, and the campaign closes in the
buried ruins beneath Mullonde against the resurrected Ultima. The scaling mechanic and the "preserve
each fight's identity" philosophy still apply (see `000`, `011`, `024`), and the two recurring design
goals continue — now at their **final escalation**:

```text
1. JOB ESCALATION — keep adding/swapping enemy jobs to raise the challenge WITHOUT breaking each
   battle's original strategy. Chapter 4 fields the game's top castes: enemy SAMURAI (Draw Out),
   the ULTIMA/ARCHAEO DEMONS (elite Lucavi minions), the multi-head DRAGONS (Hydra/Tiamat), and the
   remaining LUCAVI themselves (Zalera, Adramelk, Hashmal, and Ultima). It is the finale, so a fight
   is allowed its boss-spike - but still ONE headline demand per battle.
2. RARE / NON-BUYABLE GEAR — this is the chapter where the RESERVED best-in-slot gear finally unlocks.
   Bosses still carry the named Tier-A/Tier-S highlights, but Chapter 4 normal enemies may also carry
   role-fitting non-buyable gear as part of broken puzzle-party builds. The absolute best-of-the-best
   is paid by the end of the Mullonde chain, before the no-resupply final gauntlet.
```

## Story framing (why this is the final climb)

After Riovanes, Ramza is a hunted heretic chasing the Lucavi to their source. He duels **Meliadoul**
(who learns the truth), crosses the war-torn south (**Bervenia**, **Finath**, **Bed Desert**,
**Bethla**'s floodgate), purges the undead of **Poeskas Lake**, and storms **Limberry** where
**Elmdor** and his assassins are revealed as demons (**Zalera**). He returns home to **Eagrose/Igros**
to face his brother **Dycedarg** (**Adramelk**), then descends into **Mullonde Cathedral** where
**Folmarv** becomes **Hashmal** and the dead **Zalbaag** is turned against him. The final five-battle
gauntlet beneath Mullonde ends at the **Airship Graveyard**, where **Ultima** rises. Enemies are at
their absolute peak — Lucavi, Ultima Demons, Samurai, dragons — and the chapter must feel like the
hardest, most climactic content in the mod, capped by the two-phase final battle.

## Chapter 4 battle list

"Battle N" follows in-game/Game8 numbering. Doc numbers continue the flat sequence (Chapter 3 ended
at `036`; this overview is `037`, so Battle 33 = doc `038`, i.e. **doc = battle + 5**). Classic
(War of the Lions) names given for cross-reference.

| Doc | Battle | Location (TIC / classic) | Role in story | New element | Status |
|-----|--------|---------------------------|---------------|-------------|--------|
| `038` | 33 | Dugeura Pass / Doguola Pass | Open-field opener | Black Mage AoE priority + Dragoon Jump; Haste tempo | ✅ Done |
| `039` | 34 | Free City of Bervenia | **Meliadoul** (Templar); ends when she falls | full Templar break-duel; **Save the Queen** (Tier A) | ✅ Done |
| `040` | 35 | Finnath Creek / Finath River | Wild chocobo field; Pig recruit | de-randomized chocobo tempo (Choco Cure/Meteor); no rare | ✅ Done |
| `041` | 36 | Outlying Church / Zeltennia Church | **Zalmo** rematch — DIES here | elevated holy-boss burst-duel; **Light Robe** (Tier A); deferred rare paid | ✅ Done |
| `042` | 37 | Beddha Sandwaste / Bed Desert | **Barich** (Templar gunner) — dies here | open-desert gun-duel; **Glacial Gun** steal (Tier A); no Hydra (that's `057`) | ✅ Done |
| `043a` | 38A | Fort Besselat South Wall / Bethla | Wall assault (South path) | melee/stealth vertical wall; route-parity Yoichi/Perseus reward | ✅ Done |
| `043b` | 38B | Fort Besselat North Wall / Bethla | Wall assault (North path) | ranged/AoE vertical wall; route-parity Yoichi/Perseus reward | ✅ Done |
| `044` | 39 | Fort Besselat Sluice / Bethla Sluice | The floodgate; pull levers (open the gate) | v3 kits approved; six enemies retuned to 100, lever Knights stay 102 | 🧪 Retest |
| `045` | 40 | Mount Germinas / Germinas Peak | Climb; buried Invisibility Cloak | 4/5★ v3: 2 Ninja + 2 Thief + 2 Archer; playtest pending | 🧪 Test |
| `046` | 41 | Lake Poescas / Poeskas Lake | All-undead lake (5★) | v3 complete undead shell; Mystic/Summoner anchors; playtest pending | 🧪 Test |
| `047` | 42 | Limberry Castle Gate | **Celia & Lettie** (Assassins; flee on critical) | v3 dual-blade flee-race; band 100-102; playtest pending | 🧪 Test |
| `048` | 43 | Limberry Castle Keep | **Elmdor** (dies); Celia/Lettie → Ultima Demons | v3 Chirijiraden boss + armed Assassins; band 100-102; playtest pending | 🧪 Test |
| `049` | 44 | Limberry Undercroft | **Zalera** + 2 Archaeodaemon + Undead Mystic + 2 Undead Knights | v3 implemented; six enemies; band 100-102; playtest pending | 🧪 Test |
| `050` | 45 | Eagrose Castle / Igros Castle | **Dycedarg → Adrammelech** (Lucavi) | v3 implemented/deployed: 2 Martial Knights + Samurai Knight + 2 Javelin "II" Dragoons | 🧪 Test |
| `051` | 46 | Mullonde Cathedral / Murond | Exterior; 2 Geomancer/2 Orator/Summoner + hidden roof W.Mage | v3 implemented/deployed: gender recast + protected healer + Rod-of-Faith Summoner + Stoneshooter Orators | 🧪 Test |
| `052` | 47 | Mullonde Nave | **Folmarv/Loffrey/Cletienne** (ends when ONE falls; others retreat) | v3 implemented/deployed: boss equipment refresh; chain 2/3; **Tier-S Chaos Blade + Escutcheon + Lordly Robe** unchanged | 🧪 Test |
| `053` | 48 | Mullonde Sanctuary | **Zalbaag** (vampire Ark Knight) + 2 Archaeodaemon + Ultima Demon | v3 implemented/deployed: Eagrose guest loadout; chain 3/3; **Tier-S Ragnarok + Ribbon** unchanged | 🧪 Test |
| `054` | 49 | Monastery Vaults 4th Floor | ENDGAME 1/5; 2 Eagrose Knight Martial Artists + Eagrose Knight Samurai + 2 South Wall Monks + South Wall Ninja | v3 implemented/deployed; Loffrey exits; no reward | 🧪 Test |
| `055` | 50 | Monastery Vaults 5th Floor | ENDGAME 2/5; **Loffrey** + 2 female Black Mage/2 female Summoner/female Time Mage | v3 implemented/deployed; Zeus Mace equipped; Loffrey objective | 🧪 Test |
| `056` | 51 | Necrohol of Mullonde | ENDGAME 3/5; **Cletienne** (Magick Surge) + 2 Samurai/2 Ninja/2 Time Mage | **Samurai** endgame showcase; Silence/burst-the-surge race; win-when-Cletienne-falls; no usable gauntlet reward | ✅ Done |
| `057` | 52 | Lost Halidom / Lost Sacred Precincts | ENDGAME 4/5 (**5★ peak**); **Barich** rematch + Chemist + 4 apex monsters | overlapping breath lanes + Disable/Immobilize control; win-when-Barich-falls; no usable gauntlet reward | ✅ Done |
| `058` | 53 | Airship Graveyard | ENDGAME 5/5; **Hashmal -> Ultima** (FINAL, L106) + Ultima Demons | two-phase Lucavi finale; full restore between; Dispelja/Almagest + 2nd form; no usable gauntlet reward | ✅ Done |
| `059` | — | Chapter 4 Balance Review | Cross-battle curve + consistency audit | — | ✅ Done |

## Carried-over rules (from Chapters 1–3)

Still in force — see `000`, `011`, `024` for full text:

```text
- Scale to party: enemy Level = 100 + offset. Offsets stay small; bosses are the spikes.
- Preserve each battle's identity (theme, archetypes, terrain, what it teaches).
- Respect job equipment rules (mages wear robes, monsters wear nothing, etc.).
- Keep the curve readable: at most ONE new meaningful demand per fight (the finale earns its
  boss-spikes, but never stacks two brand-new player-facing mechanics in one battle).
- Guest-control rule: from Chapter 1 onward, every active guest is player-controlled in NG+,
  whether or not the objective says to save them. Guest AI is not a skill check.
- Document any rule exception per-battle (Time Mage control, equipment-break, boss self-heal,
  boss mass-status, undead reraise, instant-death, Lucavi AoE — see the Ch3 exception log in `036`).
- Retreat/flee/survive boss = NO rare drop (the drop is paid where the boss dies for good).
```

## NEW rule 1 — Job escalation (Chapter 4 castes)

The roster reaches its ceiling. The goal is unchanged: **more challenge through variety**, never at
the cost of the fight's original strategy.

```text
CHAPTER 4 CASTES / FOES TO DEPLOY (canon castes are texture, not a job-tier limit):
- Samurai (enemy)   : Draw Out (katana spirits) — AoE elemental/heal/buff from the blade. Previewed
                      at the Besselat Sluice and showcased at the Necrohol (Cletienne's guard). Treat
                      Draw Out like a telegraphed AoE: strong, spaceable, not a lock.
- Ultima/Archaeo    : elite demon minions flanking the Lucavi and the named demons (Elmdor, the
  Demons               assassins, Zalbaag's guard, the final fight). High stats; the "generic" of the
                      endgame. Used as the level-103-class body around the boss spikes.
- Dragons (Hydra/   : multi-head/breath monsters (Bed Desert, Lost Halidom). Big HP, line/cone breath.
  Tiamat)              Vertical/positional threat; the monster-tier capstone.
- The LUCAVI        : Zalera (Limberry), Adramelk (Eagrose), Hashmal (Airship P1), and ULTIMA (final).
                      Each is a sanctioned boss-spike with ONE telegraphed mass effect + counters.
- Elite Templar     : Meliadoul (Mighty Sword break), Barich (machinist + dragon), Loffrey (summoner),
  named bosses         Cletienne (summoner + Samurai). Full kits; the human bosses of the finale.

RULE: Chapter 4 may tune the whole enemy team into a synergistic broken puzzle, not just upgrade 1-2
slots. Keep one headline engine per battle, then let the surrounding generics amplify that engine with
complete kits, role-fitting non-buyable gear, and readable support roles. Never stack two unrelated
player-facing puzzle engines on one map, and never introduce hard lockdown (Stop/Don't Act/Petrify
spam) on the endgame party.
```

A short **"Enemy party escalation"** section in each battle doc states the vanilla battle spirit, the
headline puzzle engine, the supporting party roles, any non-buyable gear on normal enemies, and why
the original strategy still holds at Chapter 4 intensity.

## NEW rule 2 — Best-in-slot boss loot (the Chapter 4 tier), with the best held for last

> **Superseded for the endgame gauntlet (2026-06-27):** "hold the best for last" does NOT mean inside the
> 5-battle no-resupply gauntlet (054-058). Rewards placed there can never be equipped (no shop/save between
> fights), and final-boss loot drops after the game ends. All best-in-game gear is now paid by the end of
> the **Mullonde chain (051-053)**, the last save before the point of no return. This also bends the carried
> "retreat/survive = no drop" rule for Loffrey/Cletienne (they pay at Nave via kill-independent spoils).
> Canonical record: `chapter-4-rewards-implementation.md`.

Chapters 2–3 paid out low- then mid-high rares. Chapter 4 finally unlocks the **reserved best-in-slot
gear** — but tiered so the campaign's power curve still peaks at the very end.

```text
NOW UNLOCKED (the game's best uniques) — assign by tier:

  TIER A — best NON-ultimate uniques  → mid-Chapter-4 bosses (Bervenia, Bed Desert, Limberry, Eagrose):
    Save the Queen (knight sword), Masamune (katana), the Genji set (helm/armor/shield/gloves),
    Excalibur (Holy + auto-Float), Defense-tier accessories (Cursed/Angel Ring, 108 Gems already used),
    Aegis Shield, best robes below Lordly Robe, Grand Helm/Crystal-tier armor.

  TIER S — the BEST OF THE BEST  -> paid before the no-resupply final gauntlet, concentrated in the
    Mullonde sequence:
    Chaos Blade (best knight sword), Ribbon (ultimate status protection), Ragnarok (best sword),
    Lordly Robe (best robe), and Escutcheon (best shield). Materia Blade remains outside this
    gauntlet reward plan as a side/Move-Find pickup, not a 057 battle reward.

ASSIGNMENT RULES:
  - A boss that FLEES/SURVIVES still drops nothing unless a documented guaranteed-spoils layer pays the
    item before a point of no return.
  - Each reward-bearing boss battle gives a named highlight; this is no longer exclusive. Chapter 4 normal enemies
    may also carry role-fitting non-buyable gear when it supports a readable broken-party puzzle.
  - Any normal-enemy non-buyable gear must be documented per battle as steal-bait, role identity,
    or puzzle pressure. Do not hide essential rewards on throwaway generics without intent.
  - The rare fits the boss's identity AND is a real in-fight threat or a tempting steal.
  - Elmdor's iconic MASAMUNE + GENJI (deferred from Riovanes in Ch3) are paid HERE, at Limberry Keep
    (043), where he is decisively defeated — Tier A, not the absolute capstone.
  - No usable reward is placed inside the final no-resupply gauntlet (`054`-`058`). Final-boss loot is
    dead loot after the campaign ends, and mid-gauntlet loot cannot be equipped before the next fight.
```

Each boss battle doc includes a **"Rare/reward handling"** line naming the item policy, its tier when
applicable, and whether the battle is reward-bearing or challenge-only.

## Brave/Faith tuning policy (Chapter 4)

Brave/Faith is an explicit Chapter-4 puzzle lever. Battle docs use a `Br/Fa` column for fixed enemy and
active guest/story slots. These are target ENTD values for Bravery (`0x06`) and Faith (`0x07`) during
implementation. Player-deployed units are not fixed by the encounter doc because their Brave/Faith are
part of the player's build.

Chapter 4 may use high Brave/Faith, but the values must still explain the battle's readable answer:

| Archetype | Target Br/Fa | Why |
|-----------|--------------|-----|
| Knights / Templars / physical bosses | `88-90/42-60` | High-Brave reactions and physical pressure; Faith stays moderate unless magic vulnerability is intended. |
| Ninjas / Thieves / Assassins | `88-90/35-60` | Fast, high-Brave killers; Faith depends on whether magic is meant to be a primary answer. |
| Black Mage / Summoner / Time Mage | `60-62/80-84` | Endgame magic must matter, and high Faith keeps caster priority fair both ways. |
| Mystic / Orator / support casters | `68/78` | Soft control works but should remain resistable/cleansable. |
| Samurai | `88/60` | Strong physical/reaction profile with enough Faith for Iaido/magic-adjacent pressure when relevant. |
| Undead / demons / Lucavi | `86-92/35-90` | Undead keep low Faith; Lucavi/finale units get high Faith to make Holy/status/magic answers meaningful. |
| Apex monsters / beasts | `90/30` | High-Brave monster pressure; low Faith keeps monster fights about innate breath, positioning, and disable answers. |
| Script placeholders | `preserve` | Do not assign active Brave/Faith unless implementation proves the record fights. |

## Difficulty budget per battle (Chapter 4)

Bands reach their ceiling; the Lucavi and the final demon are the spikes. Generics `100–103`,
Ultima-Demon bodies `103`, sub-bosses `103–104`, human bosses `104–105`, Lucavi `105`, the FINAL
Ultima `106` (the single highest band in the game).

| Battle | Target feel | Level band | New wrinkle / boss loot |
|--------|-------------|------------|--------------------------|
| Doguola (33) | Ambush pincer | 100–103 | Dragoon+Black Mage pincer |
| Bervenia (34) | Templar duel | boss 104, adds 100–103 | **Meliadoul** Mighty Sword; **rare (Tier A)** |
| Finath (35) | Wild beast field | monsters 100–103 | chocobo/monster tempo; Pig recruit |
| Zeltennia Church (36) | Zalmo dies at last | boss 104, adds 100–103 | reviving Inquisitor killed; **rare (Tier A)** |
| Bed Desert (37) | Open-desert gun-duel | boss 104, adds 101-102 | **Barich** Glacial Gun; **rare (Tier A)**; no Hydra (->`057`) |
| Bethla South Wall (38A) | Melee/stealth wall assault | 101-102 | Knight wall + Ninja/Thief flank |
| Bethla North Wall (38B) | Ranged/AoE wall assault | 101-102 | Summoner + 2 Dragoon Jump pressure |
| Bethla Sluice (39) | Floodgate objective | 100–102 | lever puzzle under casters; only lever Knights at 102 |
| Germinas (40) | Vertical skirmish | 100–102 | 2 Ninja/2 Thief climb; only 2 anchors at 102; buried loot |
| Poeskas Lake (41) | Undead lake | 100–102 | four L100-101; only Mystic/Summoner L102; reraise |
| Limberry Gate (42) | Assassin flee-race | 100–102 | Celia/Lettie L102; Reavers L100-101; chain 1/3 |
| Limberry Keep (43) | **Elmdor → demon** | 100–102 | Elmdor L102; Assassins L101; demons L100; chain 2/3 |
| Limberry Undercroft (44) | **Zalera** Lucavi | 100–102 | Zalera L102; Mystic/Knights L101; 2 Archaeodaemons L100; chain 3/3 |
| Eagrose (45) | **Dycedarg → Adramelk** | s2/s3/s6 L100; s4/s5 L101; named 103; Lucavi 105 | v3 three-style Knight wall complete; **rare** |
| Mullonde Exterior (46) | Holy-ground casters | 100–102 | W.Mage L102; Summoner/Orators L101; Geomancers L100; chain 1/3 |
| Mullonde Nave (47) | Triple-Templar boss | bosses 104–105 | **Folmarv/Loffrey/Cletienne**; Tier-S spoils; chain 2/3 |
| Mullonde Sanctuary (48) | Undead **Zalbaag** | boss 105, demons 103 | undead brother + Ultima Demons; Tier-S spoils; chain 3/3 |
| Vaults 4th (49) | ENDGAME 1/5; break gauntlet | 103–104 | Rend Knights; no resupply |
| Vaults 5th (50) | ENDGAME 2/5; **Loffrey** | boss 105, casters 103 | caster crossfire; no usable gauntlet reward |
| Necrohol (51) | ENDGAME 3/5; **Cletienne** | boss 105, elite screen 104 | **Samurai** debut; surge race; no usable gauntlet reward |
| Lost Halidom (52) | ENDGAME 4/5; **Barich** + apex monsters | Barich 105, monsters 105 | 4-monster breath pit + control; no usable gauntlet reward |
| Airship Graveyard (53) | ENDGAME 5/5; **Hashmal -> Ultima** | Hashmal 105, **Ultima 106** | two-phase FINAL; no usable gauntlet reward |

**Consecutive chains to test back-to-back:** Limberry (42→43→44), Mullonde (46→47→48), and the
five-battle **endgame gauntlet** (49→50→51→52→53). These are the chapter's defining structural test —
no resupply within a chain.

## Workflow per battle (same as Chapters 1–3)

```text
1. Read this overview + the battle doc.
2. On Windows: identify the BattleId / ENTD entry (cross-ref SortieConfirm, EventId, Map,
   scenario tables; sanity-check with FFTIvaliceEditor).
3. Dump the entry; confirm the original roster matches the doc's "Original Battle".
4. Apply the New Game++ composition: levels, JOB ESCALATION swaps, gear, BEST-TIER BOSS LOOT, skills,
   placement, and guest-control flags for every active guest.
5. Patch via the right layer (.bin or OverrideEntryData); keep the diff inside the battle window.
6. Copy into the mod, install to Reloaded-II, test from a New Game+ save.
7. Record results back in the battle doc.
```

## Sources

- Game8, "Chapter 4: In the Name of Love Walkthrough":
  https://game8.co/games/Final-Fantasy-Tactics/archives/543560
- Game8 per-battle walkthroughs (rosters) — linked in each battle doc (IDs are NON-sequential, verify
  each before designing).
- Local: `000-chapter-1-overview.md`, `011-chapter-2-overview.md`, `024-chapter-3-overview.md`
  (carried rules), `036-chapter-3-balance-review.md` (exception log + rare-loot ledger this chapter
  builds on and completes).
