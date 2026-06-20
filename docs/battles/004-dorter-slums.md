# 004 - Dorter Slums (Dorter Trade City)

Status: ✅ implemented (v1) — NG+ only, awaiting playtest
Chapter: 1
Battle order: Battle 5 (after Siedge Weald)
Target version: Enhanced v1.5.0
ENTD: global entry **385** (local entry 1, `battle_entd4_ent.bin`)
Patcher: `tools/battle_patch.py dorter`

> Identified by exact roster: 1 Knight + 3 Archer + 2 Black Mage (the only such low-level entry).
> Vanilla slots: s3 Knight, s4-s6 Archer, s7-s8 Black Mage (s0/s1 guest slots, s2 a story slot —
> all left untouched). No OverrideEntryData on this entry, so the `.bin` edits apply directly.
> Implemented mapping (gear = strongest SHOP-tier per category, no treasure/Unknown20 loot):
> - s3 Knight L102: Counter/Attack Boost/Move+1; Helm(154)/Armor(182)/Bracers(218)/Runeblade(30)/Shield(139)
> - s4,s5 Archer L101 + s6 Archer L100: Reflexes/Concentration/Move+1; Thief's Cap/Black Garb/Bracers/Windslash Bow
> - s7,s8 Black Mage L101: Reflexes/Move+1; Mage Hat(167)/Robe(206)/Featherweave(234)/Rod(56). Support
>   left vanilla (no confirmed MA-boost support id yet — revisit if the mages underperform).
> Positions kept vanilla (already the rooftop layout). 60 bytes changed, all inside entry 385.

## Original Battle

Objective:

```text
Defeat all enemies!
```

Player deployment:

```text
Up to 4 units, including Ramza. No guests — this is the party's own fight.
```

Original enemy composition:

```text
1x Knight
3x Archer
2x Black Mage
```

Public walkthrough details:

```text
Recommended level: ~3
The famous Chapter 1 difficulty spike — the first fight that filters new players.
Urban map of stacked buildings: tall rooftops and stairs create steep elevation.
The Archer on the topmost building has offensive reach over most of the map.
Black Mages bring the first stacked magic threat; the Knight anchors the ground.
Lesson: control the high ground, kill ranged/magic first, bring your own ranged + a frontliner.
```

Design reading:

Dorter is **the wall**. Every earlier fight is a tutorial; Dorter is the exam. It is the first
battle built around **verticality plus ranged plus magic**: three Archers rain down from
rooftops (one with near-map-wide reach), two Black Mages threaten the first real AoE, and a
single Knight holds the ground so the player can't just rush the casters. The terrain *is* the
boss — if you fight on the low ground you lose.

