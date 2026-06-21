# 050 - Eagrose Castle (Igros Castle)

Status: ✅ implemented (v1, entry 459) — see Rend-cap caveat
Chapter: 4 — "In the Name of Love"
Battle order: Battle 45 (after the Limberry chain)
Target version: Enhanced v1.5.0
ENTD: global entry **459** (local 75, entd4)
File: `battle_entd4_ent.bin`

## Implemented (v1, entry 459)

```text
IDENTIFICATION: entry 459 is the only one in the band with 5 generic Knights (job 76) = Phase-1 stair-
  wall. slot7 job 69 is a LUCAVI -> entry 470 (the multi-Lucavi battle) shows job 69 with name_id==job_id
  exactly like Velius(60)/Zalera(62), so job 69 = Adramelk. Roster:
    slot 0 = GUEST (tail 00 84), name 8, job 8, real gear -> story ally.
    slot 1 = Dycedarg (name 9, job 9; eq incl. Defender rh=33 + Aegis Shield lh=136) -> Phase-1 boss.
    slots 2-6 = 5 Knights (job 76; were near-naked, only a sword) -> the upper-stair wall.
    slot 7 = Adramelk (name 69, job 69, eq=255 Lucavi no-equip) -> Phase-2 transform spike.
    slots 8,9 = job 8, eq=0, lvl 254 -> scripting placeholders (left untouched).

CHANGE:
  Dycedarg = 104, head set to GRAND HELM (156) = the Tier-A steal/poach reward (he has equip slots;
    kept his Aegis Shield + Defender). 5 Knights = 103, armed (Heavy Helm/Armor + Bracers + shield,
    their sword kept) jl8. Adramelk = 105 (eq255, level only). Win-cond + 2-phase transform preserved.
  GUEST (slot 0): SPRITE COLLISION -> charId 8 also appears as enemy/placeholder clones at slots 8,9
    (job8==charId8), so the runtime GuestCharIds scaler can't be used (Rapha-Roof precedent, 433).
    Scaled by DIRECT ENTD level (103); gear + guest tail preserved. Program.cs NOT modified.

CAVEAT (Rend/Break <=2-source cap): Knight (job 76) has Arts of War as its primary command, which can't
  be removed via ENTD without changing the job (and losing the knight-wall identity). All 5 kept as
  Knights; the <=2-Rend cap is left as a SOFT/AI item to verify in-game (enemy Knight AI does not
  coordinate a 5-source break-lock, and the player has Safeguard/Steal answers). If testing shows a
  break-lock, a follow-up will re-job 3 of the 5 to a non-break bruiser or edit the ability layer.
Buried map treasure (Blood Sword, Healing Staff, Featherweave Cloak, Thief's Cap) left as-is.
```

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `037-chapter-4-overview.md`. Two-phase Lucavi fight (Velius precedent, `034`).

## Original Battle

Objective:

```text
Defeat Dycedarg, Ramza's elder brother!   (two-phase: Dycedarg → the Lucavi Adrammelech)
```

Player deployment:

```text
Up to 5 units, including Ramza. No guests.
```

Original enemy composition (verified via Game8, Battle 45):

```text
PHASE 1 — Dycedarg (Knight) + 5x Knight (Rend; on the upper stairs)
PHASE 2 — Dycedarg TRANSFORMS into ADRAMMELECH (Lucavi) after defeat:
            summons Bahamut / Leviathan (big AoE), inflicts Confuse, AoE devastates grouped units.
```

Public walkthrough details:

```text
Recommended level: ~60.  Difficulty: 4/5 stars.  Deploy up to 5.  Win: defeat Dycedarg/Adrammelech.
TERRAIN: Eagrose Castle keep — MULTI-LEVEL with STAIRS; the Knights hold the UPPER stairs (elevation).
PHASE 1: crack a Rend-Knight wall on the high ground — attack from BELOW with elevation-ignoring
  abilities (Holy Sword, height-ignoring magic).
PHASE 2: Dycedarg becomes ADRAMMELECH (Lucavi) — summon-AoE (Bahamut/Leviathan) that devastates
  GROUPED units, plus Confuse/Stone. Tips: Jade Armlet to nullify Stone, spread out, Holy Sword/magic
  that ignores height, heavy hitters (Orlandeau/Agrias/Meliadoul).
Rewards: 36,100 Gil; buried (Blood Sword, Featherweave Cloak, Healing Staff, Thief's Cap).
```

