# Architecture

## High-level flow
1. `main.py` creates the Tk root and starts `GameUI`
2. `GameUI` creates `GameEngine` and `AnimationManager`
3. Each phase advance calls `engine.advance_phase()`
4. Engine returns a timed script (`ScriptEvent[]`)
5. UI replays script events and renders animations

## Module interaction diagram
```text
main.py
  └── ui.py (GameUI)
       ├── engine.py (GameEngine + AI profiles)
       │    ├── models.py (Role, Phase, Player, Dialogue, ScriptEvent)
       │    └── utils.py (math helpers)
       ├── animations.py (animation lifecycle manager + effects)
       └── config.py (theme, sizing, timing, assets)

experiments.py
  └── engine.py (headless batch evaluation + reproducible seeds)
```

## Core components

### GameEngine (`engine.py`)
- Owns player roster, phase state, day counter, winner state
- Runs day and night phase logic
- Produces timed script-event structures for UI playback
- Maintains AI instances per player role
- Supports evaluation profiles:
  - `standard`
  - `baseline_random`
  - `baseline_majority`
  - `ablation_no_memory`
  - `ablation_role_agnostic`
- Captures per-phase timeline and exposes `match_summary()` for analytics

### AI players (`engine.py`)
- `AIPlayer` base with suspicion/trust tracking
- `Villager`, `Werewolf`, `Doctor`, `Detective` specialize behavior
- Baseline and ablation variants for experiment comparisons

### GameUI (`ui.py`)
- Handles widgets, scene rendering, and input
- Maintains selected player perspective for suspicion meter
- Dispatches script events into log + animation effects
- Uses `root.after(...)` loop for frame updates

### Animation system (`animations.py`)
- `AnimationManager` updates active animations each frame
- Each animation has duration, update, and finish lifecycle
- Includes speech bubbles, vote arrows, reveal pulses, shield flashes, and winner effects

## Data models (`models.py`)
- `Role`, `Phase` enums
- `Player`, `Dialogue`, `ScriptEvent` dataclasses

## Configuration and utilities
- `config.py`: colors, sizing, timing, asset variants
- `utils.py`: clamp/interpolation/easing + asset path resolution

## Engine ↔ UI script-event contract
`GameEngine.advance_phase()` returns ordered `ScriptEvent` items. Each event has:
- `at`: relative timestamp (seconds from phase start)
- `kind`: event type
- `payload`: data for UI render/log actions

Event kinds consumed by UI:
- `speech`, `vote`, `log`, `death`, `reveal`, `kill_move`, `shield`, `scan`, `phase_transition`, `winner`

The UI reads and animates events; authoritative game-state mutation happens in the engine.

## Heuristic design rationale
- Suspicion + trust provide interpretable and explainable AI behavior.
- Role-specialized logic captures asymmetric information in social deduction gameplay.
- Baselines and ablations provide controlled comparisons for academic evaluation.

## Complexity and performance notes
- Day vote tally: `O(P)` votes + `O(P)` counting (`P` = living players)
- Dialogue + observation updates: approximately `O(P^2)` per day
- Night actions: `O(P)` target selection per active power role
- Practical runtime is small for supported range (6–12 players), enabling large headless batch runs
