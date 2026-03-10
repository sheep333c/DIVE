#!/bin/bash
set -euo pipefail

# Usage:
#   ./scripts/run.sh synthesize                    # Generate tasks only
#   ./scripts/run.sh end2end                       # Full pipeline
#   ./scripts/run.sh end2end --domain biological   # With CLI overrides

MODE="${1:?Usage: $0 <synthesize|end2end> [extra args...]}"
shift

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

python -m dive "$MODE" --config dive.yaml "$@"
