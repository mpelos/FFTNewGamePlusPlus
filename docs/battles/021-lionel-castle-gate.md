# 021 - Lionel Castle Gate

Status: designed (not yet implemented)
Chapter: 2 — "The Manipulator and the Subservient"
Battle order: Battle 20 (after Golgollada Gallows)
Target version: Enhanced v1.5.0
ENTD: global entry **TBD** — confirm on Windows game data
File: `battle_entd*_ent.bin` (TBD) / `OverrideEntryData` rows (TBD)

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `011-chapter-2-overview.md`.

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
1x Gaffgarion   (Dark Knight BOSS — Shadowblade/Drain via his ANCIENT SWORD; dies here)
3x Knight
2x Archer
1x Summoner     (AoE pressure on the gate defenders)
```

Public walkthrough details:

```text
Recommended level: ~23.
Ramza is split off to face Gaffgarion while the others hold the gate.
TOP PRIORITY: disarm Gaffgarion — Steal Weapon (Thief) or Rend Weapon (Knight) takes his ANCIENT
  SWORD, which switches off Shadowblade (his Drain sustain). Disarmed, he is beatable.
The Knights + Archers + a Summoner press the gate-defense team; a lever opens the gate to reunite.
No resupply before the next fight (Cúchulainn), so don't burn everything.
```

Design reading:

Lionel Gate is **Gaffgarion's last stand** — the payoff to the threat established at the Gallows.
Its identity is a **two-front boss duel**: Ramza is isolated with the self-healing Dark Knight
while the rest of the party survives a siege at the gate, and the player must again solve
Gaffgarion by **denial** (steal/break his Ancient Sword to kill Shadowblade) — but now under the
added pressure of a split party and a Summoner shelling the defenders. Because he *dies* here, this
is the chapter's first **rare, non-buyable boss drop**: his **Ancient Sword** itself — the very
weapon you're trying to take off him — which doubles as the steal target and the reward. It
teaches resource discipline too (no resupply before Cúchulainn).

For New Game++ the identity must stay: **an isolated duel with a self-healing Dark Knight, solved
by stealing/breaking his Ancient Sword, while the rest of the party holds a besieged gate — and
the Ancient Sword is the rare prize for finishing him.**

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm slots: Gaffgarion + 3 Knight + 2 Archer + 1 Summoner, plus the player's split (Ramza-solo
  vs gate-defense) deployment.
CRITICAL: preserve the TWO-PHASE structure (Ramza split off + the LEVER that opens the gate).
Keep Gaffgarion's Shadowblade tied to his ANCIENT SWORD so steal/break shuts off his sustain AND
  yields the rare drop.
Gaffgarion DIES here — his rare item (Ancient Sword) is stealable/droppable (contrast the Gallows,
  020, where he carried a non-rare blade and retreated).
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
```

Job IDs (carry over known, verify the rest in-game):

```text
77 = Archer            (confirmed)
Knight job id          (TBD - verify)
Summoner job id        (TBD - verify; from Balias Tor 016)
Dark Knight job id     (TBD - verify; Gaffgarion — from Zeirchele 014 / Gallows 020)
```

## Job Escalation (Chapter 2 rule)

```text
THE ESCALATION IS BUILT IN: Gaffgarion as a full BOSS (dies) inside a TWO-PHASE split — Ramza
isolated vs the self-healing Dark Knight while the party holds a besieged gate — IS the wrinkle,
amplified by a Summoner shelling the defenders. Per "one new wrinkle per fight," NO additional
brand-new generic job is introduced; the canonical 3 Knight / 2 Archer / 1 Summoner screen is kept.
WHY: an isolated boss duel + a simultaneous gate defense + a Summoner is already a dense step up
  from the Gallows; piling on another new job would blur the "disarm Gaffgarion, hold the gate" read.
```

## Sanctioned exceptions (carried precedents)

```text
DRAIN / self-heal on the boss — allowed and intended (Gallows 020 precedent): Shadowblade stays
  WEAPON-tied (the ANCIENT SWORD), so the steal/break counter remains the fair, telegraphed answer.
SUMMONER — allowed (Balias Tor 016 precedent): MID-TIER summons with intact charge times; here it
  pressures the gate defenders, not the Ramza-solo phase, so it doesn't double up on the duel.
```

