# 018 - Goug Lowtown (Goug Machine City)

Status: ✅ implemented (v1, entry 411) — Thief→Time Mage escalation done inline
Chapter: 2 — "The Manipulator and the Subservient"
Battle order: Battle 17 (after Tchigolith Fenlands)
Target version: Enhanced v1.5.0
ENTD: global entry **411** (battle_entd4, local entry 27) — confirmed by composition (2nd Summoner fight)
File: `entd/battle_entd4_ent.bin` (embedded; swapped only in NG+ by the code mod)

> Implemented via `tools/battle_patch.py goug`. NG+-only by construction. See
> `011-chapter-2-overview.md`.

## Original Battle

Objective:

```text
Defeat all enemies!
```

Player deployment:

```text
Up to 5 units, including Ramza.
Guest: Mustadio appears as a temporary guest. His death does NOT cause a Game Over here — he
  is a bonus ally, not an escort (contrast with Zaland, where protecting him was mandatory).
```

Original enemy composition:

```text
2x Summoner
2x Archer
2x Thief   (charm — Steal Heart)
```

Public walkthrough details:

```text
Recommended level: ~19.
Urban machine-city terrain with elevation; Summoners positioned above.
The Summoners are again the biggest threat — devastating AoE; neutralize them first.
The Thieves harass and can charm (Steal Heart); Archers add ranged pressure.
Mustadio fights on his own and often goes down early, but losing him is not a failure.
```

Design reading:

Goug is **the second Summoner fight**, deliberately staged to feel different from Balias Tor.
Where Balias Tor screened its Summoners with break-Knights on an open hill, Goug screens them
with **charm-Thieves in tight urban terrain**, and the guest (Mustadio) is expendable rather
than protected. The core lesson is the same — **race the summon, kill the casters first** — but
the harassment profile (fast thieves + charm) and the cramped lanes change how the player gets
there. Because the player has *already* learned "kill the Summoners," the New Game++ escalation
must add a new twist so this isn't a re-run of Balias Tor.

For New Game++ the identity must stay: **an urban race to silence the Summoners while fast,
charming Thieves harass the approach — now under tempo pressure, so the summon clock runs faster.**

## Local Data Confirmed (entry 411)

```text
slot  cid    flags  job          role                        action
s0    0x16   0x91   22 (==cid)   ally guest (NOT Mustadio)   LEAVE (see note)
s1    0x23   0x80   35           disabled named (lvl 254)    LEAVE
s2    0x80   0x80   83 Thief     -> TIME MAGE (escalation)   SCALE -> L101, re-job 81 (jl4)
s3    0x80   0x80   83 Thief     charm harasser              SCALE -> L100
s4    0x80   0x80   83 Thief     disabled (lvl 254)          LEAVE
s5    0x81   0x40   77 Archer    ranged                      SCALE -> L101
s6    0x81   0x40   77 Archer    ranged                      SCALE -> L100
s7    0x80   0x80   82 Summoner  priority AoE                SCALE -> L101
s8    0x80   0x80   82 Summoner  priority AoE                SCALE -> L101
s9    0x80   0x80   83 Thief     charm harasser              SCALE -> L100
s10   0x80   0x80   83 Thief     anomalous lvl-1/jl-0        LEAVE (likely special/scripted)
```

Job IDs: Summoner 82, Archer 77, Thief 83, Time Mage 81. **TIC differs from the walkthrough:** 4
active Thieves (not 2), plus an anomalous lvl-1 thief (s10) left untouched. The escalation Time Mage
is **JobLevel-capped to 4** (Lenalian precedent) to bias toward Haste/Slow and keep Stop/Immobilize
off. Steal Heart stays innate on the remaining Thieves (job 83 at jl8).

### Goug ally guest (cid 0x16) — left at vanilla level

The guest here is **cid 0x16 (job 22 == cid, flags 0x91 = ally)** — NOT Mustadio (cid 0x22), who is a
party member by now. Its identity is unconfirmed, so unlike Mustadio at Zaland it was NOT added to
GuestCharIds; it stays at lvl 12. Its death is explicitly NOT a Game Over here, so a weak guest is
non-blocking. PLAYTEST: confirm who it is and, if it's a beneficial ally, add cid 0x16 to GuestCharIds.

## Job Escalation (Chapter 2 rule)

