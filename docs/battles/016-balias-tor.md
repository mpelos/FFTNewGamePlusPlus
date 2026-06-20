# 016 - Balias Tor (Bariaus Hill)

Status: designed (not yet implemented)
Chapter: 2 — "The Manipulator and the Subservient"
Battle order: Battle 15 (after Castled City of Zaland)
Target version: Enhanced v1.5.0
ENTD: global entry **TBD** — confirm on Windows game data
File: `battle_entd*_ent.bin` (TBD) / `OverrideEntryData` rows (TBD)

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `011-chapter-2-overview.md`.

## Original Battle

Objective:

```text
Defeat all enemies!
```

Player deployment:

```text
Up to 4 units, including Ramza. No guests.
```

Original enemy composition:

```text
2x Summoner
2x Knight
2x Archer
```

Public walkthrough details:

```text
Recommended level: ~16.
Hill terrain; the enemy is split into left / center / right groups.
The Summoners are the primary danger: take them out fast before they drop Ifrit (or another
  big summon) on your party. Their summons are slow to charge but hit a wide area hard.
The Knights threaten gear loss via Rend (equipment break) — Safeguard is valuable.
A Chemist is "indispensable" for sustained healing/revival.
```

Design reading:

Balias Tor is **the first Summoner fight** — the chapter's marquee new caster threat. Summoners
trade speed for reach: a charging summon (Ifrit/Shiva/Ramuh/Titan) is telegraphed but, when it
lands, blankets a group for heavy elemental damage. The fight teaches the player to **race the
charge** (rush or snipe the Summoners before they unleash), to **respect break-Knights**
(Safeguard), and to manage a **three-flank hill**. It is a tempo-and-priority puzzle: ignore the
Summoners and a single cast can wreck the party.

For New Game++ the identity must stay: **a three-flank hill where slow-but-devastating Summoners
must be raced down before they cast, while break-Knights and Archers screen them — priority and
tempo are the whole fight.**

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm slots: 2 Summoner + 2 Knight + 2 Archer, plus the player slots.
Confirm the left/center/right group positions on the hill.
Keep Summoner charge times intact (the race-the-cast counterplay depends on them NOT being instant).
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
```

Job IDs (carry over known, verify the rest in-game):

```text
77 = Archer            (confirmed)
Summoner job id        (TBD - verify; FIRST use of this job in the mod)
Knight job id          (TBD - verify)
```

## Job Escalation (Chapter 2 rule)

```text
THE NEW JOB IS BUILT IN: this battle canonically introduces the SUMMONER — the marquee new
caster of Chapter 2. The Summoner IS this fight's escalation; per the "one new wrinkle per
fight" rule, NO additional job swap is added. Keep the 2 Summoner / 2 Knight / 2 Archer shape.
WHY: the Summoner's slow-charge / big-AoE pattern is a genuinely new tactical problem (race the
  cast) that the player hasn't faced. Stacking another new job on top would muddy the lesson.
