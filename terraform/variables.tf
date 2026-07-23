variable "project_id" {
  description = "Google Cloud project ID."
  type        = string
}

variable "region" {
  description = "Google Cloud region for Cloud Run and Artifact Registry."
  type        = string
  default     = "us-central1"
}

variable "artifact_registry_repository_id" {
  description = "Artifact Registry repository ID for container images."
  type        = string
  default     = "coupon-chatbot"
}

variable "image_tag" {
  description = "Container image tag applied to both services."
  type        = string
  default     = "latest"
}

variable "mcp_service_name" {
  description = "Cloud Run service name for the MCP server."
  type        = string
  default     = "coupon-mcp-server"
}

variable "agent_service_name" {
  description = "Cloud Run service name for the agent API."
  type        = string
  default     = "coupon-agent-api"
}

variable "openai_api_key" {
  description = "OpenAI API key stored in Secret Manager and mounted into the agent service."
  type        = string
  sensitive   = true
}

variable "openai_model" {
  description = "OpenAI model name used by the agent."
  type        = string
  default     = "gpt-4o-mini"
}

variable "agent_allow_unauthenticated" {
  description = "Whether the public agent API allows unauthenticated invocation."
  type        = bool
  default     = true
}

variable "mcp_min_instances" {
  description = "Minimum number of MCP server instances."
  type        = number
  default     = 0
}

variable "agent_min_instances" {
  description = "Minimum number of agent API instances."
  type        = number
  default     = 0
}
