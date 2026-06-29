# 021 - Lionel Castle Gate

Status: ✅ implemented (v1, entry 415) — Gaffgarion boss + first rare boss loot (Blood Sword). **v2 redesign documented only** (implementation pending).
Chapter: 2 — "The Manipulator and the Subservient"
Battle order: Battle 20 (after Golgollada Gallows)
Target version: Enhanced v1.5.0
ENTD: global entry **415** (battle_entd4, local entry 31) — confirmed by composition + cid 0x11 (Gaffgarion)
File: `entd/battle_entd4_ent.bin` (embedded; swapped only in NG+ by the code mod)

> Implemented via `tools/battle_patch.py lionel_gate`. NG+-only by construction. See
> `011-chapter-2-overview.md`.

## Original Battle

Objective:

```text
Defeat all enemies!  (Gaffgarion is DEFEATED FOR GOOD here — this is his death/last stand.)
```

Player deployment:

```text
Up to 5 units, including Ramza. TWO-PHASE / SPLIT battle:
  - Phase 1: Ramza fights essentially ALONE against Gaffgarion inside the gate, while the rest
    of the party defends OUTSIDE the castle gate against the other enemies.
  - A LEVER opens the gate; once open, the full party can converge and overwhelm Gaffgarion.
No guests. NOTE: immediately followed by Lionel Castle Keep (Cúchulainn) with NO resupply — plan
  resources across both fights.
```

Original enemy composition:

```text
1x Gaffgarion   (Dark Knight BOSS — Shadowblade/Drain via his drain sword; dies here)
3x Knight
2x Archer
1x Summoner     (AoE pressure on the gate defenders)
```

Public walkthrough details:

```text
Recommended level: ~23.
Ramza is split off to face Gaffgarion while the others hold the gate.
TOP PRIORITY: disarm Gaffgarion — Steal Weapon (Thief) or Rend Weapon (Knight) takes his weapon,
  which switches off Shadowblade (his Drain sustain). Disarmed, he is beatable.
The Knights + Archers + a Summoner press the gate-defense team; a lever opens the gate to reunite.
No resupply before the next fight (Cúchulainn), so don't burn everything.
```

Design reading:

Lionel Gate is **Gaffgarion's last stand** — the payoff to the threat established at the Gallows.
Its identity is a **two-front boss duel**: Ramza is isolated with the self-healing Dark Knight
while the rest of the party survives a siege at the gate, and the player must again solve
Gaffgarion by **denial** (steal/break his Blood Sword to kill Shadowblade) — but now under the
added pressure of a split party and a Summoner shelling the defenders. Because he *dies* here, this
is the chapter's first **rare, non-buyable boss drop**: his **Blood Sword** itself — the very weapon
you're trying to take off him — which doubles as the steal target and the reward. It
teaches resource discipline too (no resupply before Cúchulainn).

For New Game++ the identity must stay: **an isolated duel with a self-healing Dark Knight, solved
by stealing/breaking his Blood Sword, while the rest of the party holds a besieged gate — and the
Blood Sword is the rare prize for finishing him.**

## Local Data Confirmed (entry 415)

```text
slot  cid    flags  job          role                        action
s0    0x11   0x80   17 Fell Kn.  Gaffgarion (BOSS, dies)     SCALE -> L103 (job/sec kept) + Blood Sword
s1    0x80   0x80   77 Archer    gate-siege ranged           SCALE -> L101
s2    0x80   0x80   77 Archer    gate-siege ranged           SCALE -> L100
s3    0x81   0x40   76 Knight    gate siege (Rend)           SCALE -> L101
s4    0x81   0x40   76 Knight    gate siege (Rend)           SCALE -> L101
s5    0x81   0x40   76 Knight    gate siege                  SCALE -> L101
s6    0x80   0x80   82 Summoner  AoE shelling the defenders  SCALE -> L101
```

