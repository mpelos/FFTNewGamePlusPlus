# 047 - Limberry Castle Gate

Status: designed (not yet implemented)
Chapter: 4 — "In the Name of Love"
Battle order: Battle 42 (Limberry chain 1 of 3 — NO resupply between 42→43→44)
Target version: Enhanced v1.5.0
ENTD: global entry **TBD** — confirm on Windows game data
File: `battle_entd*_ent.bin` (TBD) / `OverrideEntryData` rows (TBD)

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `037-chapter-4-overview.md`. LIMBERRY CHAIN: 42 (`047`) → 43 (`048`) → 44 (`049`), one loadout.

## Original Battle

Objective:

```text
Defeat all enemies!   (but the battle ENDS when ONE Assassin is reduced to CRITICAL — they flee)
```

Player deployment:

```text
Up to 5 units, including Ramza. No guests. NO outfitter access (chain 1/3).
```

Original enemy composition (verified via Game8, Battle 42):

```text
Celia    (Assassin — teleport killer; Charm/Stone/Stop/Toad + ULTIMA)
Lettie   (Assassin — teleport killer; Charm/Stone/Stop/Toad + ULTIMA)
4x Reaver (demon/undead monster bodies)
```

Public walkthrough details:

```text
Recommended level: ~60.  Difficulty: 5/5 stars.  Deploy up to 5.  NO resupply (Limberry chain 1/3).
WIN/END: the fight ends the instant ONE assassin hits CRITICAL health — Celia & Lettie FLEE (they are
  not killed here; their reckoning comes later). So this is a flee-on-critical RACE, like Ch3 Roof (035).
THE THREAT — CELIA & LETTIE: fast teleporting assassins with a nasty status kit (Charm, Stone/Petrify,
  Stop, Toad) AND ULTIMA (massive AoE). KEY TENSION: the walkthrough notes they cast Ultima MORE when
  your party is status-IMMUNE — so full immunity trades "no status" for "more Ultima." A real choice.
ADDS: 4 Reavers (demon monster bodies) press while the assassins flit and snipe.
Rewards: 34,300 Gil, Echo Herbs; buried (Gaia Gear, Black Robe, Hermes Shoes, Bracers).
```

Design reading:

Limberry Gate is **the assassin flee-race, escalated to 5★** and opening the no-resupply Limberry
gauntlet. It reprises Ch3's Riovanes Roof (`035`) — burst ONE teleporting assassin to critical to end
it — but raises the stakes with **Ultima** and a fuller hard-status kit, plus a **genuine build
tension**: stack status immunity and they answer with more Ultima; go unprotected and you eat
Charm/Stop/Petrify. Its identity is **a high-mobility status-vs-Ultima race against two flitting
killers and their demon escort, on no resupply** — won by fast focus and a *balanced* (not all-or-
nothing) defensive build.

For New Game++ the identity must stay: **a 5★ teleporting-assassin flee-race opening the Limberry
chain — burst one assassin to critical while navigating the deliberate status-immunity-vs-Ultima
tradeoff and the Reaver escort — with every lethal effect resistable and telegraphed (no hard lock,
no unavoidable nuke), and NO drop (they flee).**

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm slots: Celia + Lettie (Assassins) + 4 Reaver, plus the player slots. NO outfitter (chain 1/3).
Keep the FLEE-ON-CRITICAL end trigger (one assassin to critical ends the fight) — it IS the win shape.
Keep the assassins' TELEPORT mobility + their status kit (Charm/Stone/Stop/Toad) + ULTIMA, AND the
  "more Ultima vs status-immune party" targeting bias (the build tension is the puzzle).
This is a boss-tier chain fight: assassins 104, Reavers 103. NO rare (they flee).
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
Leave the buried treasure (Gaia Gear, Black Robe, Hermes Shoes) as-is — map loot.
```

Job IDs (carry over known, verify the rest in-game):

```text
Assassin id            (TBD - verify; Celia/Lettie — Ch3 debut, Roof 035)
Reaver id              (TBD - verify; demon/undead monster)
```

## Job Escalation (Chapter 4 rule)

```text
CHANGE: NO new caste. The escalation is the ASSASSINS themselves — the Ch3 Roof assassins (035) return
  at 5★ with ULTIMA and a fuller status kit, plus the status-immunity-vs-Ultima targeting tension. The
  4 Reaver demon bodies are the escort.
