# 031 - Walled City of Yardrow (Yardow)

Status: ✅ implemented (v1, entry 428) — NG+ only; pending playtest. **v2 redesign documented only** (implementation pending).
Chapter: 3 — "The Valiant"
Battle order: Battle 28 (after Grogh Heights)
Target version: Enhanced v1.5.0
ENTD: global entry **428** (local entry 44, `battle_entd4_ent.bin`)
File: `battle_entd4_ent.bin` (embedded NG+ swap) — `tools/battle_patch.py yardrow`
+ `Program.cs` GuestCharIds += `0x19` (Rapha runtime level-scaling)

Implemented composition (entry 428, vanilla-dump verified):
- s0 **Rapha** (job 25 Skyseer — PROTECTED GUEST, control bytes `00 84` like Alma/Orran; lose-on-death):
  runtime level-scaled (charId 0x19 added to GuestCharIds). 2026-06-27: also re-equipped to best buyable
  end-game gear in her ENTD slot — **Thief's Cap 168** (HP +100) / **Luminous Robe 206** (HP +75, MP +50) /
  **Featherweave Cloak 234** (40/30 evasion) / **Eight-fluted Pole 113**; identical kit at Riovanes Roof 433.
- s1 **Marach** (job 26 Netherseer — enemy BOSS, survives/recruitable): L103 + durability gear
  (Mage Hat/shop Robe/Bracers — he was naked); job/jobLevel(unchanged, no hard-lock unlock)/secondary/
  weapon/survive scripting preserved. NO rare (survives).
- s2,s4,s6 **Ninja** L102/L101/L101 (NEW caste) — dual-wield (two Ninja Longblades 14, innate Two
  Swords); Thief's Cap/Black Garb/Germinas; First Strike/Atk Boost/Mv+2 (wall-climb vantage + Throw innate).
- s3,s5 Summoner L101 — Mage Hat/shop Robe/Featherweave/shop Rod; Reflexes/Atk Boost/Mv+1.

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `024-chapter-3-overview.md`.

## Original Battle

Objective:

```text
Save Rapha!  (Rapha is a protected NPC — if she dies, the battle is lost.)
```

Player deployment:

```text
Up to 5 units, including Ramza. Protected NPC: RAPHA (her brother Marach is forced to fight; she
  must survive). For NG+, Rapha must be player-controlled even though the lose-on-death objective
  remains.
```

Original enemy composition:

```text
1x Marach    (named BOSS — Rapha's brother; survives the fight, recruitable later)
3x Ninja     (dual-wield, high Move/Jump, WALL-CLIMB, Throw — the new caste)
2x Summoner  (AoE pressure)
Terrain: a massive WALL with a single central PATH (chokepoint); some enemies CLIMB the wall for
  ranged vantage onto the field (and onto Rapha).
```

Public walkthrough details:

```text
Recommended level: ~32.  Difficulty: 3/5 stars.
The Ninjas are fast, dual-wield, and CLIMB THE WALL to gain ranged vantage (Throw) — they slip past
  body-blocks and threaten Rapha directly.
A single central path is a CHOKEPOINT; the Summoners shell the approach with AoE.
Mustadio's Leg Shot (Immobilize) is recommended to PIN the wall-climbing Ninjas.
Lose if Rapha dies.
```

Design reading:

Yardow is **the Ninja debut and a protect-the-guest-from-fast-assassins puzzle**. The Ninja is the
chapter's marquee new caste: fast, dual-wielding, **wall-climbing**, with **Throw** for ranged
damage — so unlike the slow Knights or grounded Dragoons, Ninjas **ignore your front line**, scale
the wall, and rain shuriken on the protected Rapha from vantage. Layered on a **single-path
chokepoint** with **Summoner AoE** and Rapha's brother Marach as the boss, the fight asks the player
to **protect a fragile controlled guest against threats that won't be body-blocked** — move Rapha
intelligently, pin assassins (Leg Shot/ranged disable), screen the chokepoint, and burst the Ninjas
before they whittle her down. It teaches dealing with high-mobility vertical assassins, the recurring
lesson of Chapter 3's elite roster, without making guest AI a skill check.

For New Game++ the identity must stay: **a single-path wall defense of a fragile controlled guest
against fast, wall-climbing, Throw-wielding Ninjas plus Summoner AoE — won by moving Rapha, then
pinning/intercepting assassins that ignore your front line, not by holding a simple wall.**

## Local Data Confirmed

