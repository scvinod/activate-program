#!/usr/bin/env bash
set -euo pipefail

PROJECT_ID="${PROJECT_ID:?Set PROJECT_ID}"
REGION="${REGION:-us-central1}"

echo "Deploying MCP server..."
gcloud run deploy coupon-mcp-server \
  --source ./mcp-server \
  --region "${REGION}" \
  --allow-unauthenticated \
  --set-env-vars "MCP_TRANSPORT=streamable-http" \
  --project "${PROJECT_ID}"

MCP_URL="$(gcloud run services describe coupon-mcp-server \
  --region "${REGION}" \
  --project "${PROJECT_ID}" \
  --format 'value(status.url)')"

echo "Deploying agent API..."
gcloud run deploy coupon-agent-api \
  --source ./agent-api \
  --region "${REGION}" \
  --allow-unauthenticated \
  --set-env-vars "MCP_SERVER_URL=${MCP_URL},OPENAI_MODEL=gpt-4o-mini" \
  --set-secrets "OPENAI_API_KEY=openai-api-key:latest" \
  --project "${PROJECT_ID}"

echo "Deployment complete."
echo "MCP server: ${MCP_URL}"
echo "Agent API: $(gcloud run services describe coupon-agent-api --region "${REGION}" --project "${PROJECT_ID}" --format 'value(status.url)')"
