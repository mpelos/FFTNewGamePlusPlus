#!/usr/bin/env python3
"""
Data-driven story battle patcher for the New Game++ code mod.

Edits the EMBEDDED modded ENTD (src/fftivc.battles.ngplus/entd/battle_entd4_ent.bin)
in place. Because the whole file is swapped only in NG+ by the code mod, every edit here
is automatically NG+-only. Guests are scaled separately at runtime, so we never touch
guest/player slots.

Field map (0x28-byte slot), VERIFIED against the in-game-validated Gariland (entry 388):
  +0x03 level   +0x08 JobUnlock / roster JP target  +0x09 JobLevel seed  +0x0A mainJob  +0x0B secondary
  +0x0C reaction(u16)  +0x0E support(u16)  +0x10 movement(u16)
  +0x12 head  +0x13 body  +0x14 accessory  +0x15 rightHand  +0x16 leftHand
Untouched on a re-tune: sprite/flags/name/brave/faith/position (preserve the
working vanilla unit skeleton). Only convert mainJob when the design changes the job.
For named guest job-level seeding, +0x08 is NOT a visible rank: +0x08=7 gave Delita
Time Mage Job Level 8. Known Chapter-1 Squire guest records use +0x08=1 in vanilla,
so the current Squire Job Level 8 test uses +0x08=1 and +0x09=8.

Run:  python tools/battle_patch.py <battle> [<battle> ...]   (or "all")
"""
from __future__ import annotations

import struct
import sys
from pathlib import Path

EMBED = Path("src/fftivc.battles.ngplus/entd/battle_entd4_ent.bin")
VANILLA = Path("extracted/enhanced_0002_selected/fftpack/battle_entd4_ent.bin")
ENTRY = 0x280
SLOT = 0x28
SPOILS_OFFSET = 0x1E
CONTROL_OFFSET = 0x18
PLAYER_CONTROL_BIT = 0x08
EMPTY_SLOT = bytes.fromhex(
    "00 00 ff fe fe fe fe fe 00 00 00 00 fe 01 fe 01 fe 01 fe fe"
    " fe fe fe 00 00 00 00 00 fe ff 00 00 ff 00 00 00 00 00 00 00"
)

# --- verified IDs (from Gariland 001 doc, validated in-game) ---
# jobs
SQUIRE, CHEMIST, ARCHER, THIEF = 74, 75, 77, 83
KNIGHT, BMAGE, MONK, WMAGE, TMAGE = 76, 80, 78, 79, 81
ENEMY_BMAGE, ENEMY_TMAGE = 66, 68  # Yuguewood enemy-variant casters; keep their job identities.
LANCER = 87  # Dragoon (innate Jump command); Ch2 vertical-threat escalation
SUMMONER = 82  # Summon command innate; Ch2 marquee caster (Balias Tor / Goug)
ORATOR = 84   # Mediator — Ch3 charm/status caste (Gollund debut); equips Hat/Clothing/Robe/Gun/Knife
GEOMANCER = 86  # terrain elemental attacks (Ch3 debut, Balias Swale 019); equips Hat/Clothing/Robe/Sword
NINJA = 89    # dual-wield/wall-climb/Throw — Ch3 marquee caste (Yardow)
SAMURAI = 88  # Bushido/draw-out — Ch3 elite
MYSTIC = 85   # Oracle-equivalent — soft status; equips Hat/Robe/Clothing/Rod/Staff/Book (Ch4 Zalmo screen)
ARITHMETICIAN = 90  # Calculator-equivalent; used as a JP/skill bucket seed for Arithmeticks.
DANCER = 92   # global Dance pressure; ENTD cannot mask learned dances per unit.
MIME = 93     # Mime; used as a broad Archer ability bucket at Mount Germinas.
TEMPLAR = 38  # Knights Templar (Izlude's job, 028) — Mighty Sword ranged breaks; equips Helmet/Armor/
              # Shield/Polearm/KnightSword/Sword/NinjaBlade. Used as a generic swap at Riovanes Gate (033).
# skills
COUNTER, PARRY, ATK_BOOST, MV1, MV2, MV3 = 442, 447, 465, 486, 487, 488
DRAGONHEART = 427
NATURES_WRATH = 437
VIGILANCE = 426
VANISH = 425
SOULBIND = 446
FURY = 422  # table name: Strength Surge; battle docs call this Dancer reaction Fury.
SPEED_SURGE = 424
FIRST_STRIKE, REFLEXES, CONCENTRATION = 453, 449, 469
SHIRAHADORI = 451
DOUBLEHAND = 476
DUAL_WIELD = 477
BRAWLER = 472
TELEPORT = 498
SWIFTSPELL, MAGICK_BOOST, DEFENSE_BOOST = 482, 467, 466  # Ch2 supports: Short-Charge / MA-up / phys-def-up
MAGICK_DEFENSE_BOOST = 468
AUTO_POTION, THROW_ITEMS = 441, 474
FUNDAMENTS = 5
ITEMS = 6
MARTIAL_ARTS = 9
TIME_MAGICKS = 12
PUGILISM = 53
ARTS_OF_WAR = 8
WHITE_MAGICKS = 10
BLACK_MAGICKS = 11
SUMMON = 13
MYSTIC_ARTS = 16
GEOMANCY = 17
MIGHTY_SWORD = 52
HOLY_SWORD_AGRIAS = 0x21
IAIDO = 19
STEAL = 14
SPEECHCRAFT = 15
THROW = 20
# Argath/Ziekden crossbow-sniper kit. IDs resolved from the FFTPatcher PSX tables, which TIC
# reuses 1:1 (verified vs 9 known item anchors: RuneBlade 30, FeatherMantle 234, CrystalShield 139,
# TwistHeadband 163, PowerSleeve 195, etc.). Names cross PSX<->WotL but the ids are identical.
AIM = 8           # Archer secondary skillset (PSX "Charge") — innate ranged charge-up shots
EQUIP_GUNS = 461
EQUIP_HEAVY_ARMOR = 454
MANA_SHIELD = 445 # reaction: redirect HP damage to MP (PSX "MP Switch"); Brave-gated trigger
MOVE_MP_UP = 494  # movement: restore MP each move (WotL "Manafont") — refuels the Mana Shield buffer
IGNORE_HEIGHT = 492
JUMP2 = 490
JUMP3 = 491
# items
HEADBAND, POWER_GARB, BRACERS, ICEBRAND, RUNEBLADE = 163, 195, 218, 29, 30
WINGED_BOOTS = 212
THIEFS_CAP, BLACK_GARB, GERMINAS, AIR_KNIFE, WINDSLASH = 168, 198, 210, 9, 87
YOICHI_BOW, PERSEUS_BOW = 90, 91
FEATHERWEAVE, MYTHRIL_GUN = 234, 72
MAGEPOWER_GLOVES = 217
POWER_GAUNTLETS = 215  # docs sometimes call this "Magic Gauntlet"; table name is Power Gauntlets.
RED_SHOES = 214
WIZARD_ROBE = 202
BLACK_ROBE = 205
OBELISK = 103
SLASHER = 50  # strongest buyable axe (Chapter3_Zalmo shop tier)
X_POTION, ELIXIR, PHOENIX_DOWN = 242, 245, 253
HERMES_SHOES = 213
SORTILEGE = 239  # reserved (Unknown20) female-only Perfume = Always Protect+Shell (EquipBonus 68); used on
                 # must-survive caster VIP Ovelia (Zeirchele) so Protect halves her charging one-shot
GOLDEN_STAFF = 64  # == SHOP_STAFF; Ovelia's MA staff (alias for readability in her VIP slot)
GOLD_HAIRPIN = 166  # Hat (Princess-legal), MP+50/HP+80, buyable (Chapter3_SaveRafa); Ovelia head — HP cushion
GASTROPHETES = 82  # best buyable crossbow (WP 10, PSX "Gastrafitis"); one-handed -> shield-compatible
CRYSTAL_SHIELD = 139  # best buyable shield (== SHOP_SHIELD); high evade -> "hard to hit"
KAISER_SHIELD = 141
VENETIAN_SHIELD = 142
# Dorter additions — strongest SHOP-tier per category (no Unknown20 treasure tier):
HEAVY_HELM, HEAVY_ARMOR, SHOP_SHIELD = 154, 182, 139   # Knight heavy gear (Helmet/Armor/Shield)
MAGE_HAT, SHOP_ROBE, SHOP_ROD = 167, 206, 56           # Black Mage gear (Hat/Robe/Rod)
SHOP_STAFF = 64                                          # White Mage weapon (Staff, MA/heal)
PARTISAN = 102   # strongest pre-Ch4 SHOP-tier spear (Holy Lance/Dragon Whisker are Unknown20/reserved)
WHALE_WHISKER = 114  # rare pole for Zalmo (041); two-handed marker required in LH.
GEMS_108 = 226  # TIC English name: Japa Mala. Docs call it 108 Gems; Ch2 Cuchulainn reward.
BLOOD_SWORD = 23  # HP-drain sword — Ch2 rare boss loot (overview-named); IS Gaffgarion's Shadowblade
                  # sustain in item form, so Steal Weapon both ends his self-heal and claims the prize
LH_EMPTY, LH_TWOHAND = 255, 254  # sword w/ empty offhand vs two-handed marker (bow/gun)
FLAME_SHIELD = 135  # Fire-absorb shield — Ch3 Lesalia band element puzzle (enemy gear, any availability)
MIRROR_MAIL = 184   # auto-Reflect armor — TIC's name for the PSX "Reflect Mail"; Izlude's Ch3 rare (028)
NINJA_BLADE = 14    # Ninja Longblade — best NON-reserved ninja blade available at Yardow (Chapter3_SaveRafa)
DEFENDER = 33       # weakest KnightSword (non-buyable) — Wiegraf's Ch3 rare at the Keep (034); the
                    # reserved best KnightSwords are 34-37 (Save the Queen/Excalibur/Ragnarok/Chaos Blade)
KIKU_ICHIMONJI = 45  # best buyable non-rare katana below Masamune; safe for fleeing Ch3 Elmdor
KOGA_BLADE = 18
IGA_BLADE = 17
ASSASSINS_DAGGER = 8
ZWILL_STRAIGHTBLADE = 10
# --- Chapter 4 best-in-slot rares (Unknown20-reserved tier, unlocked tiered in Ch4 per docs/037) ---
SAVE_THE_QUEEN = 34  # Tier-A KnightSword — Meliadoul (039). Best KnightSword below the Tier-S pair.
CASHMERE = 120       # cloth weapon; former Bervenia Dancer test kit.
MASAMUNE = 46        # Tier-A Katana — Elmdor (048, deferred from Ch3).
CHIRIJIRADEN = 47
GENJI_SHIELD = 140
GENJI_HELM = 155
GENJI_ARMOR = 183    # Tier-A Armor — Elmdor (048).
GENJI_GLOVES = 216
AEGIS_SHIELD = 136   # Tier-A Shield (best magic-evade + status ward) — Zalera (049).
GRAND_HELM = 156     # Tier-A Helmet (best non-Genji) — Adramelk/Dycedarg (050).
MAXIMILLIAN = 185
CHAOS_BLADE = 37     # Tier-S KnightSword — Folmarv (052).
RIBBON = 171         # Tier-S HairAdornment (best headgear) — Zalbaag (053).
HAIRBAND = 169
BARRETTE = 170
NINJA_GEAR = 197
RUBBER_SUIT = 199
ENVOUTEMENT = 237
ESCUTCHEON = 143     # Tier-S Shield (Unknown20 best; paid before the gauntlet at Mullonde Nave 052).
MATERIA_BLADE = 32   # Tier-S Sword (Unknown20; side/relic plan only, not awarded in Lost Halidom 057).
RAGNAROK = 36        # Tier-S KnightSword capstone; paid before the final gauntlet at Sanctuary 053.
STONESHOOTER = 73    # Barich v3 active gun/disarm bait (042).
GLACIAL_GUN = 74     # Tier-A Gun — Barich (042).
BLAZE_GUN = 75
BLASTER = 76
LIGHT_ROBE = 206     # Tier-A robe — Zalmo (041). TIC's Luminous Robe = top robe BELOW Lordly; == SHOP_ROBE
ROBE_OF_LORDS = 207  # Tier-S robe (Lordly Robe, Unknown20 best; paid before the gauntlet at 052).
# --- Ch4 monster job ids (Finath chocobo flock, 040) ---
CHOCOBO, BLACK_CHOCOBO, RED_CHOCOBO, PIG = 94, 95, 96, 121
GOBLIN, BLACK_GOBLIN, GOBBLEDYGOOK = 97, 98, 99
RED_PANTHER, COEURL, VAMPIRE_CAT = 103, 104, 105
SKELETON, BONESNATCH, SKELETAL_FIEND = 109, 110, 111
GHOUL, GHAST, REVENANT = 112, 113, 114
FLOATING_EYE, PLAGUE_HORROR = 115, 117
WILD_BOAR = 123
MALBORO, OCHU = 130, 131


def generic_job_rank(job):
    return job - 0x4A


def set_slot(data, global_entry, slot, *, level=None, jobrank=None, joblevel=None, job=None,
             secondary=None, reaction=None, support=None, movement=None,
             head=None, body=None, acc=None, rh=None, lh=None, brave=None, faith=None,
             palette=None):
    b = (global_entry % 128) * ENTRY + slot * SLOT
    if jobrank is None and job is not None and SQUIRE <= job <= NINJA:
        jobrank = generic_job_rank(job)

    def w8(off, val):
        if val is not None:
            data[b + off] = val

    def w16(off, val):
        if val is not None:
            struct.pack_into("<H", data, b + off, val)

    w8(0x03, level); w8(0x06, brave)  # brave is at 0x06 — NOT 0x05 (verified 2026-06-28: in-game
    w8(0x07, faith)
    # Brave == byte@0x06; the old 0x05 write hit a different field). Re-run + re-verify any battle that
    # set brave via this tool (e.g. Argath/ziekden) — their 0x05 may still hold a stray brave value.
    w8(0x08, jobrank); w8(0x09, joblevel); w8(0x0A, job); w8(0x0B, secondary)
    w16(0x0C, reaction); w16(0x0E, support); w16(0x10, movement)
    w8(0x12, head); w8(0x13, body); w8(0x14, acc); w8(0x15, rh); w8(0x16, lh)
    w8(0x17, palette)


# ---------------------------------------------------------------------------
# Battle 003 — Mandalia Plain (entry 389): re-tune existing 6 enemies, convert
# one Squire -> Archer. Composition per docs/battles/002-mandalia-plain.md.
# Vanilla 389: s2 Thief, s3-s6 Squire, s7 Red Panther(monster j103); s0/s1 guests.
def set_spoil(data, global_entry, slot, item):
    b = (global_entry % 128) * ENTRY + slot * SLOT
    data[b + SPOILS_OFFSET] = item


def set_player_control(data, global_entry, slot):
    b = (global_entry % 128) * ENTRY + slot * SLOT
    data[b + CONTROL_OFFSET] |= PLAYER_CONTROL_BIT


def set_control_flags(data, global_entry, slot, flags):
    b = (global_entry % 128) * ENTRY + slot * SLOT
    data[b + CONTROL_OFFSET] = flags


def clone_slot(data, global_entry, src_slot, dst_slot, *, unitid, x=None, y=None, facing=None,
               clear_spoil=True):
    base = (global_entry % 128) * ENTRY
    src = base + src_slot * SLOT
    dst = base + dst_slot * SLOT
    data[dst:dst + SLOT] = data[src:src + SLOT]
    data[dst + 0x20] = unitid
    if x is not None:
        data[dst + 0x19] = x
    if y is not None:
        data[dst + 0x1A] = y
    if facing is not None:
        data[dst + 0x1B] = facing
    if clear_spoil:
        data[dst + SPOILS_OFFSET] = 0


def set_position(data, global_entry, slot, *, x=None, y=None, facing=None):
    b = (global_entry % 128) * ENTRY + slot * SLOT
    if x is not None:
        data[b + 0x19] = x
    if y is not None:
        data[b + 0x1A] = y
    if facing is not None:
        data[b + 0x1B] = facing


def restore_vanilla_slot(data, global_entry, slot):
    base = (global_entry % 128) * ENTRY
    off = base + slot * SLOT
    data[off:off + SLOT] = VANILLA.read_bytes()[off:off + SLOT]


def clear_slot(data, global_entry, slot):
    base = (global_entry % 128) * ENTRY
    off = base + slot * SLOT
    data[off:off + SLOT] = EMPTY_SLOT


def chapter1_guest_control(data):
    """Make Delita/Argath guest-form slots player-controllable in NG++ Ch1."""
    touched = []
    for global_entry in (384, 385, 386, 388, 389, 392, 395, 399, 400, 401):
        entry_touched = False
        base = (global_entry % 128) * ENTRY
        for slot in range(16):
            b = base + slot * SLOT
            char_id = data[b + 0x00]
            job = data[b + 0x0A]
            if char_id in (0x04, 0x07) and job == char_id:
                set_player_control(data, global_entry, slot)
                entry_touched = True
        if entry_touched:
            touched.append(global_entry)
    return touched


# ---------------------------------------------------------------------------
# Battle 002 - Magick City of Gariland (entry 388): already tuned by hand in
# the first validated build. Keep that build, but bring guest JobLevel and
# Spoils of War into the reproducible patch flow.
def gariland(data):
    E = 388
    # Delita's active Gariland slot: keep JobUnlock on Squire (1), raise that job level to 8.
    # JobUnlock 7 maps to Time Mage in the roster JP grid, not to "visible rank 8".
    set_slot(data, E, 0, level=100, jobrank=1, joblevel=8)

    # Vanilla spoils: Mythril Knife + Phoenix Down + Potion.
    # NG++ spoils preserve categories: Air Knife + Phoenix Down + X-Potion.
    set_spoil(data, E, 1, AIR_KNIFE)
    set_spoil(data, E, 2, PHOENIX_DOWN)
    set_spoil(data, E, 3, X_POTION)

    # Delita's pre-Gariland join/cache record. Only visible from a save before he joins.
    set_slot(data, 392, 1, level=100, jobrank=1, joblevel=8)
    return [388, 392]


def mandalia(data):
    E = 389
    # s3 Brigade leader — Squire L102 (Runeblade)
    set_slot(data, E, 3, level=102, joblevel=8, job=SQUIRE, secondary=0,
             reaction=COUNTER, support=ATK_BOOST, movement=MV1,
             head=HEADBAND, body=POWER_GARB, acc=BRACERS, rh=RUNEBLADE, lh=LH_EMPTY)
    # s4, s5 Brigade soldiers — Squire L100 (Icebrand)
    for s in (4, 5):
        set_slot(data, E, s, level=100, joblevel=8, job=SQUIRE, secondary=0,
                 reaction=COUNTER, support=ATK_BOOST, movement=MV1,
                 head=HEADBAND, body=POWER_GARB, acc=BRACERS, rh=ICEBRAND, lh=LH_EMPTY)
    # s2 Skirmisher — Thief L101 (Air Knife), no secondary (v1)
    set_slot(data, E, 2, level=101, joblevel=8, job=THIEF, secondary=0,
             reaction=FIRST_STRIKE, support=ATK_BOOST, movement=MV2,
             head=THIEFS_CAP, body=BLACK_GARB, acc=GERMINAS, rh=AIR_KNIFE, lh=LH_TWOHAND)
    # s6 Marksman — Squire -> Archer L101 (Windslash Bow), Fundaments secondary
    set_slot(data, E, 6, level=101, joblevel=8, job=ARCHER, secondary=FUNDAMENTS,
             reaction=REFLEXES, support=CONCENTRATION, movement=MV1,
             head=THIEFS_CAP, body=BLACK_GARB, acc=BRACERS, rh=WINDSLASH, lh=LH_TWOHAND)
    # s7 Beast — Red Panther (keep monster), scale level + jobLevel only
    set_slot(data, E, 7, level=101, joblevel=8)
    # s1 Argath (guest ally, job 7) — playtest fix: the runtime guest-scaler gives him PARTY LEVEL
    # (high HP) but his vanilla slot is NAKED (no head/body), so the reckless guest charged in and
    # died fast. Give him endgame, job-7-LEGAL gear (job 7 equips Hat/Robe/Clothing/Sword + accessories
    # only — NO helmet/armor/shield) so he survives. NG+-only (rides the .bin swap); we do NOT set
    # level (the scaler keeps it at party level) or job (keep 7) or secondary. lh stays 254 (two-hand
    # bonus on the 1H sword). Accessory = Featherweave Cloak (best phys+magic EVASION, shop-buyable):
    # for a MUST-SURVIVE guest, evasion (avoid the hit) beats Reraise, which is useless when his death
    # is an instant mission-fail. Reflexes reaction stacks more evade.
    set_slot(data, E, 1, jobrank=7, joblevel=8, reaction=REFLEXES, support=ATK_BOOST, movement=MV1,
             head=THIEFS_CAP, body=BLACK_GARB, acc=FEATHERWEAVE, rh=RUNEBLADE)
    return [E]


