# 049 - Limberry Castle Undercroft

Status: ✅ implemented (v1, entry 457) — see reward + verify notes below
Chapter: 4 — "In the Name of Love"
Battle order: Battle 44 (Limberry chain 3 of 3 — NO resupply across 42→43→44; the capstone)
Target version: Enhanced v1.5.0
ENTD: global entry **457** (local 73, entd4)
File: `battle_entd4_ent.bin`

## Implemented (v1, entry 457)

```text
DATA (verified from entd4 dump + JobData InnateStatus/MonsterGraphic):
  slot 1 = Zalera (job 62 "Float", name n62, lvl 44 jl8, eq=255 Lucavi no-equip)  -> the boss.
  slots 2,3 = job 61 (InnateStatus Undead, gfx0 humanoid)                          -> 2 undead Knights.
  slots 4,5,6,8,9 = jobs 109/110/111 (Undead, gfx6)                -> Skeleton/Bonesnatch/Skeletal Fiend.
  slot 7 = job 42 / name 0x2a, tail "00.." (guest), eq=(153,206,213,34,136) = Save the Queen + AEGIS
           SHIELD (136) + Luminous Robe -> MELIADOUL, the guest who JOINS after this battle. (Strong
           Undercroft signal: she recruits right after.) Left untouched -> her gear reaches the player.
  slot 0 = Elmdor (job 27, name 0x1b, lvl 43 jl8) BUT eq=255 (no gear, unlike his fully-equipped Keep
           appearance at 456). Most likely a scripted/cameo unit, not a lootable combatant. LEFT
           UNTOUCHED (preserve scripting). >>> VERIFY IN-GAME whether this Elmdor is an active enemy;
           if he fights, a follow-up will scale him to ~104.

CHANGE (faithful, minimal): LEVEL only on the active foes.
  Zalera = 105 (the lone Lucavi spike)   2 undead Knights = 103   skeleton family = 103
  Win-cond ("Defeat Zalera"), Zalera's mass-status kit, and every UNDEAD/reraise innate preserved.

REWARD NOTE (Tier-A AEGIS SHIELD): Zalera is eq=255 (no equip slots) -> the shield CANNOT be equipped
  on him via ENTD (same limitation as the Belias Defense Ring). It is already delivered via Meliadoul's
  join gear (slot 7 carries an Aegis Shield). For a guaranteed boss-drop copy, the map Move-Find reward
  layer is the clean path -> flagged as a reward-layer follow-up. No fake equip placed on the boss.
```

> Data-layer fields (BattleId, ENTD entry, slot offsets) are placeholders until dumped from
> the real game files. This doc is the design; the byte patch is applied on the Windows box.
> See `037-chapter-4-overview.md`. LIMBERRY CHAIN: 42 (`047`) → 43 (`048`) → 44 (`049`), one loadout.
> Meliadoul Tengille joins permanently AFTER this battle.

## Original Battle

Objective:

```text
Defeat Zalera!   (the third Lucavi — defeating Zalera ends the battle)
```

Player deployment:

```text
Up to 5 units, including Ramza. No guests. NO outfitter access (chain 3/3 capstone).
```

Original enemy composition (verified via Game8, Battle 44):

```text
Zalera (Death Seraph)   (BOSS — Lucavi; continuous MASS STATUS magic)
2x Knight (undead)      (undead front-line)
1x Skeleton             (undead)
1x Bonesnatch           (undead)
1x Skeletal Fiend       (undead)
```

Public walkthrough details:

```text
Recommended level: ~60.  Difficulty: 3/5 stars.  Deploy up to 5.  NO resupply (Limberry chain 3/3).
Win: "Defeat Zalera!" (his death ends it).  Undercroft / graveyard (underground) terrain.
THE THREAT — ZALERA, the status Lucavi: he "continuously casts status ailment spells," hitting MULTIPLE
  party members with STOP, DOOM, SLEEP, CONFUSE, TOAD (Confuseja called out). This mass-status spam is
  the whole danger — NOT raw damage.
ESCORT: 2 undead Knights + Skeleton + Bonesnatch + Skeletal Fiend — an all-UNDEAD guard (reraise; weak
  to Holy / Phoenix Down).
Lower star rating (3/5) than the Gate/Keep (5/5): predictable undead + a single status source you can
  answer with resist/cleanse and by bursting Zalera.
Rewards: 41,900 Gil; buried (Gastrophetes, Obelisk, Eight-Fluted Pole). Meliadoul joins after.
```

