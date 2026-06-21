# 012 - Merchant City of Dorter (Chapter 2)

Status: ✅ implemented (v1, entry 403) — Knight job-escalation deferred (see below)
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

## Job Escalation (Chapter 2 rule)

```text
CHANGE: add ONE Knight as a frontline anchor (the band gains muscle it lacked).
WHY: Chapter 2 Dorter's original squad is all-squishy (no frontline). Adding a Knight wall
  forces the player to break through before reaching the archers/mages/thieves — raising the
  challenge while KEEPING the strategy (still "take the high ground, avoid AoE clumping,
  counter charm", now with a wall in the way). This is the single new wrinkle for this fight.
WHAT IS NOT CHANGED: the 2 Archer / 2 Black Mage / 2 Thief core stays intact, so the fight's
  finesse identity is preserved.
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

## Proposed Composition (New Game++ Merchant Dorter v1)

Keep the original six and add one Knight anchor (7 enemies). Archers and mages at `101`, the
new Knight at `101`, the Thieves at `100`.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Anchor (NEW) | Knight | `101` | Frontline wall; guards the archers/mages so they can't be rushed. |
| n | Rooftop Archer | Archer | `101` | Elevated ranged pressure; the classic Dorter menace. |
| n | Rooftop Archer | Archer | `100` | Second elevated bow; covers the other approach. |
| n | Black Mage | Black Mage | `101` | AoE threat #1 — punishes a clumped advance. |
| n | Black Mage | Black Mage | `101` | AoE threat #2 — forces the player to spread. |
| n | Thief (charm) | Thief | `100` | Steal Heart pressure + fast harassment. |
| n | Thief (charm) | Thief | `100` | Second charm threat; splits the player's caution. |

Reasoning:

The original band is already the platonic "finesse ambush," so the move is to **scale, gear,
and add the single Knight wrinkle**. The Knight protects what was an exposed backline, turning
a race-to-the-casters into a real break-through — the Chapter 2 escalation — without changing
the core read. Both Black Mages keep AoE relevant at party level; the two charm Thieves keep
the fight's signature threat; the elevated archers keep the Dorter rooftop identity.

## Builds (final-shop quality; coordinated mercenary band flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Knight Anchor (Lv 101) — NEW

```text
Job: Knight (id TBD)   JobLevel: 8   Secondary: none (NO Break this fight)
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head/Body: shop heavy helm + heavy armor (ids TBD)
Accessory: Bracers (218)
Right hand: Runeblade (30) or Icebrand (29)   Left hand: shop shield (id TBD)
```

Role: the wall the original band lacked. Stalls the street so the casters/archers keep working.

### Archer x2 (Lv 101 / 100)

```text
Job: Archer (77)   JobLevel: 8   Secondary: none
Reaction: Reflexes (449)   Support: Concentration (469)   Movement: Movement +1 (486)
Head: Thief's Cap (168)   Body: Black Garb (198)   Accessory: Bracers (218)
Right hand: Windslash Bow (87)   Left hand: none / two-hand marker (254)
```

Role: elevated harassment. Concentration keeps them relevant against evasive NG+ units.

### Black Mage x2 (Lv 101)

```text
Job: Black Mage (id TBD)   JobLevel: 8   Secondary: none
Reaction: Reflexes (449) or magic-defensive reaction (id TBD)
Support: MA/Magick-boost support if available (id TBD)
Movement: Movement +1 (486)
Head: cloth/mage hat (id TBD)   Body: shop robe (id TBD)
Accessory: Featherweave Cloak (234)   Right hand: shop magic-boost rod (id TBD)   Left: none (255)
```

Role: the AoE that punishes clumping — the biggest threat, exactly as the walkthrough warns.

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
Knight starts on the ground at the main approach, between the player and the backline.
Both Archers start on the elevated tiles (rooftops/high ground) with wide sightlines.
Both Black Mages start behind the Knight / at mid-height, able to AoE the approach lane.
Both Thieves start on the flanks with movement lanes to dart at the player's formation.
Do NOT alter the Gaffgarion/Agrias ally placements.
```

The map should read: "a wall up front, archers above, mages lobbing AoE, and charm-thieves
circling" — a formation puzzle, the Chapter 2 escalation of Dorter's high-ground lesson.

## Implemented (v1, entry 403)

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

**Deferred — the Knight job-escalation (a 7th unit).** The doc's single Chapter-2 wrinkle is to
ADD a Knight frontline wall. That means inserting a new unit into an empty slot (s9+), which needs
a verified, walkable map position — every Chapter 1 battle only re-tuned existing slots, so adding a
unit is a new, untested operation best done with an in-game playtest. The 6-unit finesse identity
(elevation + AoE + charm) is fully delivered; the Knight add is batched for the playtest pass.

## Implementation Checklist

- [x] Identify Merchant Dorter ENTD entry (403) on Windows data; fill "Local Data Confirmed".
- [x] Dump original entry; verify 2 Archer + 2 Black Mage + 2 Thief + ally slots.
- [x] Confirm Black Mage / Archer / Thief job IDs and legal equipment.
- [ ] Add the Knight slot (deferred — needs a verified map position; do during playtest).
- [x] Set levels: Archer(1) + both Black Mages `101`; Archer(2) + both Thieves `100`.
- [x] Set JobLevel `8` on all active enemy slots.
- [x] Keep Steal Heart on the two Thieves (innate to the Thief job at jl8).
- [x] Equip per builds; preserve the elevation positions and the allies.
- [x] Patch the embedded ENTD (NG+-only by construction); diff inside entry 403 only.
- [x] Re-dump and diff; confirm changes are small and intentional.
- [ ] Install mod, test from a New Game+ save; then add the Knight wrinkle (playtest).

## Test Questions

- Does the added Knight meaningfully change the fight (force a break-through) without breaking
  the "take the high ground / avoid AoE / counter charm" strategy?
- Are the two Black Mages still the biggest threat at scale?
- Is the charm (Steal Heart) a fair, telegraphed threat the player can counter, not a coin-flip loss?
- Does it clearly read as a step up from Chapter 1 Dorter — coordinated finesse, not a brawl?
- Is it a fitting Chapter 2 opener: harder than Ch1 but not a wall this early in the chapter?
- Does it still feel like a mercenary ambush in the merchant city, not a designed arena?

## Sources

- Game8, "Merchant City of Dorter Walkthrough (Battle 11)": roster (2 Archer, 2 Black Mage,
  2 Thief), objective "Defeat all enemies!", deploy 4, recommended level ~10, elevated archers,
  Black Mage AoE as the top threat, Thieves' Steal Heart charm (all-male-party counter), allies
  Gaffgarion + Agrias, contrast with Chapter 1 Dorter.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553172
- Local: `docs/battles/011-chapter-2-overview.md` (job-escalation + boss-loot rules),
  `004-dorter-slums.md` (Chapter 1 Dorter, for contrast), `001-gariland.md` (slot-add method,
  confirmed item/skill IDs).
</content>