## Boss rare loot

```text
Gaffgarion -> ANCIENT SWORD (Knight Sword; non-buyable, steal/poach/drop in vanilla).
WHY IT FITS: it is literally his weapon and the disarm/steal TARGET — taking it both neutralizes
  Shadowblade and IS the reward, a perfect identity-and-mechanic match. It is the LOWEST-tier
  Knight Sword (well below Save the Queen / Excalibur / Ragnarok / Chaos Blade), so it is squarely
  MID-TIER and NOT a Chapter-4-reserved best item. First rare boss drop of the mod.
IMPLEMENTATION: set it as both his equipped weapon AND his rare drop/steal so the player can either
  Steal Weapon it mid-fight (shutting off Drain) or claim it on his defeat.
```

## Proposed Composition (New Game++ Lionel Gate v1)

Keep the exact roster; Gaffgarion is the boss spike. Gaffgarion `103`; Knights `101`; Summoner
`101`; Archers `100`–`101`.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Gaffgarion (BOSS) | Dark Knight | `103` | Shadowblade/Drain via Ancient Sword; disarm him, then kill. Dies → rare drop. |
| n | Knight (Rend) | Knight | `101` | Gate-siege body; pressures the defense team. |
| n | Knight (Rend) | Knight | `101` | Second break-wall at the gate. |
| n | Knight | Knight | `101` | Third body; threatens the lever / defenders. |
| n | Archer | Archer | `101` | Ranged pressure on the gate defenders. |
| n | Archer | Archer | `100` | Second bow; covers the other approach to the gate. |
| n | Summoner | Summoner | `101` | Mid-tier AoE shelling the clustered gate-defense team. |

Reasoning:

The faithful move is to **make Gaffgarion the boss spike, keep the disarm-the-Ancient-Sword puzzle,
and let the Summoner punish the gate cluster**. Phase 1 isolates Ramza with a `103` self-healing
Dark Knight — trading blows loses, so the player must steal/break the Ancient Sword (which also
nets the rare). Meanwhile the gate-defense team weathers three Knights, two Archers, and a Summoner
whose AoE punishes clumping near the lever. Opening the gate reunites the party to finish him. Keep
the summons MID-TIER with intact charge times, and remember the no-resupply lead-in to Cúchulainn —
this fight should tax resources, not exhaust them. A clear boss step, still under Cúchulainn.

## Builds (final-shop quality; Order garrison + Dark Knight boss flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Gaffgarion — Dark Knight BOSS (Lv 103) — rare: Ancient Sword

```text
Job: Dark Knight (id TBD)   JobLevel: 8   Primary: Dark Sword / Shadowblade (Drain) — WEAPON-tied
Secondary: none extra (Drain is the threat)
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head/Body: shop heavy helm + heavy armor (ids TBD)
Accessory: Bracers (218)
Right hand: ANCIENT SWORD (id TBD) — his rare; the steal/break target AND the drop reward
Left hand: none / two-hand marker (254)
DIES here. Set the Ancient Sword as equipped weapon + rare steal/drop.
```

Role: the boss. Self-heals via Shadowblade until disarmed; the Ancient Sword is both the off-switch
and the prize.

### Knight x3 (Lv 101) — 2x Rend

```text
Job: Knight (id TBD)   JobLevel: 8   Secondary: Rend (break) on TWO of the three (id TBD)
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head/Body: shop heavy helm + heavy armor (ids TBD)
Accessory: Bracers (218)   Right hand: Runeblade (30) or Icebrand (29)   Left: shop shield (id TBD)
```

Role: the gate siege — bodies that pressure the defense team and the lever.

### Archer x2 (Lv 101 / 100)

```text
Job: Archer (77)   JobLevel: 8   Secondary: none
Reaction: Reflexes (449)   Support: Concentration (469)   Movement: Movement +1 (486)
Head: Thief's Cap (168)   Body: Black Garb (198)   Accessory: Bracers (218)
Right hand: Windslash Bow (87)   Left hand: none / two-hand marker (254)
```

Role: ranged punishment on the gate defenders.

### Summoner (Lv 101) — mid-tier summons

