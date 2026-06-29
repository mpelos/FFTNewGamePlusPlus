# Chapter 1 — "The Meager": New Game++ Design Overview

This is the master plan for rescaling and redesigning every **Chapter 1** story battle of
*FINAL FANTASY TACTICS - The Ivalice Chronicles* (Enhanced v1.5.0) for New Game++.

Each battle gets its own design doc. This file holds the shared philosophy, the battle list,
the per-battle status table, and the design rules that keep every fight consistent.

## Naming note (Ivalice Chronicles / WotL retranslation)

The remaster uses the War of the Lions retranslation. Classic PSX names map as:

```text
Sweegy Woods      -> Siedge Weald
Dorter Trade City -> Dorter Slums
Sand Rat Cellar   -> Sand Rat Sietch
Death Corps       -> Corpse Brigade
Algus             -> Argath
Fort Zeakden      -> Ziekden Fortress
```

## Chapter 1 battle list

"Battle N" follows the in-game/Game8 numbering. Doc numbers are our own design order.

| Doc | Battle | Location | Role in story | Design status |
|-----|--------|----------|---------------|---------------|
| (skip) | 1 | Orbonne Monastery | Scripted tutorial | Out of scope — see below |
| `001` | 2 | Magick City of Gariland | First real fight; city street brawl | ✅ Implemented (final-shop v1) |
| `002` | 3 | Mandalia Plain | First monster + escort a reckless guest | ✅ Implemented (v1, entry 389) |
| `003` | 4 | Siedge Weald (Sweegy Woods) | Monster-pack woodland; Bombs | ✅ Implemented (v1, entry 384) |
| `004` | 5 | Dorter Slums | First difficulty spike; rooftop ranged+magic | ✅ Implemented (v1, entry 385) |
| `005` | 6 | Sand Rat Sietch | Cramped corridors; split-team melee attrition | ✅ Implemented (v1, entry 386) |
| `006` | 7 | Brigands' Den | Milleuda boss; rainy thieves + healers | ✅ Implemented (v1, entry 395) |
| `007` | 8 | Lenalian Plateau | Milleuda falls; mage-heavy field + Time Mage | ✅ Implemented (v1, entry 399) |
| `008` | 9 | Fovoham Windflats | Wiegraf duel; Judgment Blade spike | ✅ Implemented (v1, entry 400) |
| `009` | 10 | Ziekden Fortress | Chapter finale; Argath boss + hostage | ✅ Implemented (v1, entry 401) |

### ENTD entry map (Chapter 1) — solved 2026-06-20

Entries identified by exact roster matching against each battle's original composition (job IDs
decoded), then cross-checked against the OverrideEntryData layer; the code mod also logs the live
ENTD entry from the save (`resume_enbtl_main.sav` u16 @ 0x16C) for in-game confirmation.

```text
388 Gariland (confirmed in-game)   389 Mandalia (confirmed in-game)
384 Sweegy   385 Dorter   386 Sand Rat   395 Brigands' Den
399 Lenalia  400 Fovoham  401 Ziekden
```

Monster job ids: Chocobo 94-96, Goblin 97-99, Bomb 100-102, Panther 103-105. The OverrideEntryData
remaps Ch1 monster jobs at runtime (169=Red Panther, 170=Goblin, 171=Black Goblin, 172=Bomb,
173=Chocobo) but leaves Level/JobLevel = -1, so editing the base `.bin` level/joblevel still scales them.
| `010` | — | Chapter 1 Balance Review | Cross-battle curve + consistency audit | ✅ Done (all 10) |

**Battle count corrected:** Chapter 1 "The Meager" has **10 story battles**, not 7. The
Milleuda/Wiegraf (Corpse Brigade leaders) arc — Brigands' Den, Lenalian Plateau, Fovoham
Windflats — sits between Sand Rat (Battle 6) and the Ziekden finale (Battle 10). These three
were added in a backfill pass; Ziekden and the balance review were renumbered to `009`/`010`
to keep the docs in story order.

**Design status:** COMPLETE — `001` implemented and tested; `002`–`009` designed on paper.
The cross-battle audit (`010-chapter-1-balance-review.md`) covers all 10 battles. Remaining
work: identify each `BattleId`/ENTD entry on the Windows game files, patch, and playtest in
story order (see the review doc for the order and risks).

**Chapter boundary:** Chapter 1 "The Meager" ends at Ziekden Fortress (Battle 10), after which
Delita leaves the party. The next playable battle (Merchant City of Dorter, Battle 11) opens
Chapter 2 "The Manipulator and the Subservient" — covered in a separate Chapter 2 overview.

### Why Orbonne (Battle 1) is skipped

