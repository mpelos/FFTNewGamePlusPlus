# 059 - Chapter 4 Balance Review

A cross-battle audit of all **21** Chapter 4 New Game++ designs (`038`–`058`) — the final and largest
chapter. It checks the difficulty curve, verifies level bands / gear / job-skill consistency, logs the
deliberate design exceptions, and carries the **job-escalation ledger** and **rare-boss-loot ledger**
forward from Chapter 3 — now split into **Tier-A** and the chapter-defining **Tier-S best-of-best**. It
audits the **three no-resupply chains** (Limberry, Mullonde, and the five-battle endgame gauntlet) and
the **two-phase finale**, then flags the open risks and a recommended playtest order. Paper review —
every finding re-validates in-game once each battle is patched on the Windows data.

## The central balancing insight (carried from Chapters 1–3)

Enemies are still scaled `Level = 100 + offset`, so the offset is fine-tuning, not the main lever.
Difficulty comes from composition, terrain, mechanics, the new job/escalation each fight, and the
bosses. Chapter 4 is the **climax**: it takes the elite Ch3 roster and adds the campaign's heaviest
structural pressures.

```text
- APEX CASTES & BOSSES: the SAMURAI preview at Sluice and showcase at Necrohol, the Ultima-Demon caste (Limberry Keep on), apex
  MONSTER PIT (Lost Halidom jobs 135/139/140/141), the vampire Ark Knight (Zalbaag), the triple-Templar last
  stand (Folmarv/Loffrey/Cletienne), the Magick-Surge sorcerer, THREE Lucavi (Zalera, Adrammelech, and
  the final Hashmal→Ultima), and named bosses paying out across the chapter.
- THREE NO-RESUPPLY CHAINS: Limberry (42-44), Mullonde (46-48), and the FIVE-battle ENDGAME GAUNTLET
  (49-53) — the longest sustained stretch in the game. Resource economy is a primary difficulty axis.
- TIER-S BEST-OF-BEST: the campaign's finest usable rewards are paid by the end of the Mullonde chain
  (`051`-`053`), before the point of no return. The final gauntlet (`054`-`058`) adds no usable reward;
  it is the challenge payoff, not an equipment payout.
```

## Difficulty curve (all 21 battles, as designed)

