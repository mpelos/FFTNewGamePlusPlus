# 033 - Riovanes Castle Gate

Status: ✅ implemented (v1, entry 431) — NG+ only; pending playtest. **v2 redesign documented only** (implementation pending).
Chapter: 3 — "The Valiant"
Battle order: Battle 30 (after The Yuguewood) — **Riovanes chain 1 of 3**
Target version: Enhanced v1.5.0
ENTD: global entry **431** (local entry 47, `battle_entd4_ent.bin`)
File: `battle_entd4_ent.bin` (embedded NG+ swap) — `tools/battle_patch.py riovanes_gate`

Implemented composition (entry 431, vanilla-dump verified) — TIC has **4 Knights** (one more than
the walkthrough's 3), so after the Templar swap there are 3 Knights + 1 Templar:
- s1 **Marach** (job 26 Netherseer — enemy BOSS, survives/recruitable): L103 + durability gear
  (Mage Hat/shop Robe/Bracers — naked); job/jobLevel/secondary/weapon/survive scripting preserved. NO rare.
- s5 Knight→**Knights Templar** (job 38, the Izlude caste) L102 — Mighty-Sword ranged breaks; Heavy
  Helm/Heavy Armor/Bracers/Runeblade/shop Shield; Counter/Atk Boost/Mv+1.
- s6,s7,s8 Knight L101 — Heavy Helm/Heavy Armor/Bracers/Runeblade/shop Shield; Rend innate; Counter/Atk Boost/Mv+1.
- s2,s3,s4 Archer L102/L101/L100 (s2 = high anchor) — Thief's Cap/Black Garb/Bracers/Windslash (two-hand); Reflexes/Concentration/Mv+1.
- s0 = Rapha placeholder (level 0xFE) — left untouched.

> ⚠️ Verify in-game: job 38 (Knights Templar) is applied to a generic sprite (s5) — Izlude's job on a
> generic slot. Confirm it renders and uses Mighty Sword correctly; if not, fall back to a Knight with
> heavy break gear.

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
ENTD entry 431 confirmed in `024-chapter-3-overview.md` and v1 implementation.
TIC roster differs from the public walkthrough: Marach + 4 Knight + 3 Archer, plus player slots.
v1/v2 active roster after the one-Knight Templar swap: Marach + 1 Templar + 3 Knight + 3 Archer.
DO NOT touch Marach's survive/retreat scripting (he is recruitable later — he must NOT die here).
Keep the bridge chokepoint + the archers' high-ground positions (the crossing puzzle).
Confirm the NO-RESUPPLY chain link into the Keep — do not break the chain.
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
```

Job IDs (carry over known, verify the rest in-game):

```text
77 = Archer            (confirmed)
26 = Marach Netherseer enemy boss (confirmed from Yardow/Gate recurrence)
38 = Knights Templar special (confirmed from Izlude 028 / v1 generic swap; verify generic rendering)
76 = Knight (confirmed generic Knight id in local docs)
```

## Enemy Party Escalation (Chapter 3 redesign)

```text
VANILLA SPIRIT: storm a bridge under high-ground archers while Marach and a break-capable line
  contest the crossing before the no-resupply Keep.
CHAPTER-3 UPGRADE: keep the confirmed eight-active-unit TIC roster, but complete every active human
  setup with secondary/reaction/support/movement. One Knight remains swapped to Templar; only one
  generic Knight carries Rend.
WHY: the original already demands Safeguard. The Templar makes that demand concrete from range, but
  all-Rend Knights, a second Templar, or hard-lock Marach would overtax the Riovanes chain before
  Wiegraf/Belias.
WHAT IS NOT CHANGED: the answer remains cross the bridge economically, solve the high-ground archers,
  protect gear with Safeguard/Maintenance, and preserve resources for Keep.
```

Chapter 3 requirements applied:

```text
- Every active human enemy has full equipment.
- Every active human enemy has secondary, reaction, support, and movement.
- The party has real synergy: Templar break pressure + one Rend body + bridge bodies + elevated
  archers + Marach pressure.
- No guests are present.
- No second Templar, no all-Rend bridge, no hard-lock Marach.
```

## Sanctioned exceptions (carried precedents)

```text
TEMPLAR "MIGHTY SWORD" breaks — allowed, constrained (Izlude 028 precedent): the lone Templar breaks
  gear from range (telegraphed); Safeguard/Maintenance is the answer. It does NOT break every slot
  every turn.
KNIGHT Rend — allowed on ONE of the three remaining Knights only (<=2 break sources total counting
  the Templar): shop-tier breakable gear, Safeguard counter.
NO hard lock anywhere; Marach's boss skills constrained to damage/soft-status (no Stop/Don't Act).
```

## Boss rare loot

```text
None. Marach is a named boss but SURVIVES (recruitable later — he does not die here), so there is
nothing to drop (surviving/retreating boss = no rare, per Gallows 020 / Zalmo 026 / Yardow 031).
Generics stay shop-tier. The map's rare TREASURE (Fuma Shuriken / Aegis Shield / Diamond Helm /
Celebrant's Miter) is existing map treasure, not boss loot; leave it as-is.
```

## Proposed Composition (New Game++ Riovanes Gate v2)

Keep the confirmed TIC/v1 count (8); swap one of the four Knights for a Templar. Marach `103`;
Templar `102`; Knights `101`; Archers `100`–`102` (one elevated anchor at `102`).

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Marach (BOSS) | Heaven/Nether line | `103` | Advances over the bridge; boss pressure. Survives (no drop). |
| n | Templar (NEW swap) | Knights Templar | `102` | Mighty-Sword ranged breaks — makes Safeguard a must on the crossing. |
| n | Knight (Rend) | Knight | `101` | Bridge body; melee break-wall. |
| n | Knight | Knight | `101` | Second body; contests the chokepoint. |
| n | Knight | Knight | `101` | Third body from TIC; blocks without adding Rend. |
| n | Archer (high) | Archer | `102` | Elevated anchor; commands the bridge with bowfire. |
| n | Archer (high) | Archer | `101` | Second elevated bow; crossfire on the crossing. |
| n | Archer | Archer | `100` | Third bow; covers a flank lane. |

Reasoning:

The faithful move is to **keep the bridge-and-high-ground assault and make the Safeguard demand real**.
Three Archers on elevation punish the crossing; the Knight line plus Marach contest the bridge
chokepoint; the swapped-in Templar breaks gear from range so Safeguard/Maintenance genuinely matters.
The confirmed TIC extra Knight stays active, but only one Knight carries Rend, so the eight-body
action economy becomes bridge pressure instead of a gear-break grinder. Marach pressures but survives
(no kill, no drop). Crucially, this is the **on-ramp to the no-resupply Keep**, so it should be
winnable WITHOUT burning the resources the player needs for Velius — a clean "cross the bridge,
answer the high ground, protect your gear" puzzle, not an attrition trap.

## Builds (final-shop quality; Templar stronghold garrison flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Marach — BOSS (Lv 103) — survives, no drop

```text
Job: Heaven/Nether line (26)   JobLevel: 8   Primary: his canonical skillset (damage/soft-status only)
Secondary: Item / basic support equivalent; no second status/control engine
Reaction: a defensive reaction (id TBD)   Support: Attack Boost (465) or MA-boost (id TBD)
Movement: Movement +1 (486)
Head/Body: shop gear his job allows (ids TBD)   Accessory: Bracers (218)
Right hand: shop-tier weapon (id TBD; NOT a rare — he survives, nothing drops)
SURVIVES — do NOT let him die here; no rare loot at the Gate.
```

Role: boss pressure advancing over the bridge; survives the battle.

### Knights Templar (Lv 102) — NEW swap

```text
Job: Knights Templar (38)   JobLevel: 8   Primary: Templar/basic command
Secondary: Mighty Sword (ranged equip/stat break)
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head/Body: shop helm + medium/heavy armor (ids TBD)
Accessory: Bracers (218)   Right hand: shop-tier-best sword (id TBD; not a reserved best)   Left: shop shield (id TBD)
```

Role: the ranged break threat that makes Safeguard mandatory on the crossing.

### Knight x3 (Lv 101) — 1x Rend

```text
Job: Knight (76)   JobLevel: 8
Secondary: Knight A = Rend (break) / Knights B-C = Item or Fundaments equivalent (NO Rend)
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head/Body: shop heavy helm + heavy armor (ids TBD)
Accessory: Bracers (218)   Right hand: Runeblade (30) / Icebrand (29)   Left: shop shield (id TBD)
```

Role: bridge bodies that contest the chokepoint.

### Archer x3 (Lv 102 / 101 / 100) — high ground

```text
Job: Archer (77)   JobLevel: 8   Primary: Aim/Charge
Secondary: Item or Fundaments equivalent; no hard status
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