Battle 1 is the opening tutorial: a fixed, scripted teaching fight with forced moves and a
guaranteed outcome. It has no New Game+ replay value and scaling it would fight the tutorial
scripting. We leave it stock. If desired later, it can be revisited as an optional "tutorial
hard mode," but it is intentionally not part of the Chapter 1 rescale pass.

## Core scaling mechanic (recap)

Proven on Gariland. The enemy `Level` field uses the classic ENTD encoding:

```text
1-99 = fixed level
100  = party's highest level + 0
101  = party's highest level + 1   (etc.)
```

In TIC, the moddable layer is the NXD table **`OverrideEntryData`** (keyed by
`BattleId, UnitSlot`); it patches the base `battle_entd*_ent.bin` only for fields that are
set. Gariland was done directly in the `.bin` because its override rows left `Level=-1`.
For each new battle, confirm whether to patch via the `.bin` or via `OverrideEntryData`
once the BattleId and override rows are dumped on the Windows game data.

> ⚠️ Every new battle doc lists its **enemy data (BattleId / ENTD entry / slot offsets) as
> TBD** until dumped from the real game files on the Windows machine. These docs are the
> *design layer*; the byte-level patch is applied on the machine that has `extracted/`.

## Design philosophy

The mod's promise: **"story battles scale now."** Endgame New Game+ characters should no
longer trivialize Chapter 1. But Chapter 1 is the game's on-ramp, so the curve must rise
gently and each fight must still *feel like itself*.

### The six rules

1. **Preserve the battle's identity.** Keep the original's theme, enemy archetypes, terrain
   pressure, and "what this fight teaches." Gariland stays a street brawl; Dorter stays a
   rooftop-ranged wall; Siedge Weald stays a monster pack. We re-skin and re-tune, we do not
   replace the fantasy.

2. **Scale, don't escalate to boss tier.** Non-boss enemies sit at level `100` to `102`
   (party + 0..2). Leaders/uniques may go `+3`. Nothing in Chapter 1 should out-level the
   party by more than a few points.

3. **Final-shop gear, never superboss loot.** Enemies scale to an endgame party, so paper
   gear makes them irrelevant. Use strong gear that exists in shops or the loader's shop
   table. Forbidden: Genji set, Chaos Blade, Excalibur, Ragnarok, Save the Queen, and other
   unique steal/treasure rewards. Gear *flavor* follows the faction (academy cadets vs.
   Corpse Brigade deserters vs. monsters).

4. **Respect job equipment rules.** Generic enemy Squires don't wear shields/heavy armor;
   monsters wear nothing; mages use robes/rods. Builds must be legal for the job or they
   silently break.

5. **Keep the difficulty curve readable.** A returning player should feel the chapter ramp:
   Gariland (warm-up) < Mandalia (escort + first beast) < Siedge Weald (monster swarm) <
   Dorter (the wall) ≈ Sand Rat (attrition) < Brigands' Den (first named boss) <
   Lenalian (mage-heavy boss rematch) < Fovoham (Wiegraf spike) < Ziekden (finale). Add at
   most one new meaningful threat per fight; never bury the player in status/burst this early.

6. **Guests are controlled by the player in NG+.** From Chapter 1 onward, every active guest unit
   in a story battle must be player-controllable in New Game++: Delita, Argath, Boco, Ovelia,
   Mustadio, Agrias, Orran/Olan, Alma, Rapha, and any later temporary ally. This applies whether
   the battle objective says to save them, merely includes them as allied help, or uses them for
   story texture. Guest AI is not a skill test.

### Guest policy: player controls every guest from Chapter 1

Guest units can add story texture, extra board presence, or a reason for the enemy to be arranged
in a certain way, but their AI must never be the main difficulty lever. A player should not lose
because Delita, Argath, Boco, Ovelia, Mustadio, Agrias, Orran/Olan, Alma, Rapha, or any other guest
made a bad AI decision before the player had a reasonable chance to respond.

From Chapter 1 onward, in New Game++:

```text
- Every active guest in every story battle must be controllable by the player, whether or not that
  guest is a loss-condition target.
- Do not frame "the guest AI must survive itself" as the build check. If a vanilla objective asks
  the player to save a guest, the challenge is the enemy plan around that guest, not the guest's AI.
- If a guest death is a loss condition, the mod must scale/gear/position that guest so the player
  loses only after misplaying or ignoring the board, not after one foolish AI move.
- Prefer to make the real challenge the enemy plan around the guest fight: betrayal, terrain,
  caster priority, flank control, disarm, undead/permakill, or boss mechanics.
- Battle docs must record guest-control handling alongside scaling, gear, and placement. Named
  guests can use the shared guest-control rule; ambiguous units such as Boco must be targeted by
  battle/slot or a similarly safe identifier instead of a broad monster charId rule.
```

### Chapter 2+ challenge philosophy: tuned players, not first clears

