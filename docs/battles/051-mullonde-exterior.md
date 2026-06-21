# 051 - Mullonde Cathedral Exterior (Murond Holy Place)

Status: ✅ implemented (v1, entry 460)
Chapter: 4 — "In the Name of Love"
Battle order: Battle 46 (Mullonde chain 1 of 3 — NO resupply across 46→47→48)
Target version: Enhanced v1.5.0
ENTD: global entry **460** (local 76, entd4)
File: `battle_entd4_ent.bin`

## Implemented (v1, entry 460)

```text
DATA (exact roster match, all generic casters spr128/name255):
  slot 0 = White Mage (job 79, rh=64 staff)   -> the HIDDEN rooftop heal + Raise-multi sustain engine.
  slot 1 = Summoner   (job 82, rh=57 Dragon Rod) -> AoE; the rod is the stealable reward (rh KEPT).
  slots 2,3 = Geomancer (job 86; were naked)  -> terrain elemental.
  slots 4,5 = Orator   (job 84, rh=72 gun)    -> soft status (one-disruptor cap).

CHANGE (faithful, no boss / no rare): scale to the chain-opener band + arm the bare casters + jl8.
  White Mage = 103 (priority kill), rest = 102. jl8 on all (the White Mage was jl5 -> jl8 so its
  Cure/Raise tier is real -- the sustain IS the fight). Armed each with Mage Hat (167) + Luminous/shop
  Robe (206) + Featherweave Cloak (234); Geomancers given a shop Rod (56); White Mage staff (64),
  Summoner Dragon Rod (57), Orator guns (72) all KEPT. Verticality / hidden-roof start / split
  deployment live in the map + unit tail and are untouched. Buried Elixir + Dragon Rod steal left as-is.
```

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `037-chapter-4-overview.md`. MULLONDE CHAIN: 46 (`051`) → 47 (`052`) → 48 (`053`), one loadout.

## Original Battle

Objective:

```text
Defeat all enemies!
```

Player deployment:

```text
Up to 5 units, including Ramza, SPLIT into two groups (split deployment). No outfitter (chain 1/3).
```

Original enemy composition (verified via Game8, Battle 46):

```text
1x White Mage   (HIDDEN on the roof — heals AND raises multiple enemies; the sustain engine)
2x Geomancer    (terrain attacks)
2x Orator       (status / charm)
1x Summoner     (AoE; holds a stealable Dragon Rod)
```

Public walkthrough details:

```text
Recommended level: ~60.  Difficulty: 3/5 stars.  Deploy up to 5 (SPLIT into two groups).  Win: defeat all.
TERRAIN: cathedral exterior with ROOFED structures (verticality).
THE THREAT — the HIDDEN WHITE MAGE on the roof: he heals and RAISES multiple enemies at once. The
  walkthrough's #1 tip: take him out FIRST (use height-ignoring abilities to reach the roof), or the
  caster band won't stay down.
SUPPORT: 2 Geomancers (terrain attacks), 2 Orators (status/charm), 1 Summoner (AoE; Dragon Rod steal).
Rewards: 30,600 Gil, X Potion; buried (rare Elixir possible).
```

Design reading:

The Cathedral Exterior is **the hidden-healer caster screen** opening the Mullonde gauntlet. Its
identity is **a sustain-priority puzzle on holy ground**: a varied caster band (Geomancer terrain,
Orator status, Summoner AoE) that *won't stay dead* because a **White Mage hidden on the roof** heals
and raises it — so the player must **reach and kill the rooftop healer first** (height-ignoring
damage), all while the party starts **split into two groups** and must work both flanks or regroup.
It's a 3/5★ chain-opener — lighter than the Nave/Sanctuary bosses ahead — whose one demand is *find
and silence the sustain, then mop the casters*.

For New Game++ the identity must stay: **a holy-ground caster screen whose whole demand is the hidden
rooftop White Mage's heal/raise sustain — reach and kill it (height-ignoring damage) or the band
revives — under a split deployment, on no resupply; boss-less and rare-less, the Mullonde chain's
opener.**

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm slots: hidden White Mage (roof) + 2 Geomancer + 2 Orator + 1 Summoner, + the SPLIT player
  deployment. NO outfitter (chain 1/3).
Keep the HIDDEN ROOFTOP White Mage (heal + Raise-multi sustain) + the ROOFED verticality + the SPLIT
  deployment (these ARE the fight). Keep the Summoner's stealable Dragon Rod.
