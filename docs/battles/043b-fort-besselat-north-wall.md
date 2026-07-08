# 043b - Fort Besselat: North Wall (Bethla Garrison)

Status: 📝 redesign v3 planned (docs-only) — v1 implementation exists for entry 449
Chapter: 4 — "In the Name of Love"
Battle order: Battle 38B (North Wall — mutually exclusive with `043a`)
Target version: Enhanced v1.5.0
ENTD: global entry **449** (North) — `battle_entd4_ent.bin` local 65
File: `battle_entd4_ent.bin` (embedded NG+ swap) — `tools/battle_patch.py besselat_wall`

> **NG++ reward applied (2026-06-27):** Yoichi Bow + Perseus Bow on the Archer slots of BOTH path entries
> (448 s3/s4, 449 s0/s3), so either route awards them. Guaranteed Spoils of War (ENTD 0x1e), NG+ only,
> within the 3-cap, no steal needed. Canonical map: `chapter-4-rewards-implementation.md`.

Current implementation (entry 449, vanilla-dump verified):
- s0 Archer L102, s3 Archer L101.
- s1 Dragoon L102, s2 Dragoon L101 — Partisan/heavy, Jump innate. TIC has 2 Dragoons vs the public
  walkthrough's 1.
- s4 Summoner L102 — priority caster, charge intact.
- s5 Monk L102 — bare-fist, Power Garb/Bracers.
- No boss / no named boss rare; low Ch4 band (101-102). Map treasure (other layer) untouched.

Planned v3 redesign (docs-only in this pass): keep the North ranged/AoE wall identity, but convert the
two local Lancer/Dragoon slots into Geomancer-bucket terrain fighters. The route still asks the player
to climb through ranged pressure toward the Summoner, but the former Jump threat becomes armor-backed
Geomancy pressure across the wall geometry.

## Design Goal

```text
Make North Wall the ranged/AoE branch of Fort Besselat: the player rushes a Summoner while weathering two
Geomancer terrain fighters on narrow vertical terrain. The route should feel distinct from South's
melee/stealth branch and clearly below the Sluice spike.
```

No active guests appear here. No guest-control implementation is needed.

## Original Battle

Objective:

```text
Defeat all enemies!
```

Player deployment:

```text
Up to 5 units, including Ramza. No guests.
```

Original North composition (verified via Game8, Battle 38B):

```text
2x Archer    (ranged chip)
1x Monk      (melee bruiser; Chakra/Wave Fist)
1x Dragoon   (Jump — vertical pressure)
1x Summoner  (wide-area summon — the priority threat)
```

Local data correction:

```text
TIC / current local data has 2x Dragoon, not 1x Dragoon. The NG++ North doc follows the local roster:
2 Archer + 2 Dragoon + 1 Monk + 1 Summoner.
```

Vanilla comparison:

```text
- The route keeps the vanilla North identity: ranged/AoE pressure on vertical wall terrain.
- Objective is unchanged: defeat all enemies.
- Compared to public vanilla walkthroughs, the local entry has a second Lancer/Dragoon slot; in v3 both
  of those slots become Geomancers.
- Both Archer slots change in v3: the closer Archer becomes a Black Mage shooter, while the farther/higher
  Archer Leader becomes a Knight Leader copied from South Wall.
- The difference is completeness: all active humans get Chapter-4-level gear and full ability slots.
- Yoichi Bow + Perseus Bow remain guaranteed route-parity rewards through spoils, not steal-gated rewards.
```

## Local Data Confirmed / Data Still Needed

```text
CONFIRMED:
- Entry 449 is the Fort Besselat North Wall ENTD entry.
- Original/local North roster: 2 Archer + 2 Dragoon + 1 Summoner + 1 Monk.
- Planned v3 roster: 1 far/high Knight Leader + 1 near-side Black Mage shooter + 2 Geomancer-bucket
  former Lancers/Dragoons + 1 Summoner + 1 former-Monk Knight.
- The player fights either this branch or South (`043a`), never both.
- No active guest, no boss.
- Reward ledger duplicates Yoichi Bow + Perseus Bow across both entries so either route pays the same
  guaranteed spoils.

STILL NEEDED FOR V3 IMPLEMENTATION:
- Confirm exact slot order before patching complete v3 kits.
- Confirm objective remains "Defeat all enemies".
- Confirm whether OverrideEntryData carries level for this battle or leaves levels at runtime scale.
- Preserve vertical wall / narrow-path geometry and branch scripting.
- Preserve map treasure as vanilla map loot.
```