Job IDs: Knight 76, Archer 77, Summoner 82; Gaffgarion's enemy job is **17 (Fell Knight)** — equips
Helmet/Armor/Shield/Sword (verified in JobData), so his heavy kit is legal. His **job 17 + secondary
are PRESERVED**, keeping Shadowblade/Drain and his death scripting intact.

### Rare boss loot — Blood Sword (23), not "Ancient Sword"

The doc designed "Ancient Sword" as a lowest-tier Knight Sword, but in TIC **all KnightSword-category
items (Defender/Save the Queen/Excalibur/Ragnarok/Chaos Blade) are Unknown20 = the Chapter-4-reserved
best gear**, and item 25 "Ancient Sword" is a plain buyable Sword. So Gaffgarion's rare loot is the
**Blood Sword (23)** — the overview's named Chapter-2 rare-loot weapon, and a perfect fit: an HP-drain
blade that IS his Shadowblade sustain in item form, so **Steal Weapon both ends his self-heal and
claims the prize**. It's two-handed (lh 254) to maximize the drain and emphasize the disarm puzzle.
The ENTD has no separate "drop" field — equipping it makes it the steal target (and what he wields).
Two-phase structure (Ramza split / lever / gate) is map+event scripting, not ENTD slot data — untouched.

## Enemy Party Escalation (Chapter 2 redesign)

```text
VANILLA SPIRIT: two-front boss gate. Ramza is trapped with Gaffgarion while the party holds the
  lever side against the Order.
CHAPTER-2 UPGRADE: keep the exact 7-enemy roster: Gaffgarion, 3 Knights, 2 Archers, and 1 Summoner.
  The v2 change is to tune the duel and gate-defense pressure with complete enemy kits, not to add
  another job engine.
WHY: this fight is already denser than the Gallows because it combines a solo denial duel, gate
  defense, a lever/reunion objective, Summoner pressure, rare loot, and no-resupply chain tax.
WHAT IS NOT CHANGED: Blood Sword remains the readable off-switch and reward. Disarm/steal it,
  open the gate, finish Gaffgarion, then enter Cúchulainn without being fully drained.
```

Chapter 2 requirements applied:

```text
- Every active human enemy has full equipment.
- Every active human enemy has intentional reaction, support, and movement.
- Secondary is optional; the jobs' primary commands already express the roles.
- No active guests are present.
- Gaffgarion must remain weapon-dependent and strippable: no Safeguard/Maintenance, no
  Shirahadori/Blade Grasp, and no non-strippable Blood Sword behavior.
- No Time Mage engine and no second Summoner; protect the no-resupply chain into Cúchulainn.
```

## Sanctioned exceptions (carried precedents)

```text
DRAIN / self-heal on the boss — allowed and intended (Gallows 020 precedent): Shadowblade stays
  WEAPON-tied (Blood Sword in this mod), so the steal/break counter remains the fair, telegraphed
  answer.
SUMMONER — allowed (Balias Tor 016 precedent): MID-TIER summons with intact charge times; here it
  pressures the gate defenders, not the Ramza-solo phase, so it doesn't double up on the duel.
```

## Boss rare loot

```text
Gaffgarion -> BLOOD SWORD (23).
WHY IT FITS: it is his drain identity as an item. Steal/Rend Weapon both neutralizes Shadowblade
  sustain and claims the first rare boss prize. It is non-buyable and thematically perfect, but not
  Chapter-4 best gear.
IMPLEMENTATION: keep it as his equipped weapon and steal target. If no separate drop field exists,
  the equipped Blood Sword is the reward path; do not add a second rare.
```

## Proposed Composition (New Game++ Lionel Gate v2)

