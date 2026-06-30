# 015 - Castled City of Zaland

Status: ✅ implemented (v1, entry 407) — Knight→Dragoon escalation done inline; Mustadio auto-scaled + endgame gear (2026-06-27). **v2 redesign documented only** (implementation pending).
Chapter: 2 — "The Manipulator and the Subservient"
Battle order: Battle 14 (after Zeirchele Falls)
Target version: Enhanced v1.5.0
ENTD: global entry **407** (battle_entd4, local entry 23) — confirmed by sequence + composition
File: `entd/battle_entd4_ent.bin` (embedded; swapped only in NG+ by the code mod)

> Implemented via `tools/battle_patch.py zaland`, plus a Program.cs change adding Mustadio (cid
> 0x22) to the runtime guest-scaler. NG+-only enemy edits; the guest-scaler runs always. See
> `011-chapter-2-overview.md`.

**Guest gear upgrade (NG+ survivability, 2026-06-27):** Mustadio (s0) re-equipped to the best buyable
end-game gear in his ENTD slot (he was Ch2-tier): **Thief's Cap 168** (HP +100, +2 Spd, immune
Disable/Immobilize), **Black Garb 198** (HP +100, immune Stop), **Hermes Shoes 213**, **Mythril Gun 72**.
Level still comes from the runtime guest-scaler.

## Original Battle

Objective:

```text
Defeat all enemies!  — OR —  Protect Mustadio!
(Choosing "We cannot stand by and watch!" grants +5 Bravery and makes Mustadio's death a Game Over.)
```

Player deployment:

```text
Up to 4 units, including Ramza.
Guest: Mustadio joins and fights AGGRESSIVELY on his own (no player control) — he charges in
  and can die if unsupported. On the protect path, his death ends the run.
```

Original enemy composition:

```text
2x Knight
2x Archer
2x Black Mage
(no named leader)
```

Public walkthrough details:

```text
Recommended level: ~14 (3/5 stars).
Castle map with HIGH WALLS — a Jump stat of 4+ scales them efficiently; otherwise units take a
  long way around. Verticality is central.
Black Mages and Archers are the priority threats; the Knights anchor.
Mustadio acts independently and recklessly — the standard play is to immediately Protect/Shell
  him and screen his charge. Dragoons' Jump helps reach elevated enemies.
```

Design reading:

Zaland fuses two earlier lessons: it is **a recruit rescue** staged on **a vertical, Dorter-style
combined-arms map** (Knights + Archers + Black Mages, high walls, Jump matters). In vanilla,
Mustadio's reckless AI is part of the stress. In New Game++, that cannot be the skill check.
Mustadio should be party-level, geared, and player-controlled; the challenge should come from
the enemy using the walls better than the player.

For New Game++ the identity must stay: **a vertical castle rescue where the player routes Mustadio
as a controllable gunner while a combined-arms squad uses walls, Jump, arrows, and AoE to pressure
the whole party.**

## Local Data Confirmed (entry 407)

```text
slot  cid    name  flags  job        role                       action
s0    0x22   34    0x91   34         Mustadio (reckless guest)  AUTO-SCALED (GuestCharIds, not here)
s1    0x80   255   0x80   76 Knight  ground anchor              SCALE -> L101
s2    0x80   255   0x80   80 BMage   priority AoE               SCALE -> L101
s3    0x80   255   0x80   80 BMage   priority AoE               SCALE -> L101
s4    0x80   255   0x80   76 Knight  -> DRAGOON (escalation)    SCALE -> L101, re-job 87
s5    0x81   255   0x40   77 Archer  wall archer                SCALE -> L101
s6    0x81   255   0x40   77 Archer  archer                     SCALE -> L100
s7    0x34   52    0x49   52         recurring story unit       LEAVE (lvl 254)
```

Job IDs: Knight 76, Black Mage 80, Archer 77, **Dragoon/Lancer 87** (first use in the mod). The
escalation Dragoon carries **Partisan (102)** — the strongest pre-Chapter-4 SHOP-tier spear (Holy
Lance/Dragon Whisker are Unknown20/reserved).