Job IDs (carry over known, verify the rest in-game):

```text
77 = Archer            (confirmed)
Monk job id            (TBD - verify)
Knight job id          (TBD - verify)
Dragoon / Lancer id    (TBD - verify; enemy Dragoon, 027/038)
Geomancer job id       (TBD - verify)
Summoner job id        (TBD - verify)
```

## Enemy Party Escalation (Chapter 4 rule)

```text
CHANGE: North becomes a complete ranged/AoE wall team: Summoner wide-AoE and two Geomancer terrain
  fighters punish exposed climbing lanes while a far/high Knight Leader, one near-side Black Mage shooter,
  and a dual-wield Knight hold the route.
WHY: North's identity is "rush the Summoner through ranged wall pressure." The faithful Ch4 move is to
  make every defender fully built and let the wall terrain matter more, not to add a boss or a second
  unrelated engine.
CONSTRAINTS: Geomancy is terrain pressure, not hard control; Summoner keeps intact charge times and
  remains race-able; the high/distant Archer Leader uses the same "Holy Knight if possible" fallback as
  South Wall's Knight Leader.
REJECTED DEFAULTS: no accelerated Summoner, no hard-status support, no 103+ overlevel spike, no one-sided
  rewards. Branch parity matters because the player chooses only one path.
WHAT IS NOT CHANGED: enemy count, the "defeat all" objective, and wall/chokepoint geometry remain.
```

## Rare/reward handling

```text
Guaranteed spoils for entry 449: YOICHI BOW + PERSEUS BOW.
These are duplicated on South entry 448 because the player fights only one path.
The player must never be forced to pick a route or Steal to receive the reward pair.
PRESERVE: North map treasure (Carabineer Mail, Angel Ring, Runeblade, Kiku-Ichimonji) remains existing
map loot, not the NG++ reward channel.
```

## Proposed Composition (New Game++ North Wall v3)

Keep the local enemy count and the boss-less wall-skirmish feel. No `103`+ spike.

| Slot | Role | Job | Level | Br/Fa | Purpose |
| ------ | ------ | ----- | ------- | --- | --------- |
| n | Summoner | Summoner | `102` | `60/84` | Wide-area summon — priority kill; reaches you from start. |
| n | Geomancer | Geomancer bucket | `102` | `86/40` | Former Lancer/Dragoon; armored Geomancy pressure on the ledges. |
| n | Geomancer | Geomancer bucket | `101` | `86/40` | Second former Lancer/Dragoon; mirrors terrain pressure. |
| n | Knight | Knight, former Monk slot | `102` | `88/40` | Dual Rune Blade bruiser with Martial Arts secondary. |
| n | Knight Leader | Holy Knight bucket, if possible | `102` | `88/42` | Former far/high Archer Leader; Defender + Crystal Shield anchor. |
| n | Near-side Black Mage shooter | Black Mage bucket | `101` | `62/84` | Former closer Archer; Blaze Gun pressure near the player approach. |

Reasoning:

North remains a ranged/AoE wall problem. The player must prioritize the Summoner, endure Geomancy from
two armored former Lancer/Dragoon slots, and handle a far/high Knight Leader plus a near-side Black Mage
shooter and dual-wield Knight while climbing narrow terrain. The second former Lancer/Dragoon slot is a
local-data correction, not an added unit.

## Builds

### Summoner (Lv 102)

```text
Job bucket: Summoner   JobLevel: 8
Primary: Summon Magic with intact charge times
Secondary: Time Magic, Time Mage JobLevel 8
Reaction: Soulbind
Support: Swiftspell
Movement: Movement +2
Right hand: Wizard's Rod
Head: Lambent Hat   Body: Wizard's Robe   Accessory: Featherweave Cloak
Forbidden: instant summons, Stop/Don't Act engines, unrelated hard status.
```

### Geomancer x2 (former Lancer/Dragoon slots, Lv 102/101)

```text
Job bucket: Geomancer   JobLevel: 8
Secondary: None
Reaction: Nature's Wrath
Support: Equip Armor
Movement: Movement +2
Right hand: Rune Blade
Head: Crystal Helm   Body: Crystal Mail   Accessory: Magepower Glove
```

### Knight (former Monk slot, Lv 102)

```text
Job bucket: Monk   JobLevel: 8
Role/job: Knight, if implementation supports the requested Monk-bucket former-Monk conversion.
Secondary: Martial Arts
Reaction: First Strike
Support: Dual Wield
Movement: Movement +2
Right hand: Rune Blade   Left hand: Rune Blade
Head: Crystal Helm   Body: Crystal Mail   Accessory: Bracers
```