| # | Battle | Doc | Enemies | New demand / party engine | Terrain | Tier |
|---|--------|-----|---------|------------------------------|---------|------|
| 33 | Dugeura Pass | `038` | 6 (2 Black Mage + 2 **Dragoon** + Knight + Haste Time Mage) | open-field tempo (Haste); no boss | open field | ▃ moderate |
| 34 | Free City of Bervenia | `039` | 6 (**Meliadoul** + 2 Summoner + 2 Archer + Ninja; dies) | first Ch4 boss duel; equip-break; **Tier-A Save the Queen** | urban | ▅ hard |
| 35 | Finnath Creek | `040` | 5 (2 Black Choco + 2 Yellow Choco + Red) + Pig | de-randomized beast flock; no boss | creek | ▂ light |
| 36 | Outlying Church | `041` | 6 (**Zalmo** + 3 Knight + 2 Mystic; dies) | holy burst-duel; Rend cap 2; **Tier-A Light Robe** | church | ▄ moderate+ |
| 37 | Bed Desert | `042` | 6 (**Barich** + 2 Knight + 2 Archer + Black Mage; recurs) | open-desert gun-duel; **Tier-A Glacial Gun** | desert | ▄ moderate+ |
| 38A | Fort Besselat — South Wall | `043a` | 7 (3 Knight + 2 Archer + Thief + Ninja) | melee/stealth wall approach; no boss | wall | ▃ moderate |
| 38B | Fort Besselat — North Wall | `043b` | 6 (2 Archer + 2 Dragoon + Summoner + Monk) | ranged/AoE wall approach; no boss | wall | ▃ moderate |
| 39 | Fort Besselat — Sluice | `044` | 8 (2 Black Mage + 2 lever Knight + 2 Samurai + 2 Geomancer) | six L100; only lever Knights L102; level-regression pending | sluice | ▅ hard |
| 40 | Mount Germinas | `045` | 6 (2 **Ninja** + 2 Thief + 2 Archer) | band 100-102; only Apex Ninja + primary Archer L102; playtest pending | mountain | ▄ moderate+ |
| 41 | Poeska's Lake | `046` | 6 (2 Revenant + 2 Archer + Mystic + Summoner) | band 100-102; four complete human-undead kits; playtest pending | frozen lake | ▅ hard |
| 42 | Limberry — Gate | `047` | 6 (Celia & Lettie **Assassins**, flee + 4 Reaver) | band 100-102; dual Masamune vs Koga/Iga flee-race; playtest pending | gate | ▃ moderate (race) |
| 43 | Limberry — Keep | `048` | (**Elmdore** Ark Knight; dies → Celia/Lettie transform to **Ultima Demons**) | band 100-102; Chirijiraden + armed Assassin parry-race; playtest pending | keep | ▆ harder |
| 44 | Limberry — Undercroft | `049` | (**Zalera** + 2 Archaeodaemon + 3 Martial Arts Undead Knights) | v3 implemented; 6 enemies; sprite-budget-safe guard; band 100-102; **Tier-A Aegis Shield**; playtest pending | undercroft | ▆ harder |
| 45 | Eagrose Castle | `050` | Zalbaag + **Dycedarg** + 2 Martial Knights + Samurai Knight + 2 Dragoons → **Adrammelech** | v3 Javelin "II" Dragoons; playtest pending | castle | █ SPIKE |
| 46 | Mullonde — Exterior | `051` | 6 (hidden roof **White Mage** + 2 Geomancer + 2 Orator + Summoner) | v3 implemented/deployed; playtest pending; gender recast; band 100-102; Stoneshooter/Mana-Shield Orators | cathedral ext | ▃ moderate |
| 47 | Mullonde — Nave | `052` | 3 (**Folmarv + Loffrey + Cletienne**; win when ONE falls) | v3 implemented/deployed; boss equipment refresh; **Tier-S Chaos Blade + Escutcheon + Lordly Robe** unchanged; chain 2/3; playtest pending | nave | ▅ hard |
| 48 | Mullonde — Sanctuary | `053` | (**Zalbaag** vampire Ark Knight + 2 Archaeodaemon + Ultima Demon; dies) | v3 implemented/deployed: Eagrose guest loadout; **Tier-S Ragnarok + Ribbon** unchanged; chain 3/3; playtest pending | sanctuary | ▆ harder |
| 49 | Monastery Vaults — 4th | `054` | 6 (2 Eagrose Knight Martial Artists + Eagrose Knight Samurai + 2 South Wall Monks + South Wall Ninja) | v3 implemented/deployed; no reward; gauntlet 1/5; playtest pending | vault | ▂ light (opener) |
| 50 | Monastery Vaults — 5th | `055` | 6 (**Loffrey** + 2 female Black Mage + 2 female Summoner + female Time Mage) | v3 implemented/deployed; level-102 caster crossfire; active Zeus Mace exception; playtest pending | wide vault | ▅ hard |
| 51 | Necrohol of Mullonde | `056` | 7 (**Cletienne** + 2 true **Samurai** + 2 Ninja + 2 female Time Mage) | v3 implemented/deployed; generics 102-103; no special spoil; playtest pending | dead city | ▆ harder |
| 52 | Lost Halidom | `057` | 6 (**Barich** + 2 Monks + Greater Hydra + Tiamat + Dark Behemoth) | v3 implemented/deployed; copied Stoneshooter Barich; playtest pending | holy ground | █ 5★ PEAK |
| 53 | Airship Graveyard | `058` | P1 **Hashmal** → P2 **Ultima** + Ultima Demons/Lucavi support | v3 implemented/deployed; bosses/forms 105, support/demons 103; playtest pending | airship | █ FINALE |

Reading: Chapter 4 is a **long rising arc broken into three no-resupply chains, with two mid-chapter
Lucavi spikes and a five-fight gauntlet to the finale**. The open battles (33-41) escalate the elite
roster and pay out the **Tier-A** unlocks one boss at a time, with two valleys (Finnath 35, Besselat
Wall 38) for breath. The **Limberry chain (42-44)** climbs from a flee-race to the first Lucavi spike
(**Zalera**). **Eagrose (45)** is the second spike (the **Dycedarg→Adrammelech** brother duel). The
**Mullonde chain (46-48)** completes the usable **Tier-S** payouts before the point of no return. The
**endgame gauntlet (49-53)** is the campaign's spine: a light opener, two escalating boss-races, the
**5★ Lost Halidom** peak, and the **two-phase finale**, with no usable rewards inside the gauntlet.