# ---------------------------------------------------------------------------
# Battle 004 — Siedge Weald / Sweegy Woods (entry 384): all-monster pack.
# Vanilla 384 .bin monsters s2-s7 (Goblin/BlkGoblin/Bomb/RedPanther); the override remaps the
# monster JOBS (169=RedPanther,170=Goblin,171=BlkGoblin,172=Bomb) but leaves Level/JobLevel = -1,
# so editing the .bin LEVEL + JOBLEVEL is what scales them. Monsters carry no gear / no R-S-M edits.
# Per docs/battles/003-siedge-weald.md: Goblins 100; Red Panther / Black Goblin / Bombs 101.
def sweegy(data):
    E = 384
    set_slot(data, E, 2, level=100, joblevel=8)  # Goblin
    set_slot(data, E, 3, level=100, joblevel=8)  # Goblin
    set_slot(data, E, 4, level=101, joblevel=8)  # Black Goblin
    set_slot(data, E, 5, level=101, joblevel=8)  # Bomb
    set_slot(data, E, 6, level=101, joblevel=8)  # Bomb
    set_slot(data, E, 7, level=101, joblevel=8)  # Red Panther
    return [E]


# ---------------------------------------------------------------------------
# Battle 005 — Dorter Slums (entry 385): the rooftop ranged+magic spike.
# Vanilla 385: s3 Knight, s4-s6 Archer, s7-s8 Black Mage (s0/s1 guests, s2 a story slot).
# Keep vanilla positions (they already are the iconic rooftop layout). Per docs 004.
def dorter(data):
    E = 385
    # s3 Ground anchor — Knight L102: heavy helm/armor + shield, sword. NO break skillset.
    set_slot(data, E, 3, level=102, joblevel=8, job=KNIGHT, secondary=0,
             reaction=COUNTER, support=ATK_BOOST, movement=MV1,
             head=HEAVY_HELM, body=HEAVY_ARMOR, acc=BRACERS, rh=RUNEBLADE, lh=SHOP_SHIELD)
    # s4 Rooftop sniper + s5 rooftop archer — Archer L101 (Concentration + Windslash Bow)
    for s in (4, 5):
        set_slot(data, E, s, level=101, joblevel=8, job=ARCHER, secondary=FUNDAMENTS,
                 reaction=REFLEXES, support=CONCENTRATION, movement=MV1,
                 head=THIEFS_CAP, body=BLACK_GARB, acc=BRACERS, rh=WINDSLASH, lh=LH_TWOHAND)
    # s6 Street archer — Archer L100
    set_slot(data, E, 6, level=100, joblevel=8, job=ARCHER, secondary=FUNDAMENTS,
             reaction=REFLEXES, support=CONCENTRATION, movement=MV1,
             head=THIEFS_CAP, body=BLACK_GARB, acc=BRACERS, rh=WINDSLASH, lh=LH_TWOHAND)
    # s7, s8 Black Mage L101 — robe/rod for AoE. Support left vanilla (no confirmed MA-boost id).
    for s in (7, 8):
        set_slot(data, E, s, level=101, joblevel=8, job=BMAGE, secondary=0,
                 reaction=REFLEXES, movement=MV1,
                 head=MAGE_HAT, body=SHOP_ROBE, acc=FEATHERWEAVE, rh=SHOP_ROD, lh=LH_EMPTY)
    return [E]


# ---------------------------------------------------------------------------
# Battle 006 — Sand Rat Sietch (entry 386): cramped melee attrition, split party.
# Vanilla 386: s2/s5/s6 Knight, s3 Archer, s4/s7 Monk (s0/s1 guests). Keep vanilla positions
# (the chokepoint layout) and the split player zones. Per docs 005.
def sand_rat(data):
    E = 386
    # 3 Knights: captain L102 (s2), then L101 (s5), L100 (s6). Shop heavy gear + sword + shield.
    for s, lvl in ((2, 102), (5, 101), (6, 100)):
        set_slot(data, E, s, level=lvl, jobrank=generic_job_rank(KNIGHT), joblevel=8,
                 job=KNIGHT, secondary=0,
                 reaction=COUNTER, support=ATK_BOOST, movement=MV1,
                 head=HEAVY_HELM, body=HEAVY_ARMOR, acc=BRACERS, rh=RUNEBLADE, lh=SHOP_SHIELD)
    # 2 Monks L101 (s4, s7): bare-handed (Martial Arts) — leave RH/LH vanilla; PA hat+clothing.
    for s in (4, 7):
        set_slot(data, E, s, level=101, joblevel=8, job=MONK, secondary=0,
                 reaction=COUNTER, support=ATK_BOOST, movement=MV1,
                 head=HEADBAND, body=POWER_GARB, acc=BRACERS)
    # Archer L100 (s3): corridor poke.
    set_slot(data, E, 3, level=100, joblevel=8, job=ARCHER, secondary=FUNDAMENTS,
             reaction=REFLEXES, support=CONCENTRATION, movement=MV1,
             head=THIEFS_CAP, body=BLACK_GARB, acc=BRACERS, rh=WINDSLASH, lh=LH_TWOHAND)
    return [E]


# ---------------------------------------------------------------------------
# Battle 007 — Brigands' Den (entry 395): first named boss (Milleuda) + healers + thieves.
# Vanilla 395: s2 = Milleuda (BOSS, name_id=75, Knight-class cid 0x81) — set_slot preserves her
# identity bytes (name_id/cid/unitid/flags), so gearing her is safe; s3,s4 White Mage; s5-s7 Thief
# (s0/s1 guests). No OverrideEntryData. Per docs 006. Boss-kill objective targets her by id (kept).
def brigands(data):
    E = 395
    # Milleuda (boss) L102 — durable Knight-class boss, NON-unique shop gear + focus-fire reaction.
    set_slot(data, E, 2, level=102, joblevel=8, job=KNIGHT, secondary=FUNDAMENTS,
             reaction=COUNTER, support=ATK_BOOST, movement=MV1,
             head=HEAVY_HELM, body=HEAVY_ARMOR, acc=BRACERS, rh=RUNEBLADE, lh=SHOP_SHIELD)
    # 2 White Mages L101 (s3,s4): sustain engines — robe/staff. Support left vanilla.
    for s in (3, 4):
        set_slot(data, E, s, level=101, joblevel=8, job=WMAGE, secondary=0,
                 reaction=REFLEXES, movement=MV1,
                 head=MAGE_HAT, body=SHOP_ROBE, acc=FEATHERWEAVE, rh=SHOP_STAFF, lh=LH_EMPTY)
    # 3 Thieves L100 (s5,s6,s7): fast harassers (Gariland-validated thief build).
    for s in (5, 6, 7):
        set_slot(data, E, s, level=100, joblevel=8, job=THIEF, secondary=0,
                 reaction=FIRST_STRIKE, support=ATK_BOOST, movement=MV2,
                 head=THIEFS_CAP, body=BLACK_GARB, acc=GERMINAS, rh=AIR_KNIFE, lh=LH_TWOHAND)
    return [E]


# ---------------------------------------------------------------------------
# Battle 008 — Lenalian Plateau (entry 399): Milleuda rematch, mage-heavy + Time Mage.
# Vanilla 399: s1 = Milleuda (BOSS, name_id=75); s2,s6 Knight; s3,s5 Black Mage; s4 Time Mage
# (s0 guest Delita only — Argath has left by now). No OverrideEntryData. Per docs 007.
# Time Mage JobLevel is CAPPED low so it sticks to early-tier Time magic (Haste/Slow) and does
# NOT get hard lockdown (Stop/Immobilize), per the doc's explicit control limit. Verify in-game.
def lenalian(data):
    E = 399
    # Milleuda (boss) L102 — same durable non-unique kit as Brigands' (identity bytes preserved).
    set_slot(data, E, 1, level=102, joblevel=8, job=KNIGHT, secondary=FUNDAMENTS,
             reaction=COUNTER, support=ATK_BOOST, movement=MV1,
             head=HEAVY_HELM, body=HEAVY_ARMOR, acc=BRACERS, rh=RUNEBLADE, lh=SHOP_SHIELD)
    # Knights: s2 L101 (lead), s6 L100.
    for s, lvl in ((2, 101), (6, 100)):
        set_slot(data, E, s, level=lvl, joblevel=8, job=KNIGHT, secondary=0,
                 reaction=COUNTER, support=ATK_BOOST, movement=MV1,
                 head=HEAVY_HELM, body=HEAVY_ARMOR, acc=BRACERS, rh=RUNEBLADE, lh=SHOP_SHIELD)
    # Black Mages L101 (s3,s5): AoE threat. Support left vanilla.
    for s in (3, 5):
        set_slot(data, E, s, level=101, joblevel=8, job=BMAGE, secondary=0,
                 reaction=REFLEXES, movement=MV1,
                 head=MAGE_HAT, body=SHOP_ROBE, acc=FEATHERWEAVE, rh=SHOP_ROD, lh=LH_EMPTY)
    # Time Mage L101 (s4): JobLevel capped to 4 to limit it to Haste/Slow (no hard lockdown).
    set_slot(data, E, 4, level=101, joblevel=4, job=TMAGE, secondary=0,
             reaction=REFLEXES, movement=MV1,
             head=MAGE_HAT, body=SHOP_ROBE, acc=FEATHERWEAVE, rh=SHOP_ROD, lh=LH_EMPTY)
    return [E]


# ---------------------------------------------------------------------------
# Battle 009 — Fovoham Windflats (entry 400): Wiegraf duel, the pre-finale spike.
# Vanilla 400: s1 = Wiegraf (BOSS, cid 0x20, job 32 = Holy Knight w/ Judgment Blade, name_id=32);
# s2 = Chocobo (monster, override MainJob->173, level via .bin); s3 Knight; s4,s5 Monk (s0 guest
# Delita). Per docs 008. CRITICAL: do NOT change Wiegraf's job (32) or secondary — that IS his
# Holy Sword skillset (Judgment Blade). We only scale his level/JobLevel and upgrade gear (keeping
# a breakable sword so Rend Weapon stays the intended counter). set_slot preserves identity bytes.
def fovoham(data):
    E = 400
    # Wiegraf (boss) L103 — keep job 32 + his sword skillset; upgrade to durable non-unique gear.
    set_slot(data, E, 1, level=103, joblevel=8,
             reaction=COUNTER, support=ATK_BOOST, movement=MV1,
             head=HEAVY_HELM, body=HEAVY_ARMOR, acc=BRACERS, rh=RUNEBLADE, lh=SHOP_SHIELD)
    # Chocobo (monster, override-jobbed) L100 — scale level + JobLevel only.
    set_slot(data, E, 2, level=100, joblevel=8)
    # Knight L101 (s3): bodyguard wall.
    set_slot(data, E, 3, level=101, joblevel=8, job=KNIGHT, secondary=0,
             reaction=COUNTER, support=ATK_BOOST, movement=MV1,
             head=HEAVY_HELM, body=HEAVY_ARMOR, acc=BRACERS, rh=RUNEBLADE, lh=SHOP_SHIELD)
    # 2 Monks L101 (s4,s5): bare-handed bruisers (Martial Arts), PA hat+clothing.
    for s in (4, 5):
        set_slot(data, E, s, level=101, joblevel=8, job=MONK, secondary=0,
                 reaction=COUNTER, support=ATK_BOOST, movement=MV1,
                 head=HEADBAND, body=POWER_GARB, acc=BRACERS)
    return [E]


# ---------------------------------------------------------------------------
# Battle 010 — Ziekden Fortress (entry 401): the Chapter 1 FINALE. Argath boss + escort.
# Vanilla 401: s0 = Argath (cid 0x07, BOSS — re-jobbed to Knight 76, name_id=7); s1 = Tietra
# (cid 0x08, name 8, lvl 254 = scripted hostage); s2 = cid 0x1c name 28 lvl 254 (scripted cutscene
# actor); s3-s7 = 5 generic Knights (job 76); s8 = Delita guest (cid 0x04); s9,s10 = Black Mages
# (cid 0x81, job 80). Per docs/battles/009-ziekden-fortress.md. CRITICAL:
#  - Argath's slot uses guest charId 0x07; the code mod's guest-scaler skips it ONLY because his job
#    (76) != charId (7), so his .bin level stands. set_slot preserves identity bytes (name_id/cid/
#    flags/unitid) -> the "Defeat Argath!" boss-kill objective + named-unit link stay intact.
#  - Leave s1/s2 (lvl 254 scripted hostage + cutscene actor) and s8 (Delita guest) UNTOUCHED.
# Boss reaches +3 (103); generics 100-102. Equip is non-unique shop-tier (boss included). Rend/break
# on the Knights is a documented future tweak (needs the verified Knight Battle-Skill skillset id).
def ziekden(data):
    E = 401
    # Argath (BOSS) L103 — the evasive self-healing CROSSBOW SNIPER (restores his vanilla identity:
    # vanilla rh=78 was a crossbow). Keep his job (76) and identity bytes; off-job gear is assigned
    # via ENTD exactly like vanilla already does (vanilla equips this Knight with a crossbow), so the
    # crossbow's PA*WP ranged Attack fires regardless of job. Survival = double evasion (Crystal Shield
    # + Feather Mantle cloak) + Mana Shield routing damage to MP + Move-MP Up refueling MP as he kites;
    # Brave 90 makes the Mana Shield reaction fire ~90%. Offense = max PA (Twist Headband + Power Sleeve
    # + Attack Boost) * Gastrophetes (WP 10), with Aim (Archer charge) as the secondary for big charged
    # shots at range. Crossbow is one-handed -> the shield is legal alongside it.
    set_slot(data, E, 0, level=103, joblevel=8, brave=90, secondary=AIM,
             reaction=MANA_SHIELD, support=ATK_BOOST, movement=MOVE_MP_UP,
             head=HEADBAND, body=POWER_GARB, acc=FEATHERWEAVE,
             rh=GASTROPHETES, lh=CRYSTAL_SHIELD)
    # 5 generic Knights: captain s3 L102, s4 L101, then s5/s6/s7 anchors L100. Heavy shop gear.
    for s, lvl in ((3, 102), (4, 101), (5, 100), (6, 100), (7, 100)):
        set_slot(data, E, s, level=lvl, joblevel=8, job=KNIGHT, secondary=0,
                 reaction=COUNTER, support=ATK_BOOST, movement=MV1,
                 head=HEAVY_HELM, body=HEAVY_ARMOR, acc=BRACERS, rh=RUNEBLADE, lh=SHOP_SHIELD)
    # 2 Black Mages L101 (s9,s10): the standout AoE threat the walkthroughs warn about. Robe/rod.
    for s in (9, 10):
        set_slot(data, E, s, level=101, joblevel=8, job=BMAGE, secondary=0,
                 reaction=REFLEXES, movement=MV1,
                 head=MAGE_HAT, body=SHOP_ROBE, acc=FEATHERWEAVE, rh=SHOP_ROD, lh=LH_EMPTY)
    return [E]


# ===========================================================================
# CHAPTER 2 — "The Manipulator and the Subservient"
# ===========================================================================

# Battle 011 — Merchant City of Dorter (entry 403): Chapter 2 opener, mercenary ambush.
# Vanilla 403: s0 = Gaffgarion (cid 0x24, lv254 scripted ally), s2 = Agrias (cid 0x17, flags 0x04
# ally, lv254), s3 = another named story unit (cid 0x34, lv254) — all LEFT untouched. Enemies:
# s4,s5 Archer (cid 0x81 female), s7,s8 Black Mage (cid 0x80), s1,s6 Thief (cid 0x80). Per
# docs/battles/012-merchant-dorter.md.
#   - Steal Heart (charm) is INNATE to the Thief job command at JobLevel 8 (keep job 83, no secondary).
#   - v2 = split the Black Mages into a fast/power pair + a Knight street-captain.
#   - Current implementation note: Merchant Dorter is the one Chapter-2 event-spawned slot-add.
#     ENTD s9/uid 0x86 works only because event119.e also registers and spawns that uid.
#     Static ENTD-only slot-adds are for later fully-static Ch2 rosters, not this scripted wave.
#   - HISTORICAL FAILED TEST: a plain ENTD-only s9 reinforcement
#     (flags 0x10, correct generic-male Knight skeleton, unique unit-id, ground tile) NEVER SPAWNED.
#     This battle's enemy wave is placed by the event script by explicit slot index (0-8), so a 9th
#     slot is never added to the fight. (It is also outside the per-battle sprite preload, so when it
#     was wrongly drawn in the intro it fell back to a Thief sprite.) This is NOT a sprite cap (vanilla
#     battles load 7-16 sprites) and NOT OverrideEntryData (403's NXD rows are all sentinel —
#     work/enhanced_0004.sqlite). The .bin is authoritative; the engine just won't add a unit the event
#     doesn't place unless the event script is also patched.
#   - Final fix: keep both Thieves and add the Knight as ENTD s9/uid 0x86 with the matching
#     event119.e registration/choreography recipe.
def merchant_dorter(data):
    E = 403
    # 2 Archers: s4 L101, s5 L100 — elevated bow pressure (Concentration vs evasive NG+ units).
    for s, lvl in ((4, 101), (5, 100)):
        set_slot(data, E, s, level=lvl, joblevel=8, job=ARCHER, secondary=0,
                 brave=74, faith=50,
                 reaction=REFLEXES, support=CONCENTRATION, movement=MV1,
                 head=THIEFS_CAP, body=BLACK_GARB, acc=BRACERS, rh=WINDSLASH, lh=LH_TWOHAND)
    # v2: split the Black Mages — fast caster (s7) races the first AoE, power caster (s8) punishes
    # clumping. Mana Shield + Swiftspell vs Reflexes + Magick Boost (the MA-up v1 left vanilla).
    set_slot(data, E, 7, level=102, joblevel=8, job=BMAGE, secondary=0,
             reaction=MANA_SHIELD, support=SWIFTSPELL, movement=MV1,
             head=MAGE_HAT, body=SHOP_ROBE, acc=FEATHERWEAVE, rh=SHOP_ROD, lh=LH_EMPTY)
    set_slot(data, E, 8, level=101, joblevel=8, job=BMAGE, secondary=0,
             reaction=REFLEXES, support=MAGICK_BOOST, movement=MV1,
             head=MAGE_HAT, body=SHOP_ROBE, acc=FEATHERWEAVE, rh=SHOP_ROD, lh=LH_EMPTY)
    # 2 charm Thieves L100 (s1/s6) — Steal Heart innate to the Thief job (jl8).
    set_slot(data, E, 1, level=100, joblevel=8, job=THIEF, secondary=0,
             reaction=FIRST_STRIKE, support=ATK_BOOST, movement=MV2,
             head=THIEFS_CAP, body=BLACK_GARB, acc=GERMINAS, rh=AIR_KNIFE, lh=LH_TWOHAND)
    set_slot(data, E, 6, level=100, joblevel=8, job=THIEF, secondary=0,
             reaction=FIRST_STRIKE, support=ATK_BOOST, movement=MV2,
             head=THIEFS_CAP, body=BLACK_GARB, acc=GERMINAS, rh=AIR_KNIFE, lh=LH_TWOHAND)

    # Street Captain — true 7th enemy in s9. The event script must also include uid 0x86 in the
    # late 45-list and run the copied 0x86 spawn block in event119.e, or this ENTD slot will stay
    # prepared but inactive.
    src = (E % 128) * ENTRY + 6 * SLOT
    dst = (E % 128) * ENTRY + 9 * SLOT
    data[dst:dst + SLOT] = data[src:src + SLOT]
    data[dst + 0x19] = 0x07
    data[dst + 0x20] = 0x86
    set_slot(data, E, 9, level=102, joblevel=8, jobrank=KNIGHT - 0x4A, job=KNIGHT, secondary=0,
             reaction=COUNTER, support=DEFENSE_BOOST, movement=MV1,
             head=HEAVY_HELM, body=HEAVY_ARMOR, acc=BRACERS, rh=RUNEBLADE, lh=SHOP_SHIELD)
    # Gaffgarion (0x24) + Agrias (0x17) player-control = runtime scaler (Program.cs), not ENTD edits.
    return [E]


# ---------------------------------------------------------------------------
# Battle 012 — Araguay Woods (entry 404): goblin swarm in the woods + rescue Boco the chocobo.
# Vanilla 404: s0 = Boco (cid 0x82 monster, name_id 118, flags 0x30 special, job 94 Chocobo) — the
# RESCUABLE ally; LEFT untouched (its death = Game Over if rescue is chosen; scripting keys on its
# unit id, not its level). s1 = Gobbledeguck/Black-Goblin tier (job 98), s2-s6 = 5 Goblins (job 97).
# s7,s8 = named story units (lvl 254, left alone). Per docs/battles/013-araguay-woods.md.
#   - All-monster fight: scale Level + JobLevel only, no gear / no R-S-M (same as Ch1 Sweegy). The
#     OverrideEntryData remaps monster jobs at runtime but leaves Level/JobLevel = -1, so .bin edits
#     still scale them.
#   - v2 static slot-add: s9 Coeurl, with vanilla Goblins promoted to Black Goblins and two
#     far/central slots promoted to Gobbledygook. Keep the closest slot to Boco as Black Goblin.
#   - Boco is directly scaled/controlled here; its generic monster cid cannot use the named-guest
#     runtime scaler without also matching the enemy monsters.
def araguay(data):
    E = 404
    # Black-Goblin tier (s1) L101 — the durable melee of the pack.
    set_slot(data, E, 0, level=100, joblevel=8, brave=72, faith=40)
    set_player_control(data, E, 0)

    for s in (1, 2, 5, 6):
        set_slot(data, E, s, level=100, joblevel=8, job=BLACK_GOBLIN, brave=78, faith=35)

    set_slot(data, E, 3, level=101, joblevel=8, job=GOBBLEDYGOOK, brave=78, faith=35)
    set_slot(data, E, 4, level=102, joblevel=8, job=GOBBLEDYGOOK, brave=78, faith=35)

    clone_slot(data, E, 6, 9, unitid=0x87, x=10, y=2)
    set_slot(data, E, 9, level=101, joblevel=8, job=COEURL, brave=78, faith=35)
    # 5 Goblins (s2-s6) L100 — Ice-weak swarm bodies.
    return [E]


