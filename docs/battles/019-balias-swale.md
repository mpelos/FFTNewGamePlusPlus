# 019 - Balias Swale (Bariaus Valley)

Status: ✅ implemented (v1, entry 413) — Geomancer add deferred; Agrias auto-scaled
Chapter: 2 — "The Manipulator and the Subservient"
Battle order: Battle 18 (after Goug Lowtown)
Target version: Enhanced v1.5.0
ENTD: global entry **413** (battle_entd4, local entry 29) — confirmed by composition + Agrias guest
File: `entd/battle_entd4_ent.bin` (embedded; swapped only in NG+ by the code mod)

> Implemented via `tools/battle_patch.py balias_swale`, plus a Program.cs change adding Agrias (cid
> 0x1e) to the runtime guest-scaler. NG+-only enemy edits. See `011-chapter-2-overview.md`.

## Original Battle

Objective:

```text
Save Agrias!  (she must survive — losing her fails the battle and the recruit)
```

Player deployment:

```text
Up to 5 units, including Ramza — across a SPLIT-team deployment.
Ally: Agrias is the protected guest. She can hold her own but starts OUTNUMBERED and isolated;
  she becomes a permanent party member after this battle.
```

Original enemy composition:

```text
1x Knight
2x Archer
2x Black Mage   (Thunder — amplified by the rain)
```

Public walkthrough details:

```text
Recommended level: ~20 (2/5 stars on paper).
Rainy valley/swale; RAIN BOOSTS THUNDER damage (both sides).
The Black Mages are the primary threat — rain-boosted Thunder hurts.
Enemies start on the FAR END; the player needs ranged units or Movement 4+ to reach them and
  to relieve the isolated, outnumbered Agrias quickly.
Split your forces: mix mages and physical attackers across the two teams.
```

Design reading:

Balias Swale is a **split-team race to relieve an outnumbered VIP in the rain**. It braids three
earlier ideas — Sand Rat's split deployment, Zeirchele's protect-the-guest, and the rain-Thunder
gimmick — into one: Agrias is stranded and outgunned on the far side, and the player must split
their force and **close distance fast** before the rain-boosted Black Mages and Archers wear her
down. It teaches split-team coordination, mobility (Move 4+), and respecting weather (Thunder
cuts both ways).

For New Game++ the identity must stay: **a rainy split-team rush to save an isolated, outnumbered
Agrias from a ranged firing line whose Thunder the weather amplifies — distance and tempo are the
whole fight.**

## Local Data Confirmed (entry 413)

```text
slot  cid    flags  job        role                       action
s0    0x1e   0x50   30 (==cid) Agrias (Save-Agrias VIP)   AUTO-SCALED (GuestCharIds, not here)
s1    0x80   0x80   76 Knight  frontline body             SCALE -> L101
s2    0x81   0x40   77 Archer  far-end ranged             SCALE -> L101
s3    0x81   0x40   77 Archer  far-end ranged             SCALE -> L100
s4    0x80   0x80   76 Knight  frontline body             SCALE -> L100
s5    0x80   0x80   80 BMage   rain-Thunder (primary)     SCALE -> L101
s6    0x80   0x80   80 BMage   rain-Thunder (primary)     SCALE -> L101
```

Job IDs: Knight 76, Archer 77, Black Mage 80, Agrias's Holy-Knight job 30. (TIC has 2 Knights vs the
walkthrough's 1.) The Knights run job 76 at jl8, so they carry Battle Skill (Rend) innately — a minor
extra over this doc's "no break" preference, not suppressible without changing the job; non-blocking.

### Agrias (VIP) — auto-scaled, not patched here

Agrias (**cid 0x1e, job 30 == cid**) is the "Save Agrias!" objective unit — isolated, outnumbered,
and her death FAILS the battle; she joins permanently right after. She was added to `GuestCharIds`
in Program.cs, so the runtime guest-scaler keeps her at party level (job==cid guarded) and the
rescue is viable in NG+. Her slot is not touched here, only auto-scaled at read time. The RAIN flag
and split-team zones are map/terrain data (not in the ENTD slots), so they are untouched.

