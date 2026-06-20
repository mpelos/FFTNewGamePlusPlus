# 041 - Outlying Church (Zeltennia Church)

Status: designed (not yet implemented)
Chapter: 4 — "In the Name of Love"
Battle order: Battle 36 (after Finnath Creek)
Target version: Enhanced v1.5.0
ENTD: global entry **TBD** — confirm on Windows game data
File: `battle_entd*_ent.bin` (TBD) / `OverrideEntryData` rows (TBD)

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `037-chapter-4-overview.md`.

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

Because he died-not in Ch3, his rare was **deferred** (see the Ch3 ledger, `036`). Here he dies for
good, so the deferred drop pays out — a Tier-A holy-caster reward — while the map's iconic, thematic
**Angel Ring** (auto-Reraise — perfect for "the man who revives") stays as the existing guaranteed
reward.

For New Game++ the identity must stay: **an elevated holy boss-duel — reach or silence the sustaining
Inquisitor and burst him through a Knight/Mystic screen — now with the deferred Zalmo rare finally
paid; the boss is the escalation, the screen stays familiar.**

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm slots: Zalmour (boss) + 3 Knight + 2 Mystic, plus the player slots.
Keep the win condition = "Defeat Zalmour" (ends on his death) and the ELEVATED church geometry
  (the height wall IS the fight — do not flatten it).