This is a no-boss, no-rare chain OPENER: levels 102-103; lighter than the Nave/Sanctuary ahead.
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
Leave the buried map treasure (possible Elixir) + the Dragon Rod steal as-is — existing loot.
```

Job IDs (carry over known, verify the rest in-game):

```text
White Mage job id      (TBD - verify; the hidden sustain engine)
Geomancer job id       (TBD - verify; Ch3 debut, 019)
Orator / Mediator id   (TBD - verify; enemy Orator, Ch3 debut 025)
Summoner job id        (TBD - verify)
```

## Job Escalation (Chapter 4 rule)

```text
CHANGE: NO new caste / NO generic swap. The escalation is the SUSTAIN — the hidden rooftop White Mage
  is a genuine heal+Raise-multi engine at Ch4 strength, so chipping the casters fails until he dies;
  the SPLIT deployment + rooftop verticality make reaching him the puzzle.
WHY: the fight's identity is already "kill the hidden reviving healer, then the casters fold." The
  faithful Ch4 escalation is to make that sustain matter (Raise-multi at endgame strength) on a
  vertical map with a split start — NOT to bolt on a new mechanic. The hidden-healer priority IS the
  one demand. This is a chain OPENER (3/5★) — keep it lighter than the bosses ahead.
CONSTRAINTS (carried): Orator charm/status SOFT, one-disruptor cap, no hard lock (025); Geomancer
  terrain attacks established (019); Summoner INTACT charge times, race-able (028); White Mage sustain
  answered by reaching/killing it or Silence — not a lock.
WHAT IS NOT CHANGED: the caster roster, the rooftop hidden healer, the split deployment, and the
  "defeat all" objective remain. No boss, no rare.
```

## Sanctioned exceptions (carried precedents)

```text
HIDDEN-HEALER SUSTAIN (White Mage, roof) — heal + Raise-multi; the answer is to REACH and kill it
  (height-ignoring damage) or Silence it. Sustain, not a lock; the whole point of the fight.
ORATOR CHARM/STATUS — soft, resistable, ONE-disruptor cap, no hard lock (025 precedent).
GEOMANCER TERRAIN ATTACKS — established (019); ranged elemental, race-able.
SUMMONER AoE — mid-tier, INTACT charge times, race-able (028); Dragon Rod stealable (vanilla).
SPLIT DEPLOYMENT — a positioning wrinkle, not a status; preserved as the tactical layer.
```

## Boss rare loot

```text
None. No named boss here — no rare boss item (per the Chapter 4 overview tiering). Generics stay
Chapter-4 shop-tier. The Summoner's stealable Dragon Rod + the buried Elixir are EXISTING loot — leave
as-is. (Tier-S best-of-best begins at the NAVE, 052.)
```

## Proposed Composition (New Game++ Mullonde Exterior v1)

Keep the count (6) and the hidden-healer caster-screen feel; make the rooftop White Mage a real
sustain engine. Chain-opener levels `102`–`103` (lighter than the Nave/Sanctuary). White Mage `103`
(priority); rest `102`.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | White Mage (HIDDEN, roof) | White Mage | `103` | Heal + Raise-multi sustain — the priority kill; reach the roof. |
| n | Geomancer | Geomancer | `102` | Terrain elemental attacks across the courtyard. |
| n | Geomancer | Geomancer | `102` | Second Geomancer; pressures the split groups. |
| n | Orator | Orator | `102` | Soft status / charm (one-disruptor cap). |
| n | Orator | Orator | `102` | Second Orator; harasses but no hard lock. |
| n | Summoner | Summoner | `102` | AoE (intact charge times); Dragon Rod steal. |

Reasoning:

The faithful move is to **make the hidden healer the whole puzzle and keep it a lighter opener**. The
rooftop White Mage (`103`) heals and raises the band, so the player must use height-ignoring damage to
reach and kill it first — then the Geomancers, Orators, and Summoner fold. The split deployment forces
the player to work two flanks or regroup under fire. Levels stay chain-opener tier (`102`–`103`), and
the status stays soft (Orator one-disruptor cap) — keeping it 3/5★, the calm before the Nave's triple
boss. No rare (no boss); the Dragon Rod steal stays as the optional reward.

## Builds (Chapter-4 quality; holy-ground caster flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### White Mage (Lv 103) — HIDDEN sustain (roof)

```text
Job: White Mage (id TBD)   JobLevel: 8   Primary: White Magic (Cure-line + RAISE/Raise-2 — multi-target)
Reaction: Reflexes (449)   Support: MA/Magick-boost (id TBD)   Movement: Movement +1 (486) / Ignore Height
Head: mage hat (id TBD)   Body: shop robe (id TBD)
Accessory: Featherweave Cloak (234)   Right hand: Healing Staff / magic-boost rod (id TBD)   Left: none (255)
Starts HIDDEN on the roof. The sustain engine — kill it first.
```

Role: heals and revives the band; the priority target; answered by reaching it or Silence.

### Geomancer x2 (Lv 102) — terrain

```text
Job: Geomancer (id TBD)   JobLevel: 8   Primary: Geomancy (terrain elemental)
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head: shop hat (id TBD)   Body: shop robe/clothes (id TBD)   Accessory: Featherweave Cloak (234)
Right hand: shop element-rod / sword (id TBD)   Left: shop shield (id TBD)
```

Role: ranged terrain attacks pressuring the split groups; race-able.

### Orator x2 (Lv 102) — soft status

```text
Job: Orator / Mediator (id TBD)   JobLevel: 8   Secondary: none
Soft status / charm (resistable; ONE-disruptor cap across the two — not both hard-CCing).
Reaction: Reflexes (449)   Support: MA-boost (id TBD)   Movement: Movement +1 (486)
Head: shop hat (id TBD)   Body: shop robe (id TBD)   Accessory: Featherweave Cloak (234)
Right hand: shop gun/rod (id TBD)   Left: none (255)
```

Role: soft harass; no hard lock.

### Summoner (Lv 102) — AoE + steal-bait

```text
Job: Summoner (id TBD)   JobLevel: 8   Mid-tier summons, INTACT charge times.
Reaction: Reflexes (449)   Support: MA-boost (id TBD)   Movement: Movement +1 (486)
Body: shop robe (id TBD)   Accessory: Featherweave Cloak (234)   Right hand: Dragon Rod (stealable, id TBD)
```

Role: AoE pressure; the Dragon Rod is an optional steal reward.

## Positioning Plan

```text
Cathedral exterior: the White Mage starts HIDDEN on a ROOF with sustain sightlines over the courtyard;
  the Geomancers/Orators/Summoner spread across the holy ground; the PLAYER deploys SPLIT into two
  groups (work both flanks or regroup). Keep the rooftop height (the healer must be reached with
  height-ignoring damage) and the split start.