```text
ENTD entry 428 confirmed in `024-chapter-3-overview.md` and v1 implementation.
Roster: Marach + 3 Ninja + 2 Summoner, plus the player slots and RAPHA's protected guest slot.
Rapha is control bytes `00 84` like Orran/Alma; v1 runtime scaling already added charId `0x19`.
For v2, apply/verify player control for Rapha in NG+ while preserving lose-on-death scripting.
DO NOT touch Marach's survive/retreat scripting (he is recruitable later — he must NOT die here).
Keep the wall + single central path geometry AND the Ninja wall-climb capability (the fight's core).
Keep Summoner charge times intact (race-the-cast counter).
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
```

Job IDs (carry over known, verify the rest in-game):

```text
25 = Rapha Skyseer guest (confirmed in v1 implementation)
26 = Marach Netherseer enemy boss (confirmed in v1 implementation)
82 = Summoner (confirmed from Balias Tor 016)
Ninja job id = TBD (v1 slots confirmed as Ninja; verify exact id before implementation)
```

## Enemy Party Escalation (Chapter 3 redesign)

```text
VANILLA SPIRIT: save Rapha from a wall-climbing assassin squad while Marach and Summoners pressure
  the central path.
CHAPTER-3 UPGRADE: keep the exact 3 Ninja / 2 Summoner / Marach roster, but complete every active
  human setup with secondary/reaction/support/movement. Rapha must be player-controlled in NG+.
WHY: the Ninja debut is the whole escalation. Three fast, vertical, front-line-ignoring assassins
  are enough; adding a fourth Ninja, Time Mage tempo, or instant summons turns the protect objective
  into a failure lottery instead of a readable skill check.
WHAT IS NOT CHANGED: the answer remains pin/intercept the Ninjas, manage Summoner AoE at the
  chokepoint, move Rapha intelligently, and force Marach's survival/retreat state without killing him.
```

Chapter 3 requirements applied:

```text
- Every active human enemy has full equipment.
- Every active human enemy has secondary, reaction, support, and movement.
- The party has real synergy: wall-climbing Ninjas pressure Rapha, Summoners punish chokepoint
  clumps, and Marach adds named boss pressure.
- Rapha is scaled, geared, and player-controlled in NG+.
- No extra Ninja, no Time Mage tempo, no instant summons, no hard-lock Marach.
```

## Sanctioned exceptions (carried precedents)

```text
NINJA Throw — allowed: Throw is RANGED PHYSICAL DAMAGE, not a status lock — a fair, telegraphed
  threat (the player can disable/intercept). Keep it damage-only; do NOT pair it with hard status.
SUMMONER — allowed (Balias Tor 016): MID-TIER summons, charge times intact; shells the chokepoint.
PROTECT-NPC — Rapha's lose-on-death is preserved (Balias Swale 019 / Gollund 025 handling); the
  challenge is keeping a fragile controlled guest alive vs. mobility, not hoping guest AI behaves.
NO hard lock anywhere; Marach's boss skills constrained to damage/soft-status (no Stop/Don't Act).
```

## Boss rare loot

```text
None. Marach is a named boss but SURVIVES (he is recruitable later — he does not die here), so there
is nothing to drop (retreating/surviving boss = no rare, per Gallows 020 / Zalmo 026). Generics stay
shop-tier. The map's rare TREASURE (Yagyu Darkrood / Flail of Flame / Slasher / Hunting Crossbow /
Mythril Gun) is existing map treasure, not boss loot; leave it as-is.
```

## Guest handling

```text
Rapha is an active protected guest and must be player-controlled in NG+. Preserve the Save Rapha
lose-on-death objective, her scaling, and her re-equipped guest kit, but do not let her AI decide
the fight. The challenge should come from Ninja wall-climb/Throw pressure and Summoner AoE, while
the player chooses where Rapha moves, waits, defends, and casts.
```


Fixed encounter Brave/Faith targets:

| Unit | Br/Fa | Rationale |
|------|-------|-----------|
| Rapha | `65/75` | Controlled protected guest; Faith supports Skyseer identity, Brave stays moderate to keep protection relevant. |

## Proposed Composition (New Game++ Yardow v2)

Keep the exact roster; the Ninjas are the headline. One Ninja anchors at `102`; Marach at `103`;
Summoners `101`; other Ninjas `101`.

| Slot | Role | Job | Level | Br/Fa | Purpose |
| ------ | ------ | ----- | ------- | --- | --------- |
| n | Marach (BOSS) | Netherseer/Heaven-line | `103` | `78/72` | Boss pressure; survives (recruitable later). Damage/soft-status only. |
| n | Ninja (lead, NEW caste) | Ninja | `102` | `86/40` | Wall-climbs to vantage; Throws at Rapha; ignores the front line. |
| n | Ninja | Ninja | `101` | `90/60` | Second assassin; rushes the chokepoint or scales the wall. |
| n | Ninja | Ninja | `101` | `90/60` | Third assassin; splits the player's protection of Rapha. |
| n | Summoner | Summoner | `101` | `58/78` | Mid-tier AoE shelling the central path. |
| n | Summoner | Summoner | `101` | `58/78` | Second summon threat; punishes clumping at the chokepoint. |

