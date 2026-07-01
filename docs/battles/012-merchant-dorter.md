# 012 - Merchant City of Dorter (Chapter 2)

Status: ⏳ v2 applied (entry 403) — BM fast/power split live; true slot-add 7th enemy validated in-game via `event119.e`; pending NG+ placement check for the new Knight
Chapter: 2 — "The Manipulator and the Subservient"
Battle order: Battle 11 (Chapter 2 opener)
Target version: Enhanced v1.5.0
ENTD: global entry **403** (battle_entd4, local entry 19) — confirmed by composition matching
File: `entd/battle_entd4_ent.bin` (embedded; swapped only in NG+ by the code mod)

> Implemented via `tools/battle_patch.py merchant_dorter`. The whole ENTD is swapped only in NG+,
> so the edit is automatically NG+-only — a first playthrough is untouched. See
> `011-chapter-2-overview.md`.

## Original Battle

Objective:

```text
Defeat all enemies!
```

Player deployment:

```text
Up to 4 units, including Ramza.
Allies: Gaffgarion and Agrias contribute automatically as story units.
```

Original enemy composition:

```text
2x Archer
2x Black Mage
2x Thief   (male — carry Steal Heart / charm)
```

Public walkthrough details:

```text
Recommended level: ~10.
Compact urban map; Archers stationed on higher tiles (rooftop/elevation pressure).
The Black Mages are the biggest danger — AoE spells devastate clustered units.
The male Thieves can Steal Heart (charm) female party members and turn them against you;
  the standard counter is an all-male party.
This is the mercenary-era return to Dorter: a coordinated band, not Chapter 1's deserters.
```

Design reading:

This is Dorter revisited as a **mercenary ambush** — and the contrast with Chapter 1's Dorter
is the point. Where the Chapter 1 fight was a melee/ranged wall on the rooftops, this band is
all *finesse*: elevated archers, AoE black magic, and **charm thieves**. It teaches the player
(again) to fight the high ground, but now adds **don't clump into AoE** and **protect against
charm**. It is the Chapter 2 opener and should feel like a clear step up from anything in
Chapter 1 — coordinated, multi-threat, and punishing of a careless formation.

For New Game++ the identity must stay: **a coordinated urban ambush where elevation, AoE magic,
and charm all pressure the player's formation at once — a finesse fight, not a brawl.**

## Local Data Confirmed (entry 403)

Dumped from the embedded ENTD; roster matches the doc exactly (2 Archer + 2 Black Mage + 2 Thief).

```text
slot  cid    name  job          role                         action
s0    0x24   36    36           Gaffgarion — scripted ally   LEAVE (lvl 254, story unit)
s1    0x80   255   83 Thief     enemy Thief                  SCALE -> L100
s2    0x17   23    23           Agrias — scripted ally       LEAVE (lvl 254, flags 0x89 ally)
s3    0x34   52    52           named story unit             LEAVE (lvl 254)
s4    0x81   255   77 Archer    enemy Archer (elevated)      SCALE -> L101
s5    0x81   255   77 Archer    enemy Archer (elevated)      SCALE -> L100
s6    0x80   255   83 Thief     enemy Thief                  SCALE -> L100
s7    0x80   255   80 BlackMage enemy Black Mage             SCALE -> L101
s8    0x80   255   80 BlackMage enemy Black Mage             SCALE -> L101
```

Job IDs: Archer 77, Thief 83, Black Mage 80 (all confirmed; shared with Ch1). **Steal Heart (charm)
is innate to the Thief job command at JobLevel 8** — no secondary skillset is needed to deliver the
fight's signature charm threat. The Gaffgarion/Agrias/story slots are all lvl 254 in the base ENTD
(enabled by story scripting) and are left untouched.

## Enemy Party Escalation (Chapter 2 redesign)

```text
VANILLA SPIRIT: a coordinated city ambush where rooftops, Black Magic, and charm punish a bad
  formation.
CHAPTER-2 UPGRADE: keep the full 2 Archer / 2 Black Mage / 2 Thief core, add exactly ONE Knight
  captain as the street anchor, and tune the two Black Mages as real endgame casters instead of
  adding extra bodies or extra status.
WHY: a single anchor forces the player to route around or break a front line before deleting the
  mages. Optimized Black Mages make the original "do not clump" lesson matter to a tuned NG+
  party. Two anchors were rejected because they turn the opener into cleanup.
WHAT IS NOT CHANGED: the fight is still won by reading high ground, caster priority, and charm
  risk. It is not a Chapter-3 synergy puzzle and not a Chapter-4 broken-build puzzle.
```

