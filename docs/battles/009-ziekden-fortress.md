# 009 - Ziekden Fortress (Fort Zeakden)

Status: ✅ implemented (v1, entry 401) — Chapter 1 COMPLETE
Chapter: 1 — **FINALE**
Battle order: Battle 10 (after Fovoham Windflats); last battle of "The Meager"
Target version: Enhanced v1.5.0
ENTD: global entry **401** (battle_entd4, local entry 17) — confirmed by composition matching
File: `entd/battle_entd4_ent.bin` (embedded; swapped only in NG+ by the code mod)

> Implemented via `tools/battle_patch.py ziekden`, which edits the embedded modded ENTD. The whole
> file is swapped only in NG+, so the edit is automatically NG+-only — a first playthrough is
> untouched. See `000-chapter-1-overview.md`.

## Original Battle

Objective:

```text
Defeat Argath!  (boss kill — the fight ends when the boss falls, not when all enemies die)
```

Player deployment:

```text
Up to 4 units, including Ramza, across a split two-zone field.
Ally: Delita fights alongside the party as a story unit.
```

Original enemy composition:

```text
1x Argath (boss)
3x Knight
2x Black Mage
```

Public walkthrough details:

```text
Recommended level: ~9 — the highest of Chapter 1; this is the climax.
Snowbound fortress: a split battlefield that forces divided deployment, like Sand Rat.
The two Black Mages are the biggest threat if left unchecked.
The enemy Knights carry Rend abilities (equipment BREAK) — the game expects the player to
  bring the Safeguard support ability to protect their gear.
Story: this is the famous Ziekden tragedy (the Tietra hostage scene and the Ramza/Delita
  rift). That sequence is scripted cutscene, not a battle mechanic.
```

Design reading:

Ziekden is **the chapter's exam and its emotional climax in one**. Mechanically it raises every
bar at once: a real **boss** with a kill-the-leader objective, the highest recommended level of
the chapter, a **split deployment** that strains your force, two **Black Mages** as the standout
damage threat, and Knights that **break your equipment** (the one fight the original explicitly
expects you to counter with Safeguard). It is meant to feel like a wall you only clear once
you've internalized everything Chapter 1 taught.

For New Game++ the identity must be: **a genuine boss fight against Argath and his Knight/mage
escort on a divided snowfield, where the boss, the mages, and the gear-breaking Knights each
demand an answer.** This is the only Chapter 1 fight that should out-tier everything before it.

## Local Data Confirmed (entry 401)

Dumped from the embedded ENTD. The TIC encounter is slightly larger than the PSX walkthroughs
say: **5 generic Knights**, not 3, plus the 2 Black Mages and the Argath boss.

```text
slot  cid    name  job          role                         action
s0    0x07   7     76 Knight    Argath — BOSS                SCALE (boss, identity preserved)
s1    0x08   8     8            Tietra — scripted hostage    LEAVE (lvl 254, disabled)
s2    0x1c   28    28           scripted cutscene actor      LEAVE (lvl 254, disabled)
s3    0x80   76    76 Knight    captain Knight               SCALE -> L102
s4    0x80   255   76 Knight    Knight                       SCALE -> L101
s5    0x80   255   76 Knight    Knight (anchor)              SCALE -> L100
s6    0x80   255   76 Knight    Knight (anchor)              SCALE -> L100
s7    0x80   255   76 Knight    Knight (anchor)              SCALE -> L100
s8    0x04   4     4            Delita — ally guest          LEAVE (runtime guest-scaler -> 100)
s9    0x81   255   80 BlackMage Black Mage                   SCALE -> L101
s10   0x81   255   80 BlackMage Black Mage                   SCALE -> L101
```

Job IDs: Knight 76, Black Mage 80 (shared with Dorter/Sand Rat). Argath is **not** a unique-job
boss like Wiegraf — his Ziekden slot is a plain Knight (job 76); his boss identity is the named-unit
link (cid 0x07 / name_id 7), which `set_slot` preserves, so the "Defeat Argath!" objective is intact.

### Boss / guest-scaler interaction (important)

Argath's slot reuses the **guest charId 0x07** (he was the player's ally earlier in Chapter 1). The
code mod's always-on `ScaleGuestsAlways` clamps guest charIds to party level — which would have
forced the boss to 100 and, worse, **broken a normal first playthrough** (vanilla boss Argath lvl 10
→ 100, unwinnable). Fixed by scaling a guest slot **only when its job == charId** (true ally guests
keep job 4/7; the Ziekden boss is re-jobbed to Knight 76). So the boss's designed level (103) stands
and the finale is safe in both NG+ and normal play.

