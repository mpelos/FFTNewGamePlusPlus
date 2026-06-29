# Chapter 3 — "The Valiant": New Game++ Design Overview

Master plan for rescaling and redesigning every **Chapter 3** story battle of *FINAL FANTASY
TACTICS - The Ivalice Chronicles* (Enhanced v1.5.0) for New Game++.

Chapter 3 is the **dark turn**: the Church / Knights Templar are revealed as the true enemy,
wielding the Zodiac Stones to call Lucavi, and the chapter ends in the harrowing Riovanes
sequence. The scaling mechanic and the "preserve each fight's identity" philosophy still apply
(see `000-chapter-1-overview.md` and `011-chapter-2-overview.md`), and the two Chapter 2 design
goals continue — escalated one notch:

```text
1. ENEMY PARTY ESCALATION — every active human enemy now gets a complete setup (full gear plus
   secondary/reaction/support/movement), and enemy parties are tuned as coherent teams WITHOUT
   breaking each battle's original strategy. Chapter 3 introduces marquee castes: Knights Templar,
   enemy Dragoons, the Ninja, Orator utility, the second Lucavi demon, and Assassins. Synergy is
   expected; deliberately broken Chapter 4 puzzle stacks are not.
2. RARE BOSS LOOT — important (boss) battles equip the boss with a RARE, non-buyable item, now a
   TIER ABOVE Chapter 2 (better than the Blood Sword / 108 Gems baseline) — but still NOT best-in-slot.
   The very best gear (Excalibur, Ragnarok, Chaos Blade, Masamune, Genji set, Save the Queen,
   Ribbon, best robes/shields) remains reserved for CHAPTER 4.
```

## Story framing (why the difficulty rises again)

After Lionel, Ramza chases the conspiracy into the heart of the Church. The Knights Templar —
Wiegraf reborn as a Templar, Izlude, Vormav's circle — hunt the Zodiac Stones and Ramza's sister
**Alma**. The chapter raids the **Orbonne Monastery Vaults**, crosses **Grog Hill** and **Yardow**,
fights the undead of **Yuguo Woods**, and culminates at **Riovanes Castle**, where Wiegraf
transforms into the Lucavi **Velius**, and **Elmdor's assassins** (Celia, Lettie) strike on the
roof. Enemies are now elite: Templar knights with real sword skills, Ninjas, a second demon, and
named assassins. Chapter 3 should feel clearly harder than Chapter 2 — more elite jobs, more
bosses, and two no-resupply battle chains (the Vaults and Riovanes).

## Chapter 3 battle list

"Battle N" follows in-game/Game8 numbering. Doc numbers continue the flat sequence (Chapter 2
ended at `023`; this overview is `024`, so Battle 22 = doc `025`, i.e. doc = battle + 3).

| Doc | Battle | Location | Role in story | New element | Status |
|-----|--------|----------|---------------|-------------|--------|
| `025` | 22 | Mining Town of Gollund | Ambush; Orran/Olan support guest | enemy Orator; charm/steal denial band | ✅ Done |
| `026` | 23 | Lesalia Castle Postern | **Zalmo** (Inquisitor) revives the wall; retreats | reviving boss + Flame-Shield/Thunder puzzle | ✅ Done |
| `027` | 24 | Monastery Vaults — 2nd Level | Vault raid (chain 1/3); Chemist + **Dragoons** | enemy Dragoon (Hasted Jump); no-resupply chain | ✅ Done |
| `028` | 25 | Monastery Vaults — 3rd Level | **Izlude** on high ground + casters | Templar debut + rare (Reflect Mail); elevation | ✅ Done |
| `029` | 26 | Monastery Vaults — 1st Level | **Boss: Wiegraf** (Holy Knight; flees) | 5-doorway chokepoint + disarm; rare deferred to 034 | ✅ Done |
| `030` | 27 | Grogh Heights | Rain + thunder; clustered line targets | breather; two-way rain-Thunder + line-AoE | ✅ Done |
| `031` | 28 | Walled City of Yardrow | Protect/player-control Rapha; **Ninjas** scale walls; Marach boss | **Ninja** debut; vertical assassins + Summoner AoE | ✅ Done |
| `032` | 29 | The Yuguewood | Undead woods; Seal Evil / Entice | undead + caster tempo (Time/Black Mage) | ✅ Done |
| `033` | 30 | Riovanes Castle Gate | Assault (chain 1/3); pressure Marach | bridge + high-ground archers + Templar break; no-resupply | ✅ Done |
| `034` | 31 | Riovanes Castle Keep | **Wiegraf solo duel → Belias/Velius** (Lucavi) | 2-phase spike; 2nd Lucavi + 3 TIC-confirmed adds; rares (Defender, Defense Ring) | ✅ Done |
| `035` | 32 | Riovanes Castle Roof | **Elmdor** + assassins; protect/player-control Rapha | **Assassin** debut; flee-on-critical race; no loot (all flee) | ✅ Done |
| `036` | — | Chapter 3 Balance Review | Cross-battle curve + consistency audit | — | ✅ Done |

