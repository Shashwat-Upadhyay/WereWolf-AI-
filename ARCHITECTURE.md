# Architecture

## High-level flow
1. `main.py` creates the Tk root and starts `GameUI`
2. `GameUI` creates `GameEngine` and `AnimationManager`
3. Each phase advance calls `engine.advance_phase()`
4. Engine returns a timed script (`ScriptEvent[]`)
5. UI replays script events and renders animations

## Core components

### GameEngine (`engine.py`)
- Owns player roster, phase state, day counter, winner state
- Runs day and night phase logic
- Produces deterministic event structures for UI playback
- Maintains AI instances per player role

### AI players (`engine.py`)
- `AIPlayer` base with suspicion/trust tracking
- `Villager`, `Werewolf`, `Doctor`, `Detective` specialize behavior
- Observe dialogue/votes/reveals and adapt decisions

### GameUI (`ui.py`)
- Handles widgets, scene rendering, and input
- Maintains selected player perspective for suspicion meter
- Dispatches script events into log + animation effects
- Uses `root.after(...)` loop for frame updates

### Animation system (`animations.py`)
- `AnimationManager` updates active animations each frame
- Each animation has duration, update, and finish lifecycle
- Includes speech bubbles, vote arrows, reveal pulses, shield flashes, etc.

## Data models (`models.py`)
- `Role`, `Phase` enums
- `Player`, `Dialogue`, `ScriptEvent` dataclasses

## Configuration and utilities
- `config.py`: colors, sizing, timing, asset variants
- `utils.py`: clamp/interpolation/easing + asset path resolution