## Simulation Plan and Results

Simulation artifact:

```text
tmp/fft-level-design-033-riovanes-castle-gate/
```

Model scope:

```text
First five rounds only; compares action economy, break-source count, high-ground archer pressure,
bridge pressure, chain strain into Keep, and answerability. It tests whether the confirmed
eight-active-unit TIC roster can stay fair when every setup is complete.
```

Iteration results:

| Candidate | Enemies | Action ratio | Break sources | Break threat | Archer threat | Bridge threat | Total pressure | High-ground answer | Chain strain | Answerability | Result |
|-----------|---------|--------------|---------------|--------------|---------------|---------------|----------------|--------------------|--------------|---------------|--------|
| v1 eight-body gate shell | 8 | 1.12 | 2 | 48.0 | 51.2 | 33.1 | 155.6 | 59.5 | 30.5 | 67.3 | Baseline |
| v2 complete chain-safe gate assault | 8 | 1.18 | 2 | 49.8 | 54.5 | 35.3 | 175.6 | 65.8 | 31.6 | 65.6 | Accepted |
| Seven-body trimmed gate | 7 | 1.04 | 2 | 49.8 | 54.5 | 21.3 | 161.5 | 70.2 | 30.2 | 68.8 | Considered: safer but drops confirmed TIC body |
| All-Rend bridge grinder | 8 | 1.18 | 4 | 75.8 | 54.5 | 37.6 | 203.8 | 56.6 | 35.7 | 58.7 | Rejected: too many break sources / chain tax |
| Second Templar bridge lock | 8 | 1.18 | 3 | 86.6 | 54.5 | 23.6 | 200.6 | 58.0 | 35.9 | 59.3 | Rejected: second Templar / chain tax |
| Hard-lock Marach bridge | 8 | 1.18 | 2 | 49.8 | 54.5 | 35.3 | 211.6 | 65.8 | 39.2 | 38.3 | Rejected: hard-lock / chain tax |

