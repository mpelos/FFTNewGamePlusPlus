# 054 - Monastery Vaults, Fourth Level (Orbonne descent / Murond Death City)

Status: designed (not yet implemented)
Chapter: 4 — "In the Name of Love"
Battle order: Battle 49 (ENDGAME GAUNTLET 1 of 5 — NO resupply across 49→50→51→52→53)
Target version: Enhanced v1.5.0
ENTD: global entry **TBD** — confirm on Windows game data
File: `battle_entd*_ent.bin` (TBD) / `OverrideEntryData` rows (TBD)

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `037-chapter-4-overview.md`. ENDGAME GAUNTLET: 49 (`054`) → 50 (`055`) → 51 (`056`) →
> 52 (`057`) → 53 (`058`), ONE loadout, no outfitter — the longest sustained stretch in the game.

## Original Battle

Objective:

```text
Defeat all enemies!
```

Player deployment:

```text
Up to 5 units, including Ramza. No outfitter (gauntlet 1/5 — last chance to prep was BEFORE Battle 49).
```

Original enemy composition (verified via Game8, Battle 49):

```text
3x Knight   (equipment-break — Rend skills strip weapons/armor)
2x Monk      (unarmed melee; Chakra sustain / revive)
1x Archer    (ranged chip / elevation)
```

> No named boss — a pure all-generic skirmish.

Public walkthrough details:

```text
Recommended level: 60+.  Difficulty: 1/5 stars (the LIGHTEST of the final five — the gauntlet OPENER).
Deploy up to 5.  Win: defeat all enemies.
TERRAIN: the Monastery Vaults — the underground stone descent beneath Orbonne (cramped vault corridors).
THE THREAT — the KNIGHTS' equipment-break (REND): they can strip your weapons and armor. The
  walkthrough's tip: equip SAFEGUARD to protect your gear. The danger is CONTEXT — this is the FIRST of
  FIVE consecutive no-resupply fights, so gear lost HERE cascades through the entire gauntlet.
SUPPORT: two Monks (martial bodies, Chakra/revive sustain); one Archer (ranged chip from elevation).
Spoils: 32,800 Gil; buried treasure (four spots — Elixirs). No rare gear.
```

Design reading:

The Vaults Fourth Level is **the endgame gauntlet's deliberately light opener** — a pure all-generic
skirmish (3 Knight + 2 Monk + 1 Archer) whose whole point is **resource discipline at the start of a
five-battle no-resupply marathon**. Its identity is **a gear-preservation gate**: the Knights' **Rend**
equipment-break can strip your loadout, and because there's **no outfitter** for the next five fights,
losing a weapon or armor here **cascades** into the boss fights to come. It's 1/5★ by design — a warm-up
that tests whether the player came prepared (Safeguard / Maintenance) before the descent turns deadly.

For New Game++ the identity must stay: **the light, all-generic gauntlet opener whose one demand is
don't-lose-gear-to-Rend at the start of the no-resupply marathon.** It should escalate only modestly
(endgame-generic strength + a touch of tempo) — staying clearly LIGHTER than the bosses that follow
(50–53). No named boss → no rare; preserve the buried Elixirs.

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm slots: 3 Knight + 2 Monk + 1 Archer, no named boss. NO outfitter (gauntlet 1/5).
Keep the REND equipment-break threat (the wrinkle) — but CAP the sources (see Job Escalation) so it is
  answerable, not a loadout-wipe at the gauntlet's start.
Confirm whether OverrideEntryData carries Level, or leaves it at -1.
This is a no-boss, no-rare OPENER: levels 101-103; keep it LIGHTER than 50-53.
Leave the four buried Elixir spots as-is — existing loot.
```

Job IDs (carry over known, verify the rest in-game):

```text
Knight job id    (TBD - verify; Rend equipment-break)
Monk job id      (TBD - verify; Chakra / revive sustain)
Archer job id    (TBD - verify)
Ninja job id     (TBD - verify; the tempo swap — see Job Escalation)
```

## Job Escalation (Chapter 4 rule)

```text
CHANGE: keep 3 Knight + 2 Monk, but SWAP the lone Archer → a NINJA (fast dual-wield flanker). Bump the
  whole skirmish to endgame-generic strength (levels 101-103). Net feel: a 1/5★ warm-up becomes a tight
  ~2/5★ opener — still clearly the LIGHTEST of the final five, but no longer trivial at endgame levels.
