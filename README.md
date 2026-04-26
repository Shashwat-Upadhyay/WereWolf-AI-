# WereWolf-AI-

Animated AI-vs-AI Werewolf (Mafia) simulation built with Python and Tkinter.

## What this project does
- Runs a complete Werewolf game with AI players
- Simulates day discussions, voting, and night actions
- Displays animated gameplay in a Tkinter UI
- Tracks suspicion and trust between players

## Features
- 8-player default game (configurable in engine)
- Roles: Villager, Werewolf, Doctor, Detective
- Auto-play and manual phase controls
- Animated events: speech, votes, night actions, shields, reveals, winner banner
- Fallback behavior when assets are missing

## Repository
- Current repo: https://github.com/AkshUpase/WereWolf-AI-

## Requirements
- Python 3.9+
- Tkinter (usually included with Python desktop installs)

## Quick start
```bash
git clone https://github.com/AkshUpase/WereWolf-AI-.git
cd WereWolf-AI-
python main.py
```

## Controls
- `F5` or `Space`: Advance to next phase
- `F6`: Toggle auto-play
- `F2`: Start a new game
- Click a player: focus suspicion meter on that player

## Project structure
- `main.py` – app entrypoint
- `ui.py` – Tkinter UI, rendering, event playback
- `engine.py` – game loop, AI decisions, phase progression
- `models.py` – enums/data models
- `animations.py` – animation primitives and manager
- `config.py` – constants and theme settings
- `utils.py` – math and asset helpers
- `assets/` – images used by the UI

## Documentation
- [PROJECT_GUIDE.md](PROJECT_GUIDE.md) – detailed technical guide
- [SIMPLE_EXPLANATION.md](SIMPLE_EXPLANATION.md) – beginner-friendly explanation
- [ARCHITECTURE.md](ARCHITECTURE.md) – runtime architecture overview
- [GAMEPLAY.md](GAMEPLAY.md) – gameplay rules and flow
- [DEVELOPMENT.md](DEVELOPMENT.md) – development and validation notes

## Troubleshooting
- `No module named tkinter`:
  - Ubuntu/Debian: `sudo apt-get install python3-tk`
  - Fedora: `sudo dnf install python3-tkinter`
- Blank/missing images:
  - Ensure files are present in `assets/`
  - The game still runs with visual fallbacks

## License
MIT
