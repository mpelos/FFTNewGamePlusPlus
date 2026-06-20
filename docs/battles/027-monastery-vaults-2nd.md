# 027 - Monastery Vaults, 2nd Level (Orbonne Monastery — Underground Vault)

Status: designed (not yet implemented)
Chapter: 3 — "The Valiant"
Battle order: Battle 24 (after Lesalia Castle Postern) — **Vaults chain 1 of 3**
Target version: Enhanced v1.5.0
ENTD: global entry **TBD** — confirm on Windows game data
File: `battle_entd*_ent.bin` (TBD) / `OverrideEntryData` rows (TBD)

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `024-chapter-3-overview.md`.

## Original Battle

Objective:

```text
Defeat all enemies!
```

Player deployment:

```text
Up to 5 units, including Ramza. No guests.
CHAIN: this fight is IMMEDIATELY followed by the Vaults 3rd Level (Izlude) with NO resupply or
  gear change — and the 1st Level (Wiegraf) after that. Prepare for three battles on one loadout.
```

Original enemy composition:

```text
1x Chemist   (sustain — heal/revive/items)
2x Time Mage (Haste the Dragoons / Slow the player)
3x Dragoon   (Jump — telegraphed aerial strikes onto the back line; the new enemy caste)
```

Public walkthrough details:

```text
Recommended level: ~28.  Difficulty: 3/5 stars.
Underground monastery vault.
Eliminate the CHEMIST first (removes the band's sustain), then deal with the Dragoons.
The 3 Dragoons JUMP — a telegraphed leap that lands on a target after a delay, ideal for diving
  the player's casters/back line. The 2 Time Mages HASTE the Dragoons (faster, more frequent Jumps)
  and SLOW the player.
No resupply afterward — manage HP/MP/items across the chain.
```

Design reading:

