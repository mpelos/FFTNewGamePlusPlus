# 025 - Mining Town of Gollund (Goland Coal City)

Status: designed (not yet implemented)
Chapter: 3 — "The Valiant"
Battle order: Battle 22 (Chapter 3 opener)
Target version: Enhanced v1.5.0
ENTD: global entry **TBD** — confirm on Windows game data
File: `battle_entd*_ent.bin` (TBD) / `OverrideEntryData` rows (TBD)

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `024-chapter-3-overview.md`.

## Original Battle

Objective:

```text
Save Orran!  (Orran is a protected guest — if he dies, the battle is lost. He also HELPS:
  he casts Celestial Stasis, mass-inflicting Stop / Disable / Immobilize on the enemy.)
```

Player deployment:

```text
Up to 5 units, including Ramza. Guest: ORRAN (astrologer) — fights on his own, casts Celestial
  Stasis (mass Stop/Disable/Immobilize on FOES), and MUST be kept alive.
Mounted units (Chocobo) help reach the rooftops on turn 1.
```

Original enemy composition:

```text
2x Chemist   (support — items, heal/revive the band)
3x Thief     (charm — Steal Heart; also steal gear; fast, reach Orran)
1x Orator    (Mediator — status/charm utility; the chapter's new caste)
```

Public walkthrough details:

```text
Recommended level: ~25.  Difficulty: 2/5 stars.
Rooftop town; mounted units reach the high ground turn 1.
The Thieves frequently use STEAL HEART (charms opposite-gender units) and can steal gear; they
  rush to whittle Orran and your line.
The Chemists keep the band topped up (heal/revive) — a sustain problem if ignored.
The Orator adds status/charm pressure.
Orran's Celestial Stasis can freeze clusters of enemies, opening windows to pick them off.
```

Design reading:

Gollund is **the protect-the-support-VIP fight where the threat is denial, not damage**. Orran is
both the objective and a powerful ally — his Celestial Stasis can lock down the enemy — so the
enemy band is built to **rush and disable**: fast charm-Thieves who turn your own units against
you (and against Orran) and steal your gear, Chemists who out-sustain a slow kill, and an Orator
who piles on status/charm. The lesson is **anti-charm discipline + tempo**: protect Orran, don't
let charm flip your front line onto him, burst the squishy thieves/casters before their sustain
and steals grind you down, and exploit Orran's freezes. It's a fitting Chapter 3 opener — lower
raw lethality, high "lose-your-tools" pressure.

For New Game++ the identity must stay: **a rooftop scramble to keep a fragile, helpful guest alive
against a fast charm-and-steal band with healer sustain — win by spacing against charm and racing
the casters, not by trading blows.**

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm slots: 2 Chemist + 3 Thief + 1 Orator, plus the player slots and ORRAN's guest slot.
DO NOT touch Orran's guest scripting (Celestial Stasis + the "Save Orran" fail-on-death objective).
Keep the rooftop elevation and mounted-mobility option intact.
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
```

Job IDs (carry over known, verify the rest in-game):

```text
75 = Chemist           (confirmed)
83 = Thief             (confirmed)
Orator/Mediator job id (TBD - verify; FIRST enemy use of this caste in the mod)
```

## Job Escalation (Chapter 3 rule)

```text
THE NEW CASTE IS BUILT IN: this battle debuts the enemy ORATOR (Mediator) — a status/charm utility
caste not seen earlier in the mod. The Orator (alongside the charm-Thieves) IS this fight's
escalation; per "one new wrinkle per fight," NO additional generic job is swapped in. Keep the
2 Chemist / 3 Thief / 1 Orator shape.
WHY: a charm-and-steal denial band attacking a fragile guest is already a dense new puzzle (your
  own units can be turned onto Orran). Adding a Ninja or Dragoon here would muddy it — those castes
  debut in their own fights (Vaults 027 / Yardow 031).