# ---------------------------------------------------------------------------
# Battle 013 — Zeirchele Falls (entry 405): Gaffgarion's betrayal; protect Ovelia (VIP).
# Vanilla 405: s0 = Gaffgarion (named cid 0x05, ENEMY team flags 0x80, job 5 = dark-sword skillset,
# the betrayer) — scaled as a sub-boss, identity bytes + job + secondary PRESERVED so his Drain
# skills and the ally->betray + auto-retreat scripting (event-keyed on his unit id) stay intact;
# s2/s3 = lvl-254 Knight corpse/intro placeholders shown during the opening scene and removed before
# tactical control by event129.e; they are story scenery and MUST stay vanilla. s4-s8 = 5 active
# generic Knights (escort wall); s1 = Ovelia (VIP ally, flags 0x51, lv5) — s1 now BUILT for
# survival (below); s9 Agrias + s10 named (lv254) LEFT alone.
# Per docs/battles/014-zeirchele-falls.md.
#   - Gaffgarion's kit is strong but NON-unique and STRIPPABLE (Runeblade) — the canonical
#     strip-his-gear counter survives; his rare drop is reserved for Lionel Gate (doc 021).
#   - ESCALATION: one vanilla active Knight slot (s7) becomes the White Mage sustain target and the
#     formation-gated static slot-add (s11) supplies an extra Knight body. The Archer escalation was
#     dropped: Zeirchele's non-player side already carries 4 special sprites (2x Gaffgarion 0x05+0x17,
#     Agrias 0x34, Ovelia 0x0C) plus the Knight sheet, and adding TWO new generic sheets (Archer +
#     White Mage) with full 4-player deployment corrupts Agrias's sprite/palette. One new sheet
#     matches the +1-sheet pattern of every other Ch2 battle that passed playtest clean.
#   - PLAYTEST: confirm s0 is the active Gaffgarion (vs a betrayal-spawned unit). Do NOT scale s2/s3:
#     they are intro corpse placeholders, not active enemies.
def zeirchele(data):
    E = 405
    # Gaffgarion (enemy sub-boss) L103 — KEEP job 5 + secondary (dark sword skills + betray/retreat).
    set_slot(data, E, 0, level=103, joblevel=8, brave=82, faith=60,
             reaction=COUNTER, support=ATK_BOOST, movement=MV1,
             head=HEAVY_HELM, body=HEAVY_ARMOR, acc=BRACERS, rh=RUNEBLADE, lh=SHOP_SHIELD)
    # 3 vanilla-slot melee Knights: s4 captain L102, s5/s6 L101. The 5th Knight is the added s11 below.
    for s, lvl in ((4, 102), (5, 101), (6, 101)):
        set_slot(data, E, s, level=lvl, joblevel=8, job=KNIGHT, secondary=0,
                 brave=76, faith=48,
                 reaction=COUNTER, support=ATK_BOOST, movement=MV1,
                 head=HEAVY_HELM, body=HEAVY_ARMOR, acc=BRACERS, rh=RUNEBLADE, lh=SHOP_SHIELD)
    # s8 was the Archer before the sprite-budget fix. Keep the Knight sheet, but restore the ranged
    # role with an ENTD-forced crossbow kit: best buyable crossbow + Archer-style R/S/M.
    set_slot(data, E, 8, level=101, jobrank=generic_job_rank(KNIGHT), joblevel=8,
             job=KNIGHT, secondary=0, brave=74, faith=50,
             reaction=REFLEXES, support=CONCENTRATION, movement=MV1,
             head=HEAVY_HELM, body=MIRROR_MAIL, acc=BRACERS, rh=GASTROPHETES, lh=CRYSTAL_SHIELD)
    # Field Medic — the ONLY new generic sprite sheet in this battle (see escalation note above).
    set_slot(data, E, 7, level=101, jobrank=generic_job_rank(WMAGE), joblevel=8,
             job=WMAGE, secondary=0, brave=55, faith=76,
             reaction=MANA_SHIELD, support=DEFENSE_BOOST, movement=MV1,
             head=MAGE_HAT, body=SHOP_ROBE, acc=FEATHERWEAVE, rh=SHOP_STAFF, lh=LH_EMPTY)
    # Placement polish: White Mage on high-ground mountain start; s8 Knight keeps the high-left line.
    set_position(data, E, 7, x=6, y=8, facing=0)
    set_position(data, E, 8, x=5, y=9, facing=0)
    # Ovelia (VIP ally s1, job 12 == cid 0x0c; runtime guest-scaler gives PARTY LEVEL — do NOT set
    # level/job). Her death = Game Over. She is a NAMED GUEST: the engine sources her command +
    # reaction/support/movement from her JOB TEMPLATE, not from the ENTD R/S/M bytes (those are ignored
    # for named units — proven in-game: Mana Shield 445@0x0C + Move-MP Up 494@0x10 written here never
    # appeared, and her secondary stayed "Items" though this byte was 254/none). The abilities fix is
    # therefore NOT in this ENTD slot but in the JOB: Princess (12) innate abilities — see
    # FFTIVC/tables/enhanced/JobData.xml, which adds Mana Shield (445) + Manafont/Move-MP Up (494) to the
    # two free innate slots (job 12 already ships innate Defense Boost 466 + Magick Defense Boost 468).
    # Innate abilities are ALWAYS active but do NOT render in the equipped R/S/M slots (that is why her
    # Support slot looked empty in-game despite the two vanilla innates). What this ENTD slot still sets:
    # GEAR + BRAVE. Brave 61 (@0x06 — the corrected offset; the old tool wrote 0x05) now MATTERS, because
    # Mana Shield procs at Brave% (61% chance to route a lethal hit to MP). Gear: Sortilège accessory =
    # Always Protect+Shell (halves every physical hit DETERMINISTICALLY, charge-proof — unlike evasion,
    # which a charging unit loses); Gold Hairpin (+80 HP/+50 MP — the MP also feeds Mana Shield + her Holy
    # Magicks); Luminous Robe; Golden Staff (MA).
    # Preserve the two vanilla story corpses. The second corpse is uid 0x81 and event129.e removes it
    # during the intro, so it cannot be reused as the field medic.
    restore_vanilla_slot(data, E, 2)
    restore_vanilla_slot(data, E, 3)

    # 5th Knight — true 7th enemy in s11/uid 0x87. Zeirchele also needs an OverrideEntryData row
    # for Key=405/Key2=11 (shaped like the battle's active-enemy rows, Unknown64=[60,60,60]);
    # otherwise the high-slot ENTD data is valid but not materialized by this battle's formation
    # layer. (Unknown9C is NOT an end marker — vanilla keeps 150 on s10 and the s11 row uses 0 like
    # every combat knight row; verified in-game.)
    # Use a Knight here because the Knight sprite already exists in the vanilla battle. Program.cs
    # currently runs a targeted diagnostic that temporarily suppresses uid 0x87 during the intro
    # actor peak; do not remove story actors from event129.e.
    clone_slot(data, E, 4, 11, unitid=0x87, x=3, y=9, facing=0)
    set_control_flags(data, E, 11, 0x90)
    set_slot(data, E, 11, level=100, jobrank=generic_job_rank(KNIGHT), joblevel=8,
             job=KNIGHT, secondary=0, brave=76, faith=48,
             reaction=COUNTER, support=ATK_BOOST, movement=MV1,
             head=HEAVY_HELM, body=HEAVY_ARMOR, acc=BRACERS, rh=RUNEBLADE, lh=SHOP_SHIELD)

    set_slot(data, E, 1, brave=61, faith=78, head=GOLD_HAIRPIN, body=LIGHT_ROBE,
             acc=SORTILEGE, rh=GOLDEN_STAFF)
    return [E]


# ---------------------------------------------------------------------------
# Battle 014 — Castled City of Zaland (entry 407): save reckless guest Mustadio; vertical castle.
# Vanilla 407: s0 = Mustadio (guest cid 0x22, job 34 == cid, flags 0x91 — handled by the runtime
# guest-scaler, NOT here); s1,s4 Knight; s2,s3 Black Mage; s5,s6 Archer (cid 0x81); s7 = recurring
# named story unit (cid 0x34, lvl 254, LEFT alone). Per docs/battles/015-zaland.md.
#   - Mustadio is added to GuestCharIds in Program.cs (cid 0x22, job==cid guard) so he scales to
#     party level and can survive his reckless charge / the protect-path Game Over. NOT touched here.
#   - ESCALATION is a job SWAP (s4 Knight -> Dragoon/Lancer), not a slot-add: a leaping threat that
#     Jumps the high walls to dive at Mustadio / the backline — the perfect wrinkle for a wall map.
def zaland(data):
    E = 407
    set_slot(data, E, 0, brave=70, faith=55, head=THIEFS_CAP, body=BLACK_GARB,
             acc=HERMES_SHOES, rh=MYTHRIL_GUN, lh=LH_TWOHAND)
    # s1 Knight anchor L101 — ground wall at the gate/approach.
    set_slot(data, E, 1, level=101, jobrank=generic_job_rank(KNIGHT), joblevel=8,
             job=KNIGHT, secondary=0,
             brave=76, faith=48,
             reaction=COUNTER, support=ATK_BOOST, movement=MV1,
             head=HEAVY_HELM, body=HEAVY_ARMOR, acc=BRACERS, rh=RUNEBLADE, lh=SHOP_SHIELD)
    # ESCALATION (job swap): s4 Knight -> Dragoon/Lancer L101 with reach (Move +2, spear). Jumps walls.
    set_slot(data, E, 4, level=102, jobrank=generic_job_rank(LANCER), joblevel=8,
             job=LANCER, secondary=0,
             brave=76, faith=45,
             reaction=COUNTER, support=ATK_BOOST, movement=MV2,
             head=HEAVY_HELM, body=HEAVY_ARMOR, acc=GERMINAS, rh=PARTISAN, lh=LH_EMPTY)
    clone_slot(data, E, 4, 8, unitid=0x86, x=0, y=10)
    # Flags history (both states playtested 2026-07-02): 0xD0 (clone of s4) alone -> the unit
    # NEVER materializes; 0x90 -> spawns, but stands outside the intro choreography (walk-anim
    # from frame 0). Zaland's six 0xD0 enemies are SCRIPT-MANAGED: event140.e AddUnit-registers
    # and choreographs them. So the full sibling-parity fix is 0xD0 + registering/choreographing
    # uid 0x86 in event140.e (tools/patch_event140_zaland.py). If the Dragoon is ever absent
    # again, event140.e stopped being the loaded script — revert this byte to 0x90 as fallback.
    set_control_flags(data, E, 8, 0xD0)
    set_slot(data, E, 8, level=101, jobrank=generic_job_rank(LANCER), joblevel=8,
             job=LANCER, secondary=0,
             brave=76, faith=45,
             reaction=COUNTER, support=ATK_BOOST, movement=MV2,
             head=HEAVY_HELM, body=HEAVY_ARMOR, acc=GERMINAS, rh=PARTISAN, lh=LH_EMPTY)
    # 2 Black Mages L101 (s2,s3) — the priority AoE threat. Support left vanilla.
    set_slot(data, E, 2, level=102, jobrank=generic_job_rank(BMAGE), joblevel=8,
             job=BMAGE, secondary=0,
             brave=55, faith=76,
             reaction=MANA_SHIELD, support=SWIFTSPELL, movement=MV1,
             head=MAGE_HAT, body=SHOP_ROBE, acc=FEATHERWEAVE, rh=SHOP_ROD, lh=LH_EMPTY)
    set_slot(data, E, 3, level=101, jobrank=generic_job_rank(BMAGE), joblevel=8,
             job=BMAGE, secondary=0,
             brave=55, faith=76,
             reaction=REFLEXES, support=MAGICK_BOOST, movement=MV1,
             head=MAGE_HAT, body=SHOP_ROBE, acc=FEATHERWEAVE, rh=SHOP_ROD, lh=LH_EMPTY)
    # 2 Archers: s5 L101 (wall archer), s6 L100 — elevated bow pressure over the walls.
    for s, lvl in ((5, 101), (6, 100)):
        set_slot(data, E, s, level=lvl, jobrank=generic_job_rank(ARCHER), joblevel=8,
                 job=ARCHER, secondary=0,
                 brave=74, faith=50,
                 reaction=REFLEXES, support=CONCENTRATION, movement=MV1,
                 head=THIEFS_CAP, body=BLACK_GARB, acc=BRACERS, rh=WINDSLASH, lh=LH_TWOHAND)
    return [E]


# ---------------------------------------------------------------------------
# Battle 015 — Balias Tor (entry 409): the first SUMMONER fight; three-flank hill.
# Vanilla 409: s0 = Mustadio (cid 0x22, lvl 254 — disabled here), s1 = recurring story unit
# (cid 0x34, lvl 254); both LEFT alone. Enemies: s2,s7 Knight; s3,s4 Archer; s5,s6 Summoner
# (job 82, cid 0x81). Per docs/battles/016-balias-tor.md.
#   - The SUMMONER (job 82) is itself the Chapter-2 escalation — no extra job swap (one wrinkle).
#     Summon is innate to the job at jl8; the Knights get Rend innately via Battle Skill at jl8
#     (the sanctioned break exception, same as Ziekden).
#   - PLAYTEST: the "mid-tier summons only" guideline can't be enforced via ENTD fields, and jl8 is
#     kept for caster-stat consistency (Black Mages likewise run full spell lists). If best-tier
#     summons appear and over-spike the curve, cap the Summoners' level/joblevel here.
def balias_tor(data):
    E = 409
    # 2 Summoners L101 (s5,s6) — slow-charge big AoE; the priority kills. Support left vanilla.
    set_slot(data, E, 5, level=102, jobrank=generic_job_rank(SUMMONER), joblevel=8,
             job=SUMMONER, secondary=0,
             brave=55, faith=76,
             reaction=MANA_SHIELD, support=SWIFTSPELL, movement=MV1,
             head=MAGE_HAT, body=SHOP_ROBE, acc=FEATHERWEAVE, rh=SHOP_ROD, lh=LH_EMPTY)
    set_slot(data, E, 6, level=101, jobrank=generic_job_rank(SUMMONER), joblevel=8,
             job=SUMMONER, secondary=0,
             brave=55, faith=76,
             reaction=REFLEXES, support=MAGICK_BOOST, movement=MV1,
             head=MAGE_HAT, body=SHOP_ROBE, acc=FEATHERWEAVE, rh=SHOP_ROD, lh=LH_EMPTY)
    # 2 Knights L101 (s2,s7) — break-walls screening the Summoners (Rend innate to Battle Skill).
    for s in (2, 7):
        set_slot(data, E, s, level=101, jobrank=generic_job_rank(KNIGHT), joblevel=8,
                 job=KNIGHT, secondary=0,
                 brave=76, faith=48,
                 reaction=COUNTER, support=ATK_BOOST, movement=MV1,
                 head=HEAVY_HELM, body=HEAVY_ARMOR, acc=BRACERS, rh=RUNEBLADE, lh=SHOP_SHIELD)
    # 2 Archers: s3 L101, s4 L100 — ranged support punishing the rush toward the Summoners.
    for s, lvl in ((3, 101), (4, 100)):
        set_slot(data, E, s, level=lvl, jobrank=generic_job_rank(ARCHER), joblevel=8,
                 job=ARCHER, secondary=0,
                 brave=74, faith=50,
                 reaction=REFLEXES, support=CONCENTRATION, movement=MV1,
                 head=THIEFS_CAP, body=BLACK_GARB, acc=BRACERS, rh=WINDSLASH, lh=LH_TWOHAND)
    clone_slot(data, E, 3, 8, unitid=0x86, x=13, y=4)
    set_slot(data, E, 8, level=101, jobrank=generic_job_rank(CHEMIST), joblevel=8,
             job=CHEMIST, secondary=0, brave=64, faith=60,
             reaction=AUTO_POTION, support=THROW_ITEMS, movement=MV1,
             head=THIEFS_CAP, body=BLACK_GARB, acc=FEATHERWEAVE, rh=MYTHRIL_GUN, lh=LH_TWOHAND)
    return [E]


# ---------------------------------------------------------------------------
# Battle 016 — Tchigolith Fenlands (entry 410): undead-swamp horror; all-monster status/attrition.
# Vanilla 410: s0 = Mustadio (cid 0x22, lvl 254, disabled — LEFT alone); s1-s5 = fixed monsters;
# s6/s7/s8 share UnitID 0x85 and position, forming the vanilla variant pool.
# Active roster:
#   fixed: 2 Revenants, 2 Bonesnatches, 2 Skeletal Fiends, 1 Ochu.
#   pool 0x85: Plague Horror or Wild Boar.
#   Per docs/battles/017-tchigolith-fenlands.md.
#   - The UNDEAD + status-swamp mechanic IS the Chapter-2 escalation — no job add.
#   - Scale Level + JobLevel ONLY (no gear, no R-S-M, no job change) exactly like Ch1 Sweegy/Araguay.
#     This PRESERVES the undead flags (reraise / heal-damages-undead / Phoenix-Down-instakill, which
#     are intrinsic to the job id + flag byte we never touch) and the swamp terrain.
#   - One mass-status disruptor only (the Malboro); no extra status monster added (project rule).
def tchigolith(data):
    E = 410
    set_slot(data, E, 1, level=102, joblevel=8, job=SKELETAL_FIEND, brave=80, faith=35)
    set_slot(data, E, 3, level=101, joblevel=8, job=BONESNATCH, brave=80, faith=35)
    for s, job in ((2, BONESNATCH), (4, REVENANT), (5, REVENANT)):
        set_slot(data, E, s, level=100, joblevel=8, job=job, brave=80, faith=35)
    # Keep the shared-uid variant logic, but make the pool exactly Plague Horror / Wild Boar.
    # This mirrors the two-entry random pools seen in Finnath: 0x50 variant followed by 0x90 base.
    set_slot(data, E, 6, level=100, joblevel=8, job=PLAGUE_HORROR, brave=78, faith=35)
    set_slot(data, E, 7, level=100, joblevel=8, job=WILD_BOAR, brave=78, faith=35)
    set_control_flags(data, E, 7, 0x90)
    clear_slot(data, E, 8)
    clone_slot(data, E, 1, 9, unitid=0x86, x=7, y=4)
    set_slot(data, E, 9, level=101, joblevel=8, job=SKELETAL_FIEND, brave=80, faith=35)
    clone_slot(data, E, 7, 10, unitid=0x87, x=9, y=8)
    set_control_flags(data, E, 10, 0x90)
    set_slot(data, E, 10, level=102, joblevel=8, job=OCHU, brave=78, faith=35)
    return [E]


# ---------------------------------------------------------------------------
# Battle 017 — Goug Lowtown (entry 411): second Summoner fight; urban race + charm + tempo.
# Vanilla 411: s0 = ally guest (cid 0x16, job 22 == cid, flags 0x91 — NOT Mustadio, who is a party
# member by now; LEFT untouched, see note); s1 = disabled named (cid 0x23, lvl 254); s2,s3,s9,s10 =
# Thieves (job 83); s5,s6 Archers (cid 0x81); s7,s8 Summoners (job 82); s4 = disabled Thief (lvl 254).
# Per docs/battles/018-goug-lowtown.md. TIC has 4 active Thieves (vs the walkthrough's 2); s10 is an
# anomalous lvl-1/jl-0 thief — LEFT untouched (likely special/scripted; harmless free kill if not).
#   - s2 stays the original active Thief. The prior s9 Thief path did not materialize in-game as
#     the second thief, so it is not counted as an active combatant here.
#   - ESCALATION (script-managed slot-add): s11 Time Mage uid 0x89 is registered/choreographed in
#     event167.e alongside the two Summoners (uids 0x86/0x88). JobLevel CAPPED to 4 (Lenalian
#     precedent) to bias toward Haste/Slow and keep Stop/Immobilize off the table.
#   - Steal Heart stays innate on the two active Thieves (job 83 at jl8).
#   - cid 0x16 is now in GuestCharIds, so the runtime scaler handles level/control for this ally.
def goug(data):
    E = 411
    set_slot(data, E, 0, brave=68, faith=60)
    # 2 Summoners L101 (s7,s8) — the priority kills; race the cast.
    set_slot(data, E, 7, level=102, joblevel=8, job=SUMMONER, secondary=0,
             brave=55, faith=76,
             reaction=REFLEXES, support=MAGICK_BOOST, movement=MV1,
             head=MAGE_HAT, body=SHOP_ROBE, acc=FEATHERWEAVE, rh=SHOP_ROD, lh=LH_EMPTY)
    set_slot(data, E, 8, level=101, joblevel=8, job=SUMMONER, secondary=0,
             brave=55, faith=76,
             reaction=MANA_SHIELD, support=MAGICK_BOOST, movement=MV1,
             head=MAGE_HAT, body=SHOP_ROBE, acc=FEATHERWEAVE, rh=SHOP_ROD, lh=LH_EMPTY)
    # 2 Archers: s5 L101, s6 L100 — ranged punishment on the approach.
    for s, lvl in ((5, 101), (6, 100)):
        set_slot(data, E, s, level=lvl, joblevel=8, job=ARCHER, secondary=0,
                 brave=74, faith=50,
                 reaction=REFLEXES, support=CONCENTRATION, movement=MV1,
                 head=THIEFS_CAP, body=BLACK_GARB, acc=BRACERS, rh=WINDSLASH, lh=LH_TWOHAND)
    # 2 charm Thieves (s2,s3) - fast harassers; Steal Heart innate to the Thief job at jl8.
    for s, lvl in ((2, 100), (3, 101)):
        set_slot(data, E, s, level=lvl, joblevel=8, job=THIEF, secondary=0,
                 brave=78, faith=48,
                 reaction=FIRST_STRIKE, support=ATK_BOOST, movement=MV2,
                 head=THIEFS_CAP, body=BLACK_GARB, acc=GERMINAS, rh=AIR_KNIFE, lh=LH_TWOHAND)
    # Extra tempo unit: wave-scripted Time Mage revealed with the Summoners. Clone a Summoner wave
    # sibling so flags/visual convention match, then retune the role and position.
    clone_slot(data, E, 8, 11, unitid=0x89, x=0, y=5)
    set_control_flags(data, E, 11, 0x10)
    set_slot(data, E, 11, level=102, joblevel=4, job=TMAGE, secondary=0,
             brave=55, faith=76,
             reaction=REFLEXES, support=SWIFTSPELL, movement=MV1,
             head=MAGE_HAT, body=SHOP_ROBE, acc=FEATHERWEAVE, rh=SHOP_ROD, lh=LH_EMPTY)
    return [E]