## ENTD entries — ✅ roster baseline confirmed; v2 redesign docs-only

The current v1 mod has Chapter 3 entries identified and roster-checked. This v2 pass updates the
design documents only; future implementation must still patch, re-dump, and test each entry.
- **430 Yuguewood**: active casters are enemy-variant **job 66 = Black Mage** (equips Rod), **job 68 =
  Time Mage** (equips Staff) — distinct from player-generic 80/81; undead Ghoul/Ghast/Revenant
  (112/113/114) sit at level 0xFE (verify they scale; may be OverrideEntryData-driven).
- **432 Riovanes Keep**: s0 Wiegraf(40) duel + s5 Belias(60) Lucavi + s6-8 Archaeodaemon(153)×3
  (TIC has 3 adds, not 4); lvl-1 slots are transform-scripting placeholders.
- **433 Riovanes Roof**: s3 Elmdor(27 Ark Knight) + s4 Celia(45)/s5 Lettie(46) Assassins + s0 Rapha
  (41 Skyseer, guest); lvl-5 slots (s1 Rapha-clone, s2 Netherseer) are scripting placeholders.
- **Guest vs enemy in ENTD**: the unit's control bytes `raw_tail[0:2] == 00 84` mark a guest/ally
  slot (validated: Orran 417, Alma 420, Rapha 428/433); enemies use other control bytes (e.g. 03/04
  9x). This does not by itself satisfy the NG+ rule: every active guest must be player-controlled.
  Rapha's sprite/charId differs per battle (25 at Yardrow, 41 at Roof), and the Roof has an enemy
  clone sharing her sprite, so scale Roof Rapha by direct ENTD level, not the runtime scaler.

## (historical) Deduced ENTD entries (offline roster-match — confirm in-game before/after patch)

Identified by matching each battle's documented roster (units/job/level) against the dumped vanilla
ENTD (`extracted/.../battle_entd4_ent.bin`), cross-checked by **named-unit recurrence** (Wiegraf =
job 40 at both Vaults-1st and Keep; Marach = the 25/26 named pair at Yardrow and Gate) and
**story-order monotonicity** (entries rise with battle number — a strong consistency signal). Job ids
verified against a known Ch2 entry (403 Merchant Dorter). The `[battle-id]` runtime log still confirms
each on entry; treat MEDIUM rows as verify-before-patch.

| Battle | Doc | ENTD entry | Confidence | Roster signature matched |
|--------|-----|-----------|------------|--------------------------|
| Gollund (22) | 025 | **417** | HIGH | named(Orran) + 2 Chemist + 3 Thief + 1 Orator |
| Lesalia Postern (23) | 026 | **420** | HIGH | 2 named(Zalmo+Alma) + 3 Knight + 2 Monk |
| Vaults 2nd (24) | 027 | **422** | HIGH | named + 1 Chemist + 2 Time Mage + 3 Dragoon |
| Vaults 3rd (25) | 028 | **423** | HIGH | named(Izlude) + 2 Knight + 2 Archer + 1 Summoner |
| Vaults 1st (26) | 029 | **424** | HIGH | named(Wiegraf=40) + 2 Knight + 2 Archer + 1 Black Mage |
| Grogh Heights (27) | 030 | **426** | MED-HIGH | 2 Squire + 2 Chemist + Archer + Thief (+extras) |
| Yardrow (28) | 031 | **428** | HIGH | 2 named(Marach+Rapha) + 2 Summoner + 3 Ninja |
| Yuguewood (29) | 032 | **430** | HIGH | undead trio Ghoul/Ghast/Revenant + 4 casters |
| Riovanes Gate (30) | 033 | **431** | HIGH | named(Marach) + 4 Knight + 3 Archer (v2 swaps one Knight to Templar) |
| Riovanes Keep (31) | 034 | **432** | HIGH | Wiegraf(40) + Belias(60) + 3× Archaeodaemon(153) |
| Riovanes Roof (32) | 035 | **433** | HIGH | Rapha + Elmdor + Celia/Lettie + 2 scripting placeholders |

