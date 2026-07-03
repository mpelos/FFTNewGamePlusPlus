# 023 - Chapter 2 Balance Review

A cross-battle audit of all **11** Chapter 2 New Game++ designs (`012`–`022`). It checks the
difficulty curve, verifies consistency of level bands / gear / job-skill IDs, logs the deliberate
design exceptions, and adds two Chapter-2-specific ledgers the project introduced this chapter:
the **enemy-party escalation ledger** and the **rare-boss-loot ledger**. Then it flags open risks and
gives a recommended playtest order. This is a paper review — every finding must be re-validated
in-game once each battle is patched on the Windows data.

## The central balancing insight (carried from Chapter 1)

Enemies are still scaled `Level = 100 + offset`, so **the level offset is not the main difficulty
lever**. Difficulty comes from composition, terrain, and mechanics. Chapter 2 adds two new levers
on top of those, per the chapter goals:

```text
5. Enemy party escalation — full enemy kits and role-built parties that intensify the strategy.
6. Boss identity — real named bosses (Gaffgarion x2, Cúchulainn) as the spikes, each with a
   distinct puzzle (disarm the Drain / spread + Holy the demon), and rare non-buyable rewards.
```

The curve is carried by **composition + terrain + mechanics + complete R/S/M setup + the bosses**
— with level offsets (100–104) as fine tuning only.

## Difficulty curve (all 11 battles, as designed)

| # | Battle | Doc | Enemies | New demand / enemy-party escalation | Terrain | Tier |
|---|--------|-----|---------|------------------------------|---------|------|
| 11 | Merchant Dorter | `012` | 7 (2 Archer + 2 Black Mage + 2 Thief + **+1 Knight anchor**) | harder Dorter rematch; charm-Thieves | rooftops | ▃ moderate |
| 12 | Araguay Woods | `013` | 7 (4 Black Goblin + 2 Gobbledygook + **1 Coeurl**) | controlled Boco through promoted monster tiers | woods | ▃ moderate+ |
| 13 | Zeirchele Falls | `014` | Gaffgarion (turncoat) + 5 Knight (one crossbow) + 1 White Mage | controlled Ovelia/Agrias; **betrayal bridge** | falls | ▅ hard |
| 14 | Zaland | `015` | 7 (1 Knight + 2 Dragoon + 2 Archer + 2 Black Mage) | controlled Mustadio; **Dragoon** vertical pressure | castle city | ▅ hard |
| 15 | Balias Tor | `016` | 7 (2 **Summoner** + 2 Knight + 2 Archer + 1 Chemist) | **Summoner debut**: race the summon through sustain | hill | ▆ harder |
| 16 | Tchigolith Fenlands | `017` | 8 (2 Ghoul + 2 Skeleton + 2 Bonesnatch + Malboro + Floating Eye) | **undead** attrition + one mass-status monster | swamp | ▆ harder |
| 17 | Goug Lowtown | `018` | 7 (2 Summoner + 1 Time Mage + 2 Archer + 2 Thief) | 2nd Summoner fight + **tempo/charm** | urban | ▆ harder |
| 18 | Balias Swale | `019` | 7 (2 Knight + 2 Archer + 2 Black Mage + 1 Geomancer) | controlled Agrias; split-team **rain-Thunder route pressure** | wet valley | ▆ harder |
| 19 | Golgollada Gallows | `020` | **Gaffgarion sub-boss** + 3 Knight + 2 Archer + 2 Time Mage | **Dark Knight Drain**: disarm puzzle; no-guest split | gallows | ▇ very hard |
| 20 | Lionel Castle Gate | `021` | **Gaffgarion boss (dies)** + 3 Knight + 2 Archer + 1 Summoner | **boss + Blood Sword**; two-phase; disarm weapon | castle gate | ▇ very hard |
| 21 | Lionel Castle Oratory | `022` | **Cúchulainn** (lone Lucavi demon, `104`) | **demon finale**: mass-status + **Holy weakness**; reward-table rare | small arena | █ finale |

