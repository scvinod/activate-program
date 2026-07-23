resource "google_service_account" "mcp" {
  project      = var.project_id
  account_id   = "coupon-mcp-server"
  display_name = "Coca-Cola Program MCP Server Cloud Run Service Account"
}

resource "google_service_account" "agent" {
  project      = var.project_id
  account_id   = "coupon-agent-api"
  display_name = "Coca-Cola Program Agent API Cloud Run Service Account"
}

resource "google_project_iam_member" "cloudbuild_artifact_writer" {
  project = var.project_id
  role    = "roles/artifactregistry.writer"
  member  = "serviceAccount:${data.google_project.current.number}@cloudbuild.gserviceaccount.com"
}

resource "google_project_iam_member" "cloudbuild_run_admin" {
  project = var.project_id
  role    = "roles/run.admin"
  member  = "serviceAccount:${data.google_project.current.number}@cloudbuild.gserviceaccount.com"
}

resource "google_project_iam_member" "cloudbuild_service_account_user" {
  project = var.project_id
  role    = "roles/iam.serviceAccountUser"
  member  = "serviceAccount:${data.google_project.current.number}@cloudbuild.gserviceaccount.com"
}