### Mustadio (guest) — auto-scaled; v2 requires player control

Mustadio (cid 0x22) has **job 34 == cid**, exactly the Delita/Argath guest pattern, so he was added
to `GuestCharIds` in Program.cs. The runtime guest-scaler (always-on, job==cid guarded) keeps him at
party level on every ENTD read, so the reckless guest can survive his own charge and the protect-path
Game Over — without touching his slot or scripting here. (This also covers Goug Lowtown, Battle 17,
where Mustadio is again a guest.) Unlike Boco (generic monster cid 0x82, unusable by the scaler),
Mustadio's unique cid makes the scaler the clean, correct fix.

For v2, scaling and gear are not enough: Mustadio must also be player-controlled in NG+ so the fight
does not punish the player for guest AI. The protect-route Game Over can remain, but the player must
lose only after misrouting or ignoring the board.

## Enemy Party Escalation (Chapter 2 redesign)

```text
VANILLA SPIRIT: rescue Mustadio in a walled city while Archers and Black Mages punish the approach.
CHAPTER-2 UPGRADE: keep the combined-arms identity, but make verticality the headline: 1 Knight,
  2 Dragoons, 2 Archers, 2 optimized Black Mages.
WHY: a Time Mage was rejected because it adds a second system on top of verticality. Two Dragoons
  make the walls matter for both sides without introducing hard control.
WHAT IS NOT CHANGED: Archers and Black Mages remain priority threats, Jump/elevation remains the
  map lesson, and Mustadio remains the recruit objective — now controlled by the player.
```

Chapter 2 requirements applied:

```text
- Every active human enemy has full equipment.
- Every active human enemy has intentional reaction, support, and movement.
- Secondary is optional; Dragoons rely on Jump, Black Mages rely on Black Magic.
- No hard-lock status is added.
- Mustadio must be player-controlled in NG+.
```

## Boss rare loot

```text
None. No named boss here — no rare item (per the Chapter 2 overview). Generics stay shop-tier.
```

## Guest handling

```text
Mustadio is an active guest and protect-route fail condition. In NG+ he must be party-level,
fully geared, and player-controlled. His role becomes a controllable gunner/recruit in a vertical
fight, not a reckless AI unit the player must babysit.
```


Fixed encounter Brave/Faith targets:

| Unit | Br/Fa | Rationale |
|------|-------|-----------|
| Mustadio | `70/55` | Controlled Machinist recruit; physical gun utility, not a high-Faith caster. |

## Proposed Composition (New Game++ Zaland v2)

Use seven enemies: 1 Knight, 2 Dragoons, 2 Archers, 2 optimized Black Mages. The map's high walls
become the primary challenge.

| Slot | Role | Job | Level | Br/Fa | Purpose |
| ------ | ------ | ----- | ------- | --- | --------- |
| n | Anchor | Knight | `101` | `76/48` | Ground wall; contests the approach and the gate. |
| n | Skyfall Captain | Dragoon | `102` | `76/45` | Primary Jump threat; crosses walls into the backline. |
| n | Skyfall | Dragoon | `101` | `76/45` | Second Jump threat; prevents one-body screening. |
| n | Wall Archer | Archer | `101` | `74/50` | Elevated ranged pressure from the high walls. |
| n | Archer | Archer | `100` | `74/50` | Second bow; covers the long way around. |
| n | Fast Black Mage | Black Mage | `102` | `55/76` | Swiftness caster; punishes clustered routes. |
| n | Power Black Mage | Black Mage | `101` | `55/76` | Arcane Strength caster; priority kill, per the walkthrough. |

Reasoning:

The faithful move is to **scale the combined-arms squad and make the walls matter**. Two Dragoons
create delayed, answerable vertical pressure. Two Archers keep the wall threat. Two tuned Black
Mages keep caster priority high. The single Knight anchors the gate. Mustadio is controlled, so the
player's job is route planning and target priority, not compensating for reckless AI.

## Builds (final-shop quality; castle garrison flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Knight Anchor (Lv 101)

