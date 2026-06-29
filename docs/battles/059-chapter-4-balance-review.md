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
- APEX CASTES & BOSSES: the SAMURAI debut (Necrohol), the Ultima-Demon caste (Limberry Keep on), apex
  MONSTERS (Hydra/Tiamat/Dark Behemoth), the vampire Ark Knight (Zalbaag), the triple-Templar last
  stand (Folmarv/Loffrey/Cletienne), the Magick-Surge sorcerer, THREE Lucavi (Zalera, Adrammelech, and
  the final Hashmal→Ultima), and named bosses paying out across the chapter.
- THREE NO-RESUPPLY CHAINS: Limberry (42-44), Mullonde (46-48), and the FIVE-battle ENDGAME GAUNTLET
  (49-53) — the longest sustained stretch in the game. Resource economy is a primary difficulty axis.
- TIER-S BEST-OF-BEST: the campaign's finest gear (Chaos Blade, Ribbon, Escutcheon, Robe of Lords,
  Materia Blade, Ragnarok) unlocks ONLY here, tiered onto the late bosses — the long-promised payoff.
```

## Difficulty curve (all 21 battles, as designed)

| # | Battle | Doc | Enemies | New demand / party engine | Terrain | Tier |
|---|--------|-----|---------|------------------------------|---------|------|
| 33 | Dugeura Pass | `038` | 6 (2 Black Mage + 2 **Dragoon** + Knight + Haste Time Mage) | open-field tempo (Haste); no boss | open field | ▃ moderate |
| 34 | Free City of Bervenia | `039` | 6 (**Meliadoul** + 2 Summoner + 2 Archer + Ninja; dies) | first Ch4 boss duel; equip-break; **Tier-A Save the Queen** | urban | ▅ hard |
| 35 | Finnath Creek | `040` | 5 (2 Black Choco + 2 Yellow Choco + Red) + Pig | de-randomized beast flock; no boss | creek | ▂ light |
| 36 | Outlying Church | `041` | 6 (**Zalmo** + 3 Knight + 2 Mystic; dies) | holy burst-duel; Rend cap 2; **Tier-A Light Robe** | church | ▄ moderate+ |
| 37 | Bed Desert | `042` | 6 (**Barich** + 2 Knight + 2 Archer + Black Mage; recurs) | open-desert gun-duel; **Tier-A Glacial Gun** | desert | ▄ moderate+ |
| 38 | Fort Besselat — Wall | `043` | 7 (branching S/N; mutually exclusive) | branching melee-vs-ranged approach; no boss | wall | ▃ moderate |
| 39 | Fort Besselat — Sluice | `044` | 7 (4 Knight + 2 Archer + Black Mage + Slow Time Mage) | floodgate-lever objective; Rend cap 2/4 | sluice | ▅ hard |
| 40 | Mount Germinas | `045` | 6 (2 **Ninja** + Thief + 3 Archer) | vertical skirmish; Invis-Cloak dig; no boss | mountain | ▄ moderate+ |
| 41 | Poeska's Lake | `046` | 6 (2 Revenant + 2 Archer + Mystic + Summoner) | all-undead reraise war; one-disruptor cap | frozen lake | ▅ hard |
| 42 | Limberry — Gate | `047` | 6 (Celia & Lettie **Assassins**, flee + 4 Reaver) | flee-on-critical race; Ultima tradeoff; chain 1/3; no rare | gate | ▃ moderate (race) |
| 43 | Limberry — Keep | `048` | (**Elmdore** Ark Knight; dies → Celia/Lettie transform to **Ultima Demons**) | parry-race; **Tier-A Masamune + Genji Armor**; chain 2/3 | keep | ▆ harder |
| 44 | Limberry — Undercroft | `049` | (**Zalera** Lucavi + undead guard) | mass-status Lucavi (constrained); **Tier-A Aegis Shield**; chain 3/3 | undercroft | █ SPIKE |
| 45 | Eagrose Castle | `050` | P1 5 Knight stair-wall → P2 **Dycedarg→Adrammelech** | 2-phase brother Lucavi; Rend cap 2/5; **Tier-A Grand Helm** | castle | █ SPIKE |
| 46 | Mullonde — Exterior | `051` | 6 (hidden roof **White Mage** + 2 Geomancer + 2 Orator + Summoner) | hidden-healer caster screen; split deploy; chain 1/3; no rare | cathedral ext | ▃ moderate |
| 47 | Mullonde — Nave | `052` | 3 (**Folmarv + Loffrey + Cletienne**; win when ONE falls) | triple-Templar equip-break race; **Tier-S Chaos Blade**; chain 2/3 | nave | ▅ hard |
| 48 | Mullonde — Sanctuary | `053` | (**Zalbaag** vampire Ark Knight + 2 Archaeodaemon + Ultima Demon; dies) | undead-brother; vampirism + break; **Tier-S Ribbon**; chain 3/3 | sanctuary | ▆ harder |
| 49 | Monastery Vaults — 4th | `054` | 6 (3 Knight Rend-cap 2 + 2 Monk + Ninja) | light gear-preservation opener; no rare; gauntlet 1/5 | vault | ▂ light (opener) |
| 50 | Monastery Vaults — 5th | `055` | 6 (**Loffrey** Divine Knight + 2 Black Mage + 2 Summoner + Time Mage) | caster crossfire; disarm-first; **Tier-S Escutcheon**; gauntlet 2/5 | wide vault | ▅ hard |
| 51 | Necrohol of Mullonde | `056` | 7 (**Cletienne** Magick Surge + 2 **Samurai** + 2 Ninja + 2 Time Mage) | **Samurai debut**; Silence/burst the surge; **Tier-S Robe of Lords**; gauntlet 3/5 | dead city | ▅ hard |
| 52 | Lost Halidom | `057` | 6 (**Barich** + 2 Hydra + Tiamat + Dark Behemoth + Chemist) | 5★ dragon pit; 3x-breath + control; **Tier-S Materia Blade**; gauntlet 4/5 | holy ground | █ 5★ PEAK |
| 53 | Airship Graveyard | `058` | P1 **Hashmal** → P2 **Ultima** (L106) + Ultima Demons | two-phase Lucavi FINALE; **capstone Tier-S Ragnarok**; gauntlet 5/5 | airship | █ FINALE |

Reading: Chapter 4 is a **long rising arc broken into three no-resupply chains, with two mid-chapter
Lucavi spikes and a five-fight gauntlet to the finale**. The open battles (33-41) escalate the elite
roster and pay out the **Tier-A** unlocks one boss at a time, with two valleys (Finnath 35, Besselat
Wall 38) for breath. The **Limberry chain (42-44)** climbs from a flee-race to the first Lucavi spike
(**Zalera**). **Eagrose (45)** is the second spike (the **Dycedarg→Adrammelech** brother duel). The
**Mullonde chain (46-48)** opens the **Tier-S** payouts (Chaos Blade, Ribbon) on the triple-Templar and
the undead brother. The **endgame gauntlet (49-53)** is the campaign's spine: a light opener, three
boss fights paying the remaining Tier-S, the **5★ Lost Halidom** peak, and the **two-phase finale**.

```text
The back five (the endgame gauntlet) in one line each:
  Vaults 4th    : a LIGHT gear-preservation opener — don't lose your blade to Rend before the marathon
  Vaults 5th    : cross a caster crossfire, disarm Loffrey, burst him            (disperse; Steal Weapon)
  Necrohol      : Silence/burst the Magick-Surge mage past a Samurai/Ninja screen (tempo; don't slow-chip)
  Lost Halidom  : the 5★ dragon pit — disable the beasts, break Barich's hold     (elemental resist; Arm Shot)
  Airship       : Hashmal, then Ultima — spread, re-buff, weather Almagest, end it (adapt; the capstone)
```

### Curve verdict

```text
PASS (on paper). The campaign's highest overall, capped by the apex levels (Ultima L106 — the single
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
Generics: 101-103 (endgame-tier).  Elite/sub-bosses: 103-104 (Samurai, Ultima Demons, Hydra).
Human bosses: 104-105 (Meliadoul, Zalmo, Barich, Elmdore, Folmarv/Loffrey/Cletienne, Zalbaag, Dycedarg).
LUCAVI: 105 (Zalera, Adrammelech, Hashmal).  FINAL ULTIMA: 106 — the single highest band in the mod (+6).
Apex monsters: Tiamat/Dark Behemoth 104, Hydra 103.

Boss-loot policy (Chapter 4): the long-promised payoff. Bosses that DIE carry ONE named rare highlight;
the chapter splits them into TIER-A (strong, on the open/Limberry/Eagrose bosses) and TIER-S best-of-best
(the finest gear in the game, held for the Mullonde + endgame bosses). This boss-highlight ledger is no
longer exclusive: per the global philosophy in `000`, Chapter 4 normal enemies may also carry role-fitting
non-buyable gear when it supports a readable broken-party puzzle. Bosses that FLEE carry no named rare
highlight (the drop is deferred to where they die). Ragnarok is the FINAL CAPSTONE on Ultima. EXCALIBUR
stays with Orlandeau (the player's holy blade) — never on an enemy.
```

## Design-exception log

| Exception | Where | Why | Guardrail |
|-----------|-------|-----|-----------|
| Time-Mage Haste/Slow/Float | Dugeura (`038`), Sluice (`044`), Vaults-5th (`055`), Necrohol (`056`) | canonical tempo casters | Haste/Slow/Float only — no Stop/Don't Act; one effective disruptor per fight |
| Templar/Knight equip-break (Mighty/Unyielding Blade, Rend) | Bervenia (`039`), Church (`041`), Sluice (`044`), Eagrose P1 (`050`), Nave (`052`), Sanctuary (`053`), Vaults-4th (`054`), Vaults-5th (`055`) | the break castes | telegraphed; Safeguard/Steal/Maintenance counter; **≤2 break sources/fight** (even with 4-5 Knights) |
| De-randomized beasts | Finnath (`040`) | reliable, learnable flock | fixed kits (Choco-Meteor/Cure); no status beasts; no boss |
| Healer/holy boss burst | Church (`041`) | Zalmo's revive/holy IS the puzzle | Silence/focus-burst answer; holy/soft-status only; he dies → Tier-A |
| Branching mutually-exclusive approach | Besselat Wall (`043`) | the fort's two routes | each route self-contained; no boss; both lead to the Sluice |
| Objective-race (floodgate lever) | Sluice (`044`) | the canonical flood mechanic | race vs clear-first; Rend capped 2/4 |
| Undead reraise + heal-weakness | Poeska (`046`), Sanctuary (`053`), Airship demons (`058`) | the undead/demon castes | PD/Holy/finish-while-down answers; one-disruptor cap; reraise is mechanic + counterplay |
| Assassin status / instant-death / flee-on-critical | Limberry Gate (`047`) | the named Assassins | RESISTABLE + non-spam; status-immunity tradeoff; flee makes the danger window short; no rare (flee) |
| Ark-Knight parry / Shirahadori | Limberry Keep (`048`) | Elmdore's identity | magic / Divine-Ruination answer; he dies → Tier-A Masamune+Genji |
| Lucavi mass-status (Zalera) | Undercroft (`049`) | the chapter's first Lucavi | ONE telegraphed source; resistable/cleansable/non-locking; Doom race-able |
| Lucavi summon-AoE (Adrammelech) | Eagrose P2 (`050`) | the 2nd-spike Lucavi | spread-or-die spaceable; Confuse/Stone resistable; 2-phase transform |
| Hidden-healer sustain | Mullonde Exterior (`051`) | the rooftop White Mage IS the puzzle | reach it (height-ignoring) / Silence; sustain not a lock; no boss → no rare |
| Win-on-one-boss-falls (triple Templar) | Nave (`052`) | the canonical "defeat one, others flee" | the other two retreat → no drop; equip-break capped 2 |
| Vampirism (Zalbaag) | Sanctuary (`053`) | the vampire Ark Knight | SOLE source; Holy Water/Japa Mala/Esuna; non-spreading; not a lock |
| Magick Surge (comeback mechanic) | Necrohol (`056`) | Cletienne's identity | Silence shuts it / burst beats it; magic-only retaliation; telegraphed, not a wipe |
| Samurai Draw Out (NEW caste) | Necrohol (`056`) | the chapter's Samurai debut | AoE/break race-able, spaceable; no hard lock |
| Dragon breath 3x/turn + Disable/Immobilize | Lost Halidom (`057`) | the 5★ dragon pit + control boss | breath ELEMENTAL/resistable + monsters disable-able; Barich status ONE resistable source (Ribbon) |
| Almagest / Dispelja / demon surround / 2nd form | Airship (`058`) | the Lucavi FINALE | Almagest telegraphed/sub-100%/survivable; Dispelja → re-buff; surround → Ribbon+spacing; transform telegraphed; full HP/MP restore between phases |

Hard control (Stop/Don't Act/Petrify spam) remains banned everywhere. Equip-break stays ≤2 sources/fight
across all break battles, even those fielding 4-5 Knights. Every Lucavi/finale ultimate is telegraphed
and sub-lethal by design — no scripted unavoidable wipe in the entire chapter.

## Job-escalation ledger (rule 1)

```text
Dugeura      (038) : Archer -> Haste Time Mage; open-field tempo            -> outpace the Haste, no ambush
Bervenia     (039) : first Ch4 Templar BOSS duel (Meliadoul; equip-break)   -> Safeguard/Steal, burst her
Finnath      (040) : de-randomized chocobo flock                            -> learnable beasts (light)
Church       (041) : holy burst-boss Zalmo + Rend Knights (cap 2)           -> Silence/burst; keep gear
Bed Desert   (042) : open-desert gun-duel Barich                            -> close the gap, disarm the gun
Besselat Wall(043) : branching melee(S) vs ranged(N) approach               -> pick a route, no boss
Besselat Slu.(044) : floodgate-lever race + Slow Time Mage (Rend cap 2/4)   -> race the lever or clear first
Mt Germinas  (045) : Thief -> 2nd Ninja; vertical skirmish                  -> climb/intercept; dig the Cloak
Poeska       (046) : all-undead reraise war + one disruptor                 -> permakill the dead (Holy/PD)
Limberry Gate(047) : ASSASSIN flee-race + Ultima tradeoff; chain 1/3        -> burst one to critical; no rare
Limberry Keep(048) : ELMDORE Ark Knight -> Celia/Lettie ULTIMA-DEMON debut; chain 2/3 -> answer parry; Tier-A
Limberry Und.(049) : ZALERA Lucavi (mass-status, constrained); chain 3/3    -> race the one status source
Eagrose      (050) : stair-wall Knights -> DYCEDARG->ADRAMMELECH 2-phase Lucavi -> spread vs summons
Mullonde Ext.(051) : hidden-roof White Mage sustain + caster screen; chain 1/3 -> kill the healer first
Mullonde Nave(052) : TRIPLE-TEMPLAR (Folmarv/Loffrey/Cletienne; one-falls); chain 2/3 -> commit to Folmarv
Mullonde San.(053) : ZALBAAG vampire Ark Knight + undead; chain 3/3         -> cleanse vampirism; holy the dead
Vaults 4th   (054) : Archer -> Ninja; LIGHT gear-preservation opener; gauntlet 1/5 -> keep your gear (Rend cap 2)
Vaults 5th   (055) : LOFFREY + caster crossfire; gauntlet 2/5              -> disperse, disarm, burst
Necrohol     (056) : SAMURAI DEBUT + Cletienne Magick Surge; gauntlet 3/5   -> Silence/burst the surge
Lost Halidom (057) : APEX MONSTER PIT (Hydra/Tiamat/Behemoth) + Barich; gauntlet 4/5 -> disable + elemental resist
Airship      (058) : HASHMAL -> ULTIMA two-phase FINALE (L106); gauntlet 5/5 -> spread, re-buff, end it

New content first seen in Chapter 4: the SAMURAI caste (056, canonical), the ULTIMA-DEMON caste (048),
APEX MONSTERS Hydra/Tiamat/Dark Behemoth (057), the vampire Ark Knight (053), the triple-boss "one
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

TIER-S (best-of-best; Mullonde + endgame bosses; the long-promised payoff):
  Folmarv     (052) : CHAOS BLADE     (dark Knight sword)   -> first Tier-S; the corrupted leader's blade.
  Zalbaag     (053) : RIBBON          (ultimate accessory)  -> the crown that wards the curse; enables 057's
                                                               status answers downstream.
  Loffrey     (055) : ESCUTCHEON      (best shield)         -> the Divine Knight's shield (ledger fit).
  Cletienne   (056) : ROBE OF LORDS   (best caster robe)    -> the Sorcerer's robe (ledger fit).
  Lost Halidom(057) : MATERIA BLADE   (enshrined relic)     -> recovered on victory (Barich wields no sword).
  Ultima      (058) : RAGNAROK        (legendary holy sword)-> the CAPSTONE; carries into the next NG++ cycle.

NO NAMED BOSS RARE (boss flees / no named boss -> deferred or none; normal enemies may still carry
role-fitting non-buyables under the Chapter 4 puzzle-party policy):
  Dugeura (038), Finnath (040), Besselat Wall (043), Sluice (044), Mt Germinas (045), Poeska (046),
  Limberry Gate (047, Celia/Lettie flee -> paid as Ultima Demons at 048), Mullonde Exterior (051),
  Vaults 4th (054).

LEDGER REASSIGNMENT (logged): the overview pencilled Robe of Lords onto Loffrey assuming he was a
caster; Game8 confirmed Loffrey is a DIVINE KNIGHT, so Tier-S was rebalanced to archetype — Escutcheon
(shield) -> Loffrey, Robe of Lords (robe) -> the actual caster Cletienne. Net Tier-S set unchanged.

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
  Revenant/undead, and apex monsters Hydra/Tiamat/Dark Behemoth.
Boss scripting to preserve (highest-risk patches):
  Meliadoul "defeat ends fight" (039); Zalmo/Barich death triggers (041/042); the Besselat Wall BRANCH
  (043); the Sluice LEVER objective (044); Celia/Lettie FLEE at Gate (047) then TRANSFORM to Ultima
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
  TIER-S: Chaos Blade (052), Ribbon (053), Escutcheon (055), Robe of Lords (056), Materia Blade (057),
    Ragnarok (058 capstone).
  Confirm Excalibur stays with Orlandeau (player) and is never placed on an enemy. Confirm Save the
  Queen is removed from Loffrey at 055 (kept singular to 039). Confirm Barich's Glacial Gun is the 042
  reward only (not re-dropped at 057).
No conflicts found on paper.
```

### Level bands & boss kits

```text
Consistent. Generics 101-103; elite/sub-bosses 103-104; human bosses 104-105; Lucavi 105; FINAL ULTIMA
106 (the mod's single highest, +6 — one above Ch3's Belias +5, the intended capstone escalation).
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
  Exterior (hidden-healer screen) -> Nave (triple-Templar; Tier-S Chaos Blade) -> Sanctuary (vampire
  Zalbaag; Tier-S Ribbon). Risk: two Tier-S land here; the RIBBON earned at 053 is the status answer the
  ENDGAME (esp. 057 Barich control + 058 demon surround) assumes — verify the player actually has it
  before the gauntlet. Test the chain as a unit.

CHAIN 3 — ENDGAME GAUNTLET (49-53 / 054-058), 5 battles, one loadout — THE LONGEST IN THE GAME:
  Vaults 4th (LIGHT opener, gear-preservation) -> Vaults 5th (Loffrey; Tier-S Escutcheon) -> Necrohol
  (Cletienne + Samurai; Tier-S Robe of Lords) -> Lost Halidom (5★ dragon pit; Tier-S Materia Blade) ->
  Airship (Hashmal->Ultima FINALE; capstone Ragnarok). Risk: the #1 balance problem of the mod — five
  consecutive fights, no merchant, rising to a 5★ peak and a two-phase finale. The light opener (054) is
  a deliberate resource on-ramp; the finale's full HP/MP restore between phases is the one mercy. VERIFY
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
4. **5★ Lost Halidom (057)**: confirm 3x-per-turn dragon breath is survivable with elemental resist +
   disabling the monsters (Arm Shot), and Barich's Disable/Immobilize is one resistable source (Ribbon).
5. **The FINALE (058)**: the most important fairness check — Almagest telegraphed/sub-100%/survivable;
   the demon surround broken by Ribbon + spacing; both Ultima forms beatable; the full HP/MP restore and
   second-form transform fire correctly. Ultima L106 must be hard but FAIR — no unavoidable wipe.
6. **Win-on-one-falls integrity (Nave 052)**: verify defeating ONE of the three Templars ends the fight
   and the other two RETREAT (so only the focused boss — Folmarv — drops the Chaos Blade).
7. **Break-pressure stacking** (≤2 sources across 039/041/044/050/052/053/054/055): confirm Safeguard/
   Steal stays a fair answer, never a mandatory tax, even in 4-5 Knight fights.
8. **Boss-as-rare-carrier feasibility** (Tier-S slots): if a boss can't hold/drop its Tier-S item, use
   the guaranteed-reward fallback (esp. Materia Blade as a halidom relic 057, Ragnarok as victory
   capstone 058). Confirm steals are possible where documented.
9. **Repeat-foe differentiation**: Barich (042 vs 057), Elmdore/Celia/Lettie (Ch3 Roof -> 047/048), and
   the three Templars (052 -> 055/056) must read as distinct stagings, not re-runs.
10. **Breather calibration** (Finnath 035→040, Besselat Wall 043, Mullonde Exterior 051, Vaults-4th
    054): confirm these feel lighter so the spikes land harder by contrast.
11. **Protect/guest & flee scripting**: Celia/Lettie flee (047) then return as Ultima Demons (048);
    confirm no rare leaks on the flee and the transform pays out correctly.
12. **Excalibur containment**: confirm Excalibur never appears on an enemy and stays Orlandeau's.

## Recommended implementation & playtest order

Implement in story order so the curve and the three chains can be felt as a player would:

```text
038 Dugeura -> 039 Bervenia -> 040 Finnath -> 041 Church -> 042 Bed Desert -> 043 Besselat Wall ->
044 Besselat Sluice -> 045 Mt Germinas -> 046 Poeska ->
[CHAIN: 047 Limberry Gate -> 048 Limberry Keep -> 049 Limberry Undercroft] -> 050 Eagrose ->
[CHAIN: 051 Mullonde Exterior -> 052 Mullonde Nave -> 053 Mullonde Sanctuary] ->
[GAUNTLET: 054 Vaults 4th -> 055 Vaults 5th -> 056 Necrohol -> 057 Lost Halidom -> 058 Airship Graveyard]
```

For each: dump the real entry, fill the doc's "Local Data Confirmed", apply levels + job-escalation
swaps + gear + (Tier-A/Tier-S) boss loot + skills, patch, diff-check inside the battle window only, then
test from a New Game+ save and record results. **Test the three chains as units** (no resupply) — they
are the chapter's defining balance problem, and the endgame gauntlet is the whole mod's hardest stretch.

## Status

```text
Design phase: COMPLETE for all 21 Chapter 4 battles (038-058 designed; none patched yet).
Consistency: audited; exceptions logged; job-escalation and split Tier-A/Tier-S ledgers extended.
Curve: passes on paper; the campaign's highest, capped by Ultima L106 and the three no-resupply chains;
  two Lucavi spikes + a 5★ peak + a two-phase finale; deliberate valleys seat the spikes.
Job escalation: one headline puzzle engine per fight; the Samurai caste debuts cleanly (canon), plus
  Ultima Demons, apex monsters, the vampire Ark Knight, the triple-boss structure, Magick Surge, and
  three Lucavi. Chapter 4 enemies may now support those engines with full broken-party synergy.
Boss-loot: six Tier-A + six Tier-S (best-of-best) tiered onto the late bosses as named highlights;
  normal enemies may separately carry role-fitting non-buyable gear in Chapter 4 puzzle parties. Flee
  bosses deferred; the Tier-S ledger rebalanced to archetype (Escutcheon->Loffrey, Robe of Lords->
  Cletienne); Ragnarok the final capstone (carries into NG++); Excalibur kept on Orlandeau.
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