(Entries 418/419/421/425/427/429 in the gaps are Ch2 Cúchulainn=425 and cutscene/sub-event ENTDs.)

## Carried-over rules (from Chapters 1–2)

Still in force — see `000-chapter-1-overview.md` and `011-chapter-2-overview.md` for full text:

```text
- Scale to party: enemy Level = 100 + offset. Offsets stay small; bosses are the spikes.
- Preserve each battle's identity (theme, archetypes, terrain, what it teaches).
- Respect job equipment rules (mages wear robes, monsters wear nothing, etc.).
- Keep the curve readable: at most ONE new meaningful demand per fight.
- Guest-control rule: from Chapter 1 onward, every active guest is player-controlled in NG+,
  whether or not the objective says to save them. Guest AI is not a skill check.
- Document any rule exception per-battle (Time Mage control, equipment-break, boss self-heal,
  boss mass-status, undead reraise, etc. — see the Ch2 design-exception log in `023`).
```

## NEW rule 1 — Complete enemy parties (Chapter 3 castes)

Chapter 3's roster turns elite. The goal remains **more challenge through variety and synergy**,
never at the cost of the fight's original strategy. Chapter 2 already gave active human enemies full
equipment and intentional R/S/M; Chapter 3 closes the remaining gap by making secondary skillsets
mandatory and by tuning the whole enemy party as a coherent team.

```text
CHAPTER 3 CASTES TO DEPLOY (canon castes are highlighted, but any non-Mime/non-Calculator job is
legal if it preserves the battle spirit):
- Knights Templar  : elite sword-skill users (Wiegraf, Izlude) — Holy/Dark sword arts; the
                     bosses of the Vaults. Treat their sword skills like Ch2 Gaffgarion's Drain:
                     strong, but with a telegraphed counter (disarm / spacing / element).
- Dragoon (enemy)  : Jump from range/elevation (debuted on our side at Zaland, 015; now an enemy
                     caste at the Vaults). Vertical pressure on back-line casters.
- Ninja            : dual-wield, high Move/Jump, wall-climb, THROW — a fast assassin caste (Yardow).
                     The marquee new job of the chapter.
- Oracle / Orator  : status + utility (Yuguo). Constrained like all status (no hard lock spam).
- Lucavi (Velius)  : the second demon — a multi-summon "army of one" boss (Riovanes Keep).
- Assassins        : Celia / Lettie — named special units (Riovanes Roof).

RULE: every active human enemy gets complete equipment plus a complete ability setup: secondary,
reaction, support, and movement. Secondary is no longer optional. The party should have real synergy
(front line + artillery + support + disruptor + boss/engine), but not yet the deliberately broken
puzzle stacks reserved for Chapter 4. Add enemies when they create flanks, bodyguards, action economy,
or chain pressure.
DO NOT introduce hard lockdown (Stop/Don't Act/Petrify spam) on an endgame party.
```

A short **"Enemy party escalation"** section in each battle doc states the vanilla battle spirit, the
new party roles, each complete setup's job/secondary/reaction/support/movement plan, and why the
composition is synergistic without becoming a Chapter 4 broken puzzle.

## NEW rule 2 — Rare boss loot (the Chapter 3 tier)

Chapter 2 bosses dropped the LOWEST tier of rares (Blood Sword, 108 Gems). Chapter 3 bosses drop
**better, mid-HIGH rares** — clearly an upgrade — but still **not best-in-slot**.

