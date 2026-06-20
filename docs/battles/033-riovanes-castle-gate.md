# 033 - Riovanes Castle Gate

Status: designed (not yet implemented)
Chapter: 3 — "The Valiant"
Battle order: Battle 30 (after The Yuguewood) — **Riovanes chain 1 of 3**
Target version: Enhanced v1.5.0
ENTD: global entry **TBD** — confirm on Windows game data
File: `battle_entd*_ent.bin` (TBD) / `OverrideEntryData` rows (TBD)

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `024-chapter-3-overview.md`.

## Original Battle

Objective:

```text
Defeat all enemies!
```

Player deployment:

```text
Up to 5 units, including Ramza. No guests.
CHAIN: this fight is IMMEDIATELY followed by Riovanes Castle Keep (the Wiegraf duel -> Velius) with
  NO resupply or gear change. Conserve resources — the Keep is the chapter's savage spike.
```

Original enemy composition:

```text
1x Marach    (named BOSS — survives; advances over the bridge; recruitable later, so he does NOT die)
3x Knight
3x Archer    (positioned on HIGH GROUND at the gate — elevated bowfire over the approach)
Terrain: a castle GATE with a BRIDGE (chokepoint) and high ground for the archers.
```

Public walkthrough details:

```text
Recommended level: ~34.
Equip SAFEGUARD — the assault carries break pressure; protect your gear.
Marach advances over the BRIDGE; the 3 Archers hold HIGH GROUND and snipe the crossing.
No resupply into the Keep afterward — finish economically.
```

Design reading:

The Gate is **the storming-the-stronghold assault** that opens the Riovanes chain. Its identity is a
**bridge-and-high-ground crossing under break pressure**: a Knight line and a boss (Marach) contest
the bridge chokepoint while three Archers rain bowfire from elevation, and the player is told to
bring **Safeguard** because the assault threatens their gear. The deeper stakes are **resource
economy** — this is the on-ramp to the no-resupply Keep (Wiegraf → Velius), the hardest fight of the
chapter — so winning *cheaply* matters as much as winning. It tests chokepoint crossing, anti-air/
high-ground answers, break defense, and discipline before the spike.

For New Game++ the identity must stay: **a bridge-chokepoint assault on a gate where elevated archers
and a break-threatening line contest the crossing — won with Safeguard, high-ground answers, and
resource discipline, because the Velius spike follows with no resupply.**

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm slots: Marach + 3 Knight + 3 Archer, plus the player slots.
DO NOT touch Marach's survive/retreat scripting (he is recruitable later — he must NOT die here).
Keep the bridge chokepoint + the archers' high-ground positions (the crossing puzzle).
Confirm the NO-RESUPPLY chain link into the Keep — do not break the chain.
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
```

Job IDs (carry over known, verify the rest in-game):

```text
77 = Archer            (confirmed)
Knight job id          (TBD - verify)
Knights Templar job id (TBD - verify; from Izlude 028 — used below)
Marach boss job        (TBD - verify; Heaven/Nether line; survives)
```

## Job Escalation (Chapter 3 rule)

```text
CHANGE: swap ONE Knight -> a Knights Templar (Mighty Sword ranged breaks).
WHY: the original fight already DEMANDS Safeguard (break pressure) — the single, fitting escalation
  is to make that demand concrete and ranged: a Templar that breaks gear from across the bridge means
  the player genuinely needs Safeguard/Maintenance while crossing under archer fire. It INTENSIFIES
  the existing plan ("storm the bridge, protect your gear") rather than changing it, and reuses an
  ALREADY-INTRODUCED Ch3 caste (Izlude, 028) — NO brand-new caste here (Velius debuts at the Keep 034,
  the assassins at the Roof 035).
WHAT IS NOT CHANGED: the bridge chokepoint, the high-ground archers, and Marach the boss keep the
  assault identity; the strategy still holds.
```

## Sanctioned exceptions (carried precedents)

```text
TEMPLAR "MIGHTY SWORD" breaks — allowed, constrained (Izlude 028 precedent): the lone Templar breaks
  gear from range (telegraphed); Safeguard/Maintenance is the answer. It does NOT break every slot
  every turn.
KNIGHT Rend — allowed on ONE of the two remaining Knights only (<=2 break sources total counting the
  Templar): shop-tier breakable gear, Safeguard counter.
