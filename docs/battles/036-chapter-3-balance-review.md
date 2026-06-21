# 036 - Chapter 3 Balance Review

A cross-battle audit of all **11** Chapter 3 New Game++ designs (`025`–`035`). It checks the
difficulty curve, verifies consistency of level bands / gear / job-skill IDs, logs the deliberate
design exceptions, and carries the **job-escalation ledger** and **rare-boss-loot ledger** forward
from Chapter 2. Then it flags the open risks (chiefly the two no-resupply chains and the solo-duel)
and gives a recommended playtest order. This is a paper review — every finding must be re-validated
in-game once each battle is patched on the Windows data.

## The central balancing insight (carried from Chapters 1–2)

Enemies are still scaled `Level = 100 + offset`, so the offset is fine-tuning, not the main lever.
Difficulty comes from composition, terrain, mechanics, the new job each fight, and the bosses.
Chapter 3 turns the roster **elite** and adds two structural pressures:

```text
- ELITE CASTES: Knights Templar (break-from-range), enemy Dragoons (Hasted Jump), the NINJA
  (wall-climb / Throw), the second LUCAVI (Belias/Velius), and named ASSASSINS (teleport + death).
- NO-RESUPPLY CHAINS: two three-battle gauntlets on one loadout — the Orbonne Vaults (24-26) and
  Riovanes (30-32) — so RESOURCE ECONOMY becomes a difficulty axis of its own.
```

## Difficulty curve (all 11 battles, as designed)

| # | Battle | Doc | Enemies | New demand / job escalation | Terrain | Tier |
|---|--------|-----|---------|------------------------------|---------|------|
| 22 | Mining Town of Gollund | `025` | 6 (3 Thief + 2 Chemist + **Orator**) | protect Orran; charm/steal denial band | rooftops | ▃ moderate |
| 23 | Lesalia Postern | `026` | 6 (**Zalmo** + 3 Knight + 2 Monk; flees) | reviving Inquisitor + Flame-Shield/Thunder | stair gate | ▄ moderate+ |
| 24 | Vaults — 2nd | `027` | 6 (3 **Dragoon** + 2 Time Mage + Chemist) | enemy Dragoon (Hasted Jump); chain 1/3 | vault | ▅ hard |
| 25 | Vaults — 3rd | `028` | 6 (**Izlude** + 2 Knight + 2 Archer + Summoner) | **Templar** debut + Reflect Mail; elevation; chain 2/3 | shelves | ▅+ hard |
| 26 | Vaults — 1st | `029` | 6 (**Wiegraf** + 2 Knight + 2 Archer + Black Mage; flees) | 5-doorway chokepoint + disarm; chain 3/3 | doorway wall | ▆ harder |
| 27 | Grogh Heights | `030` | 6 (Squire + 2 Chemist + Archer + Thief + **Black Mage**) | rainy breather; two-way rain-Thunder | tight rain | ▂ light (breather) |
| 28 | Walled City of Yardrow | `031` | 6 (**3 Ninja** + 2 Summoner + Marach; survives) | **Ninja** debut; protect Rapha; wall-climb | wall chokepoint | ▆ harder |
| 29 | The Yuguewood | `032` | 7 (3 undead + 2 Black Mage + 2 Time Mage) | undead + caster tempo (Haste the dead) | swamp | ▄ moderate+ |
| 30 | Riovanes Gate | `033` | 7 (Marach + 2 Knight + **Templar** + 3 Archer; survives) | bridge + high-ground archers + break; chain 1/3 | gate bridge | ▆ harder |
| 31 | Riovanes Keep | `034` | P1 **Wiegraf** solo → P2 **Belias** + 4 Archaeodaemon | **2-phase spike**; solo duel + 2nd Lucavi; chain 2/3 | keep | █ FINALE SPIKE |
| 32 | Riovanes Roof | `035` | 3 (**Elmdor** + Celia + Lettie; all flee) | **Assassin** debut; flee-on-critical race; protect Rapha; chain 3/3 | rooftop | ▂ light (race) |

