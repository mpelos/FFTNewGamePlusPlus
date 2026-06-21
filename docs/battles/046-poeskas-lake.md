# 046 - Lake Poescas (Poeskas Lake)

Status: ✅ implemented (v1, entry 453)
Chapter: 4 — "In the Name of Love"
Battle order: Battle 41 (after Mount Germinas)
Target version: Enhanced v1.5.0
ENTD: global entry **453** (local 69, entd4)
File: `battle_entd4_ent.bin`

## Implemented (v1, entry 453)

```text
DATA REALITY (verified from entd4 dump + JobData.xml):
  Entry 453 sits exactly between Germinas (452) and the Limberry assassin chain (454 Celia/Lettie,
  455 Elmdor) -> confirmed Poeskas by story position. Every slot is a MONSTER undead (eq=254, no
  equip slots) -- NOT human Archer/Mystic/Summoner as Game8 loosely describes.
    slots 0,3 = job 70/71  "Float, Undead" floaters
    slots 1,2 = job 63     "Float, Undead" floaters
    slots 4,5 = job 114    Revenant family (InnateStatus: Undead)  -- the reraising bodies
  All six are innately UNDEAD -> the reraise permakill war is intact at the data level.

CHANGE (faithful, minimal): SCALE the band to the endgame curve (101-103) -- nothing else.
  slot 4 Revenant = 103 (anchor)   slot 5 Revenant = 102
  slots 0,3 floaters = 102          slots 1,2 floaters = 101
  Monsters: LEVEL only set; job / undead innates / (empty) equipment / scripting all untouched.

WHY no "swap Archer -> Mystic" escalation: the doc's planned escalation assumed human jobs. The
  actual roster is all-monster, so there are no humans to escalate and changing a monster's job would
  break its undead/reraise innate. The 5* identity (reraise permakill puzzle vs a mixed undead band)
  is already in the data; the only NG+ need is to bring it to the endgame level band. No boss, no rare
  (per Ch4 overview tiering); buried treasure + Phoenix Down spoils left as map loot.
```

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `037-chapter-4-overview.md`.

## Original Battle

Objective:

```text
Defeat all enemies!   (and make them STAY dead — every foe is undead and reraises)
```

Player deployment:

```text
Up to 5 units, including Ramza. No guests.
```

Original enemy composition (verified via Game8, Battle 41):

```text
2x Revenant   (undead melee — reraise)
2x Archer     (undead — ranged chip)
1x Mystic     (undead — soft status)
1x Summoner   (undead — AoE)
ALL six enemies are UNDEAD.
```

Public walkthrough details:

```text
Recommended level: ~59.  Difficulty: 5/5 stars (the hardest skirmish of the chapter).  Deploy up to 5.
Win: defeat all enemies — but EVERY enemy is UNDEAD and has a chance to RERAISE when its heart counter
  hits zero (resurrect instead of crystallizing). You must kill them FOR GOOD.
THE ANSWER: PHOENIX DOWN instantly one-shots an undead enemy (Chemists are MVPs); Holy Sword (Agrias/
  Orlandeau) ignores elevation and hits the undead hard; Holy/Seal Evil permakill methods.
Lake terrain. The band mixes melee reraisers (Revenants), ranged (Archers), status (Mystic), and AoE
  (Summoner) — all undead.
Rewards: 30,400 Gil, Phoenix Down x2, buried (Platinum Helm/Armor, Cashmere, Circlet, etc.).
```

Design reading:

Lake Poescas is **the all-undead permakill war** — the chapter's lone 5/5★ skirmish. There is no
boss; the difficulty is the **reraise mechanic applied to a full, dangerous band**: melee Revenants,
ranged Archers, a status Mystic, and an AoE Summoner, *all undead, all able to come back*. Chipping
them down doesn't work — they get up. The whole identity is **bring permakill tools** (Phoenix Down
instakill, Holy damage, Seal Evil) **and end each undead for good while surviving a mixed-threat
band**. It's the dark mirror of Ch3's Yuguewood (`032`), escalated: there a few undead among casters;
here *everything* is undead and the star rating reflects it.

For New Game++ the identity must stay: **a 5★ all-undead lake fight whose whole demand is the reraise
permakill puzzle (PD / Holy / Seal Evil) against a mixed melee/ranged/status/AoE undead band — kept
boss-less and rare-less, but genuinely the hardest skirmish, sharpened by one undead sustain-caster
that makes "kill them for good" matter more.**

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm slots: 2 Revenant + 2 Archer + 1 Mystic + 1 Summoner, ALL flagged UNDEAD, plus player slots.
Keep EVERY enemy UNDEAD + the RERAISE-on-heart-zero behavior (the permakill puzzle IS the fight) and
  the undead weaknesses (Phoenix Down = instakill; Holy = heavy damage). Keep the lake terrain.