Keep the exact roster; Gaffgarion is the boss spike. Gaffgarion `103`; the outside gate team ranges
from `100`–`102`, with the Summoner and lead Knight carrying the pressure.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Gaffgarion (BOSS) | Dark Knight | `103` | Blood Sword sustain; disarm/steal him, then kill. Dies here. |
| n | Gate Captain | Knight | `102` | Main outside anchor; pressures lever control. |
| n | Rend Knight | Knight | `101` | Gear pressure on defenders; keeps Safeguard relevant. |
| n | Lever Guard | Knight | `101` | Blocks easy lever access and prevents passive turtling. |
| n | Archer | Archer | `101` | Ranged pressure on the gate defenders. |
| n | Archer | Archer | `100` | Second bow; covers the other approach to the gate. |
| n | Gate Summoner | Summoner | `102` | Mid-tier AoE shelling the defenders; no second Summoner. |

Reasoning:

The faithful move is to **make Gaffgarion the boss spike, keep the Blood Sword denial puzzle, and
let one Summoner punish the gate cluster**. Phase 1 isolates Ramza with a `103` self-healing Dark
Knight; trading blows loses if the player never steals or breaks the Blood Sword. Meanwhile the
outside team must survive three Knights, two Archers, and a faster single Summoner while reaching
the lever. This should tax resources before Cúchulainn, but not exhaust them.

## Builds (final-shop quality; Order garrison + Dark Knight boss flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Gaffgarion — Dark Knight BOSS (Lv 103) — rare: Blood Sword

```text
Job: Dark Knight (id TBD)   JobLevel: 8   Primary: Dark Sword / Shadowblade (Drain) — WEAPON-tied
Secondary: none extra (Drain is the threat)
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +2 (487)
Head/Body: shop heavy helm + heavy armor (ids TBD)
Accessory: Bracers (218)
Right hand: BLOOD SWORD (23) — his rare; the steal/break target and reward path
Left hand: none / two-hand marker (254)
Forbidden on Gaffgarion here: Safeguard/Maintenance, Shirahadori/Blade Grasp, non-strippable weapon.
DIES here. Do not add a second rare item beyond Blood Sword.
```

Role: the boss. Self-heals via Shadowblade until disarmed; the Blood Sword is both the off-switch
and the prize.

### Knight x3 (Lv 102 / 101 / 101) — gate siege

```text
Gate Captain:
Job: Knight (76)   JobLevel: 8   Secondary: none
Primary: Battle Skill / Rend is inherent to the job.
Reaction: Counter (442)   Support: Defense Boost (id TBD)   Movement: Movement +1 (486)
Head/Body: shop heavy helm + heavy armor (ids TBD)
Accessory: Bracers (218)   Right hand: Runeblade (30) or Icebrand (29)   Left: shop shield (id TBD)

Rend Knight:
Job: Knight (76)   JobLevel: 8   Secondary: none
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head/Body: shop heavy helm + heavy armor (ids TBD)
Accessory: Bracers (218)   Right hand: Runeblade (30) or Icebrand (29)   Left: shop shield (id TBD)

Lever Guard:
Job: Knight (76)   JobLevel: 8   Secondary: none
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head/Body: shop heavy helm + heavy armor (ids TBD)
Accessory: Bracers (218)   Right hand: Runeblade (30) or Icebrand (29)   Left: shop shield (id TBD)
```

Role: the gate siege — bodies that pressure the defense team and the lever. They can threaten gear,
but the Blood Sword remains the only rare and the only boss off-switch.

### Archer x2 (Lv 101 / 100)

```text
Job: Archer (77)   JobLevel: 8   Secondary: none
Reaction: Reflexes (449)   Support: Concentration (469)   Movement: Movement +1 (486)
Head: Thief's Cap (168)   Body: Black Garb (198)   Accessory: Bracers (218)
Right hand: Windslash Bow (87)   Left hand: none / two-hand marker (254)
```

Role: ranged punishment on the gate defenders.

### Summoner (Lv 102) — mid-tier summons