Design reading:

Eagrose is **the brother fight** — Ramza is forced to kill his eldest brother **Dycedarg**, who is
revealed as the Lucavi **Adrammelech**. Its identity is a **two-phase castle duel**: Phase 1 is a
**Rend-Knight wall on the stairs** (an elevation puzzle — strike from below with height-ignoring
damage), and Phase 2 is a **summon-AoE Lucavi** whose Bahamut/Leviathan blasts punish grouped units,
demanding **spacing** and %-damage/Holy answers. It mirrors the Riovanes Keep two-phase (`034`,
Wiegraf→Velius) but with a distinct shape: a stair-wall human phase into a *spread-or-die* demon
phase. The emotional beat — a sibling turned monster — is the chapter's penultimate Lucavi before the
march on Mullonde.

For New Game++ the identity must stay: **a two-phase brother duel — crack the Rend-Knight stair-wall
from below (height-ignoring damage), then survive and burst the summon-AoE Lucavi Adrammelech by
spreading out — with the Rend capped, the Lucavi's mass-AoE one telegraphed source, and a Tier-A
knight-lord drop on his death.**

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm slots: Dycedarg (boss) + 5 Knight (Phase 1), and the Adrammelech transform (Phase 2), + player
  slots.
Keep win = "Defeat Dycedarg" (his/Adrammelech's death ends it) + the MULTI-LEVEL STAIR geometry (the
  elevation wall IS Phase 1) + the 2-phase transform (Phase 2 Lucavi).
Keep Adrammelech's summon-AoE + Confuse identity BUT constrain it (below): ONE telegraphed mass source,
  spaceable, Confuse resistable/non-locking.
This is a 2-phase Lucavi fight: Dycedarg 104 (Phase 1), Adrammelech 105 (Phase 2 spike), Knights 103.
  ONE Tier-A rare on Dycedarg/Adrammelech.
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
Leave the buried map treasure (Blood Sword, Healing Staff, etc.) as-is — map loot.
```

Job IDs (carry over known, verify the rest in-game):

```text
Knight job id              (TBD - verify)
Dycedarg boss job id       (TBD - verify; Knight/lord form, Phase 1)
Adrammelech / Lucavi id    (TBD - verify; Phase 2 demon form)
```

## Job Escalation (Chapter 4 rule)

```text
CHANGE: NO new generic caste. The escalation is the 2-PHASE BOSS — Dycedarg (Knight-lord) → Adrammelech
  (summon-AoE Lucavi), the fourth Lucavi of the mod (Cúchulainn/Velius/Zalera precede). The 5-Knight
  Rend-wall on the stairs is the Phase-1 demand.
WHY: the fight's identity is already "crack the stair-wall, then spread vs the demon's AoE." The faithful
  Ch4 escalation is the two-phase human→Lucavi delivered at full power with a distinct shape (stair-wall
  → spread-or-die summons) — NOT a third bolted-on mechanic. The 2-phase brother duel IS the demand.
