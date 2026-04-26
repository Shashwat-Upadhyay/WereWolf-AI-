# Development

## Local validation
Recommended baseline checks:
```bash
python -m compileall .
python -m unittest discover -s tests -p "test_*.py" -v
```

Headless experiment run (reproducible):
```bash
python experiments.py \
  --matches 200 \
  --players 8 \
  --profile standard \
  --seed 1234 \
  --json-out results/summary.json \
  --csv-out results/matches.csv \
  --timeline-out results/timeline.json
```

Compare profiles:
```bash
python experiments.py --matches 500 --profile standard --seed 1234
python experiments.py --matches 500 --profile baseline_random --seed 1234
python experiments.py --matches 500 --profile baseline_majority --seed 1234
python experiments.py --matches 500 --profile ablation_no_memory --seed 1234
python experiments.py --matches 500 --profile ablation_role_agnostic --seed 1234
```

## CI
GitHub Actions workflow (`.github/workflows/ci.yml`) runs:
- `python -m compileall .`
- `python -m unittest discover -s tests -p "test_*.py" -v`

## Coding notes
- Keep changes focused and small
- Preserve script-event contract between engine and UI
- Keep role behavior changes balanced across both teams
- Update docs when behavior or controls change