```text
The back five (the endgame gauntlet) in one line each:
  Vaults 4th    : a LIGHT gear-preservation opener — don't lose your blade to Rend before the marathon
  Vaults 5th    : cross a caster crossfire, disarm Loffrey, burst him            (disperse; Steal Weapon)
  Necrohol      : Silence/burst the Magick-Surge mage past a Samurai/Ninja screen (tempo; don't slow-chip)
  Lost Halidom  : the 5★ four-monster breath pit — disable the beasts, break Barich's hold (elemental resist; Arm Shot)
  Airship       : Hashmal, then Ultima — spread, re-buff, weather Almagest, end it (adapt; the capstone)
```

### Curve verdict

```text
PASS (on paper). The campaign's highest overall, capped by level-105 bosses, with finale support at 103. The
highest in the mod) and the three no-resupply chains. Two mid-chapter Lucavi spikes (Zalera 049,
Adrammelech 050) and the 5★ Lost Halidom (057) are the peaks; deliberate valleys (Finnath 035,
Besselat Wall 038, Mullonde Exterior 051, Vaults-4th 054) keep the long arc from being a flat climb and
seat the spikes by contrast. The repeat foes are each staged differently — Barich (open duel 042 →
dragon-pit rematch 057), Elmdore/Celia/Lettie (Limberry Keep 048, paying the Ch3 Roof deferral), and
the three Templars (retreat at the Nave 052 → die individually at 055/056) — so none read as re-runs.
The endgame GAUNTLET (49-53) is the defining structural test; flagged as the #1 playtest risk.
```

## Level bands & boss policy

```text
Generics: normally 100-103 (endgame-tier). Sluice through Limberry Undercroft deliberately concentrate most units
at 100-101 and cap their few anchors at 102; their objective/terrain and complete kits carry the pressure.
Elite/sub-bosses: 103-104 (Samurai, Ultima Demons, Hydra).
Human bosses: 104-105 (Meliadoul, Zalmo, Barich, Elmdore, Folmarv/Loffrey/Cletienne, Zalbaag, Dycedarg).
LUCAVI: normally 105 (Adrammelech, Hashmal); Zalera is the low-band exception at 102 because it closes
the three-battle Limberry chain. FINAL ULTIMA: 105, sharing the global boss cap.
Apex monsters: the final Lost Halidom monster pit uses three level-102/103 monster slots; pressure comes
from overlapping breath lanes, sustain, and Barich control, with elemental/disable answers preserved.

Boss-loot policy (Chapter 4): the long-promised payoff. Bosses that DIE carry ONE named rare highlight;
the chapter splits them into TIER-A (strong, on the open/Limberry/Eagrose bosses) and TIER-S best-of-best
(paid by the end of the Mullonde chain before the final no-resupply gauntlet). This boss-highlight ledger
is no longer exclusive: per the global philosophy in `000`, Chapter 4 normal enemies may also carry
role-fitting non-buyable gear when it supports a readable broken-party puzzle. Bosses that FLEE normally
carry no named rare highlight, except the current reward ledger deliberately pays Loffrey/Cletienne
payloads at Nave before the point of no return. The final gauntlet carries no usable rewards. EXCALIBUR
stays with Orlandeau (the player's holy blade) — never on an enemy.
```

## Brave/Faith audit

```text
PASS (docs). Every Chapter 4 battle doc (`038`-`058`) now records Br/Fa for each fixed active enemy
or active story/guest record in the proposed composition / enemy-party escalation table. Script
placeholders are marked `preserve` instead of receiving fake active values. Player-deployed units
remain player-build data and are not fixed by encounter docs.

Design intent: Chapter 4 uses Brave/Faith as a puzzle lever. Physical elites and bosses carry high
Brave; casters carry high Faith; undead and apex monsters intentionally keep low Faith unless their
Lucavi/demon identity needs magic/status interaction. The final gauntlet documents no-reward pressure
and no hidden Brave/Faith assumptions.
```

## Design-exception log