The 2nd Level is **the enemy Dragoon debut** and a tempo-and-positioning puzzle. The player learned
Jump on their *own* side at Zaland (`015`); now it is turned against them — three Dragoons leap over
the vault's obstacles to dive the back line, and two Time Mages accelerate the dives (Haste) while
slowing the player's response. The Chemist makes a slow, unfocused fight a losing attrition game.
The lesson is **target priority** (kill the Chemist's sustain, then break the Dragoon/Time-Mage
engine), **Jump-dodging** (Jump is telegraphed — reposition the dived unit, or kill the Dragoon
while it's grounded), and **resource discipline** (no resupply across the chain).

For New Game++ the identity must stay: **an underground tempo fight where Hasted Dragoons dive the
back line and a Chemist sustains the band — won by killing the sustain, punishing grounded
Dragoons, and dodging telegraphed Jumps, all on a one-loadout budget.**

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm slots: 1 Chemist + 2 Time Mage + 3 Dragoon, plus the player slots.
Keep the underground vault geometry (obstacles/elevation that Dragoons Jump over).
Confirm the NO-RESUPPLY chain link into the 3rd Level (Izlude) — do not break the chain.
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
```

Job IDs (carry over known, verify the rest in-game):

```text
75 = Chemist           (confirmed)
Time Mage job id       (TBD - verify; from Ch1 Lenalian / Ch2 Goug & Gallows)
Dragoon/Lancer job id  (TBD - verify; enemy caste debut — player-side at Zaland 015)
```

## Job Escalation (Chapter 3 rule)

```text
THE NEW CASTE IS BUILT IN: this battle debuts the enemy DRAGOON (Lancer) — three of them, using
Jump to dive the player's back line over the vault's obstacles. The Dragoon caste IS this fight's
escalation; per "one new wrinkle per fight," NO additional generic job is swapped in. Keep the
1 Chemist / 2 Time Mage / 3 Dragoon shape.
WHY: Hasted aerial Jump pressure is a genuinely new tactical problem (the threat ignores walls and
  picks your casters). The Time Mages (established tempo caste) amplify it rather than adding a new
  mechanic, so the "one new wrinkle" budget is respected. Ninja/Oracle/Velius debut later.
```

## Sanctioned exceptions (carried precedents)

```text
TIME MAGE control — allowed (Lenalian 007 / Goug 018 / Gallows 020 precedent): the TWO Time Mages
  are restricted to Haste (on the Dragoons) / Slow (on the player) / Float-tier ONLY. NO Stop,
  Immobilize, Don't Move, Don't Act. As at the Gallows, two Time Mages co-exist here because they
  are canonical AND they amplify the headline (the Dragoons), not lock the player.
DRAGOON Jump — allowed and intended: it is TELEGRAPHED (the leap shows its target/timing), so the
  counter (reposition the dived unit, or kill the grounded Dragoon, or intercept mid-charge) stays
  fair. Keep Jump's normal charge/landing cadence; do NOT make it instant.
```

## Boss rare loot

```text
None. No named boss here — no rare boss item (per the Chapter 3 overview). Generics stay shop-tier.
(The map's rare TREASURE — Murasame / Poison Crossbow / Mythril Bow / Musk Pole — is existing map
treasure, not boss loot; leave it as-is. The chapter's boss rares come at Izlude 028 / Wiegraf 029.)
```

## Proposed Composition (New Game++ Vaults 2nd v1)

Keep the exact roster; this is a tempo/positioning fight, not a damage wall. One Dragoon anchors at
`102`; the rest at `100`–`101`. The Time Mages and Chemist at `101`.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Dragoon (lead, NEW caste) | Dragoon | `102` | Jump-dives the back line; the headline aerial threat. |
| n | Dragoon | Dragoon | `101` | Second diver; splits the player's protection. |
| n | Dragoon | Dragoon | `100` | Third diver; grounded body when not leaping. |
| n | Time Mage | Time Mage | `101` | Hastes the Dragoons (faster Jumps) / Slows the player. |
| n | Time Mage | Time Mage | `101` | Second tempo caster; reinforces the dive clock. |
| n | Chemist | Chemist | `101` | Heal/revive sustain — the priority kill. |

Reasoning:

The faithful move is to **keep the Dragoon/Time-Mage engine and the Chemist sustain, and let tempo
+ positioning carry the fight**. Three Dragoons mean the player's casters are never safe behind
cover; two Time Mages shorten the dive clock and slow the response; the Chemist punishes a slow,
scattered kill. The intended solution survives: drop the Chemist first to stop the revives, then
break the Dragoon/Time-Mage loop while dodging telegraphed Jumps — all on a single loadout because
the chain offers no resupply. Modest levels keep it a 3/5★ tempo puzzle, not a numbers wall.

## Builds (final-shop quality; Templar vault garrison flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Dragoon x3 (Lv 102 / 101 / 100) — NEW caste

```text
Job: Dragoon/Lancer (id TBD)   JobLevel: 8   Primary: Jump (innate)
Reaction: Reflexes (449) or Counter (442)   Support: Attack Boost (465)
Movement: Movement +1 (486) or Ignore Height (id TBD — fits vault elevation)
Head/Body: shop helm + light/medium armor (ids TBD)
Accessory: Germinas Boots (210) or Bracers (218)
Right hand: shop spear (id TBD)   Left: shop shield (id TBD) or two-hand the spear (254)
```

Role: the aerial threat — Jump over the vault obstacles onto the back line; dangerous when Hasted,
vulnerable when grounded.

### Time Mage x2 (Lv 101) — Haste/Slow only

```text
Job: Time Mage (id TBD)   JobLevel: 8   Secondary: none
Skillset limit: Haste (on the Dragoons) / Slow (on the player) / Float-tier ONLY.
  NO Stop, Immobilize, Don't Move, Don't Act.
Reaction: Reflexes (449)   Support: MA/Magick-boost (id TBD)   Movement: Movement +1 (486)
Head: cloth/mage hat (id TBD)   Body: shop robe (id TBD)
Accessory: Featherweave Cloak (234)   Right hand: shop magic-boost rod (id TBD)   Left: none (255)
```

Role: the dive accelerator — Haste the Dragoons, Slow the player; pressure without lockdown.

### Chemist (Lv 101) — sustain

```text
Job: Chemist (75)   JobLevel: 8   Primary: Item (Hi-Potion / Phoenix Down / Remedy / Ether)
Reaction: Auto-Potion (441)   Support: Throw Items (474)   Movement: Movement +1 (486)
Head: shop hat (id TBD)   Body: shop clothes (id TBD)   Accessory: Bracers (218)
Right hand: shop gun/knife the job allows (id TBD)   Left: none
```

Role: the sustain spine and priority kill — revives keep the Dragoon engine running.

## Positioning Plan

```text
The Chemist starts back/protected (behind the Dragoons), so reaching the sustain takes effort —
  but killing it first is the intended priority.
The 3 Dragoons start spread with clear Jump lines onto where the player's casters will stand.
The 2 Time Mages start mid/back so they can Haste the Dragoons on turn 1.
Preserve the vault obstacles/elevation that make Jump (and Ignore Height) matter.
Remember: NO resupply into the 3rd Level — the player should be able to win without burning every
  item, or Izlude becomes unfair.
```

The vault should say: "their lancers ignore your walls and their chronomancers speed the dives —
kill the medic, ground the dragoons, and don't waste a potion you'll need upstairs."

## Implementation Checklist

- [ ] Identify Vaults 2nd `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify 1 Chemist + 2 Time Mage + 3 Dragoon + player slots.
- [ ] Confirm Dragoon/Lancer + Time Mage job ids; keep Jump's normal charge cadence (telegraphed).
- [ ] Constrain BOTH Time Mages to Haste/Slow (no hard lock).
- [ ] Set levels: lead Dragoon `102`; other Dragoons `100`/`101`; both Time Mages + Chemist `101`.
- [ ] Set JobLevel `8` on all active enemy slots.
- [ ] Preserve the vault geometry + the NO-RESUPPLY chain link into the 3rd Level.
- [ ] Patch via the correct layer; keep the diff inside the Vaults 2nd window only.
- [ ] Re-dump and diff; confirm changes are small and intentional.
- [ ] Install mod, test from a New Game+ save; verify Jump is dodgeable and the chain is winnable on
      one loadout.

## Test Questions

- Do the Dragoons' Jumps genuinely threaten the back line, and are they telegraphed/dodgeable?
- Does killing the Chemist first clearly matter (revive sustain), as the original taught?
- Do the Hasted Dragoons feel faster without the Time Mages ever hard-locking the player?
- Is the fight winnable without burning the items needed for the 3rd Level (chain discipline)?
- Does the enemy Dragoon read as a distinct new caste vs the player's own Zaland Dragoon (015)?
- Is it a fair 3/5★ tempo puzzle — above Lesalia, below the Izlude/Wiegraf bosses?
- Does it still read as a Templar vault garrison, not a designed arena?

## Sources

- Game8, "Monastery Vaults: Second Level Walkthrough (Battle 24)": roster (1 Chemist, 2 Time Mage,
  3 Dragoon), objective "Defeat all enemies!", recommended level ~28, 3/5 stars, deploy 5,
  underground vault, eliminate Chemist first + disable Dragoons, no-resupply chain into the 3rd
  Level, rewards/treasure.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553184
- Final Fantasy Wiki, "Orbonne Monastery": story/terrain context.
  https://finalfantasy.fandom.com/wiki/Orbonne_Monastery
- Local: `docs/battles/024-chapter-3-overview.md` (job-escalation + rare-loot rules),
  `015-zaland.md` (player-side Dragoon Jump, for contrast), `020-golgollada-gallows.md` (two Time
  Mages amplifying a headline), `018-goug-lowtown.md` (Time Mage Haste/Slow limit).
</content>
