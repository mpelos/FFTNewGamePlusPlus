# 014 - Zeirchele Falls (Zirekile Falls)

Status: ✅ implemented (v1, entry 405) — Knight→Archer escalation done inline; Ovelia survival = JOB-INNATE Mana Shield + Manafont (Princess job 12 via FFTIVC/tables/enhanced/JobData.xml) layered over gear Always-Protect (Sortilège) + Brave 61 (2026-06-28; earlier evasion + ENTD-R/S/M passes both failed — see "Ovelia survivability"). ✅ CONFIRMED in-game 2026-06-28 — Mana Shield + Move-MP Up both active. **v2 redesign documented only** (implementation pending).
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

Zeirchele is **the betrayal fight and the chapter's first real bridge-control battle**. The drama
is Gaffgarion flipping from ally to enemy. The *mechanics* should be: control Ovelia and Agrias,
hold the crossing, choose whether to strip/break Gaffgarion's weapon, and decide whether to kill the
field medic or burst the traitor. Ovelia's death can remain the loss condition, but the mod should
not make her AI or fragility the skill check. She must be durable and player-controlled in NG+.

For New Game++ the identity must stay: **a tense riverbank betrayal where a gear-dependent Dark
Knight, a Knight escort, a single ranged screen, and a healer push the bridge — control the VIP,
break the sustain, and exploit the strip-his-gear counter.**

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

## Enemy Party Escalation (Chapter 2 redesign)

```text
VANILLA SPIRIT: Gaffgarion betrays at the river crossing while an Order Knight escort pushes toward
  Ovelia.
CHAPTER-2 UPGRADE: keep Gaffgarion's gear-dependent drain threat, keep four Knights and one Archer,
  and add one White Mage field medic behind the escort.
WHY: a second Archer was rejected because it over-focuses Ovelia's line-of-sight and feels cheap.
  A White Mage instead creates target priority: if the player ignores the medic, Gaffgarion and the
  Knights get sustain; if the player overcommits to the medic, Gaffgarion punishes the line.
WHAT IS NOT CHANGED: Gaffgarion remains strippable/breakable, retreats instead of dying, Ovelia is
  still the VIP objective, and the map still reads as a bridge betrayal.
```

Chapter 2 requirements applied:

```text
- Every active human enemy has full equipment.
- Every active human enemy has intentional reaction, support, and movement.
- Secondary is optional; the White Mage uses innate White Magic, Knights need no secondary here.
- Hard-lock status remains banned.
- Ovelia and Agrias must be player-controlled in NG+; guest AI is not the skill check.
```

## Boss rare loot

```text
NONE here. Gaffgarion RETREATS (he is not defeated at Zeirchele), so there is no drop, and the
canonical counter is to strip his gear anyway. His rare, non-buyable signature item is granted
at Lionel Castle Gate (doc 021 / Battle 20), where he actually falls. Keeping his Zeirchele kit
strong-but-non-unique also keeps the strip-his-gear tactic meaningful.
```

## Guest handling

```text
Ovelia and Agrias are active allies and must be player-controlled in NG+. Ovelia keeps the v1
survivability layers (Princess innate Mana Shield + Manafont, Always-Protect gear, Brave 61), but
v2 adds control as a requirement so the player can route her instead of losing to AI.

If Gaffgarion is controllable before the betrayal phase, that control is allowed only while he is
still an ally. After betrayal he is an enemy sub-boss and must keep the scripted retreat behavior.
```


Fixed encounter Brave/Faith targets:

| Unit | Br/Fa | Rationale |
|------|-------|-----------|
| Ovelia | `61/78` | Keep the confirmed Brave 61 Mana Shield proc target; high Faith supports her defensive-magic identity. |
| Agrias | `76/65` | Controlled Holy Knight ally; durable physical ally with moderate magic interaction. |

## Proposed Composition (New Game++ Zeirchele v2)

Use seven enemies: Gaffgarion, 4 Knights, 1 Archer, 1 White Mage. Gaffgarion stays sub-boss tier
(`103`); the Knight captain reaches `102`; the ranged/support units sit at `101`.

