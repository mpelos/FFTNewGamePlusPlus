# 041 - Outlying Church (Zeltennia Church)

Status: 📝 redesign v2 planned (docs-only) — v1 implementation exists for entry 445
Chapter: 4 — "In the Name of Love"
Battle order: Battle 36 (after Finnath Creek)
Target version: Enhanced v1.5.0
ENTD: global entry **445** (local entry 61, `battle_entd4_ent.bin`)
File: `battle_entd4_ent.bin` (embedded NG+ swap) — `tools/battle_patch.py outlying_church`

Current implementation (entry 445, vanilla-dump verified):
- s1 **Zalmo** (job 16 Celebrant/Inquisitor, BOSS, dies → deferred Ch3 payout lands) — L104/jl8;
  thematic payout = **Light Robe = Luminous Robe (206)** as body (top robe below the Tier-S Lordly Robe;
  upgrades his vanilla White Robe 204; visible steal-bait). Job/secondary/head/acc/rod/holy-sustain +
  win-on-death scripting preserved. Holy+soft only, no hard lock.
- s2,s3 Mystic L102 — soft status (Oracle-equiv); Mage Hat/shop Robe/Featherweave/shop Rod; Reflexes/Atk Boost/Mv+1.
- s4,s5 Knight L102, s6 Knight L101 — height-guarding screen; Heavy gear/Runeblade/shop Shield; Rend innate.
- s0 = inactive guest placeholder (level 0xFE) — left untouched. Angel Ring + buried map rares (other layer) untouched.

Planned v2 redesign (docs-only in this pass): keep the same six-body vanilla roster, but make the
party a complete Chapter-4 **inquisition shell**: Zalmo remains the focus target, two Knights are the
only Rend sources, the third Knight is a bodyguard/item stabilizer, and both Mystics gain limited
defensive secondary magic so they support the boss without becoming a separate healer puzzle.

> Note: TIC has no distinct "Light Robe" item; the top robe below the reserved Lordly Robe (207) is
> Luminous Robe (206), used here. The current reward ledger treats this as a thematic/modest payout,
> not a best-in-slot rare.

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `037-chapter-4-overview.md`.

## Design Goal

```text
Make Outlying Church the decisive Zalmo execution: an elevated holy-boss burst duel where the player
must reach, Silence, steal from, or burst the sustaining Inquisitor through a complete but constrained
Knight/Mystic shell. The pressure comes from height, sustain, and limited Rend, not hard status or
infinite healing.
```

No active guests appear here. No guest-control implementation is needed for this battle.

## Original Battle

Objective:

```text
Defeat Zalmour!   (he is finally KILLED here — the rematch he fled from in Chapter 3, 026)
```

Player deployment:

```text
Up to 5 units, including Ramza. No guests.
```

Original enemy composition (verified via Game8, Battle 36):

```text
Zalmour Lucianada    (BOSS — Inquisitor; holy magic + revive/sustain)
3x Knight            (front-line; Rend/break pressure)
2x Mystic            (Oracle-equivalent — soft status / support)
```

Public walkthrough details:

```text
Recommended level: ~43.  Difficulty: 3/5 stars.  Deploy up to 5.  Win: defeat Zalmour (ends fight).
ELEVATED CHURCH map — Zalmour sits on high ground; ELEVATION is the tactical crux. The walkthrough
  recommends height-ignoring damage: Black Mage magic, White Mage Holy, Hallowed Bolt — or a Ninja
  (Ignore Elevation) to RUSH him turn one and burst him.
Zalmour out-sustains chip damage (holy caster who heals/revives) — the answer is to FOCUS/burst or
  reach him, not to trade slowly.
Rewards: 25,700 Gil, ANGEL RING (guaranteed — the reviving-themed accessory), buried rares
  (White Robe, Japa Mala, Magick Ring, Assassin's Dagger).
```

Design reading:

Outlying Church is **the payoff fight for Zalmo**: the reviving Inquisitor who *fled* in Chapter 3
(`026`) is finally cornered and killed. Its identity is **an elevated holy boss who out-sustains you
unless you reach or silence him** — the map's height is a wall, and the lesson is to bring
height-ignoring damage (Holy / Black magic / Hallowed Bolt) or rush him with a mobile unit, then
**burst him down before his sustain resets the fight.** A Knight screen (Rend) and two Mystics (soft
status) guard the approach.

Because he did not die in Ch3, his payout was **deferred** (see the Ch3 ledger, `036`). Here he dies for
good, so the deferred reward pays out — a thematic holy-caster reward — while the map's iconic, thematic
**Angel Ring** (auto-Reraise — perfect for "the man who revives") stays as the existing guaranteed
reward.

For New Game++ the identity must stay: **an elevated holy boss-duel — reach or silence the sustaining
Inquisitor and burst him through a Knight/Mystic screen — now with the deferred Zalmo payout finally
paid; the boss is the escalation, the screen stays familiar.**

## Local Data Confirmed / Data Still Needed

```text
CONFIRMED:
- Entry 445 is the Outlying Church ENTD entry.
- Current roster is Zalmo/Zalmour + 3 Knights + 2 Mystics.
- Current v1 implementation already sets Zalmo to L104/JL8 and preserves win-on-Zalmo-death scripting.
- No active guest.
- Reward ledger currently maps this battle to Light Robe + Angel Ring guaranteed spoils.

STILL NEEDED FOR V2 IMPLEMENTATION:
- Confirm exact enemy slot order before patching the complete v2 kits.
- Confirm the win condition remains "Defeat Zalmour" and that any equipped/accessory choices do not
  interfere with the death trigger.
- Confirm whether OverrideEntryData carries level for this battle or leaves it at runtime scale.
- Preserve elevated church geometry; the height wall is the fight.
- Preserve buried map treasure as-is.
```

Job IDs (carry over known, verify the rest in-game):

```text
Knight job id          (TBD - verify)
Mystic / Oracle id     (TBD - verify; soft-status caste)
Inquisitor id          (TBD - verify; Zalmour's boss job — Ch3 Zalmo precedent, 026)
```

## Enemy Party Escalation (Chapter 4 rule)

```text
CHANGE: NO generic-slot swap. The escalation is the complete party shell around the BOSS — Zalmour
  returns at full Chapter-4 boss strength (`104`), and crucially he now DIES here (in Ch3/026 he fled),
  closing his arc and paying his deferred/modest holy reward.
WHY: the fight's identity is already "reach/silence the sustaining holy boss and burst him on elevated
  ground." The faithful Ch4 escalation is to make the existing roster synergize cleanly: the Knights
  guard the climb and threaten gear, the Mystics add soft pressure plus defensive support, and Zalmo
  remains the single focus target. No new caste is needed.
CONSTRAINT (carry Ch3 Zalmo precedent, 026): his sustain/revive is answered by Silence / focus-burst /
  reaching him; HOLY + SOFT status only (no hard lock). Keep Knight Rend within the carried
  ≤2-break-source cap (limit Rend to at most 2 of the 3 Knights).
REJECTED DEFAULTS: no White Mage swap, no third Rend Knight, no hard-status Mystic, no overlevelled
  screen. These variants either create a second healer puzzle, break the Rend cap, or turn elevation
  into lockdown.
WHAT IS NOT CHANGED: the elevated-church geometry, the Knight/Mystic screen, and the "rush/silence and
  burst the boss" win line remain. No brand-new caste debuts here.
```

## Sanctioned exceptions (carried precedents)

```text
HOLY-BOSS SUSTAIN / REVIVE (Zalmour) — allowed as his identity (Ch3 Zalmo precedent, 026): answered by
  Silence / focus-burst / reaching him on the height; holy + soft status only; no hard lock.
KNIGHT REND / BREAK — limited to ≤2 of the 3 Knights (carried ≤2-break-source cap, 028/033); telegraphed,
  Safeguard/Steal answers.
MYSTIC SOFT STATUS (Oracle-equivalent) — allowed; soft, resistable, no hard lock (Stop/Don't Act banned).
ELEVATION WALL — a terrain feature, not a status; preserved as the fight's crux (bring height-ignoring
  damage or a mobile rush). Not an exception so much as the core puzzle.
```

