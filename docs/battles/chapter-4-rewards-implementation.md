# Chapter 4 reward distribution - full map (NG++)

Canonical record of every NG++ equipment reward in Chapter 4. Delivered via the guaranteed **Spoils of
War** channel (ENTD `0x1e`), max 3 per battle (engine cap: first 3 non-zero by slot order), **never
steal-dependent**. Mechanism + cap proof: `spoils-of-war-reward-system.md`. Edits live in the embedded
`battle_entd4_ent.bin`; tooling in scratchpad.

## Design rules

1. **NG+ only.** First playthrough is never affected.
2. **Guaranteed spoils only** (`0x1e`), max 3/battle. No reward requires stealing.
3. **No usable reward inside the no-resupply gauntlet** (054-058). All best gear pays by the last save at
   the end of the Mullonde chain (051-053). The gauntlet drops standard/vanilla loot only. See the
   "gauntlet rule" history at the bottom.
4. **Progression + story-fit.** Rewards improve as the chapter advances (peak at Nave/Sanctuary, right
   before the gauntlet). Items with a canonical owner go on that owner even if it spikes the curve early
   (Save the Queen on Meliadoul, the katanas on Elmdor, etc.) - story impact is a co-equal goal.
5. **Excalibur (35) stays Orlandeau's**, never on an enemy.
6. Only **non-buyable** items (`ShopAvailability = Unknown20`) are treated as rares. Buyable gear
   (Kiyomori, Blood Sword, Angel Ring, Aegis Shield, Crystal/Luminous/Genji-screen gear) is not a reward.

## Full per-battle map (story order)

Rank = position in the 26-item best-to-worst list (1 = best). New = items added by the 2026-06-27
progression rebalance; the rest were already placed on their canonical owner.

| Doc/Battle | Entry | Spoils (<=3) | New | Best rank |
|---|---|---|---|---|
| 038 Dugeura Pass | 442 | Rod of Faith (+item179) | Rod of Faith | 24 |
| 039 Bervenia / Meliadoul | 443 | Save the Queen + Jade Armlet + Remedy | - | 5 (story) |
| 040 Finnath Creek | - | (none - chocobo field) | - | - |
| 041 Outlying Church / Zalmo | 445 | Light Robe + Angel Ring | - | mid |
| 042 Bed Desert / Barich | 447 | Glacial Gun + Blaze Gun + Blaster | Blaze Gun, Blaster | 21 |
| 043a/043b Fort Besselat Wall | 448 (S) / 449 (N) | Yoichi Bow + Perseus Bow (BOTH path entries) | both | 13 |
| 044 Fort Besselat Sluice | 450 | Kaiser Shield | Kaiser Shield | 20 |
| 045 Mount Germinas | 452 | Ninja Gear + Koga Blade + Iga Blade | all 3 | 14 |
| 046 Poeskas Lake | 453 | Cursed Ring (+2 Phoenix Down) | Cursed Ring | 26 (story: undead) |
| 047 Limberry Gate | - | (none - assassins flee) | - | - |
| 048 Limberry Keep / Elmdor | 456 | Masamune + Genji Armor + Chirijiraden | Chirijiraden | 6 (story spike) |
| 049 Undercroft / Zalera | 457 | Aegis Shield + Zeus Mace | Zeus Mace | 19 |
| 050 Eagrose / Adramelk | 459 | Maximillian + Grand Helm + Venetian Shield | Maximillian, Venetian | 11 |
| 051 Mullonde Exterior | 460 | Staff of the Magi + Faerie Harp (+Hi-Ether) | both | 9 |
| 052 Mullonde Nave | 461 | Chaos Blade + Escutcheon + Lordly Robe | - | 3 |
| 053 Mullonde Sanctuary | 462 | Ragnarok + Ribbon (+ Elixir) | - | 1 |

Bows in BOTH Bethla Wall path entries (448 South / 449 North): the player fights only one path, so Yoichi
+ Perseus are duplicated across both so either route awards them.