```text
Job: Summoner (id TBD)   JobLevel: 8   Secondary: none
Primary: Summon (mid-tier: Ifrit / Shiva / Ramuh / Titan — NOT best summons; reserved later)
Reaction: Reflexes (449)   Support: MA/Magick-boost (id TBD)   Movement: Movement +1 (486)
Head: cloth/mage hat (id TBD)   Body: shop robe (id TBD)
Accessory: Featherweave Cloak (234)   Right hand: shop magic-boost rod (id TBD)   Left: none (255)
```

Role: AoE that punishes a clumped gate defense; keep charge times intact so it can be raced/interrupted.

## Positioning Plan

```text
Phase 1: Gaffgarion starts inside the gate with Ramza split off to face him alone (or near-alone).
The 3 Knights + 2 Archers + Summoner start OUTSIDE the gate pressing the player's defense team and
  the lever.
The Summoner starts back with a sightline onto the defenders' likely cluster.
Preserve the LEVER + gate-open trigger that reunites the party.
Preserve Gaffgarion's boss/death scripting (he dies here; Ancient Sword drops/steals).
```

The gate should say: "Ramza, take the Dark Knight's sword or lose the duel — everyone else, hold
the line and pull the lever — and claim the Ancient Sword when he falls."

## Implementation Checklist

- [ ] Identify Lionel Gate `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify Gaffgarion + 3 Knight + 2 Archer + 1 Summoner + split deployment.
- [ ] Confirm Dark Knight / Knight / Summoner job IDs; keep Shadowblade tied to the Ancient Sword.
- [ ] Set the ANCIENT SWORD as Gaffgarion's equipped weapon AND rare steal/drop (mid-tier verify).
- [ ] Put Rend on TWO of the three Knights; shop-tier breakable gear only; summons MID-TIER.
- [ ] Set levels: Gaffgarion `103`; Knights + Summoner + one Archer `101`; second Archer `100`.
- [ ] Set JobLevel `8` on all active enemy slots.
- [ ] PRESERVE the two-phase structure: Ramza split, the LEVER, and Gaffgarion's death scripting.
- [ ] Patch via the correct layer; keep the diff inside the Lionel Gate window only.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify split + drop + death.
- [ ] Install mod, test from a New Game+ save; confirm disarm shuts off Drain and Ancient Sword drops.

## Test Questions

- Is Phase 1 a real solo puzzle — must Ramza disarm Gaffgarion rather than out-trade his Drain?
- Can the player Steal Weapon / Rend the Ancient Sword mid-fight, switching off Shadowblade?
- Does the gate-defense team face genuine pressure (3 Knights, 2 Archers, Summoner) at the lever?
- Does Gaffgarion DIE here and drop/yield the ANCIENT SWORD as the rare prize?
- Is the Ancient Sword clearly mid-tier (no Ch4-reserved best gear leaked early)?
- Does the no-resupply lead-in to Cúchulainn make resource discipline matter without being unfair?
- Is it a clear boss step above the Gallows but still below Cúchulainn (the chapter finale)?

## Sources

- Game8, "Lionel Castle Gate Walkthrough (Battle 20)": roster (Gaffgarion + 3 Knight, 2 Archer,
  1 Summoner), objective "Defeat all enemies!", recommended level ~23, deploy 5, two-phase split
  (Ramza vs Gaffgarion + gate defense + lever), disarm priority on his ANCIENT SWORD (Steal/Rend
  Weapon) to stop Shadowblade, no resupply before Cúchulainn.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553180
- Game8, "How to Beat Gaffgarion": Shadowblade/Drain and the disarm counter.
  https://game8.co/games/Final-Fantasy-Tactics/archives/556394
- Final Fantasy Wiki, "Lionel Castle" / "Ancient Sword": story/terrain + item tier context.
  https://finalfantasy.fandom.com/wiki/Lionel_Castle
- Local: `docs/battles/011-chapter-2-overview.md` (job-escalation + rare-boss-loot rules),
  `020-golgollada-gallows.md` (Gaffgarion sub-boss / disarm puzzle, retreat-no-loot), `016-balias-tor.md`
  (Summoner mid-tier rule), `014-zeirchele-falls.md` (Gaffgarion Dark Knight intro).
</content>
