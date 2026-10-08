#!/usr/bin/env bash
# Reproduce every number in the report. Needs Python 3 with pandas, numpy and plotly (the board imports them).
# Never runs Streamlit: harness.py executes the board with a mock streamlit module.
set -euo pipefail
cd "$(dirname "$0")"
PY=${PYTHON:-python3}
for s in check_snapshot delay analysis2 vacuum engines engines_all recovery_threshold; do echo "== $s"; $PY -I $s.py; done