# ---------------------------------------------------------------------------
# Battle 018 — Balias Swale (entry 413): rainy split-team rush to save an outnumbered Agrias.
# Vanilla 413: s0 = Agrias (named cid 0x1e, job 30 == cid — the "Save Agrias!" VIP; handled by the
# runtime guest-scaler, NOT here); s1,s4 Knight; s2,s3 Archer (cid 0x81); s5,s6 Black Mage (job 80).
# Per docs/battles/019-balias-swale.md. (TIC has 2 Knights vs the walkthrough's 1.)
#   - Agrias added to GuestCharIds in Program.cs (cid 0x1e, job==cid guard) so she scales to party
#     level and can survive the rescue (her death fails the battle; she joins permanently after).
#   - v2 static slot-add: s7 Geomancer gives terrain pressure without event-script interaction.
#   - Knights run job 76 at jl8, so they have Battle Skill (Rend) innately — a minor extra vs the
#     doc's "no break" preference here; can't be suppressed without changing the job. Non-blocking.
def balias_swale(data):
    E = 413
    set_slot(data, E, 0, brave=76, faith=65)
    # 2 Knights: s1 L101 (lead body), s4 L100 — the frontline the player fights through to Agrias.
    for s, lvl in ((1, 101), (4, 100)):
        set_slot(data, E, s, level=lvl, joblevel=8, job=KNIGHT, secondary=0,
                 brave=76, faith=48,
                 reaction=COUNTER, support=ATK_BOOST, movement=MV1,
                 head=HEAVY_HELM, body=HEAVY_ARMOR, acc=BRACERS, rh=RUNEBLADE, lh=SHOP_SHIELD)
    # 2 Archers: s2 L101, s3 L100 — far-end ranged pressure on the isolated Agrias.
    for s, lvl in ((2, 101), (3, 100)):
        set_slot(data, E, s, level=lvl, joblevel=8, job=ARCHER, secondary=0,
                 brave=74, faith=50,
                 reaction=REFLEXES, support=CONCENTRATION, movement=MV1,
                 head=THIEFS_CAP, body=BLACK_GARB, acc=BRACERS, rh=WINDSLASH, lh=LH_TWOHAND)
    # 2 Black Mages L101 (s5,s6) — rain-boosted Thunder, the primary threat. Support left vanilla.
    set_slot(data, E, 5, level=102, joblevel=8, job=BMAGE, secondary=0,
             brave=55, faith=76,
             reaction=REFLEXES, support=SWIFTSPELL, movement=MV1,
             head=MAGE_HAT, body=SHOP_ROBE, acc=FEATHERWEAVE, rh=SHOP_ROD, lh=LH_EMPTY)
    set_slot(data, E, 6, level=101, joblevel=8, job=BMAGE, secondary=0,
             brave=55, faith=76,
             reaction=REFLEXES, support=MAGICK_BOOST, movement=MV1,
             head=MAGE_HAT, body=SHOP_ROBE, acc=FEATHERWEAVE, rh=SHOP_ROD, lh=LH_EMPTY)
    clone_slot(data, E, 1, 7, unitid=0x86, x=1, y=6)
    set_slot(data, E, 7, level=101, jobrank=generic_job_rank(GEOMANCER), joblevel=8,
             job=GEOMANCER, secondary=0, brave=62, faith=68,
             reaction=FIRST_STRIKE, support=ATK_BOOST, movement=MV1,
             head=THIEFS_CAP, body=BLACK_GARB, acc=BRACERS, rh=RUNEBLADE, lh=LH_EMPTY)
    return [E]


# ---------------------------------------------------------------------------
# Battle 019 — Golgollada Gallows (entry 414): the Gaffgarion sub-boss "disarm" trap; no guests.
# Vanilla 414: s0 = Gaffgarion (named cid 0x11, job 17, ENEMY flags 0x80 — the sub-boss); s2,s3,s4
# Knight; s1,s5 Archer (cid 0x81); s6,s7 Time Mage (cid 0x81). Per docs/battles/020-golgollada-gallows.md.
#   - Gaffgarion scaled to sub-boss L103 with job 17 + secondary PRESERVED -> his Shadowblade/Drain
#     skillset and his RETREAT-at-threshold scripting (he must NOT die here; death + rare drop are
#     reserved for Lionel Gate) stay intact. set_slot preserves identity bytes.
#   - His dark blade is a STRONG but NON-RARE, STRIPPABLE Runeblade, so the disarm counter
#     (Rend / Steal Weapon) shuts off his sustain — no rare item lootable at the Gallows.
#   - The two Time Mages are jl-CAPPED to 4 (Lenalian/Goug precedent) -> Haste/Slow, no hard lock.
#   - Knights carry Rend innately via Battle Skill at jl8 (sanctioned break exception).
def golgollada(data):
    E = 414
    # Gaffgarion (sub-boss) L103 — KEEP job 17 + secondary (Drain + retreat scripting). Strippable blade.
    set_slot(data, E, 0, level=103, joblevel=8, brave=82, faith=60,
             reaction=COUNTER, support=ATK_BOOST, movement=MV2,
             head=HEAVY_HELM, body=HEAVY_ARMOR, acc=BRACERS, rh=RUNEBLADE, lh=SHOP_SHIELD)
    # 3 Knights — the screen; Rend innate via Battle Skill at jl8.
    # s4 is the high-side leader/sniper near the Time Mages: best buyable crossbow, shield-compatible, Attack Boost.
    for s, lvl in ((2, 101), (3, 101)):
        set_slot(data, E, s, level=lvl, joblevel=8, job=KNIGHT, secondary=0,
                 brave=76, faith=48,
                 reaction=COUNTER, support=DEFENSE_BOOST, movement=MV1,
                 head=HEAVY_HELM, body=HEAVY_ARMOR, acc=BRACERS, rh=RUNEBLADE, lh=SHOP_SHIELD)
    set_slot(data, E, 4, level=102, joblevel=8, job=KNIGHT, secondary=0,
             brave=76, faith=48,
             reaction=VIGILANCE, support=ATK_BOOST, movement=MV1,
             head=HEAVY_HELM, body=HEAVY_ARMOR, acc=BRACERS, rh=GASTROPHETES, lh=SHOP_SHIELD)
    # 2 Archers: s1 L101, s5 L100 — ranged punishment on the rush to Gaffgarion.
    for s, lvl in ((1, 101), (5, 100)):
        set_slot(data, E, s, level=lvl, joblevel=8, job=ARCHER, secondary=0,
                 brave=74, faith=50,
                 reaction=REFLEXES, support=CONCENTRATION, movement=MV1,
                 head=THIEFS_CAP, body=BLACK_GARB, acc=BRACERS, rh=WINDSLASH, lh=LH_TWOHAND)
    # 2 Time Mages L101 (s6,s7) — keep Gaffgarion fast. jl CAPPED to 4 (Haste/Slow, no hard lock).
    set_slot(data, E, 6, level=102, joblevel=4, job=TMAGE, secondary=0,
             brave=58, faith=72,
             reaction=REFLEXES, support=SWIFTSPELL, movement=MV1,
             head=MAGE_HAT, body=SHOP_ROBE, acc=FEATHERWEAVE, rh=SHOP_ROD, lh=LH_EMPTY)
    set_slot(data, E, 7, level=101, joblevel=4, job=TMAGE, secondary=0,
             brave=58, faith=72,
             reaction=REFLEXES, support=MAGICK_BOOST, movement=MV1,
             head=MAGE_HAT, body=SHOP_ROBE, acc=FEATHERWEAVE, rh=SHOP_ROD, lh=LH_EMPTY)
    return [E]


# ---------------------------------------------------------------------------
# Battle 020 — Lionel Castle Gate (entry 415): Gaffgarion's last stand; first RARE BOSS LOOT.
# Vanilla 415: s0 = Gaffgarion (named cid 0x11, job 17 Fell Knight, ENEMY — the BOSS, dies here);
# s1,s2 Archer (job 77); s3,s4,s5 Knight (job 76); s6 Summoner (job 82). Per docs/battles/021-lionel-castle-gate.md.
#   - Gaffgarion scaled to BOSS L103, job 17 + secondary PRESERVED (Shadowblade/Drain + death
#     scripting intact). His weapon is Defender (33), per the latest test tuning. Steal/Rend Weapon
#     remains the readable off-switch for his weapon-tied threat.
#   - Knights carry Rend innately (Battle Skill at jl8); Summoner mid-tier (tier = playtest item).
#   - Job 17 (Fell Knight) equips Helmet/Armor/Shield/Sword (verified), so the heavy kit is legal.
def lionel_gate(data):
    E = 415
    # Gaffgarion (BOSS) L103 — KEEP job 17 + secondary. Defender steal/break target.
    set_slot(data, E, 0, level=103, joblevel=8, brave=82, faith=60,
             reaction=PARRY, support=ATK_BOOST, movement=MV2,
             head=HEAVY_HELM, body=HEAVY_ARMOR, acc=BRACERS, rh=DEFENDER, lh=LH_TWOHAND)
    # 3 Knights L101 (s3,s4,s5) — the gate siege; Rend innate via Battle Skill at jl8.
    for s, lvl, support in ((3, 102, DEFENSE_BOOST), (4, 101, ATK_BOOST), (5, 101, ATK_BOOST)):
        set_slot(data, E, s, level=lvl, joblevel=8, job=KNIGHT, secondary=0,
                 brave=76, faith=48,
                 reaction=COUNTER, support=support, movement=MV1,
                 head=HEAVY_HELM, body=HEAVY_ARMOR, acc=BRACERS, rh=RUNEBLADE, lh=SHOP_SHIELD)
    # 2 Archers: s1 L101, s2 L100 — ranged pressure on the gate defenders.
    for s, lvl in ((1, 101), (2, 100)):
        set_slot(data, E, s, level=lvl, joblevel=8, job=ARCHER, secondary=0,
                 brave=74, faith=50,
                 reaction=REFLEXES, support=CONCENTRATION, movement=MV1,
                 head=THIEFS_CAP, body=BLACK_GARB, acc=BRACERS, rh=WINDSLASH, lh=LH_TWOHAND)
    # Summoner L101 (s6) — mid-tier AoE shelling the clustered gate defense. Support left vanilla.
    set_slot(data, E, 6, level=102, joblevel=8, job=SUMMONER, secondary=0,
             brave=55, faith=76,
             reaction=REFLEXES, support=SWIFTSPELL, movement=MV1,
             head=MAGE_HAT, body=SHOP_ROBE, acc=FEATHERWEAVE, rh=SHOP_ROD, lh=LH_EMPTY)
    return [E]


# ---------------------------------------------------------------------------
# Battle 021 — Lionel Castle Oratory / Cúchulainn (entry 425): CHAPTER 2 FINALE; first Lucavi demon.
# Vanilla 425: s0-s8 = disabled cutscene placeholders (Cardinal Draclau cid 0x28 job 40 + guards,
# Ramza cid 0x02, a chocobo) all at lvl 254; s9 = Cúchulainn (named cid 0x3c, job 60 = Gigas/Demon,
# monster-team flags 0x20) — the SOLE active enemy. Per docs/battles/022-lionel-castle-oratory.md.
#   - Cúchulainn is a MONSTER/demon: job 60 equips Unarmed only, so scaling is LEVEL ONLY. We set
#     level 104 (the chapter's top band, +1 over Gaffgarion) and touch nothing else -> his entire
#     canonical kit (Nightmare mass Doom/Sleep + run-up, Holy weakness, dark/poison absorb, Blood
#     Suck) and JobLevel 8 are PRESERVED. These ARE the fight.
#   - 108 Gems is delivered through ENTD Spoils of War (slot 0x1e) on the active Lucavi slot, not
#     through equipment, because the Unarmed demon has no accessory slot.
def cuchulainn(data):
    E = 425
    set_slot(data, E, 9, level=104, joblevel=8, brave=88, faith=82)
    set_spoil(data, E, 9, GEMS_108)
    return [E]


# ===========================================================================
# CHAPTER 3 — "The Valiant". Entries deduced offline (roster-match + story-order),
# see docs/battles/024-chapter-3-overview.md. Rewards: boss rares in the ENTD here;
# Move-Find treasures handled by the code mod's MapTreasureNgPlus.
# ===========================================================================

# ---------------------------------------------------------------------------
# Battle 022 — Mining Town of Gollund (entry 417): protect-the-VIP opener; enemy ORATOR debut.
# Vanilla 417: s0 = Orran guest (cid/sprite 21, job 21; runtime-scaled, DO NOT touch here);
# s1,s4,s5 Thief (job 83); s2,s3 Chemist (job 75, gun); s6 Orator (job 84). Per docs/025.
#   - Low-lethality, high-denial: keep the 2 Chemist / 3 Thief / 1 Orator shape (one new wrinkle).
#   - Charm/steal stay on Thieves; Orator keeps Speechcraft as its primary charm/soft-status skillset
#     (NO hard lock added). Chapter 3 requires real secondaries on active humans, so Thieves/Orator
#     get Items for limited sustain and Chemists get Fundaments as mild, non-locking filler.
#   - No boss here -> no rare boss loot (per the Ch3 overview); generics on shop-tier gear.
def gollund(data):
    E = 417
    # Orran protected guest: keep job/special kit/script, but make the embedded NG+ ENTD match v2
    # Br/Fa and control intent. Runtime guest scaler still handles every read path and direct level.
    set_slot(data, E, 0, level=100, brave=65, faith=75)
    set_player_control(data, E, 0)
    # 3 Thieves: s1 L101, s4 L101, s5 L100 — fast charm/steal harassers rushing Orran.
    for s, lvl in ((1, 101), (4, 101), (5, 100)):
        set_slot(data, E, s, level=lvl, joblevel=8, job=THIEF, secondary=ITEMS,
                 brave=84, faith=42,
                 reaction=FIRST_STRIKE, support=ATK_BOOST, movement=MV2,
                 head=THIEFS_CAP, body=BLACK_GARB, acc=GERMINAS, rh=AIR_KNIFE, lh=LH_EMPTY)
    # 2 Chemists L101 (s2,s3) — heal/revive sustain spine (gun = two-handed).
    for s in (2, 3):
        set_slot(data, E, s, level=101, joblevel=8, job=CHEMIST, secondary=FUNDAMENTS,
                 brave=68, faith=64,
                 reaction=AUTO_POTION, support=THROW_ITEMS, movement=MV1,
                 head=MAGE_HAT, body=BLACK_GARB, acc=BRACERS, rh=MYTHRIL_GUN, lh=LH_TWOHAND)
    # Orator L102 (s6) — the NEW caste anchor; charm/status. Gun two-handed; Items secondary.
    set_slot(data, E, 6, level=102, joblevel=8, job=ORATOR, secondary=ITEMS,
             brave=65, faith=72,
             reaction=FIRST_STRIKE, support=ATK_BOOST, movement=MV1,
             head=MAGE_HAT, body=SHOP_ROBE, acc=GERMINAS, rh=MYTHRIL_GUN, lh=LH_TWOHAND)
    return [E]


# ---------------------------------------------------------------------------
# Battle 023 — Lesalia Castle Postern (entry 420): the reviving-healer-boss puzzle; protect Alma.
# Vanilla 420: s0 = Alma guest (cid/sprite/job 48; runtime-scaled, DO NOT touch here); s1 = Zalmo
# (named cid 0x10, job 16 Inquisitor — the SUB-BOSS; HEALS/REVIVES, RETREATS at HP threshold, no
# death/loot here); s2,s3,s5 Knight (76); s4,s6 Monk (78). Per docs/026.
#   - Zalmo: preserve job 16 + gear + the heal/revive/retreat scripting (like Cúchulainn). Safe v2
#     edits are level, Br/Fa, and an Items secondary; touching his special-job identity risks the puzzle.
#   - Knights: Flame Shield band (Fire-absorb element puzzle); Rend innate (Battle Skill primary).
#   - Monks: bare-fist; Monk equips HairAdornment (all reserved) not Hat, so NO head item -> bare head
#     (canonical). Body = Power Garb (Clothing, legal); no shield (give PA via Bracers).
#   - No rare loot (Zalmo retreats), per the Ch3 overview.
def lesalia(data):
    E = 420
    set_slot(data, E, 0, level=100, brave=60, faith=78)  # Alma guest: preserve Aegis kit/gear
    set_player_control(data, E, 0)
    set_slot(data, E, 1, level=103, secondary=ITEMS, brave=70, faith=78)  # Zalmo: preserve retreat kit
    for s in (2, 3):  # 2 main Knights — Flame Shield wall, Rend innate
        set_slot(data, E, s, level=101, joblevel=8, job=KNIGHT, secondary=ITEMS,
                 brave=84, faith=45,
                 reaction=COUNTER, support=ATK_BOOST, movement=MV1,
                 head=HEAVY_HELM, body=HEAVY_ARMOR, acc=BRACERS, rh=RUNEBLADE, lh=FLAME_SHIELD)
    set_slot(data, E, 5, level=101, joblevel=8, job=KNIGHT, secondary=FUNDAMENTS,
             brave=84, faith=45,
             reaction=COUNTER, support=ATK_BOOST, movement=MV1,
             head=HEAVY_HELM, body=HEAVY_ARMOR, acc=BRACERS, rh=RUNEBLADE, lh=FLAME_SHIELD)
    for s in (4, 6):  # 2 Monks — bare-fist bruisers (no legal Hat/shield); Power Garb + Bracers
        set_slot(data, E, s, level=101, joblevel=8, job=MONK, secondary=ITEMS,
                 brave=84, faith=42,
                 reaction=COUNTER, support=ATK_BOOST, movement=MV1,
                 body=POWER_GARB, acc=BRACERS)
    return [E]


# ---------------------------------------------------------------------------
# Battle 024 — Monastery Vaults 2nd Level (entry 422): enemy DRAGOON debut; vault chain 1/3.
# Vanilla 422: s0 = Nightblade (job 38, a Templar-type special, gearless — NOT in the walkthrough
# roster; scale LEVEL ONLY to preserve its identity/kit); s1,s2,s3 Dragoon (87); s4 Chemist (75);
# s5,s6 Time Mage (81). Per docs/027.
#   - Dragoons: Jump (innate primary). Polearm + heavy gear + shield (job 87 equips Helmet/Armor/
#     Shield/Polearm). Ignore Height lets them cross the vault; all three get Dragonheart.
#   - Time Mages: Haste/Slow ONLY -> jl CAPPED to 4 (no Stop/Immobilize). NOTE: Time Mage equips
#     STAFF, not Rod (job 81) -> use SHOP_STAFF (the Ch2 TMages were given SHOP_ROD = illegal/no-op;
#     flagged separately). Chemist = the sustain priority kill; Featherweave + Defense Boost + Move+2.
#     No boss -> no rare loot.
def vaults_2nd(data):
    E = 422
    set_slot(data, E, 0, level=102, brave=84, faith=55)  # Nightblade special: preserve identity/kit
    for s, lvl in ((1, 102), (2, 101), (3, 100)):  # 3 Dragoons — Jump divers
        set_slot(data, E, s, level=lvl, joblevel=8, job=LANCER,
                 reaction=DRAGONHEART, support=CONCENTRATION, movement=IGNORE_HEIGHT,
                 head=HEAVY_HELM, body=HEAVY_ARMOR, acc=HERMES_SHOES, rh=PARTISAN, lh=SHOP_SHIELD)
    set_slot(data, E, 4, level=101, joblevel=8, job=CHEMIST,  # Chemist — sustain / priority kill
             reaction=AUTO_POTION, support=DEFENSE_BOOST, movement=MV2,
             head=MAGE_HAT, body=BLACK_GARB, acc=FEATHERWEAVE, rh=MYTHRIL_GUN, lh=LH_TWOHAND)
    for s in (5, 6):  # 2 Time Mages — Haste/Slow only (jl4), Staff (job-legal)
        set_slot(data, E, s, level=101, joblevel=4, job=TMAGE,
                 reaction=MANA_SHIELD, movement=MOVE_MP_UP,
                 head=MAGE_HAT, body=SHOP_ROBE, acc=FEATHERWEAVE, rh=SHOP_STAFF, lh=LH_EMPTY)
    set_slot(data, E, 1, secondary=ITEMS, brave=84, faith=72)
    for s in (2, 3):
        set_slot(data, E, s, secondary=ITEMS, brave=84, faith=72)
    set_slot(data, E, 4, secondary=FUNDAMENTS, brave=68, faith=64)
    for s in (5, 6):
        set_slot(data, E, s, secondary=ITEMS, brave=60, faith=74, support=MAGICK_BOOST)
    return [E]


