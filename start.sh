#!/bin/bash
# Avvia lo Scummbar con sessioni persistenti su SQLite

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DB_PATH="${SCRIPT_DIR}/data/sessions.db"

echo "🍺 Avvio Scummbar..."
echo "   sessions DB: ${DB_PATH}"
echo "   url: http://localhost:8000"
echo ""

source "${SCRIPT_DIR}/py-env/bin/activate"

adk web "${SCRIPT_DIR}/src/" \
  --session_service_uri "sqlite+aiosqlite:///${DB_PATH}"
