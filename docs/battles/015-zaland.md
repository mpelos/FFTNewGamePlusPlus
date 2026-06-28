# 015 - Castled City of Zaland

Status: ✅ implemented (v1, entry 407) — Knight→Dragoon escalation done inline; Mustadio auto-scaled + endgame gear (2026-06-27)
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

Zaland fuses two earlier lessons: it is **Mandalia's reckless-guest escort** (Mustadio charges
like Argath did) staged on **a vertical, Dorter-style combined-arms map** (Knights + Archers +
Black Mages, high walls, Jump matters). The challenge is to keep a headstrong ally alive while
fighting up and around castle walls against ranged and magic threats. It teaches buff-the-guest
(Protect/Shell), priority targeting (mages/archers), and using elevation/Jump.

For New Game++ the identity must stay: **a vertical castle fight where the player screens a
reckless guest (Mustadio) and out-positions a combined-arms squad on the walls — buffs, target
priority, and verticality are the whole puzzle.**

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

### Mustadio (guest) — auto-scaled, not patched here

Mustadio (cid 0x22) has **job 34 == cid**, exactly the Delita/Argath guest pattern, so he was added
to `GuestCharIds` in Program.cs. The runtime guest-scaler (always-on, job==cid guarded) keeps him at
party level on every ENTD read, so the reckless guest can survive his own charge and the protect-path
Game Over — without touching his slot or scripting here. (This also covers Goug Lowtown, Battle 17,
where Mustadio is again a guest.) Unlike Boco (generic monster cid 0x82, unusable by the scaler),
Mustadio's unique cid makes the scaler the clean, correct fix.

## Job Escalation (Chapter 2 rule)

```text
CHANGE: swap ONE Knight -> a Dragoon (Lancer) with Jump (keep the count at 6).
WHY: the map is literally about high walls and Jump. An enemy Dragoon can LEAP over walls to
  strike the backline or the reckless Mustadio from elevation — a new vertical threat that the
  Knights (slow, ground-bound) can't pose. It deepens the exact challenge (verticality + escort)
  rather than changing it. Single new wrinkle; thematically perfect for a walled castle.
WHAT IS NOT CHANGED: the remaining Knight + 2 Archers + 2 Black Mages keep the combined-arms
  identity; the strategy ("buff Mustadio, kill mages/archers, manage elevation") still holds —
  now with a leaping threat the player must also screen against.
```

## Boss rare loot

```text
None. No named boss here — no rare item (per the Chapter 2 overview). Generics stay shop-tier.
```

## Proposed Composition (New Game++ Zaland v1)

Keep the combined-arms squad, swapping one Knight for a Dragoon (6 enemies). Archers/mages and
the Dragoon at `101`; the Knight and one Archer at `100`–`101`.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Anchor | Knight | `101` | Ground wall; contests the approach and the gate. |
| n | Skyfall (NEW) | Dragoon | `101` | Jumps walls to strike Mustadio / the backline — the vertical wrinkle. |
| n | Wall Archer | Archer | `101` | Elevated ranged pressure from the high walls. |
| n | Archer | Archer | `100` | Second bow; covers the long way around. |
| n | Black Mage | Black Mage | `101` | AoE threat #1 — punishes a clumped escort. |
| n | Black Mage | Black Mage | `101` | AoE threat #2 — the priority kill, per the walkthrough. |

Reasoning:

The faithful move is to **scale the combined-arms squad, keep the escort + verticality, and add
one leaping threat**. The Dragoon is the perfect Chapter-2 escalation for a high-wall castle:
it punishes a player who tucks Mustadio behind a wall, because Jump ignores the wall. Two Black
Mages keep AoE the priority; the elevated Archer keeps the vertical ranged identity. The single
Knight anchors the ground. The reckless guest plus a unit that can reach over cover makes
"screen Mustadio" a real, active job.

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

### Dragoon (Lv 101) — NEW (job swap)

```text
Job: Dragoon / Lancer (id TBD)   JobLevel: 8   Secondary: none (innate Jump command)
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +2 (487) or Jump +
  (id TBD) — emphasize reach
Head: shop helm (id TBD)   Body: shop light/medium armor (id TBD)
Accessory: Germinas Boots (210) or a Jump/Move accessory (id TBD)
Right hand: a strong shop spear (id TBD)   Left hand: none / two-hand marker (254)
```

Role: the vertical threat. Jumps over the high walls to land on Mustadio or the backline. Give
it reach (Move/Jump) so the player can't simply hide the guest behind cover.

### Archer x2 (Lv 101 / 100)

```text
Job: Archer (77)   JobLevel: 8   Secondary: none
Reaction: Reflexes (449)   Support: Concentration (469)   Movement: Movement +1 (486)
Head: Thief's Cap (168)   Body: Black Garb (198)   Accessory: Bracers (218)
Right hand: Windslash Bow (87)   Left hand: none / two-hand marker (254)
```

Role: elevated harassment over the walls; punishes the long way around.

### Black Mage x2 (Lv 101)

```text
Job: Black Mage (id TBD)   JobLevel: 8   Secondary: none
Reaction: Reflexes (449)   Support: MA/Magick-boost (id TBD)   Movement: Movement +1 (486)
Head: cloth/mage hat (id TBD)   Body: shop robe (id TBD)
Accessory: Featherweave Cloak (234)   Right hand: shop magic-boost rod (id TBD)   Left: none (255)
```

Role: the priority threat — AoE that punishes a clumped escort, exactly as the walkthrough warns.

## Positioning Plan

```text
Knight starts at the gate / main ground approach.
Dragoon starts on or near a high wall with a clear Jump arc toward Mustadio's likely charge lane.
Both Archers start on the high walls with wide sightlines.
Both Black Mages start behind the wall line / at mid-height, able to AoE the approach and the
  guest's reckless path.
Preserve Mustadio's guest start and the wall/Jump terrain; do NOT alter his scripting.
```

The map should reward verticality for BOTH sides: the player wants Jump/elevation to reach the
mages and archers, while the enemy Dragoon uses the same walls to dive at the reckless guest.

## Implemented (v1, entry 407)

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

## Implementation Checklist

- [x] Identify Zaland ENTD entry (407); fill "Local Data Confirmed".
- [x] Dump original entry; verify 2 Knight + 2 Archer + 2 Black Mage + Mustadio slot.
- [x] Confirm Knight / Black Mage / Dragoon job IDs and legal equipment (Dragoon = Partisan spear).
- [x] Swap one Knight -> Dragoon (re-job s4); give it reach (Move +2).
- [x] Set levels: Knight + Dragoon + wall Archer + both Black Mages `101`; second Archer `100`.
- [x] Set JobLevel `8` on all scaled enemy slots; Knight has no secondary.
- [x] Mustadio handled via the runtime guest-scaler (cid 0x22 added to GuestCharIds); slot untouched.
- [x] Patch the embedded ENTD (NG+-only); diff inside entry 407 only.
- [x] Re-dump and diff; changes small and intentional.
- [ ] Playtest BOTH objectives (clear vs protect Mustadio) from a NG+ save; confirm Mustadio scales.

## Test Questions

- Does the enemy Dragoon meaningfully punish hiding Mustadio behind walls (Jump ignores cover)?
- Is protecting reckless Mustadio tense but achievable with Protect/Shell + screening?
- Are the two Black Mages still the priority threat at scale?
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
- Local: `docs/battles/011-chapter-2-overview.md` (job-escalation rule), `002-mandalia-plain.md`
  (reckless-guest escort), `004-dorter-slums.md` (combined-arms verticality).
</content>