## Rare/reward handling

```text
Guaranteed spoils for entry 445: LIGHT ROBE + ANGEL RING.
These are delivered by the Spoils of War reward channel; the player must never be required to Steal.
WHY IT FITS: Zalmo is a high churchman / holy sustain boss, and the Angel Ring echoes his revive theme.
STEAL ROLE: Light Robe may still be equipped as visible steal-bait, but Steal is tactical/bonus only.
TIER: thematic mid-Chapter-4 payout; NOT Lordly Robe, Chaos Blade, Ribbon, or any Tier-S endgame item.
PRESERVE: buried map rares (White Robe, Japa Mala, Magick Ring, Assassin's Dagger) remain vanilla map
  treasure and are not the NG++ reward channel.
```

## Proposed Composition (New Game++ Outlying Church v2)

Keep the count (6) and the elevated boss-duel shape; make every active human a complete Chapter-4 unit.
Boss `104`; Knights `102`/`102`/`101`; Mystics `102`.

| Slot | Role | Job | Level | Br/Fa | Purpose |
| ------ | ------ | ----- | ------- | --- | --------- |
| n | Zalmour (BOSS) | Inquisitor | `104` | `72/82` | Holy sustain/revive on high ground; objective; Light Robe visible steal-bait. |
| n | Rend Knight | Knight | `102` | `88/42` | Front-line screen; Rend source 1; threatens gear on the climb. |
| n | Rend Knight | Knight | `102` | `88/42` | Second screen; Rend source 2 — cap reached. |
| n | Bodyguard Knight | Knight | `101` | `88/42` | No Rend learned/enabled; Item secondary stabilizes the screen without reviving Zalmo. |
| n | Mystic Chaplain | Mystic | `102` | `68/78` | Soft Mystic pressure + limited defensive White Magic secondary. |
| n | Mystic Chaplain | Mystic | `102` | `72/82` | Second soft caster; supports Zalmo without hard status or Raise/Holy. |

Reasoning:

The faithful move is to **make the returning boss the whole focus while the screen becomes fully built
Chapter 4 support**. Zalmour at `104` on the elevated church, with a Silence/focus-counterable sustain
kit and Light-Robe steal-bait, delivers the "reach-or-silence-and-burst the holy boss" duel at full Ch4
strength. The Knights guard the height with exactly two Rend sources; the third uses limited Item
support instead of adding a third break line. The Mystics gain constrained defensive secondary magic so
they reinforce the holy shell without becoming a White Mage detour. Only Zalmour sits at the boss band
(`104`); the screen is `101`–`102`.

Rejected variants:

```text
- v1 partial setup: correct roster shape, but incomplete for Chapter 4 humans.
- White Mage swap: creates a second healer target instead of sharpening the Zalmo focus race.
- Triple Rend: violates the two-break-source cap and makes gear protection too binary.
- Hard-status Mystics: turns the height puzzle into lockdown.
- Overlevelled screen: makes the guards the fight instead of Zalmo.
```

## Builds (Chapter-4 quality; holy-inquisition flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Zalmour (Lv 104) — BOSS (Inquisitor)

```text
Job: Inquisitor (id TBD)   JobLevel: 8   Primary: holy magic + sustain/revive (Holy, Cure-line, Raise);
Secondary: Mystic/White utility limited to soft support (Protect/Shell/Esuna/Cure-tier); no hard status.
Reaction: Reflexes / Counter Magic (id TBD)   Support: Arcane Strength / MA boost (id TBD)
  Movement: Movement +1 (486) or Ignore Height (id TBD — fits the elevated boss if legal)
Head: holy mitre / mage hat (id TBD)   Body: LIGHT ROBE (Tier-A, id TBD)
Accessory: non-Reraise caster accessory (do NOT equip Angel Ring unless death-trigger behavior is tested)
Right hand: high holy staff/rod (id TBD)   Left: none (255)
```

