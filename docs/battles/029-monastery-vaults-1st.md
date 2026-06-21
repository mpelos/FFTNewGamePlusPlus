# 029 - Monastery Vaults, 1st Level — Wiegraf (Orbonne Monastery)

Status: ✅ implemented (v1, entry 424)
Chapter: 3 — "The Valiant"
Battle order: Battle 26 (after Vaults 3rd Level) — **Vaults chain 3 of 3 (finale)**
Target version: Enhanced v1.5.0
ENTD: global entry **424** (local entry 40, `battle_entd4_ent.bin`)
File: `battle_entd4_ent.bin` (embedded NG+ swap) — `tools/battle_patch.py vaults_1st`

Implemented composition (entry 424, vanilla-dump verified):
- s0 Wiegraf (job 40 White/Holy Knight; Holy Sword innate) — L104/jl8; Heavy Helm/Heavy Armor/
  Bracers/Runeblade (strong NON-rare sword keeps Holy Sword weapon-tied/disarmable)/shop Shield;
  job/secondary/reaction-support-movement/FLEE scripting preserved. NO rare (flees; rare is at 034).
- s1,s2 Knight L101 — Heavy Helm/Heavy Armor/Bracers/Runeblade/shop Shield; Rend innate; Counter/Atk Boost/Mv+1.
- s4 Black Mage L101 — Mage Hat/shop Robe/Featherweave/shop Rod; Reflexes/Atk Boost/Mv+1.
- s3,s5 Archer L101/L100 — Thief's Cap/Black Garb/Bracers/Windslash Bow (two-hand); Reflexes/Concentration/Mv+1.
- s6,s7 = inactive placeholders (level 0xFE) — left untouched.

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `024-chapter-3-overview.md`.

## Original Battle

Objective:

```text
Defeat Wiegraf!  (he is defeated and FLEES — he does NOT die here. He returns at Riovanes Keep
  (034) for the duel that becomes Velius; his rare loot is paid out there, not at the Vaults.)
```

Player deployment:

```text
Up to 5 units, including Ramza. No guests. CLOSES the no-resupply Vault chain (2nd -> 3rd -> 1st):
  the player arrives on the same loadout they took into the 2nd Level.
```

Original enemy composition:

```text
1x Wiegraf  (Holy Knight BOSS — Holy Sword skills: ranged sword-waves with status; WEAPON-tied)
2x Knight
2x Archer
1x Black Mage  (ranged magic pressure)
Terrain: a TALL WALL with only FIVE DOORWAYS — center (Ramza vs Wiegraf), two upper, two lower.
```

Public walkthrough details:

```text
Recommended level: ~29.  Difficulty: 3/5 stars.
Wiegraf is a Holy Knight with Holy Sword abilities (ranged, weapon-dependent waves).
TOP PRIORITY: DISARM him — Steal Weapon (Thief) or Rend Weapon (Knight) removes his sword and
  cripples his Holy Sword offense, after which he is far more manageable.
The five doorways are natural CHOKEPOINTS: hold them to funnel the Knights/Archers and the Black
  Mage, and to control how the enemy reaches you.
No resupply (chain finale) — finish the Vaults on one loadout.
```

Design reading:

The 1st Level is **the Wiegraf rematch and chokepoint-control finale** of the Vault chain. It echoes
Fovoham (`008`) — a Holy Knight boss whose power is a **weapon-tied sword skill** answered by
**disarming him** — but now staged on a **five-doorway wall** that turns the fight into a
**positional puzzle**: hold the chokepoints to funnel the Knight/Archer/Black-Mage screen, then
punch a disarmer through to Wiegraf to switch off his Holy Sword waves. Because he **flees** rather
than dies, this is the *threat* installment; the *payoff* (his death/transformation and rare loot)
waits at Riovanes. It tests doorway control (Sand Rat `005`), disarm priority (Fovoham `008` /
Gaffgarion `020`–`021`), and resource discipline (chain finale, no resupply).

For New Game++ the identity must stay: **a five-doorway chokepoint duel where a Holy-Sword Wiegraf
must be disarmed (not out-traded) while a knight/archer/mage screen contests the gates — won by
holding the doorways and reaching him with a disarmer, on the chain's last loadout. He flees.**

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm slots: Wiegraf + 2 Knight + 2 Archer + 1 Black Mage, plus the player slots.
DO NOT touch Wiegraf's FLEE/retreat scripting (he must escape at his HP threshold; he does NOT die
  here — his death + rare loot are a Riovanes Keep matter, 034).