Design reading:

The Undercroft is **the status-Lucavi capstone** of the Limberry gauntlet — the third Lucavi of the
mod (after Cúchulainn in Ch2 and Belias/Velius in Ch3), and a deliberate **mechanical contrast** to
them: where Velius (`034`) was mass-AoE *damage*, Zalera is mass-*status* — Stop, Doom, Sleep, Confuse,
Toad raining on the party. Its identity is **a status-survival boss fight**: ward and cleanse the
ailments, keep enough units acting, and **burst the Death Seraph** before his status spam unravels your
formation, all while an all-undead guard (that reraises) screens him. The 3/5★ rating reflects that the
answers are clear (status-resist gear, Esuna/Remedy, Holy/PD on the undead, focus the boss) — it's the
*exhale* after the brutal Keep, but still a Lucavi.

For New Game++ the identity must stay: **a status-Lucavi capstone — survive and cleanse Zalera's ONE
telegraphed mass-status source while permakilling his undead guard, and burst him to win — on no
resupply; with the status kept resistable and non-locking (no unavoidable party-wide Stop), and a
Tier-A status-warding drop on his death.**

## Local Data Confirmed

```text
TBD — dump entry on Windows and fill the slot table here, like 001-gariland.
Confirm slots: Zalera (boss) + 2 undead Knight + Skeleton + Bonesnatch + Skeletal Fiend, + player slots.
  NO outfitter (chain 3/3).
Keep win = "Defeat Zalera" (his death ends it) + the undercroft geometry + every ADD flagged UNDEAD
  (reraise; Holy/PD weakness).
Keep Zalera's MASS-STATUS identity BUT constrain it (below): ONE telegraphed source, resistable,
  cleansable, NON-LOCKING (no chained party-wide Stop/Doom).
This is the Lucavi spike of the chain: Zalera 105, undead adds 103. ONE Tier-A rare on Zalera.
Confirm whether OverrideEntryData carries Level for this battle or leaves it at -1.
Leave the buried map treasure (Gastrophetes, Obelisk, etc.) as-is — map loot. Meliadoul recruits after.
```

Job IDs (carry over known, verify the rest in-game):

```text
Zalera / Death Seraph id   (TBD - verify; Lucavi boss)
Knight job id              (TBD - verify; undead-flagged here)
Skeleton / Bonesnatch / Skeletal Fiend ids (TBD - verify; undead monsters)
```

## Job Escalation (Chapter 4 rule)

```text
CHANGE: NO new generic caste. The escalation is the BOSS — Zalera, the third Lucavi, a MASS-STATUS demon
  (distinct from Velius's mass-AoE-damage at 034). His all-undead guard reprises the reraise puzzle.
WHY: the fight's identity is already "survive the status demon and burst him through an undead screen."
  The faithful Ch4 escalation is a NEW FLAVOR of Lucavi (status instead of damage) — not a second bolt-on
  mechanic. The mass-status survival IS the one new demand vs the Keep's parry race.
CONSTRAINTS (carry Lucavi precedent 034 + the boss mass-status cap, and the no-hard-lock rule):
  - Zalera is the ONE mass-status source. Effects (Stop/Doom/Sleep/Confuse/Toad) must be RESISTABLE
    (status-resist gear) and CLEANSABLE (Esuna/Remedy), and CANNOT chain into a party-wide lock — he may
    not perma-Stop/Doom the whole squad. DOOM is a countdown the player can race/cleanse, not instant death.
  - Telegraphed casts (normal cadence), spaceable AoE — survivable for a prepared party WITHOUT blanket
    immunity (mirror the Gate's balanced-build philosophy, 047).
  - Undead adds: reraise preserved AS counterplay (Holy / Phoenix Down / Seal Evil), per 032/046.
WHAT IS NOT CHANGED: the "defeat Zalera to win" shape, the all-undead guard, and the undercroft remain.
```

## Sanctioned exceptions (carried precedents)