```text
CHANGE: swap ONE Thief -> a Time Mage that HASTES the Summoners (and may Slow the player).
WHY: this is the SECOND Summoner fight, so simply scaling it would re-run Balias Tor. Adding a
  Time Mage puts the summon race on a faster clock — Haste shortens the Summoners' effective
  charge, so the player must reach and silence them even quicker. It RAISES the existing
  challenge ("kill the Summoners first") rather than changing it, and distinguishes Goug from
  Balias Tor (tempo pressure vs. break-Knights). Single new wrinkle.
WHAT IS NOT CHANGED: the 2 Summoners, both Archers, and one charm-Thief keep the urban-harass
  identity; the strategy is still "race to the casters."
```

## Sanctioned exceptions (carried precedents)

```text
TIME MAGE control — allowed (Lenalian precedent, 007): Haste (on the Summoners) / Slow (on the
  player) ONLY. NO Stop, Immobilize, Don't Move, Don't Act. One Time Mage only.
CHARM (Steal Heart) — allowed on the one remaining Thief (Merchant Dorter precedent, 012): the
  player's all-male / charm-immune counter stays valid.
```

## Boss rare loot

```text
None. No named boss here — no rare item (per the Chapter 2 overview). Generics stay shop-tier.
```

## Proposed Composition (New Game++ Goug v1)

Keep the Summoner core, swap one Thief for a Time Mage (6 enemies). Summoners and Time Mage at
`101`; Archers at `100`–`101`; the remaining Thief at `100`.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Summoner (high) | Summoner | `101` | Slow-charge big AoE; the priority kill. |
| n | Summoner (high) | Summoner | `101` | Second summon threat from elevation. |
| n | Tempo (NEW) | Time Mage | `101` | Hastes the Summoners (faster clock) / Slows the player. |
| n | Archer | Archer | `101` | Ranged pressure; punishes the rush to the casters. |
| n | Archer | Archer | `100` | Second bow; covers an urban lane. |
| n | Thief (charm) | Thief | `100` | Fast harasser; Steal Heart pressure on the approach. |

Reasoning:

The faithful move is to **scale, keep the summon-race, and add tempo pressure**. The Time Mage is
the wrinkle that makes the second Summoner fight bite differently from the first: Haste on the
Summoners means the player's window to reach them shrinks, so the urban lanes and the charm-Thief
harassing the approach matter more. Two elevated Summoners with intact charge times keep the
"silence them or eat a summon" core; one Archer and one charm-Thief keep the harassment. Mustadio
helps where he can but is expendable, so the player can play aggressively toward the casters.

## Builds (final-shop quality; urban mercenary band flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Summoner x2 (Lv 101)

```text
Job: Summoner (id TBD)   JobLevel: 8   Secondary: none
Primary: Summon (mid-tier: Ifrit / Shiva / Ramuh / Titan — NOT best summons; reserved later)
Reaction: Reflexes (449)   Support: MA/Magick-boost (id TBD)   Movement: Movement +1 (486)
Head: cloth/mage hat (id TBD)   Body: shop robe (id TBD)
Accessory: Featherweave Cloak (234)   Right hand: shop magic-boost rod (id TBD)   Left: none (255)
```

Role: the priority threat. Keep charge times intact so the player can interrupt by closing/sniping.

### Time Mage (Lv 101) — NEW (job swap)

```text
Job: Time Mage (id TBD)   JobLevel: 8   Secondary: none
Skillset limit: Haste (on the Summoners) / Slow (on the player) / Float-tier ONLY.
  NO Stop, Immobilize, Don't Move, Don't Act.
Reaction: Reflexes (449)   Support: MA/Magick-boost (id TBD)   Movement: Movement +1 (486)
Head: cloth/mage hat (id TBD)   Body: shop robe (id TBD)
Accessory: Featherweave Cloak (234)   Right hand: shop magic-boost rod (id TBD)   Left: none (255)
```

Role: the tempo escalation. Hastes the Summoners to speed up the summon clock and may Slow the
player's rush — pressure without lockdown.

### Archer x2 (Lv 101 / 100)

```text
Job: Archer (77)   JobLevel: 8   Secondary: none
Reaction: Reflexes (449)   Support: Concentration (469)   Movement: Movement +1 (486)
Head: Thief's Cap (168)   Body: Black Garb (198)   Accessory: Bracers (218)
Right hand: Windslash Bow (87)   Left hand: none / two-hand marker (254)
```

Role: ranged punishment on the approach to the casters.

### Thief (Lv 100) — charm