Chapter 2 requirements applied:

```text
- Every active human enemy has full equipment.
- Every active human enemy has intentional reaction, support, and movement.
- Secondary is optional; it appears only when it clarifies the unit's role.
- Mime and Calculator/Arithmetician remain banned.
- No Stop / Don't Act / Petrify / Death spam is introduced.
```

## Sanctioned exception — charm (Steal Heart) stays

The Chapter 1 rules banned charm. **Here it is canonical and telegraphed** (the fight is built
around it; the guide tells the player to bring male units). So it stays, constrained:

```text
ALLOWED: Steal Heart on the two Thieves (the fight's signature threat).
GUARDRAIL: only the two canonical Thieves carry it; no other charm sources. The player's
  counter (all-male party / charm-immune accessory) remains valid, so it is fair at NG+ scale.
```

## Boss rare loot

```text
None. This is NOT a boss battle, so no rare non-buyable item is granted (per the Chapter 2
overview, rare loot is reserved for boss battles — Gaffgarion and Cúchulainn). Generics stay
on strong shop-tier gear.
```

## Guest handling

```text
Gaffgarion and Agrias are active story allies here. In NG+ they must be player-controlled under
the global guest-control rule. The redesign does not use their AI as a skill check; it assumes the
player can route them deliberately against the ambush.
```


Fixed encounter Brave/Faith targets:

| Unit | Br/Fa | Rationale |
|------|-------|-----------|
| Gaffgarion story ally | `74/55` | Story ally pressure without making his later betrayal/boss forms inherit an overtuned value. |
| Agrias story ally | `76/65` | Physical Holy Knight ally; enough Faith for support magic interaction without turning enemy magic into a coin flip. |

## Proposed Composition (New Game++ Merchant Dorter v2)

Keep the original six and add one Knight captain (7 enemies). The enemy side is complete, but
still readable:

```text
1 frontline anchor
2 elevated ranged attackers
2 optimized AoE casters
2 fast charm/flank threats
```

| Slot | Role | Job | Level | Br/Fa | Purpose |
| ------ | ------ | ----- | ------- | --- | --------- |
| n | Street Captain (NEW) | Knight | `102` | `76/48` | Frontline wall; slows the rush without adding hard control. |
| n | Rooftop Archer | Archer | `101` | `74/50` | Elevated ranged pressure; the classic Dorter menace. |
| n | Rooftop Archer | Archer | `100` | `74/50` | Second elevated bow; covers the other approach. |
| n | Fast Black Mage | Black Mage | `102` | `55/76` | Swiftness caster; makes the first AoE race real. |
| n | Power Black Mage | Black Mage | `101` | `55/76` | Arcane Strength caster; punishes clumped targets. |
| n | Thief (charm) | Thief | `100` | `78/48` | Steal Heart pressure + fast harassment. |
| n | Thief (charm) | Thief | `100` | `78/48` | Second charm threat; splits the player's caution. |

Reasoning:

The original band is already the platonic "finesse ambush," so the move is to give that band a
complete NG+ version: a single bodyguard, high-ground ranged pressure, two real caster builds, and
the canonical charm thieves. The player still has fair answers: split formation, rush or silence
the casters, disarm/burst the Knight, climb to the archers, or bring charm immunity/all-male units.

## Builds (final-shop quality; coordinated mercenary band flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Street Captain — Knight (Lv 102) — NEW

```text
Job: Knight (id TBD)   JobLevel: 8   Secondary: none (NO Rend/Battle Skill this fight)
Reaction: Counter (442)   Support: Defense Boost (id TBD)
Movement: Movement +1 (486)
Head/Body: shop heavy helm + heavy armor (ids TBD)
Accessory: Bracers (218)
Right hand: Runeblade (30) or Icebrand (29)   Left hand: shop shield (id TBD)
```

Role: the wall the original band lacked. Stalls the street so the casters/archers get real turns.
No Rend here: the chapter opener previews formation pressure, not gear-break pressure.

### Archer x2 (Lv 101 / 100)