Reading: the front third (11–14) escalates the *generic* roster into real NG+ parties (Knight
anchor → faster beasts → betrayal/crossbow/medic → Dragoon pressure) while making every active guest
player-controlled. The middle (15–18)
introduces the chapter's marquee *castes* — Summoners, the undead, tempo Time-Mages, the Geomancer
— each a new tactical caste, not just a bigger number. The back third (19–21) is the **boss
escalation**, and it deliberately avoids repetition even though Gaffgarion appears twice:

```text
Golgollada Gallows : Gaffgarion SUB-boss, self-heal Drain, RETREATS   (disarm him; hold the split)
Lionel Gate        : Gaffgarion BOSS, two-phase siege, DIES + rare    (steal the Blood Sword)
Lionel Oratory     : Cúchulainn, lone Lucavi DEMON                     (spread + cleanse + HOLY)
```

### Curve verdict

```text
PASS (on paper). Monotonic in "number of distinct demands," the right axis for a scale-to-party
mod. Chapter 2 sits clearly above Chapter 1: it opens around Ch1's mid-tier (Merchant Dorter ≈
Siedge Weald) and climbs to a demon capstone harder than any Ch1 boss. The two Gaffgarion fights
are distinguished by role (retreat sub-boss vs two-phase death-boss with rare loot), so the repeat
boss does not feel like a re-run on paper. Watch-items below for the boss-dense back third.
```

## Level bands & boss policy

```text
Generic enemies: 100-102 (most 100-101; anchors/captains 102).
Sub-boss:  Gaffgarion @ Gallows 103 (+3).
Bosses:    Gaffgarion @ Lionel Gate 103 (+3, dies)  |  Cúchulainn target 105 (+5), fallback 104.
Gaffgarion also appears as the Zeirchele turncoat (014) — there a scripted betrayal, not a
  free-standing spike. No generic exceeds +2; only Gaffgarion (+3) and Cúchulainn (+5 target) go
  higher.

Boss-loot policy (Chapter 2): named bosses that DIE carry ONE rare, non-buyable item — but
MID-TIER, never best-in-slot. The best gear (Excalibur, Ragnarok, Chaos Blade, Masamune, Genji,
Save the Queen, Ribbon, best robes) is reserved for Chapter 4. A boss that only RETREATS (Gallows)
carries no rare (nothing to drop yet) — its rare is paid out where it dies (the Gate).
```

## Brave/Faith audit

```text
PASS (docs). Every Chapter 2 battle doc (`012`-`022`) now records Br/Fa for each fixed active enemy
in the proposed composition. Active guests/story allies outside the enemy composition are documented
in each battle's Guest handling block. Player-deployed units remain player-build data and are not
fixed by encounter docs.

Design intent: Chapter 2 previews Brave/Faith as a build axis without extreme values. Physical units
sit around Br 74-78 with lower Faith; casters sit around Faith 72-76; monsters stay aggressive but
low-Faith; guests use role-specific values.
```

## Design-exception log

Chapter-wide rules are deliberately broken in specific fights because the original battles are
built around those mechanics. Each is constrained to stay fair at NG+ scale:

| Exception | Where | Why | Guardrail |
|-----------|-------|-----|-----------|
| Time Mage control | Goug (`018`), Gallows (`020`) | Original fights field Time Mages; tempo is the point | Haste/Slow/Float only — **no** Stop/Immobilize/Don't Move/Don't Act. One Time Mage everywhere EXCEPT the Gallows, where TWO are canonical and exist to keep Gaffgarion fast (he, not they, is the headline) |
| Charm (Steal Heart) | Merchant Dorter (`012`), Goug (`018`) | Thieves canonically charm | Charm only; the player's charm-immune/all-male counter stays valid; cap at two charm Thieves per fight |
| Equipment break (Rend) | Balias Tor (`016`), Balias Swale (`019`), Gallows (`020`), Lionel Gate (`021`) | Order Knights carry canonical Rend/Battle Skill | No Dual Wield/Rend abuse; shop-tier breakable gear only; Safeguard remains the answer |
| Boss self-heal (Drain) | Gallows (`020`), Lionel Gate (`021`) | Gaffgarion's Shadowblade IS his identity | Kept WEAPON-tied so Steal/Rend Weapon is the fair, telegraphed off-switch |
| Boss mass-status (Nightmare) | Oratory (`022`) | Cúchulainn's Lucavi kit | ONE source (the boss), telegraphed; counters are spread-out + Immobilize + Remedy/Esuna + Holy burst; not instant |
| Monster mass-status (Bad Breath) | Tchigolith (`017`) | Malboro is canonical to the bog | ONE disruptor only; no second mass-status monster added |
| Undead reraise + heal-weakness | Tchigolith (`017`) | The undead caste IS the fight | Preserved as mechanic AND counterplay (Phoenix Down / Holy permakills); not stripped, not multiplied |