## Job Escalation (Chapter 2 rule)

```text
CHANGE: add ONE Geomancer (marsh-themed mid-range elemental attacker).
WHY: the swale is a wet valley — a Geomancer whose Geomancy draws on the terrain (water/marsh
  tiles) fits perfectly and adds a NEW ranged elemental angle that pressures the player's crossing
  and the isolated Agrias. It deepens the existing challenge (close distance under ranged fire)
  rather than changing it, and makes Agrias a touch more outnumbered — exactly the fight's premise.
  Single new wrinkle; Geomancer debut.
WHAT IS NOT CHANGED: the 1 Knight + 2 Archers + 2 rain-Thunder Black Mages keep the firing-line
  identity; the strategy ("split, rush to Agrias, manage rain-Thunder") still holds.
```

## Boss rare loot

```text
None. No named boss here — no rare item (per the Chapter 2 overview). Generics stay shop-tier.
```

## Proposed Composition (New Game++ Balias Swale v1)

Keep the original firing line and add one Geomancer (6 enemies). The Black Mages, lead Archer,
and Geomancer at `101`; the Knight and second Archer at `100`–`101`.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Knight | Knight | `101` | The lone frontline body; contests the player's crossing. |
| n | Archer | Archer | `101` | Far-end ranged pressure on Agrias and the rush. |
| n | Archer | Archer | `100` | Second bow; covers the other approach lane. |
| n | Black Mage | Black Mage | `101` | Rain-boosted Thunder — the primary threat. |
| n | Black Mage | Black Mage | `101` | Second Thunder caster; punishes a clumped rush. |
| n | Geomancer (NEW) | Geomancer | `101` | Marsh-terrain elemental at mid-range — the new pressure on the crossing. |

Reasoning:

The faithful move is to **scale the firing line, keep the rain-Thunder headline, and add one
terrain-flavored threat**. Two rain-boosted Black Mages stay the main danger to Agrias; the
Archers keep the far-end ranged pressure; the lone Knight gives the player a body to fight
through. The added Geomancer fits the wet valley and makes the crossing — already the hard part —
a little deadlier, nudging Agrias further into "outnumbered" without changing the rush-to-relieve
plan. The split-team and weather lessons stay central.

## Builds (final-shop quality; valley garrison flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Knight (Lv 101)

```text
Job: Knight (id TBD)   JobLevel: 8   Secondary: none (NO Break)
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head/Body: shop heavy helm + heavy armor (ids TBD)
Accessory: Bracers (218)   Right hand: Runeblade (30)   Left hand: shop shield (id TBD)
```

Role: the frontline body the player must get past on the way to relieve Agrias.

### Archer x2 (Lv 101 / 100)

```text
Job: Archer (77)   JobLevel: 8   Secondary: none
Reaction: Reflexes (449)   Support: Concentration (469)   Movement: Movement +1 (486)
Head: Thief's Cap (168)   Body: Black Garb (198)   Accessory: Bracers (218)
Right hand: Windslash Bow (87)  (a Lightning/Thunder bow is thematic in rain — id TBD)
Left hand: none / two-hand marker (254)
```

Role: far-end ranged pressure that wears on the isolated Agrias.

### Black Mage x2 (Lv 101) — rain-Thunder

```text
Job: Black Mage (id TBD)   JobLevel: 8   Secondary: none
Reaction: Reflexes (449)   Support: MA/Magick-boost (id TBD)   Movement: Movement +1 (486)
Head: cloth/mage hat (id TBD)   Body: shop robe (id TBD)
Accessory: Featherweave Cloak (234)   Right hand: shop magic-boost rod (id TBD)   Left: none (255)
Note: lean into Thunder so the rain amplification is the headline threat (player can exploit it too).
```

Role: the primary danger. Rain-boosted Thunder punishes a clumped rush and the exposed VIP.

### Geomancer (Lv 101) — NEW (job add)

```text
Job: Geomancer (id TBD)   JobLevel: 8   Secondary: none (innate Geomancy)
Reaction: Counter (442) or a defensive reaction (id TBD)
Support: Attack Boost (465)   Movement: Movement +1 (486)
Head: shop hat (id TBD)   Body: shop light armor / robe-tier the job allows (id TBD)
Accessory: Bracers (218)   Right hand: a shop sword/rod the job allows (id TBD)   Left: none/shield
```