```

## Sanctioned exception — Knight Rend (break) stays

```text
Like Ziekden (009), the Knights here carry canonical Rend (equipment break) and the game
telegraphs Safeguard as the counter. It stays, constrained:
ALLOWED: Rend on the two Knights (the fight's secondary threat).
GUARDRAIL: only the two canonical Knights carry it; shop-tier breakable gear only; the player's
  Safeguard counter remains valid, so it is fair at NG+ scale.
```

## Boss rare loot

```text
None. No named boss/leader here — no rare item (per the Chapter 2 overview). Generics stay
shop-tier. (The Summoners' summon spells are the threat, not their loot.)
```

## Proposed Composition (New Game++ Balias Tor v1)

Keep the exact 2/2/2 shape; scale and gear it. The Summoners are the priority kills at `101`;
the break-Knights at `101`; the Archers at `100`–`101`.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Summoner (left) | Summoner | `101` | Slow-charge big AoE; the priority kill. Race the cast. |
| n | Summoner (right) | Summoner | `101` | Second summon threat on the far flank — splits the player's rush. |
| n | Knight (Rend) | Knight | `101` | Break-wall; screens a Summoner. Safeguard-telegraphed threat. |
| n | Knight (Rend) | Knight | `101` | Second break-wall; protects the other Summoner. |
| n | Archer | Archer | `101` | Ranged support; punishes the rush toward the Summoners. |
| n | Archer | Archer | `100` | Second bow; covers the center/hill. |

Reasoning:

The faithful move is to **scale and lean into the Summoners**. Two summon-casters on opposite
flanks force the player to choose a side and race a charge while the other Summoner winds up —
exactly the original's tension, now lethal at party level. The break-Knights screen them
(making the rush costly) and keep the Safeguard lesson; the Archers punish the approach. Keep
the summons MID-TIER (Ifrit/Shiva/Ramuh/Titan), not the best summons (those are later), and keep
their charge times so the race-the-cast counter is real.

## Builds (final-shop quality; hill garrison + summoner flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Summoner x2 (Lv 101) — NEW job (the fight's identity)

```text
Job: Summoner (id TBD)   JobLevel: 8   Secondary: none
Primary: Summon (mid-tier: Ifrit / Shiva / Ramuh / Titan — NOT the best summons, reserved later)
Reaction: Reflexes (449) or magic-defensive reaction (id TBD)
Support: MA/Magick-boost support if available (id TBD)
Movement: Movement +1 (486)
Head: cloth/mage hat (id TBD)   Body: shop robe (id TBD)
Accessory: Featherweave Cloak (234) or magic-defensive accessory (id TBD)
Right hand: shop magic-boost rod/staff (id TBD)   Left hand: none (255)
```

Role: the priority threat. Slow charge, wide AoE — must be raced down. Keep charge times so the
player can interrupt by closing/sniping; do NOT make summons instant or the lesson dies.

### Knight x2 (Lv 101) — Rend (break)

```text
Job: Knight (id TBD)   JobLevel: 8   Secondary: the Knight break command (Rend, id TBD)
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head/Body: shop heavy helm + heavy armor (ids TBD)
Accessory: Bracers (218)   Right hand: Runeblade (30) or Icebrand (29)   Left: shop shield (id TBD)
```

Role: the screen in front of the Summoners. Rend punishes a careless rush; bring Safeguard.

### Archer x2 (Lv 101 / 100)

```text
Job: Archer (77)   JobLevel: 8   Secondary: none
Reaction: Reflexes (449)   Support: Concentration (469)   Movement: Movement +1 (486)
Head: Thief's Cap (168)   Body: Black Garb (198)   Accessory: Bracers (218)
Right hand: Windslash Bow (87)   Left hand: none / two-hand marker (254)
```

Role: ranged support that punishes the player's dash toward the Summoners.

## Positioning Plan

```text
Summoners start on the left and right flanks of the hill, behind their Knight screens, with
  sightlines over the center where the player must cross.
The two Rend-Knights start in front of / beside their Summoners, between the player and the casters.
The Archers start center / on the hill's high ground, covering the approach lanes to both flanks.
This recreates the original's left/center/right split: the player must pick a flank, race a
  summon, and eat fire from the rest.
```

The hill should force a choice: commit to one Summoner and race its charge while the other winds
up and the center harasses — the original's priority-and-tempo puzzle, at scale.

## Implementation Checklist

- [ ] Identify Balias Tor `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify 2 Summoner + 2 Knight + 2 Archer + player slots.
- [ ] Confirm Summoner job id + a MID-TIER summon list (no best summons) and intact charge times.
- [ ] Confirm Knight Rend command id; keep break on both Knights, shop-tier breakable gear.
- [ ] Set levels: both Summoners + both Knights + one Archer `101`; second Archer `100`.
- [ ] Set JobLevel `8` on all active enemy slots.
- [ ] Preserve the left/center/right hill positions (Summoners flanked, screened by Knights).
- [ ] Patch via the correct layer; keep the diff inside the Balias Tor window only.
- [ ] Re-dump and diff; confirm changes are small and intentional.
- [ ] Install mod, test from a New Game+ save; verify summons are scary but race-able.

## Test Questions

- Are the Summoners the clear priority — does ignoring them risk a party-wrecking summon?
- Can the player still RACE the cast (charge times intact), or do summons land too fast?
- Do the Rend-Knights make the rush costly while Safeguard keeps it fair?
- Does the three-flank hill force a real "pick a side" decision?
- Are the summons mid-tier (no best-summon power crept in early)?
- Is it harder than Zaland (a true caster threat) but below the Gaffgarion/Cúchulainn bosses?
- Does it still read as a hill ambush by a summoner cell, not a designed arena?

## Sources

- Game8, "Balias Tor Walkthrough (Battle 15)": roster (2 Summoner, 2 Knight, 2 Archer),
  objective "Defeat all enemies!", deploy 4, recommended level ~16, left/center/right hill
  groups, Summoners as the primary threat (race the summon), Knights' Rend / Safeguard counter,
  Chemist indispensable.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553176
- Final Fantasy Wiki, "Bariaus Hill": story/terrain context.
  https://finalfantasy.fandom.com/wiki/Bariaus_Hill
- Local: `docs/battles/011-chapter-2-overview.md` (job-escalation rule), `009-ziekden-fortress.md`
  (the Rend/break exception precedent), `004-dorter-slums.md` (Black Mage/Archer builds).
</content>