Reading: Chapter 3 is a **wave pattern around two gauntlets and a spike**. Gollund/Lesalia ease in
(charm-denial, reviving healer). The **Vaults chain (24-26)** is a rising three-fight gauntlet
(Hasted Jump → elevated Templar → chokepoint Wiegraf) on one loadout. Grogh Heights is a deliberate
**breather**. Yardow/Yuguo reintroduce protect-the-NPC and undead at higher intensity. The **Riovanes
chain (30-32)** climbs to the chapter's spike (the Wiegraf→Belias Keep) and then exhales into the
flee-race Roof. The two "light" fights (27, 32) are intentional valleys flanking the hardest content.

```text
The back third in one line each:
  Riovanes Gate : storm a bridge under archers + a Templar's ranged break   (Safeguard; spend little)
  Riovanes Keep : a fair SOLO DUEL, then a Lucavi army-of-one + 4 adds       (skill check; Gravity; spacing)
  Riovanes Roof : drive off teleporting assassins by bursting ONE to critical (focus + tempo; protect Rapha)
```

### Curve verdict

```text
PASS (on paper). Above Chapter 2 overall, capped by the two-phase Velius spike (Keep, the hardest
single fight in the mod so far). The two deliberate breathers (Grogh 27, Roof 32) keep the curve
from being a relentless climb and sit on either side of the heaviest content. The two no-resupply
chains are the defining structural challenge — flagged as the top playtest risk. The repeat foes
(Wiegraf x2, Marach x2, Templar x2) are each staged differently (flee vs spike; Yardow vs Gate;
Izlude-elevated vs Gate-ranged), so they don't read as re-runs on paper.
```

## Level bands & boss policy

```text
Generic enemies: 100-102.  Sub-bosses: 103 (Izlude, Zalmo, Marach).  Bosses: 104 (Wiegraf, Elmdor).
LUCAVI spike: Belias/Velius 105 (the chapter's top band, +5 — one above Ch2's Cúchulainn at +4).
Demon adds (Archaeodaemon) 102-103.

Boss-loot policy (Chapter 3): bosses that DIE carry ONE rare, now MID-HIGH (a tier above Ch2's
Ancient Sword / 108 Gems), but still NOT best-in-slot. Bosses that FLEE/SURVIVE carry no rare (the
drop is deferred to where they die — often Chapter 4). The very best gear (Excalibur, Ragnarok,
Chaos Blade, Masamune, Save the Queen, Genji, Ribbon, best robes/shields) stays reserved for Ch4.
```

## Design-exception log

| Exception | Where | Why | Guardrail |
|-----------|-------|-----|-----------|
| Charm / steal (Orator + Thieves) | Gollund (`025`) | charm/steal denial band is the fight | charm/soft-status only; player anti-charm counter valid; one Orator; no hard lock |
| Healer-boss revive sustain | Lesalia (`026`) | Zalmo's revive IS the puzzle | answered by Silence / focus-burst; he flees; holy/soft-status only |
| Elemental-resist gear (Flame Shield) | Lesalia (`026`) | the band-wide Fire-immunity / Thunder pivot | telegraphed, counterable (use Thunder); not a status |
| Time Mage control | Vaults 2nd (`027`), Yuguo (`032`) | canonical tempo casters | Haste/Slow/Float only — no Stop/Immobilize/Don't Act; amplify the headline, not lock the player |
| Dragoon Jump | Vaults 2nd (`027`) | the enemy Dragoon caste | telegraphed leap (reposition / kill grounded); normal charge cadence |
| Templar "Mighty Sword" breaks | Vaults 3rd (`028`), Riovanes Gate (`033`) | the Knights Templar caste | telegraphed ranged break; Safeguard/Maintenance counter; ≤2 break sources/fight |
| Holy Sword (weapon-tied) | Vaults 1st (`029`), Keep P1 (`034`) | Wiegraf's identity | disarm (Steal/Rend Weapon) is the answer; soft status only |
| Undead reraise + heal-weakness | Yuguo (`032`) | the undead caste | preserved as mechanic AND counterplay (PD/Holy/Seal Evil/Entice); one-disruptor cap respected |
| Ninja Throw / wall-climb | Yardow (`031`) | the Ninja caste | Throw is ranged DAMAGE (not a status lock); pin/intercept counters |
| Solo-duel fairness | Keep P1 (`034`) | the iconic 1v1 Wiegraf | must be winnable by a prepared solo Ramza; no hard lock; no-MP Martial-Arts answer stays valid |
| Lucavi mass-AoE/status (Belias) | Keep P2 (`034`) | the 2nd Lucavi | ONE telegraphed AoE source; Gravity/spacing counters; not instant; adds single-status |
| Assassin status / instant-death | Roof (`035`) | the named assassins | RESISTABLE + non-spam; no hard lock; flee-on-critical makes the danger window short |