```text
LUCAVI MASS-STATUS (Zalera) — allowed as his identity BUT the ONE source, resistable + cleansable +
  NON-LOCKING (no chained party-wide Stop/Doom); telegraphed, spaceable; Doom = a race-able countdown.
  This is the boss mass-status cap (034) applied to a status Lucavi. NO hard lock.
UNDEAD RERAISE (the guard) — preserved as mechanic AND counterplay (Holy / PD / Seal Evil), per 032/046.
LUCAVI SPIKE — Zalera at 105 (the chain's top band), consistent with Velius (034). One spike, not a wall.
```

## Boss rare loot

```text
ZALERA (boss, DIES here) drops/carries ONE Tier-A rare: AEGIS SHIELD (best magic-evade + status-ward
  shield below the Tier-S shields).
WHY IT FITS: the demon who drowns you in status magic drops the shield that WARDS magic and status —
  a thematic, identity-true reward and a real prize. It is the best non-ultimate shield, a clear Tier-A.
TIER: A (mid-Chapter-4 best non-ultimate). NOT Tier-S: Escutcheon (best phys-evade shield) stays
  reserved for the endgame (47-53); Genji Shield is Elmdor-set themed.
He DIES here (win = defeat Zalera), so the rare pays out — consistent with "retreat/flee = no drop."
The undead guard are monster/undead bodies (no boss loot). Buried map treasure stays as-is.
```

## Proposed Composition (New Game++ Limberry Undercroft v1)

Keep the count (6) and the status-Lucavi capstone shape; Zalera the spike, undead guard the screen.
Zalera `105`; undead adds `103`. No resupply (chain 3/3) — tune status to be survivable on one loadout.

| Slot | Role | Job | Level | Purpose |
|------|------|-----|-------|---------|
| n | Zalera (BOSS) | Death Seraph (Lucavi) | `105` | The status spike; ONE mass-status source; Aegis Shield drop. |
| n | Knight (undead) | Knight | `103` | Undead front-line; reraises; screens Zalera. |
| n | Knight (undead) | Knight | `103` | Second undead body; Rend (≤2 cap — these two only). |
| n | Skeleton (undead) | Skeleton | `103` | Undead body; reraise pressure. |
| n | Bonesnatch (undead) | Bonesnatch | `103` | Undead body; status bite (minor, resistable). |
| n | Skeletal Fiend (undead) | Skeletal Fiend | `103` | Undead body; the heaviest skeleton. |

Reasoning:

The faithful move is to **make Zalera's status the whole puzzle and keep it fair**. At `105` he is the
chain's spike, but his danger is mass status — constrained to one telegraphed, resistable, cleansable,
non-locking source so a prepared party survives without blanket immunity and can burst him. The
all-undead guard (`103`) reprises the reraise puzzle (Holy/PD permakill) as the screen. Because the win
is *defeat Zalera*, the line is: ward/cleanse the status, permakill or ignore the undead, and focus the
Seraph. No resupply means the status must be survivable on one loadout (no guaranteed party-wipe combo).
His death drops the Aegis Shield (Tier-A), and Meliadoul joins after.

## Builds (Chapter-4 boss quality; death-Lucavi crypt flavor)

Item/skill IDs from the loader tables (verify against the installed copy before patching):

```text
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\ItemData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\AbilityData.xml
C:\Reloaded-II\Mods\fftivc.utility.modloader\TableData\JobCommandData.xml
```

### Zalera (Lv 105) — BOSS (Death Seraph Lucavi)

```text
Job: Death Seraph / Zalera (id TBD)   JobLevel: 8   Primary: status magic (Stop/Doom/Sleep/Confuse/Toad)
  — ONE source, telegraphed, resistable, cleansable, NON-LOCKING (no chained party-wide lock); Doom is
  a race-able countdown. Secondary: light demon attack.
Reaction: (anti-burst) Counter Magic / MA-up (id TBD)   Support: MA-boost (id TBD)
  Movement: Movement +1 (486) / float (id TBD)
Body/accessory: innate Lucavi (no normal equip) — drops AEGIS SHIELD (Tier-A) on death.
```

Role: the status spike and objective — ward/cleanse his ailments and burst him; do NOT let him
perma-lock the party. His death pays the Aegis Shield.

### Undead guard x5 (Lv 103) — reraising screen