NO hard lock anywhere; Marach's boss skills constrained to damage/soft-status (no Stop/Don't Act).
```

## Boss rare loot

```text
None. Marach is a named boss but SURVIVES (recruitable later — he does not die here), so there is
nothing to drop (surviving/retreating boss = no rare, per Gallows 020 / Zalmo 026 / Yardow 031).
Generics stay shop-tier. The map's rare TREASURE (Fuma Shuriken / Aegis Shield / Diamond Helm /
Celebrant's Miter) is existing map treasure, not boss loot; leave it as-is.
```

## Proposed Composition (New Game++ Riovanes Gate v1)

Keep the count (7); swap one Knight for a Templar. Marach `103`; Templar `102`; Knights `101`;
Archers `100`–`102` (one elevated anchor at `102`).

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Marach (BOSS) | Heaven/Nether line | `103` | Advances over the bridge; boss pressure. Survives (no drop). |
| n | Templar (NEW swap) | Knights Templar | `102` | Mighty-Sword ranged breaks — makes Safeguard a must on the crossing. |
| n | Knight (Rend) | Knight | `101` | Bridge body; melee break-wall. |
| n | Knight | Knight | `101` | Second body; contests the chokepoint. |
| n | Archer (high) | Archer | `102` | Elevated anchor; commands the bridge with bowfire. |
| n | Archer (high) | Archer | `101` | Second elevated bow; crossfire on the crossing. |
| n | Archer | Archer | `100` | Third bow; covers a flank lane. |

Reasoning:

The faithful move is to **keep the bridge-and-high-ground assault and make the Safeguard demand real**.
Three Archers on elevation punish the crossing; the Knight line plus Marach contest the bridge
chokepoint; the swapped-in Templar breaks gear from range so Safeguard/Maintenance genuinely matters.
Marach pressures but survives (no kill, no drop). Crucially, this is the **on-ramp to the no-resupply
Keep**, so it should be winnable WITHOUT burning the resources the player needs for Velius — modest
levels and a clean "cross the bridge, answer the high ground, protect your gear" puzzle, not an
attrition trap. A clear assault step below the Keep spike.

## Builds (final-shop quality; Templar stronghold garrison flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Marach — BOSS (Lv 103) — survives, no drop

```text
Job: Heaven/Nether line (id TBD)   JobLevel: 8   Primary: his canonical skillset (damage/soft-status only)
Reaction: a defensive reaction (id TBD)   Support: Attack Boost (465) or MA-boost (id TBD)
Movement: Movement +1 (486)
Head/Body: shop gear his job allows (ids TBD)   Accessory: Bracers (218)
Right hand: shop-tier weapon (id TBD; NOT a rare — he survives, nothing drops)
SURVIVES — do NOT let him die here; no rare loot at the Gate.
```

Role: boss pressure advancing over the bridge; survives the battle.

### Knights Templar (Lv 102) — NEW swap

```text
Job: Knights Templar (id TBD)   JobLevel: 8   Primary: Mighty Sword (ranged equip/stat break)
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head/Body: shop helm + medium/heavy armor (ids TBD)
Accessory: Bracers (218)   Right hand: shop-tier-best sword (id TBD; not a reserved best)   Left: shop shield (id TBD)
```

Role: the ranged break threat that makes Safeguard mandatory on the crossing.

### Knight x2 (Lv 101) — 1x Rend

```text
Job: Knight (id TBD)   JobLevel: 8   Secondary: Rend (break) on ONE of the two (id TBD)
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head/Body: shop heavy helm + heavy armor (ids TBD)
Accessory: Bracers (218)   Right hand: Runeblade (30) / Icebrand (29)   Left: shop shield (id TBD)
```

Role: bridge bodies that contest the chokepoint.

### Archer x3 (Lv 102 / 101 / 100) — high ground

```text
Job: Archer (77)   JobLevel: 8   Secondary: none
Reaction: Reflexes (449)   Support: Concentration (469)   Movement: Movement +1 (486)
Head: Thief's Cap (168)   Body: Black Garb (198)   Accessory: Bracers (218)
Right hand: Windslash Bow (87)   Left: none / two-hand marker (254)
```

Role: elevated bowfire commanding the bridge — the high-ground problem to answer.

## Positioning Plan

```text
The 3 Archers start on the gate's HIGH GROUND with sightlines over the bridge crossing.
The Knight line + the Templar hold the bridge chokepoint; Marach advances over the bridge.
Preserve the bridge chokepoint + archer high ground + the NO-RESUPPLY chain link into the Keep.
Do NOT alter Marach's survive scripting.
```

The gate should say: "cross the bridge under their archers, keep your blades from the Templar's
reach, and don't spend what you'll need upstairs — the worst is still ahead."

## Implementation Checklist

- [ ] Identify Riovanes Gate `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify Marach + 3 Knight + 3 Archer + player slots.
- [ ] Confirm Knight / Templar / Marach job ids; keep Mighty-Sword breaks telegraphed.
- [ ] Swap ONE Knight -> Templar; Rend on ONE of the remaining Knights (<=2 break sources total).
- [ ] Constrain Marach to damage/soft-status (no hard lock); give him a NON-RARE weapon (no drop).
- [ ] Set levels: Marach `103`; Templar + one elevated Archer `102`; Knights + second Archer `101`;
      third Archer `100`.
- [ ] Set JobLevel `8` on all active enemy slots.
- [ ] PRESERVE Marach's survive scripting, the bridge/high-ground geometry, and the chain link.
- [ ] Patch via the correct layer; keep the diff inside the Riovanes Gate window only.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify chain + Marach intact.
- [ ] Install mod, test from a New Game+ save; confirm it's winnable economically into the Keep.

## Test Questions

- Does the bridge chokepoint + elevated archers make the crossing a real positional puzzle?
- Does the Templar's ranged break make Safeguard genuinely worth equipping (not a trap)?
- Is break pressure capped fairly (<=2 sources, all Safeguard-counterable, no hard lock)?
- Does Marach survive (no kill, no drop), consistent with him being recruitable later?
- Is the fight winnable WITHOUT burning the resources needed for the no-resupply Keep (Velius)?
- Is it an assault step above Yuguewood but clearly below the Keep spike?
- Does it still read as storming a castle gate, not a designed arena?

## Sources

- Game8, "Riovanes Castle Gate Walkthrough (Battle 30)": roster (Marach + 3 Knight, 3 Archer),
  objective "Defeat all enemies!", recommended level ~34, deploy 5, bridge + high-ground archers,
  equip Safeguard, no-resupply chain into the Keep, rewards/treasure.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553190
- Final Fantasy Wiki, "Riovanes Castle": story/terrain context.
  https://finalfantasy.fandom.com/wiki/Riovanes_Castle
- Local: `docs/battles/024-chapter-3-overview.md` (job-escalation + rare-loot rules),
  `028-monastery-vaults-3rd.md` (Templar Mighty-Sword), `031-walled-city-yardrow.md` (Marach survives),
  `005-sand-rat-sietch.md` (chokepoint control), `029-monastery-vaults-1st.md` (no-resupply chain).
</content>