```text
Job: Archer (77)   JobLevel: 8   Secondary: none
Reaction: Reflexes (449)   Support: Concentration (469)   Movement: Movement +1 (486)
Head: Thief's Cap (168)   Body: Black Garb (198)   Accessory: Bracers (218)
Right hand: Windslash Bow (87)   Left hand: none / two-hand marker (254)
```

Role: elevated harassment. Concentration keeps them relevant against evasive NG+ units.

### Black Mage x2 (Lv 102 / 101)

```text
Fast Black Mage:
Job: Black Mage (id TBD)   JobLevel: 8   Secondary: none
Reaction: Mana Shield (id TBD)   Support: Swiftness (id TBD)   Movement: Movement +1 (486)
Head: cloth/mage hat (id TBD)   Body: shop robe (id TBD)
Accessory: Featherweave Cloak (234)   Right hand: shop magic-boost rod (id TBD)   Left: none (255)

Power Black Mage:
Job: Black Mage (id TBD)   JobLevel: 8   Secondary: none
Reaction: Reflexes (449)   Support: Arcane Strength (id TBD)   Movement: Movement +1 (486)
Head: cloth/mage hat (id TBD)   Body: shop robe (id TBD)
Accessory: Featherweave Cloak (234)   Right hand: shop magic-boost rod (id TBD)   Left: none (255)
```

Role: the AoE that punishes clumping — the biggest threat, exactly as the walkthrough warns.
The fast mage creates the race; the power mage creates the punishment. No status magic is added.

### Thief x2 (Lv 100) — charm

```text
Job: Thief (83)   JobLevel: 8   Secondary: Steal (incl. Steal Heart — the fight's signature)
Reaction: First Strike (453)   Support: Attack Boost (465)   Movement: Movement +2 (487)
Head: Thief's Cap (168)   Body: Black Garb (198)   Accessory: Germinas Boots (210)
Right hand: Air Knife (9)   Left hand: none / two-hand marker (254)
```

Role: fast charm harassment. Forces the player to respect formation and unit gender/immunity.

## Positioning Plan

```text
Knight starts on the ground at the main approach, between the player and the backline, but not
  on a tile that seals every route.
Both Archers start on the elevated tiles (rooftops/high ground) with wide sightlines.
Fast Black Mage starts where the first spell threatens the obvious clustered approach.
Power Black Mage starts farther back, protected but reachable by a committed rush.
Both Thieves start on the flanks with movement lanes to dart at the player's formation.
Do NOT alter the Gaffgarion/Agrias ally placements except for the NG+ player-control flag.
```

The map should read: "a wall up front, archers above, mages lobbing AoE, and charm-thieves
circling" — a formation problem, the Chapter 2 escalation of Dorter's high-ground lesson.

## Simulation Plan and Results

Simulation artifact:

```text
tmp/fft-level-design-012-merchant-dorter/
```

Model scope:

```text
First four rounds only; compares action economy and weighted pressure. It does not claim exact FFT
damage. It checks whether the opener gains meaningful pressure without adding hard-lock or cleanup.
```

Iteration results:

| Candidate | Enemy actions | Action ratio | Pressure | Delta vs v1 | Result |
|-----------|---------------|--------------|----------|-------------|--------|
| v1 current: 2 Archer, 2 Black Mage, 2 Thief | 24.0 | 1.00 | 56.6 | 0.0% | Baseline |
| Add 2 Knight anchors | 31.2 | 1.30 | 69.6 | +23.0% | Rejected: too much bodyblock/cleanup |
| Add 1 Knight anchor only | 27.6 | 1.15 | 63.1 | +11.5% | Fair but soft |
| Add 1 Knight anchor + optimized Black Mages | 28.4 | 1.18 | 67.8 | +19.8% | Accepted |

Decision:

```text
Use one Knight captain and two optimized Black Mages. Do not add a second anchor, a third charm
source, a third AoE source, or any hard-lock status. The accepted version raises pressure enough for
the Chapter-2 opener while preserving the original answers.
```

## Current Implementation (v1, entry 403 — superseded by v2 design)

Applied with `python tools/battle_patch.py merchant_dorter`; diff contained to local entry 19
(global 403), 58 bytes.