Chapter 1 is intentionally a New Game+ presentation chapter. It proves the promise ("story
battles scale now"), introduces stronger enemy gear, and gives the player room to enjoy an
overpowered post-game party without immediately forcing a meta response. Starting in Chapter 2,
that changes: the player is assumed to be not merely high-level, but **tuned**.

For Chapter 2 onward, design against a player who may bring several of these solved tools:

```text
- high Brave reactions and high/managed Faith casters
- Auto-Potion with X-Potions, Item, Throw Item, Phoenix Down, Remedy, and Esuna coverage
- Safeguard/Maintenance/Reequip against Rend and steal pressure
- Ninja Speed, Dual Wield, Brawler/Monk burst, high-mobility finishers
- Shirahadori/Blade Grasp, Reflexes, Featherweave/Aegis-style evasion stacks
- Arithmeticks/Holy setups, Chameleon Robe or other elemental absorption plans
- Swiftspell/Summon or high-MA Black/White Mage cores
- special-character power, especially Orlandeau-style sword-skill pressure later
```

The design consequence is important: **"one headline demand per fight" does not mean "change
only one small thing."** Against NG+ builds, a single slot swap or small level bump often changes
nothing. From Chapter 2 onward, each battle still needs one readable tactical identity, but the
whole enemy side may be built to support it: legal gear, meaningful reactions/support/move skills,
threat placement, target priority, and reward bait all point at the same problem.

Research basis:

```text
- FFT difficulty is action-economy difficulty. CT reaches turns at 100, and Speed controls how
  often a unit acts, so Haste/Slow, Ninja Speed, Jump timing, Throw, and charge times are core
  levers, not minor flavor.
- Brave/Faith are build axes, not cosmetic stats. Brave changes reaction and several damage
  formulas; Faith changes magic risk/reward. Optimized parties will manage them.
- Modern player advice consistently identifies Item/Throw Item, Auto-Potion, Dual Wield,
  Shirahadori, Swiftspell, Equip Guns, Arithmeticks/Holy, elemental absorption, and Safeguard as
  high-value tools. The mod should assume players know these tools by Chapter 2+.
- FFT difficulty mods show the useful target and the failure case: match the depth of FFT's
  customization, but avoid the "every fight is stacked against you" trap where scaling and hidden
  counters feel unfair instead of tactical.
```

#### What makes FFT harder without making it cheap

Use these levers before raising level offsets:

| Lever | Fair use | Cheap use to avoid |
|-------|----------|--------------------|
| Action economy | More credible threats, Haste/Slow tempo, fast flankers, turn-order races | giving every enemy overwhelming speed or instant actions |
| Threat diversity | Mix physical, magic, status, break, undead, and terrain pressure around one plan | random grab-bag kits with no battle identity |
| Terrain and deployment | High ground, split starts, chokepoints, rivers, rooftops, soft terrain | trapping the player before they can act |
| Objectives | Route around NPC pressure, reach a healer/caster, lever race, flee-on-critical race | objectives that fail before the player can respond |
| Resource economy | No-resupply chains, item pressure, revive/cleanse tax | draining inventories through chip spam |
| Rewards as pressure | Rare gear on bosses as steal/disarm bait | hiding best gear on throwaway generics or making steal mandatory |
| Status/control | One visible disruptor, resistable/cleansable status, clear priority targets | Stop/Don't Act/Petrify spam or party-wide locks |

#### Chapter-by-chapter challenge ramp

| Chapter | Challenge role | Player assumption | Encounter policy |
|---------|----------------|-------------------|------------------|
| Chapter 1 | Presentation and proof of scaling | Endgame party, not yet asked to solve meta checks | Light counters only; keep battles recognizable and readable |
| Chapter 2 | Preview of real NG+ checks | Player has survivability, Items, good reactions, and at least one burst plan | Less puzzle; every active human has full equipment and R/S/M setup; secondary is optional |
| Chapter 3 | Complete synergistic parties | Player has optimized cores: Ninja/Dual Wield, strong casters, high Brave/Faith, and chain prep | Every active human enemy gets full equipment and full setup including secondary; parties have good synergy, but are not "broken" yet |
| Chapter 4 | Broken puzzle parties | Player may have the builds people call "best in the game" plus mod-paid rare gear | Enemy parties can use broken combos, non-buyable gear on normal enemies, and puzzle-like synergy; every spike must still be readable |

#### Operational tuning rules: how the philosophy becomes battle data

Do not solve the mod by blindly giving every enemy a full perfect build. FFT power comes from
stacked systems, so enemy power must also be staged system-by-system. The practical knobs are:

```text
1. Gear tier and legality
2. Ability-slot completeness (action / reaction / support / movement)
3. Enemy Speed, CT pressure, Haste/Slow, and charge-time pressure
4. Brave/Faith tuning for reactions, magic risk, and caster payoff
5. Composition roles: anchor, diver, artillery, support, disruptor, thief/breaker, boss
6. Terrain/placement: who starts in range, who threatens high ground, who blocks routes
7. Reward pressure: rare gear as steal/disarm bait, not just a post-battle trophy
```

#### Enemy party construction: preserve the battle's spirit, not its job tier

Starting in Chapter 2, job tier is no longer a progression lock. Any normal FFT job may appear if it
translates the original battle's spirit into a higher-skill New Game+ version. The only global bans
are **Mime** and **Calculator/Arithmetician** before Chapter 4 puzzle design explicitly calls for
them; those jobs are encounter engines, not ordinary roster upgrades.

Before choosing jobs, read the vanilla battle as a designer:

```text
1. What difficulty level did the original designers intend here: warm-up, spike, breather, boss,
   attrition, race, puzzle, duel, finale?
2. What feeling did the battle try to create: ambush, high-ground pressure, being surrounded,
   saving time, crossing a kill zone, fear of undead, caster priority, betrayal, disarm, demon panic?
3. What was the original tactical lesson: spread out, climb, kill the healer, interrupt the caster,
   protect gear, finish undead, burst the boss, survive a chain?
4. What must remain recognizable after the NG++ upgrade?
```

Then build the enemy party around roles, not vanilla job loyalty:

```text
- Anchor: holds terrain, protects a route, carries Safeguard/evasion/tank gear.
- Diver: threatens backline or isolated units through Move/Jump/Teleport/Jump/Throw.
- Artillery: ranged physical, gun, bow, summon, black magic, Iaido, or monster breath.
- Support: Haste/Shell/Protect/heal/Raise/Esuna/Math support in later chapters.
- Disruptor: status, charm, Silence, Slow, break, steal, undead pressure.
- Breaker/thief: attacks gear, rare items, or the player's build assumptions.
- Boss/engine: the unit or combo the battle is really about.
```

Add enemies when it strengthens the intended feeling. Extra units are good when they create action
economy, flanks, bodyguards, target priority, or a route puzzle; they are bad when they only add HP
cleanup after the battle is solved. More enemies should also respect scripting, deployment size, and
readability: a crowded map with no clear target priority is not harder in the FFT sense, just noisy.

Chapter progression for party construction:

| Chapter | Enemy party rule | Job freedom | Enemy count policy |
|---------|------------------|-------------|--------------------|
| Chapter 2 | Stronger parties that preview advanced systems; every active human has full equipment and complete R/S/M | Any job tier except Mime/Calculator if it fits the battle spirit | Add 1-2 enemies if it sharpens the original feeling; do not create dense puzzle teams yet |
| Chapter 3 | Complete synergistic parties; every human enemy has a full build including secondary | Any job tier except Mime/Calculator; advanced jobs are normal tools now | Add enemies freely when needed for flanks, chains, bodyguards, or action economy |
| Chapter 4 | Broken puzzle parties with a headline engine and team combo | All fitting jobs and rare gear allowed; Calculator/Mime only as explicit puzzle engines | Use full enemy teams when the map can carry them; every extra unit must serve the puzzle |

The conversion rule is: **same emotional job, higher tactical grammar**. A vanilla Archer can become
a gunner, Geomancer, Ninja thrower, Dragoon, or Time-supported sniper if the original point was range,
height, or pressure. A vanilla Knight can become a Templar, breaker, evasion wall, Mana-Shield anchor,
or rare-gear bait if the original point was a front line. A vanilla mage can become a Summoner, Iaido
mage, Time engine, Mystic disruptor, or Black Mage nuke if the original point was caster priority.

Use ability slots as a visible power budget:

| Chapter | Generic enemies | Advanced/elite generics | Bosses |
|---------|-----------------|-------------------------|--------|
| Chapter 2 | Full legal gear; reaction/support/movement set; secondary optional | Advanced enemies also get full gear and R/S/M; secondary only when it clarifies the role | Bosses get full gear, R/S/M, usually secondary, one rare/highlight item, clear counter |
| Chapter 3 | Full legal gear and full slots: secondary, reaction, support, movement | Complete coherent kits, role-specific accessory, good party synergy | Full slots; mid-high rare; boss mechanic plus counter |
| Chapter 4 | Full kits; non-buyable gear may appear on normal enemies when it serves the puzzle | Broken combo pieces are allowed; elite generics can mirror player-quality builds | Full broken-but-readable kits; Tier-A/Tier-S loot; boss spike must stay answerable |

Examples of the ramp:

```text
Chapter 2:
- Give every active human full equipment plus reaction/support/movement; secondary is optional
  when the primary job already expresses the unit's role.
- Give a Summoner real summon pressure, but do not also build the whole escort as a synergy puzzle.
- Give Order Knights Rend or Safeguard-relevant gear pressure, but cap break sources.
- Give casters good rods/robes and R/S/M that support their job; secondary only if it teaches the knob.
- Give monsters/undead their natural mechanic plus placement, not artificial equipment.
- Treat Chapter 2 as the preview chapter for Chapter 3 systems: less puzzle, more "learn the knob."

Chapter 3:
- Every active human enemy gets complete equipment and a complete ability setup: secondary,
  reaction, support, and movement. Chapter 3 makes secondary mandatory. No leveled shells.
- The setup should be synergistic but not abusive: mobility on divers, Concentration on snipers,
  Arcane Strength/Magic Boost on casters, Maintenance/Safeguard on gear anchors.
- Start using accessories and elemental gear as puzzle pieces: Reflect Mail, Flame Shield,
  Defense Ring, Aegis-style magic evasion, status protection where it creates a readable plan.
- No-resupply chains become real: each fight may tax HP/MP/items/status recovery, but cannot
  quietly consume everything before the next battle.

Chapter 4:
- Enemy parties may become "broken" on purpose: not just strong individuals, but a whole team
  combo that creates a puzzle.
- Normal enemies may carry non-buyable equipment as normal Chapter 4 loadout, not only bosses.
- Bosses carry the best gear as threat + reward, and the gear should matter in the fight.
- The best player strategies are pressured by map design, mixed threat types, and target priority,
  not by blanket immunity.
- Full kits are allowed; unreadable pile-ups are not. If a boss is the headline, the adds should
  amplify that boss instead of introducing a second unrelated headline.
```

#### Broken setup catalog: ingredients for Chapter 4 puzzles

This catalog is the source list for battle-by-battle Chapter 4 design. A "broken" setup is not just
one strong item; it is a stack of FFT systems that multiply each other. Chapter 3 can preview pieces
of these stacks with complete, synergistic-but-fair kits. Chapter 4 may combine them into enemy
party puzzles.

Rules for using the catalog:

```text
- Chapter 2: use one ingredient at a time as a preview.
- Chapter 3: use complete setups with good synergy, but avoid full broken stacks.
- Chapter 4: use full broken stacks and non-buyable gear on normal enemies, but make the engine
  visible enough that the player can identify and dismantle it.
- Never use hidden Zodiac compatibility, invisible stat inflation, or blanket immunity as the
  main answer. If the puzzle cannot be read from jobs, gear, placement, or first turns, revise it.
```

| Broken setup family | Ingredients | Why it is broken | Enemy-side puzzle use |
|---------------------|-------------|------------------|-----------------------|
| Arithmeticks/Holy battery | Arithmeticks, Holy/Flare/Death/Raise/Haste/Stop, Chameleon Robe or holy absorption, varied ally setup | Instant, no-MP, board-wide targeting can damage enemies while healing prepared allies | Cap4 only as a puzzle engine; vary levels/heights/CT so the player can counter by killing/silencing/displacing the engine |
| Calculator support web | Math Cure/Raise/Haste/Esuna plus protected allies | Turns one caster into board-wide sustain and tempo | Use behind bodyguards; the answer is priority kill, Silence, Faith pressure, or terrain reach |
| High-Brave Shirahadori wall | 90+ Brave, Shirahadori/Blade Grasp, physical frontliner or boss | Turns many physical attacks into misses | Pair with magic-vulnerable allies; answer with magic, status, rear attacks, unevadable skills, or disarm |
| Reflexes/Abandon evasion stack | Reflexes/Abandon, Aegis/Escutcheon, cloak, shield, high C-Ev job | Physical and magic evasion stack into a fake-invincible target | Use as a puzzle wall, not every enemy; answer with unevadable, status, flank/rear, or target bypass |
| Auto-Potion tank | Auto-Potion, X-Potion stock, high HP/armor | Converts chip damage into sustain and punishes weak attacks | Use on anchors; answer with burst, status, MP/CT pressure, or kill support first |
| Mana Shield battery | Mana Shield/MP Switch, Manafont/Move-MP Up, high MP gear | Survives lethal hits by converting damage into MP loss, then regenerates MP by moving | Cap4 tank puzzle; answer with MP pressure, Immobilize, burst after MP break, or status |
| Reraise perfume loop | Chantage/Angel Ring/Reraise, Ribbon/status immunity, healer nearby | Death is not a clean answer until the loop source is removed | Use sparingly on normal enemies in Cap4; answer with steal/break accessory, status if no Ribbon, or repeated kill under pressure |
| Ribbon immunity carrier | Ribbon plus high-value role unit | Deletes broad status answers and frees the unit to run a risky role | Cap4 normal enemies may carry it; do not put Ribbon on every key target |
| Dual Wield burst | Ninja or Dual Wield support, high PA, Bracer/Twist Headband, strong weapons | Two damage packets can erase units before recovery matters | Use as diver/assassin; answer with spacing, Protect, reaction punish, status, or body-blocking |
| Dual Wield Rend | Knight/Templar with Rend plus Dual Wield or two-hit access | Doubles break attempts and can dismantle gear-based builds | Cap4 puzzle only unless tightly capped; answer with Safeguard/Maintenance, Steal/Rend Weapon, or kill the breaker |
| Equip Gun Rend/Snipe | Equip Guns or Machinist/Gunner kit plus Rend/Snipe/status | Applies break/status from safe range | Use on maps with line-of-sight counterplay; answer by blocking shots, closing range, or disarming |
| Concentration thief/breaker | Concentration, Steal/Rend/Throw/aimed status | Removes evasion from the steal/break plan | Use as a named elite role; answer by disabling the specialist or protecting key gear |
| Ninja Throw battery | Ninja Speed, Throw, high-level rare throwables, Move+2/3/Teleport | Fast ranged burst from unexpected angles | Cap3 preview with normal gear; Cap4 can throw rare weapons if the battle is designed around it |
| Hasted Dragoon dive | Dragoon, Jump, Haste, spear, vertical map | Forces movement under delayed burst and threatens backliners | Cap3 fair elite; Cap4 add bodyguards/Slow Dance support for puzzle pressure |
| Monk/Brawler boss-killer | Brawler, Martial Arts/Monk skills, high PA, Dual Wield or Attack Boost | No-MP sustain, revive, Chakra, and burst in one kit | Use as bruiser support; answer with range, magic, status, or CT control |
| Black Mage nuke core | High Faith, MA gear, Arcane Strength/Magic Boost, strong spells, Swiftspell/Short Charge | Converts one cast window into lethal AoE | Pair with Time Mage or bodyguards; answer with Silence, Shell, spread, dive, or Faith manipulation |
| Summoner bomb | Summoner, high MA, Swiftspell/Short Charge, bodyguards, Haste | Large AoE with friendly-fire safety | Use as priority target; answer by interrupting, spreading, Silence, or killing the haste source |
| Iaido/Draw Out mage | Samurai skillset on high-MA job, MA gear, Arcane Strength/Magic Boost | Faith-independent AoE damage/heal/buff from a caster shell | Cap3 preview; Cap4 puzzle with katanas/rare gear as steal-bait |
| Magic-gun caster | Magic gun, high range, Faith-aware target selection, elemental support | Gun user becomes ranged spell pressure without normal cast time | Use with elemental shields/absorbs; answer with line-of-sight, Faith, or disarm |
| Elemental absorption team | Flame/Ice/Thunder/Holy absorb gear, matching allied AoE, Chameleon Robe/Excalibur-style healing | The party turns friendly fire into healing | Cap4 puzzle: player must notice absorb gear and change damage type or remove the engine |
| Bard/Dancer board control | Slow Dance, Nameless Song, Rousing Melody/Battle Chant/Magickal Refrain | Global buffs/debuffs scale with time and punish slow play | Use one performer as engine; answer by rushing, Silence, or forcing movement |
| Time Mage tempo engine | Haste/Slow/Quick/Float, fast support, protected caster | Changes the action economy without raw stat inflation | Cap2 preview, Cap3 standard synergy, Cap4 protected engine |
| Mystic/Orator disable web | Sleep, Silence, Don't Act, Charm, Berserk, Invitation-adjacent effects | Removes turns or makes AI/player positioning collapse | One visible disruptor unless the whole fight is the status puzzle; never hidden lock spam |
| Undead sustain knot | Undead reraise, healer/caster support, Time Mage tempo, terrain | Killing is not enough; bodies must be finished/permakilled | Use with living threats so Phoenix Down is not the only answer |
| Chocobo tempo flock | Choco Cure, Choco Meteor, fast movement, mixed colors | Fast monsters heal and snipe while ignoring gear rules | Good Cap4 light puzzle or Cap3 preview; answer with focus fire and anti-monster tools |
| Dragon/monster pit | Hydra/Tiamat/Behemoth breath, elemental gear, Disable/Immobilize support | Huge HP plus repeated AoE/line breath stresses positioning | Cap4 peak puzzle; answer with elemental resist, status, break support, or boss-race objective |
| Mime copy engine | Mime behind strong ally actions, protected positioning | Multiplies the best action without spending normal build slots | Cap4-only if data supports it; keep visible and avoid excessive copies |
| Special sword-skill tyrant | Holy/Mighty/Dark sword skills, rare sword, high PA/Speed, support caster | Range, damage, status/break, and no charge time in one boss package | Boss/elite centerpiece; answer with disarm, steal, status, spread, or terrain |
| Low-Faith anti-mage | Very low Faith, physical role, Item support | Shrugs off magic while still receiving item healing | Use as anti-caster flankers; answer with physical, Rend, items, or Faith-independent damage |
| High-Faith glass cannon | Very high Faith, MA gear, magic offense | Damage and status scale both ways: more output, more incoming magic risk | Use as dangerous but burstable caster; answer with magic retaliation, Silence, or dive |
| Max-stat / delevel fantasy | Level-down/up stat optimization, best growth jobs | Can make any unit absurd before equipment is counted | Do not simulate directly with invisible stats; express it through visible gear/abilities instead |

#### Broken party puzzle templates

Use these as battle-level patterns in Chapter 4. Each template should have one engine, two to four
supporting roles, and at least two fair answers.

| Template | Enemy package | Puzzle question |
|----------|---------------|-----------------|
| Holy algorithm cell | Arithmeticks engine + holy-absorbing allies + physical bodyguards | Can the player identify the algorithm engine and stop it before it turns the board into healing/damage? |
| Break-and-burst squad | Dual Wield/Rend or gun-Rend breaker + Ninja/Monk finisher + Time Mage | Can the player protect key gear while killing the finisher or disarming the breaker? |
| Evasion palace | Shirahadori/Reflexes anchor + magic/status backline + objective pressure | Can the player stop attacking the wall and solve the backline/unevadable route? |
| Reraise perfume court | Chantage/Ribbon carrier + healer + bodyguards + thief/break bait | Can the player remove the loop source instead of wasting turns on repeated kills? |
| Mana-shield phalanx | Mana Shield tanks + Move-MP Up + protected casters | Can the player pin, drain, or burst after MP breaks instead of feeding the battery? |
| Haste assassination net | Time Mage + Hasted Ninjas/Dragoons + ranged support | Can the player kill or silence the tempo engine before the divers double-turn the backline? |
| Iaido storm | High-MA Iaido unit + Protect/Shell support + stealable katana bait | Can the player interrupt the AoE engine or steal the katana without overcommitting? |
| Undead machine | Undead front + Time support + living mage/healer | Can the player permakill the undead while also reaching the living engine? |
| Monster cathedral | Hydra/Tiamat/Behemoth line threats + status gunner/caster | Can the player solve positioning and disable the monsters before breath tempo overwhelms them? |

#### Best-build pressure matrix

Chapter 2 starts introducing these answers gently. Chapter 3 uses them as real checks. Chapter 4
is allowed to combine them with boss-spike mechanics, as long as the fight still has one headline
read.

| Player power | Fair pressure | Guardrail |
|--------------|---------------|-----------|
| Shirahadori / Reflex physical evasion | magic, status, unevadable boss skills, objective pressure, flanks | do not make every enemy ignore evasion |
| Auto-Potion / X-Potion | status, burst thresholds, MP pressure, revive/cleanse tax, no-resupply chains | do not use endless chip just to burn 99 items |
| Dual Wield / Ninja / Monk burst | spacing, Protect, counter-frontliners, bodyguards, terrain, target priority | do not solve it with pure HP inflation |
| Arithmeticks / Holy | varied level/height/CT, elemental absorption, spread enemies, priority threats that act before setup | do not blanket-ban magic or make all enemies immune |
| High-Faith casters | Silence, Shell, fast divers, line-of-sight/range pressure, Faith risk on incoming magic | do not hard-lock the caster for the whole fight |
| Item / Throw Item / Phoenix Down | mixed undead and living threats, protected undead casters, distance and verticality | do not disable inventory or make PD the only solution |
| Safeguard / Maintenance | capped, visible break sources with valuable gear at stake | do not make Safeguard a mandatory tax on every map |
| Orlandeau / special sword skills | split threats, bosses that require disarm/steal/status/positioning, targets outside one AoE pattern | do not hard-counter the character; make the battle bigger than one swing |

#### Battle-doc requirement from Chapter 2 onward

Every Chapter 2+ battle doc should be able to answer these questions:

```text
1. What was the vanilla battle's intended difficulty level and feeling?
2. What original tactical lesson or emotional beat must survive the NG++ upgrade?
3. What enemy party roles express that feeling now: anchor, diver, artillery, support, disruptor,
   breaker/thief, boss/engine?
4. What tuned-player build or habit does this fight test?
5. What is the fight's one headline demand?
6. If jobs were upgraded or extra enemies were added, why do they sharpen the original feeling?
7. What are at least two fair answers available to a prepared NG+ party?
8. Which player meta is intentionally NOT countered here, to keep the fight from becoming a pile-up?
9. If the battle is in a no-resupply chain, what resource is it allowed to tax before the next fight?
10. What would make the fight feel cheap, and is that explicitly banned in the doc?
```

The preferred failure lesson is tactical, not punitive: "I ignored the Time Mage," "I clumped into
the Summoner," "I entered the chain without cleanse," "I let the Templar keep the break weapon,"
"I tried to solve an undead fight with only physical burst." A loss should explain the fight; it
should not imply the player needed blind immunity, a hidden rule, or more grinding.

### Difficulty budget per battle

| Battle | Target feel | Level band | Allowed new threat |
|--------|-------------|------------|--------------------|
| Gariland | Warm-up, fast | 100–102 | one ranged unit |
| Mandalia | Escort tension | 100–102 | ranged pressure on the guest + keep the beast |
| Siedge Weald | Swarm management | 100–101 | extra monster, Bomb self-destruct threat |
| Dorter | The spike / the wall | 100–102 | real elevation + ranged + one mage |
| Sand Rat | Grind / corridor attrition | 100–102 | mixed melee+caster behind a chokepoint |
| Brigands' Den | First named boss; healers prolong | boss +2, adds 100–101 | Milleuda as a boss; White-Mage sustain; rain (Thunder) |
| Lenalian | Boss rematch, mage-heavy | boss +2, adds 100–102 | stacked Black Mages + first Time Mage (Haste/Slow) |
| Fovoham | Wiegraf spike | boss +3, adds 100–102 | Wiegraf's Judgment Blade + hard-hitting Monks |
| Ziekden | Climactic boss fight | boss +3, adds 100–102 | Argath as a genuine boss; protect the hostage beat |

### Things to avoid chapter-wide

```text
Black Mage burst stacking before Dorter
Time Mage control (Stop/Don't Move) anywhere in Chapter 1
Heavy status spam (Petrify, Charm, Death) on generics
More than one true caster per fight before Dorter
Boss-tier level offsets on generic units
Unique/superboss equipment
```

## Workflow for each battle (design -> implement)

1. Read this overview + the battle's own doc.
2. On the Windows machine, identify the battle's `BattleId` / ENTD entry (cross-reference
   `SortieConfirm`, `EventId`, `Map`, scenario tables; sanity-check with FFTIvaliceEditor).
