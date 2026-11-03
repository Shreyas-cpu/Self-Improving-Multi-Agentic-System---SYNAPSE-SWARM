#!/usr/bin/env bash
# ==============================================================================
# SYNAPSE-SWARM // Faculty Demonstration Launcher
# 1-Click Startup for Autonomous Self-Improving Multi-Agent Platform
# ==============================================================================

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$DIR"

PORT="${PORT:-8765}"
HOST="${HOST:-127.0.0.1}"

echo "========================================================================"
echo " 🧠 SYNAPSE-SWARM: Self-Improving Multi-Agent System"
echo " MDM Faculty Demonstration Engine"
echo "========================================================================"
echo "📍 Location: $DIR"
echo "🌐 URL:      http://$HOST:$PORT"
echo "⚙️ Mode:     Dual (Accelerated Presets + Live Gemini 2.5 Flash API)"
echo "📄 Report:   $DIR/PROJECT_REPORT.md"
echo "========================================================================"

# Check if port is in use
if lsof -Pi :"$PORT" -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️ Port $PORT is already in use. Killing prior instance..."
    kill -9 $(lsof -t -i:"$PORT") 2>/dev/null || true
    sleep 1
fi

# Attempt to open browser in background after 1.5s
(
    sleep 1.5
    if command -v xdg-open >/dev/null 2>&1; then
        xdg-open "http://$HOST:$PORT" >/dev/null 2>&1 || true
    fi
) &

export PYTHONPATH="$DIR"
python3 -m app.web.server
