# 042 - Beddha Sandwaste (Bed Desert)

Status: ✅ implemented (v1, entry 447)
Chapter: 4 — "In the Name of Love"
Battle order: Battle 37 (after Outlying Church)
Target version: Enhanced v1.5.0
ENTD: global entry **447** (local entry 63, `battle_entd4_ent.bin`)
File: `battle_entd4_ent.bin` (embedded NG+ swap) — `tools/battle_patch.py bed_desert`

Implemented (entry 447, vanilla-dump verified):
- s0 **Barich** (job 43 Machinist, BOSS, dies → rare pays) — L104/jl8; Tier-A rare = **Glacial Gun (74)**,
  already his equipped weapon (steal-bait = disarm + reward); job/secondary/head/body/acc/win-on-death preserved.
- s1,s2 Knight L102 — Heavy gear/Runeblade/shop Shield; Rend innate (cap 2); Counter/Atk Boost/Mv+1.
- s3 Black Mage L102 — Mage Hat/shop Robe/Featherweave/shop Rod; Reflexes/Atk Boost/Mv+1.
- s4,s5 Archer L102/L101 — Thief's Cap/Black Garb/Bracers/Windslash (two-hand); Reflexes/Concentration/Mv+1.
- s6,s7 = job-43 Barich-clone scripting placeholders (jl0) — left untouched. NO Hydra. Only Barich at band 104.
- Barich recurs at Lost Halidom (057) as a Tier-S dragon fight — no double-best (gun paid here only).

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `037-chapter-4-overview.md`.

## Original Battle

Objective:

```text
Defeat Barich!   (the battle ends the instant he falls — he is defeated here)
```

Player deployment:

```text
Up to 5 units, including Ramza. No guests.
```

Original enemy composition (verified via Game8, Battle 37):

```text
Barich Fendsor (Desert)   (BOSS — Knights Templar machinist; GLACIAL GUN — ranged ice nukes)
2x Knight                 (front-line; Rend/break)
2x Archer                 (ranged chip — desert sightlines)
1x Black Mage             (AoE caster)
```

> Correction to the overview's tentative note: there is **NO Hydra** at Bed Desert. The Hydra (and
> Tiamat) appear later, at **Lost Halidom (`052`)**, in the endgame. Bed Desert is Barich's
> long-range **gun-sniper** fight.

Public walkthrough details:

```text
Recommended level: ~43.  Difficulty: 3/5 stars.  Deploy up to 5.  Win: defeat Barich (ends fight).
DESERT open field — long, open sightlines suit ranged play (gun, bows, AoE).
THE THREAT — BARICH'S GLACIAL GUN: fires ICE spells (Blizzard up to Blizzaga) at GUN RANGE — a
  long-range elemental nuke that ignores the usual caster charge time. The walkthrough's tip: equip an
  ICE SHIELD to ABSORB his shots (turn his damage into healing), and/or close the distance.
SUPPORT: two Knights screen, two Archers snipe the open lanes, one Black Mage adds AoE.
Rewards: 30,600 Gil, buried rare Yagyu Darkrood (ninja sword).
```

Design reading:

Bed Desert is **the long-range gun-duel**: Barich is a Knights Templar **machinist** whose **Glacial
Gun** snipes high-tier ice from across the open desert — a ranged nuke with no charge tell. Its
identity is **a distance/elemental puzzle**: the player must **close on the gunner, absorb his element
(Ice Shield), or disarm him**, all while crossing open sand under a ranged screen (Archers + Black
Mage AoE). Because the fight ends when Barich falls, it rewards reaching and bursting the gunner over
trading shots across the dunes.

The most elegant New Game++ move is to keep his **Glacial Gun as the steal-bait Tier-A rare** — so the
disarm line (Steal Weapon) *both* rewards the player with a rare elemental gun *and* removes his ice
threat, exactly like disarming Wiegraf's Holy Sword in Ch3.

For New Game++ the identity must stay: **an open-desert gun-duel — close on / absorb / disarm a
long-range ice-gun Templar and burst him through a ranged screen — with his Glacial Gun as the
tempting, threat-removing steal; the boss is the escalation, the screen stays familiar.**

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm slots: Barich (boss) + 2 Knight + 2 Archer + 1 Black Mage, plus the player slots. NO Hydra.
Keep the win condition = "Defeat Barich" (ends on his fall) and the OPEN DESERT geometry (long
  sightlines — the distance puzzle IS the fight; do not box it in).
Keep Barich's Glacial Gun (ranged ice) and make it STEALABLE (Steal Weapon disarms his threat = reward).
This is a Tier-A BOSS fight: boss spike at 104, adds 101-103; ONE Tier-A rare on Barich (his gun).
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
Leave the buried map rare (Yagyu Darkrood) as-is — map loot, not boss loot.
BARICH RECURS at Lost Halidom (052) as a Tier-S endgame fight (with Hydra + Tiamat) — pay only the
  Tier-A gun HERE; the 052 encounter is handled separately (the dragons are its stars). No double-best.