WHY: the fight's identity is already "burst a teleporting assassin to critical under status pressure."
  The faithful Ch4 escalation is to deliver those assassins at full endgame power (Ultima + the
  immunity tradeoff) — NOT to add a second new mechanic. The build tension IS the one new demand.
CONSTRAINTS (carry Ch3 Roof precedent 035 + the Lucavi/boss mass-status cap):
  - ALL lethal/control effects (Charm/Stone/Stop/Toad/instant-death) must be RESISTABLE and NON-SPAM —
    never a hard lock. The player must be able to survive without full immunity.
  - ULTIMA is ONE telegraphed, spaceable AoE per caster — not instant, not unavoidable. Preserve the
    "more likely vs status-immune" bias so the choice (eat soft status OR face Ultima) stays real and
    BALANCED builds are rewarded over all-or-nothing immunity.
  - FLEE-ON-CRITICAL preserved → NO drop here.
WHAT IS NOT CHANGED: the flee-race win shape, the teleport mobility, and the Reaver escort remain.
```

## Sanctioned exceptions (carried precedents)

```text
ASSASSIN STATUS / INSTANT-DEATH (Celia/Lettie) — Charm/Stone/Stop/Toad + death effects allowed as their
  identity BUT resistable + non-spam + telegraphed; no hard lock (Ch3 Roof 035). A non-immune party
  must be able to survive — these are race-pressure, not a lockout.
ULTIMA (boss mass-AoE) — ONE telegraphed, spaceable AoE per assassin; not instant; the Lucavi/boss
  mass-status cap. Keep the "more vs status-immune" targeting so the tradeoff stays meaningful.
FLEE-ON-CRITICAL — preserved (the race); → no rare drop (retreat = no drop).
REAVER DEMON ADDS — monster bodies; innate kit; press while the assassins flit.
```

## Boss rare loot

```text
None HERE. Celia & Lettie FLEE on critical (retreat = no drop). Their reckoning — and any loot — is
deferred to where they are decisively defeated (their later Ultima-Demon forms / the Limberry interior).
The chapter's deferred MASAMUNE + GENJI belong to ELMDOR and pay at the Limberry KEEP (`048`), not here.
Generics (Reavers) are monster bodies. Buried map treasure stays as-is.
```

## Proposed Composition (New Game++ Limberry Gate v1)

Keep the count (6) and the flee-race shape; deliver the assassins at full 5★ power with the build
tension intact. Assassins `104`; Reavers `103`. No resupply (chain 1/3) — design lethality to be
survivable on a single loadout.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Celia (BOSS) | Assassin | `104` | Teleport killer; Charm/Stop/Stone/Toad + Ultima; flee-on-critical. |
| n | Lettie (BOSS) | Assassin | `104` | Second assassin; same kit; the race ends when EITHER hits critical. |
| n | Reaver | Reaver | `103` | Demon body; presses the front while assassins flit. |
| n | Reaver | Reaver | `103` | Second demon body. |
| n | Reaver | Reaver | `103` | Third demon body; flanks. |
| n | Reaver | Reaver | `103` | Fourth demon body; screens the assassins. |

Reasoning:

The faithful move is to **re-stage the assassin flee-race at endgame intensity and protect the build
tension**. Both assassins at `104` teleport and threaten Ultima + resistable hard-status; the player
races to drop ONE to critical while the four Reavers (`103`) pressure. Crucially, the status is
resistable/non-spam and Ultima is telegraphed and *more frequent against immune parties* — so a
balanced defensive build (some resist, not blanket immunity) is the intended answer, exactly as the
original teaches. No resupply means lethality is tuned to be survivable on one loadout (no
guaranteed-kill combos). No rare — they flee.

## Builds (Chapter-4 boss quality; Limberry assassin flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Celia & Lettie (Lv 104) — BOSS assassins

```text
Job: Assassin (id TBD)   JobLevel: 8   Primary: assassin arts (Charm/Stone/Stop/Toad + death effect —
  ALL resistable, non-spam, telegraphed) + ULTIMA (one telegraphed AoE)   Secondary: basic