```text
Job: Thief (83)   JobLevel: 8   Secondary: Steal (incl. Steal Heart)
Reaction: First Strike (453)   Support: Attack Boost (465)   Movement: Movement +2 (487)
Head: Thief's Cap (168)   Body: Black Garb (198)   Accessory: Germinas Boots (210)
Right hand: Air Knife (9)   Left hand: none / two-hand marker (254)
```

Role: fast harasser; charm pressure as the player commits toward the Summoners.

## Positioning Plan

```text
Both Summoners start on elevated/back urban tiles with sightlines over the approach.
The Time Mage starts near/behind the Summoners so it can Haste them turn 1.
The Archers start at mid-height covering the lanes the player must use to reach the casters.
The charm-Thief starts forward on a flank to harass the rush.
Preserve Mustadio's guest start; do NOT alter his (non-Game-Over) scripting.
```

The city should make reaching the Summoners a gauntlet — and the Time Mage's Haste means the
player has fewer turns to do it. Tempo is the new pressure.

## Implemented (v1, entry 411)

Applied with `python tools/battle_patch.py goug`; diff contained to local entry 27 (global 411),
70 bytes. The Chapter-2 escalation was a **job SWAP** (s2 Thief → Time Mage), done inline.

```text
s7  Summoner  L101 jl8  R Reflexes  M +1  Mage Hat / shop Robe / Featherweave + shop Rod
s8  Summoner  L101 jl8  (same kit)
s2  Time Mage L101 jl4  R Reflexes  M +1  (same caster kit)  -- Haste/Slow, no hard lock
s5  Archer    L101 jl8  R Reflexes  S Concentration  M +1  Thief's Cap / Black Garb / Bracers + Windslash Bow
s6  Archer    L100 jl8  (same kit)
s3  Thief     L100 jl8  R First Strike  S Atk-Boost  M +2  Thief's Cap / Black Garb / Germinas + Air Knife
s9  Thief     L100 jl8  (same kit)  -- Steal Heart innate
```

## Implementation Checklist

- [x] Identify Goug ENTD entry (411); fill "Local Data Confirmed".
- [x] Dump original entry; verify Summoners + Archers + Thieves (+ guest, disabled slots).
- [x] Confirm Summoner + Time Mage job IDs. (Summon-tier control = playtest item, as at Balias Tor.)
- [x] Swap one Thief -> Time Mage; jl capped to 4 (Haste/Slow, no hard lock).
- [x] Set levels: both Summoners + Time Mage + one Archer `101`; second Archer + Thieves `100`.
- [x] Set JobLevel `8` on scaled slots (Time Mage jl4); Steal Heart innate on the Thieves.
- [x] Guest (cid 0x16) and anomalous lvl-1 thief (s10) left untouched.
- [x] Patch the embedded ENTD (NG+-only); diff inside entry 411 only.
- [x] Re-dump and diff; changes small and intentional.
- [ ] Playtest from a NG+ save; verify Haste speeds the race fairly; confirm guest cid 0x16 identity.

## Test Questions

- Does the Time Mage's Haste make the summon race tangibly tenser than Balias Tor (a faster clock)?
- Are the Summoners still race-able (charge times intact, not instant) under Haste?
- Does Goug feel DISTINCT from Balias Tor (tempo + charm + urban vs. break + hill)?
- Is the charm-Thief a fair, counterable harasser, not a coin-flip?
- Since Mustadio's death isn't a Game Over, can the player play aggressively toward the casters?
- Is it harder than Balias Tor (later in the chapter) but below the Gaffgarion/Cúchulainn bosses?
- Does it still read as an urban summoner ambush, not a designed arena?

## Sources

- Game8, "Goug Lowtown Walkthrough (Battle 17)": roster (2 Summoner, 2 Archer, 2 Thief),
  objective "Defeat all enemies!", deploy 5, recommended level ~19, urban terrain, Summoners as
  the biggest threat (elevated AoE), Mustadio guest whose death is NOT a Game Over.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553177
- Final Fantasy Wiki, "Goug Machine City": story/terrain context.
  https://finalfantasy.fandom.com/wiki/Goug_Machine_City
- Local: `docs/battles/011-chapter-2-overview.md` (job-escalation rule), `016-balias-tor.md`
  (first Summoner fight, for contrast), `007-lenalian-plateau.md` (Time Mage control limit),
  `012-merchant-dorter.md` (Steal Heart charm precedent).
</content>
