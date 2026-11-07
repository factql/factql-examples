#!/usr/bin/env bash
# Usage: ./ask.sh "your question"
set -euo pipefail
: "${FACTQL_API_KEY:?Set FACTQL_API_KEY first}"
QUESTION="${1:-What were the top 5 products by revenue?}"

curl -sS -X POST "https://api.factql.ai/query" \
  -H "X-API-Key: $FACTQL_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(printf '{"q": %s}' "$(printf '%s' "$QUESTION" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')")"
echo