# ---------------------------------------------------------------------------
# Battle 025 — Monastery Vaults 3rd Level (entry 423): Izlude SUB-BOSS; vault chain 2/3.
# Vanilla 423: s0 = Izlude (named cid, job 38 Nightblade/Knights-Templar special, sec 52 Mighty
# Sword, GEARED) — the elevated decapitation target; s1,s2 Knight (76); s3 Summoner (82); s4,s5
# Archer (77). Per docs/028.
#   - Izlude: PRESERVE job 38 + secondary 52 (Mighty-Sword breaks) + reaction/support/movement
#     (his special kit — possibly innate dual-wield; clobbering it risks losing the boss identity).
#     Only LEVEL 103 + jl8, and his RARE: body = Mirror Mail (184 = TIC's "Reflect Mail", auto-Reflect;
#     forces a physical finish). Modest weapon bump (Runeblade) + Bracers; keep his shield (lh) + head.
#     Defeating him ENDS the fight (do NOT touch the objective/chain scripting).
#   - Knights: screen the climb; Rend innate (Battle Skill primary). Heavy gear + shop shield.
#   - Summoner: mid-tier shelling the approach; Summon innate. Summoner equips ROD (job 82, verified).
#   - Archers: ranged punishment on the climb (two-hand bow).
#   - Rare loot is Izlude's Mirror Mail ONLY (his Riovanes Roof appearance is a cutscene death, 035).
def vaults_3rd(data):
    E = 423
    # Izlude SUB-BOSS — level/jl + Reflect Mail (rare) only; preserve job 38 / sec 52 / kit / shield.
    set_slot(data, E, 0, level=103, joblevel=8, body=MIRROR_MAIL, acc=BRACERS, rh=RUNEBLADE)
    for s in (1, 2):  # 2 Knights — screen the vertical lane; Rend innate
        set_slot(data, E, s, level=101, joblevel=8, job=KNIGHT,
                 reaction=COUNTER, support=ATK_BOOST, movement=MV1,
                 head=HEAVY_HELM, body=HEAVY_ARMOR, acc=BRACERS, rh=RUNEBLADE, lh=SHOP_SHIELD)
    set_slot(data, E, 3, level=101, joblevel=8, job=SUMMONER,  # Summoner — mid-tier shelling (Rod-legal)
             reaction=REFLEXES, support=ATK_BOOST, movement=MV1,
             head=MAGE_HAT, body=SHOP_ROBE, acc=FEATHERWEAVE, rh=SHOP_ROD, lh=LH_EMPTY)
    for s, lvl in ((4, 101), (5, 100)):  # 2 Archers — ranged punishment on the climb
        set_slot(data, E, s, level=lvl, joblevel=8, job=ARCHER, secondary=FUNDAMENTS,
                 reaction=REFLEXES, support=CONCENTRATION, movement=MV1,
                 head=THIEFS_CAP, body=BLACK_GARB, acc=BRACERS, rh=WINDSLASH, lh=LH_TWOHAND)
    return [E]


# ---------------------------------------------------------------------------
# Battle 026 — Monastery Vaults 1st Level (entry 424): Wiegraf rematch; vault chain 3/3 (finale).
# Vanilla 424: s0 = Wiegraf (named cid/sprite 40, job 40 White/Holy Knight; Holy Sword is the job's
# INNATE command, sec 254; he FLEES — does NOT die here); s1,s2 Knight (76); s3,s5 Archer (77);
# s4 Black Mage (80). s6,s7 are INACTIVE placeholders (level 0xFE) — leave untouched. Per docs/029.
#   - Wiegraf: PRESERVE job 40 + flee scripting + reaction/support/movement. Set LEVEL 104 + jl8 and
#     gear him as the boss spike (job 40 equips Helmet/Armor/Shield/Sword — verified): heavy gear +
#     Runeblade (strong NON-rare sword keeps Holy Sword weapon-tied/disarmable). NO rare loot (he
#     flees; his rare is paid out at Riovanes Keep 034).
#   - Knights: contest the doorways; Rend innate (Battle Skill primary). Heavy gear + shop shield.
#   - Black Mage: ranged magic punishing a clumped gate; Rod (job-80-legal).
#   - Archers: fire through the doorways (two-hand bow).
def vaults_1st(data):
    E = 424
    # Wiegraf BOSS — level/jl + boss gear; preserve job 40 / Holy Sword / kit / flee scripting. No drop.
    set_slot(data, E, 0, level=104, joblevel=8,
             head=HEAVY_HELM, body=HEAVY_ARMOR, acc=BRACERS, rh=RUNEBLADE, lh=SHOP_SHIELD)
    for s in (1, 2):  # 2 Knights — gate bodies; Rend innate
        set_slot(data, E, s, level=101, joblevel=8, job=KNIGHT,
                 reaction=COUNTER, support=ATK_BOOST, movement=MV1,
                 head=HEAVY_HELM, body=HEAVY_ARMOR, acc=BRACERS, rh=RUNEBLADE, lh=SHOP_SHIELD)
    set_slot(data, E, 4, level=101, joblevel=8, job=BMAGE,  # Black Mage — ranged magic vs. clumped gate
             reaction=REFLEXES, support=ATK_BOOST, movement=MV1,
             head=MAGE_HAT, body=SHOP_ROBE, acc=FEATHERWEAVE, rh=SHOP_ROD, lh=LH_EMPTY)
    for s, lvl in ((3, 101), (5, 100)):  # 2 Archers — fire through the doorways
        set_slot(data, E, s, level=lvl, joblevel=8, job=ARCHER, secondary=FUNDAMENTS,
                 reaction=REFLEXES, support=CONCENTRATION, movement=MV1,
                 head=THIEFS_CAP, body=BLACK_GARB, acc=BRACERS, rh=WINDSLASH, lh=LH_TWOHAND)
    return [E]


# ---------------------------------------------------------------------------
# Battle 027 — Grogh Heights (entry 426): the rainy breather; weather + clustering. Per docs/030.
# Vanilla 426: s0,s2 Squire (74); s1,s3 Chemist (75, gun); s4 Archer (77); s5 Thief (83). s6 (Orran
# placeholder, job 21), s7 (Knight), s8 (monster) are INACTIVE (level 0xFE) — leave untouched.
#   - DESIGN: swap ONE Squire (s0) -> rain-Thunder Black Mage (the two-way-weather escalation); keep
#     the other Squire. This is a BREATHER — modest levels (mostly 100-101, no 102 anchor), no boss,
#     no rare loot. Keep the rain flag + tight clustering geometry (untouched scripting/terrain).
def grogh(data):
    E = 426
    set_slot(data, E, 0, level=100, joblevel=8, job=SQUIRE, secondary=GEOMANCY,
             reaction=FIRST_STRIKE, support=ATK_BOOST, movement=MV2,
             head=HEADBAND, body=POWER_GARB, acc=BRACERS, rh=SLASHER, lh=LH_EMPTY)
    set_slot(data, E, 2, level=101, joblevel=8, job=BMAGE, secondary=0,  # rain-Thunder caster, moved off intro-animated s0
             reaction=MANA_SHIELD, support=ATK_BOOST, movement=MOVE_MP_UP,
             head=MAGE_HAT, body=SHOP_ROBE, acc=FEATHERWEAVE, rh=SHOP_ROD, lh=LH_EMPTY)
    for s, lvl in ((1, 101), (3, 100)):  # 2 Chemists — light heal sustain (gun = two-handed)
        set_slot(data, E, s, level=lvl, joblevel=8, job=CHEMIST,
                 reaction=AUTO_POTION, support=THROW_ITEMS, movement=MV2,
                 head=THIEFS_CAP, body=BLACK_GARB, acc=FEATHERWEAVE, rh=MYTHRIL_GUN, lh=LH_TWOHAND)
    set_slot(data, E, 4, level=101, joblevel=8, job=ARCHER, secondary=FUNDAMENTS,  # ranged chip
             reaction=REFLEXES, support=CONCENTRATION, movement=MV1,
             head=THIEFS_CAP, body=BLACK_GARB, acc=BRACERS, rh=WINDSLASH, lh=LH_TWOHAND)
    set_slot(data, E, 5, level=100, joblevel=8, job=THIEF,  # fast steal/charm harass (Steal innate)
             reaction=FIRST_STRIKE, support=ATK_BOOST, movement=MV2,
             head=THIEFS_CAP, body=BLACK_GARB, acc=GERMINAS, rh=AIR_KNIFE, lh=LH_EMPTY)
    return [E]


# ---------------------------------------------------------------------------
# Battle 028 — Walled City of Yardrow (entry 428): NINJA debut; protect-Rapha puzzle. Per docs/031.
# Vanilla 428: s0 = Rapha (cid/job 25 Skyseer, control bytes 00 84 = GUEST/ALLY — the protected NPC,
# LOSE-on-death; already geared White Robe + Elven Cloak evasion); s1 = Marach (cid/job 26 Netherseer,
# enemy BOSS, survives/recruitable later — nearly naked); s2,s4,s6 Ninja (89); s3,s5 Summoner (82).
#   - Rapha: NOT touched here — she is runtime level-scaled (charId 0x19 added to GuestCharIds in
#     Program.cs); her vanilla evasion gear suffices. PRESERVE her lose-on-death scripting.
#   - Marach: BOSS that SURVIVES. Scale LEVEL 103 only + durability gear (he's naked); PRESERVE job 26
#     + jobLevel (NOT raised — keeps his kit damage/soft-status, no hard-lock Hell Ivy spam) + secondary
#     + weapon + survive scripting. NO rare loot (he survives).
#   - Ninjas: the headline — dual-wield (innate Two Swords -> two Ninja Longblades, NOT a two-hand
#     marker) + high Move for the wall-climb vantage + Throw (innate). Lead L102, others L101.
#   - Summoners: mid-tier AoE shelling the central path. L101.
def yardrow(data):
    E = 428
    # Marach BOSS — level + durability only; preserve job 26 / jl / kit / weapon / survive scripting.
    set_slot(data, E, 1, level=103, head=MAGE_HAT, body=SHOP_ROBE, acc=BRACERS)
    for s, lvl in ((2, 102), (4, 101), (6, 101)):  # 3 Ninja — dual-wield wall-climbing assassins
        set_slot(data, E, s, level=lvl, joblevel=8, job=NINJA,
                 reaction=FIRST_STRIKE, support=ATK_BOOST, movement=MV2,
                 head=THIEFS_CAP, body=BLACK_GARB, acc=GERMINAS, rh=NINJA_BLADE, lh=NINJA_BLADE)
    for s in (3, 5):  # 2 Summoners — mid-tier AoE shelling the central path
        set_slot(data, E, s, level=101, joblevel=8, job=SUMMONER,
                 reaction=REFLEXES, support=ATK_BOOST, movement=MV1,
                 head=MAGE_HAT, body=SHOP_ROBE, acc=FEATHERWEAVE, rh=SHOP_ROD, lh=LH_EMPTY)
    # s0 Rapha (protected guest): NOT touched — runtime level-scaler + her vanilla evasion gear.
    return [E]


# ---------------------------------------------------------------------------
# Battle 029 — The Yuguewood (entry 430): second undead fight + living caster backline. Per docs/032.
# Vanilla 430: s0 = Rapha placeholder (job 25, level 0xFE — inactive, leave alone); s1,s3 Black Mage
# (enemy-variant job 66, equips ROD); s2,s4 Time Mage (enemy-variant job 68, equips STAFF); s5 Ghoul
# (112), s6 Ghast (113), s7 Revenant (114) — the 3 undead (monsters carry no gear). The undead sit at
# level 0xFE in the base .bin (the norm for undead game-wide); per the tchigolith (410) monster-scaling
# precedent we set their LEVEL+jl directly. NOTE: if the enhanced edition's OverrideEntryData drives
# undead levels for this entry, that layer wins — verify in-game that the undead scale (else move them
# to the override layer). The slots unambiguously belong here (unique undead+caster roster match).
#   - Black Mages: ranged elemental punishment (jl8, Rod). One L101, one L100.
#   - Time Mages: Haste(undead)/Slow(player)/Float ONLY -> jl CAPPED to 4 (no Stop/Immobilize). Staff.
#   - Undead: reraising attrition core; level+jl only. PRESERVE undead flags (reraise / heal-damages /
#     Phoenix-Down-instakill / Seal-Evil / Entice) and the swamp terrain — untouched (we only scale).
#   - No boss -> no rare loot.
def yuguewood(data):
    E = 430
    for s, lvl in ((1, 101), (3, 100)):  # 2 Black Mages — ranged elemental (Rod, jl8)
        set_slot(data, E, s, level=lvl, joblevel=8, job=BMAGE,
                 reaction=REFLEXES, support=ATK_BOOST, movement=MV1,
                 head=MAGE_HAT, body=SHOP_ROBE, acc=FEATHERWEAVE, rh=SHOP_ROD, lh=LH_EMPTY)
    for s in (2, 4):  # 2 Time Mages — Haste/Slow only (jl4), Staff (job-legal)
        set_slot(data, E, s, level=101, joblevel=4, job=TMAGE,
                 reaction=REFLEXES, movement=MV1,
                 head=MAGE_HAT, body=SHOP_ROBE, acc=FEATHERWEAVE, rh=SHOP_STAFF, lh=LH_EMPTY)
    # 3 undead — level+jl only (monsters, no gear); preserve reraise/heal-weakness/Seal-Evil flags.
    set_slot(data, E, 5, level=100, joblevel=8)  # Ghoul
    set_slot(data, E, 6, level=100, joblevel=8)  # Ghast
    set_slot(data, E, 7, level=101, joblevel=8)  # Revenant (tougher anchor)
    return [E]


# ---------------------------------------------------------------------------
# Battle 030 — Riovanes Castle Gate (entry 431): bridge-and-high-ground assault; Riovanes chain 1/3.
# Vanilla 431: s0 = Rapha placeholder (job 25, level 0xFE — inactive, leave alone); s1 = Marach (job 26
# Netherseer, enemy BOSS, survives/recruitable — nearly naked, only Gokuu's Pole 111); s2,s3,s4 Archer
# (77); s5,s6,s7,s8 Knight (76) — TIC has 4 Knights, one more than the walkthrough's 3 (cf. Goug's
# extra thieves). Per docs/033.
#   - ESCALATION: swap ONE Knight (s5) -> Knights Templar (job 38, the Izlude caste) for Mighty-Sword
#     ranged breaks (makes Safeguard a real demand on the crossing). VERIFY in-game: job 38 on a generic
#     sprite is the Izlude job applied to a generic slot — confirm it renders/behaves.
#   - Marach: BOSS that SURVIVES. Level 103 + durability gear only (naked); PRESERVE job 26 / jobLevel
#     (not raised — kit stays damage/soft-status) / secondary / weapon / survive scripting. NO rare.
#   - Knights (s6,s7,s8): bridge bodies; Rend innate (Battle Skill). Heavy gear + shop shield.
#   - Archers (s2,s3,s4): elevated bowfire; one anchor at 102. Keep it winnable into the no-resupply Keep.
def riovanes_gate(data):
    E = 431
    # Marach BOSS — level + durability only; preserve job 26 / jl / kit / weapon / survive scripting.
    set_slot(data, E, 1, level=103, head=MAGE_HAT, body=SHOP_ROBE, acc=BRACERS)
    # s5 Knight -> Knights Templar (NEW swap) — ranged Mighty-Sword breaks; KnightSword/heavy gear.
    set_slot(data, E, 5, level=102, joblevel=8, job=TEMPLAR, secondary=0,
             reaction=COUNTER, support=ATK_BOOST, movement=MV1,
             head=HEAVY_HELM, body=HEAVY_ARMOR, acc=BRACERS, rh=RUNEBLADE, lh=SHOP_SHIELD)
    for s in (6, 7, 8):  # 3 Knights — bridge bodies; Rend innate
        set_slot(data, E, s, level=101, joblevel=8, job=KNIGHT,
                 reaction=COUNTER, support=ATK_BOOST, movement=MV1,
                 head=HEAVY_HELM, body=HEAVY_ARMOR, acc=BRACERS, rh=RUNEBLADE, lh=SHOP_SHIELD)
    for s, lvl in ((2, 102), (3, 101), (4, 100)):  # 3 Archers — elevated bowfire (s2 = high anchor)
        set_slot(data, E, s, level=lvl, joblevel=8, job=ARCHER, secondary=FUNDAMENTS,
                 reaction=REFLEXES, support=CONCENTRATION, movement=MV1,
                 head=THIEFS_CAP, body=BLACK_GARB, acc=BRACERS, rh=WINDSLASH, lh=LH_TWOHAND)
    return [E]


# ---------------------------------------------------------------------------
# Battle 031 — Riovanes Castle Keep (entry 432): the CHAPTER SPIKE; two-phase Wiegraf -> Belias.
# Vanilla 432: s0 = Wiegraf (job 40 Holy Knight, GEARED — the PHASE-1 solo-duel boss); s1-s4 = lvl-1/
# jl-0 placeholder Knights and s9-s11 = lvl-1 placeholder Wiegraf slots — these are TRANSFORM-SCRIPTING
# artifacts, DO NOT TOUCH; s5 = Belias/Velius (job 60 Lucavi demon, no equip slots); s6,s7,s8 =
# Archaeodaemon (job 153, demon adds — only 3 in TIC, walkthrough says 4). Per docs/034.
#   - Wiegraf (P1 duel): level 104 + Defender (33, his rare; Steal-Weapon target). PRESERVE job 40 /
#     secondary 53 / jobLevel / his other gear / the SOLO-DUEL deployment lock + transform trigger.
#     FAIRNESS: no skillset change -> no new hard lock; a prepared solo Ramza still wins.
#   - Belias (P2 Lucavi): level 105 only (chapter top). PRESERVE job 60 / demon kit / transform + spawn.
#     Defense Ring (his rare) CANNOT be set here (demon has no equip slots, eq=255) -> it must be a
#     REWARD-LAYER item (guaranteed reward), tracked as a TODO outside this ENTD patch.
#   - Archaeodaemons: demon adds, level only (no gear). 103/103/102.
def riovanes_keep(data):
    E = 432
    # Wiegraf PHASE-1 duel boss: complete but still disarmable/stealable. Preserve job 40 and scripting.
    set_slot(data, E, 0, level=104, joblevel=8, secondary=PUGILISM, brave=88, faith=60,
             reaction=COUNTER, support=ATK_BOOST, movement=MV2,
             head=HEAVY_HELM, body=HEAVY_ARMOR, acc=BRACERS, rh=DEFENDER, lh=SHOP_SHIELD)
    # Belias PHASE-2 Lucavi: no gear slots; keep canonical demon kit and transform/spawn.
    set_slot(data, E, 5, level=105, joblevel=8, brave=88, faith=82)
    for s, lvl in ((6, 103), (7, 103), (8, 102)):  # 3 Archaeodaemon adds — monsters, no gear.
        set_slot(data, E, s, level=lvl, joblevel=8, brave=84, faith=72)
    return [E]


# ---------------------------------------------------------------------------
# Battle 032 — Riovanes Castle Roof (entry 433): CHAPTER FINALE; Elmdor + the assassins. Per docs/035.
# Vanilla 433: s0 = Rapha (job 41 Skyseer, GUEST control 00 84 — protected NPC, fail-on-death; same
# evasion gear as her Yardow appearance); s1 = job-41 lvl-5 enemy CLONE of Rapha + s2 = job-18
# Netherseer lvl-5 (Marach-class) — both lvl-5 SCRIPTING placeholders, DO NOT TOUCH; s3 = Elmdor
# (job 27 Ark Knight); s4 = Celia (job 45 Assassin); s5 = Lettie (job 46 Assassin). All three enemies
# FLEE on critical (none die) -> NO loot; preserve their special kits + the flee-on-critical scripting.
#   - The 3 enemies: keep original ability fields, but upgrade iconic gear; preserve the flee-on-critical
#     trigger + protect-Rapha fail condition + 4-unit cap.
#   - Rapha (s0): controlled in NG+, direct ENTD level/control/gear, and runtime guest stat growth via
#     UnitID 0x29 (the script clone is uid 0x80, so the runtime guard can distinguish them).
def riovanes_roof(data):
    E = 433
    set_slot(data, E, 0, level=100, jobrank=generic_job_rank(WMAGE), joblevel=8,
             secondary=WHITE_MAGICKS, brave=65, faith=75,
             reaction=MANA_SHIELD, support=DEFENSE_BOOST, movement=MOVE_MP_UP,
             head=THIEFS_CAP, body=SHOP_ROBE, acc=FEATHERWEAVE, rh=113, lh=LH_TWOHAND)
    set_player_control(data, E, 0)
    set_slot(data, E, 3, level=104, joblevel=7, secondary=0, brave=90, faith=65,
             reaction=FIRST_STRIKE, support=DOUBLEHAND, movement=IGNORE_HEIGHT,
             head=GENJI_HELM, body=GENJI_ARMOR, acc=GENJI_GLOVES, rh=CHIRIJIRADEN, lh=GENJI_SHIELD)
    set_slot(data, E, 4, level=103, joblevel=8, secondary=254, brave=90, faith=60,
             reaction=510, support=510, movement=510,
             head=HAIRBAND, body=NINJA_GEAR, acc=ENVOUTEMENT, rh=MASAMUNE, lh=LH_TWOHAND)
    set_slot(data, E, 5, level=103, joblevel=8, secondary=254, brave=90, faith=60,
             reaction=510, support=510, movement=510,
             head=BARRETTE, body=NINJA_GEAR, acc=SORTILEGE, rh=KOGA_BLADE, lh=KOGA_BLADE)
    for s in (3, 4, 5):
        set_spoil(data, E, s, 0)
    return [E]