## New Game++ Design Goal

Keep the identity:

```text
A climactic boss fight: kill Argath while his escort — gear-breaking Knights and two real
Black Mages — pressures a split party on a snowy fortress. The hardest fight of the chapter.
```

Raise the challenge by:

```text
Giving Argath a true boss kit: level +3, durable gear, a reaction that punishes focus-fire,
  so he is a deliberate centerpiece rather than a slightly bigger Knight.
Scaling the two Black Mages so their AoE is the standout threat the walkthroughs warn about.
KEEPING Rend / equipment break on the Knights (see special note) — this is the one fight where
  break is canonical AND telegraphed, so it stays as the signature "bring Safeguard" threat.
Preserving the split deployment so the player fights toward the boss from two directions.
```

### Special note — equipment break is allowed HERE (and only here)

The chapter-wide rules (see `000-chapter-1-overview.md`) forbid Knight equipment-break because
breaking an endgame party's gear is normally unfun. **Ziekden is the deliberate exception:** the
original fight is *built* around Rend and openly tells the player to bring Safeguard. Removing
it would erase the fight's defining challenge. To keep it fair at NG+ scale:

```text
Give Rend/break to only 1-2 of the 3 Knights, not all three.
Keep break to weapons/armor tiers the player can re-buy (shop gear), never unique items.
The boss Argath does NOT spam break — his threat is presence and durability, not gear denial.
```

Avoid for this battle (see overview rules):

```text
Time Mage control / Stop-lock (the pressure is damage + break, not lockdown).
Superboss unique gear on Argath (he is a Chapter 1 noble, not an endgame superboss).
Touching the scripted hostage/cutscene units or the boss's named-unit link.
Pushing generics past +2 (only the boss reaches +3).
```

## Proposed Composition (New Game++ Ziekden v1)

Keep the exact original shape: Argath + 3 Knights + 2 Black Mages. Argath is the only unit at
boss tier (`103`); the mages and the captain Knight sit at `101-102`.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | **Argath (boss)** | Argath / Knight-type | `103` | The objective. Durable centerpiece; the fight ends when he falls. |
| n | Knight (Render) | Knight | `102` | Front anchor with **Rend** — the telegraphed break threat. |
| n | Knight (Render) | Knight | `101` | Second breaker on the other zone; covers the split. |
| n | Knight | Knight | `100` | Pure anchor, NO break; bodyguards the mages/boss. |
| n | Black Mage | Black Mage | `101` | Standout AoE threat #1; punishes the approach to the boss. |
| n | Black Mage | Black Mage | `101` | Standout AoE threat #2; the pair is the real danger. |

Reasoning:

The roster is already a proper finale, so the faithful move is to **scale it and elevate the
boss**, not redesign. Argath at `103` with a durable kit and a focus-fire-punishing reaction
makes the kill-the-leader objective meaningful instead of a coin-flip. Two scaled Black Mages
preserve the "mages are the biggest threat" reading. Two of the three Knights keep Rend so the
Safeguard lesson still lands; the third is a clean anchor so break never feels total. The split
field forces the player to fight toward Argath from two sides, exactly as designed.

## Builds (final-shop quality; boss gets a distinct, non-unique kit)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Argath - Boss (Lv 103) — evasive self-healing crossbow sniper

This restores Argath's VANILLA identity: his vanilla slot equips this Knight-job unit with a
**crossbow** (vanilla `rh=78`) + Auto-Potion — a unit that's hard to hit and heals when struck.
The first re-tune mistakenly turned him into a melee Knight with Runeblade + Fundaments (no real
offense, mild Counter, only +3 levels) and he played as a passive, toothless tank. The rework below
leans all the way into the sniper archetype.