Reaction: (mobility) Reflexes / First Strike (id TBD)   Support: Attack Boost (465) / MA-boost
  Movement: Teleport (id TBD) or Movement +2 (487)
Head: Tier-A/boss headgear (id TBD)   Body: Black Robe-equivalent (id TBD)
Accessory: Tier-A accessory (id TBD)   Right hand: assassin dagger (id TBD)   Left: none (255)
```

Role: the flee-race targets — burst one to critical to end it; keep status resistable and Ultima
telegraphed (and biased toward status-immune parties). Do NOT make them an instant-death lock.

### Reaver x4 (Lv 103) — demon escort (monsters)

```text
Monster: Reaver (id TBD)   demon/undead flag per vanilla; innate skillset (drain/claw/status bite).
No equipment slots (monster). Set only LEVEL.
```

Role: the demon bodies that pressure the front while the assassins teleport and snipe.

## Positioning Plan

```text
Castle gate: the two Assassins start spread (teleport range onto the back-line), the four Reavers
  forward as the screen between the player and the assassins. Keep sightlines so Ultima is a telegraphed
  threat the player can space against, not an ambush nuke.
Preserve the FLEE-ON-CRITICAL trigger and the assassins' teleport mobility (the race identity).
Tune for NO resupply: survivable lethality on one loadout; status resistable; Ultima spaceable.
Keep the status-immunity-vs-Ultima bias intact so balanced builds are rewarded.
```

The gate should say: "two knives in the dark open Limberry's gauntlet — run one of them to the brink
before their Ultima finds you, and don't bet everything on immunity."

## Implementation Checklist

- [ ] Identify Limberry Gate `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify Celia + Lettie (Assassins) + 4 Reaver + player slots.
- [ ] Keep the FLEE-ON-CRITICAL end trigger (one assassin to critical ends it) → NO drop.
- [ ] Set assassins `104`, Reavers `103`; keep teleport mobility.
- [ ] Make ALL status (Charm/Stone/Stop/Toad/death) resistable + non-spam + telegraphed (no hard lock).
- [ ] Keep ULTIMA as ONE telegraphed, spaceable AoE per assassin; preserve the "more vs immune" bias.
- [ ] Tune lethality to be survivable on ONE loadout (chain 1/3, no resupply).
- [ ] Set JobLevel `8` on the assassin slots.
- [ ] Patch via the correct layer; keep the diff inside the Limberry Gate window only.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify flee trigger + status caps.
- [ ] Install mod, test from a New Game+ save (entering with chain-realistic resources); confirm the
      race is winnable without blanket immunity and no hard lock/Ultima-ambush occurs.

## Test Questions

- Is the flee-on-critical race intact (burst ONE assassin to critical to end it), with NO drop?
- Are Charm/Stone/Stop/Toad/death ALL resistable + non-spam + telegraphed — never a hard lock?
- Is Ultima ONE telegraphed, spaceable AoE per assassin (not an ambush nuke), and is the
  "more-vs-immune" bias preserved so balanced builds beat blanket immunity?
- Is the fight survivable on ONE loadout (no resupply, chain 1/3)?
- Are the assassins `104` and Reavers `103` — a boss-tier chain opener, not an over-spike?
- Does it read as the Ch3-Roof assassin race reborn at endgame intensity, opening Limberry?

## Sources

- Game8, "Limberry Castle Gate Walkthrough (Battle 42)": roster (4 Reaver + Celia + Lettie Assassins),
  ends when one assassin hits critical (they flee), rec ~60, 5/5 stars, deploy 5, Charm/Stone/Stop/Toad
  + Ultima (more vs status-immune), no resupply (Limberry chain), rewards (34,300 Gil; buried Gaia Gear,
  Black Robe, Hermes Shoes). https://game8.co/games/Final-Fantasy-Tactics/archives/553202
- Final Fantasy Wiki, "Celia and Lettie" / "Limberry Castle": story/terrain context.
  https://finalfantasy.fandom.com/wiki/Celia_and_Lettie
- Local: `037-chapter-4-overview.md` (rules), `035-riovanes-castle-roof.md` (Ch3 assassin flee-race
  precedent), `048-limberry-keep.md` & `049-limberry-undercroft.md` (the rest of the chain — to be designed).
```
</content>