Keep Zalmour's holy sustain/revive kit + make his equipped Tier-A item stealable.
This is a Tier-A BOSS fight: boss spike at 104, adds 101-103; ONE Tier-A rare on Zalmour.
Preserve the vanilla guaranteed ANGEL RING reward + the buried map rares (White Robe etc.) as-is.
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
```

Job IDs (carry over known, verify the rest in-game):

```text
Knight job id          (TBD - verify)
Mystic / Oracle id     (TBD - verify; soft-status caste)
Inquisitor id          (TBD - verify; Zalmour's boss job — Ch3 Zalmo precedent, 026)
```

## Job Escalation (Chapter 4 rule)

```text
CHANGE: NO generic-slot swap. The escalation is the BOSS — Zalmour returns at full Chapter-4 boss
  strength (`104`), and crucially he now DIES here (in Ch3/026 he fled), closing his arc and paying his
  deferred rare.
WHY: the fight's identity is already "reach/silence the sustaining holy boss and burst him on elevated
  ground." The faithful Ch4 escalation is to deliver that boss at full power on the height map — NOT to
  add a new mechanic onto a roster that already pairs a Knight screen (Rend) with Mystic soft-status.
  Adding a second wrinkle would break the one-new-demand rule; the elevated out-sustaining boss IS the
  demand.
CONSTRAINT (carry Ch3 Zalmo precedent, 026): his sustain/revive is answered by Silence / focus-burst /
  reaching him; HOLY + SOFT status only (no hard lock). Keep Knight Rend within the carried
  ≤2-break-source cap (limit Rend to at most 2 of the 3 Knights).
OPTIONAL: if testing finds his sustain too easy to out-race, swap ONE Knight -> a White Mage to double
  the heal-pressure (sharpening "focus the healers") — still soft, still no hard lock. Default keeps the
  faithful 3 Knight + 2 Mystic screen.
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

## Boss rare loot

```text
ZALMOUR (boss) drops/carries ONE Tier-A rare: LIGHT ROBE (top holy/magic robe below Robe of Lords).
WHY IT FITS: he is a high churchman / holy caster; the best non-ultimate caster robe (Holy-aligned) is
  his natural vestment and a tempting STEAL. It is a clear upgrade over Ch2/Ch3 caster gear without being
  best-in-slot.
TIER: A (mid-Chapter-4 best non-ultimate). NOT Robe of Lords (Tier-S, reserved for the endgame, 47-53).
He DIES here (win = defeat Zalmour), so the deferred Ch3 rare finally pays — consistent with
  "retreat/flee = no drop" (his Ch3/026 flee meant no drop THEN; it pays NOW).
PRESERVE (vanilla, not added by us): the guaranteed ANGEL RING reward (auto-Reraise — thematically the
  reviving Inquisitor's signature) and the buried map rares (White Robe, Japa Mala, Magick Ring,
  Assassin's Dagger). Different slots from his equipped Light Robe — no double-dip.
```

## Proposed Composition (New Game++ Outlying Church v1)

Keep the count (6) and the elevated boss-duel shape; elevate Zalmour to full boss strength, keep the
screen. Boss `104`; Knights `102`/`102`/`101`; Mystics `102`.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Zalmour (BOSS) | Inquisitor | `104` | Holy sustain/revive on high ground; the objective; Light Robe steal-bait. |
| n | Knight | Knight | `102` | Front-line screen; Rend (break source 1). |
| n | Knight | Knight | `102` | Second screen; Rend (break source 2 — cap reached). |
| n | Knight | Knight | `101` | Third body; NO Rend (cap kept) — pure bruiser. |
| n | Mystic | Mystic | `102` | Soft status (Oracle-equivalent) guarding the approach. |
| n | Mystic | Mystic | `102` | Second status caster; pins the player off the height. |

Reasoning:

The faithful move is to **make the returning boss the whole escalation and keep the screen
recognizable**. Zalmour at `104` on the elevated church, with a Silence/focus-counterable sustain kit
and Light-Robe steal-bait, delivers the "reach-or-silence-and-burst the holy boss" duel at full Ch4
strength — and finally kills him, paying the deferred rare. The three Knights (Rend capped to two) and
two Mystics stay as the height-guarding screen — no new mechanic added. Only Zalmour sits at the boss
band (`104`); the screen is `101`–`102`.

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
  Secondary: (light) soft status   — HOLY + SOFT status only; no hard lock.
Reaction: (anti-burst) Reflexes / Counter Magic (id TBD)   Support: MA/Magick-boost (id TBD)
  Movement: Movement +1 (486) or Ignore Height (id TBD — fits the elevated boss)
Head: holy mitre / mage hat (id TBD)   Body: LIGHT ROBE (Tier-A, id TBD)
Accessory: Tier-A caster accessory (id TBD)   Right hand: high holy staff/rod (id TBD)   Left: none (255)
```

Role: the objective and the sustain threat — reach/silence and burst him; steal his Light Robe.

### Knight x3 (Lv 102 / 102 / 101) — height-guarding screen

```text
Job: Knight (id TBD)   JobLevel: 8   Primary: basic + Rend (ONLY on 2 of the 3 — cap)
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Movement +1 (486)
Head: shop helm (id TBD)   Body: shop heavy armor (id TBD)   Accessory: Bracers (218)
Right hand: shop knight sword (id TBD)   Left: shop shield (id TBD)
```

Role: front-line screen guarding the approach to the height; Rend on at most two (cap), no break-lock.

### Mystic x2 (Lv 102) — soft status

```text
Job: Mystic / Oracle (id TBD)   JobLevel: 8   Secondary: none
Soft, resistable status (no Stop/Don't Act/Petrify). Normal cast cadence.
Reaction: Reflexes (449)   Support: MA/Magick-boost (id TBD)   Movement: Movement +1 (486)
Head: mage hat (id TBD)   Body: shop robe (id TBD)
Accessory: Featherweave Cloak (234)   Right hand: magic-boost rod (id TBD)   Left: none (255)
```

Role: soft status that pins the party off the height while Zalmour sustains; race-able.

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

## Implementation Checklist

- [ ] Identify Outlying Church `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify Zalmour + 3 Knight + 2 Mystic + player slots.
- [ ] Keep win condition = "Defeat Zalmour" (ends on his death); keep the elevated geometry.
- [ ] Set Zalmour `104` with holy sustain/revive — Silence/focus answerable, holy+soft only, no hard lock.
- [ ] Equip Zalmour with Light Robe (Tier-A) + Tier-A accessory; confirm STEAL works.
- [ ] Limit Rend to 2 of the 3 Knights (≤2-break-source cap); Mystics soft status only.
- [ ] Set add levels: 2 Knight + 2 Mystic `102`; third Knight `101`.
- [ ] Preserve the guaranteed Angel Ring + buried map rares (do not remove/duplicate).
- [ ] Set JobLevel `8` on all active enemy slots.
- [ ] Patch via the correct layer; keep the diff inside the Outlying Church window only.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify elevation + steal + win-cond.
- [ ] Install mod, test from a New Game+ save; confirm it plays as an elevated holy-boss burst-duel.

## Test Questions

- Is the ELEVATION still the crux (player must bring height-ignoring damage or rush the boss)?
- Does Zalmour still out-sustain chip damage so the answer is reach/Silence/focus-burst (no slow trade)?
- Is his sustain holy/soft only — never a hard lock — and is he a tempting STEAL (Light Robe)?
- Does the deferred Zalmo rare now pay correctly (he dies here), while Angel Ring stays the map reward?
- Is Knight Rend within the ≤2-source cap (no break-lock) and Mystic status soft/resistable?
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
- Local: `037-chapter-4-overview.md` (job-escalation + Tier-A rare-loot rules),
  `026-lesalia-castle-postern.md` (Zalmo Ch3 — reviving Inquisitor who fled; rare deferred),
  `036-chapter-3-balance-review.md` (the deferred-rare ledger this pays out).
```
</content>