```

## Sanctioned exceptions (carried + new precedent)

```text
CHARM (Steal Heart / Entice) — allowed, constrained (Ch2 Merchant Dorter 012 / Goug 018 precedent,
  now extended to the Orator):
  ALLOWED: Steal Heart on the Thieves + the Orator's charm/Entice.
  GUARDRAILS: charm only — NO hard lock (no Stop/Don't Act/Immobilize from the ENEMY side; the only
    mass-disable on the field is ORRAN's, working FOR the player). The player's anti-charm counter
    stays valid (charm-immune accessory, all-male/all-female sub-team, or fast bursts). Do not stack
    a second charm source beyond the one Orator + the canonical Thieves.
THEFT (Steal gear) — allowed on the Thieves: a real threat that rewards equipping non-stealable or
  expendable gear; it is counterable and not run-ending. Keep it to the canonical Thieves.
```

## Boss rare loot

```text
None. No named boss here — no rare boss item (per the Chapter 3 overview). Generics stay shop-tier.
(The map's rare TREASURE pickups — Mage's Staff / Spear / Iron Flail / Close Helmet — are existing
map treasure, not boss loot; leave them as-is.)
```

## Proposed Composition (New Game++ Gollund v1)

Keep the exact roster; this is a low-lethality, high-denial opener. The Orator anchors at `102`;
Thieves `100`–`101`; Chemists `101`.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Orator (anchor, NEW caste) | Orator | `102` | Status/charm utility; the new wrinkle. Pressures Orran + your line. |
| n | Thief (charm) | Thief | `101` | Fast; Steal Heart + steal gear; rushes Orran. |
| n | Thief (charm) | Thief | `101` | Second charm/steal threat on the other roof lane. |
| n | Thief | Thief | `100` | Third fast body; flanks toward Orran. |
| n | Chemist | Chemist | `101` | Heal/revive sustain — punishes a slow kill. |
| n | Chemist | Chemist | `101` | Second medic; keeps the band standing. |

Reasoning:

The faithful move is to **keep raw damage low and lean into denial + sustain**. Three fast Thieves
with Steal Heart threaten to flip your units onto Orran and strip your gear; two Chemists make
ignoring the band a losing attrition game; the Orator piles charm/status. The player must protect
Orran (use his Celestial Stasis windows), space against charm, and race the casters/thieves down.
No enemy hard-lock — the only mass-disable belongs to Orran, keeping the fight a fair tempo puzzle
rather than a lockdown. A deliberately gentle Chapter 3 opener (2/5★) before the Vaults escalate.

## Builds (final-shop quality; coal-town brigand flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Orator (Lv 102) — NEW caste (anchor)

```text
Job: Orator/Mediator (id TBD)   JobLevel: 8   Primary: Speechcraft (charm/Entice + status talk)
Skillset limit: charm/Entice + soft status ONLY — NO Stop/Don't Act/Immobilize (those stay Orran's).
Reaction: First Strike (453) or a defensive reaction (id TBD)
Support: Attack Boost (465)   Movement: Movement +1 (486)
Head: shop hat (id TBD)   Body: shop light armor/robe the job allows (id TBD)
Accessory: Germinas Boots (210)   Right hand: shop gun/rod the job allows (id TBD)   Left: none
```

Role: the new caste — charm/status utility that pressures Orran and your line without hard-locking.

### Thief x3 (Lv 101 / 101 / 100) — charm + steal

```text
Job: Thief (83)   JobLevel: 8   Secondary: Steal (incl. Steal Heart)
Reaction: First Strike (453)   Support: Attack Boost (465)   Movement: Movement +2 (487)
Head: Thief's Cap (168)   Body: Black Garb (198)   Accessory: Germinas Boots (210)
Right hand: Air Knife (9)   Left hand: none / two-hand marker (254)
```

Role: fast charm/steal harassers that rush Orran and strip your gear.

### Chemist x2 (Lv 101) — sustain

```text
Job: Chemist (75)   JobLevel: 8   Primary: Item (Potions/Hi-Potion/Phoenix Down/Antidote)
Reaction: Auto-Potion (441)   Support: Throw Items (474)   Movement: Movement +1 (486)
Head: shop hat (id TBD)   Body: shop clothes (id TBD)   Accessory: Bracers (218)
Right hand: shop gun/knife the job allows (id TBD)   Left: none
```

Role: the sustain spine — heal/revive that punishes a slow, unfocused kill.

## Positioning Plan

```text
Orran starts forward/exposed (story placement) so the "protect him" pressure is real; the enemy
  Thieves start positioned to RUSH him across the rooftops.
The two Chemists start back, supporting the band; the Orator starts mid, with charm range on the
  player's likely cluster and on Orran.
Preserve the rooftop elevation and the turn-1 mounted-mobility path so the player can contest the
  high ground and intercept the rush to Orran.
Do NOT alter Orran's guest start or his Celestial Stasis scripting.
```

The town should say: "keep the astrologer alive — they're not here to out-fight you, they're here
to charm your hands, rob you blind, and out-heal you; protect him and pick them off in his freezes."

## Implementation Checklist

- [ ] Identify Gollund `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify 2 Chemist + 3 Thief + 1 Orator + player + Orran guest slots.
- [ ] Confirm Orator/Mediator job id + a charm/soft-status-only skillset (no hard lock).
- [ ] Keep Steal Heart + Steal on the Thieves; constrain the Orator to charm/soft status.
- [ ] Set levels: Orator `102`; two Thieves + both Chemists `101`; third Thief `100`.
- [ ] Set JobLevel `8` on all active enemy slots.
- [ ] Do NOT touch Orran's guest scripting (Celestial Stasis + Save-Orran fail-on-death).
- [ ] Preserve rooftop elevation + mounted-mobility path.
- [ ] Patch via the correct layer; keep the diff inside the Gollund window only.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify Orran + objective intact.
- [ ] Install mod, test from a New Game+ save; confirm Orran survives a careful run and charm is fair.

## Test Questions

- Is keeping Orran alive a real but achievable task against the rushing charm-Thieves?
- Is charm a fair, counterable threat (spacing / charm-immune / sub-team), never a hard lock?
- Do the Chemists make focus-fire and tempo matter (ignoring them = losing attrition)?
- Does the enemy Orator read as a distinct new caste without crossing into lockdown?
- Can the player exploit Orran's Celestial Stasis windows to pick off the frozen band?
- Is it a deliberately gentle Chapter 3 opener (2/5★) below the Vaults and Riovanes?
- Does it still read as a coal-town ambush on rooftops, not a designed arena?

## Sources

- Game8, "Mining Town of Gollund Walkthrough (Battle 22)": roster (2 Chemist, 3 Thief, 1 Orator),
  objective "Save Orran!", recommended level ~25, 2/5 stars, deploy 5, Orran guest casting
  Celestial Stasis, Thieves' Steal Heart charm, rooftop terrain + mounted mobility, rewards/treasure.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553182
- Final Fantasy Wiki, "Goland Coal City" / "Orran Durai": story/terrain context.
  https://finalfantasy.fandom.com/wiki/Goland_Coal_City
- Local: `docs/battles/024-chapter-3-overview.md` (job-escalation + rare-loot rules),
  `012-merchant-dorter.md` & `018-goug-lowtown.md` (Steal Heart charm precedent),
  `019-balias-swale.md` (protect-the-guest handling).
</content>