```text
Job: Knight (id TBD)   JobLevel: 8   Secondary: none (NO Break)
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head/Body: shop heavy helm + heavy armor (ids TBD)
Accessory: Bracers (218)   Right hand: Runeblade (30)   Left hand: shop shield (id TBD)
```

Role: the ground wall at the gate/approach.

### Dragoon x2 (Lv 102 / 101)

```text
Job: Dragoon / Lancer (id TBD)   JobLevel: 8   Secondary: none (innate Jump command)
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +2 (487) or Jump +
  (id TBD) — emphasize reach
Head: shop helm (id TBD)   Body: shop light/medium armor (id TBD)
Accessory: Germinas Boots (210) or a Jump/Move accessory (id TBD)
Right hand: a strong shop spear (id TBD)   Left hand: none / two-hand marker (254)
```

Role: the vertical threat. Jumps over the high walls into the backline and forces the player to
read CT/landing timing. Give them reach (Move/Jump) so the walls matter, but keep Jump answerable.

### Archer x2 (Lv 101 / 100)

```text
Job: Archer (77)   JobLevel: 8   Secondary: none
Reaction: Reflexes (449)   Support: Concentration (469)   Movement: Movement +1 (486)
Head: Thief's Cap (168)   Body: Black Garb (198)   Accessory: Bracers (218)
Right hand: Windslash Bow (87)   Left hand: none / two-hand marker (254)
```

Role: elevated harassment over the walls; punishes the long way around.

### Black Mage x2 (Lv 102 / 101)

```text
Fast Black Mage:
Job: Black Mage (id TBD)   JobLevel: 8   Secondary: none
Reaction: Mana Shield / Reflexes (id TBD / 449)
Support: Swiftness (id TBD)   Movement: Movement +1 (486)
Head: cloth/mage hat (id TBD)   Body: shop robe (id TBD)
Accessory: Featherweave Cloak (234)   Right hand: shop magic-boost rod (id TBD)   Left: none (255)

Power Black Mage:
Job: Black Mage (id TBD)   JobLevel: 8   Secondary: none
Reaction: Reflexes (449)   Support: Arcane Strength (id TBD)   Movement: Movement +1 (486)
Head: cloth/mage hat (id TBD)   Body: shop robe (id TBD)
Accessory: Featherweave Cloak (234)   Right hand: shop magic-boost rod (id TBD)   Left: none (255)
```

Role: the priority threat — AoE that punishes clumped wall routes, exactly as the walkthrough warns.

## Positioning Plan

```text
Knight starts at the gate / main ground approach.
Dragoons start on or near high walls with clear Jump arcs toward the player backline and Mustadio's
  controllable route.
Both Archers start on the high walls with wide sightlines.
Both Black Mages start behind the wall line / at mid-height, able to AoE the approach and the
  most obvious clustered route.
Preserve Mustadio's guest start and the wall/Jump terrain; add NG+ player-control handling.
```

The map should reward verticality for BOTH sides: the player wants Jump/elevation to reach the
mages and archers, while the enemy Dragoons use the same walls to dive into the party's route.

## Simulation Plan and Results

Simulation artifact:

```text
tmp/fft-level-design-015-zaland/
```

Model scope:

```text
First four rounds only; compares vertical action economy and weighted pressure. It rejects
candidates that leave Mustadio AI-framed or add Time Mage tempo on top of verticality.
```

Iteration results:

| Candidate | Enemies | Enemy actions | Action ratio | Pressure | Delta vs v1 | Result |
|-----------|---------|---------------|--------------|----------|-------------|--------|
| v1 current: 1 Knight, 1 Dragoon, 2 Archer, 2 Black Mage | 6 | 21.8 | 1.09 | 54.8 | 0.0% | Baseline |
| Add Time Mage tempo | 7 | 25.4 | 1.27 | 63.6 | +16.1% | Rejected: extra system |
| Mustadio still AI-framed | 7 | 26.0 | 1.30 | 69.1 | +26.1% | Rejected: guest-AI framing |
| 1 Knight, 2 Dragoon, 2 Archer, 2 optimized Black Mage | 7 | 26.0 | 1.30 | 69.1 | +26.1% | Accepted |