WHY: the chapter wants more challenge via jobs without breaking strategy. The Ninja adds endgame TEMPO
  (a fast flanker that punishes a sloppy formation) while the Knights' Rend stays the central wrinkle.
  Keeping it light is deliberate — it's the gauntlet's gear-preservation gate, not a boss fight.
CONSTRAINTS (carried): REND CAPPED — only 2 of the 3 Knights carry the break command (2 sources,
  telegraphed), so Safeguard / Maintenance / Steal-Weapon can answer it; breaks are recoverable, NOT a
  loadout-wipe (044 Sluice, 050 Eagrose stair-wall precedents — Rend capped even with 3+ Knights). Monk
  Chakra/revive = sustain, race-able. Ninja = physical tempo, no status lock.
WHAT IS NOT CHANGED: the all-generic shape, the Rend equipment-break wrinkle, the "defeat all" objective,
  and the OPENER lightness remain. No named boss, no rare.
```

## Sanctioned exceptions (carried precedents)

```text
REND EQUIPMENT-BREAK (Knights) — CAPPED at 2 of 3 sources, telegraphed; answer = Safeguard / Maintenance /
  Steal-Weapon; recoverable, NOT a loadout-wipe (044 / 050 precedents). Context-critical (no resupply).
MONK CHAKRA / REVIVE — unarmed sustain; race-able (Ch1 precedent).
NINJA TEMPO (swap) — fast dual-wield flanker; physical, no status lock (045 Mount Germinas precedent).
```

## Boss rare loot

```text
None. No named boss here — no rare boss item (per the Chapter 4 overview tiering). Generics stay
Chapter-4 endgame shop-tier. The four buried Elixir spots are EXISTING loot — leave as-is.
(Tier-S items resume on the gauntlet's bosses: Robe of Lords at Vaults 5th / Loffrey, 055.)
```

## Proposed Composition (New Game++ Vaults Fourth Level v1)

Keep the count (6) and the light-opener feel; swap Archer → Ninja; cap Rend. Endgame-opener band
`101`–`103`. Knights `102` (Rend carriers `103`); Monks `102`; Ninja `103`.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Knight (Rend) | Knight | `103` | Equipment-break source #1 (capped); the gear-preservation wrinkle. |
| n | Knight (Rend) | Knight | `103` | Equipment-break source #2 (capped); the second/last break source. |
| n | Knight | Knight | `102` | Front-line body; NO break command (cap held at 2). |
| n | Monk | Monk | `102` | Unarmed melee + Chakra/revive sustain. |
| n | Monk | Monk | `102` | Second Monk; sustain + martial pressure. |
| n | Ninja | Ninja | `103` | Tempo swap (was Archer); fast dual-wield flanker punishing loose formation. |

Reasoning:

The faithful move is **a light, gear-testing opener that escalates by tempo, not by boss pressure**. The
two Rend Knights (`103`) keep the equipment-break wrinkle, capped to 2 sources so Safeguard / Steal-
Weapon can answer it — critical because the next four fights have **no resupply**. The two Monks (`102`)
bring martial sustain; the **Ninja `103`** (replacing the Archer) adds an endgame flanker so the 1/5★
warm-up becomes a tight ~2/5★ gate without becoming a boss fight. No rare (no boss); the buried Elixirs
remain the reward for clearing the vault.

## Builds (Chapter-4 endgame generics; vault-guard flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Knight x2 (Lv 103) — Rend carriers (capped)

```text
Job: Knight (id TBD)   JobLevel: 8   Primary: Battle Skill (Rend Weapon / Rend Armor — the 2 capped sources)
Reaction: Reflexes (449)   Support: Defense Boost (id TBD)   Movement: Move +1 (486)
Head: heavy helm (id TBD)   Body: heavy armor (id TBD)   Accessory: shop accessory (id TBD)
Right hand: knight sword (id TBD)   Left: shield (id TBD)
ONLY these two carry the break command — answer with Safeguard / Steal-Weapon. Recoverable.
```

Role: the equipment-break wrinkle, capped and telegraphed.

### Knight x1 (Lv 102) — front-line body (no break)

```text
Job: Knight (id TBD)   JobLevel: 8   Primary: Battle Skill — NO Rend (cap held at 2).
Reaction: Reflexes (449)   Support: Defense Boost (id TBD)   Movement: Move +1 (486)
Right hand: knight sword (id TBD)   Left: shield (id TBD)
```

Role: a third armored body without adding a break source.

### Monk x2 (Lv 102) — martial sustain

```text
Job: Monk (id TBD)   JobLevel: 8   Primary: Martial Arts (Chakra / Revive sustain + unarmed hits)
Reaction: Counter (442)   Support: Attack Boost (465)   Movement: Move +1 (486)
Head/Body: martial gear (id TBD)   Accessory: Featherweave Cloak (234)
```

Role: unarmed melee + Chakra/revive; the skirmish's staying power.

### Ninja (Lv 103) — tempo swap

```text
Job: Ninja (id TBD)   JobLevel: 8   Primary: dual-wield strikes (+ Throw optional)
Reaction: Reflexes (449)   Support: Dual Wield (id TBD)   Movement: Move +2 (id TBD)
Right/Left hand: shop ninja blades (id TBD)   Accessory: Featherweave Cloak (234)
```

Role: fast flanker (was Archer); punishes loose formation in the vault corridors.

## Positioning Plan

```text
The Monastery Vaults: cramped stone descent / vault corridors beneath Orbonne. Place the 3 Knights as
  a front wall (the 2 Rend carriers leading), the 2 Monks behind as sustain, and the Ninja on a flank
  to exploit a stretched party. Keep the corridor chokepoints (they make the Rend Knights a real wall).
Preserve: the all-generic shape, the Rend wrinkle (capped 2), the "defeat all" objective, and the
  OPENER lightness (clearly easier than 50-53). No boss, no rare.
```

The vault entry should say: "the descent's first guards aren't the danger — losing your blade to a Rend
here, with five fights and no merchant ahead, is. Bring Safeguard and keep your gear."

## Implementation Checklist

- [ ] Identify Vaults Fourth Level `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify 3 Knight + 2 Monk + 1 Archer, no named boss.
- [ ] Swap the Archer slot → Ninja; keep 3 Knight + 2 Monk.
- [ ] CAP Rend to 2 of 3 Knights (answerable; not a loadout-wipe at the gauntlet's start).
- [ ] Set levels: Rend Knights & Ninja `103`; third Knight & Monks `102`. JobLevel `8` on all slots.
- [ ] Patch via the correct layer; keep the diff inside the Vaults Fourth Level window only.
- [ ] Re-dump and diff; confirm small, intentional changes; verify the roster + Rend cap.
- [ ] Install mod, test from a New Game+ save; confirm it plays as a LIGHT opener, Rend is answerable,
      and gear can be preserved into the no-resupply gauntlet.

## Test Questions

- Is it clearly the LIGHTEST of the final five (a ~2/5★ gear-preservation gate, not a boss fight)?
- Is the Rend equipment-break answerable (capped 2 sources; Safeguard / Steal-Weapon) and recoverable —
  not a loadout-wipe that cripples the rest of the gauntlet?
- Does the Ninja add real tempo (punishing a loose formation) without overstepping the opener's role?
- Is gear-preservation the felt lesson (no resupply ahead)?
- Is it survivable on ONE loadout as the FIRST of five consecutive no-resupply fights?
- Does it read as the vault's first guards, not a designed arena?

## Sources

- Game8, "Monastery Vaults: Fourth Level Walkthrough (Battle 49)": roster (3 Knight + 2 Monk + 1
  Archer), "Defeat all enemies!", rec 60+, 1/5 stars, equipment-break Knights + Safeguard advice, "final
  five consecutive fights" context, spoils 32,800 Gil + buried Elixirs, no rare gear.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553225
- Game8, Chapter 4 hub (endgame battle list / page IDs 553225-553229).
  https://game8.co/games/Final-Fantasy-Tactics/archives/543560
- Local: `037-chapter-4-overview.md` (gauntlet + tiering), `044-fort-besselat-sluice.md` &
  `050-eagrose-castle.md` (Rend-cap precedents), `045-mount-germinas.md` (Ninja tempo swap),
  `055-monastery-vaults-fifth-level.md` (gauntlet 2/5 — to be designed).
```