Keep Wiegraf's Holy Sword tied to his WEAPON so Steal/Rend Weapon is the fair counter.
Keep the FIVE-DOORWAY wall geometry (the chokepoint puzzle depends on it).
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
```

Job IDs (carry over known, verify the rest in-game):

```text
77 = Archer            (confirmed)
Knight job id          (TBD - verify)
Black Mage job id      (TBD - verify)
Holy Knight job id     (TBD - verify; Wiegraf — Holy Sword; from Fovoham 008)
```

## Job Escalation (Chapter 3 rule)

```text
THE WRINKLE IS THE TERRAIN + RETURNING BOSS: Wiegraf the Holy Knight already appeared at Fovoham
(008); here the escalation is the FIVE-DOORWAY CHOKEPOINT WALL layered on the disarm-the-Holy-Sword
puzzle, now backed by RANGED MAGIC (a Black Mage) instead of bruisers. Per "one new wrinkle per
fight," NO new generic caste is added — the positional doorway control is the new demand.
WHY: a chokepoint duel against a weapon-tied sword-boss with a mage screen is a dense, distinct
  problem; the brand-new castes (Ninja, Oracle, Velius) debut in their own fights. Keep the
  2 Knight / 2 Archer / 1 Black Mage / Wiegraf shape.
```

## Sanctioned exceptions (carried precedents)

```text
HOLY SWORD / weapon-tied boss skill — allowed and intended (Fovoham 008 precedent): Wiegraf's Holy
  Sword waves stay WEAPON-tied so Steal/Rend Weapon is the fair, telegraphed off-switch. Constrain
  any status on the waves to soft status — NO hard lock (no Stop/Don't Act) on an endgame party.
KNIGHT Rend (break) — allowed on ONE of the two Knights (016/021/028 precedent): shop-tier
  breakable gear, Safeguard counter.
```

## Boss rare loot

```text
None HERE. Wiegraf FLEES — he does not die at the Vaults, so there is nothing to drop (Gallows 020
/ Zalmo 026 precedent: a retreating boss carries no rare). His rare is paid out at RIOVANES KEEP
(034), where the Wiegraf duel becomes Velius and is killed — give the marquee Templar/Holy-Knight
KNIGHT-SWORD rare (e.g. Defender) and/or the Velius demon rare THERE, not here.
Generics stay shop-tier. The map's rare TREASURE (Winged Boots / Magepower Gloves / Reflect Ring /
Nu Khai Armband) is existing map treasure, not boss loot; leave it as-is.
```

## Proposed Composition (New Game++ Vaults 1st v1)

Keep the exact roster; Wiegraf is the boss spike (flees). Wiegraf `104`; Knights `101`; Black
Mage `101`; Archers `100`–`101`.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Wiegraf (BOSS) | Holy Knight | `104` | Weapon-tied Holy Sword waves; DISARM him, then beat him to his flee threshold. |
| n | Knight (Rend) | Knight | `101` | Holds/contests a doorway; break-wall on the disarmer's path. |
| n | Knight | Knight | `101` | Second gate body; pressures a flank doorway. |
| n | Archer | Archer | `101` | Ranged punishment through the doorways. |
| n | Archer | Archer | `100` | Second bow; covers another gate lane. |
| n | Black Mage | Black Mage | `101` | Ranged magic that punishes a clumped doorway hold. |

Reasoning:

The faithful move is to **make Wiegraf the spike, keep the disarm puzzle, and let the five doorways
carry the tactics**. At `104` with weapon-tied Holy Sword, trading blows loses to his ranged waves —
the player must hold the chokepoints, funnel the Knight/Archer/Black-Mage screen, and push a
disarmer (Steal/Rend Weapon) through to him, then beat him to his flee threshold. The Black Mage
punishes a careless doorway cluster (don't stack in one gate). He flees (no kill, no drop),
preserving the Riovanes payoff. As the chain finale it should tax the one-loadout party hardest of
the three Vaults — a clear boss step, still below Riovanes Keep / the demon.

## Builds (final-shop quality; Holy Knight + vault garrison flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Wiegraf — Holy Knight BOSS (Lv 104) — flees, no drop

```text
Job: Holy Knight (id TBD)   JobLevel: 8   Primary: Holy Sword (ranged waves; WEAPON-tied; soft status only)
Reaction: Counter (442) or a parry reaction (id TBD)   Support: Attack Boost (465)
Movement: Movement +1 (486)
Head/Body: shop heavy helm + heavy armor (ids TBD)
Accessory: Bracers (218)   Right hand: a strong NON-RARE knight sword (shop-tier-best, id TBD —
  NOT his Riovanes rare)   Left: shop shield (id TBD)
