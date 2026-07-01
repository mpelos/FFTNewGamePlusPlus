# Chapter 2 V2 Implementation Validation

Date: 2026-07-01

This file records the objective implementation evidence for the Chapter 2 v2 redesign pass. It is a
technical status document, not a design proposal. The source of truth for reproducing the binary
patch is `tools/battle_patch.py`; the patched embedded ENTD is
`src/fftivc.battles.ngplus/entd/battle_entd4_ent.bin`.

## Implemented Entries

| Doc | Entry | Patcher target | Implementation layer | Key validation evidence |
|---|---:|---|---|---|
| `012` Merchant City of Dorter | `403` | `merchant` | ENTD retune + event-spawned slot-add | Knight captain slot `s9` UnitID `0x86`; `event119.e` contains `45 86 00 01` registration and `5f 86 00` choreography block. |
| `013` Araguay Woods | `404` | `araguay` | ENTD direct scale + plain static slot-add | Boco level/control; roster jobs `98,98,99,99,98,98,104`; Coeurl slot `s9` UnitID `0x87`. |
| `014` Zeirchele Falls | `405` | `zeirchele` | ENTD retune + NXD row for true static slot-add | White Mage slot `s11` UnitID `0x87`; intro corpses `s2/s3` untouched; `OverrideEntryData` row count `518` with `405/11`; enemy levels applied; Ovelia survival gear/Faith applied. |
| `015` Castled City of Zaland | `407` | `zaland` | ENTD retune + plain static slot-add | Second Dragoon slot `s8` UnitID `0x86`; Dragoon/Black Mage/Archer levels and job-rank seeds applied. |
| `016` Balias Tor | `409` | `balias_tor` | ENTD retune + plain static slot-add | Chemist slot `s8` UnitID `0x86`; Summoner/Knight/Archer levels and support kits applied. |
| `017` Tchigolith Fenlands | `410` | `tchigolith` | ENTD monster retune + plain static slot-add | Second Bonesnatch slot `s9` UnitID `0x86`; monster jobs and levels applied. |
| `018` Goug Lowtown | `411` | `goug` | ENTD retune + runtime guest scaler/control | Summoner/Time Mage/Archer/Thief roster applied; Time Mage JobLevel capped to `4`; `cid 0x16` guest covered by `GuestCharIds`. |
| `019` Balias Swale | `413` | `balias_swale` | ENTD retune + plain static slot-add + runtime guest scaler/control | Geomancer slot `s7` UnitID `0x86`; Agrias Brave/Faith support applied; human job-rank seeds applied. |
| `020` Golgollada Gallows | `414` | `golgollada` | ENTD retune | Gaffgarion level `103`; Knights/Archers/Time Mages tuned; Time Mages capped to JobLevel `4`. |
| `021` Lionel Castle Gate | `415` | `lionel_gate` | ENTD retune + boss rare equipment | Gaffgarion level `103`; Blood Sword equipped; no Time Mage/second Summoner added. |
| `022` Lionel Castle Oratory | `425` | `cuchulainn` | ENTD boss retune + Spoils of War byte | Cuchulainn level `104`; JobLevel `8`; Brave/Faith `88/82`; 108 Gems/Japa Mala item `226` at offset `0x1e`. |

Merchant City of Dorter (`012`, entry `403`) was already implemented and playtested before this
continuation pass. It remains the event-spawned slot-add reference case documented under
`docs/modding/04-adding-event-spawned-enemies.md`.

## Validation Commands

Reproduction:

```powershell
python -m py_compile tools/battle_patch.py
python tools/battle_patch.py araguay zeirchele zaland balias_tor tchigolith goug balias_swale golgollada lionel_gate cuchulainn
python tools/validate_ch2_v2.py
```

Post-patch binary validation was run against
`src/fftivc.battles.ngplus/entd/battle_entd4_ent.bin`. The stronger validation covered:

- all static slot-add UnitIDs and jobs;
- Merchant Dorter's event-spawned Knight ENTD slot and `event119.e` registration/choreography bytes;
- Chapter 2 roster jobs/levels for every implemented entry;
- generic human job-rank seeds matching `mainJob - 0x4a`;
- Boco player-control bit;
- Zeirchele's vanilla intro corpse placeholders `s2/s3` remain byte-for-byte untouched;
- Zeirchele's `root.nxl` `OverrideEntryData` count includes the new `s11` row;
- Lionel Gate Blood Sword equipment;
- Cuchulainn's 108 Gems/Japa Mala Spoils byte.

Latest local result from `python tools/validate_ch2_v2.py`: `76/76 checks passed`.

Build/deploy validation:

```powershell
$env:RELOADEDIIMODS='C:/Reloaded-II/Mods'
dotnet build src\fftivc.battles.ngplus\fftivc.battles.ngplus.csproj -c Release
```

Latest deploy result: build succeeded with `0 Warning(s)` and `0 Error(s)`, outputting the DLL to
`C:\Reloaded-II\Mods\fftivc.battles.ngplus\fftivc.battles.ngplus.dll`.

## Remaining Playtest Questions

The binary implementation is complete, but in-game balance still needs human playtest feedback:

- whether Araguay's promoted monster pack and Coeurl pressure are fair with controlled Boco;
- whether Zeirchele's `s11` White Mage support appears as the seventh enemy and makes Ovelia protection tense without dragging the fight;
- whether Zaland's two Dragoons pressure Mustadio without creating an unfair opener;
- whether Balias Tor and Goug Summoner tempo remains race-able;
- whether the Lionel Gate -> Cuchulainn no-resupply chain taxes resources without item starvation.