Decision:

```text
Use the confirmed eight-body TIC roster, but cap break pressure at the Templar plus one Rend Knight
and keep Marach soft. Do not trim the extra Knight in the doc pass; instead make the third Knight a
non-Rend body and validate chain strain into Keep. Reject all-Rend, second Templar, and hard-lock
Marach variants.
```

## Current Implementation (v1, entry 431 — superseded by v2 design)

The shipped v1 already establishes the confirmed eight-active-unit TIC roster, one generic Templar
swap, high-ground archers, Marach survival, and the chain into Keep. The v2 redesign above is
**documentation only** in this pass; it requires a later implementation pass to complete secondary
setups and verify the eight-body chain tax in-game.

## Future Implementation Checklist (v2)

- [x] Identify Riovanes Gate ENTD entry 431; fill "Local Data Confirmed".
- [x] Dump original entry; verify Marach + 4 Knight + 3 Archer + player slots.
- [ ] Confirm generic job 38 Templar renders/acts correctly; if not, fall back to a Knight with
      limited break gear and document the implementation limitation.
- [ ] Swap ONE Knight -> Templar; Rend on ONE of the three remaining Knights (<=2 break sources total).
- [ ] Constrain Marach to damage/soft-status (no hard lock); give him a NON-RARE weapon (no drop).
- [ ] Set levels: Marach `103`; Templar + one elevated Archer `102`; Knights + second Archer `101`;
      third Archer `100`.
- [ ] Set JobLevel `8` on all active enemy slots.
- [ ] Give every active human enemy full equipment plus secondary/reaction/support/movement.
- [ ] Preserve Riovanes chain economy: no all-Rend setup, no second Templar, no hard-lock Marach.
- [ ] PRESERVE Marach's survive scripting, the bridge/high-ground geometry, and the chain link.
- [ ] Patch via the correct layer in a later implementation pass; no binary/data change in this doc pass.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify chain + Marach intact.
- [ ] Install mod, test from a New Game+ save; confirm it's winnable economically into the Keep.

## Test Questions

- Does the bridge chokepoint + elevated archers make the crossing a real positional puzzle?
- Does the Templar's ranged break make Safeguard genuinely worth equipping (not a trap)?
- Is break pressure capped fairly (<=2 sources, all Safeguard-counterable, no hard lock)?
- Does the confirmed eighth enemy add bridge pressure without making the Keep chain feel starved?
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
- Local: `docs/battles/024-chapter-3-overview.md` (Chapter 3 complete-party + rare-loot rules),
  `028-monastery-vaults-3rd.md` (Templar Mighty-Sword), `031-walled-city-yardrow.md` (Marach survives),
  `005-sand-rat-sietch.md` (chokepoint control), `029-monastery-vaults-1st.md` (no-resupply chain).