# ===========================================================================
# CHAPTER 4 — "In the Name of Love" (the endgame). Entries in entd4 (Ch3 ended at 433).
# Generics 100-103, Ultima-Demon bodies 103, sub-bosses 103-104, human bosses 104-105, Lucavi 105,
# final Ultima 106. The reserved best-in-slot gear (Unknown20 tier) finally unlocks here, TIERED:
# Tier A (Save the Queen/Masamune/Genji/Aegis/Grand Helm) on mid-Ch4 bosses; Tier S (Chaos Blade/
# Ribbon/Escutcheon/Robe of Lords/Materia Blade/Ragnarok) on the endgame sequence only. Per docs/037.
# ---------------------------------------------------------------------------
# Battle 033 — Dugeura Pass (entry 442): Ch4 open-field opener; AoE-priority + Jump-dodge. Per docs/038 v3.
# Vanilla 442: s0 Knight (76); s1,s3 Black Mage (80); s2 Archer (77); s4,s5 Dragoon (87). All enemies,
# no gear. No boss -> no rare; bottom-of-band levels (101-102), not a spike.
#   - v3: s0 Knight -> Samurai parry screen; s2 old Time Mage connector -> Geomancer terrain bruiser.
#   - 2 Black Mages: Mana Shield + Swiftness + Manafont priority casters. 2 Dragoons: Jump pressure.
def dugeura(data):
    E = 442
    set_slot(data, E, 0, level=101, joblevel=8, job=SAMURAI,
             secondary=GEOMANCY, brave=88, faith=60,
             reaction=SHIRAHADORI, support=DOUBLEHAND, movement=MV2,
             head=HEAVY_HELM, body=HEAVY_ARMOR, acc=MAGEPOWER_GLOVES,
             rh=KIKU_ICHIMONJI, lh=LH_TWOHAND)
    set_slot(data, E, 1, level=102, joblevel=8, job=BMAGE,
             secondary=WHITE_MAGICKS, brave=60, faith=84,
             reaction=MANA_SHIELD, support=SWIFTSPELL, movement=MOVE_MP_UP,
             head=MAGE_HAT, body=BLACK_ROBE, acc=BARRETTE, rh=SHOP_ROD, lh=LH_EMPTY)
    set_slot(data, E, 2, level=102, joblevel=8, job=GEOMANCER,
             secondary=MARTIAL_ARTS, brave=84, faith=60,
             reaction=NATURES_WRATH, support=ATK_BOOST, movement=MV2,
             head=THIEFS_CAP, body=POWER_GARB, acc=RED_SHOES, rh=RUNEBLADE, lh=LH_EMPTY)
    set_slot(data, E, 3, level=102, joblevel=8, job=BMAGE,
             secondary=TIME_MAGICKS, brave=60, faith=84,
             reaction=MANA_SHIELD, support=SWIFTSPELL, movement=MOVE_MP_UP,
             head=MAGE_HAT, body=BLACK_ROBE, acc=BARRETTE, rh=SHOP_ROD, lh=LH_EMPTY)
    for s, lvl in ((4, 102), (5, 101)):  # 2 Dragoons — Jump (innate); vertical back-line pressure
        set_slot(data, E, s, level=lvl, joblevel=8, job=LANCER,
                 secondary=MARTIAL_ARTS, brave=86, faith=40,
                 reaction=DRAGONHEART, support=ATK_BOOST, movement=IGNORE_HEIGHT,
                 head=HEAVY_HELM, body=HEAVY_ARMOR, acc=HERMES_SHOES, rh=OBELISK, lh=LH_EMPTY)
    return [E]


# ---------------------------------------------------------------------------
# Battle 034 — Free City of Bervenia (entry 443): first Ch4 boss duel; Meliadoul (Templar). Per docs/039.
# Vanilla 443: s0 = Meliadoul (job 47 Divine Knight, GEARED, wields Defender 33 — win = defeat her,
# she DIES); s1,s4 Summoner (82); s2,s3 Archer (77); s5 Ninja (89). Per docs/039.
#   - Meliadoul: BOSS L104 + jl8 (full Mighty Sword break kit). Her Tier-A rare = SAVE THE QUEEN (34)
#     as her equipped KnightSword (steal-bait; job 47 equips KnightSword — verified). Upgrades her
#     vanilla Defender. PRESERVE job 47 / secondary / other gear (helm/armor/acc/shield) / win-on-death
#     scripting. Break is telegraphed (Safeguard/Steal Weapon answer it); no hard lock added.
#   - v3 adjusted: Summoners are complete charge-time screens, both Archers remain lane pressure,
#     and the vanilla Ninja becomes a Counter Monk flanker.
def bervenia(data):
    E = 443
    # Meliadoul BOSS: preserve job/identity/accessory/scripting; equip Save the Queen as steal-bait.
    set_slot(data, E, 0, level=104, joblevel=8, secondary=FUNDAMENTS, brave=88, faith=78,
             reaction=COUNTER, support=MAGICK_DEFENSE_BOOST, movement=MV2,
             head=HEAVY_HELM, body=MIRROR_MAIL, rh=SAVE_THE_QUEEN, lh=CRYSTAL_SHIELD)

    # 2 Summoners: split White/Time secondary, no instant casts; Swiftspell keeps the charge-clock relevant.
    set_slot(data, E, 1, level=102, joblevel=8, job=SUMMONER, secondary=WHITE_MAGICKS,
             brave=60, faith=84, reaction=SOULBIND, support=SWIFTSPELL, movement=MV2,
             head=MAGE_HAT, body=WIZARD_ROBE, acc=FEATHERWEAVE, rh=SHOP_ROD, lh=LH_EMPTY)
    set_slot(data, E, 4, level=102, joblevel=8, job=SUMMONER, secondary=TIME_MAGICKS,
             brave=60, faith=84, reaction=SOULBIND, support=SWIFTSPELL, movement=MV2,
             head=MAGE_HAT, body=WIZARD_ROBE, acc=FEATHERWEAVE, rh=SHOP_ROD, lh=LH_EMPTY)

    # Two high-ground Archers cover approach lanes without adding another break source.
    set_slot(data, E, 2, level=102, joblevel=8, job=ARCHER, secondary=ITEMS,
             brave=88, faith=55, reaction=REFLEXES, support=THROW_ITEMS, movement=IGNORE_HEIGHT,
             head=THIEFS_CAP, body=BLACK_GARB, acc=BRACERS, rh=WINDSLASH, lh=LH_TWOHAND)
    set_slot(data, E, 3, level=102, joblevel=8, job=ARCHER, secondary=ITEMS,
             brave=88, faith=55, reaction=REFLEXES, support=THROW_ITEMS, movement=IGNORE_HEIGHT,
             head=THIEFS_CAP, body=BLACK_GARB, acc=BRACERS, rh=WINDSLASH, lh=LH_TWOHAND)

    # Monk replaces the vanilla Ninja as fast physical flank pressure without rare weapon leakage.
    set_slot(data, E, 5, level=102, joblevel=8, job=MONK, secondary=ITEMS,
             brave=90, faith=35, reaction=COUNTER, support=DUAL_WIELD, movement=MV2,
             head=LH_EMPTY, body=BLACK_GARB, acc=BRACERS, rh=LH_EMPTY, lh=LH_EMPTY)
    return [E]


# ---------------------------------------------------------------------------
# Battle 035 — Finnath Creek (entry 444): wild chocobo menagerie; RANDOMIZED flock. Per docs/040.
# Vanilla 444 is a 12-slot RANDOM POOL, all at level 0xFE (runtime-driven spawn/level, unlike fixed
# battles): s0-s5 Chocobo(94, yellow), s6-s9 Red Chocobo(96), s10 Black Chocobo(95), s11 Pig(121).
# No boss, no rare; a light change-of-pace.
#   - DE-RANDOMIZE per v3 doc: clear the six 0x50 variant records and keep the six 0x90 base records
#     as a fixed flock: 2 Red Chocobo, 2 yellow Chocobo, 1 Black Chocobo, 1 Wild Boar.
#   - PRESERVE the boar-family slot (s11) + its Entice-recruit/poach tail; only set job/level/Br/Fa.
#   ⚠️ VERIFY in-game: if this randomized battle ignores ENTD level bytes, move the Ch4 levels
#     (Red 102 / yellow+Black 101 / Wild Boar 100) to the OverrideEntryData layer.
def finath(data):
    E = 444
    for s in range(0, 6):
        clear_slot(data, E, s)
    for s in (6, 7):  # 2 Red Chocobo — fast ranged tempo pressure
        set_slot(data, E, s, level=102, joblevel=8, job=RED_CHOCOBO, brave=90, faith=30)
    for s in (8, 9):  # 2 yellow Chocobo — Choco Cure sustain
        set_slot(data, E, s, level=101, joblevel=8, job=CHOCOBO, brave=90, faith=30)
    set_slot(data, E, 10, level=101, joblevel=8, job=BLACK_CHOCOBO, brave=90, faith=30)
    set_slot(data, E, 11, level=100, joblevel=8, job=WILD_BOAR, brave=60, faith=40)
    return [E]


# ---------------------------------------------------------------------------
# Battle 036 — Outlying Church / Zeltennia (entry 445): Zalmo dies at last; elevated holy-boss duel.
# Vanilla 445: s0 = inactive guest placeholder (job 5, level 0xFE, control 00 84 — leave alone);
# s1 = Zalmo (job 16 Celebrant/Inquisitor, GEARED, wields a rod; win = defeat him, he DIES here, paying
# his Ch3-deferred rare); s2,s3 Mystic (85); s4,s5,s6 Knight (76). Per docs/041.
#   - Zalmo: BOSS L104/jl8. Light Robe body + Sortilege and Whale Whisker steal-bait; preserve
#     job/win-on-death scripting and avoid Angel Ring/Reraise gear.
#   - 2 Mystics: soft status with Black Magicks secondary; Arithmetician bucket seeds math JP/JL.
#   - 2 Rend Knights + 1 lower-JL bodyguard Knight (s6) to respect the <=2 break-source cap.
#   - PRESERVE the vanilla guaranteed Angel Ring reward + buried map rares (different layer, untouched).
def outlying_church(data):
    E = 445
    # Zalmo BOSS: Light Robe/Sortilege steal-bait; Whale Whisker is two-handed.
    set_slot(data, E, 1, level=104, jobrank=generic_job_rank(MYSTIC), joblevel=8,
             secondary=MYSTIC_ARTS, brave=72, faith=82,
             reaction=REFLEXES, support=DEFENSE_BOOST, movement=MV2,
             head=MAGE_HAT, body=LIGHT_ROBE, acc=SORTILEGE, rh=WHALE_WHISKER, lh=LH_TWOHAND)
    for s in (2, 3):  # 2 Mystics: soft status plus Black Magicks; Arithmetician bucket at JL8.
        set_slot(data, E, s, level=102, jobrank=generic_job_rank(ARITHMETICIAN), joblevel=8,
                 job=MYSTIC, secondary=BLACK_MAGICKS,
                 brave=68 if s == 2 else 72, faith=78 if s == 2 else 82,
                 reaction=MANA_SHIELD, support=SWIFTSPELL, movement=MOVE_MP_UP,
                 head=MAGE_HAT, body=BLACK_ROBE, acc=MAGEPOWER_GLOVES, rh=SHOP_ROD, lh=LH_EMPTY)
    for s, lvl in ((4, 102), (5, 102), (6, 101)):  # 0x17 restored to the vanilla value for this battle.
        set_slot(data, E, s, level=lvl, jobrank=generic_job_rank(MONK), joblevel=8,
                 job=KNIGHT, secondary=MARTIAL_ARTS,
                 brave=88, faith=42,
                 reaction=FIRST_STRIKE, support=ATK_BOOST, movement=MV2,
                 head=HEAVY_HELM, body=HEAVY_ARMOR, acc=GENJI_GLOVES, rh=RUNEBLADE, lh=SHOP_SHIELD,
                 palette=4)
    return [E]


# ---------------------------------------------------------------------------
# Battle 037 — Beddha Sandwaste / Bed Desert (entry 447): open-desert gun-duel; Barich. Per docs/042 v3.
# Vanilla 447: s0 = Barich (job 43 Machinist, win = defeat him); s1,s2 Knight (76); s3 Black Mage (80);
# s4,s5 Archer (77); s6,s7 job-43 Barich-clone scripting placeholders (jl0, tail 04 d0 — leave untouched).
# v3 keeps six active enemies: Barich + 2 Samurai + 2 Geomancers + Black Mage. Glacial/Blaze/Blaster
# remain guaranteed spoils only; Barich's active steal/disarm bait is Stoneshooter.
def bed_desert(data):
    E = 447
    set_slot(data, E, 0, level=104, joblevel=8, secondary=0, brave=84, faith=55,
             reaction=REFLEXES, support=DEFENSE_BOOST, movement=JUMP3,
             head=THIEFS_CAP, body=BLACK_GARB, acc=FEATHERWEAVE, rh=STONESHOOTER, lh=LH_TWOHAND)
    for s in (1, 2):  # 2 Samurai — parry screen, no Rend/break pressure.
        set_slot(data, E, s, level=102, joblevel=8, job=SAMURAI, secondary=MARTIAL_ARTS,
                 brave=88, faith=60,
                 reaction=SHIRAHADORI, support=DOUBLEHAND, movement=MV3,
                 head=HEAVY_HELM, body=HEAVY_ARMOR, acc=POWER_GAUNTLETS,
                 rh=KIKU_ICHIMONJI, lh=LH_TWOHAND)
    set_slot(data, E, 3, level=102, joblevel=8, job=BMAGE,  # Black Mage — AoE punishing clumps.
             secondary=ITEMS, brave=60, faith=84,
             reaction=REFLEXES, support=MAGICK_BOOST, movement=MV1,
             head=MAGE_HAT, body=BLACK_ROBE, acc=FEATHERWEAVE, rh=SHOP_ROD, lh=LH_EMPTY)
    for s, lvl in ((4, 102), (5, 101)):  # 2 Geomancers — terrain bruisers on open desert lanes.
        set_slot(data, E, s, level=lvl, joblevel=8, job=GEOMANCER, secondary=ITEMS,
                 brave=84, faith=60,
                 reaction=NATURES_WRATH, support=ATK_BOOST, movement=MV2,
                 head=MAGE_HAT, body=POWER_GARB, acc=MAGEPOWER_GLOVES, rh=RUNEBLADE, lh=LH_EMPTY)
    return [E]


# ---------------------------------------------------------------------------
# Battle 038 — Fort Besselat S/N Wall (entries 448 South, 449 North): branching wall assault. Per docs/043.
# Player picks ONE wall; both converge on the Sluice (044). No boss, no rare; low Ch4 band (101-102),
# verticality carries the difficulty.
#   SOUTH 448 (melee/stealth): s0,s1,s2 Knight (76); s3,s4 Archer (77); s5 Ninja (89); s6 Thief (83).
#   NORTH 449 (ranged/AoE):    s0 Knight leader; s1,s2 Geomancer; s3 BMage shooter; s4 Summoner;
#     s5 Knight bruiser. Constraints carried: Summoner charge times intact, no added unit, low Ch4 band.
def besselat_wall(data):
    # --- South Wall (448) — melee/stealth ---
    S = 448
    set_slot(data, S, 0, level=101, joblevel=8, job=KNIGHT, secondary=HOLY_SWORD_AGRIAS,
             brave=88, faith=42,
             reaction=COUNTER, support=ATK_BOOST, movement=MV3,
             head=HEAVY_HELM, body=HEAVY_ARMOR, acc=BRACERS, rh=DEFENDER, lh=CRYSTAL_SHIELD)
    for s in (1, 2):
        set_slot(data, S, s, level=102, jobrank=generic_job_rank(SAMURAI), joblevel=8,
                 job=KNIGHT, secondary=AIM,
                 brave=88, faith=42,
                 reaction=DRAGONHEART, support=DEFENSE_BOOST, movement=MV3,
                 head=HEAVY_HELM, body=MIRROR_MAIL, acc=BRACERS, rh=GASTROPHETES, lh=CRYSTAL_SHIELD)
    for s, lvl, gun in ((3, 102, GLACIAL_GUN), (4, 101, BLASTER)):
        set_slot(data, S, s, level=lvl, joblevel=0, job=BMAGE, secondary=0,
                 brave=62, faith=84,
                 reaction=REFLEXES, support=EQUIP_GUNS, movement=TELEPORT,
                 head=MAGE_HAT, body=WIZARD_ROBE, acc=MAGEPOWER_GLOVES, rh=gun, lh=LH_TWOHAND)
    set_slot(data, S, 5, level=102, joblevel=8, job=NINJA,
             secondary=MARTIAL_ARTS, brave=90, faith=35,
             reaction=COUNTER, support=BRAWLER, movement=JUMP3,
             head=THIEFS_CAP, body=POWER_GARB, acc=BRACERS, rh=LH_EMPTY, lh=LH_EMPTY)
    set_slot(data, S, 6, level=101, joblevel=8, job=MONK,
             secondary=0, brave=88, faith=38,
             reaction=COUNTER, support=DUAL_WIELD, movement=JUMP3,
             head=BARRETTE, body=POWER_GARB, acc=BRACERS, rh=LH_EMPTY, lh=LH_EMPTY)
    # --- North Wall (449) — ranged/AoE v3 ---
    N = 449
    set_slot(data, N, 0, level=102, jobrank=generic_job_rank(MONK), joblevel=8,
             job=KNIGHT, secondary=HOLY_SWORD_AGRIAS,
             brave=88, faith=42,
             reaction=COUNTER, support=ATK_BOOST, movement=MV3,
             head=HEAVY_HELM, body=HEAVY_ARMOR, acc=BRACERS, rh=DEFENDER, lh=CRYSTAL_SHIELD)
    for s, lvl in ((1, 102), (2, 101)):
        set_slot(data, N, s, level=lvl, joblevel=8, job=GEOMANCER, secondary=0,
                 brave=86, faith=40,
                 reaction=NATURES_WRATH, support=MAGICK_BOOST, movement=MV2,
                 head=MAGE_HAT, body=WIZARD_ROBE, acc=GEMS_108, rh=RUNEBLADE, lh=AEGIS_SHIELD)
    set_slot(data, N, 3, level=101, joblevel=0, job=BMAGE, secondary=0,
             brave=62, faith=84,
             reaction=REFLEXES, support=EQUIP_GUNS, movement=TELEPORT,
             head=MAGE_HAT, body=WIZARD_ROBE, acc=MAGEPOWER_GLOVES, rh=BLAZE_GUN, lh=LH_TWOHAND)
    # Keep the talk-trigger Knight in s0, but swap its battlefield position with the BMage shooter.
    set_position(data, N, 0, x=7, y=4)
    set_position(data, N, 3, x=9, y=7)
    set_slot(data, N, 4, level=102, joblevel=8, job=SUMMONER, secondary=TIME_MAGICKS,
             brave=60, faith=84,
             reaction=SOULBIND, support=SWIFTSPELL, movement=MV2,
             head=MAGE_HAT, body=WIZARD_ROBE, acc=FEATHERWEAVE, rh=SHOP_ROD, lh=LH_EMPTY)
    set_slot(data, N, 5, level=102, jobrank=generic_job_rank(MONK), joblevel=8,
             job=KNIGHT, secondary=MARTIAL_ARTS,
             brave=88, faith=40,
             reaction=FIRST_STRIKE, support=DUAL_WIELD, movement=MV3,
             head=HEAVY_HELM, body=HEAVY_ARMOR, acc=BRACERS, rh=RUNEBLADE, lh=RUNEBLADE)
    return [S, N]


# ---------------------------------------------------------------------------
# Battle 039 — Fort Besselat Sluice Gate (entry 450): floodgate-lever objective map. Per docs/044.
# Vanilla 450: s0,s1 Archer (77); s2,s3,s6,s7 Knight (76); s4,s5 Black Mage (80). No boss, no rare;
# low Ch4 band. The "open the water gate" lever objective + lever tiles are scripting — untouched.
#   - v3: both Black Mages carry Summon; s6/s7 are Samurai-bucket lever Knights; s2/s3 become
#     battle Samurais; s0/s1 become Geomancers. No Time Mage, Rend wall, new slot, or script edit.
def besselat_sluice(data):
    E = 450
    # v3 keeps all eight static slots and the lever scripting untouched. The caster screen returns
    # to two Black Mages, with Summoner bucket data so Summon is the charged objective pressure.
    for s in (4, 5):
        set_slot(data, E, s, level=100, jobrank=generic_job_rank(SUMMONER), joblevel=8,
                 job=BMAGE, secondary=SUMMON, brave=60, faith=84,
                 reaction=REFLEXES, support=SWIFTSPELL, movement=MV2,
                 head=MAGE_HAT, body=BLACK_ROBE, acc=FEATHERWEAVE,
                 rh=SHOP_ROD, lh=LH_EMPTY)

    # In-game placement confirmation: s6/s7 are the two units protecting the lever tiles. They remain
    # Knights, but use the documented Samurai bucket. Their job byte must stay Knight (76).
    for s in (6, 7):
        set_slot(data, E, s, level=102, jobrank=generic_job_rank(SAMURAI), joblevel=8,
                 job=KNIGHT, secondary=AIM, brave=88, faith=42,
                 reaction=REFLEXES, support=DEFENSE_BOOST, movement=MV2,
                 head=HEAVY_HELM, body=MIRROR_MAIL, acc=BRACERS,
                 rh=GASTROPHETES, lh=CRYSTAL_SHIELD)

    # s2/s3 are the mobile battle screen and become MA-boosted Samurais with Masamune pressure.
    # Kaiser Shield remains guaranteed on s2 through the untouched 0x1e spoils byte.
    for s in (2, 3):
        set_slot(data, E, s, level=100, jobrank=generic_job_rank(SAMURAI), joblevel=8,
                 job=SAMURAI, secondary=0, brave=88, faith=42,
                 reaction=DRAGONHEART, support=MAGICK_BOOST, movement=MV3,
                 head=HEAVY_HELM, body=MIRROR_MAIL, acc=BRACERS,
                 rh=MASAMUNE, lh=CRYSTAL_SHIELD)

    # Former Archer lanes become Geomancers. Their terrain pressure keeps both approach lanes relevant.
    for s, lvl in ((0, 100), (1, 100)):
        set_slot(data, E, s, level=lvl, jobrank=generic_job_rank(GEOMANCER), joblevel=8,
                 job=GEOMANCER, secondary=0, brave=82, faith=45,
                 reaction=SHIRAHADORI, support=MAGICK_BOOST, movement=MV2,
                 head=MAGE_HAT, body=WIZARD_ROBE, acc=GEMS_108,
                 rh=RUNEBLADE, lh=CRYSTAL_SHIELD)
    return [E]