```

Job IDs (carry over known, verify the rest in-game):

```text
77 = Archer            (confirmed)
Knight job id          (TBD - verify)
Black Mage job id      (TBD - verify)
Knights Templar / Machinist id (TBD - verify; Barich's boss job)
```

## Job Escalation (Chapter 4 rule)

```text
CHANGE: NO generic-slot swap. The escalation is the BOSS — Barich is a Knights Templar machinist whose
  Glacial Gun delivers high-tier RANGED ELEMENTAL damage with no charge tell, a distinct threat-profile
  from the melee-break Templars (Meliadoul/Izlude).
WHY: the fight's identity is already "cross open ground and neutralize a long-range elemental gunner."
  The faithful Ch4 escalation is to deliver that gun-boss at full strength on the open desert — NOT to
  add a new mechanic onto a roster that already has Archers (ranged) + a Black Mage (AoE). A second
  wrinkle would break the one-new-demand rule; the ranged ice-gun boss IS the demand.
CONSTRAINT: the gun is answerable — ICE SHIELD absorbs it, closing distance removes the range
  advantage, and STEAL WEAPON disarms it (the intended reward). High but FAIR; no hard lock.
WHAT IS NOT CHANGED: the open desert, the 2 Knight + 2 Archer + 1 Black Mage ranged screen, and the
  "reach and burst the boss" win line remain. No brand-new caste debuts here.
```

## Sanctioned exceptions (carried precedents)

```text
RANGED ELEMENTAL GUN (Barich's Glacial Gun) — allowed as the boss's identity: high-tier ice at gun
  range. Counters: Ice Shield ABSORB (heals you), close the distance, or Steal Weapon (disarm = the
  reward). Not a status; race-able; no hard lock.
KNIGHT REND / BREAK — only 2 Knights here, within the carried ≤2-break-source cap; telegraphed,
  Safeguard/Steal answers.
BLACK MAGE AoE — boosted elemental, race-able by rushing it (Ch4 opener precedent, 038). Not new.
```

## Boss rare loot

```text
BARICH (boss) drops/carries ONE Tier-A rare: GLACIAL GUN (his equipped weapon — a rare, non-buyable
  ice-element gun).
WHY IT FITS: it IS his signature; making it the steal-bait means the disarm line (Steal Weapon) both
  REWARDS the player with a rare elemental gun AND removes his ranged ice threat — a clean,
  identity-true mechanic (cf. disarming Wiegraf's Holy Sword, Ch3 029/034). A rare elemental gun is a
  clear best-non-ultimate prize without being best-in-slot.
TIER: A (mid-Chapter-4 best non-ultimate). NOT Tier-S — guns have no reserved "ultimate" tier, but the
  Tier-S capstones (Ragnarok/Chaos Blade/etc.) stay on the endgame (47-53).
He is DEFEATED here (win = defeat Barich), so the rare pays out here. His later Lost Halidom (052)
  appearance is a SEPARATE endgame encounter (Tier-S, dragon-themed) — no double-best.
```

## Proposed Composition (New Game++ Bed Desert v1)

Keep the count (6) and the open-desert gun-duel shape; elevate Barich to full boss strength, keep the
ranged screen. Boss `104`; Knights `102`; Archers `102`/`101`; Black Mage `102`.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Barich (BOSS) | Knights Templar (machinist) | `104` | Glacial-Gun ranged ice nukes; the objective; gun is the steal-bait. |
| n | Knight | Knight | `102` | Front-line screen; Rend (break source 1). |
| n | Knight | Knight | `102` | Second screen; Rend (break source 2 — cap reached). |
| n | Archer | Archer | `102` | Ranged chip across the open dunes. |
| n | Archer | Archer | `101` | Second archer; covers the approach lanes. |
| n | Black Mage | Black Mage | `102` | AoE caster — punishes the player if they clump while closing. |

Reasoning:

The faithful move is to **make the gun-boss the whole escalation and keep the desert screen
recognizable**. Barich at `104` with a high-range Glacial Gun (absorb-/close-/steal-counterable) and
his gun as steal-bait delivers the "cross the sand and neutralize the gunner" duel at full Ch4
strength — and the steal line is its own reward. The two Knights (Rend capped at the two of them),
two Archers, and Black Mage stay as the ranged screen that makes crossing the open ground costly — no
new mechanic added. Only Barich sits at the boss band (`104`); the screen is `101`–`102`.

## Builds (Chapter-4 quality; desert machinist-Templar flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Barich (Lv 104) — BOSS (machinist Templar)

```text
Job: Knights Templar / Machinist (id TBD)   JobLevel: 8   Primary: gun fire (Glacial Gun ice spells) +
  (light) Aim/disable shots   Secondary: basic
Reaction: (anti-burst) Reflexes / Counter (id TBD)   Support: Concentration (469) or Attack Boost (465)
  Movement: Movement +1 (486)
Head: Tier-A helm (id TBD)   Body: Tier-A armor (id TBD)   Accessory: Tier-A accessory (id TBD)
Right hand: GLACIAL GUN (Tier-A rare, ice element, id TBD)   Left: none / two-hand (254)
```

Role: the long-range threat and objective — absorb (Ice Shield) / close / disarm (Steal Weapon) and
burst him. Keep the gun stealable (the reward AND the disarm).

### Knight x2 (Lv 102) — desert screen

```text
Job: Knight (id TBD)   JobLevel: 8   Primary: basic + Rend (both — 2 sources = cap)
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head: shop helm (id TBD)   Body: shop heavy armor (id TBD)   Accessory: Bracers (218)
Right hand: shop knight sword (id TBD)   Left: shop shield (id TBD)
```

Role: front-line screen slowing the player's approach across the sand; Rend within the cap.

### Archer x2 (Lv 102 / 101) — open-lane chip

```text
Job: Archer (77)   JobLevel: 8   Secondary: none
Reaction: Reflexes (449)   Support: Concentration (469)   Movement: Movement +1 (486)
Head: Thief's Cap (168)   Body: Black Garb (198)   Accessory: Bracers (218)
Right hand: shop high-tier bow (id TBD)   Left: none / two-hand marker (254)
```

Role: ranged chip exploiting the open desert sightlines; punishes a slow approach.

### Black Mage (Lv 102) — AoE

```text
Job: Black Mage (id TBD)   JobLevel: 8   Secondary: none
High-tier AoE (Fire/Bolt/Ice 3-tier). Black-Robe-equivalent body.
Reaction: Reflexes (449)   Support: MA/Magick-boost (id TBD)   Movement: Movement +1 (486)
Head: mage hat (id TBD)   Body: Black Robe-equivalent (id TBD)
Accessory: Featherweave Cloak (234)   Right hand: magic-boost rod (id TBD)   Left: none (255)
```

Role: punishes the player for clumping while crossing the open ground toward Barich.

## Positioning Plan

```text
Open desert: Barich starts at MAX distance with clear gun sightlines (the long-range duel), the two
  Knights forward as the screen, the two Archers on flanking dunes/high ground, the Black Mage mid-back.
Preserve the open geometry and long sightlines (the distance puzzle IS the fight) — do not box Barich
  in a corner where he can be reached trivially turn one.
Keep the gun stealable and Ice-Shield-absorbable; the player should have multiple valid answers (absorb,
  close, disarm), none mandatory.
Only the boss at `104`; do not over-scale the screen.
```

The desert should say: "a Templar gunner rules the open sand — soak his ice, sprint the dunes, or
snatch his gun, then put him down before the desert wears you thin."

## Implementation Checklist

- [ ] Identify Bed Desert `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify Barich + 2 Knight + 2 Archer + 1 Black Mage + player slots (NO Hydra).
- [ ] Keep win condition = "Defeat Barich" (ends on his fall); keep the open desert geometry.
- [ ] Set Barich `104` with Glacial Gun (ranged ice); confirm Ice-Shield absorb + STEAL WEAPON work.
- [ ] Equip Barich with Tier-A armor/accessory; the Glacial Gun is his Tier-A steal/drop.
- [ ] Limit Rend to the 2 Knights (cap); keep Black Mage AoE + Archer ranged chip.
- [ ] Set add levels: 2 Knight + 1 Archer + Black Mage `102`; second Archer `101`.
- [ ] Set JobLevel `8` on all active enemy slots.
- [ ] Patch via the correct layer; keep the diff inside the Bed Desert window only.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify gun + steal + win-cond.
- [ ] Install mod, test from a New Game+ save; confirm it plays as an open-desert gun-duel.

## Test Questions

- Is Barich's Glacial Gun a real long-range threat with multiple FAIR answers (Ice Shield absorb, close
  distance, Steal Weapon disarm) — never a hard lock?
- Does stealing the Glacial Gun both reward the player AND remove his ice threat (the intended line)?
- Does "Defeat Barich ends the fight" keep it a reach-and-burst race, not a cross-desert trade war?
- Is the open desert geometry preserved (long sightlines — the distance puzzle)?
- Is Knight Rend within the cap (2 sources) and the AoE Black Mage race-able?
- Is only Barich at the boss band (`104`), screen `101`-`102` — a Tier-A boss, not a spike?
- Does the loot stay consistent with his later Lost Halidom (`052`) appearance (no double-best)?

## Sources

- Game8, "Beddha Sandwaste Walkthrough (Battle 37)": roster (Barich boss + 2 Knight + 2 Archer +
  1 Black Mage; NO Hydra), objective "Defeat Barich!", recommended level ~43, 3/5 stars, deploy 5,
  desert terrain, Glacial-Gun ice + Ice-Shield-absorb tip, rewards (30,600 Gil, buried Yagyu Darkrood).
  https://game8.co/games/Final-Fantasy-Tactics/archives/553197
- Final Fantasy Wiki, "Balk Fendsor" / "Bed Desert": story/terrain context.
  https://finalfantasy.fandom.com/wiki/Balk_Fendsor
- Local: `037-chapter-4-overview.md` (job-escalation + Tier-A rare-loot rules),
  `029-monastery-vaults-1st.md`/`034` (disarm-the-boss-weapon precedent), `038-dugeura-pass.md`
  (Black Mage AoE build), and `057-lost-halidom.md` (Barich's later Tier-S endgame appearance — to be
  designed; keep loot consistent).
```
</content>
