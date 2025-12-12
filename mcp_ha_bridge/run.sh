#!/usr/bin/env bash
set -e

OPTIONS_FILE=/data/options.json

# Read variables from options.json using jq
HA_URL=$(jq -r '.ha_url' "$OPTIONS_FILE")
HA_TOKEN=$(jq -r '.ha_token' "$OPTIONS_FILE")
EXPOSED=$(jq -r '.exposed_entities | join(",")' "$OPTIONS_FILE")

export HA_URL
export HA_TOKEN
export EXPOSED

echo "Starting MCP HA bridge with:"
echo "  HA_URL=$HA_URL"
echo "  Exposed entities: $EXPOSED"

python3 /app/mcp_server.py