Role: the objective and the sustain threat — reach/silence and burst him; steal his Light Robe.

### Knight x3 (Lv 102 / 102 / 101) — height-guarding screen

```text
Job: Knight (id TBD)   JobLevel: 8   Primary: basic + Rend (ONLY on 2 of the 3 — cap)
Secondary: Item, limited to Potion/Hi-Potion/Remedy style stabilization; no Phoenix Down/Elixir.
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head: shop helm (id TBD)   Body: shop heavy armor (id TBD)   Accessory: Bracers (218)
Right hand: shop knight sword (id TBD)   Left: shop shield (id TBD)
```

Role: front-line screen guarding the approach to the height; Rend on at most two (cap), no break-lock.

Third Knight rule:

```text
The Lv101 bodyguard Knight has the same complete equipment/reaction/support/movement package, but NO
Rend abilities learned/enabled. His job is body-blocking, Item cleanup, and melee pressure.
```

### Mystic x2 (Lv 102) — soft status

```text
Job: Mystic / Oracle (id TBD)   JobLevel: 8
Primary: soft, resistable Mystic pressure only.
Secondary: White Magic, LIMITED to defensive/light sustain (Protect/Shell/Esuna/Cure-tier).
  No Raise, no Holy, no Stop/Don't Act/Petrify/Death/Charm-equivalent turn deletion.
Reaction: Reflexes (449)   Support: MA/Magick-boost (id TBD)   Movement: Movement +1 (486)
Head: mage hat (id TBD)   Body: shop robe (id TBD)
Accessory: Featherweave Cloak (234)   Right hand: magic-boost rod (id TBD)   Left: none (255)
```

Role: soft pressure and defensive shelling that buys Zalmo a turn or two without creating a separate
healer-kill detour.

## Positioning Plan

```text
Elevated church: Zalmour starts atop the high ground (the height wall), the three Knights screening the
  stairs/ramp up to him, the two Mystics flanking with status sightlines onto the approach.
Preserve the ELEVATION (the height is the puzzle) — the player must bring height-ignoring damage
  (Holy / Black magic / Hallowed Bolt) or rush him with a mobile unit (Ninja / Ignore Height).
Keep Zalmour reachable-but-guarded so it's a fight THROUGH the screen to the boss, not a free snipe.
Only the boss at `104`; do not over-scale the screen.
```

The church should say: "the inquisitor who ran is cornered at last — climb to him or smite him from
below, and end him before his prayers undo your work."

## Simulation Plan and Results

Simulation artifact:

```text
tmp/fft-level-design-041-outlying-church/
  assumptions.md
  simulate.py
  iteration-1-results.json
  iteration-1-results.md
  iteration-2-results.json
  iteration-2-results.md
  iteration-results.json
  iteration-results.md
```

Model scope:

```text
Coarse deterministic opening-pressure model over the first five rounds.
It scores local pressure, focus clarity, boss answerability, break fairness, sustain fairness, and
hard-status risk. It does not simulate exact FFT formulas.
```

Final iteration result:

| Candidate | Pressure | Focus clarity | Boss answer | Break fairness | Sustain fairness | Hard status | Verdict |
|---|---:|---:|---:|---:|---:|---:|---|
| v1 partial setup | 180 | 78 | 82 | 74 | 84 | 0 | Rejected: incomplete setup |
| v2 constrained inquisition shell | 190 | 100 | 88 | 74 | 88 | 0 | **Accepted** |
| white mage swap sustain stack | 216 | 86 | 66 | 74 | 60 | 0 | Rejected: too spiky |
| triple rend stair lock | 200 | 74 | 70 | 35 | 88 | 0 | Rejected: break cap violation |
| hard status mystic lock | 246 | 69 | 39 | 74 | 48 | 55 | Rejected: hard status |
| overlevelled screen | 212 | 100 | 78 | 66 | 80 | 0 | Rejected: too spiky |