Hard control (Stop/Don't Act/Petrify spam) remains banned everywhere; break stays limited to the
three Order fights above.

## Enemy-party escalation ledger (NEW rule 1)

Every fight states which slot(s) changed job and confirms the original strategy survived:

```text
Merchant Dorter (012) : 2 Archer + 2 Black Mage + 2 Thief + 1 Knight anchor -> rooftop pressure + charm
Araguay Woods   (013) : 4 Black Goblin + 2 Gobbledygook + 1 Coeurl          -> controlled Boco route pressure
Zeirchele Falls (014) : Gaffgarion + 5 Knight (one crossbow) + White Mage   -> bridge betrayal, not Ovelia AI
Zaland          (015) : 1 Knight + 2 Dragoon + 2 Archer + 2 Black Mage       -> controlled Mustadio under vertical pressure
Balias Tor      (016) : 2 Summoner + 2 Knight + 2 Archer + Chemist           -> first summon race through sustain
Tchigolith      (017) : undead pack + one Malboro + one Eye                  -> attrition/status without spam
Goug Lowtown    (018) : 2 Summoner + Time Mage + 2 Archer + 2 Thief          -> faster summon race + charm
Balias Swale    (019) : 2 Knight + 2 Archer + 2 Black Mage + Geomancer       -> controlled Agrias + route-biased storm cell
Golgollada      (020) : canonical Gaffgarion trap, stronger but strippable   -> disarm the Drain
Lionel Gate     (021) : canonical two-front boss gate, Blood Sword reward    -> disarm + hold the gate
Lionel Oratory  (022) : CÚCHULAINN solo Lucavi level 104 chain-aware         -> spread + cleanse + Holy

New jobs/castes first seen in Chapter 2: Dragoon (015), Summoner (016), the undead trio +
Malboro + Floating Eye (017), enemy Time-Mage-as-tempo (018, the Ch1 Lenalian job now used
offensively), Geomancer (019), Gaffgarion as a committed Dark Knight boss (020/021), and the
first Lucavi demon (022). The v2 rule is one headline demand per fight, with the whole enemy side
supporting that demand.
```

## Rare-boss-loot ledger (NEW rule 2)

```text
Lionel Gate (021)   : Gaffgarion -> BLOOD SWORD (23).
                      Doubles as the Steal/Rend target AND the reward path. MID-TIER/non-best
                      drain identity item; no Ch4-reserved best gear leaked. First rare boss loot.
Lionel Oratory (022): Cúchulainn -> 108 GEMS (accessory, elemental damage reduction; non-buyable).
                      A demon's trinket. MID-TIER (below Ribbon/Genji/best robes — Ch4-reserved).
                      Because the Lucavi slot is Unarmed, this should be a reward-table/battle
                      reward rather than fake ENTD equipment.

Non-boss fights and the RETREAT-only Gallows (020) carry NO rare items — generics stay shop-tier,
keeping the two real drops impactful. No Chapter-4-reserved best item appears anywhere in Ch2.
```

## Move-Find treasure rewards (NG+ post-game upgrade)

Separate from the boss-held loot above (which lives in the ENTD), each map's hidden **Move-Find
Items** ("battle rewards") are upgraded for post-game players, **NG+ only** (a first playthrough
keeps vanilla treasures). Chapter 2 escalates over the Chapter-1 reward pass (see `010`): the same
post-game baseline PLUS the chapter where **non-buyable rares start appearing in treasures** — but
only the *early/initial* unbuyable tier, never endgame.

```text
TWO-TIER DESIGN (user-confirmed 2026-06-21):
- BASELINE (all 11 battles): rare slot -> strongest item in its ORIGINAL category whose availability
  is not Unknown20/Blank and id<256 (post-game gear, never the endgame-reserved best). Commons ->
  X-Potion / Remedy / Hi-Ether (Phoenix Down kept). Same rule as Chapter 1.
- SIGNATURE (only the battles that "deserve a good item" = boss / recruit / climax): ONE early
  NON-buyable rare added as the highlight. The "early non-buyable" pool = the lowest-reqlv Unknown20
  items (rl5-14), which are special/unique but NOT endgame: Invisibility Cloak 235, Cursed Ring 222,
  the Perfumes 236-239, Elixir 245. Endgame Unknown20 (rl90+ weapons, Genji set, Maximillian, best
  robes, Ribbon, best shields/bows) stays reserved for Chapter 4.
```

| Battle | Map | Tier | Highlight (non-buyable) + why |
|--------|-----|------|-------------------------------|
| Merchant Dorter | 31 | baseline | — (Bow/Throwing/Shield/Helmet → best non-reserved) |
| Araguay Woods | 80 | baseline | — (Hat/Armor/Clothing/Shoes) |
| Zeirchele Falls | 83 | **signature** | **Invisibility Cloak** — Gaffgarion's ambush/betrayal |
| Zaland | 35 | **signature** | **Elixir** (common slot) — Mustadio recruit |
| Balias Tor | 84 | baseline | — (Hat/Armor/Clothing/Armguard) |
| Tchigolith Fenlands | 78 | baseline | — (Katana/Katana/Axe/Gun) |
| Goug Lowtown | 40 | baseline | — (Crossbow/Bow/Instrument/Book) |
| Balias Swale | 87 | **signature** | **Chantage** (auto-Reraise perfume) — "Save Agrias!"; she can wear it |
| Golgollada Gallows | 63 | **signature** | **Cursed Ring** — Gaffgarion the Dark Knight |
| Lionel Castle Gate | 12 | **signature** | **Elixir** (common slot) — Gaffgarion boss duel |
| Lionel Castle Oratory | 13 | **signature** | **Septième Sens** (perfume) — Cúchulainn, chapter climax |

Implemented in the same NG+-conditional `MAP_TRAP_FORMATION_DATA` direct-write subsystem as the
Chapter-1 rewards (Program.cs `MapTreasureNgPlus`). Confirm in play via the `[mapitems]` log line.
See memory note [[fft-tic-rewards-ngplus]].

## Consistency audit

### Job IDs

```text
Confirmed & reused identically: Archer 77, Thief 83 (and Squire 74 / Chemist 75 where present).
TBD (verify on Windows, used by name): Knight, Black Mage, Summoner, Time Mage, Geomancer,
  Dragoon, Dark Knight (Gaffgarion), the monsters (Black Goblin, Gobbledygook, Coeurl, Ghoul,
  Skeleton, Bonesnatch, Malboro, Floating Eye), and Cúchulainn (Lucavi).
Boss scripting to preserve: Gaffgarion betrayal (014), retreat threshold (020), death + drop (021);
  Cúchulainn transform/solo (022); Ovelia/Agrias/Mustadio guest/escort flags (014/015/018/019).
```

### Equipment & skill IDs

```text
Reused without conflict (same as Chapter 1): Thief's Cap 168, Black Garb 198, Bracers 218,
  Germinas Boots 210, Featherweave Cloak 234, Runeblade 30, Icebrand 29, Windslash Bow 87,
  Air Knife 9. Skills: Counter 442, Attack Boost 465, Movement +1 486, Movement +2 487,
  Concentration 469, Reflexes 449, First Strike 453.
NEW Ch2 reward items to map in ItemData/reward data: BLOOD SWORD (23) at Lionel Gate (021),
  108 GEMS (022) through reward-table/battle reward. Confirm neither leaks Ch4-reserved best gear.
Mage/Knight shop gear and summon/Time/Geomancy skillsets referenced by tier, left TBD until
  mapped — consistent across 012-022. No conflicts found on paper.
```

### Level bands & boss kits

```text
Consistent. Generics 100-102; Gaffgarion 103 at both free-standing appearances (sub-boss retreat
vs death-boss), differentiated by role and the Gate's Blood Sword; Cúchulainn stays 104 as the
solo capstone and must be tested from the Gate chain. Summons stay MID-TIER with intact charge times in all three
summoner fights (016/018/021).
```

## Open risks / watch-items for playtest

1. **Boss-dense back third** (`020`–`022`): three heavy fights in a row, Gaffgarion twice. Verify
   the Gallows (retreat/disarm) and the Gate (two-phase/death/rare) feel distinct, not a re-run.
2. **Disarm dependency** (`020`, `021`): both Gaffgarion fights assume the player can disarm
   (Thief Steal Weapon / Knight Rend / Mustadio Arm Shot). Confirm an NG+ party reliably has one;
   if not, Drain becomes a slog — consider a telegraph/hint rather than lowering his HP.
3. **Cúchulainn solo scaling** (`022`): keep level `104` and test from the Gate→Oratory chain, not
   a fresh save. Holy must stay decisive and Nightmare survivable with spacing/cleansing.
4. **No-resupply Gate→Oratory** (`021`→`022`): verify resource discipline is tense, not punishing;
   the Gate fight shouldn't force item-starvation into Cúchulainn.
5. **Summoner race-ability** (`016`, `018`, `021`): confirm charge times keep summons interruptible;
   a Haste'd Summoner (Goug) must still be race-able, not effectively instant.
6. **Two Time Mages at the Gallows** (`020`): verify Haste-on-Gaffgarion + Slow-on-player is
   pressure, not a lock; drop to one if oppressive.
7. **Guest-control implementation** (`014` Ovelia/Agrias, `015` Mustadio, `019` Agrias, plus other
   active guests): confirm every active guest is player-controlled in NG+ and that difficulty comes
   from enemy route/target pressure, not guest AI.
8. **Vertical/terrain jobs on scaled maps** (`015` Dragoon Jump, `019` Geomancer terrain): verify
   they actually function on the real map geometry.
9. **Rare-slot feasibility on the Lucavi** (`022`): if Cúchulainn can't hold/drop 108 Gems, use the
   guaranteed-reward fallback (already documented in the battle doc).
10. **Boss-scripting integrity** (highest-risk patches): Gaffgarion's betrayal (`014`), retreat
    threshold (`020`), and death + Blood Sword steal/reward path (`021`); Cúchulainn's transform/solo (`022`).
    Diff-check and test every objective/retreat/death trigger.

## Recommended implementation & playtest order

Implement in story order so the curve can be felt as a player would:

```text
012 Merchant Dorter -> 013 Araguay Woods -> 014 Zeirchele Falls -> 015 Zaland ->
016 Balias Tor -> 017 Tchigolith Fenlands -> 018 Goug Lowtown -> 019 Balias Swale ->
020 Golgollada Gallows -> 021 Lionel Castle Gate -> 022 Lionel Castle Oratory
```

For each: dump the real entry, fill the doc's "Local Data Confirmed", apply levels + enemy-party
roles + gear + rare boss loot/rewards + skills, patch, diff-check inside the battle window only, then test
from a New Game+ save and record results back in the doc. Test the Gate→Oratory pair back-to-back
(no resupply) to validate the resource curve.

## Status

```text
Design phase: v2 COMPLETE for all 11 Chapter 2 battle docs (012-022); implementation applied for all Chapter 2 entries.
Consistency: audited; exceptions logged; enemy-party escalation and rare-loot ledgers updated.
Curve: passes on paper; clearly above Chapter 1, capping at the Cúchulainn solo finale; risk items
  above to confirm in-game (boss-dense back third + chain-aware solo-demon tuning are the key watches).
Enemy escalation: one headline demand per fight held across all 11; full enemy-side support is documented.
Boss-loot: Blood Sword plus 108 Gems reward path; no Ch4-reserved best gear leaked.
Next: data-layer patching + playtest in order; then Chapter 3 (new overview to follow).
```

## Sources

- Local design docs: `011-chapter-2-overview.md`, `012-merchant-dorter.md` … `022-lionel-castle-oratory.md`.
- Original-battle rosters cross-referenced from Game8 Chapter 2 battle walkthroughs (see each
  battle doc's Sources section).
- `010-chapter-1-balance-review.md` (the review template + the boss-loot escalation seed).
</content>