```text
Job: Knight (76) — UNCHANGED. Keeping the vanilla job preserves the "Defeat Argath!" named-unit
     link AND the runtime guest-scaler skip (it ignores his slot only because job 76 != charId 7).
     Off-job gear (crossbow/hat/clothing) is assigned via ENTD — vanilla already does exactly this.
JobLevel: 8
Brave: 90        — Mana Shield is Brave-gated, so 90 fires it on ~90% of hits (vanilla was 29)
Secondary: Aim (8) — Archer's charge-up command (PSX "Charge"): big charged crossbow shots at range
Reaction: Mana Shield (445) — routes HP damage into MP (PSX "MP Switch")
Support: Attack Boost (465) — boosts the physical (crossbow) damage; does NOT use the movement slot
Movement: Move-MP Up (494) — refuels MP each move (WotL "Manafont"); he kites every turn -> tops off

Head: Twist Headband (163)  — PA item (crossbow dmg = PA * WP)
Body: Power Sleeve / "Power Garb" (195) — PA item
Accessory: Feather Mantle / "Featherweave" cloak (234) — best buyable cloak: phys+magic evasion
Right hand: Gastrophetes (82) — best buyable crossbow (WP 10); one-handed, so a shield is legal
Left hand: Crystal Shield (139) — best buyable shield; high evasion
```

Role: the centerpiece, reworked into a frustrating attrition boss. Survival rides on DOUBLE evasion
(Crystal Shield + Feather Mantle) so most attacks whiff; what lands is routed into MP by Mana Shield,
and Move-MP Up refills that MP buffer as he kites at crossbow range 4. Offense is real this time:
max PA (Headband + Power Sleeve + Attack Boost) * a WP-10 crossbow, with Aim landing heavy charged
shots from afar. Strong and annoying, but pointedly NOT a superboss — and every piece is non-unique
shop gear.

Trade-offs / playtest watch-items (all approved by design):
- The accessory is the cloak (evasion), NOT Bracer (+3 PA) — chosen to maximize "hard to hit," so
  crossbow damage is a touch lower than a Bracer build.
- Mana Shield's buffer scales with Max MP, and a Knight's MP is low; big single hits will still spill
  into HP. Move-MP Up only tops off what the small pool can hold. Verify he feels durable-but-killable,
  not either trivial or unkillable.
- Off-job: confirm in-game that the Knight-job Argath actually fires the crossbow's ranged Attack and
  that Aim charges/fires correctly. (Vanilla already equips him a crossbow, so this is expected to work.)
- We could NOT force the Auto-Potion X-Potion tier via ENTD (engine picks the lowest available potion),
  which is why the survival package is Mana Shield + Move-MP Up instead of Auto-Potion.

### Knight (Render) x2 (Lv 102 / 101)

```text
Job: Knight (id TBD)   JobLevel: 8   Secondary: the Knight break command (Rend, id TBD)
Reaction: Counter (442)
Support: Attack Boost (465)
Movement: Movement +1 (486)

Head: shop heavy helm (id TBD)
Body: shop heavy armor (id TBD)
Accessory: Bracers (218)
Right hand: Runeblade (30) or Icebrand (29)
Left hand: shop shield (id TBD)
```

Role: the telegraphed break threat. They threaten the player's weapons/armor — bring Safeguard
or lose gear, exactly as the original taught. Two of them, on opposite zones.

### Knight (Anchor) x1 (Lv 100)

```text
Job: Knight (id TBD)   JobLevel: 8   Secondary: none (NO break)
Reaction: Counter (442)
Support: Attack Boost (465)
Movement: Movement +1 (486)

Gear: same shop heavy kit as above.
```

Role: a clean wall that bodyguards the mages and Argath, so break never covers the whole field.

### Black Mage x2 (Lv 101)

```text
Job: Black Mage (id TBD)   JobLevel: 8   Secondary: none
Reaction: Reflexes (449) or a magic-defensive reaction (id TBD)
Support: MA/Magick-boost support if available (id TBD)
Movement: Movement +1 (486)

Head: cloth/mage hat (id TBD)
Body: shop robe (e.g. Black Robe / Light Robe-tier, id TBD)
Accessory: Featherweave Cloak (234) or magic-defensive accessory (id TBD)
Right hand: shop rod/staff that boosts magic (id TBD)
Left hand: none (255)
```

Role: the biggest threat, per the walkthroughs. At party level their Fire/Ice/Thunder AoE
genuinely punishes the approach to Argath; the player must close or silence them fast.

## Positioning Plan

```text
Argath starts deep in the fortress, central to both zones — the player fights inward to reach him.
One Render-Knight anchors each zone's approach so both halves of the split party meet a breaker.
The clean Anchor-Knight starts near Argath / the mages as a bodyguard wall.
Both Black Mages start behind the Knight line with sightlines over the two approach lanes,
  so their AoE covers the kill zone while the Knights stall.
Preserve the two player deployment zones and Delita's ally placement.
```

The map should read as a climactic assault: two fronts, gear under threat, mages raining AoE,
and a durable boss waiting at the center.

