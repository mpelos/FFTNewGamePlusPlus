---
name: fft-level-design
description: Use this skill whenever designing, revising, implementing, or reviewing a Final Fantasy Tactics New Game++ story battle/level in this repo. Trigger on requests like "fazer level", "fazer uma batalha", "ajustar uma batalha", "balancear esse mapa", "implementar o doc da batalha", "revisar dificuldade", "simular a batalha", or any task involving FFTNewGamePlusPlus battle docs, ENTD entries, level bands, enemy compositions, guest handling, gear, abilities, rewards, or chapter difficulty progression. This skill enforces gate questions before edits, required document reads, chapter-specific philosophy, tmp/ simulations, iteration, and validation before changing battle docs or patch data.
---

# FFT Level Design

Use this skill to turn a story battle into a coherent New Game++ level: the player-facing idea,
enemy party, gear, abilities, rewards, guest handling, ENTD implementation, and playtest questions
must all point at the same intended challenge.

The word "level" means the whole battle/encounter design, not only numeric unit levels.

## Hard Start Rule: Gate Before Edits

Before changing tracked docs, code, binary data, or patch scripts, ask gate questions and wait for
answers unless the user's latest prompt already answers them concretely. Keep the questions short.

Use these gates:

```text
1. Which battle/doc is in scope, and is the task design-only, implementation-only, or both?
2. What is allowed to change: jobs, enemy count, gear, abilities, placement, rewards, guest flags,
   level bands, objectives, or only documentation?
3. What is the chapter target: Chapter 1 presentation, Chapter 2 preview, Chapter 3 complete
   synergy, or Chapter 4 broken puzzle?
4. What must remain recognizable from vanilla: feeling, lesson, terrain pressure, objective,
   roster archetypes, named boss behavior, chain/no-resupply constraint?
5. Are there active guests or protected NPCs? Confirm that every active guest must be player-
   controlled in NG+ regardless of whether the objective says to save them.
6. What is the success bar: doc draft, patch function, binary diff, simulation report, in-game
   playtest checklist, or all of these?
```

If one answer is missing but does not affect the first safe step, state the assumption and continue
only with read-only investigation or `tmp/` simulation scaffolding. Do not patch the battle under an
unstated scope assumption.

## Required Reads

Read the smallest complete set before proposing changes.

Always read:

```text
README.md
docs/battles/000-chapter-1-overview.md
the target battle doc under docs/battles/
the relevant chapter overview:
  Chapter 1 -> 000-chapter-1-overview.md
  Chapter 2 -> 011-chapter-2-overview.md
  Chapter 3 -> 024-chapter-3-overview.md
  Chapter 4 -> 037-chapter-4-overview.md
```

Before changing any code, patch script, binary game data, NXD table, event script, runtime hook,
or deployed mod artifact, also read:

```text
docs/modding/10-event-scripts-and-the-e-files.md
```

This read is mandatory for implementation work because battle changes can live in several
different layers: ENTD slots, `OverrideEntryData`/`root.nxl`, `.e` event scripts, sprite-sheet
budget, runtime hooks, and deploy verification. Use doc `10` to classify the change before
editing: job-swap, static add, formation-gated static add, or script-managed/wave add. Do not
patch gameplay data by intuition when doc `10` says the unit's existence may depend on event
registration, choreography, NXD rows, or sprite-budget limits.

Read additionally when relevant:

```text
Chapter balance reviews:
  Chapter 1 -> docs/battles/010-chapter-1-balance-review.md
  Chapter 2 -> docs/battles/023-chapter-2-balance-review.md
  Chapter 3 -> docs/battles/036-chapter-3-balance-review.md
  Chapter 4 -> docs/battles/059-chapter-4-balance-review.md

Reward work:
  docs/spoils-of-war-reward-system.md
  docs/battles/chapter-4-rewards-implementation.md

No-resupply or endgame chains:
  every battle doc in the chain
  docs/battles/ENDGAME-BLOCKER.md for the final gauntlet

Implementation:
  tools/entd_tool.py
  tools/battle_patch.py if present
  tools/guest_scan.py for guest/team flag facts
  src/fftivc.battles.ngplus/Program.cs for runtime ENTD/guest behavior
```

When external facts are needed, prefer primary/local project docs first. Browse only when the user
asks for current external research or the local docs do not answer a mechanics question.

## Chapter Principles

Carry the chapter philosophy into every proposal.

```text
Chapter 1:
- Presentation chapter. Story battles scale, but the player is not forced into meta checks yet.
- Keep identity and curve readable; at most one meaningful new threat.
- Final-shop style gear; no unique/superboss loot.
- Non-boss enemies usually 100-102; leaders/uniques may go slightly higher.
- Every active guest is player-controlled in NG+.

Chapter 2:
- First real step up. Less puzzle, more preview of advanced systems.
- Any normal job tier is legal if it preserves the battle spirit, except Mime/Calculator.
- Every active human enemy has full equipment and intentional reaction/support/movement.
- Secondary is allowed but optional; use it when it clarifies the role.
- Extra enemies are allowed only when they sharpen action economy, flanks, bodyguards, or route pressure.

Chapter 3:
- Complete, synergistic enemy parties.
- Every active human enemy has equipment plus secondary, reaction, support, and movement.
- Advanced jobs are ordinary tools; parties should work together but avoid full broken stacks.
- No-resupply chains must be evaluated as chains, not isolated fights.

Chapter 4:
- Broken-but-readable puzzle parties are allowed and expected.
- Normal enemies may carry role-fitting non-buyable gear when it serves the puzzle.
- One headline engine per battle; supporting units amplify it instead of introducing unrelated engines.
- Best gear and Tier-A/Tier-S rewards must match the reward ledger.
```