```text
CHAPTER 3 RARE-LOOT TIER (examples — verify exact ids/availability in ItemData.xml):
  Weapons:   Defender (knight sword, above Blood Sword/below Save the Queen), Platinum Sword,
             a mid-HIGH katana (Kiyomori / Murasame / Heaven's Cloud — NOT Masamune), an elemental
             gun (Blaze/Glacial/Blast), a rare bow above shop tier.
  Armor:     Reflect Mail (auto-Reflect), Carabini/Platinum-tier armor, a Wizard/Light Robe
             (above shop, below best robes).
  Shields:   Aegis Shield (high magic-evade) or Kaiser Plate — NOT Escutcheon/Genji Shield.
  Accessory: Defense Ring, Magic Ring, Sprint Shoes, Feather Boots, a Diamond Armlet, or a better
             elemental-mitigation trinket than 108 Gems.
  Headgear:  Golden Hairpin, Flash Hat, Twist Headband — NOT Ribbon.

RESERVED FOR CHAPTER 4 (do NOT use in Ch3):
  Excalibur, Ragnarok, Chaos Blade, Masamune, Save the Queen, Genji set (helm/armor/shield/gloves),
  Escutcheon II / best shields, Ribbon, best robes (Robe of Lords / Maximillian-tier).

SPECIAL — ELMDOR (Riovanes Roof, 035): canonically the source of the Genji set + Masamune, but those
are BEST-tier and RESERVED for his CHAPTER 4 rematch (Limberry). At Riovanes Roof he flees, so he
carries no rare highlight; use only non-rare, non-best equipment.

RULE OF THUMB: each boss battle's boss gets ONE rare highlight only when the boss dies or is otherwise
claimable. Fleeing/surviving bosses carry no rare; their loot is deferred. Generics stay shop-tier.
```

Each boss battle doc includes a **"Boss rare loot"** line naming the item, why it fits, and
confirming it is mid-high (not reserved-for-Ch4).

## Difficulty budget per battle (Chapter 3)

Bands creep slightly above Chapter 2; bosses are the spikes. Generics `100–102`, sub-bosses
`102–103`, bosses `103–104`, the Lucavi/major spike `104–105`.

| Battle | Target feel | Level band | New wrinkle / boss loot |
|--------|-------------|------------|--------------------------|
| Gollund (22) | Ambush with a controlled guest | 100–102 | Orran/Olan crowd-control ally; tougher mercs |
| Lesalia Postern (23) | Defend controlled Alma; silence the healer | 100–103 | **Zalmo** Inquisitor heal/revive; protect Alma |
| Vaults 2nd (24) | Vault raid, chain 1/3 | 100–102 | enemy **Dragoon** Jump; no resupply |
| Vaults 3rd (25) | Izlude on high ground | sub-boss 103, adds 100–102 | **Izlude** Templar sub-boss + casters |
| Vaults 1st (26) | **Wiegraf** Templar boss | boss 104, adds 100–102 | boss pressure; disarm his sword arts; rare deferred to Keep |
| Grogh Heights (27) | Rain/thunder line puzzle | 100–102 | weather + line-AoE clustering |
| Yardrow (28) | Protect controlled Rapha vs Ninjas | 100–103 | **Ninja** debut; wall-climb assassins |
| Yuguewood (29) | Undead woods | 100–102 | undead (reraise) + Oracle status |
| Riovanes Gate (30) | Assault, chain 1/3 | 100–103 | Safeguard wall; no resupply |
| Riovanes Keep (31) | **Wiegraf → Velius** | duel 104, Velius 105 | **2nd Lucavi + 3 adds + rare loot**; the chapter spike |
| Riovanes Roof (32) | **Elmdor** + assassins | boss 104, assassins 103 | assassins + flee race; protect/player-control Rapha; no loot |

Two **no-resupply chains** to test back-to-back: the Vaults (24→25→26) and Riovanes (30→31→32).

## Workflow per battle (same as Chapters 1–2)

```text
1. Read this overview + the battle doc.
2. On Windows: identify the BattleId / ENTD entry (cross-ref SortieConfirm, EventId, Map,
   scenario tables; sanity-check with FFTIvaliceEditor).
3. Dump the entry; confirm the original roster matches the doc's "Original Battle".
4. Apply the New Game++ composition: levels, enemy-party escalation swaps, gear, rare boss loot, skills,
   placement, and guest-control flags for every active guest.
5. Patch via the right layer (.bin or OverrideEntryData); keep the diff inside the battle window.
6. Copy into the mod, install to Reloaded-II, test from a New Game+ save.
7. Record results back in the battle doc.
```

## Sources

- Game8, "Chapter 3: The Valiant Walkthrough":
  https://game8.co/games/Final-Fantasy-Tactics/archives/543256
- Game8 per-battle walkthroughs (rosters) — linked in each battle doc (archives 553182–553192;
  IDs are NON-sequential, verify each).
- Local: `000-chapter-1-overview.md`, `011-chapter-2-overview.md` (carried rules),
  `023-chapter-2-balance-review.md` (exception log + rare-loot ledger this chapter builds on).