Preserve the verticality + split deployment (the tactical puzzle) and the hidden-healer priority.
Keep it a lighter chain opener: levels 102-103, soft status, no boss.
```

The cathedral steps should say: "the choir of the church won't fall while their hidden cantor sings —
climb to the roof and silence him, then the rest is mopping up."

## Implementation Checklist

- [ ] Identify Mullonde Exterior `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify hidden White Mage + 2 Geomancer + 2 Orator + 1 Summoner + the split deploy.
- [ ] Keep the hidden rooftop White Mage (heal + Raise-multi) + roofed verticality + split deployment.
- [ ] Keep Orator status SOFT (one-disruptor cap); Summoner charge times intact; Dragon Rod stealable.
- [ ] Set levels: White Mage `103`; the rest `102` (chain-opener band).
- [ ] Set JobLevel `8` on all active enemy slots.
- [ ] Patch via the correct layer; keep the diff inside the Mullonde Exterior window only.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify hidden-healer + split + verticality.
- [ ] Install mod, test from a New Game+ save; confirm the hidden healer is the priority, split start works,
      and it plays as a lighter chain opener (no hard lock).

## Test Questions

- Is the hidden rooftop White Mage the clear priority (heal/raise sustain; reach it with height-ignoring
  damage or Silence) — does the band fold once it dies?
- Does the SPLIT deployment + rooftop verticality form the tactical puzzle (work both flanks / climb)?
- Is the Orator status soft (one-disruptor cap, no hard lock) and the Summoner race-able?
- Is it clearly a LIGHTER chain opener (3/5★, levels 102-103) before the Nave's triple boss?
- Is it survivable on ONE loadout (no resupply, chain 1/3)?
- Does it read as a holy-ground caster screen with a hidden cantor, not a designed arena?

## Sources

- Game8, "Mullonde Cathedral Walkthrough (Battle 46)": roster (hidden White Mage + 2 Geomancer +
  2 Orator + 1 Summoner), "Defeat all enemies!", rec ~60, 3/5 stars, deploy 5 split into two groups,
  cathedral-exterior rooftops, kill-the-hidden-White-Mage-first + height-ignoring tips, Dragon Rod
  steal, rewards (30,600 Gil, possible Elixir).
  https://game8.co/games/Final-Fantasy-Tactics/archives/553206
- Final Fantasy Wiki, "Mullonde" / "Murond Holy Place": story/terrain context.
  https://finalfantasy.fandom.com/wiki/Mullonde
- Local: `037-chapter-4-overview.md` (rules), `019-balias-swale.md` (Geomancer), `025-mining-town-gollund.md`
  (enemy Orator), `052-mullonde-nave.md` & `053-mullonde-sanctuary.md` (the rest of the chain — to be designed).
```
</content>