```text
Job: Summoner (82)   JobLevel: 8   Secondary: none
Primary: Summon (mid-tier: Ifrit / Shiva / Ramuh / Titan — NOT best summons; reserved later)
Reaction: Reflexes (449)   Support: Swiftness/Short Charge or Arcane Strength (id TBD)
Movement: Movement +1 (486)
Head: cloth/mage hat (id TBD)   Body: shop robe (id TBD)
Accessory: Featherweave Cloak (234)   Right hand: shop magic-boost rod (id TBD)   Left: none (255)
```

Role: AoE that punishes a clumped gate defense; keep charge times intact so it can be
raced/interrupted. There is only one Summoner because the next battle has no resupply.

## Positioning Plan

```text
Phase 1: Gaffgarion starts inside the gate with Ramza split off to face him alone (or near-alone).
He should be close enough to force the duel, but Blood Sword steal/break must be attemptable before
  the duel becomes a pure drain race.
The 3 Knights + 2 Archers + Summoner start OUTSIDE the gate pressing the player's defense team and
  the lever.
The Summoner starts back with a sightline onto the defenders' likely cluster, but remains reachable
  by a committed ranged threat or dive after the first summon window.
Preserve the LEVER + gate-open trigger that reunites the party.
Preserve Gaffgarion's boss/death scripting (he dies here; Blood Sword steals/yields).
```

The gate should say: "Ramza, take the Dark Knight's sword or lose the duel — everyone else, hold
the line and pull the lever — and claim the Blood Sword when he falls."

## Simulation Plan and Results

Simulation artifact:

```text
tmp/fft-level-design-021-lionel-castle-gate/
```

Model scope:

```text
First four rounds only; compares Ramza's Blood Sword duel, outside gate pressure, disarm payoff,
and no-resupply chain tax. It rejects variants that protect Gaffgarion from disarm, add Time Mage
tempo, or add a second Summoner before Cúchulainn.
```

Iteration results:

| Candidate | Enemies | Enemy actions | Pressure armed | Pressure disarmed | Disarm payoff | Chain tax | Delta vs v1 | Result |
|-----------|---------|---------------|----------------|-------------------|---------------|-----------|-------------|--------|
| v1 current Blood Sword gate | 7 | 23.2 | 137.6 | 88.7 | 35.5% | 21.5 | +0.0% | Baseline |
| Gaffgarion protected from disarm | 7 | 23.2 | 154.6 | 106.9 | 30.9% | 22.0 | +12.4% | Rejected: invalidates Blood Sword answer |
| Second Summoner shelling | 8 | 26.4 | 192.9 | 131.3 | 31.9% | 41.3 | +40.2% | Rejected: no-resupply tax |
| Add Time Mage tempo | 8 | 26.4 | 164.3 | 107.9 | 34.4% | 35.0 | +19.4% | Rejected: wrong identity |
| v2 two-front payoff | 7 | 23.2 | 153.8 | 98.4 | 36.0% | 24.6 | +11.8% | Accepted |

Decision:

```text
Keep the canonical roster, use Blood Sword consistently, make one Knight and the Summoner the
outside pressure upgrades, and do not add Time Mage tempo or a second Summoner before the
no-resupply Cúchulainn fight.
```

## Current Implementation (v1, entry 415 — superseded by v2 design)

Applied with `python tools/battle_patch.py lionel_gate`; diff contained to local entry 31 (global
415), 71 bytes.

```text
s0  Gaffgarion  L103 jl8  (job 17 + secondary KEPT)  R Counter  S Atk-Boost  M +1  heavy kit + BLOOD SWORD (two-handed) + Bracers
s3  Knight      L101 jl8  R Counter  S Atk-Boost  M +1  heavy shop kit + Runeblade + Shield  (Rend innate)
s4  Knight      L101 jl8  (same kit)
s5  Knight      L101 jl8  (same kit)
s1  Archer      L101 jl8  R Reflexes  S Concentration  M +1  Thief's Cap / Black Garb / Bracers + Windslash Bow
s2  Archer      L100 jl8  (same kit)
s6  Summoner    L101 jl8  R Reflexes  M +1  Mage Hat / shop Robe / Featherweave + shop Rod
```