## Implemented (v1, entry 401)

Applied with `python tools/battle_patch.py ziekden`; diff contained to local entry 17 (global 401),
83 bytes. Faithful to the design, with one data-driven adjustment: the TIC encounter has **5 Knights**
(not 3), so all five are scaled (captain L102, one L101, three anchors L100) rather than inventing a
roster. Argath is the only +3 unit (L103); both Black Mages L101.

```text
s0  Argath BOSS  L103 jl8  sec Fundaments(5)  R Counter  S Atk-Boost  M +1  HeavyHelm/Armor/Bracers + Runeblade + Shield
s3  Knight       L102 jl8  R Counter  S Atk-Boost  M +1  heavy shop kit + Runeblade + Shield
s4  Knight       L101 jl8  (same kit)
s5  Knight       L100 jl8  (same kit)
s6  Knight       L100 jl8  (same kit)
s7  Knight       L100 jl8  (same kit)
s9  Black Mage   L101 jl8  R Reflexes  M +1  Mage Hat / shop Robe / Featherweave + shop Rod
s10 Black Mage   L101 jl8  (same kit)
```

**Deferred — Rend / equipment break:** the doc's signature "bring Safeguard" threat (Rend on 2 of the
Knights) is NOT yet applied — it needs the verified Knight **Battle-Skill** secondary-skillset id,
which isn't decoded yet. The Knights currently run no secondary command. This is the one safe-to-add
flavor tweak left for Ziekden; everything else (scaling, boss, mages, identity, NG+-gating) is done.

## Implementation Checklist

- [x] Identify Ziekden ENTD entry (401) on Windows data; fill "Local Data Confirmed".
- [x] Dump original entry; verify Argath + Knights + 2 Black Mage + scripted/ally slots.
- [x] Confirm Argath's named-unit link and DO NOT break boss/cutscene scripting (identity bytes kept).
- [x] Confirm Black Mage job/equipment. (Knight Rend command id still TBD — see Deferred above.)
- [x] Map shop-tier heavy armor / shield / robe / rod item IDs in `ItemData.xml`.
- [x] Set levels: Argath `103`; captain Knight `102`; `101`; anchors `100`; mages `101`.
- [x] Set JobLevel `8` on all active enemy slots.
- [ ] Give Rend to 2 Knights (deferred — needs Battle-Skill skillset id). Argath has Fundaments + Counter. ✅
- [x] Equip per builds (all non-unique / shop-tier, including the boss).
- [x] Preserve scripted hostage/cutscene units (s1/s2 lvl 254) and Delita guest (s8).
- [x] Patch the embedded ENTD (NG+-only by construction); diff inside entry 401 only.
- [x] Re-dump and diff; confirm changes are small and intentional; boss identity link intact.
- [ ] Install mod, test from a New Game+ save; confirm the kill-Argath objective still ends it (playtest).

## Test Questions

- Is this clearly the hardest fight of Chapter 1 — a real step above Dorter?
- Does Argath feel like a boss (durable, punishes dogpiling) without being a superboss wall?
- Do the two Black Mages read as the top threat, as the walkthroughs say?
- Does keeping Rend on 2 Knights preserve the "bring Safeguard" challenge without feeling cheap?
- Does the split field force a genuine two-front assault toward the boss?
- Does the kill-the-leader objective still trigger correctly (fight ends on Argath's defeat)?
- Is the scripted Tietra/Delita story sequence completely intact and unaffected?
- Does it still feel like the Ziekden climax, not a generic boss arena?

## Sources

- Game8, "Ziekden Fortress Walkthrough (Chapter 1 finale)": roster (3 Knight, 2 Black Mage,
  boss Argath), objective "Defeat Argath!", split two-zone field, deploy 4, recommended
  level ~9, Black Mages as the biggest threat, enemy Knights' Rend / Safeguard counter.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553171
- StrategyWiki / Final Fantasy Wiki, "Fort Zeakden / Ziekden Fortress": boss Algus/Argath,
  Delita ally, the Tietra hostage tragedy (scripted story), snowbound split battlefield.
  https://strategywiki.org/wiki/Final_Fantasy_Tactics
- Local: `docs/battles/000-chapter-1-overview.md` (design rules + the break exception),
  `004-dorter-slums.md` (Black Mage + Knight builds), `005-sand-rat-sietch.md` (split-field
  handling), `001-gariland.md` (confirmed item/skill IDs).
</content>
