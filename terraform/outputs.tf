output "project_id" {
  description = "Deployed Google Cloud project ID."
  value       = var.project_id
}

output "region" {
  description = "Deployed Google Cloud region."
  value       = var.region
}

output "artifact_registry_repository" {
  description = "Artifact Registry repository for service images."
  value       = google_artifact_registry_repository.containers.name
}

output "mcp_server_url" {
  description = "Public URL of the MCP Cloud Run service."
  value       = google_cloud_run_v2_service.mcp_server.uri
}

output "mcp_server_name" {
  description = "Cloud Run service name for the MCP server."
  value       = google_cloud_run_v2_service.mcp_server.name
}

output "agent_api_url" {
  description = "Public URL of the agent API Cloud Run service."
  value       = google_cloud_run_v2_service.agent_api.uri
}

output "agent_chat_endpoint" {
  description = "Chat endpoint exposed by the agent API."
  value       = "${google_cloud_run_v2_service.agent_api.uri}/api/chat"
}

output "agent_health_endpoint" {
  description = "Health endpoint exposed by the agent API."
  value       = "${google_cloud_run_v2_service.agent_api.uri}/health"
}

output "agent_service_account_email" {
  description = "Service account used by the agent API to call the MCP server."
  value       = google_service_account.agent.email
}

output "mcp_service_account_email" {
  description = "Service account used by the MCP server."
  value       = google_service_account.mcp.email
}

output "openai_secret_id" {
  description = "Secret Manager secret ID containing the OpenAI API key."
  value       = google_secret_manager_secret.openai_api_key.secret_id
}