| Exception | Where | Why | Guardrail |
|-----------|-------|-----|-----------|
| Time-Mage Haste/Slow/Float | Dugeura (`038`), Vaults-5th (`055`), Necrohol (`056`) | canonical tempo casters | Haste/Slow/Float only — no Stop/Don't Act; one effective disruptor per fight |
| Templar/Knight equip-break (Mighty/Unyielding Blade, Rend/Arts of War) | Bervenia (`039`), Church (`041`), Undercroft (`049`), Eagrose (`050`), Nave (`052`), Sanctuary (`053`), Vaults-4th (`054`), Vaults-5th (`055`) | the break castes | normally **≤2 break sources/fight**; Eagrose is the documented exception with three main-job Knights retaining Arts of War |
| Knight/Dragoon castes | Eagrose P1 (`050`) | 2 Monk-bucket Knights + Samurai-bucket Knight + 2 true Dragoons | Knights retain Arts of War; Dragoons use Jump, no secondary, Doublehand and Javelin "II" |
| De-randomized beasts | Finnath (`040`) | reliable, learnable flock | fixed kits (Choco-Meteor/Cure); no status beasts; no boss |
| Healer/holy boss burst | Church (`041`) | Zalmo's revive/holy IS the puzzle | Silence/focus-burst answer; holy/soft-status only; he dies → Tier-A |
| Branching mutually-exclusive approach | Besselat Wall (`043a`/`043b`) | the fort's two routes | each route self-contained; no boss; both lead to the Sluice |
| Objective-race (floodgate lever) | Sluice (`044`) | the canonical flood mechanic | race vs clear-first; charged damage and visible guards, no hard control or Rend wall |
| Undead reraise + heal-weakness | Poeska (`046`), Undercroft (`049`), Sanctuary (`053`), Airship demons (`058`) | the undead/demon castes | PD/Holy/finish-while-down answers; one-disruptor cap; reraise is mechanic + counterplay |
| Assassin status / instant-death / flee-on-critical | Limberry Gate (`047`) | the named Assassins | RESISTABLE + non-spam; status-immunity tradeoff; flee makes the danger window short; no rare (flee) |
| Ark-Knight parry / Shirahadori | Limberry Keep (`048`) | Elmdore's identity | magic / Divine-Ruination answer; he dies → Tier-A Masamune+Genji |
| Lucavi mass-status (Zalera) | Undercroft (`049`) | the chapter's first Lucavi | ONE telegraphed source; resistable/cleansable/non-locking; Doom race-able |
| Lucavi summon-AoE (Adrammelech) | Eagrose P2 (`050`) | the 2nd-spike Lucavi | spread-or-die spaceable; Confuse/Stone resistable; 2-phase transform |
| Hidden-healer sustain | Mullonde Exterior (`051`) | the rooftop White Mage IS the puzzle | reach it (height-ignoring) / Silence; sustain not a lock; no boss → no rare |
| Win-on-one-boss-falls (triple Templar) | Nave (`052`) | the canonical "defeat one, others flee" | the other two retreat → no drop; equip-break capped 2 |
| Vampirism (Zalbaag) | Sanctuary (`053`) | the vampire Ark Knight | SOLE source; Holy Water/Japa Mala/Esuna; non-spreading; not a lock |
| Magick Surge (comeback mechanic) | Necrohol (`056`) | Cletienne's identity | Silence shuts it / burst beats it; magic-only retaliation; telegraphed, not a wipe |
| Samurai Draw Out (NEW caste) | Sluice (`044`), Necrohol (`056`) | preview at the floodgate, endgame showcase in Cletienne's guard | AoE/break race-able, spaceable; no hard lock |
| Monster breath lanes + Disable/Immobilize | Lost Halidom (`057`) | the 5★ four-monster pit + control boss | breath ELEMENTAL/resistable + monsters disable-able; Barich status ONE resistable source (Ribbon) |
| Almagest / Dispelja / demon surround / 2nd form | Airship (`058`) | the Lucavi FINALE | Almagest telegraphed/sub-100%/survivable; Dispelja → re-buff; surround → Ribbon+spacing; transform telegraphed; full HP/MP restore between phases |

