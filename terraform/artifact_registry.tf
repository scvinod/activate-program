resource "google_artifact_registry_repository" "containers" {
  project       = var.project_id
  location      = var.region
  repository_id = var.artifact_registry_repository_id
  description   = "Container images for the Coca-Cola program chatbot services."
  format        = "DOCKER"

  depends_on = [google_project_service.required]
}