# ---------------------------------------------------------------------------
# Battle 040 — Mount Germinas (entry 452): 4/5-star vertical mobility/steal skirmish. Per docs/045.
# v3: 2 Ninjas + 2 Thieves + 2 Archers. Three Martial Arts users check all-party Shihadori while the
# Throw Thief and Yoichi Archers preserve the mountain-bandit crossfire. Positions, event data, buried
# Invisibility Cloak, and guaranteed Ninja Gear/Koga/Iga spoils remain untouched.
def germinas(data):
    E = 452
    set_slot(data, E, 0, level=102, jobrank=generic_job_rank(SAMURAI), joblevel=8, job=NINJA,
             secondary=MARTIAL_ARTS, brave=90, faith=35,
             reaction=SHIRAHADORI, support=BRAWLER, movement=JUMP3,
             head=THIEFS_CAP, body=NINJA_GEAR, acc=BRACERS, rh=KOGA_BLADE, lh=IGA_BLADE)
    set_slot(data, E, 1, level=101, jobrank=generic_job_rank(MONK), joblevel=8, job=NINJA,
             secondary=MARTIAL_ARTS, brave=90, faith=38,
             reaction=FIRST_STRIKE, support=BRAWLER, movement=MV3,
             head=HEADBAND, body=POWER_GARB, acc=BRACERS, rh=LH_EMPTY, lh=LH_EMPTY)
    set_slot(data, E, 2, level=101, jobrank=generic_job_rank(MONK), joblevel=8, job=THIEF,
             secondary=MARTIAL_ARTS, brave=88, faith=38,
             reaction=REFLEXES, support=BRAWLER, movement=MV3,
             head=HEADBAND, body=POWER_GARB, acc=BRACERS, rh=LH_EMPTY, lh=LH_EMPTY)

    # Slot 4's central ledge Archer becomes the roving Throw Thief; slots 3 and 5 keep separate bow angles.
    set_slot(data, E, 4, level=100, jobrank=generic_job_rank(NINJA), joblevel=8, job=THIEF,
             secondary=THROW, brave=88, faith=38,
             reaction=SPEED_SURGE, support=DUAL_WIELD, movement=JUMP3,
             head=THIEFS_CAP, body=POWER_GARB, acc=BRACERS,
             rh=ZWILL_STRAIGHTBLADE, lh=ASSASSINS_DAGGER)
    for s, lvl in ((3, 102), (5, 100)):
        set_slot(data, E, s, level=lvl, jobrank=generic_job_rank(MIME), joblevel=8,
                 job=ARCHER, secondary=ITEMS, brave=82, faith=45,
                 reaction=REFLEXES, support=THROW_ITEMS, movement=JUMP3,
                 head=THIEFS_CAP, body=POWER_GARB, acc=BRACERS, rh=YOICHI_BOW, lh=LH_TWOHAND)
    return [E]


def poeskas(data):
    # Battle 41 - Lake Poescas: all-undead permakill field. Jobs 63/70/71 are special HUMAN undead jobs
    # with legal equipment categories and innate Float + Undead; only s4/s5 (Revenant 114) are monsters.
    # v3 completes the four human kits while preserving every main job, position, flag, objective, and
    # reward payload. Four of six enemies stay at 100-101; only the Mystic/Summoner anchors reach 102.
    E = 453
    set_slot(data, E, 0, level=102, jobrank=generic_job_rank(MIME), joblevel=8, job=70,
             secondary=GEOMANCY, brave=72, faith=84,
             reaction=MANA_SHIELD, support=MAGICK_BOOST, movement=MV2,
             head=MAGE_HAT, body=BLACK_ROBE, acc=MAGEPOWER_GLOVES, rh=SHOP_ROD, lh=LH_EMPTY)
    set_slot(data, E, 1, level=101, jobrank=generic_job_rank(MIME), joblevel=8, job=63,
             secondary=ITEMS, brave=88, faith=70,
             reaction=REFLEXES, support=THROW_ITEMS, movement=JUMP3,
             head=THIEFS_CAP, body=POWER_GARB, acc=BRACERS, rh=YOICHI_BOW, lh=LH_TWOHAND)
    set_slot(data, E, 2, level=100, jobrank=generic_job_rank(CHEMIST), joblevel=8, job=63,
             secondary=ITEMS, brave=88, faith=70,
             reaction=REFLEXES, support=THROW_ITEMS, movement=MV3,
             head=THIEFS_CAP, body=RUBBER_SUIT, acc=FEATHERWEAVE, rh=YOICHI_BOW, lh=LH_TWOHAND)
    set_slot(data, E, 3, level=102, jobrank=generic_job_rank(SUMMONER), joblevel=8, job=71,
             secondary=BLACK_MAGICKS, brave=72, faith=84,
             reaction=REFLEXES, support=SWIFTSPELL, movement=MOVE_MP_UP,
             head=MAGE_HAT, body=BLACK_ROBE, acc=MAGEPOWER_GLOVES, rh=SHOP_ROD, lh=LH_EMPTY)

    # Monster records: level/Br-Fa only. Preserve equipment-zero shape and every innate monster field.
    set_slot(data, E, 4, level=101, brave=90, faith=55)
    set_slot(data, E, 5, level=100, brave=88, faith=55)
    return [E]


def limberry_gate(data):
    # Battle 42 - Limberry Castle Gate: the assassin flee-race, opening the no-resupply Limberry chain
    #   (42 -> 43 -> 44, one loadout). Entry 454 = Celia (job 45) + Lettie (job 46) + 4 Reavers.
    # WIN SHAPE: fight ends when ONE assassin hits CRITICAL -> they FLEE. Flee => NO drop (no rare here;
    #   the Masamune/Genji reckoning is Elmdor's, at the Keep 048). Same assassins as Roof (433).
    # v3 keeps the v2 flee race but gives the dual-wield Assassins explicit legal weapons: Celia's job
    # equips Katana; Lettie's equips Ninja Blades. Their fixed head/body/accessory and all scripting stay
    # untouched. Low-band rule: Assassins 102, Reavers 101/101/100/100.
    E = 454
    set_slot(data, E, 0, level=102, brave=92, faith=90, rh=MASAMUNE, lh=MASAMUNE)
    set_slot(data, E, 1, level=102, brave=92, faith=90, rh=KOGA_BLADE, lh=IGA_BLADE)
    for s, lvl in ((2, 101), (3, 101), (4, 100), (5, 100)):
        set_slot(data, E, s, level=lvl, brave=88, faith=76)
    return [E]


def limberry_keep(data):
    # Battle 43 - Limberry Castle Keep: the Elmdor reckoning (Limberry chain 2/3, no resupply).
    #   WIN = "Defeat Elmdore" (his death ends it). Entry 456 (455 is an all-placeholder event formation):
    #     slot0 = Elmdor (job 27 Ark Knight, name 0x1b)  eq=(155,183,216,46,140)
    #             -> ALREADY wears MASAMUNE (rh=46) + GENJI ARMOR (body=183): the deferred Tier-A loot is
    #                present in vanilla. Shirahadori parry + Vampire drain + Draw Out live in his unit/AI.
    #     slot1 = Celia  (job 45 Assassin, eq=254 fixed)   slot2 = Lettie (job 46 Assassin, eq=254)
    #     slots 3,4 = job 154, name-linked to Celia/Lettie -> their ULTIMA-DEMON transform forms (eq=0).
    # v3 keeps the parry race and transform timer. Elmdor uses Chirijiraden + Genji Shield; Celia/Lettie
    # repeat their Gate weapons and add Featherweave Cloaks. All other fixed/scripted fields stay intact.
    # Low-band rule: Elmdor 102; Assassins 101; their Ultima-Demon forms 100.
    E = 456
    set_slot(data, E, 0, level=102, brave=90, faith=65, rh=CHIRIJIRADEN, lh=GENJI_SHIELD)
    set_slot(data, E, 1, level=101, brave=90, faith=60, acc=FEATHERWEAVE,
             rh=MASAMUNE, lh=MASAMUNE)
    set_slot(data, E, 2, level=101, brave=90, faith=60, acc=FEATHERWEAVE,
             rh=KOGA_BLADE, lh=IGA_BLADE)
    set_slot(data, E, 3, level=100, brave=88, faith=76)  # Celia -> Ultima Demon
    set_slot(data, E, 4, level=100, brave=88, faith=76)  # Lettie -> Ultima Demon
    return [E]


def limberry_undercroft(data):
    # Battle 44 - Limberry Castle Undercroft v3: status-Lucavi capstone (chain 3/3, no resupply).
    # WIN = "Defeat Zalera". Keep the six active slots and recast the guard in place:
    #   s1 Zalera; s2/s3 Archaeodaemon; s4 Undead Mystic; s5/s6 Undead Knight.
    # Slots 0 (Elmdor event placeholder), 7 (Meliadoul join record), and inactive raw records 8/9 stay
    # byte-identical. This is a same-count ENTD job-swap: control flags, positions, UnitIDs, and spoils
    # remain attached to the target slots. In particular, s2 keeps the Zeus Mace reward payload.
    E = 457

    # Reset only the editable identity/build prefix from the vanilla target slots before authoring v3.
    # This prevents stale fields from an older design or a previous partial run while preserving every
    # target tail byte, including positions, control flags, UnitIDs, and reward payloads.
    vanilla = VANILLA.read_bytes()
    for s in (2, 3, 4, 5, 6):
        b = (E % 128) * ENTRY + s * SLOT
        data[b:b + 0x17] = vanilla[b:b + 0x17]

    # Set the identity header explicitly so the patch remains idempotent after s2/s3 stop being Knights.
    # Tail bytes 0x17-0x27 remain untouched: palette/control/position/spoils/UnitID/script context stay
    # attached to the original target slot.
    def set_identity(slot, char_id, flags, name=255):
        b = (E % 128) * ENTRY + slot * SLOT
        data[b + 0x00] = char_id
        data[b + 0x01] = flags
        data[b + 0x02] = name

    set_slot(data, E, 1, level=102, brave=92, faith=86)  # Zalera; preserve status kit and eq=255.

    for s in (2, 3):
        set_identity(s, 130, 0x20)
        set_slot(data, E, s, level=100, jobrank=0, joblevel=8, job=153,
                 secondary=0, brave=88, faith=76,
                 reaction=510, support=510, movement=510,
                 head=0, body=0, acc=0, rh=0, lh=0)

    set_identity(4, 70, 0x80)
    set_slot(data, E, 4, level=101, jobrank=generic_job_rank(MIME), joblevel=8, job=70,
             secondary=GEOMANCY, brave=72, faith=84,
             reaction=MANA_SHIELD, support=MAGICK_BOOST, movement=MV2,
             head=MAGE_HAT, body=BLACK_ROBE, acc=MAGEPOWER_GLOVES, rh=SHOP_ROD, lh=LH_EMPTY)

    for s in (5, 6):
        set_identity(s, 61, 0x20)
        set_slot(data, E, s, level=101, jobrank=generic_job_rank(MONK), joblevel=8, job=61,
                 secondary=MARTIAL_ARTS, brave=88, faith=40,
                 reaction=COUNTER, support=DUAL_WIELD, movement=MV3,
                 head=HEAVY_HELM, body=HEAVY_ARMOR, acc=BRACERS,
                 rh=RUNEBLADE, lh=RUNEBLADE)
    return [E]


def eagrose(data):
    # Battle 45 - Eagrose Castle: the brother fight, two-phase Dycedarg -> Adramelk (Lucavi). Entry 459.
    #   IDENTIFICATION: only entry in the band with 5 generic Knights (job 76) = the stair-wall. slot7
    #     job 69 is a LUCAVI: entry 470 (multi-Lucavi) shows job69 with name_id==job_id like Velius(60)/
    #     Zalera(62) -> job 69 = Adramelk. So:
    #     slot 0 = GUEST (tail 00 84), name 8, job 8, real gear -> story ally. SPRITE-COLLISION: charId 8
    #              also appears as enemy/placeholder clones at slots 8,9 (job8==charId8), so the runtime
    #              GuestCharIds scaler can't be used (it can't tell ally from clone; Rapha-Roof precedent
    #              433). Scaled by DIRECT ENTD level (103) instead; gear + guest tail preserved.
    #     slot 1 = Dycedarg (name 9, job 9; eq incl. Aegis Shield lh=136, Defender rh=33) -> Phase-1 boss.
    #              Carries the Tier-A GRAND HELM (head=156) as the steal/poach reward (he has equip slots).
    #     slots 2-6 = 5 Knights (job 76) -> the upper-stair wall; armed (were near-naked) + scaled.
    #     slot 7 = Adramelk (name 69, job 69, eq=255 Lucavi no-equip) -> Phase-2 transform spike; lvl only.
    #     slots 8,9 = job 8, eq=0, lvl254 -> scripting placeholders; left untouched.
    # V3 keeps all five bodies as main-job Knights, so Arts of War remains primary for all of them.
    # JobUnlock seeds the requested secondary-job bucket (Monk/Samurai/Ninja); it does not replace the
    # Knight main job or its primary command. event436.e keeps the existing registration/choreography.
    E = 459
    set_slot(data, E, 0, level=103, brave=70, faith=65,
             head=GRAND_HELM, body=MAXIMILLIAN, acc=BRACERS,
             rh=CHAOS_BLADE, lh=VENETIAN_SHIELD)  # Zalbaag guest ally - direct-level scale
    set_player_control(data, E, 0)
    set_slot(data, E, 1, level=103, brave=88, faith=60,
             head=GRAND_HELM, body=ROBE_OF_LORDS, acc=BRACERS,
             rh=CHAOS_BLADE, lh=VENETIAN_SHIELD)  # Dycedarg; preserve existing abilities/transform

    set_slot(data, E, 2, level=100, jobrank=generic_job_rank(MONK), joblevel=8,
             job=KNIGHT, secondary=MARTIAL_ARTS, brave=88, faith=42,
             reaction=COUNTER, support=ATK_BOOST, movement=MV3,
             head=HEAVY_HELM, body=HEAVY_ARMOR, acc=BRACERS,
             rh=RUNEBLADE, lh=CRYSTAL_SHIELD)
    set_slot(data, E, 3, level=100, jobrank=generic_job_rank(MONK), joblevel=8,
             job=KNIGHT, secondary=MARTIAL_ARTS, brave=86, faith=44,
             reaction=COUNTER, support=ATK_BOOST, movement=MV3,
             head=HEAVY_HELM, body=HEAVY_ARMOR, acc=BRACERS,
             rh=RUNEBLADE, lh=CRYSTAL_SHIELD)

    set_slot(data, E, 4, level=101, jobrank=generic_job_rank(SAMURAI), joblevel=8,
             job=KNIGHT, secondary=IAIDO, brave=88, faith=58,
             reaction=SHIRAHADORI, support=DOUBLEHAND, movement=MV3,
             head=HEAVY_HELM, body=HEAVY_ARMOR, acc=MAGEPOWER_GLOVES,
             rh=RUNEBLADE, lh=LH_EMPTY)

    set_slot(data, E, 5, level=101, jobrank=generic_job_rank(NINJA), joblevel=8,
             job=KNIGHT, secondary=THROW, brave=88, faith=52,
             reaction=REFLEXES, support=DUAL_WIELD, movement=IGNORE_HEIGHT,
             head=HEAVY_HELM, body=HEAVY_ARMOR, acc=HERMES_SHOES,
             rh=RUNEBLADE, lh=RUNEBLADE)
    set_slot(data, E, 6, level=100, jobrank=generic_job_rank(NINJA), joblevel=8,
             job=KNIGHT, secondary=THROW, brave=86, faith=56,
             reaction=REFLEXES, support=DUAL_WIELD, movement=IGNORE_HEIGHT,
             head=HEAVY_HELM, body=HEAVY_ARMOR, acc=HERMES_SHOES,
             rh=RUNEBLADE, lh=RUNEBLADE)
    set_slot(data, E, 7, level=105, brave=92, faith=86)  # Adramelk (Lucavi, Phase 2)
    return [E]


def mullonde_exterior(data):
    # Battle 46 - Mullonde Cathedral Exterior: the hidden-healer caster screen, opening the Mullonde
    #   chain (46->47->48, no resupply). Entry 460 (exact roster match, all generic casters spr128):
    #     slot 0 = White Mage (job 79, rh=64 staff) -> the HIDDEN rooftop heal+Raise-multi sustain engine.
    #     slot 1 = Summoner (job 82, rh=57 Dragon Rod) -> AoE; Dragon Rod remains steal flavor (KEEP rh).
    #     slots 2,3 = Geomancer (job 86; were naked) -> terrain elemental.
    #     slots 4,5 = Orator (job 84, rh=72 gun) -> soft status (one-disruptor cap).
    # CHANGE (v2): complete the caster kits while keeping this lighter than the Nave/Sanctuary bosses.
    #   Items is the safe secondary across the team: useful chain pressure, no Stop/Charm hard-lock.
    #   Staff of the Magi + Faerie Harp rewards are handled through spoils, not Steal requirements.
    E = 460
    set_slot(data, E, 0, level=103, joblevel=8, job=WMAGE,       # hidden rooftop sustain - priority kill
             secondary=ITEMS, brave=60, faith=84,
             reaction=REFLEXES, support=MAGICK_BOOST, movement=MV1,
             head=MAGE_HAT, body=SHOP_ROBE, acc=FEATHERWEAVE)    # keep rh=64 staff
    set_slot(data, E, 1, level=102, joblevel=8, job=SUMMONER,    # AoE; KEEP rh=57 Dragon Rod (steal)
             secondary=ITEMS, brave=60, faith=84,
             reaction=REFLEXES, support=MAGICK_BOOST, movement=MV1,
             head=MAGE_HAT, body=SHOP_ROBE, acc=FEATHERWEAVE)
    for s in (2, 3):                                              # 2 Geomancer - terrain (were naked)
        set_slot(data, E, s, level=102, joblevel=8, job=GEOMANCER, secondary=ITEMS,
                 brave=68, faith=78,
                 reaction=COUNTER, support=ATK_BOOST, movement=MV1,
                 head=MAGE_HAT, body=SHOP_ROBE, acc=FEATHERWEAVE, rh=SHOP_ROD)
    for s in (4, 5):                                              # 2 Orator - soft status (one-disruptor)
        set_slot(data, E, s, level=102, joblevel=8, job=ORATOR, secondary=ITEMS,
                 brave=68, faith=78,
                 reaction=REFLEXES, support=DEFENSE_BOOST, movement=MV1,
                 head=MAGE_HAT, body=SHOP_ROBE, acc=FEATHERWEAVE)  # keep rh=72 gun
    return [E]


def mullonde_nave(data):
    # Battle 47 - Mullonde Cathedral Nave: the triple-Templar boss rush (Mullonde chain 2/3, no resupply).
    #   *** TIER-S UNLOCK BEGINS HERE *** WIN = "Defeat Folmarv" (fight ends when ANY one drops to
    #   critical; the other two RETREAT -> flee = no drop). Entry 461 (story order 459->460->461, three
    #   named bosses, NO generics):
    #     slot 0 = Folmarv  (name 36, job 36 Divine-Knight-class; eq incl. rh=30 Runeblade) -> the named
    #              kill target + Tier-S carrier. rh set to CHAOS BLADE (37): a KnightSword, so it both
    #              powers his Divine Sword / Unyielding-Blade break AND is the steal/drop reward.
    #     slot 1 = Loffrey  (name 37, job 37 Divine-Knight-class; rh=29 Icebrand) -> 2nd equip-breaker.
    #              RETREATS, but the reward ledger pays Escutcheon here through guaranteed spoils.
    #     slot 2 = Cletienne (name 39, job 39 Sorcerer; rh=57 rod) -> caster, denies turtling. RETREATS
    #              but the reward ledger pays Lordly Robe here through guaranteed spoils. Gear kept.
    #     slot 3 = job 39 clone (name255, lvl65, eq=0) -> scripting/summon placeholder; left untouched.
    # CHANGE: scale to the human-boss band + jl8 (full kit incl. the equip-break). Folmarv 105 (leader),
    #   Loffrey & Cletienne 104. Win-on-one-falls, equip-break (Folmarv+Loffrey only), and caster pressure
    #   all preserved. Br/Fa tunes two physical break bosses and one high-Faith caster.
    E = 461
    set_slot(data, E, 0, level=105, joblevel=8, brave=90, faith=55,
             rh=CHAOS_BLADE)                                    # Folmarv - Tier-S Chaos Blade (KnightSword)
    set_slot(data, E, 1, level=104, joblevel=8, brave=90, faith=55)  # Loffrey - second break source
    set_slot(data, E, 2, level=104, joblevel=8, brave=65, faith=88)  # Cletienne - caster pressure
    return [E]