Reasoning:

The faithful move is to **make the wall-climbing Ninjas the core threat to Rapha and keep the
chokepoint + Summoner pressure**. Three fast, dual-wielding Ninjas that scale the wall and Throw mean
the player cannot simply hold the central path — the assassins go over the top and snipe Rapha, so
the player must move her, pin them (Leg Shot/ranged disable), intercept on the wall, and burst them
down while screening the chokepoint against Summoner AoE. Marach adds boss pressure but survives
(no kill, no drop). A clear 3/5★ step that showcases the Ninja's mobility, harder than Grogh Heights,
below the Riovanes finale.

## Builds (final-shop quality; Yardow assassin cell flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Ninja x3 (Lv 102 / 101 / 101) — NEW caste

```text
Job: Ninja (id TBD)   JobLevel: 8   Primary: Throw (ranged) + dual-wield melee
Secondary: Item or Fundaments equivalent; no status package
Reaction: First Strike (453) or Vanish/Reflexes (449)
Support: Attack Boost (465) if dual-wield is innate; otherwise Dual Wield (id TBD)
Movement: Movement +2 (487) or +3 / Ignore Height (id TBD — enables the wall-climb vantage)
Head: Thief's Cap (168)   Body: Black Garb (198)   Accessory: Germinas Boots (210)
Right/Left hand: shop ninja blades / knives (ids TBD; not a reserved best — Yagyu Darkrood stays map treasure)
```

Role: the headline — fast, wall-climbing, Throw-wielding assassins that ignore the front line and
threaten Rapha from vantage.

### Summoner x2 (Lv 101) — mid-tier summons

```text
Job: Summoner (82)   JobLevel: 8
Secondary: Item or low-tier White Magic if legal; no Time Magic / no hard control
Primary: Summon (mid-tier: Ifrit / Shiva / Ramuh / Titan — NOT best summons; reserved later)
Reaction: Reflexes (449)   Support: MA/Magick-boost (id TBD)   Movement: Movement +1 (486)
Head: cloth/mage hat (id TBD)   Body: shop robe (id TBD)
Accessory: Featherweave Cloak (234)   Right hand: shop magic-boost rod (id TBD)   Left: none (255)
```

Role: AoE shelling the central path; punishes a clumped chokepoint hold.

### Marach — BOSS (Lv 103) — survives, no drop

```text
Job: Netherseer / Heaven-Knight line (26)   JobLevel: 8   Primary: his canonical skillset
Secondary: Item / basic support equivalent; no second status/control engine
Skillset limit: damage / soft-status ONLY — NO hard lock (no Stop/Don't Act/Immobilize spam).
Reaction: a defensive reaction (id TBD)   Support: Attack Boost (465) or MA-boost (id TBD)
Movement: Movement +1 (486)
Head/Body: shop gear his job allows (ids TBD)   Accessory: Bracers (218)
Right hand: shop-tier weapon (id TBD; NOT a rare — he survives, nothing drops)
SURVIVES — do NOT let him die here (recruitable later); no rare loot at Yardow.
```

Role: boss pressure that adds to the assault on Rapha; survives the battle.

## Positioning Plan

```text
Rapha starts forward/exposed (story placement), so the "protect her" pressure is real; in NG+ the
  player controls her, but she should still need immediate movement/defense.
The Ninjas start positioned to RUSH the central path OR climb the wall and Throw at her from vantage.
The 2 Summoners start back with sightlines onto the central path; Marach anchors with the band.
Preserve the WALL + single central path AND the Ninja wall-climb capability (the core puzzle).
Do NOT alter Rapha's protected-NPC lose condition or Marach's survive scripting.
```

The city should say: "your front line means nothing to them — they go over the wall and put knives
in the girl you're protecting; pin them, chase them up, and kill them before she falls."

## Simulation Plan and Results

Simulation artifact:

```text
tmp/fft-level-design-031-walled-city-yardrow/
```

Model scope:

```text
First four rounds only; compares Ninja wall pressure, Summoner chokepoint pressure, Rapha risk,
pin/intercept access, and the effect of making Rapha player-controlled in NG+.
```

Iteration results:

| Candidate | Enemies | Action ratio | Ninja threat | Summon threat | Total pressure | Rapha risk | Pin/intercept | Answerability | Result |
|-----------|---------|--------------|--------------|---------------|----------------|------------|---------------|---------------|--------|
| v1 AI-Rapha Ninja debut | 6 | 0.94 | 82.1 | 29.9 | 152.5 | 38.7 | 54.8 | 47.5 | Rejected: Rapha AI skill check |
| v2 controlled-Rapha Ninja cell | 6 | 1.00 | 88.6 | 31.7 | 173.6 | 28.6 | 64.8 | 66.2 | Accepted |
| Fourth Ninja wall rush | 7 | 1.15 | 118.1 | 31.7 | 204.5 | 37.4 | 60.4 | 57.9 | Rejected: extra Ninja body |
| Time-Hasted Ninja tempo | 7 | 1.15 | 95.0 | 31.7 | 196.1 | 41.7 | 47.8 | 54.9 | Rejected: tempo muddies debut |
| Instant Summoner chokepoint | 6 | 1.00 | 88.6 | 50.6 | 193.9 | 41.5 | 51.8 | 56.1 | Rejected: summon counterplay removed |
| Hard-lock Marach support | 6 | 1.00 | 88.6 | 31.7 | 208.6 | 38.4 | 64.8 | 36.0 | Rejected: hard-lock |

Decision:

```text
Use the complete six-enemy Ninja cell and make Rapha player-controlled. Three Ninjas plus two
raceable Summoners are enough to create the wall-climb protection puzzle. Reject guest AI, a fourth
Ninja, Time Mage tempo, instant summons, and hard-lock Marach because they turn the protect objective
into a failure lottery instead of a skill check.
```

## Current Implementation (v1, entry 428 — superseded by v2 design)

The shipped v1 already establishes Rapha scaling/gear, Marach, three Ninjas, two Summoners, and the
wall-climb Ninja debut on entry 428. The v2 redesign above is **documentation only** in this pass;
it requires a later implementation pass to apply/verify Rapha player control and complete secondary
setups for every active enemy.

## Future Implementation Checklist (v2)

- [x] Identify Yardow ENTD entry 428; fill "Local Data Confirmed".
- [x] Dump original entry; verify Marach + 3 Ninja + 2 Summoner + player + Rapha NPC slots.
- [ ] Apply/verify Rapha player control in NG+ while preserving her lose-on-death protected objective.
- [ ] Confirm Ninja / Summoner / Marach job ids; keep Ninja Throw (damage-only) + wall-climb mobility.
- [ ] Constrain Marach to damage/soft-status (no hard lock); summons MID-TIER, charge intact.
- [ ] Set levels: Marach `103`; lead Ninja `102`; other Ninjas + both Summoners `101`.
- [ ] Set JobLevel `8` on all active enemy slots.
- [ ] Give every active human enemy full equipment plus secondary/reaction/support/movement.
- [ ] PRESERVE Rapha's lose-on-death scripting AND Marach's survive scripting (no death/no drop).
- [ ] Preserve the wall + central chokepoint + Ninja wall-climb; no fourth Ninja and no Time Mage.
- [ ] Patch via the correct layer in a later implementation pass; no binary/data change in this doc pass.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify Rapha + Marach + wall-climb.
- [ ] Install mod, test from a New Game+ save; confirm the Ninjas threaten Rapha and are pin-able.

## Test Questions

- Do the wall-climbing Ninjas genuinely bypass the front line and threaten Rapha from vantage?
- With Rapha player-controlled, is protecting her tense because of Ninja pressure, not guest AI?
- Is pinning/intercepting them (Leg Shot, ranged disable, chasing up the wall) the clear answer?
- Does the single central path make chokepoint control matter against the Summoner AoE?
- Is keeping the fragile Rapha alive tense but achievable with active protection?
- Does Marach survive (no kill, no drop), consistent with him being recruitable later?
- Does the Ninja read as a distinct new caste (fast, vertical, Throw) vs Dragoon/Thief?
- Is it a 3/5★ step above Grogh Heights but below the Riovanes finale?

## Sources

- Game8, "Walled City of Yardrow Walkthrough (Battle 28)": roster (Marach + 3 Ninja, 2 Summoner),
  objective "Save Rapha!" (lose if Rapha dies), recommended level ~32, 3/5 stars, deploy 5, wall
  with a single central chokepoint, wall-climbing enemies, Leg Shot to pin Ninjas, rewards/treasure.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553189
- Final Fantasy Wiki, "Marach Galthena" / "Yardow Fort City": story/terrain context.
  https://finalfantasy.fandom.com/wiki/Marach_Galthena
- Local: `docs/battles/024-chapter-3-overview.md` (Chapter 3 complete-party + rare-loot rules),
  `019-balias-swale.md` & `025-mining-town-gollund.md` (controlled protect-VIP handling), `016-balias-tor.md`
  (Summoner mid-tier), `020-golgollada-gallows.md` (surviving boss → no drop).