3. Dump the entry with `tools/entd_tool.py` (or the `OverrideEntryData` rows) and confirm
   the original slot layout matches the doc's "Original Battle" section.
4. Apply the doc's New Game++ composition: levels, jobs, gear, skills, placement, and guest-control
   flags for every active guest.
5. Patch via the appropriate layer (`.bin` or `OverrideEntryData`), keeping the diff minimal
   and inside the target battle's window.
6. Copy into the mod, install to Reloaded-II, test from a New Game+ save.
7. Record results and tuning notes back in the battle doc.

## Sources

- Game8, "Chapter 1: The Meager Walkthrough":
  https://game8.co/games/Final-Fantasy-Tactics/archives/543067
- StrategyWiki, FFT Chapter 1 battle pages:
  https://strategywiki.org/wiki/Final_Fantasy_Tactics
- Caves of Narshe FFT battle walkthrough (per-battle rosters):
  https://www.cavesofnarshe.com/fft/walkthrough.php
- FFHacktics ENTD reference: https://ffhacktics.com/wiki/ENTD
- AeroStar, "Final Fantasy Tactics Battle Mechanics Guide" (CT, Speed, formulas):
  https://gamefaqs.gamespot.com/ps/197339-final-fantasy-tactics/faqs/3876
- AstrologistOlan19, "Final Fantasy Tactics Brave/Faith FAQ":
  https://gamefaqs.gamespot.com/ps/197339-final-fantasy-tactics/faqs/15053
- Atom_Edge, "Final Fantasy Tactics Character Setups Guide":
  https://gamefaqs.gamespot.com/ps/197339-final-fantasy-tactics/faqs/6991
- Leviatan, "Final Fantasy Tactics Calculator FAQ":
  https://gamefaqs.gamespot.com/ps/197339-final-fantasy-tactics/faqs/3877
- Steam Community, "FFT Basic Mechanic and Job guide" (job growth, Items, Safeguard, Arithmeticks):
  https://steamcommunity.com/sharedfiles/filedetails/?id=3581203978
- Kotaku, "Final Fantasy Tactics Ivalice Chronicles Guide: 15 Best Abilities To Unlock":
  https://kotaku.com/final-fantasy-tactics-best-abilities-guide-ivalice-chronicles-2000631130
- Something Awful, "Let's Play Final Fantasy Tactics 1.3" (difficulty-mod framing and cautionary notes):
  https://forums.somethingawful.com/showthread.php?threadid=3520559
- Local: `docs/battles/001-gariland.md`, `notes/01-encounter-data-and-gariland.md`
</content>
</invoke>