This implementation remains the shipped v1 data. The v2 redesign above is **documentation only** in
this pass; it requires a later implementation pass to tune Gaffgarion's movement, the outside
gate-team roles, and the Summoner pressure while preserving the Blood Sword steal/break answer.

## Future Implementation Checklist (v2)

- [x] Identify Lionel Gate ENTD entry (415); fill "Local Data Confirmed".
- [x] Dump original entry; verify Gaffgarion + 3 Knight + 2 Archer + 1 Summoner.
- [x] Confirm job IDs; keep Shadowblade tied to his weapon (Blood Sword, the steal target).
- [ ] Keep Blood Sword (23) as Gaffgarion's equipped weapon and steal/break reward path.
- [ ] Explicitly avoid Safeguard/Maintenance or any non-strippable weapon behavior on Gaffgarion.
- [ ] Set v2 levels: Gaffgarion `103`; Gate Captain + Gate Summoner `102`; Rend Knight + Lever
  Guard + lead Archer `101`; second Archer `100`.
- [ ] Set JobLevel `8` on all active enemies.
- [ ] Give every active human enemy complete equipment plus intentional reaction/support/movement.
- [ ] Preserve Gaffgarion's job/secondary -> Drain + death scripting; two-phase/lever is event data.
- [ ] Preserve no-resupply chain balance into Cúchulainn; no Time Mage and no second Summoner.
- [ ] Patch the embedded ENTD in a later implementation pass; no binary/data change in this doc pass.
- [ ] Re-dump and diff; changes small and intentional.
- [ ] Playtest from a NG+ save; confirm Steal Weapon (Blood Sword) shuts off Drain and he dies/drops it.

## Test Questions

- Is Phase 1 a real solo puzzle — must Ramza disarm Gaffgarion rather than out-trade his Drain?
- Can the player Steal Weapon / Rend the Blood Sword mid-fight, switching off Shadowblade?
- Does Gaffgarion stay strippable (no Safeguard/Maintenance or non-strippable weapon behavior)?
- Does the gate-defense team face genuine pressure (3 Knights, 2 Archers, Summoner) at the lever?
- Does Gaffgarion DIE here and yield the Blood Sword as the rare prize?
- Is Blood Sword clearly mid-tier/non-best (no Ch4-reserved best gear leaked early)?
- Are Time Mage tempo and second-Summoner shelling still absent?
- Does the no-resupply lead-in to Cúchulainn make resource discipline matter without being unfair?
- Is it a clear boss step above the Gallows but still below Cúchulainn (the chapter finale)?

## Sources

- Game8, "Lionel Castle Gate Walkthrough (Battle 20)": roster (Gaffgarion + 3 Knight, 2 Archer,
  1 Summoner), objective "Defeat all enemies!", recommended level ~23, deploy 5, two-phase split
  (Ramza vs Gaffgarion + gate defense + lever), disarm priority on his ANCIENT SWORD (Steal/Rend
  Weapon) to stop Shadowblade, no resupply before Cúchulainn. Local item-data correction maps the
  actual mod reward to Blood Sword (23), not Ancient Sword.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553180
- Game8, "How to Beat Gaffgarion": Shadowblade/Drain and the disarm counter.
  https://game8.co/games/Final-Fantasy-Tactics/archives/556394
- Final Fantasy Wiki, "Lionel Castle" / "Ancient Sword": story/terrain + item tier context.
  https://finalfantasy.fandom.com/wiki/Lionel_Castle
- Local: `docs/battles/011-chapter-2-overview.md` (enemy-party escalation + rare-boss-loot rules),
  `020-golgollada-gallows.md` (Gaffgarion sub-boss / disarm puzzle, retreat-no-loot), `016-balias-tor.md`
  (Summoner mid-tier rule), `014-zeirchele-falls.md` (Gaffgarion Dark Knight intro).
</content>
