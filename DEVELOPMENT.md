# Development

## Local validation
This repository currently has no dedicated test suite.

Recommended baseline check:
```bash
python -m compileall .
```

Optional engine stress check (headless):
```bash
python - <<'PY'
from engine import GameEngine
for n in [6,7,8,9,10,11,12]:
    for _ in range(100):
        g = GameEngine(n)
        while not g.winner:
            g.advance_phase()
print('ok')
PY
```

## Coding notes
- Keep changes focused and small
- Preserve script-event contract between engine and UI
- Keep role behavior changes balanced across both teams
- Update docs when behavior or controls change
