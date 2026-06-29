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
   is allowed its boss-spike — but still ONE headline demand per battle.
2. RARE / NON-BUYABLE GEAR — this is the chapter where the RESERVED best-in-slot gear finally unlocks.
   Bosses still carry the named Tier-A/Tier-S highlights, but Chapter 4 normal enemies may also carry
   role-fitting non-buyable gear as part of broken puzzle-party builds. The absolute best-of-the-best
   remains tiered into the ENDGAME sequence (Mullonde → Airship Graveyard).
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
| `043` | 38 | Fort Besselat S/N Wall / Bethla | Wall assault (player picks S or N path) | branching vertical wall — S melee/stealth, N ranged/AoE; no rare | ✅ Done |
| `044` | 39 | Fort Besselat Sluice / Bethla Sluice | The floodgate; pull levers (open the gate) | lever objective-race + AoE on high ground; Time-Mage Slow; no rare | ✅ Done |
| `045` | 40 | Mount Germinas / Germinas Peak | Climb; buried Invisibility Cloak | 4/5★ vertical mobility/steal; Thief→2nd Ninja; no rare | ✅ Done |
| `046` | 41 | Lake Poescas / Poeskas Lake | All-undead lake (5★) | reraise permakill war; +Dark-heal Mystic; PD/Holy answer; no rare | ✅ Done |
| `047` | 42 | Limberry Castle Gate | **Celia & Lettie** (Assassins; flee on critical) | 5★ assassin flee-race + Ultima/status-immunity tradeoff; chain 1/3; no rare | ✅ Done |
| `048` | 43 | Limberry Castle Keep | **Elmdor** (dies); Celia/Lettie → Ultima Demons | Shirahadori parry-puzzle race; **Masamune + Genji Armor** (Tier A); chain 2/3 | ✅ Done |
| `049` | 44 | Limberry Undercroft | **Zalera** (3rd Lucavi) + undead guard | mass-status Lucavi (constrained); **Aegis Shield** (Tier A); chain 3/3 | ✅ Done |
| `050` | 45 | Eagrose Castle / Igros Castle | **Dycedarg → Adrammelech** (Lucavi) | 2-phase brother duel: stair-wall → spread-or-die; **Grand Helm** (Tier A) | ✅ Done |
| `051` | 46 | Mullonde Cathedral / Murond | Exterior; 2 Geomancer/2 Orator/Summoner + hidden roof W.Mage | hidden-healer caster screen; split deploy; chain 1/3 | ✅ Done |
| `052` | 47 | Mullonde Nave | **Folmarv/Loffrey/Cletienne** (ends when ONE falls; others retreat) | triple-Templar boss; equip-break race; chain 2/3; **Tier-S Chaos Blade (Folmarv)** | ✅ Done |
| `053` | 48 | Mullonde Sanctuary | **Zalbaag** (vampire Ark Knight) + 2 Archaeodaemon + Ultima Demon | undead brother; vampirism+break race; chain 3/3; **Tier-S Ribbon (Zalbaag)** | ✅ Done |
| `054` | 49 | Monastery Vaults 4th Floor | ENDGAME 1/5; 3 Knight (Rend cap 2) + 2 Monk + Ninja(was Archer) | light gear-preservation opener; no boss/no rare | ✅ Done |
| `055` | 50 | Monastery Vaults 5th Floor | ENDGAME 2/5; **Loffrey** (Divine Knight) + 2 BlackMage/2 Summoner/Time Mage | caster crossfire; disarm-first; win-when-Loffrey-falls; **Tier-S Escutcheon (Loffrey)** | ✅ Done |
| `056` | 51 | Necrohol of Mullonde | ENDGAME 3/5; **Cletienne** (Magick Surge) + 2 Samurai/2 Ninja/2 Time Mage | **Samurai** debut (canon); Silence/burst-the-surge race; win-when-Cletienne-falls; **Tier-S Robe of Lords (Cletienne)** | ✅ Done |
| `057` | 52 | Lost Halidom / Lost Sacred Precincts | ENDGAME 4/5 (**5★ peak**); **Barich** rematch + 2 Hydra/Tiamat/Dark Behemoth/Chemist | 3x-breath dragon pit + Disable/Immobilize control; win-when-Barich-falls; **Tier-S Materia Blade (halidom relic)** | ✅ Done |
| `058` | 53 | Airship Graveyard | ENDGAME 5/5; **Hashmal → Ultima** (FINAL, L106) + Ultima Demons | two-phase Lucavi finale; full-restore between; Dispelja/Almagest + 2nd form; **capstone Tier-S Ragnarok (Ultima)** | ✅ Done |
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
- Samurai (enemy)   : Draw Out (katana spirits) — AoE elemental/heal/buff from the blade. Debut at
                      the Necrohol (Cletienne's guard). Treat Draw Out like a telegraphed AoE: strong,
                      spaceable, not a lock.
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
    Aegis Shield, best robes below Robe of Lords, Grand Helm/Crystal-tier armor.

  TIER S — the BEST OF THE BEST  → the ENDGAME sequence ONLY (Mullonde 47-48, Vaults/Necrohol/Halidom
    50-52, and the Airship Graveyard finale 53):
    Ragnarok (best sword), Chaos Blade (best knight sword), Ribbon (best headgear), Robe of Lords
    (best robe), Escutcheon (best shield), Materia Blade (special), and the single capstone reward on
    the FINAL boss.

ASSIGNMENT RULES:
  - A boss that FLEES/SURVIVES still drops nothing; the rare is paid where it dies.
  - Each boss battle gives ONE rare highlight; this is no longer exclusive. Chapter 4 normal enemies
    may also carry role-fitting non-buyable gear when it supports a readable broken-party puzzle.
  - Any normal-enemy non-buyable gear must be documented per battle as steal-bait, role identity,
    or puzzle pressure. Do not hide essential rewards on throwaway generics without intent.
  - The rare fits the boss's identity AND is a real in-fight threat or a tempting steal.
  - Elmdor's iconic MASAMUNE + GENJI (deferred from Riovanes in Ch3) are paid HERE, at Limberry Keep
    (043), where he is decisively defeated — Tier A, not the absolute capstone.
  - The single best capstone item is reserved for the FINAL battle (Airship Graveyard, 058).
```

Each boss battle doc includes a **"Boss rare loot"** line naming the item, its tier (A vs S), why it
fits, and confirming the best-of-best stays on the endgame.

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
| Bethla Wall (38) | Branching wall assault | 100–103 | choose S/N path; Ninja/Summoner |
| Bethla Sluice (39) | Floodgate objective | 100–103 | lever puzzle under casters |
| Germinas (40) | Vertical skirmish | 100–103 | Ninja/Thief climb; buried loot |
| Poeskas Lake (41) | Undead lake | 100–103 | high undead + reraise |
| Limberry Gate (42) | Assassins-as-demons | adds 103, bosses 104 | Celia/Lettie Ultima Demons; chain 1/3 |
| Limberry Keep (43) | **Elmdor → demon** | boss 104→demon 105 | **Masamune + Genji (Tier A)**; chain 2/3 |
| Limberry Undercroft (44) | **Zalera** Lucavi | Lucavi 105, adds 103 | 3rd Lucavi spike; **rare**; chain 3/3 |
| Eagrose (45) | **Dycedarg → Adramelk** | duel 104, Lucavi 105 | brother → Lucavi (2-phase); **rare** |
| Mullonde Exterior (46) | Holy-ground casters | 100–103 | Geomancer/Orator; hidden W.Mage; chain 1/3 |
| Mullonde Nave (47) | Triple-Templar boss | bosses 104–105 | **Folmarv/Loffrey/Cletienne**; **rare (Tier S)**; chain 2/3 |
| Mullonde Sanctuary (48) | Undead **Zalbaag** | boss 104, demons 103 | undead brother + Ultima Demons; **rare (Tier S)**; chain 3/3 |
| Vaults 4th (49) | ENDGAME 1/5; break gauntlet | 103–104 | Rend Knights; no resupply |
| Vaults 5th (50) | ENDGAME 2/5; **Loffrey** | boss 104, adds 103 | Templar summoner; **rare (Tier S)** |
| Necrohol (51) | ENDGAME 3/5; **Cletienne** | boss 104, adds 103 | **Samurai** debut; **rare (Tier S)** |
| Lost Halidom (52) | ENDGAME 4/5; **Barich** + dragons | boss 104, dragons 104 | **Hydra + Tiamat**; **rare (Tier S)** |
| Airship Graveyard (53) | ENDGAME 5/5; **Hashmal → Ultima** | Hashmal 105, **Ultima 106** | two-phase FINAL; **THE capstone rare (Tier S)** |

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
```
</content>