| Slot | Role | Job | Level | Br/Fa | Purpose |
| ------ | ------ | ----- | ------- | --- | --------- |
| n | **Gaffgarion (betrayer)** | Dark Knight / Fell Knight | `103` | `82/60` | Draining sword-skill pressure; retreats at low HP. Strip-his-gear neuters him. |
| n | Knight Captain | Knight | `102` | `76/48` | Lead wall; contests the crossing and protects the medic. |
| n | Knight | Knight | `101` | `76/48` | Second wall; presses the bridge. |
| n | Knight | Knight | `101` | `76/48` | Bank guard; stops a free rush to the backline. |
| n | Knight | Knight | `100` | `76/48` | Body; reinforces the push. |
| n | Archer | Archer | `101` | `74/50` | One line-of-sight threat; prevents a pure bridge turtle. |
| n | Field Medic (NEW) | White Mage | `101` | `55/76` | Sustain/revive pressure; forces target priority. |

Reasoning:

The faithful move is to **scale the betrayal and bridge pressure**, not turn Ovelia into a coin-flip
liability. Gaffgarion at `103` with draining dark sword skills is a genuine menace, but his power
is still in his strippable weapon. Four Knights keep the Order escort identity. One Archer prevents
a pure turtle. The White Mage is the v2 escalation: sustain makes target priority matter without
adding hard status or a second cheap line-of-sight attacker.

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

### Knight x4 (Lv 102 / 101 / 101 / 100)

```text
Job: Knight (id TBD)   JobLevel: 8   Secondary: none (NO Break)
Reaction: Counter (442)   Support: Defense Boost on captain / Attack Boost on others (ids TBD / 465)
Movement: Movement +1 (486)
Head/Body: shop heavy helm + heavy armor (ids TBD)
Accessory: Bracers (218)
Right hand: Runeblade (30) or Icebrand (29)   Left hand: shop shield (id TBD)
```

Role: the wall that controls the crossing. No Rend here; the fight's gear lesson is Gaffgarion's
weapon, not generic equipment break pressure.

### Archer (Lv 101)

```text
Job: Archer (77)   JobLevel: 8   Secondary: none
Reaction: Reflexes (449)   Support: Concentration (469)   Movement: Movement +1 (486)
Head: Thief's Cap (168)   Body: Black Garb (198)   Accessory: Bracers (218)
Right hand: Windslash Bow (87)   Left hand: none / two-hand marker (254)
```

Role: the ranged screen. Positioned to punish a bridge turtle, not to create unavoidable shots on
Ovelia before the player can respond.

### Field Medic — White Mage (Lv 101) — NEW

```text
Job: White Mage (id TBD)   JobLevel: 8   Secondary: none
Reaction: Mana Shield / Reflexes (id TBD / 449)
Support: Arcane Defense / Defense Boost if legal (id TBD)
Movement: Movement +1 (486)
Head: mage hat (id TBD)   Body: shop robe (id TBD)
Accessory: Magic Ring / Featherweave Cloak (id TBD / 234)
Right hand: Golden Staff (64) or shop staff (id TBD)   Left hand: none (255)
```

Role: sustain and revive pressure. The player can answer by rushing the medic, silencing it,
or bursting Gaffgarion through the sustain.

## Positioning Plan

```text
Gaffgarion starts on the party's side or the bridge (per his betray scripting) — when he turns,
  he pressures the player's line and drives toward Ovelia.
The four Knights start across/at the bridge, pushing toward Ovelia's hang-back position.
The Archer starts on elevation or the far bank with a sightline to the approach lane — pressure,
  not unavoidable VIP sniping.
The White Mage starts behind the Knight line, close enough to heal Gaffgarion/Knights but reachable
  by a committed push or ranged answer.
Preserve Ovelia's protected position, Agrias's ally slot, and Gaffgarion's betray/retreat link;
  add NG+ player-control handling for Ovelia/Agrias.
```