This is a no-boss, no-rare 5-star skirmish: keep enemy band scale-to-party (101-103); the reraise
  mechanic + mixed threats carry the 5★, NOT a level spike (rec ~59 is the player's curve).
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
Leave the buried treasure (Platinum Helm/Armor, etc.) + Phoenix Down spoils as-is — map loot.
```

Job IDs (carry over known, verify the rest in-game):

```text
77 = Archer            (confirmed)
Revenant id            (TBD - verify; undead melee)
Mystic / Oracle id     (TBD - verify; soft-status caste)
Summoner job id        (TBD - verify)
(all enemy slots flagged UNDEAD)
```

## Job Escalation (Chapter 4 rule)

```text
CHANGE: swap ONE Archer -> a second (undead) MYSTIC that DARK-HEALS the undead band (Dark element heals
  undead) and adds soft status.
WHY: the fight's identity is "permakill a reraising undead band." The single, fitting escalation is to
  add an undead sustain-caster: Dark-element healing on undead allies + the reraise means chipping is
  even more futile, so the player MUST bring true permakill tools (PD / Holy). It INTENSIFIES the
  reraise puzzle without changing it — and it stays fair because the answers BYPASS sustain entirely
  (Phoenix Down one-shots regardless of healing; Holy burns through). The remaining Archer keeps ranged.
CONSTRAINT (carry Ch3 Yuguewood precedent, 032): undead reraise + heal-weakness/PD-instakill preserved
  AS counterplay; mass-status capped to ONE disruptor (the Mystic), soft/resistable, no hard lock.
WHAT IS NOT CHANGED: the all-undead band, the reraise mechanic, the Revenant melee, the Summoner AoE,
  and the lake terrain remain. No boss, no rare. Still a skirmish — the hardest one.
```

## Sanctioned exceptions (carried precedents)

```text
UNDEAD RERAISE — preserved as the core mechanic AND its own counterplay (PD instakill / Holy / Seal
  Evil / Entice), exactly as Ch3 Yuguewood (032). The challenge is permakill, not an unavoidable loop.
DARK-HEAL ON UNDEAD (Mystic) — allowed: Dark element heals undead allies; fair because the player's
  permakill answers (PD/Holy) ignore it. Sustain, not a lock.
MYSTIC SOFT STATUS — ONE disruptor only (one-disruptor mass-status cap); soft, resistable, no hard lock.
SUMMONER AoE — mid-tier, INTACT charge times, race-able (028). Not new.
```

## Boss rare loot

```text
None. No named boss here — no rare boss item (per the Chapter 4 overview tiering). Generics stay
Chapter-4 shop-tier. The buried treasure (Platinum Helm/Armor, etc.) + Phoenix Down spoils are EXISTING
map loot — leave as-is.
```

## Proposed Composition (New Game++ Lake Poescas v1)

Keep the count (6) and the all-undead 5★ feel; swap one Archer for an undead Dark-heal Mystic. Band
`101`–`103` (the reraise + mixed threats carry the star rating). One `103` anchor on a Revenant.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Revenant (undead) | Revenant | `103` | Reraising melee — the body that won't stay down. |
| n | Revenant (undead) | Revenant | `102` | Second reraiser — forces true permakill tools. |
| n | Summoner (undead) | Summoner | `102` | AoE pressure while the band reraises. |
| n | Mystic (undead) | Mystic | `102` | Soft status (one disruptor) + threat to the player. |
| n | Mystic (undead, NEW) | Mystic | `101` | Dark-heals the undead band — the escalation. |
| n | Archer (undead) | Archer | `101` | Ranged chip; the lone ranged body. |

Reasoning:

The faithful move is to **make the reraise war the whole fight and add one sustain twist**. Two
Revenants anchor the "won't stay dead" core; the Summoner pressures with AoE; one Mystic disrupts with
soft status; the swapped-in second Mystic Dark-heals the undead so chipping is hopeless — the player
*must* bring Phoenix Down / Holy / Seal Evil to end each foe for good. The lone Archer keeps a ranged
threat. Levels stay in-band (`101`–`103`, one `103` anchor) so the 5★ comes from the reraise mechanic
and the mixed band, not a number spike — exactly the original's identity, sharpened.

## Builds (Chapter-4 quality; drowned-dead lake flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Revenant x2 (Lv 103 / 102) — reraisers (monsters)

```text
Monster: Revenant (id TBD)   UNDEAD flag ON; reraise-on-heart-zero behavior intact.
Innate undead skillset (drain touch / status bite). No equipment slots (monster).
Set only LEVEL + UNDEAD flag. Weak to Holy; Phoenix Down = instakill.
```

Role: the melee bodies that keep getting up; permakill them (PD/Holy) or they return.

### Summoner (undead, Lv 102) — AoE

```text
Job: Summoner (id TBD)   JobLevel: 8   UNDEAD flag ON   Secondary: none
Mid-tier summons, INTACT charge times (race-able).
Reaction: Reflexes (449)   Support: MA-boost (id TBD)   Movement: Movement +1 (486)
Body: shop robe (id TBD)   Accessory: Featherweave Cloak (234)   Right: magic-boost rod (id TBD)
```

Role: AoE pressure while the band reraises; race-able, but undead (PD/Holy ends it for good).

### Mystic x2 (undead, Lv 102 / 101) — status + Dark-heal (one NEW)

```text
Job: Mystic / Oracle (id TBD)   JobLevel: 8   UNDEAD flag ON
Mystic #1: soft status (ONE disruptor; no hard lock).
Mystic #2 (NEW): DARK-element healing on undead allies (the sustain escalation) + light soft status.
Reaction: Reflexes (449)   Support: MA-boost (id TBD)   Movement: Movement +1 (486)
Body: shop robe (id TBD)   Accessory: Featherweave Cloak (234)   Right: magic-boost rod (id TBD)
```

Role: keep the band alive (Dark-heal) and disrupt the player (one soft-status source) — both bypassed
by the player's permakill answers.

### Archer (undead, Lv 101) — ranged

```text
Job: Archer (77)   JobLevel: 8   UNDEAD flag ON   Secondary: none
Reaction: Reflexes (449)   Support: Concentration (469)   Movement: Movement +1 (486)
Head: Thief's Cap (168)   Body: Black Garb (198)   Accessory: Bracers (218)
Right hand: shop high-tier bow (id TBD)   Left: none / two-hand marker (254)
```

Role: the lone ranged body; chips while the melee reraises.

## Positioning Plan

```text
Lake terrain: spread the undead so the player can't AoE the whole band into one permakill — the two
  Revenants press from the water's edge, the Summoner back with AoE sightlines, the two Mystics
  central (Dark-heal range to the band + status range to the player), the Archer on a flank.
Preserve the lake geometry + every UNDEAD flag + the reraise behavior (the permakill puzzle IS the fight).
Keep it in-band level-wise; the 5★ comes from reraise + sustain + mixed threats, not a number spike.
Ensure the player's answers (PD instakill / Holy / Seal Evil) remain decisive — no unkillable loop.
```

The lake should say: "the drowned dead won't lie still — bring fire that ends them for good, or they
rise from the water again and again."

## Implementation Checklist

- [ ] Identify Lake Poescas `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify 2 Revenant + 2 Archer + 1 Mystic + 1 Summoner, ALL undead, + player slots.
- [ ] Swap ONE Archer -> a second (undead) Mystic with Dark-heal-on-undead + light soft status.
- [ ] Keep every enemy UNDEAD + reraise-on-heart-zero + Holy weakness + PD-instakill.
- [ ] Cap mass-status to ONE disruptor (Mystic #1); keep Summoner charge times intact.
- [ ] Set levels in-band (`101`-`103`, one `103` Revenant anchor); JobLevel `8` on job slots.
- [ ] Patch via the correct layer; keep the diff inside the Lake Poescas window only.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify undead flags + reraise intact.
- [ ] Install mod, test from a New Game+ save; confirm the permakill puzzle (PD/Holy) is decisive, no loop.

## Test Questions

- Does the reraise mechanic still define the fight (chipping fails; PD/Holy/Seal Evil permakill is the
  answer) — and is that answer always decisive (no unkillable loop)?
- Does the new Dark-heal Mystic sharpen "kill them for good" WITHOUT being a hard lock (PD bypasses it)?
- Is mass-status capped to one soft disruptor (no hard lock)?
- Are levels kept in-band (101-103) so the reraise + mixed band — not a number spike — earn the 5★?
- Is it clearly the hardest SKIRMISH of the chapter, the dark mirror of Yuguewood (032)?
- Does it read as a drowned-dead lake that won't stay dead, not a designed arena?

## Sources

- Game8, "Lake Poescas Walkthrough (Battle 41)": roster (2 Revenant + 2 Archer + 1 Mystic + 1 Summoner,
  all undead), "Defeat all enemies!", rec ~59, 5/5 stars, deploy 5, undead reraise + Phoenix-Down-
  instakill + Chemist/Holy tips, rewards (30,400 Gil, Phoenix Down x2, buried Platinum Helm/Armor etc.).
  https://game8.co/games/Final-Fantasy-Tactics/archives/553201
- Final Fantasy Wiki, "Poeskas Lake": story/terrain context.
  https://finalfantasy.fandom.com/wiki/Poeskas_Lake
- Local: `037-chapter-4-overview.md` (rules), `032-yuguewood.md` (Ch3 undead precedent this escalates).
```
</content>