FLEES at HP threshold — do NOT let him die here; no rare loot at the Vaults.
```

Role: the boss. His Holy Sword waves dominate at range until disarmed; the answer is Steal/Rend Weapon.

### Knight x2 (Lv 101) — 1x Rend

```text
Job: Knight (id TBD)   JobLevel: 8   Secondary: Rend (break) on ONE of the two (id TBD)
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head/Body: shop heavy helm + heavy armor (ids TBD)
Accessory: Bracers (218)   Right hand: Runeblade (30) / Icebrand (29)   Left: shop shield (id TBD)
```

Role: gate bodies that contest the doorways and make reaching Wiegraf with a disarmer costly.

### Archer x2 (Lv 101 / 100)

```text
Job: Archer (77)   JobLevel: 8   Secondary: none
Reaction: Reflexes (449)   Support: Concentration (469)   Movement: Movement +1 (486)
Head: Thief's Cap (168)   Body: Black Garb (198)   Accessory: Bracers (218)
Right hand: Windslash Bow (87)   Left hand: none / two-hand marker (254)
```

Role: ranged fire through the doorways onto the holders.

### Black Mage (Lv 101)

```text
Job: Black Mage (id TBD)   JobLevel: 8   Secondary: none
Reaction: Reflexes (449)   Support: MA/Magick-boost (id TBD)   Movement: Movement +1 (486)
Head: cloth/mage hat (id TBD)   Body: shop robe (id TBD)
Accessory: Featherweave Cloak (234)   Right hand: shop magic-boost rod (id TBD)   Left: none (255)
```

Role: AoE/ranged magic that punishes a clumped doorway hold — forces the player to spread the gates.

## Positioning Plan

```text
Wiegraf starts at the CENTER doorway (the canonical Ramza-vs-Wiegraf spot), with Holy Sword reach
  over the approach.
The 2 Knights hold/contest the upper and lower side doorways; the 2 Archers fire through gates; the
  Black Mage sits back with a line onto whichever doorway the player clusters at.
Preserve the FIVE-DOORWAY wall so chokepoint control is the core tactic.
Preserve Wiegraf's flee trigger; keep his Holy Sword weapon-tied.
```

The vault should say: "hold the gates, funnel his guard, and take the Holy Knight's sword before his
waves take your party — then run him off."

## Implementation Checklist

- [ ] Identify Vaults 1st `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify Wiegraf + 2 Knight + 2 Archer + 1 Black Mage + player slots.
- [ ] Confirm Holy Knight / Knight / Black Mage job ids; keep Holy Sword WEAPON-tied (disarmable).
- [ ] Give Wiegraf a strong NON-RARE knight sword here (no drop; the rare is at Riovanes 034).
- [ ] Constrain Holy Sword to soft status (no hard lock); Rend on ONE Knight.
- [ ] Set levels: Wiegraf `104`; Knights + Black Mage + one Archer `101`; second Archer `100`.
- [ ] Set JobLevel `8` on all active enemy slots.
- [ ] PRESERVE Wiegraf's FLEE scripting (he must NOT die here) and the five-doorway geometry.
- [ ] Patch via the correct layer; keep the diff inside the Vaults 1st window only.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify flee + doorways.
- [ ] Install mod, test from a New Game+ save (on the chain loadout); confirm disarm + chokepoints work.

## Test Questions

- Is disarming Wiegraf (Steal/Rend Weapon) the clear answer to his Holy Sword waves?
- Do the five doorways make chokepoint control the core tactic (funnel the screen, pick a gate)?
- Does the Black Mage punish clumping enough to force gate discipline?
- Does Wiegraf FLEE (not die) with no lootable rare, preserving the Riovanes Keep payoff?
- Is the chain finale winnable on one loadout without feeling resource-starved?
- Is it a boss step above Izlude but below Riovanes Keep / the Velius demon?
- Does it still read as a desperate vault stand, not a designed arena?

## Sources

- Game8, "Monastery Vaults: First Level Walkthrough (Battle 26)": roster (Wiegraf + 2 Knight,
  2 Archer, 1 Black Mage), objective "Defeat Wiegraf!", recommended level ~29, 3/5 stars, deploy 5,
  Holy Knight Holy Sword skills, disarm priority (Steal/Rend Weapon), five-doorway wall chokepoints,
  rewards/treasure.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553186
- Final Fantasy Wiki, "Wiegraf Folles": story + Holy Sword context.
  https://finalfantasy.fandom.com/wiki/Wiegraf_Folles
- Local: `docs/battles/024-chapter-3-overview.md` (job-escalation + rare-loot rules),
  `008-fovoham-windflats.md` (Wiegraf Holy-Knight / disarm precedent), `005-sand-rat-sietch.md`
  (chokepoint control), `028-monastery-vaults-3rd.md` (Izlude, chain 2/3), `020-golgollada-gallows.md`
  (retreating boss → no drop).
</content>