Capacity notes (all within the 3-cap, verified in the deployed DLL at offset 0x100f0):
- Eagrose (459): drops its Phoenix Down (s1 253 -> Maximillian) so Maximillian + Grand Helm + Venetian fit.
- Germinas (452): the two pre-existing minor spoils (s1 item212, s2 Germinas Boots 210) are OVERWRITTEN by
  Koga + Iga so the three ninja items (Ninja Gear s0 + Koga s1 + Iga s2) are the awarded 3.
- Items marked "(+...)" share the battle with a kept minor/consumable spoil that also lands in the first 3
  (Dugeura item179, Bethla Wall item153/item181, Poeskas 2x Phoenix Down, Mullonde Ext Hi-Ether) - bonus,
  not a rare, never displacing a designed rare.
Finnath (040) and Limberry Gate (047) carry no equipment reward by design (monster field / fleeing assassins).

## All 26 non-buyable items - placement checklist

Best to worst (rank): 1 Ribbon (Sanctuary 462) · 2 Excalibur (RESERVED Orlandeau) · 3 Chaos Blade (Nave
461) · 4 Ragnarok (Sanctuary 462) · 5 Save the Queen (Bervenia 443) · 6 Chirijiraden (Limberry Keep 456)
· 7 Masamune (Limberry Keep 456) · 8 Escutcheon (Nave 461) · 9 Staff of the Magi (Mullonde Exterior) ·
10 Lordly Robe (Nave 461) · 11 Grand Helm (Eagrose 459) · 12 Maximillian (Eagrose 459) · 13 Yoichi Bow
(Bethla Wall) · 14 Koga Blade (Germinas) · 15 Iga Blade (Germinas) · 16 Perseus Bow (Bethla Wall) ·
17 Venetian Shield (Eagrose 459) · 18 Ninja Gear (Germinas) · 19 Zeus Mace (Undercroft 457) · 20 Kaiser
Shield (Bethla Sluice) · 21 Blaster (Bed Desert 447) · 22 Blaze Gun (Bed Desert 447) · 23 Glacial Gun
(Bed Desert 447) · 24 Rod of Faith (Dugeura) · 25 Faerie Harp (Mullonde Exterior) · 26 Cursed Ring
(Poeskas).

All 26 accounted for: 25 placed across 14 battles + Excalibur reserved on Orlandeau.

## Status

- **Design: DONE (2026-06-27).** Full distribution decided; every non-buyable item placed; within the
  3-cap; no steal-dependence; progression + story-fit verified.
- **Apply: DONE (2026-06-27).** All 6 remaining ENTD entries resolved (038=442, 043a/043b=448/449, 044=450,
  045=452, 046=453, 051=460). 18 `0x1e` spoils written on active enemy slots (16 unique items; the two
  Bethla Wall bows duplicated across both path entries). Built Release -> deployed DLL. Verified: source
  `battle_entd4_ent.bin` embedded verbatim at DLL offset 0x100f0; every designed rare lands in the awarded
  first-3; 3-cap respected in all 11 edited entries. Per-battle docs bannered.
- **Pre-release (still pending, separate task):** confirm `DEBUG_FORCE_NGPLUS=false` and
  `DEBUG_SPOILS_PROBE=false` before shipping.

## Gauntlet rule history (still in force)

The endgame is a 5-battle no-resupply gauntlet (054-058: Vaults 4th, Vaults 5th, Necrohol, Lost Halidom,
Airship). On 2026-06-27 the four Tier-S capstones originally dropped there were pulled out (gauntlet
restored to vanilla loot: Loffrey shield back to Crystal Shield 139, Cletienne body back to Black Garb
198) and relocated pre-gauntlet: Escutcheon + Lordly Robe to Nave (Loffrey/Cletienne), Ragnarok to
Zalbaag (Sanctuary). Materia Blade was dropped from the gauntlet (side-quest / Move-Find map-54 pickup).
This bends the carried "retreat/survive = no drop" convention for the Templars at Nave (kill-independent
spoils on Folmarv's death). 440 Hashmal keeps its vanilla dormant Ragnarok at s2 (never awarded).