Global rules:

```text
- Preserve the vanilla feeling before choosing jobs.
- Difficulty comes from action economy, threat diversity, terrain, target priority, resource pressure,
  and readable synergies, not hidden stat inflation.
- Do not use guest AI as a skill check. Guests must be player-controlled in NG+.
- Avoid hard lockdown spam: Stop, Don't Act, Petrify, Death, Charm, or equivalent turn deletion must
  be visible, limited, answerable, and chapter-appropriate.
- Respect job equipment rules and data constraints.
- Never silently remove a protected FFT system: stealing, breaking, Poach, monster/recruitment,
  Brave/Faith planning, map treasure, chain constraints, or rare rewards.
```

## Workflow

### 1. Establish Scope And Read Context

Answer the gate questions first. Then read the required docs. Summarize the constraints in a short
block before designing:

```text
Battle:
Chapter:
Vanilla feeling:
Chapter rule:
Allowed changes:
Guest/control implications:
Reward implications:
Chain/no-resupply implications:
Implementation layer:
```

### 2. Diagnose The Vanilla Battle

Before picking jobs or equipment, write the battle's intent:

```text
Original difficulty role:
Original emotional beat:
Original tactical lesson:
What must remain recognizable:
What made vanilla trivial under NG+:
What would make the redesign cheap:
```

### 3. Draft The Level

Create a first draft in the battle doc style already used by the repo. For new or revised battle
docs, include:

```text
Design Goal
Local Data Confirmed / data still needed
Enemy party escalation
Sanctioned exceptions
Rare/reward handling
Proposed Composition
Builds
Positioning Plan
Simulation Plan and Results
Implementation Checklist
Test Questions
Sources
```

For implementation tasks, keep edits scoped to the target battle window or patch function. Do not
rewrite unrelated battle docs or global rules unless the user explicitly asks.

### 4. Simulate Before Finalizing

Every non-trivial battle change needs a simulation artifact under `tmp/`.

Create a directory like:

```text
tmp/fft-level-design-<doc-number-or-entry>-<slug>/
```

Put the simulation code and outputs there:

```text
model.py or simulate.py
input.json or assumptions.md
iteration-1-results.json
iteration-1-results.md
iteration-2-results.json
iteration-2-results.md
```

The simulation can be coarse. Its job is to expose bad assumptions before patching. Model only what
matters for the battle's headline demand:

```text
- action economy: expected enemy/player actions over the first 3-5 rounds
- time to first lethal threat or first objective pressure
- target priority: whether the intended engine is reachable/answerable
- guest survival/control: guest starts controllable and does not fail before player response
- boss race: expected turns to break/disarm/burst/flee/phase transition
- chain tax: HP/MP/item/status pressure carried into the next fight
- status/control risk: chance and impact of lost turns, with available answers
```

Use deterministic assumptions where exact FFT formulas are unavailable. Name those assumptions in
the results. Do not claim the sim proves the fight is balanced; claim only that the design passes
the stated model and list residual playtest risks.

### 5. Iterate

Run at least one draft-sim-review loop:

```text
1. Draft composition.
2. Simulate the headline demand.
3. Identify failure modes: trivial burst, guest fail, hard lock, cleanup slog, impossible chain tax,
   reward exploit, unreadable target priority.
4. Revise composition/placement/gear/abilities.
5. Re-run the sim.
6. Record what changed and why.
```

Stop iterating only when the design meets the chapter objective under the model and the remaining
risks are explicit playtest questions.

### 6. Validate Against Gates

Before final edits or patching, run this checklist:

```text
- The vanilla feeling is still recognizable.
- The chapter-specific progression rule is obeyed.
- The enemy party has a clear role structure.
- Every active human has the required equipment/ability completeness for the chapter.
- Guest-control handling is documented for every active guest.
- Rewards and non-buyable gear follow the chapter reward policy.
- Added enemies sharpen the battle instead of creating cleanup.
- The fight has at least two fair answers.
- The fight explicitly avoids one or more player metas so it does not become a pile-up.
- The simulation artifacts exist under tmp/ and their assumptions are named.
- Open risks are translated into concrete in-game test questions.
```

If a checklist item fails, revise before patching.

## Output Format

When reporting back to the user, keep it concise:

```text
Gate answers / assumptions:
Files read:
Draft summary:
Simulation artifacts:
Iteration changes:
Files changed:
Validation:
Remaining playtest risks:
```

Use clickable file links for local files in final responses.