```text
Knights (undead, id TBD): JobLevel 8; Rend on the 2 Knights ONLY (≤2-break-source cap); UNDEAD flag ON.
  Reaction: Counter (442)   Support: Attack Boost (465)   Body: shop heavy armor   Right: knight sword.
Skeleton / Bonesnatch / Skeletal Fiend (monsters, ids TBD): UNDEAD flag ON; innate skeleton kit
  (claw / status bite — minor, resistable). No equipment slots. Set LEVEL only.
All five reraise (Holy / Phoenix Down / Seal Evil permakill them).
```

Role: the undead screen between the player and Zalera; reraise pressure answered by Holy/PD.

## Positioning Plan

```text
Undercroft/graveyard: Zalera starts central/back with mass-status sightlines onto the party (telegraphed,
  spaceable), the five undead bodies forming the screen the player must permakill or push through.
Preserve the undercroft geometry + every UNDEAD flag + reraise; keep Zalera's status ONE source and
  spaceable (the player can break line / spread to limit the multi-target hits).
Tune for NO resupply: status survivable on one loadout (resist + cleanse), no party-wide lock, Doom
  race-able. Zalera the lone 105 spike; undead at 103.
```

The crypt should say: "the death-angel buries your will under a tide of curses — ward your minds, burn
the bones for good, and cut him down before the silence takes you."

## Implementation Checklist

- [ ] Identify Limberry Undercroft `BattleId` / ENTD entry on Windows data; fill "Local Data Confirmed".
- [ ] Dump original entry; verify Zalera + 2 undead Knight + Skeleton + Bonesnatch + Skeletal Fiend + slots.
- [ ] Keep win = "Defeat Zalera"; keep the undercroft geometry + all ADDS undead (reraise, Holy/PD weak).
- [ ] Set Zalera `105` as the ONE mass-status source — resistable, cleansable, NON-LOCKING; Doom race-able.
- [ ] Equip the drop: AEGIS SHIELD (Tier-A) on Zalera's death.
- [ ] Limit Rend to the 2 undead Knights; keep skeleton status bites minor/resistable.
- [ ] Set undead adds `103`; JobLevel `8` on job slots.
- [ ] Tune status lethality to ONE loadout (chain 3/3, no resupply) — no guaranteed party-wipe combo.
- [ ] Patch via the correct layer; keep the diff inside the Undercroft window only.
- [ ] Re-dump and diff; confirm changes are small and intentional; verify status caps + undead + drop.
- [ ] Install mod, test from a New Game+ save (chain-realistic resources); confirm no party-wide lock,
      Doom is survivable, undead permakillable, Zalera burst-able, Aegis Shield drops, Meliadoul recruits.

## Test Questions

- Is Zalera's mass status a FAIR survival puzzle (one source, resistable, cleansable, NON-LOCKING) —
  never an unavoidable party-wide Stop/Doom lock, with Doom race-able?
- Is the fight survivable WITHOUT blanket status immunity (balanced-build philosophy, like the Gate)?
- Do the undead adds reraise with the usual answers (Holy / PD / Seal Evil), as a screen not a wall?
- Does "Defeat Zalera ends it" keep it a focus race; does his death drop the Tier-A Aegis Shield?
- Is Zalera the lone `105` spike (undead `103`) — a Lucavi capstone, not an over-wall — and survivable
  on ONE loadout (no resupply)?
- Does it read as the death-angel crypt and the climax of the Limberry gauntlet (with Meliadoul joining)?

## Sources

- Game8, "Limberry Castle Undercroft Walkthrough (Battle 44)": roster (Zalera boss + 2 undead Knight +
  Skeleton + Bonesnatch + Skeletal Fiend), objective "Defeat Zalera!", rec ~60, 3/5 stars, deploy 5,
  Zalera's mass status (Stop/Doom/Sleep/Confuse/Toad, Confuseja), no resupply (Limberry chain), buried
  treasure (Gastrophetes, Obelisk), Meliadoul recruits after.
  https://game8.co/games/Final-Fantasy-Tactics/archives/553204
- Final Fantasy Wiki, "Zalera" / "Limberry Castle": story/terrain context.
  https://finalfantasy.fandom.com/wiki/Zalera
- Local: `037-chapter-4-overview.md` (rules), `034-riovanes-castle-keep.md` (Velius — the Ch3 Lucavi /
  boss mass-effect cap precedent), `046-poeskas-lake.md` (undead reraise handling),
  `047`/`048` (Limberry chain 1-2).
```
</content>