Iteration decision:

```text
ACCEPT v2 constrained inquisition shell.
Iteration 1 rejected the full-healer reading because it pushed sustain over the local budget.
Iteration 2 keeps the vanilla roster and complete setups, but constrains Mystic secondary magic and
Knight item access so the answer remains Zalmo-focused: Silence, mobility, height-ignoring burst, or
fast gear disruption.
```

## Implementation Checklist

- [ ] Confirm current entry 445 slot order: Zalmour + 3 Knight + 2 Mystic + player slots.
- [ ] Keep win condition = "Defeat Zalmour" (ends on his death); keep the elevated geometry.
- [ ] Set Zalmour `104` with holy sustain/revive — Silence/focus answerable, holy+soft only, no hard lock.
- [ ] Equip Zalmour with Light Robe as visible steal-bait; rewards must still be guaranteed spoils.
- [ ] Do not equip Angel Ring on Zalmo unless death-trigger/Reraise behavior is explicitly tested.
- [ ] Limit Rend to 2 of the 3 Knights (≤2-break-source cap); third Knight has no Rend enabled.
- [ ] Give Knights complete kits; Item secondary is limited and does not include Phoenix Down/Elixir.
- [ ] Give Mystics complete kits; secondary White Magic is limited to defensive/light support, no Raise/Holy.
- [ ] Set add levels: 2 Knight + 2 Mystic `102`; third Knight `101`.
- [ ] Preserve guaranteed spoils: Light Robe + Angel Ring; preserve buried map rares (do not remove/duplicate).
- [ ] Set JobLevel `8` on all active enemy slots.
- [ ] Patch via the correct layer; keep the diff inside the Outlying Church window only.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify elevation + steal + win-cond.
- [ ] Install mod, test from a New Game+ save; confirm it plays as an elevated holy-boss burst-duel.

## Test Questions

- Is the ELEVATION still the crux (player must bring height-ignoring damage or rush the boss)?
- Does Zalmour still out-sustain chip damage so the answer is reach/Silence/focus-burst (no slow trade)?
- Is his sustain holy/soft only — never a hard lock — and is he a tempting STEAL (Light Robe)?
- Do Light Robe + Angel Ring pay through guaranteed spoils, without requiring Steal?
- Is Knight Rend within the ≤2-source cap (no break-lock) and Mystic status soft/resistable?
- Do all active humans have complete equipment plus secondary/reaction/support/movement?
- Does Mystic secondary support Zalmo without becoming a second healer puzzle?
- Is only Zalmour at the boss band (`104`), screen `101`-`102` — a Tier-A boss, not a spike?
- Does it read as the long-awaited execution of the runaway inquisitor on his own church steps?

## Sources

- Game8, "Outlying Church Walkthrough (Battle 36)": roster (Zalmour boss + 3 Knight + 2 Mystic),
  objective "Defeat Zalmour!", recommended level ~43, 3/5 stars, deploy 5, elevated-church terrain +
  height-ignoring-damage / Ninja-rush tips, rewards (25,700 Gil, guaranteed Angel Ring, buried rares
  White Robe / Japa Mala / Magick Ring / Assassin's Dagger).
  https://game8.co/games/Final-Fantasy-Tactics/archives/553196
- Final Fantasy Wiki, "Zalmour Lucianada" / "Zeltennia": story/terrain context.
  https://finalfantasy.fandom.com/wiki/Zalmo_Rusnada
- Local: `037-chapter-4-overview.md` (job-escalation + Chapter 4 reward rules),
  `026-lesalia-castle-postern.md` (Zalmo Ch3 — reviving Inquisitor who fled; payout deferred),
  `036-chapter-3-balance-review.md` (the deferred Zalmo ledger this pays out),
  `chapter-4-rewards-implementation.md` (guaranteed Light Robe + Angel Ring spoils).
