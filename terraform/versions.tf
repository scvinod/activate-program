terraform {
  required_version = ">= 1.5.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 5.30.0"
    }
    null = {
      source  = "hashicorp/null"
      version = ">= 3.2.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

data "google_project" "current" {
  project_id = var.project_id
}

locals {
  repo_root = abspath("${path.module}/..")

  artifact_registry_host = "${var.region}-docker.pkg.dev"
  mcp_image              = "${local.artifact_registry_host}/${var.project_id}/${var.artifact_registry_repository_id}/mcp-server:${var.image_tag}"
  agent_image            = "${local.artifact_registry_host}/${var.project_id}/${var.artifact_registry_repository_id}/agent-api:${var.image_tag}"

  mcp_source_files = [
    "${local.repo_root}/mcp-server/Dockerfile",
    "${local.repo_root}/mcp-server/requirements.txt",
    "${local.repo_root}/mcp-server/server.py",
    "${local.repo_root}/mcp-server/program_service.py",
  ]

  agent_source_files = [
    "${local.repo_root}/agent-api/Dockerfile",
    "${local.repo_root}/agent-api/requirements.txt",
    "${local.repo_root}/agent-api/main.py",
    "${local.repo_root}/agent-api/agent.py",
    "${local.repo_root}/agent-api/config.py",
    "${local.repo_root}/agent-api/cloud_run_auth.py",
  ]
}