The map should read: "a draining traitor and a Knight wall drive across the bridge at the
princess, with one archer and one medic forcing target priority." Control Ovelia, strip the
traitor, break the sustain, hold the crossing.

## Simulation Plan and Results

Simulation artifact:

```text
tmp/fft-level-design-014-zeirchele-falls/
```

Model scope:

```text
First four rounds after betrayal; compares action economy and weighted pressure. It explicitly
rejects candidates that rely on Ovelia AI or excessive line-of-sight pressure.
```

Iteration results:

| Candidate | Enemies | Enemy actions | Action ratio | Pressure | Delta vs v1 | Result |
|-----------|---------|---------------|--------------|----------|-------------|--------|
| v1 current: Gaffgarion, 4 Knight, 1 Archer | 6 | 22.2 | 0.92 | 52.4 | 0.0% | Baseline |
| Add second Archer LoS | 7 | 26.2 | 1.09 | 60.8 | +16.0% | Rejected: too much VIP LoS |
| Ovelia durable but not controlled | 7 | 25.6 | 1.07 | 61.2 | +16.8% | Rejected: guest-AI framing |
| Gaffgarion, 4 Knight, 1 Archer, 1 White Mage | 7 | 25.6 | 1.07 | 61.2 | +16.8% | Accepted |

Decision:

```text
Use one White Mage field medic as the v2 escalation. Do not add a second Archer. Ovelia and Agrias
must be player-controlled in NG+, while Gaffgarion remains weapon-dependent and scripted to retreat.
```

## Current Implementation (v1, entry 405 — superseded by v2 design)

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

This implementation remains the shipped v1 data. The v2 redesign above is **documentation only** in
this pass; it requires a later ENTD/table implementation pass to add the White Mage, verify/apply
Ovelia/Agrias player control, and keep Gaffgarion's betrayal/retreat scripting intact.

## Future Implementation Checklist (v2)

- [x] Identify Zeirchele ENTD entry (405); fill "Local Data Confirmed".
- [x] Dump original entry; verify Gaffgarion + 5 Knight + Agrias + Ovelia slots.
- [x] Preserve Gaffgarion's job/secondary + identity (betray/auto-retreat link untouched).
- [x] Keep his gear strippable + non-unique (Runeblade).
- [x] Swap one Knight -> Archer (re-job s8); Archer build applied.
- [ ] Add one White Mage field medic in a verified reachable backline slot.
- [ ] Set levels: Gaffgarion `103`; Knight captain `102`; two Knights + Archer + White Mage `101`;
  last Knight `100`.
- [ ] Set JobLevel `8` on all active enemy slots; Knights have no secondary.
- [ ] Give every active human enemy complete equipment plus intentional reaction/support/movement.
- [ ] Set Ovelia and Agrias player-controlled in NG+; do not rely on guest AI.
- [x] Equip Ovelia for survival (playtest fix): endgame job-legal kit; level left to the scaler. See "Ovelia survivability".
- [ ] Patch the embedded ENTD/table data in a later implementation pass; no binary/data change in this doc pass.
- [ ] Re-dump and diff; changes small and intentional; named links intact.
- [ ] Playtest from a NG+ save; confirm Ovelia-protect + Gaffgarion-retreat work; decide on s2/s3.

## Test Questions

- Does controlling Ovelia create a fair routing decision instead of an AI survival check?
- Does Gaffgarion feel like a dangerous betrayer, while the strip-his-gear counter still defangs him?
- Does his auto-retreat-at-low-HP still trigger (he must NOT be killable here)?
- Does the White Mage create meaningful target priority without making the fight a slog?
- Does the single Archer prevent bridge turtling without creating unavoidable VIP snipes?
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
- Local: `docs/battles/011-chapter-2-overview.md` (enemy-party escalation + boss-loot rules),
  `008-fovoham-windflats.md` (gear-dependent sword-skill boss handling),
  `021-lionel-castle-gate.md` (where Gaffgarion falls and gets his rare drop — to be written).
</content>