Hard control (Stop/Don't Act/Petrify spam) remains banned everywhere; break stays limited to the
Templar/Order fights above with the ≤2-source cap.

## Job-escalation ledger (rule 1)

```text
Gollund      (025) : enemy ORATOR debut (charm/status caste)        -> protect-Orran still the read
Lesalia      (026) : Inquisitor reviving boss + Flame-Shield lock    -> silence the reviver, bring Thunder
Vaults 2nd   (027) : enemy DRAGOON debut (Hasted Jump)               -> kill the Chemist, ground the dragoons
Vaults 3rd   (028) : KNIGHTS TEMPLAR debut (Izlude; Mighty Sword)    -> climb to the elevated boss, keep gear
Vaults 1st   (029) : five-doorway chokepoint + disarm Wiegraf        -> hold the gates, take his sword
Grogh        (030) : swap 1 Squire -> rain-Thunder Black Mage         -> Thunder/AoE the cluster (breather)
Yardow       (031) : NINJA debut (wall-climb / Throw)                 -> protect Rapha, pin the assassins
Yuguo        (032) : undead + CASTER TEMPO (Time/Black Mage)          -> permakill the dead, faster (Haste)
Riovanes Gate(033) : swap 1 Knight -> TEMPLAR (ranged break)          -> cross the bridge, hold Safeguard
Riovanes Keep(034) : SOLO DUEL -> 2nd LUCAVI (Belias) + 4 adds        -> win the duel, Gravity the demon
Riovanes Roof(035) : ASSASSIN debut (Celia & Lettie; teleport+death)  -> burst one to critical, save Rapha

New castes first seen in Chapter 3: enemy Orator (025), enemy Dragoon (027), Knights Templar (028),
Ninja (031), the second Lucavi / Belias (034), and the Assassin (035). At most one new wrinkle per
fight — the rule held. (The Geomancer/Summoner/Time-Mage from earlier chapters recur as amplifiers.)
```

## Rare-boss-loot ledger (rule 2)

```text
Izlude       (028) : REFLECT MAIL (armor; auto-Reflect)          -> forces physical damage; first Ch3 rare.
Wiegraf      (034) : DEFENDER (Knight Sword)                      -> stealable in the Phase-1 duel; the
                     deferred Vaults-Wiegraf rare, finally paid out where he dies (as Belias).
Belias       (034) : DEFENSE RING (accessory; status-immunity)   -> the Lucavi's drop (or guaranteed reward).

NO RARE (boss flees/survives -> deferred):
  Zalmo (026, flees) ; Wiegraf-at-Vaults (029, flees -> paid at 034) ; Marach (031 & 033, survives,
  recruitable) ; Elmdor + Celia + Lettie (035, all flee -> Elmdor's MASAMUNE/GENJI deferred to his
  Ch4 Limberry rematch).

All Ch3 rares are MID-HIGH (a clear step above Ch2's Ancient Sword / 108 Gems) and NONE are
Ch4-reserved best gear. Generics stay shop-tier. Two rares land in the marquee Keep fight (two boss
forms), per the overview's "two notable foes" allowance.
```

## Move-Find treasure rewards (NG+ post-game upgrade)

Same NG+-only treasure system as Chapters 1–2 (`010`, `023`), escalated one tier. Chapter 3 is where
treasures begin handing out **mid-high non-buyable "ótimos itens"** — clearly above Ch2's early
non-buyables (Invisibility Cloak/perfume/Elixir tier), but still never the final-game best.

```text
TIER (user-confirmed 2026-06-21):
- BASELINE (all 11 battles): rare slot -> best BUYABLE item per original category; commons -> X-Potion
  / Remedy / Hi-Ether. Post-game floor, same as Ch1/Ch2.
- HIGHLIGHT (6 deserving battles): ONE mid-high NON-buyable item. Ch3 pool = Ninja Gear 197, Rubber
  Suit 199, Kaiser/Venetian Shield 141/142, Grand Helm 156, Yoichi Bow 90, Faerie Harp 94, Hairband/
  Barrette 169/170, plus the carried-over Invisibility Cloak 235 / perfumes 236-239.
- RESERVED FOR CH4 (never in Ch3): rl90+ ultimate weapons (Excalibur/Masamune/Chaos Blade/etc.), Genji
  set, Maximillian, best robes (Lordly Robe), best shields (Escutcheon/Genji Shield), Ribbon, Perseus Bow.
```

| Battle | Map | Tier | Highlight (non-buyable) |
|--------|-----|------|--------------------------|
| Gollund (22) | 27 | baseline | — |
| Lesalia Postern (23) | 2 | **highlight** | **Ninja Gear** (defend Alma vs Zalmo) |
| Vaults 2nd (24) | 58 | baseline | — |
| Vaults 3rd (25) | 59 | **highlight** | **Kaiser Shield** (Izlude; + Reflect Mail boss loot) |
| Vaults 1st (26) | 57 | baseline | — (Wiegraf flees; loot deferred to Keep) |
| Grogh Heights (27) | 81 | baseline | — |
| Yardrow (28) | 25 | **highlight** | **Septième Sens** perfume (protect Rapha; she can wear it) |
| Yuguewood (29) | 79 | baseline | — |
| Riovanes Gate (30) | 6 | **highlight** | **Grand Helm** (the assault) |
| Riovanes Keep (31) | 7 | **highlight** | **Rubber Suit** (chapter spike; + Defender/Defense Ring boss loot) |
| Riovanes Roof (32) | 5 | **highlight** | **Invisibility Cloak** (Elmdor's assassins) |

Implemented in the same `MAP_TRAP_FORMATION_DATA` direct-write subsystem (`MapTreasureNgPlus`); boss
rares above live in the ENTD and are applied during each battle's implementation. See memory note
[[fft-tic-rewards-ngplus]].

## Consistency audit

### Job IDs

```text
Confirmed & reused identically: Squire 74, Chemist 75, Archer 77, Thief 83.
TBD (verify on Windows, used by name): Knight, Monk, Black Mage, Time Mage, Summoner, and the
  Ch3 debuts — Orator/Mediator, Dragoon/Lancer, Knights Templar, Ninja, Inquisitor (Zalmo),
  Holy Knight (Wiegraf), Arc Knight (Elmdor), Assassin (Celia/Lettie), Belias/Velius (Lucavi),
  Archaeodaemon, the undead (Ghoul/Ghast/Revenant), and the boss jobs (Izlude, Marach).
Boss scripting to preserve: Zalmo retreat (026); Izlude "defeat ends fight" (028); Wiegraf flee
  (029) and the Keep two-phase transform + 4-add spawn (034); Marach survive (031, 033); the Roof
  flee-on-critical trigger (035); Orran/Rapha/Alma guest & protect flags (025, 026, 031, 035).
```

### Equipment & skill IDs

```text
Reused without conflict (as Chapters 1–2): Thief's Cap 168, Black Garb 198, Power Garb 195,
  Headband 163, Bracers 218, Germinas Boots 210, Featherweave Cloak 234, Runeblade 30, Icebrand 29,
  Windslash Bow 87, Air Knife 9. Skills: Counter 442, Attack Boost 465, Movement +1 486, +2 487,
  Concentration 469, Reflexes 449, First Strike 453, Auto-Potion 441, Throw Items 474, Fundaments 5.
NEW Ch3 rare items to map in ItemData.xml (verify non-buyable + mid-high, NOT Ch4-reserved):
  REFLECT MAIL (028), DEFENDER knight sword (034), DEFENSE RING (034). Confirm Flame Shield (026),
  ninja blades, spears, katanas referenced by tier.
Mage/Knight/Templar/Ninja shop gear referenced by tier, left TBD until mapped — consistent across
  025-035. No conflicts found on paper.
```

### Level bands & boss kits

```text
Consistent. Generics 100-102; sub-bosses 103 (Izlude/Zalmo/Marach); bosses 104 (Wiegraf/Elmdor);
Belias 105 (chapter top, +5). Summons kept MID-TIER with intact charge times (028). The +5 Lucavi
is the single highest band so far, one above Ch2's Cúchulainn (+4) — the intended escalation.
```

## Open risks / watch-items for playtest

1. **The two no-resupply chains** (Vaults `027`–`029`; Riovanes `033`–`035`) are the #1 risk:
   verify each chain is winnable on ONE loadout without becoming an item-starvation trap. Test each
   chain back-to-back, not battle-in-isolation.
2. **Solo-duel fairness** (Keep P1, `034`): the single most important fairness check in the mod — a
   prepared solo Ramza MUST win; no hard lock; the no-MP Martial-Arts answer must stay valid. If
   Wiegraf is over-tuned, the chapter becomes a brick wall here.
3. **Belias spike tuning** (Keep P2, `034`): high-AoE Lucavi + 4 adds at `105` — verify Gravity
   %-damage stays viable, AoE is telegraphed/spaceable, and the adds are clearable without a wipe.
4. **Assassin lethality** (Roof, `035`): instant-death/status must be resistable and non-spam; verify
   the flee-on-critical trigger actually ends the fight quickly so the danger window stays short, and
   that a 4-unit squad can protect Rapha.
5. **Protect-NPC survivability** (Orran `025`, Rapha `031` & `035`): confirm the guarded NPC's AI
   survives scaled threats (charm-thieves, wall-climbing Ninjas, teleporting assassins) long enough.
6. **Break-pressure stacking** (Templar at `028`/`033` + Rend-Knights): confirm the ≤2-break-source
   cap keeps Safeguard a fair answer, not mandatory tax.
7. **Repeat-foe fatigue** (Wiegraf x2, Marach x2, Templar x2): verify the differentiated staging
   (flee vs spike; Yardow vs Gate; elevated vs ranged) reads as distinct in play.
8. **Breather calibration** (Grogh `030`, Roof `035`): confirm these genuinely feel lighter (curve
   valleys), so the spike lands harder by contrast — don't let scale-to-party inflate them.
9. **Rare-slot feasibility on the Lucavi** (Belias `034`): if Belias can't hold/drop Defense Ring,
   use the guaranteed-reward fallback (as documented). Confirm Defender is stealable in the duel.
10. **Boss-scripting integrity** (highest-risk patches): Zalmo retreat (`026`), Izlude end-trigger
    (`028`), Wiegraf flee (`029`), the Keep two-phase transform + 4-add spawn (`034`), Marach survive
    (`031`/`033`), and the Roof flee-on-critical (`035`). Diff-check and test every trigger.

## Recommended implementation & playtest order

Implement in story order so the curve (and the chains) can be felt as a player would:

```text
025 Gollund -> 026 Lesalia Postern -> [CHAIN: 027 Vaults 2nd -> 028 Vaults 3rd -> 029 Vaults 1st] ->
030 Grogh Heights -> 031 Yardow -> 032 Yuguewood ->
[CHAIN: 033 Riovanes Gate -> 034 Riovanes Keep -> 035 Riovanes Roof]
```

For each: dump the real entry, fill the doc's "Local Data Confirmed", apply levels + job-escalation
swaps + gear + rare boss loot + skills, patch, diff-check inside the battle window only, then test
from a New Game+ save and record results back in the doc. **Test the two chains as units** (no
resupply) — they are the chapter's defining balance problem.

## Status

```text
Design phase: COMPLETE for all 11 Chapter 3 battles (025-035 designed; none patched yet).
Consistency: audited; exceptions logged; job-escalation and rare-loot ledgers extended.
Curve: passes on paper; above Chapter 2, capped by the Wiegraf->Belias spike; two intentional
  breathers; two no-resupply chains + the solo duel are the key in-game watches.
Job escalation: one new wrinkle per fight held across all 11; five new castes introduced cleanly
  (Orator, Dragoon, Templar, Ninja, Assassin) plus the second Lucavi.
Boss-loot: three mid-high rares (Reflect Mail, Defender, Defense Ring); all flee/survive bosses
  deferred; no Ch4-reserved best gear leaked; Elmdor's Masamune/Genji held for Ch4.
Next: data-layer patching + playtest in order (chains as units); then Chapter 4 (new overview).
```

## Sources

- Local design docs: `024-chapter-3-overview.md`, `025-mining-town-gollund.md` … `035-riovanes-castle-roof.md`.
- Original-battle rosters cross-referenced from Game8 Chapter 3 battle walkthroughs (see each battle
  doc's Sources section).
- `010-chapter-1-balance-review.md`, `023-chapter-2-balance-review.md` (the review template + ledgers
  this chapter extends).
</content>