```text
s4  Archer     L101 jl8  R Reflexes  S Concentration  M +1  Thief's Cap / Black Garb / Bracers + Windslash Bow
s5  Archer     L100 jl8  (same kit)
s7  Black Mage L101 jl8  R Reflexes  M +1  Mage Hat / shop Robe / Featherweave + shop Rod
s8  Black Mage L101 jl8  (same kit)
s1  Thief      L100 jl8  R First Strike  S Atk-Boost  M +2  Thief's Cap / Black Garb / Germinas + Air Knife
s6  Thief      L100 jl8  (same kit)  — Steal Heart innate to the Thief job
```

## v2 Implementation (entry 403)

Applied in-place to the embedded `battle_entd4_ent.bin` via `tools/battle_patch.py merchant_dorter`
(NG+-only via the code mod's .bin swap). The two Archers (s4/s5) and two Thieves (s1/s6) already
matched the v2 builds, so the live changes are the Black Mage split + the new 7th-enemy Knight. The
doc's "id TBD" were resolved against the installed loader tables:

```text
Swiftness      = Swiftspell 482   (魔法詠唱短縮 / Short-Charge — fast caster support)
Arcane Strength = Magick Boost 467 (魔法攻撃アップ / MA-up)
Defense Boost  = 466,  Mana Shield = 445,  Counter = 442,  Reflexes = 449,  Movement +1 = 486
Knight 76 / Black Mage 80; Heavy Helm 154 / Heavy Armor 182 / Bracers 218 / Runeblade 30 /
Crystal Shield 139; Mage Hat 167 / Luminous Robe 206 / Featherweave 234 / shop Rod 56.
```

Builds:

```text
s7 Fast Black Mage  -> L102 jl8  R Mana Shield(445)  S Swiftspell(482)   M +1  Mage Hat/Robe/Featherweave/Rod
s8 Power Black Mage -> L101 jl8  R Reflexes(449)     S Magick Boost(467) M +1  Mage Hat/Robe/Featherweave/Rod
s1/s6 Thieves       -> L100 jl8  R First Strike(453) S Attack Boost(465) M +2  Thief's Cap/Black Garb/Germinas/Air Knife
s9 Street Captain   -> L102 jl8  R Counter(442)      S Defense Boost(466) M +1
   Heavy Helm/Heavy Armor/Bracers/Runeblade/Crystal Shield; secondary none.
```

### The 7th-enemy Knight: first attempt, root cause, and the fix

> 2026-06-30 correction: the earlier "slot-add is impossible" conclusion was wrong. The validated
> rule for this event-scripted battle is three-layer authoring: ENTD slot + copied/retargeted
> `event119.e` spawn block + adding the new uid to the script's late `45` list. With `45 86 00 01`
> added after `45 84`/`45 85`, s9/uid `0x86` became a real active enemy in-game
> (`st=0x09`, `aux1b5=0x01`). The temporary s6 Thief -> Knight job-swap is reverted; s6 is again a
> Thief, and s9 is the only Knight captain. Current tuning is placement only: first successful s9
> spawn landed on the roof at `(7,10)`; `(6,9)` and `(5,9)` were valid ground but still behind/side
> of the nearby Archer, so the next test moves him to `(5,7)` to stand in front of her.

The first v2 build added the Knight by cloning the Ch1 Dorter Knight (385 s3) onto s9 at tile (2,5).
In-game it failed four ways: on a rooftop, **a Thief portrait**, facing backward, and **present during
the story intro** (before the other enemies arrive). Investigation (2026-06-30) found the real cause —
and disproved two earlier guesses:

```text
NOT a sprite/VRAM cap: a census of all 512 vanilla ENTD entries shows battles routinely load 7-16
  distinct sprites (entry 383 loads 16). Vanilla 403 uses 6; a 7th is well within range.
NOT OverrideEntryData: entry 403's NXD OverrideEntryData rows (work/enhanced_0004.sqlite) are ALL
  sentinel (Spriteset 0, MainJob 0, Level -1, Present 255, Pos -1). Spriteset is set in only 4 rows
  in the whole game. So the .bin is authoritative for 403 — the override layer is not gating sprites.
ROOT CAUSE = the ENTD flags byte (0x18). The cloned 385 s3 is a LoadFormation unit (bit 0x80,
  flags 0x90) = present in the tactical-view intro. During that intro only the intro's sprite set is
  loaded, so the Knight fell back to an already-loaded sprite (the Thief = problem #2). The real
  Dorter enemies (s4-s8) are REINFORCEMENTS (flags 0x10, NO LoadFormation): they appear AFTER the
  intro, so their sprites load with the battle proper.
```

First fix tried (s9 as a `0x10` reinforcement, cloned from s8, unique unit-id, ground tile (4,1)):
**ENTD-only did not spawn it.** That proved the enemy wave is event-scripted, but not that slot-add
is impossible.

Final fix (`merchant_dorter()` + `event119.e`): deliver the Knight as a true slot-add. The ENTD
creates s9/uid `0x86`; `event119.e` copies and retargets the uid `0x85` wave block to uid `0x86`;
and the late event-script list includes `45 86 00 01`. Cost: one external script override plus the
embedded ENTD update. Result: **7 enemies**, with s6 restored to Thief and s9 as the only Knight.

Guest control (Gaffgarion `0x24` / Agrias `0x17`) is handled by the runtime scaler
(`Program.cs` `GuestCharIds` + non-enemy-team guard), **not** by ENTD flag edits.

Pending NG+ in-game test:
```text
1. Does the s9 Knight render as a real Knight and start on a valid ground tile at (5,7), directly in front of the nearby Archer?
2. Does the full 7-enemy formation preserve the intended pressure: 2 Archer / 2 Black Mage / 2 Thief / 1 Knight?
3. BM threat at scale; charm fairness with two Thieves restored.
```

## Future Implementation Checklist (v2)

- [x] Identify Merchant Dorter ENTD entry (403) on Windows data; fill "Local Data Confirmed".
- [x] Dump original entry; verify 2 Archer + 2 Black Mage + 2 Thief + ally slots.
- [x] Confirm Black Mage / Archer / Thief job IDs and legal equipment.
- [x] Knight captain delivered as a true 7th enemy: s9/uid `0x86` in ENTD + retargeted `event119.e`
  spawn block + `45 86 00 01` in the late event-script list. First at-start clone of 385 s3 had failed
  on rooftop / Thief sprite / backward / intro.
- [x] Set levels: Knight `102`, fast Black Mage `102`, power Black Mage + lead Archer `101`,
  second Archer + Thieves `100`.
- [x] Set JobLevel `8` on all active enemy slots.
- [x] Keep Steal Heart on exactly the two canonical Thieves; add no other charm source.
- [x] Give every active human enemy complete equipment plus intentional reaction/support/movement.
- [x] Set Gaffgarion and Agrias player-controlled in NG+ (runtime scaler / `GuestCharIds`; not ENTD edits).
- [x] Patch the embedded ENTD (entry 403, slots s1/s6/s7/s8/s9) and `event119.e`.
- [x] Re-dump and diff; confirm changes are contained to entry 403.
- [x] Build/deploy with the game closed (verified in the embedded DLL + external `event119.e`).
- [ ] NG+ in-game test: s9 Knight starts on valid ground at `(5,7)` in front of the nearby Archer; BM threat at scale; charm fairness with two Thieves restored.

## Test Questions

- Does one Knight captain create a real route/target-priority decision without turning Dorter into
  a slow bodyblock cleanup?
- Are the two optimized Black Mages still the biggest threat at scale?
- Is the charm (Steal Heart) a fair, telegraphed threat the player can counter, not a coin-flip loss?
- Do Gaffgarion and Agrias behave correctly as player-controlled NG+ guests?
- Does it clearly read as a step up from Chapter 1 Dorter — coordinated finesse, not a brawl?
- Is it a fitting Chapter 2 opener: harder than Ch1 but not a wall this early in the chapter?
- Does it still feel like a mercenary ambush in the merchant city, not a designed arena?

## Sources

- Game8, "Merchant City of Dorter Walkthrough (Battle 11)": roster (2 Archer, 2 Black Mage,
  2 Thief), objective "Defeat all enemies!", deploy 4, recommended level ~10, elevated archers,
  Black Mage AoE as the top threat, Thieves' Steal Heart charm (all-male-party counter), allies
  Gaffgarion + Agrias, contrast with Chapter 1 Dorter.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553172
- Local: `docs/battles/011-chapter-2-overview.md` (enemy-party escalation + boss-loot rules),
  `004-dorter-slums.md` (Chapter 1 Dorter, for contrast), `001-gariland.md` (slot-add method,
  confirmed item/skill IDs).
</content>