Decision:

```text
Use two Dragoons as the vertical headline and tune the Black Mages. Do not add Time Mage tempo.
Mustadio must be party-level, geared, and player-controlled in NG+.
```

## Current Implementation (v1, entry 407 — superseded by v2 design)

Applied with `python tools/battle_patch.py zaland`; diff contained to local entry 23 (global 407),
63 bytes. The Chapter-2 escalation was a **job SWAP** (s4 Knight → Dragoon/Lancer), done inline.

```text
s1  Knight   L101 jl8  R Counter  S Atk-Boost  M +1  heavy shop kit + Runeblade + Shield
s4  Dragoon  L101 jl8  R Counter  S Atk-Boost  M +2  heavy kit + Germinas + Partisan (Jump over walls)
s2  BMage    L101 jl8  R Reflexes  M +1  Mage Hat / shop Robe / Featherweave + shop Rod
s3  BMage    L101 jl8  (same kit)
s5  Archer   L101 jl8  R Reflexes  S Concentration  M +1  Thief's Cap / Black Garb / Bracers + Windslash Bow
s6  Archer   L100 jl8  (same kit)
```

This implementation remains the shipped v1 data. The v2 redesign above is **documentation only** in
this pass; it requires a later ENTD implementation pass to add the second Dragoon, tune the Black
Mages, and verify/apply Mustadio player control.

## Future Implementation Checklist (v2)

- [x] Identify Zaland ENTD entry (407); fill "Local Data Confirmed".
- [x] Dump original entry; verify 2 Knight + 2 Archer + 2 Black Mage + Mustadio slot.
- [x] Confirm Knight / Black Mage / Dragoon job IDs and legal equipment (Dragoon = Partisan spear).
- [x] Swap one Knight -> Dragoon (re-job s4); give it reach (Move +2).
- [ ] Add or convert one more enemy into a second Dragoon; do not add a Time Mage.
- [ ] Set levels: Dragoon captain + fast Black Mage `102`; second Dragoon + wall Archer + power
  Black Mage + Knight `101`; second Archer `100`.
- [ ] Set JobLevel `8` on all active enemy slots; Knight has no secondary.
- [ ] Give every active human enemy complete equipment plus intentional reaction/support/movement.
- [x] Mustadio handled via the runtime guest-scaler (cid 0x22 added to GuestCharIds); slot untouched.
- [ ] Verify/apply Mustadio player control in NG+.
- [ ] Patch the embedded ENTD in a later implementation pass; no binary/data change in this doc pass.
- [ ] Re-dump and diff; changes small and intentional.
- [ ] Playtest BOTH objectives (clear vs Mustadio survival) from a NG+ save; confirm Mustadio scales
  and is controllable by the player.

## Test Questions

- Do two enemy Dragoons make wall routing matter without making Jump feel unavoidable?
- Does controlled Mustadio become a useful gunner/recruit instead of an AI liability?
- Are the two optimized Black Mages still the priority threat at scale?
- Does verticality matter for the player too (is Jump/elevation rewarded for reaching the casters)?
- Does it read as a vertical castle rescue blending Mandalia's escort with Dorter's combined arms?
- Is it a fair step up from Zeirchele but below the Gaffgarion/Cúchulainn bosses, per the curve?

## Sources

- Game8, "Castled City of Zaland Walkthrough (Battle 14)": roster (2 Knight, 2 Archer, 2 Black
  Mage), objective "Defeat all / Protect Mustadio", deploy 4, recommended level ~14, high-wall
  castle terrain (Jump 4+), Mustadio reckless guest + protect-path Game Over, Black Mages/Archers
  as priority threats.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553175
- Final Fantasy Wiki, "Zaland Fort City" / "Mustadio": story context (rescue from bounty hunters).
  https://finalfantasy.fandom.com/wiki/Mustadio_Bunansa
- Local: `docs/battles/011-chapter-2-overview.md` (enemy-party escalation rule), `002-mandalia-plain.md`
  (reckless-guest escort), `004-dorter-slums.md` (combined-arms verticality).
</content>