Hard control (Stop/Don't Act/Petrify spam) remains banned everywhere. Equip-break normally stays at
≤2 sources/fight; Eagrose is the explicit exception with three main-job Knights and therefore three
primary Arts of War sources. Every Lucavi/finale ultimate is telegraphed and sub-lethal by design — no
scripted unavoidable wipe in the entire chapter.

## Job-escalation ledger (rule 1)

```text
Dugeura      (038) : Archer -> Haste Time Mage; open-field tempo            -> outpace the Haste, no ambush
Bervenia     (039) : first Ch4 Templar BOSS duel (Meliadoul; equip-break)   -> Safeguard/Steal, burst her
Finnath      (040) : de-randomized chocobo flock                            -> learnable beasts (light)
Church       (041) : holy burst-boss Zalmo + Rend Knights (cap 2)           -> Silence/burst; keep gear
Bed Desert   (042) : open-desert gun-duel Barich                            -> close the gap, disarm the gun
Besselat Wall(043a/043b) : split melee(S) vs ranged(N) approach            -> pick a route, no boss
Besselat Slu.(044) : floodgate race; six L100 + two lever Knights L102      -> race the lever or clear first
Mt Germinas  (045) : four L100-101 + two L102 anchors; Martial Arts       -> climb/intercept; dig the Cloak
Poeska       (046) : four L100-101 + Mystic/Summoner L102; all-undead       -> permakill the dead (Holy/PD)
Limberry Gate(047) : L102 Assassins + L100-101 Reavers; dual blades         -> burst one to critical; no rare
Limberry Keep(048) : L102 Elmdor + L101 Assassins + L100 demons            -> answer parry; Tier-A
Limberry Und.(049) : L102 ZALERA + 3 L101 Undead Knights + 2 L100 Archaeodaemons -> race status
Eagrose      (050) : L103 Zalbaag/Dycedarg + L100-101 Martial/Samurai Knights + Javelin "II" Dragoons -> L105 Adrammelech
Mullonde Ext.(051) : hidden-roof White Mage sustain + caster screen; chain 1/3 -> kill the healer first
Mullonde Nave(052) : TRIPLE-TEMPLAR (Folmarv/Loffrey/Cletienne; one-falls); chain 2/3 -> commit to Folmarv
Mullonde San.(053) : ZALBAAG vampire Ark Knight + undead; chain 3/3         -> cleanse vampirism; holy the dead
Vaults 4th   (054) : Archer -> Ninja; LIGHT gear-preservation opener; gauntlet 1/5 -> keep your gear (Rend cap 2)
Vaults 5th   (055) : LOFFREY + caster crossfire; gauntlet 2/5              -> disperse, disarm, burst
Sluice       (044) : SAMURAI PREVIEW in the floodgate screen                -> race or clear the charged guard line
Necrohol     (056) : SAMURAI SHOWCASE + Cletienne Magick Surge; gauntlet 3/5 -> Silence/burst the surge
Lost Halidom (057) : APEX MONSTER PIT (4 monster/dragon slots) + Barich; gauntlet 4/5 -> disable + elemental resist
Airship      (058) : HASHMAL -> ULTIMA two-phase FINALE (bosses 105); gauntlet 5/5 -> spread, re-buff, end it

New content first seen in Chapter 4: the SAMURAI caste (056, canonical), the ULTIMA-DEMON caste (048),
APEX MONSTERS / monster-dragon slots (057), the vampire Ark Knight (053), the triple-boss "one
falls" structure (052), the Magick-Surge mechanic (056), and THREE Lucavi (Zalera 049, Adrammelech 050,
Hashmal+Ultima 058). Revised rule: one headline puzzle engine per fight, with the rest of the enemy
team allowed to amplify that engine through complete, synergistic, sometimes broken Chapter 4 kits.
```

## Rare-boss-loot ledger (rule 2) — TIER-A + TIER-S

```text
TIER-A (strong, non-best-in-slot; open + Limberry + Eagrose bosses that DIE):
  Meliadoul   (039) : SAVE THE QUEEN  (Knight Sword; steal-bait)        -> first Ch4 rare; kept singular.
  Zalmo       (041) : LIGHT ROBE      (robe; holy/defensive)            -> the holy boss's drop.
  Barich      (042) : GLACIAL GUN     (gun; disarm reward)              -> his first fight; not re-dropped at 057.
  Elmdore     (048) : MASAMUNE + GENJI ARMOR  (katana + armor)          -> pays the Ch3 Roof deferral.
  Zalera      (049) : AEGIS SHIELD    (shield; magic-evade)             -> the 1st Lucavi's drop.
  Adrammelech (050) : GRAND HELM      (helm; top defense)               -> the 2nd-spike Lucavi's drop.

TIER-S (best-of-best; paid before the no-resupply final gauntlet):
  Folmarv     (052) : CHAOS BLADE     (dark Knight sword)   -> first Tier-S; the corrupted leader's blade.
  Loffrey     (052) : ESCUTCHEON      (best shield)         -> guaranteed Nave payload, before point of no return.
  Cletienne   (052) : LORDLY ROBE     (best caster robe)    -> guaranteed Nave payload, before point of no return.
  Zalbaag     (053) : RIBBON          (ultimate protection) -> status answer for 057/058.
  Zalbaag     (053) : RAGNAROK        (legendary sword)     -> paid before the final gauntlet; no dead final loot.
  Materia Blade      : NOT placed in campaign battle 057; remains outside this gauntlet reward plan.

NO NAMED BOSS RARE (boss flees / no named boss -> deferred or none; normal enemies may still carry
role-fitting non-buyables under the Chapter 4 puzzle-party policy):
  Dugeura (038), Finnath (040), Besselat Wall (043a/043b), Sluice (044), Mt Germinas (045), Poeska (046),
  Limberry Gate (047, Celia/Lettie flee -> paid as Ultima Demons at 048), Mullonde Exterior (051),
  Vaults 4th (054), Vaults 5th (055), Necrohol (056), Lost Halidom (057), Airship Graveyard (058).

LEDGER REASSIGNMENT (logged): the old endgame plan placed Escutcheon/Lordly Robe/Materia Blade/
Ragnarok inside the no-resupply gauntlet. That is now superseded. Escutcheon and Lordly Robe pay at
Nave (052), Ragnarok pays at Sanctuary (053), Materia Blade is not placed in campaign battle 057, and
the final gauntlet is restored to standard/vanilla loot only.

UNUSED Tier-A (available, not needed this chapter): Genji Shield/Helm, Diamond Armlet. DEFENSE RING was
AVOIDED (already the Ch3 Belias drop). No best gear leaked early; Excalibur reserved to Orlandeau.
```

## Consistency audit

### Job / unit IDs

```text
Confirmed & reused identically (Ch1-3): Squire 74, Chemist 75, Archer 77, Thief 83.
TBD (verify on Windows, used by name): Knight, Monk, Black Mage, Time Mage, Summoner, Geomancer, Orator,
  White Mage, Mystic, Ninja, Dragoon, and the Ch4 names — Samurai (DEBUT), Divine Knight (Folmarv/
  Loffrey), Sorcerer (Cletienne), Ark Knight (Elmdore/Zalbaag), Inquisitor (Zalmo), Machinist (Barich),
  Assassin (Celia/Lettie), Lucavi (Zalera/Adrammelech/Hashmal/Ultima), Ultima Demon, Archaeodaemon,
  Revenant/undead, and apex monster pit jobs 135/139/140/141.
Boss scripting to preserve (highest-risk patches):
  Meliadoul "defeat ends fight" (039); Zalmo/Barich death triggers (041/042); the Besselat Wall BRANCH
  (043a/043b); the Sluice LEVER objective (044); Celia/Lettie FLEE at Gate (047) then TRANSFORM to Ultima
  Demons at Keep (048); Elmdore death (048); Zalera mass-status script (049); the Eagrose 2-phase
  Dycedarg->Adrammelech TRANSFORM + summon spawn (050); the Nave "win when ONE of three falls, others
  RETREAT" (052); Zalbaag vampire/undead + "defeat ends fight" (053); the Vaults-5th "Defeat Loffrey"
  (055) and Necrohol "Defeat Cletienne" + Magick Surge (056); the Lost Halidom "Defeat Barich, monsters
  optional" (057); and the FINALE two-phase Hashmal->Ultima + full HP/MP RESTORE between phases + the
  low-HP SECOND-FORM transformation (058). Diff-check and test every trigger.
```

### Equipment & skill IDs

```text
Reused without conflict (as Ch1-3): Featherweave Cloak 234, Runeblade 30, and the standard shop/mage/
  knight gear referenced by tier. Skills: Counter 442, Attack Boost 465, Movement +1 486, +2 487,
  Reflexes 449, Auto-Potion 441, Dual Wield/Concentration (TBD).
NEW Ch4 rare items to map in ItemData.xml (verify non-buyable + correct tier; NOT leaked earlier):
  TIER-A: Save the Queen (039), Light Robe (041), Glacial Gun (042), Masamune + Genji Armor (048),
    Aegis Shield (049), Grand Helm (050).
  TIER-S: Chaos Blade + Escutcheon + Lordly Robe (052), Ribbon + Ragnarok (053). Materia Blade is not
    placed in campaign battle 057. No usable reward appears in 054-058.
  Confirm Excalibur stays with Orlandeau (player) and is never placed on an enemy. Confirm Save the
  Queen is removed/avoided on Loffrey or any active finale script record if stealable. Confirm Barich's
  gun trio rewards stay at 042 and are not re-dropped or steal-leaked at 057.
No conflicts found on paper.
```

### Level bands & boss kits

```text
Consistent. Generics normally 100-103; Sluice through Limberry Undercroft use low-band 100-102 distributions;
elite/sub-bosses 103-104; later human bosses 104-105; later Lucavi 105; FINAL ULTIMA
105 (the global boss cap; finale distinction comes from its two-phase scripting rather than +6 scaling).
Summons kept MID-TIER with intact charge times; Draw Out (new) race-able; apex monster breath elemental/
resistable. Every Lucavi/finale ultimate telegraphed + sub-lethal.
```

## No-resupply chain audit (the chapter's defining structural test)

```text
CHAIN 1 — LIMBERRY (42-44 / 047-049), 3 battles, one loadout:
  Gate (flee-race) -> Keep (Elmdore parry; Tier-A Masamune+Genji) -> Undercroft (Zalera Lucavi SPIKE).
  Risk: a rising chain ending in the first Lucavi. The Tier-A Masamune+Genji land MID-chain, so the
  Undercroft spike is faced freshly geared. Verify winnable without item starvation; test back-to-back.

CHAIN 2 — MULLONDE (46-48 / 051-053), 3 battles, one loadout:
  Exterior (hidden-healer screen) -> Nave (triple-Templar; Chaos Blade + Escutcheon + Lordly Robe) ->
  Sanctuary (vampire Zalbaag; Ragnarok + Ribbon). Risk: the usable Tier-S set lands before the final
  point of no return; the RIBBON earned at 053 is the status answer the ENDGAME (esp. 057 Barich control
  + 058 demon surround) assumes — verify the player actually has it before the gauntlet. Test the chain
  as a unit.

CHAIN 3 — ENDGAME GAUNTLET (49-53 / 054-058), 5 battles, one loadout — THE LONGEST IN THE GAME:
  Vaults 4th (LIGHT opener, gear-preservation) -> Vaults 5th (Loffrey caster crossfire) -> Necrohol
  (Cletienne + Samurai surge race) -> Lost Halidom (5★ four-monster breath pit) -> Airship
  (Hashmal->Ultima FINALE). Risk: the #1 balance problem of the mod — five consecutive fights, no
  merchant, no usable rewards, rising to a 5★ peak and a two-phase finale. The light opener (054) is a
  deliberate resource on-ramp; the finale's full HP/MP restore between phases is the one mercy. VERIFY
  the whole gauntlet is winnable on a single well-prepared loadout (prep happens BEFORE 049). Test all
  five back-to-back, never in isolation.
```

## Open risks / watch-items for playtest

1. **The endgame gauntlet (49-53)** is the #1 risk: five no-resupply fights to a 5★ peak + two-phase
   finale. Verify winnable on ONE loadout (prep before 049); test all five back-to-back.
2. **The two earlier chains (Limberry 42-44, Mullonde 46-48)**: verify each is winnable on one loadout
   and that the Tier-S Ribbon (053) is in hand before the gauntlet's status threats.
3. **Two-phase Lucavi spikes (Zalera 049, Adrammelech 050)**: verify the single telegraphed status/
   summon source stays spaceable/resistable, the transforms fire correctly, and adds are clearable.
4. **5★ Lost Halidom (057)**: confirm the four-slot monster/dragon pressure is survivable with elemental
   resist + disabling/breaking the monsters, and Barich's Disable/Immobilize is one resistable source
   (Ribbon).
5. **The FINALE (058)**: the most important fairness check — Almagest telegraphed/sub-100%/survivable;
   the demon surround broken by Ribbon + spacing; both Ultima forms beatable; the full HP/MP restore and
   second-form transform fire correctly. Ultima L105 must be hard but FAIR — no unavoidable wipe.
6. **Win-on-one-falls integrity (Nave 052)**: verify defeating ONE of the three Templars ends the fight
   and the other two RETREAT, while the guaranteed spoils still pay the documented Nave reward set.
7. **Break-pressure stacking**: confirm the normal ≤2-source fights remain fair, and separately verify
   that Eagrose's documented five-Arts-of-War exception remains answerable through Safeguard, disarm,
   status, range, or focus fire rather than becoming an unavoidable equipment-deletion tax.
8. **Final-gauntlet reward leakage**: confirm no usable reward, steal-only unique, dormant reward, or
   duplicate best gear leaks from `054`-`058` (especially Save the Queen-like scripted gear at `055/058`,
   Barich gun-trio duplication at `057`, and any dormant Hashmal/Ultima reward data).
9. **Repeat-foe differentiation**: Barich (042 vs 057), Elmdore/Celia/Lettie (Ch3 Roof -> 047/048), and
   the three Templars (052 -> 055/056) must read as distinct stagings, not re-runs.
10. **Breather calibration** (Finnath 035→040, Besselat Wall 043a/043b, Mullonde Exterior 051, Vaults-4th
    054): confirm these feel lighter so the spikes land harder by contrast.
11. **Protect/guest & flee scripting**: Celia/Lettie flee (047) then return as Ultima Demons (048);
    confirm no rare leaks on the flee and the transform pays out correctly.
12. **Excalibur containment**: confirm Excalibur never appears on an enemy and stays Orlandeau's.

## Recommended implementation & playtest order

Implement in story order so the curve and the three chains can be felt as a player would:

```text
038 Dugeura -> 039 Bervenia -> 040 Finnath -> 041 Church -> 042 Bed Desert -> 043a South Wall / 043b North Wall ->
044 Besselat Sluice -> 045 Mt Germinas -> 046 Poeska ->
[CHAIN: 047 Limberry Gate -> 048 Limberry Keep -> 049 Limberry Undercroft] -> 050 Eagrose ->
[CHAIN: 051 Mullonde Exterior -> 052 Mullonde Nave -> 053 Mullonde Sanctuary] ->
[GAUNTLET: 054 Vaults 4th -> 055 Vaults 5th -> 056 Necrohol -> 057 Lost Halidom -> 058 Airship Graveyard]
```

For each: dump the real entry, fill the doc's "Local Data Confirmed", apply levels + job-escalation
swaps + gear + reward-ledger rules + skills, patch, diff-check inside the battle window only, then
test from a New Game+ save and record results. **Test the three chains as units** (no resupply) — they
are the chapter's defining balance problem, and the endgame gauntlet is the whole mod's hardest stretch.

## Status

```text
Design phase: COMPLETE for all 21 Chapter 4 battles (038-058 designed; this pass changed docs only).
Consistency: audited; exceptions logged; job-escalation and split Tier-A/Tier-S ledgers extended.
Curve: passes on paper; the campaign is capped by level-105 bosses and the three no-resupply chains;
  two Lucavi spikes + a 5★ peak + a two-phase finale; deliberate valleys seat the spikes.
Job escalation: one headline puzzle engine per fight; the Samurai caste debuts cleanly (canon), plus
  Ultima Demons, apex monsters, the vampire Ark Knight, the triple-boss structure, Magick Surge, and
  three Lucavi. Chapter 4 enemies may now support those engines with full broken-party synergy.
Boss-loot: six Tier-A plus the Tier-S best-of-best paid by the end of Mullonde (`052`-`053`);
  normal enemies may separately carry role-fitting non-buyable gear in Chapter 4 puzzle parties. The
  final gauntlet (`054`-`058`) is no-usable-reward challenge content; Excalibur stays with Orlandeau.
Next: data-layer patching + playtest in story order (the three chains as units; the gauntlet is the
  headline risk). This completes the New Game++ campaign design (Chapters 1-4, docs 000-059).
```

## Sources

- Local design docs: `037-chapter-4-overview.md`, `038-dugeura-pass.md` … `058-airship-graveyard.md`.
- Original-battle rosters cross-referenced from Game8 Chapter 4 battle walkthroughs (see each battle
  doc's Sources section; endgame page IDs 553225-553229).
- `010-chapter-1-balance-review.md`, `023-chapter-2-balance-review.md`, `036-chapter-3-balance-review.md`
  (the review template + ledgers this chapter extends and concludes).
```