CONSTRAINTS (carry Velius 2-phase precedent 034 + the caps):
  - REND CAP: only 2 of the 5 Knights carry Rend (≤2-break-source cap) — the other 3 are plain bruisers.
    A 5-Rend wall would be a break-lock; forbidden.
  - LUCAVI MASS-AoE (Bahamut/Leviathan): ONE telegraphed, spaceable source; the answer is SPACING +
    %-damage/Holy (mirror Velius's Gravity answer). Not instant, no hard lock.
  - CONFUSE / STONE: resistable (Jade-Armlet-class gear) + non-locking; the boss mass-status cap.
WHAT IS NOT CHANGED: the stair geometry, the elevation puzzle, the transform, and the "defeat Dycedarg
  to win" shape remain.
```

## Sanctioned exceptions (carried precedents)

```text
KNIGHT REND / BREAK — capped to 2 of the 5 Knights (≤2-break-source cap, 028/033/044); telegraphed,
  Safeguard/Steal answers. NEVER a 5-source break-lock.
LUCAVI SUMMON-AoE (Adrammelech) — ONE telegraphed, spaceable mass source (Bahamut/Leviathan); answered
  by SPACING + %-damage/Holy; not instant, no hard lock (Velius precedent, 034).
LUCAVI STATUS (Confuse/Stone) — resistable (status/Stone-ward gear) + non-locking; boss mass-status cap.
TWO-PHASE TRANSFORM — the human→Lucavi spike, as Wiegraf→Velius (034). One transform, telegraphed.
```

## Boss rare loot

```text
DYCEDARG / ADRAMMELECH (boss, DIES here) drops/carries ONE Tier-A rare: GRAND HELM (the best non-Genji
  heavy helm).
WHY IT FITS: Dycedarg is the Beoulve warlord — the head of Ramza's knightly house; the finest heavy helm
  is his natural crown and a clear best-non-ultimate prize. It is unused so far and unmistakably Tier-A.
TIER: A (mid-Chapter-4 best non-ultimate). NOT Tier-S: the Genji set is Elmdor-themed (Genji Armor paid
  at 048); Ribbon / Robe of Lords / the Tier-S capstones stay on the endgame (47-53 / docs 052-058).
He DIES here (win = defeat Dycedarg), so the rare pays out — consistent with "retreat/flee = no drop."
The 5 Knights are generic (no boss loot). Buried map treasure (Blood Sword, etc.) stays as-is.
```

## Proposed Composition (New Game++ Eagrose Castle v1)

Keep the two-phase shape; Phase-1 stair-wall (Rend capped) into Phase-2 summon-AoE Lucavi. Dycedarg
`104`; Knights `103`; Adrammelech `105`.

### Phase 1 — Dycedarg + Knight stair-wall

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Dycedarg (BOSS) | Knight-lord | `104` | Holds the high ground; transforms on defeat; Grand Helm drop. |
| n | Knight | Knight | `103` | Upper-stair wall; Rend (break source 1). |
| n | Knight | Knight | `103` | Upper-stair wall; Rend (break source 2 — cap reached). |
| n | Knight | Knight | `103` | Upper-stair wall; NO Rend (plain bruiser). |
| n | Knight | Knight | `103` | Upper-stair wall; NO Rend. |
| n | Knight | Knight | `103` | Upper-stair wall; NO Rend. |

### Phase 2 — Adrammelech (Lucavi spike)

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Adrammelech (BOSS) | Lucavi | `105` | Summon-AoE (Bahamut/Leviathan) + Confuse; spread-or-die; the spike. |

Reasoning:

The faithful move is to **honor the two-phase brother duel with both caps in place**. Phase 1 is the
stair-wall elevation puzzle: Dycedarg (`104`) and five Knights (`103`) on the high ground, but Rend is
limited to two of them (no break-lock), so the player strikes from below with height-ignoring damage.
Phase 2 is the Lucavi spike: Adrammelech (`105`) with ONE telegraphed summon-AoE source that punishes
clumping — answered by spreading out and %-damage/Holy, with Confuse/Stone resistable. Killing the
boss (either phase's final blow) ends it and drops the Grand Helm (Tier-A). It echoes Velius (`034`)
but plays differently: wall-crack then spread-or-die.

## Builds (Chapter-4 boss quality; Beoulve-lord + demon flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Dycedarg (Lv 104) — BOSS Phase 1 (Knight-lord)

```text
Job: Knight-lord (id TBD)   JobLevel: 8   Primary: Rend/Mighty Sword + basic   Secondary: basic
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head: GRAND HELM (Tier-A, id TBD)   Body: Tier-A heavy armor (id TBD)   Accessory: Tier-A accessory (id TBD)
Right hand: Tier-A knight sword (id TBD)   Left: Tier-A shield (id TBD)
```

Role: the high-ground anchor; transforms on defeat. Drops Grand Helm.

### Knight x5 (Lv 103) — stair-wall (Rend on 2 only)

```text
Job: Knight (id TBD)   JobLevel: 8   Primary: basic + Rend (ONLY 2 of the 5 — cap)
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head: shop helm (id TBD)   Body: shop heavy armor (id TBD)   Accessory: Bracers (218)
Right hand: shop knight sword (id TBD)   Left: shop shield (id TBD)
```

Role: the elevation wall guarding the stairs; Rend on at most two (cap), never a break-lock.

### Adrammelech (Lv 105) — BOSS Phase 2 (Lucavi)

```text
Job: Adrammelech / Lucavi (id TBD)   JobLevel: 8   Primary: summon-AoE (Bahamut/Leviathan — ONE
  telegraphed, spaceable source) + Confuse/Stone (resistable, non-locking)   Secondary: demon melee
Reaction: (anti-burst) Counter Magic / MA-up (id TBD)   Support: MA-boost (id TBD)   Movement: float/+1
Innate Lucavi (no normal equip). Continues Dycedarg's loot (Grand Helm pays on final death).
```

Role: the spread-or-die spike — devastates grouped units; answered by spacing + %-damage/Holy. Keep
the mass-AoE one telegraphed source and status resistable; no hard lock.

## Positioning Plan

```text
PHASE 1: the Knights hold the UPPER STAIRS with Dycedarg behind them — the player approaches from BELOW,
  so the elevation is a wall best answered by height-ignoring damage (Holy Sword / magic). Keep the
  stair geometry; Rend on only 2 Knights.
PHASE 2: Adrammelech occupies the keep floor with summon-AoE sightlines — keep them telegraphed and
  spaceable so SPREADING OUT is the answer (punish clumping, not the careful player). Confuse/Stone
  resistable.
Bosses are the spikes (104 → 105); Knights at 103. Preserve the two-phase transform.
```

The keep should say: "your own blood holds the high stair, then wears a demon's shape — climb to him,
break his guard, and when the monster rises, scatter and burn it down."

## Implementation Checklist

- [ ] Identify Eagrose Castle `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify Dycedarg + 5 Knight (Phase 1) + the Adrammelech transform + player slots.
- [ ] Keep win = "Defeat Dycedarg"; keep the multi-level stair geometry + the 2-phase transform.
- [ ] Phase 1: Dycedarg `104`, Knights `103`; LIMIT Rend to 2 of the 5 Knights (cap).
- [ ] Phase 2: Adrammelech `105`; summon-AoE = ONE telegraphed, spaceable source; Confuse/Stone resistable, non-locking.
- [ ] Equip the drop: GRAND HELM (Tier-A) paid on the boss's final death.
- [ ] Set JobLevel `8` on boss/Knight slots.
- [ ] Patch via the correct layer; keep the diff inside the Eagrose window only.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify Rend cap + AoE cap + transform + drop.
- [ ] Install mod, test from a New Game+ save; confirm Phase-1 stair-wall is fair (Rend capped), Phase-2
      AoE is spaceable (spread-or-die, not unavoidable), Confuse resistable, and Grand Helm drops.

## Test Questions

- Is Phase 1 a fair elevation puzzle (crack the stair-wall from below; Rend capped to 2; no break-lock)?
- Is Phase 2's summon-AoE ONE telegraphed, spaceable source so SPREADING is the answer (no unavoidable wipe)?
- Are Confuse/Stone resistable + non-locking (boss mass-status cap)?
- Does killing the boss end it, and does the Grand Helm (Tier-A) drop on his final death?
- Are the bands right (Dycedarg 104, Knights 103, Adrammelech 105) — a 2-phase Lucavi, not an over-wall?
- Does it land the brother-fight beat and read as the Beoulve keep, echoing Velius (034) yet distinct?

## Sources

- Game8, "Eagrose Castle Walkthrough (Battle 45)": roster (Dycedarg boss + 5 Knight), two-phase
  (Dycedarg → Adrammelech Lucavi), "Defeat Dycedarg!", rec ~60, 4/5 stars, deploy 5, multi-level stair
  terrain, Phase-1 Rend wall on the high ground, Phase-2 Bahamut/Leviathan AoE + Confuse/Stone (Jade
  Armlet tip), rewards (36,100 Gil; buried Blood Sword, Healing Staff, Featherweave Cloak, Thief's Cap).
  https://game8.co/games/Final-Fantasy-Tactics/archives/553205
- Final Fantasy Wiki, "Dycedarg Beoulve" / "Adramelk": story/terrain context.
  https://finalfantasy.fandom.com/wiki/Dycedarg_Beoulve
- Local: `037-chapter-4-overview.md` (rules), `034-riovanes-castle-keep.md` (Wiegraf→Velius — the
  two-phase Lucavi precedent + Gravity/spacing answer), `049-limberry-undercroft.md` (Zalera Lucavi).
```
</content>
