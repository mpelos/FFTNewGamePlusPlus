# 014 - Zeirchele Falls (Zirekile Falls)

Status: ✅ implemented (v1, entry 405) — Knight→Archer escalation done inline; Ovelia survival = JOB-INNATE Mana Shield + Manafont (Princess job 12 via FFTIVC/tables/enhanced/JobData.xml) layered over gear Always-Protect (Sortilège) + Brave 61 (2026-06-28; earlier evasion + ENTD-R/S/M passes both failed — see "Ovelia survivability"). ✅ CONFIRMED in-game 2026-06-28 — Mana Shield + Move-MP Up both active.
Chapter: 2 — "The Manipulator and the Subservient"
Battle order: Battle 13 (after Araguay Woods)
Target version: Enhanced v1.5.0
ENTD: global entry **405** (battle_entd4, local entry 21) — confirmed by sequence + composition
File: `entd/battle_entd4_ent.bin` (embedded; swapped only in NG+ by the code mod)

> Implemented via `tools/battle_patch.py zeirchele`. NG+-only by construction. See
> `011-chapter-2-overview.md`.

## Original Battle

Objective:

```text
Save Princess Ovelia!  (she must survive the battle — her death is a failure/Game Over)
```

Player deployment:

```text
Up to 4 units, including Ramza.
Allies: Agrias joins here and fights alongside the party. Ovelia hangs back and casts
  defensive magic (Aegis/Shell-type); she is the unit the player must protect.
Note: Gaffgarion starts as a party ally, then BETRAYS mid-battle and turns enemy.
```

Original enemy composition:

```text
1x Gaffgarion (Dark Knight / Fell Knight — betrayer; RETREATS at low HP, not killed here)
5x Knight
```

Public walkthrough details:

```text
Recommended level: ~13.
Riverside map: a bridge crossing water, with elevation changes on the banks.
Gaffgarion's betrayal is the story beat; he uses HP-draining dark sword skills (Drain/
  Shadowblade-type) and his power lives in his weapon.
Canonical tip: STRIP Gaffgarion's equipment while he is still your ally (formation screen)
  so his attacks are far weaker once he turns — his threat is gear-dependent.
He retreats after taking enough damage — you do NOT have to defeat him outright.
The Knights press toward Ovelia; protecting her is the whole battle.
```

Design reading:

Zeirchele is **the betrayal fight and the chapter's first big escort-defense**. The drama is
Gaffgarion flipping from ally to enemy, but the *mechanics* are: keep **Ovelia** alive while a
Knight wall pushes toward her and a draining Dark Knight pressures your line. It teaches the
player to **defend a fixed, fragile VIP** across a bridge chokepoint, and rewards prep (stripping
Gaffgarion's gear neuters him). Agrias arriving gives the player a strong sword-skill ally to
offset the loss of Gaffgarion.

For New Game++ the identity must stay: **a tense VIP-defense on a riverbank where a betraying,
gear-dependent Dark Knight and his Knight escort drive at Princess Ovelia — protect her, exploit
the strip-his-gear counter, and lean on Agrias.**

## Local Data Confirmed (entry 405)

```text
slot  cid    name  flags  job        role                          action
s0    0x05   5     0x80   5          Gaffgarion (betrayer, ENEMY)  SCALE -> L103 (job/sec kept)
s1    0x0c   12    0x51   12         Ovelia (VIP ally)            EQUIP survival kit; lvl via scaler->100
s2    0x80   255   0x80   76 Knight  reinforcement (lvl 254)       LEAVE (spawn scripting)
s3    0x80   255   0x80   76 Knight  reinforcement (lvl 254)       LEAVE (spawn scripting)
s4    0x80   255   0x80   76 Knight  escort wall (lead)            SCALE -> L101
s5    0x80   255   0x80   76 Knight  escort wall                   SCALE -> L101
s6    0x80   255   0x80   76 Knight  escort wall                   SCALE -> L100
s7    0x80   255   0x80   76 Knight  escort wall                   SCALE -> L100
s8    0x80   255   0x80   76 Knight  -> ARCHER (escalation swap)   SCALE -> L101, re-job 77
s9    0x17   23    0x88   23         Agrias (ally, lvl 254)        LEAVE
s10   0x34   52    0x49   52         named story unit (lvl 254)    LEAVE
```

Gaffgarion is on the **enemy team** (flags 0x80) in the base ENTD; his ally→betray phase is pure
scripting. Scaling him is therefore safe regardless of the exact named-unit mapping, and `set_slot`
preserves his identity bytes. **Job 5 = his dark-sword skillset (Drain/Shadowblade)** and his
secondary are KEPT, so his skills and the betray/auto-retreat link (event-keyed on unit id, not
level/gear) stay intact. His Runeblade is non-unique and STRIPPABLE — the canonical counter survives.

PLAYTEST: confirm s0 is the active Gaffgarion (vs a betrayal-spawned unit), and decide whether the
lvl-254 reinforcement Knights (s2/s3) should be scaled too (left untouched to avoid disturbing their
spawn scripting).

### Ovelia survivability (four passes; landed on JOB-INNATE Mana Shield + Manafont over gear Always-Protect, 2026-06-28)

**Player report (2026-06-27):** at NG+ party level, Ovelia "is dying with one hit of anything" on the
Save-Ovelia path, making it near-unwinnable. **Root cause:** her level IS auto-scaled to party level
(the runtime guest-scaler hits her because job 12 == charId 0x0c), but her slot shipped **gear-light**
(Wizard's Hat / Wizard's Robe / no accessory / White Staff). The level was never the problem; the
defense was.

**Fix #1 (evasion kit) — FAILED in playtest #2.** First pass gave her an evasion kit (Ribbon /
Luminous Robe / **Featherweave Cloak** 40/30 evade / Golden Staff). It did NOT save her, because of a
hard engine rule: **a charging unit has 0 evasion from every side AND takes +50% physical damage**
(only Blade Grasp bypasses this). Ovelia's AI hangs back and casts defensive magic, so she is almost
always mid-charge when the adjacent Knight/Archer reach her — at which point her evasion is *zero* and
the incoming hit is *amplified*: a guaranteed one-shot. **Evasion is the wrong stat for a unit that
lives in the charge state.**