Role: marsh-terrain elemental at mid-range — a new angle on the crossing that fits the wet valley.

## Positioning Plan

```text
The firing line (2 Archers + 2 Black Mages + Geomancer) starts on the FAR END, with sightlines
  to Agrias's isolated position, so distance is the core problem.
The Knight starts forward of the casters as the body the player must fight through.
Agrias starts isolated/outnumbered on the far side; the player's split teams start apart and must
  converge to relieve her.
Preserve the split-team zones, Agrias's protected slot, and the RAIN flag.
```

The valley should say: "your VIP is stranded under a rain-charged firing line — split up, close
fast, and use the weather before it's used on you."

## Implemented (v1, entry 413)

Applied with `python tools/battle_patch.py balias_swale`; diff contained to local entry 29 (global
413), 62 bytes. Knights L101/L100, Archers L101/L100, Black Mages L101; JobLevel 8 on all.

```text
s1  Knight   L101 jl8  R Counter  S Atk-Boost  M +1  heavy shop kit + Runeblade + Shield
s4  Knight   L100 jl8  (same kit)
s2  Archer   L101 jl8  R Reflexes  S Concentration  M +1  Thief's Cap / Black Garb / Bracers + Windslash Bow
s3  Archer   L100 jl8  (same kit)
s5  BMage    L101 jl8  R Reflexes  M +1  Mage Hat / shop Robe / Featherweave + shop Rod  (rain-Thunder)
s6  BMage    L101 jl8  (same kit)
```

**Deferred — Geomancer escalation (slot-add).** The doc's wrinkle adds a Geomancer (first use of the
job), which needs a verified map position; batched for the playtest pass.

## Implementation Checklist

- [x] Identify Balias Swale ENTD entry (413); fill "Local Data Confirmed".
- [x] Dump original entry; verify Knights + Archers + Black Mages + Agrias.
- [x] Confirm Knight / Black Mage / Archer job IDs and legal equipment.
- [ ] Add the Geomancer slot (deferred — needs a verified map position; do during playtest).
- [x] Set levels: Knights `101`/`100`; Archers `101`/`100`; both Black Mages `101`.
- [x] Set JobLevel `8` on all scaled slots; Black Mages lean on Thunder (rain-amplified).
- [x] Agrias auto-scaled via GuestCharIds (cid 0x1e); slot/scripting and RAIN/split terrain untouched.
- [x] Patch the embedded ENTD (NG+-only); diff inside entry 413 only.
- [x] Re-dump and diff; changes small and intentional.
- [ ] Playtest from a NG+ save; confirm Save-Agrias + split work; verify Agrias scales.

## Test Questions

- Is relieving the isolated, outnumbered Agrias tense but achievable with a fast split-team rush?
- Are the rain-boosted Black Mages the clear primary threat (and can the player exploit Thunder too)?
- Does the added Geomancer make the crossing deadlier without making Agrias's survival impossible?
- Does the split-team deployment still force genuine two-front coordination?
- Does it read as a distinct fight (rainy VIP-rescue) vs the other split/escort battles?
- Is it a fair step (later in the chapter) but below the Gaffgarion/Cúchulainn bosses?

## Sources

- Game8, "Balias Swale Walkthrough (Battle 18)": objective "Save Agrias!", roster (1 Knight,
  2 Archer, 2 Black Mage), recommended level ~20, rain boosts Thunder, enemies on the far end,
  split-team deploy 5, Agrias outnumbered guest who becomes permanent after.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553178
- Final Fantasy Wiki, "Bariaus Valley" / "Agrias Oaks": story/terrain context.
  https://finalfantasy.fandom.com/wiki/Bariaus_Valley
- Local: `docs/battles/011-chapter-2-overview.md` (job-escalation rule), `005-sand-rat-sietch.md`
  (split-team handling), `006-brigands-den.md` (rain-Thunder gimmick), `014-zeirchele-falls.md`
  (protect-the-guest).
</content>