def mullonde_sanctuary(data):
    # Battle 48 - Mullonde Cathedral Sanctuary: the tragic undead-brother climax (Mullonde chain 3/3,
    #   no resupply). WIN = "Defeat Zalbaag" (demons optional). Entry 462 (story order 459->...->462):
    #     slot 0 = Folmarv (name 36, eq255, lvl254) -> INACTIVE cutscene placeholder; left untouched.
    #     slot 1 = Zalbaag (name 51, job 51 Ark-Knight-class; jl8; eq head154/body182/acc210/rh30 Runeblade/
    #              lh139 shield) -> the ACTIVE vampire boss + Tier-S carrier. Real equip slots.
    #     slots 2,3 = Archaeodaemon (job 153, undead) -> the reraise/HP-drain screen.
    #     slot 4 = Ultima Demon (job 154) -> telegraphed Ultima pressure (optional target).
    #     slot 5 = job 51 clone (name255, eq255, lvl254) -> scripting placeholder; left untouched.
    # CHANGE: scale + Tier-S reward. Zalbaag 105, acc set to RIBBON (171) for status-warding identity.
    #   Ragnarok remains reward payload only; keep his Runeblade (the equip-break weapon) + vampirism/
    #   undead flags + scripting. Archaeodaemons & Ultima Demon 103.
    E = 462
    set_slot(data, E, 1, level=105, brave=90, faith=78,
             acc=RIBBON)  # Zalbaag - keep Runeblade + vampire kit; Ragnarok is spoil-only
    for s in (2, 3, 4):                           # 2 Archaeodaemon (undead) + 1 Ultima Demon
        set_slot(data, E, s, level=103, brave=88, faith=76)
    return [E]


# ---------------------------------------------------------------------------
# ENDGAME GAUNTLET (battles 49-53) — entries confirmed IN-GAME 2026-06-21 by
# matching the on-screen roster to a vanilla entd4 dump (the [battle-id] save
# read LAGS — do not trust it; see docs/battles/ENDGAME-BLOCKER.md). All six
# gauntlet records are direct entd4 entries; Vaults 4th is entry 435, not a
# template battle.
# No usable reward is placed inside this five-battle gauntlet. Tier-S gear is paid by the
# Mullonde chain before the point of no return; these entries are challenge content only.
# ---------------------------------------------------------------------------
def vaults_4th(data):
    # Battle 49 - Monastery Vaults, Fourth Level (entry 435): the gauntlet OPENER. CONFIRMED in-game =
    #   Loffrey only ENTERS in a cutscene and walks out the door (a scripted NPC exit, NOT a fightable
    #   boss here — his real fight is the Fifth Level, 436). The actual enemies are slots 1-6 = 3 Knight/
    #   2 Monk/1 Archer in vanilla. v2 keeps the all-generic opener but swaps the Archer to a tempered
    #   Ninja. No boss, no rare, no usable gauntlet reward. slot0 Loffrey is cutscene-only.
    E = 435
    set_slot(data, E, 0, brave=90, faith=55)  # Loffrey cutscene unit; preserve level/gear/event behavior.
    for s in (1, 2):                                             # 2 Knight - capped Rend sources
        set_slot(data, E, s, level=103, joblevel=8, job=KNIGHT, secondary=ITEMS,
                 brave=88, faith=42,
                 reaction=COUNTER, support=ATK_BOOST, movement=MV1,
                 head=HEAVY_HELM, body=HEAVY_ARMOR, acc=BRACERS, rh=RUNEBLADE, lh=SHOP_SHIELD)
    set_slot(data, E, 3, level=102, joblevel=1, job=KNIGHT, secondary=ITEMS,
             brave=88, faith=42,
             reaction=COUNTER, support=DEFENSE_BOOST, movement=MV1,
             head=HEAVY_HELM, body=HEAVY_ARMOR, acc=BRACERS, rh=RUNEBLADE, lh=SHOP_SHIELD)
    for s in (4, 5):                                             # 2 Monk - Chakra sustain
        set_slot(data, E, s, level=102, joblevel=8, job=MONK, secondary=FUNDAMENTS,
                 brave=88, faith=40,
                 reaction=COUNTER, support=ATK_BOOST, movement=MV1,
                 head=HEADBAND, body=POWER_GARB, acc=BRACERS)
    set_slot(data, E, 6, level=103, joblevel=8, job=NINJA, secondary=STEAL,  # tempered tempo flanker
             brave=90, faith=35,
             reaction=REFLEXES, support=ATK_BOOST, movement=MV2,
             head=THIEFS_CAP, body=BLACK_GARB, acc=BRACERS, rh=NINJA_BLADE, lh=NINJA_BLADE)
    return [E]


def vaults_5th(data):
    # Battle 50 - Monastery Vaults, Fifth Level (entry 436): Loffrey's death battle.
    # Roster matches doc 055: Loffrey + 2 Black Mage + 2 Summoner + 1 Time Mage. The final
    # gauntlet has no usable rewards, so Loffrey uses standard gear instead of duplicate uniques.
    E = 436
    set_slot(data, E, 0, level=105, joblevel=8, brave=90, faith=55,
             rh=RUNEBLADE, lh=SHOP_SHIELD, movement=MV2)  # Loffrey - one break boss, no gauntlet rare
    for s in (1, 2):                                             # 2 Black Mage - heavy AoE magic
        set_slot(data, E, s, level=103, joblevel=8, job=BMAGE, secondary=ITEMS,
                 brave=60, faith=84,
                 reaction=REFLEXES, support=MAGICK_BOOST, movement=MV1,
                 head=MAGE_HAT, body=SHOP_ROBE, acc=FEATHERWEAVE, rh=SHOP_ROD, lh=LH_EMPTY)
    for s in (3, 4):                                             # 2 Summoner - AoE summon damage
        set_slot(data, E, s, level=103, joblevel=8, job=SUMMONER, secondary=ITEMS,
                 brave=60, faith=84,
                 reaction=REFLEXES, support=MAGICK_BOOST, movement=MV1,
                 head=MAGE_HAT, body=SHOP_ROBE, acc=FEATHERWEAVE, rh=SHOP_ROD, lh=LH_EMPTY)
    set_slot(data, E, 5, level=103, joblevel=4, job=TMAGE, secondary=ITEMS,  # Haste/Slow/Float, no Stop
             brave=62, faith=80,
             reaction=REFLEXES, support=MAGICK_BOOST, movement=MV1,
             head=MAGE_HAT, body=SHOP_ROBE, acc=FEATHERWEAVE, rh=SHOP_ROD, lh=LH_EMPTY)
    return [E]


def capitoline(data):
    # Battle 51 - Necrohol of Mullonde / The Capitoline (entry 438): Cletienne's death battle.
    # Win = "Defeat Cletienne". Roster is Cletienne + 2 Time Mage + 2 Ninja + 2 Samurai.
    # Keep the Magick Surge race, fill the elite screen's kits, and add no gauntlet reward.
    E = 438
    set_slot(data, E, 0, level=105, joblevel=8, secondary=FUNDAMENTS,
             brave=65, faith=88, body=BLACK_GARB)  # Cletienne - Silence/burst remains the answer.
    for s in (1, 2):                                                  # 2 Time Mage - Slow/Haste tempo
        set_slot(data, E, s, level=104, joblevel=8, job=TMAGE, secondary=ITEMS,
                 brave=62, faith=80,
                 reaction=REFLEXES, support=MAGICK_BOOST, movement=MV1,
                 head=MAGE_HAT, body=SHOP_ROBE, acc=FEATHERWEAVE, rh=SHOP_ROD, lh=LH_EMPTY)
    for s in (3, 4):                                                  # 2 Ninja - dual-wield flankers
        set_slot(data, E, s, level=104, joblevel=8, job=NINJA, secondary=ITEMS,
                 brave=90, faith=35,
                 reaction=FIRST_STRIKE, support=ATK_BOOST, movement=MV2,
                 head=THIEFS_CAP, body=BLACK_GARB, acc=GERMINAS, rh=NINJA_BLADE, lh=NINJA_BLADE)
    for s in (5, 6):                                                  # 2 Samurai - Draw Out (katana auto)
        set_slot(data, E, s, level=104, joblevel=8, job=SAMURAI, secondary=ITEMS,
                 brave=88, faith=60,
                 reaction=COUNTER, support=ATK_BOOST, movement=MV1,
                 head=HEAVY_HELM, body=HEAVY_ARMOR, acc=BRACERS,
                 rh=KIKU_ICHIMONJI, lh=LH_TWOHAND)
    return [E]


def lost_halidom(data):
    # Battle 52 - Necrohol of Mullonde / Lost Halidom (entry 439): Barich rematch.
    # Win = "Defeat Barich". Roster is Barich + Chemist + 4 apex monsters. This is the
    # gauntlet 4/5 peak: one answerable control boss, raceable sustain, no usable reward.
    E = 439
    set_slot(data, E, 0, level=105, joblevel=8, secondary=ITEMS,
             brave=84, faith=55, rh=MYTHRIL_GUN, lh=LH_TWOHAND)  # Barich - no 042 gun duplicate.
    set_slot(data, E, 1, level=104, joblevel=8, job=CHEMIST, secondary=FUNDAMENTS,
             brave=72, faith=68,
             reaction=AUTO_POTION, support=DEFENSE_BOOST, movement=MV1,
             head=THIEFS_CAP, body=BLACK_GARB, acc=FEATHERWEAVE, rh=MYTHRIL_GUN, lh=LH_TWOHAND)
    for s in (2, 3, 4, 5):                                      # 4 dragons - apex beasts, scale only
        set_slot(data, E, s, level=105, joblevel=8, brave=90, faith=30)
    return [E]


def airship_hashmal(data):
    # Battle 53 / PHASE 1 - Airship Graveyard, Hashmal (entry 440).
    # Preserve the scripted Hashmal transition and full restore; tune levels/Br-Fa only, except
    # removing Save the Queen from slot0 so no unique payload leaks inside the final gauntlet.
    E = 440
    set_slot(data, E, 0, level=105, joblevel=8, brave=92, faith=86,
             rh=RUNEBLADE, lh=SHOP_SHIELD)  # Folmarv/Hashmal host; preserve transform script tail.
    set_slot(data, E, 1, level=105, joblevel=8, brave=88, faith=76)
    set_slot(data, E, 2, level=105, brave=92, faith=86)              # Lucavi (job64, eq255)
    for s in (3, 4, 5):                          # transform/clone forms (eq255)
        set_slot(data, E, s, level=104, brave=88, faith=76)
    return [E]


def airship_ultima(data):
    # Battle 53 / PHASE 2 - Airship Graveyard, Ultima (entry 441).
    # Ultima is the single level-106 capstone. Lucavi/form records and Ultima Demons stay capped at
    # 105 so the finale reads as adaptation, not raw support overleveling. No reward payload.
    E = 441
    set_slot(data, E, 0, level=105, brave=92, faith=86)              # Lucavi (job49, eq255)
    set_slot(data, E, 1, level=105, brave=92, faith=86)              # Lucavi (job49, eq255)
    set_slot(data, E, 2, level=106, joblevel=8, brave=92, faith=90)  # Ultima final boss
    for s in (3, 4, 5, 6):                       # 4 Ultima Demons (job154)
        set_slot(data, E, s, level=105, brave=88, faith=76)
    set_slot(data, E, 7, level=105, brave=92, faith=86)              # Lucavi (job65, eq255)
    set_slot(data, E, 8, level=105, brave=92, faith=86)              # Lucavi (job73, eq255)
    return [E]


def vaults_3rd_v2(data):
    touched = vaults_3rd(data)
    E = 423
    set_slot(data, E, 0, brave=86, faith=55, support=ATK_BOOST, rh=RUNEBLADE)
    set_slot(data, E, 1, secondary=GEOMANCY, brave=86, faith=55, reaction=FIRST_STRIKE, movement=MV2)
    set_slot(data, E, 2, secondary=GEOMANCY, brave=84, faith=45, reaction=FIRST_STRIKE, movement=MV2)
    set_slot(data, E, 3, secondary=ITEMS, brave=58, faith=78, support=SWIFTSPELL, movement=TELEPORT)
    for s in (4, 5):
        set_slot(data, E, s, secondary=ARTS_OF_WAR, brave=80, faith=45, movement=JUMP2)
    return touched


def vaults_1st_v2(data):
    touched = vaults_1st(data)
    E = 424
    set_slot(data, E, 0, secondary=FUNDAMENTS, brave=88, faith=60,
             reaction=PARRY, support=ATK_BOOST, movement=MV2, rh=DEFENDER)
    set_slot(data, E, 1, secondary=ITEMS, brave=84, faith=45)
    set_slot(data, E, 2, secondary=FUNDAMENTS, brave=84, faith=45)
    set_slot(data, E, 4, secondary=ITEMS, brave=58, faith=78,
             support=MAGICK_BOOST, movement=TELEPORT)
    for s in (3, 5):
        set_slot(data, E, s, brave=80, faith=45, movement=MV2)
    return touched


def grogh_v2(data):
    touched = grogh(data)
    E = 426
    set_slot(data, E, 0, secondary=GEOMANCY, brave=70, faith=50,
             reaction=FIRST_STRIKE, movement=MV2)
    for s in (1, 3):
        set_slot(data, E, s, secondary=FUNDAMENTS, brave=68, faith=64)
    set_slot(data, E, 2, secondary=ITEMS, brave=58, faith=78,
             reaction=MANA_SHIELD, support=SWIFTSPELL, movement=MOVE_MP_UP)
    set_slot(data, E, 4, brave=80, faith=45)
    set_slot(data, E, 5, secondary=ITEMS, brave=84, faith=42)
    return touched


def yardrow_v2(data):
    touched = yardrow(data)
    E = 428
    set_slot(data, E, 0, level=100, jobrank=generic_job_rank(WMAGE), joblevel=8,
             secondary=WHITE_MAGICKS, brave=65, faith=75,
             reaction=MANA_SHIELD, support=DEFENSE_BOOST, movement=MOVE_MP_UP)
    set_player_control(data, E, 0)
    set_slot(data, E, 1, joblevel=8, secondary=ITEMS, brave=78, faith=72,
             reaction=REFLEXES, support=MAGICK_BOOST, movement=MV2,
             acc=MAGEPOWER_GLOVES)
    # s2 is the lead/far-edge Ninja: keep the special Ninja Blade pair here only.
    set_slot(data, E, 2, secondary=ITEMS, brave=86, faith=40,
             reaction=REFLEXES, movement=JUMP2)
    for s in (4, 6):
        set_slot(data, E, s, secondary=ITEMS, brave=90, faith=60,
                 reaction=REFLEXES, movement=JUMP2,
                 acc=BRACERS, rh=AIR_KNIFE, lh=LH_EMPTY)
    for s in (3, 5):
        set_slot(data, E, s, secondary=WHITE_MAGICKS, brave=58, faith=78,
                 reaction=SOULBIND, support=SWIFTSPELL, movement=TELEPORT)
    return touched


def yuguewood_v2(data):
    touched = yuguewood(data)
    E = 430
    for s, lvl in ((1, 101), (3, 100)):
        set_slot(data, E, s, level=lvl, jobrank=0, joblevel=8, job=ENEMY_BMAGE,
                 secondary=WHITE_MAGICKS, brave=58, faith=78,
                 reaction=REFLEXES, support=SWIFTSPELL, movement=MV2,
                 head=MAGE_HAT, body=SHOP_ROBE, acc=MAGEPOWER_GLOVES, rh=SHOP_ROD, lh=LH_EMPTY)
    for s in (2, 4):
        set_slot(data, E, s, level=101, jobrank=0, joblevel=8, job=ENEMY_TMAGE,
                 secondary=MYSTIC_ARTS, brave=60, faith=74,
                 reaction=REFLEXES, support=MAGICK_BOOST, movement=MV2,
                 head=MAGE_HAT, body=SHOP_ROBE, acc=FEATHERWEAVE, rh=SHOP_STAFF, lh=LH_EMPTY)
    for s, lvl in ((5, 100), (6, 100), (7, 101)):
        set_slot(data, E, s, level=lvl, joblevel=8, brave=86, faith=35)
    return touched


def riovanes_gate_v2(data):
    touched = riovanes_gate(data)
    E = 431
    # Marach survives and is intentionally excluded from the runtime generic-stat pass.
    set_slot(data, E, 1, joblevel=8, secondary=ITEMS, brave=78, faith=72,
             reaction=REFLEXES, support=MAGICK_BOOST, movement=MV2,
             acc=MAGEPOWER_GLOVES)
    # Crossbow Knight replaces the bugged special Templar job without adding another sprite sheet.
    set_slot(data, E, 5, job=KNIGHT, secondary=GEOMANCY, brave=84, faith=45,
             reaction=DRAGONHEART, support=ATK_BOOST, movement=MV2,
             head=HEAVY_HELM, body=HEAVY_ARMOR, acc=BRACERS, rh=GASTROPHETES, lh=SHOP_SHIELD)
    # Samurai elite: physical parry puzzle and katana pressure without a secondary skillset.
    set_slot(data, E, 6, job=SAMURAI, secondary=0, brave=84, faith=45,
             reaction=SHIRAHADORI, support=DOUBLEHAND, movement=MV2,
             head=HEAVY_HELM, body=MIRROR_MAIL, acc=BRACERS, rh=KIKU_ICHIMONJI, lh=LH_TWOHAND)
    # s7 is the vanilla Winged Boots Knight. Restore that mobility identity with crossbow pressure.
    set_slot(data, E, 7, secondary=ITEMS, brave=84, faith=45,
             reaction=DRAGONHEART, support=ATK_BOOST, movement=MV2,
             head=HEAVY_HELM, body=HEAVY_ARMOR, acc=WINGED_BOOTS, rh=GASTROPHETES, lh=SHOP_SHIELD)
    set_slot(data, E, 8, secondary=ITEMS, brave=84, faith=45)
    for s in (2, 3, 4):
        set_slot(data, E, s, brave=80, faith=45)
    return touched


BATTLES = {
    "chapter1_guest_control": chapter1_guest_control,
    "gariland": gariland,
    "sweegy": sweegy,
    "mandalia": mandalia,
    "dorter": dorter,
    "sand_rat": sand_rat,
    "brigands": brigands,
    "lenalian": lenalian,
    "fovoham": fovoham,
    "ziekden": ziekden,
    "merchant_dorter": merchant_dorter,
    "araguay": araguay,
    "zeirchele": zeirchele,
    "zaland": zaland,
    "balias_tor": balias_tor,
    "tchigolith": tchigolith,
    "goug": goug,
    "balias_swale": balias_swale,
    "golgollada": golgollada,
    "lionel_gate": lionel_gate,
    "cuchulainn": cuchulainn,
    "gollund": gollund,
    "lesalia": lesalia,
    "vaults_2nd": vaults_2nd,
    "vaults_3rd": vaults_3rd_v2,
    "vaults_1st": vaults_1st_v2,
    "grogh": grogh_v2,
    "yardrow": yardrow_v2,
    "yuguewood": yuguewood_v2,
    "riovanes_gate": riovanes_gate_v2,
    "riovanes_keep": riovanes_keep,
    "riovanes_roof": riovanes_roof,
    "dugeura": dugeura,
    "bervenia": bervenia,
    "finath": finath,
    "outlying_church": outlying_church,
    "bed_desert": bed_desert,
    "besselat_wall": besselat_wall,
    "besselat_sluice": besselat_sluice,
    "germinas": germinas,
    "poeskas": poeskas,
    "limberry_gate": limberry_gate,
    "limberry_keep": limberry_keep,
    "limberry_undercroft": limberry_undercroft,
    "eagrose": eagrose,
    "mullonde_exterior": mullonde_exterior,
    "mullonde_nave": mullonde_nave,
    "mullonde_sanctuary": mullonde_sanctuary,
    "vaults_4th": vaults_4th,
    "vaults_5th": vaults_5th,
    "capitoline": capitoline,
    "lost_halidom": lost_halidom,
    "airship_hashmal": airship_hashmal,
    "airship_ultima": airship_ultima,
}


def main(argv):
    names = argv or ["all"]
    if names == ["all"]:
        names = list(BATTLES)
    data = bytearray(EMBED.read_bytes())
    before = bytes(data)
    touched = []
    for name in names:
        if name not in BATTLES:
            print(f"unknown battle '{name}'; known: {', '.join(BATTLES)}")
            return 2
        touched += BATTLES[name](data)
    EMBED.write_bytes(data)

    # Report: which entries changed (must only be the intended ones).
    # The file holds local entries 0..127 (global = 384 + local for entd4).
    changed_local = sorted({i // ENTRY for i in range(len(data)) if data[i] != before[i]})
    expected_local = sorted({g % 128 for g in touched})
    nchanged = sum(1 for i in range(len(data)) if data[i] != before[i])
    print(f"applied: {', '.join(names)}")
    print(f"bytes changed this run: {nchanged}")
    print(f"local entries changed: {changed_local} (expected: {expected_local}; global: {sorted(set(touched))})")
    ok = set(changed_local) <= set(expected_local)
    print("OK — diff contained to intended entries" if ok else "WARNING — diff leaked outside intended entries!")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