### Knight Leader (former far/high Archer Leader slot, Lv 102)

```text
Job bucket: Holy Knight, if possible   JobLevel: 8
Secondary: Holy Knight, if possible
Reaction: Counter (442)
Support: Attack Boost (465)
Movement: Movement +3
Right hand: Defender   Left hand: Crystal Shield
Head: Crystal Helm   Body: Crystal Mail   Accessory: Bracers
```

Implementation note:

```text
If Holy Knight cannot be assigned cleanly for this generic slot, preserve the role as a Knight Leader:
Defender + Crystal Shield anchor, Counter, Attack Boost, Movement +3, and no Rend wall plan.
```

Role: copied from South Wall's Knight Leader and assigned to the Archer Leader that starts farthest/highest.
Rewards still pay via guaranteed spoils; Steal is optional.

### Black Mage shooter (former closer Archer slot, Lv 101)

```text
Job bucket: Black Mage   JobLevel: 8
Secondary: None
Reaction: Reflexes (449)
Support: Equip Guns
Movement: Teleport
Right hand: Blaze Gun
Head: Lambent Hat   Body: Wizard's Robe   Accessory: Magepower Glove
```

Role: copied from the South Wall Black Mage shooter model, but with Blaze Gun. This replaces only the
Archer closer to the player approach; the farther/higher Archer Leader becomes the Knight Leader above.

## Positioning Plan

```text
North: the Summoner starts high/back with wide-AoE sightlines onto the climb, the 2 Geomancers start on
  staggered elevation to exploit wall terrain, the former-Monk Knight starts forward as bruiser, the
  far/high Archer Leader becomes a Knight Leader on the upper rampart, and the closer Archer slot becomes
  a near-side Black Mage shooter covering the approach.
Preserve the narrow paths + height; do NOT flatten or widen the wall.
Modest levels — one of two converging skirmishes, not a spike.
```

## Simulation Plan and Results

Simulation artifact:

```text
tmp/fft-level-design-043b-fort-besselat-north-wall/
  assumptions.md
  simulate.py
  iteration-results.json
  iteration-results.md
```

Current result source: inherited from the former combined 043 branch-balance simulation. The v3 redesign
needs a refreshed simulation pass because the old Dragoon Jump pressure has become armored Geomancy
terrain pressure.

## Implementation Checklist

- [ ] Confirm entry 449 North slot order before patching complete kits.
- [ ] Keep objective = "Defeat all enemies" + the vertical wall / narrow-path geometry.
- [ ] Keep Summoner charge times intact and rushable.
- [ ] Former Lancer/Dragoon slots become Geomancer JobLevel 8 units with no secondary, Nature's Wrath,
  Equip Armor, Movement +2.
- [ ] Former Monk slot becomes the requested Knight bruiser with Monk JobLevel 8 bucket note, Martial Arts,
  First Strike, Dual Wield, Movement +2, and dual Rune Blades.
- [ ] Replace only the Archer closer to the player with a Black Mage shooter copied from South Wall's
  shooter model, using Blaze Gun.
- [ ] Replace the farther/higher Archer Leader with a Knight Leader copied from South Wall's Knight Leader.
- [ ] Give every active human complete equipment plus secondary/reaction/support/movement.
- [ ] Preserve guaranteed spoils: Yoichi Bow + Perseus Bow on this branch.
- [ ] Set levels in the low Ch4 band (`101`-`102`, no `103`); JobLevel `8` on all active slots.
- [ ] Patch entry 449 via the correct layer; keep the diff inside the North Wall window.
- [ ] Test this path from a New Game+ save and confirm North = ranged/AoE wall assault.

## Test Questions

- Does North still feel like the ranged/AoE branch, distinct from South?
- Is the Summoner still the clear priority and race-able with intact charge times?
- Do the two Geomancers make wall terrain matter without becoming hard-control pressure?
- Is the Knight Leader plus Blaze Gun shooter pressure still below Sluice pressure?
- Does the route pay Yoichi Bow + Perseus Bow equivalently to South?

## Sources

- Game8, "Fort Besselat: North Wall (Battle 38B)": roster, objective, Summoner priority, terrain, rewards.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553199
- Local: `037-chapter-4-overview.md`, `043a-fort-besselat-south-wall.md`,
  `044-fort-besselat-sluice.md` (wall pressure / terrain handling),
  `chapter-4-rewards-implementation.md`, and `tmp/fft-level-design-043b-fort-besselat-north-wall/`.
