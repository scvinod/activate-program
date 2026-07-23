resource "google_cloud_run_v2_service" "agent_api" {
  project  = var.project_id
  name     = var.agent_service_name
  location            = var.region
  ingress             = "INGRESS_TRAFFIC_ALL"
  deletion_protection = false

  template {
    service_account = google_service_account.agent.email

    containers {
      name  = "agent-api"
      image = local.agent_image

      ports {
        container_port = 8080
      }

      env {
        name  = "MCP_SERVER_URL"
        value = google_cloud_run_v2_service.mcp_server.uri
      }

      env {
        name  = "MCP_SERVER_NAME"
        value = "program"
      }

      env {
        name  = "MCP_USE_CLOUD_RUN_AUTH"
        value = "true"
      }

      env {
        name  = "OPENAI_MODEL"
        value = var.openai_model
      }

      env {
        name  = "OPENAI_SSL_VERIFY"
        value = "true"
      }

      env {
        name  = "LOG_LEVEL"
        value = "INFO"
      }

      env {
        name = "OPENAI_API_KEY"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.openai_api_key.secret_id
            version = "latest"
          }
        }
      }

      resources {
        limits = {
          cpu    = "1"
          memory = "1Gi"
        }
      }
    }

    scaling {
      min_instance_count = var.agent_min_instances
      max_instance_count = 10
    }
  }

  depends_on = [
    null_resource.build_agent_image,
    google_cloud_run_v2_service.mcp_server,
    google_secret_manager_secret_version.openai_api_key,
    google_secret_manager_secret_iam_member.agent_openai_accessor,
    google_cloud_run_v2_service_iam_member.agent_invokes_mcp,
    google_project_service.required,
  ]
}

resource "google_cloud_run_v2_service_iam_member" "agent_public_invoker" {
  count = var.agent_allow_unauthenticated ? 1 : 0

  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.agent_api.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