For New Game++ the identity must stay exactly this: **a vertical gauntlet where the high
ground, the archers, and the mages punish anyone who clumps on the street.** This is the one
Chapter 1 fight where stacked casters and ranged units are not just allowed but mandatory —
the budget for "the spike" is spent here, deliberately. It should be the hardest fight of the
chapter short of the Ziekden finale.

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm the 6 enemy slots: 1 Knight / 3 Archer / 2 Black Mage, plus the player slot(s).
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
```

Job IDs (carry over known, verify the rest in-game):

```text
77 = Archer            (confirmed)
Knight job id          (TBD - verify)
Black Mage job id      (TBD - verify)
```

## New Game++ Design Goal

Keep the identity:

```text
A rooftop gauntlet. The high ground belongs to the enemy until the player takes it.
Three archers + two mages + one anchor knight = the player must answer range AND magic AND
a frontline at the same time, exactly as the original demanded.
```

Raise the challenge by:

```text
Scaling all six so archer chip and Black Mage AoE are genuinely dangerous to an endgame party.
Keeping the topmost archer as a real map-wide sniper (high level + Concentration + strong bow).
Equipping the Knight as a true durable anchor so the casters can't be reached for free.
Final-shop gear throughout, flavored as a better-funded Corpse Brigade cell in a trade city.
```

Avoid for this battle (see overview rules):

```text
Knight equipment-break skillsets (breaking an endgame party's gear is unfun, not "hard").
Time Mage control (Stop / Don't Move) — magic pressure here is AoE damage, not lockdown.
Adding a 7th unit — the fight is already dense; the spike is elevation + scaling, not numbers.
Boss-tier offsets on generics (the Knight may hit +2, no further).
```

## Proposed Composition (New Game++ Dorter v1)

Keep the exact original 1/3/2 shape; scale and gear it. The rooftop sniper and the mages sit
at `101`, the ground Knight anchors at `102`, the two lower archers at `100-101`.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Ground anchor | Knight | `102` | Durable frontline; guards the stairs so casters can't be rushed. |
| n | Rooftop sniper | Archer | `101` | The map-wide threat on the topmost building. Concentration + strong bow. |
| n | Rooftop archer | Archer | `101` | Second elevated bow; covers the opposite approach. |
| n | Street archer | Archer | `100` | Lower-elevation bow; pressures units climbing toward the roofs. |
| n | Black Mage | Black Mage | `101` | First AoE threat; punishes clumped advances. |
| n | Black Mage | Black Mage | `101` | Second caster; forces the player to split and to close distance fast. |

Reasoning:

The original roster is already the platonic "spike," so the faithful move is to **scale and
properly equip it**, not redesign it. The Knight at `102` is the lynchpin: a tanky anchor on
the ground means the player has to deal with him *while* eating archer fire and mage AoE from
above — which is the whole point of Dorter. The topmost archer with Concentration is the
signature menace the walkthroughs warn about. Two Black Mages provide the AoE the original
introduced; at party level their spells finally bite.

## Builds (final-shop quality, trade-city Corpse Brigade)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

Gear flavor for Dorter: a better-funded Brigade cell in a trade hub — the Knight gets real
shop heavy gear (shield + mail), mages get robes/rods, archers get strong bows. All
non-unique / shop-tier (no Genji, no superboss loot).

### Ground Anchor - Knight (Lv 102)

```text
Job: Knight (id TBD)   JobLevel: 8   Secondary: none (NO Break skillset — see avoid list)
Reaction: Counter (442)
Support: Attack Boost (465)
Movement: Movement +1 (486)

Head: shop heavy helm (e.g. Crystal Helm-tier, id TBD)
Body: shop heavy armor (e.g. Crystal Mail-tier, id TBD)   - Knights CAN wear heavy armor
Accessory: Bracers (218)
Right hand: Runeblade (30) or Icebrand (29)
Left hand: shop shield (e.g. Crystal Shield-tier, id TBD) - high evade/block, anchors the ground
```

Role: the wall in front of the wall. Soaks the player's advance so the rooftop units keep
shooting. Shield + heavy armor makes him a real time-sink, not a speed bump.

### Rooftop Sniper - Archer (Lv 101)  [topmost building]

```text
Job: Archer (77)   JobLevel: 8   Secondary: none (or Fundaments 5)
Reaction: Reflexes (449)
Support: Concentration (469)     - the signature: ignores evasion across the map
Movement: Movement +1 (486)

Head: Thief's Cap (168)
Body: Black Garb (198)
Accessory: Bracers (218)
Right hand: Windslash Bow (87)   - long range + wind damage
Left hand: none / two-hand marker (254)
```

Role: the map-wide menace the guides warn about. Perched highest, Concentration means cover
and evasion won't save the player — they must climb to it or block line of sight.

### Rooftop Archer x1 + Street Archer x1 (Lv 101 / 100)

```text
Job: Archer (77)   JobLevel: 8   Secondary: none
Reaction: Reflexes (449)
Support: Concentration (469)
Movement: Movement +1 (486)

Head: Thief's Cap (168)
Body: Black Garb (198)
Accessory: Bracers (218)
Right hand: Windslash Bow (87)   (street archer may use a slightly lesser bow, id TBD)
Left hand: none / two-hand marker (254)
```

Role: cover the second approach and the climb. Together the three bows mean no lane up to the
roofs is safe.

### Black Mage x2 (Lv 101)

```text
Job: Black Mage (id TBD)   JobLevel: 8   Secondary: none
Reaction: Reflexes (449)        (or a magic-defensive reaction, id TBD)
Support: Magick/MA-boost support if available (id TBD)
Movement: Movement +1 (486)

Head: cloth/mage hat (id TBD)
Body: shop robe (e.g. Black Robe / Light Robe-tier, id TBD)
Accessory: Featherweave Cloak (234) or magic-defensive accessory (id TBD)
Right hand: shop rod/staff that boosts magic (id TBD)
Left hand: none (255)
```

Role: the first stacked AoE threat. Fire/Ice/Thunder at party level finally hurts. They
punish a clumped advance and force the player to spread out *while* archers pick off the
spread — the core tension of Dorter.

## Positioning Plan

```text
Knight starts on the ground at the foot of the main stairway/approach, facing the player's
  deployment — the gatekeeper to the rooftops.
Rooftop Sniper starts on the topmost building with the widest line of sight over the map.
Second rooftop Archer starts on an adjacent/opposite roof covering the other climb lane.
Street Archer starts at mid-elevation, punishing units that try to flank along the ground.
Both Black Mages start on rooftops behind the archers — reachable only after a climb, so
  their AoE covers the kill zone while the Knight stalls the front.
```

The whole map should say: "take the high ground or lose." Every safe-looking street tile
should be inside someone's range.

## Implementation Checklist

- [ ] Identify Dorter `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify 1 Knight + 3 Archer + 2 Black Mage + player slot(s).
- [ ] Confirm Knight and Black Mage job IDs and their legal equipment.
- [ ] Map shop-tier heavy armor / shield / robe / rod item IDs in `ItemData.xml`.
- [ ] Set levels: Knight `102`; rooftop sniper / 2nd archer / both mages `101`; street archer `100`.
- [ ] Set JobLevel `8` on all active enemy slots.
- [ ] Equip per builds; ensure the Knight does NOT get a Break skillset.
- [ ] Set positions: archers + mages on roofs, Knight on the ground approach.
- [ ] Patch via the correct layer; keep the diff inside the Dorter window only.
- [ ] Re-dump and diff; confirm changes are small and intentional.
- [ ] Install mod, test from a New Game+ save; verify the rooftop sniper actually pressures the map.

## Test Questions

- Is it the hardest fight of Chapter 1 before Ziekden, as it should be?
- Does the topmost archer feel like the menace the walkthroughs describe (without being unfair)?
- Does the Knight successfully stall the ground so the player can't just rush the casters?
- Do the two Black Mages punish clumping — is the player forced to spread *and* climb?
- Is "take the high ground" the obvious winning read, the way the original taught it?
- Does it still feel like a desperate trade-city street fight, not a designed arena?

## Sources

- Game8, "Dorter Slums Walkthrough (Battle 5)": roster (1 Knight, 3 Archer, 2 Black Mage),
  objective "Defeat all enemies!", deploy 4, recommended level ~3, topmost-archer map-wide
  reach, why it is the difficulty spike (elevation + ranged + magic).
  https://game8.co/games/Final-Fantasy-Tactics/archives/553166
- StrategyWiki, "Final Fantasy Tactics/Dorter Trade City": rooftop terrain, the classic
  difficulty-spike reputation, high-ground strategy.
  https://strategywiki.org/wiki/Final_Fantasy_Tactics
- Local: `docs/battles/000-chapter-1-overview.md` (design rules), `001-gariland.md`
  (confirmed Archer build: Concentration + Windslash Bow).
</content>
