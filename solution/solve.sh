#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "[solve.sh] Running golden solution..."
python3 "$SCRIPT_DIR/solve.py"
echo "[solve.sh] Done."