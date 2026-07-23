resource "google_cloud_run_v2_service" "mcp_server" {
  project  = var.project_id
  name     = var.mcp_service_name
  location            = var.region
  ingress             = "INGRESS_TRAFFIC_ALL"
  deletion_protection = false

  template {
    service_account = google_service_account.mcp.email

    containers {
      name  = "mcp-server"
      image = local.mcp_image

      ports {
        container_port = 8080
      }

      env {
        name  = "MCP_TRANSPORT"
        value = "streamable-http"
      }

      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }
    }

    scaling {
      min_instance_count = var.mcp_min_instances
      max_instance_count = 5
    }
  }

  depends_on = [
    null_resource.build_mcp_image,
    google_project_service.required,
  ]
}

resource "google_cloud_run_v2_service_iam_member" "agent_invokes_mcp" {
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.mcp_server.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.agent.email}"
}