**Fix #2 (Mana Shield / Move-MP Up via the ENTD R/S/M bytes) — BLOCKED.** The plan was to soak the
(Protect-halved) hit into MP via Mana Shield. Writing it to her ENTD slot did nothing: **Ovelia is a
NAMED GUEST, and the engine sources her command + reaction/support/movement from her fixed character
template, NOT from the ENTD R/S/M bytes.** Proof in-game (playtest #3): the Mana Shield (445) and
Move-MP Up (494) we wrote to her slot never appeared, and her *secondary still showed "Items"* even
though the slot's secondary byte is 254/none. Side-finding — **`battle_patch.py` brave offset bug:**
brave is at **0x06**, not 0x05 (the tool wrote the wrong byte; in-game Brave stayed at her template 53,
and the stray 0x05 write corrupted a different field — now fixed). *(The conclusion first drawn here —
"abilities can only come from a runtime code patch" — was WRONG about the remedy: the ENTD R/S/M bytes
are indeed ignored, but the "template" the engine reads passives from is the unit's **JOB**, which is
fully data-moddable. See Fix #4.)*

**Fix #3 (gear-granted Always-Protect) — RETAINED as the deterministic layer.** Gear *does* apply to a
named guest, so the accessory carries a charge-proof cut that needs no proc roll:

- **Accessory: Sortilège (239)** — reserved female-only Perfume granting **Always: Protect + Shell**
  (EquipBonus 68). **Protect halves every physical hit DETERMINISTICALLY, even mid-charge** — while
  charging a hit resolves base → ×1.5 (charge) → ×0.5 (Protect) = **0.75× of a normal hit** instead of
  an amplified one-shot. Shell halves magic. (Reserved item is fine: battle-only VIP; gear never enters
  the player inventory.)
- **Head: Gold Hairpin (166)** — +80 HP / +50 MP (user pick over Ribbon: HP cushion + MP that now also
  feeds Mana Shield as well as her Holy Magicks). **Body: Luminous Robe (206)** — +75 HP. **Weapon:
  Golden Staff (64)** — MA.

**Fix #4 (JOB-INNATE Mana Shield + Manafont) — THE breakthrough; current.** The "template" the engine
reads a named guest's passives from is the unit's **JOB**, and a job's innate abilities are data-moddable.
Princess (job 12, unique to Ovelia) already ships innate **Defense Boost (466) + Magick Defense Boost
(468)** in innate slots 1-2 — which is *why* her R/S/M slots render empty in-game yet she still mitigates:
**innate abilities are always active but never display in the equipped slots.** Slots 3-4 were free, so via
the modloader's per-mod table override — `src/fftivc.battles.ngplus/FFTIVC/tables/enhanced/JobData.xml`
(deployed next to the DLL; wired into the `.csproj`) — we add:
- **InnateAbilityId3 = 445 Mana Shield** — routes a would-be lethal hit to MP. No HP overflow in FFT: as
  long as she has ≥1 MP, *any* single hit is fully absorbed, and it **works mid-charge**. Procs at Brave%.
- **InnateAbilityId4 = 494 Manafont** (the Enhanced-edition name for **Move-MP Up**) — refills MP each
  step to keep the Mana Shield pool topped up.
- **Brave = 61** (ENTD 0x06, the corrected offset) — now meaningful: it IS Mana Shield's proc rate.

Net layered defense: innate Defense/Magick-Defense Boost (vanilla) + gear Always-Protect (deterministic ½
physical, charge-proof) + **61% innate Mana Shield** (negates a hit outright into MP) + ~155 bonus HP.
Because innate abilities don't reliably show in the menu, **verify in battle by the EFFECT**, not the slot:
watch a hit drain her MP, or watch her live through a blow that previously one-shot her. **Confirmed in-game
2026-06-28:** both active — Mana Shield (reaction) was recognized in-game, but Manafont/Move-MP Up (movement)
did NOT render in the slot yet worked (she moved and regained MP), same as her two vanilla support innates.
Innate display is type-dependent; trust the effect.

**If still insufficient (playtest), escalate by:** more HP via gear (body Luminous Robe → **Black Garb
198, +100 HP**, or head → Thief's Cap 168, +100 HP but no MP). The abilities lever is now data-driven —
further passives (e.g. innate Auto-Potion/Regen) can be added to the same JobData override, **no code
patch required**. This generalizes to every named guest: give them survivability via *their job's* innate
ability slots, not the ENTD.

## Job Escalation (Chapter 2 rule)

```text
CHANGE: swap ONE Knight -> an Archer (keep the count at 6).
WHY: the original escort threat is all melee Knights, which a player can wall off at the bridge
  to shield a hanging-back Ovelia. Adding a ranged Archer means Ovelia can be threatened from
  across the water / from elevation, so the player must actually cover her line of sight, not
  just block the bridge. This is the single new wrinkle; the strategy ("defend Ovelia, weather
  Gaffgarion, use Agrias") is unchanged — only harder.
WHAT IS NOT CHANGED: Gaffgarion's gear-dependent threat and the four remaining Knights keep the
  betrayal-and-press identity intact.
```

## Boss rare loot

```text
NONE here. Gaffgarion RETREATS (he is not defeated at Zeirchele), so there is no drop, and the
canonical counter is to strip his gear anyway. His rare, non-buyable signature item is granted
at Lionel Castle Gate (doc 021 / Battle 20), where he actually falls. Keeping his Zeirchele kit
strong-but-non-unique also keeps the strip-his-gear tactic meaningful.
```

## Proposed Composition (New Game++ Zeirchele v1)

Keep Gaffgarion + the Knight escort, swapping one Knight for an Archer (6 enemies). Gaffgarion
at sub-boss tier (`103`); the Archer and lead Knight at `101`; the rest at `100`–`101`.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | **Gaffgarion (betrayer)** | Dark Knight / Fell Knight | `103` | Draining sword-skill pressure; retreats at low HP. Strip-his-gear neuters him. |
| n | Knight | Knight | `101` | Lead wall; drives toward Ovelia. |
| n | Knight | Knight | `101` | Second wall; contests the bridge. |
| n | Knight | Knight | `100` | Body; flanks along the bank. |
| n | Knight | Knight | `100` | Body; reinforces the push on Ovelia. |
| n | Archer (NEW) | Archer | `101` | Ranged threat to Ovelia from across the water / elevation — the new escort wrinkle. |

Reasoning:

The faithful move is to **scale the escort, elevate Gaffgarion to a real sub-boss, and add one
ranged threat to Ovelia**. Gaffgarion at `103` with draining dark sword skills is a genuine
menace — but, true to the original, his power is in his (strippable, non-unique) weapon, so the
counter survives. Four Knights keep the bridge-push identity; the swapped-in Archer means the
player can't simply block the bridge and ignore Ovelia's line of sight. Agrias (ally) offsets
the difficulty, as intended.

## Builds (final-shop quality; Gaffgarion gear-dependent and strippable)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Gaffgarion - Betrayer sub-boss (Lv 103)

```text
Job: Dark Knight / Fell Knight (id TBD — preserve the ally->betray + auto-retreat link)
JobLevel: 8
Primary/Secondary: his dark sword skillset (Drain/Shadowblade-type, id TBD) — keep it
  WEAPON-dependent so stripping his sword (the canonical counter) truly weakens him
Reaction: Counter or Damage Split (id TBD) — punishes dogpiling
Support: Attack Boost (465)   Movement: Movement +1 (486)

Head: shop heavy helm (id TBD)        Body: shop heavy armor (id TBD)
Accessory: Bracers (218)
Right hand: a strong shop sword (Runeblade 30 / Icebrand 29) — NON-unique and STRIPPABLE
Left hand: shop shield (id TBD)
```

Role: the betrayer. Drains HP off the party with his sword skills, but a player who stripped
his gear (or breaks it) defangs him — exactly the original lesson. NON-unique kit (his rare
drop is reserved for Lionel Gate).

### Knight x4 (Lv 101 / 101 / 100 / 100)

```text
Job: Knight (id TBD)   JobLevel: 8   Secondary: none (NO Break)
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head/Body: shop heavy helm + heavy armor (ids TBD)
Accessory: Bracers (218)
Right hand: Runeblade (30) or Icebrand (29)   Left hand: shop shield (id TBD)
```

Role: the wall that drives at Ovelia. Forces the player to hold the bridge/bank chokepoint.

### Archer (Lv 101) — NEW (job swap)

```text
Job: Archer (77)   JobLevel: 8   Secondary: none
Reaction: Reflexes (449)   Support: Concentration (469)   Movement: Movement +1 (486)
Head: Thief's Cap (168)   Body: Black Garb (198)   Accessory: Bracers (218)
Right hand: Windslash Bow (87)   Left hand: none / two-hand marker (254)
```

Role: the ranged escort threat. Positioned to draw a line on Ovelia from across the water or
from elevation, so the player must screen her, not just block the melee.

## Positioning Plan

```text
Gaffgarion starts on the party's side or the bridge (per his betray scripting) — when he turns,
  he pressures the player's line and drives toward Ovelia.
The four Knights start across/at the bridge, pushing toward Ovelia's hang-back position.
The Archer starts on elevation or the far bank with a sightline to Ovelia's area — the threat
  the player must screen.
Preserve Ovelia's protected position, Agrias's ally slot, and Gaffgarion's betray/retreat link.
```

The map should read: "a draining traitor and a Knight wall drive across the bridge at the
princess, with an archer drawing a bead on her from afar." Screen Ovelia, strip the traitor,
hold the crossing.

## Implemented (v1, entry 405)

Applied with `python tools/battle_patch.py zeirchele`; diff contained to local entry 21 (global 405),
65 bytes. Unlike Merchant Dorter / Araguay, the Chapter-2 escalation here was a **job SWAP** (Knight
→ Archer on s8), so it was done inline — no slot-add deferral needed.

```text
s0  Gaffgarion  L103 jl8  (job 5 + secondary KEPT)  R Counter  S Atk-Boost  M +1  heavy kit + Runeblade(strippable) + Shield
s4  Knight      L101 jl8  R Counter  S Atk-Boost  M +1  heavy shop kit + Runeblade + Shield
s5  Knight      L101 jl8  (same kit)
s6  Knight      L100 jl8  (same kit)
s7  Knight      L100 jl8  (same kit)
s8  Archer      L101 jl8  R Reflexes  S Concentration  M +1  Thief's Cap / Black Garb / Bracers + Windslash Bow
```

## Implementation Checklist

- [x] Identify Zeirchele ENTD entry (405); fill "Local Data Confirmed".
- [x] Dump original entry; verify Gaffgarion + 5 Knight + Agrias + Ovelia slots.
- [x] Preserve Gaffgarion's job/secondary + identity (betray/auto-retreat link untouched).
- [x] Keep his gear strippable + non-unique (Runeblade).
- [x] Swap one Knight -> Archer (re-job s8); Archer build applied.
- [x] Set levels: Gaffgarion `103`; lead Knights + Archer `101`; other two Knights `100`.
- [x] Set JobLevel `8` on all scaled enemy slots; Knights have no secondary.
- [x] Do NOT touch Agrias/reinforcement/story slots.
- [x] Equip Ovelia for survival (playtest fix): endgame job-legal kit; level left to the scaler. See "Ovelia survivability".
- [x] Patch the embedded ENTD (NG+-only); diff inside entry 405 only.
- [x] Re-dump and diff; changes small and intentional; named links intact.
- [ ] Playtest from a NG+ save; confirm Ovelia-protect + Gaffgarion-retreat work; decide on s2/s3.

## Test Questions

- Is protecting Ovelia genuinely tense at scale (Knight push + the new Archer threat) without
  being an unavoidable loss?
- Does Gaffgarion feel like a dangerous betrayer, while the strip-his-gear counter still defangs him?
- Does his auto-retreat-at-low-HP still trigger (he must NOT be killable here)?
- Does the swapped-in Archer change the escort math (must the player screen Ovelia's LoS)?
- Does Agrias as an ally offset the difficulty as intended?
- Is it harder than Araguay but not yet a Gaffgarion/Cúchulainn-tier boss wall, per the curve?
- Does it still read as the riverbank betrayal, not a designed arena?

## Sources

- Game8, "Zeirchele Falls Walkthrough (Battle 13)": roster (Gaffgarion + 5 Knight), objective
  "Save Princess Ovelia!", deploy 4, recommended level ~13, riverside/bridge terrain,
  Gaffgarion betrayal + strip-his-gear tip + auto-retreat-at-low-HP, Ovelia defensive-magic VIP.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553174
- Final Fantasy Wiki, "Zirekile Falls" / "Gaffgarion": story context (betrayal, Agrias joins).
  https://finalfantasy.fandom.com/wiki/Zirekile_Falls
- Local: `docs/battles/011-chapter-2-overview.md` (job-escalation + boss-loot rules),
  `008-fovoham-windflats.md` (gear-dependent sword-skill boss handling),
  `021-lionel-castle-gate.md` (where Gaffgarion falls and gets his rare drop — to be written).
</content>
