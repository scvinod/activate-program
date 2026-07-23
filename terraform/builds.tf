resource "null_resource" "build_mcp_image" {
  triggers = {
    image      = local.mcp_image
    source_md5 = md5(join("", [for file in local.mcp_source_files : filemd5(file)]))
  }

  provisioner "local-exec" {
    command = "gcloud builds submit ${local.repo_root}/mcp-server --config=${local.repo_root}/mcp-server/cloudbuild.yaml --substitutions=_IMAGE=${local.mcp_image} --project=${var.project_id} --region=${var.region}"
  }

  depends_on = [
    google_artifact_registry_repository.containers,
    google_project_service.required,
    google_project_iam_member.cloudbuild_artifact_writer,
  ]
}

resource "null_resource" "build_agent_image" {
  triggers = {
    image      = local.agent_image
    source_md5 = md5(join("", [for file in local.agent_source_files : filemd5(file)]))
  }

  provisioner "local-exec" {
    command = "gcloud builds submit ${local.repo_root}/agent-api --config=${local.repo_root}/agent-api/cloudbuild.yaml --substitutions=_IMAGE=${local.agent_image} --project=${var.project_id} --region=${var.region}"
  }

  depends_on = [
    google_artifact_registry_repository.containers,
    google_project_service.required,
    google_project_iam_member.cloudbuild_artifact_writer,
  ]
}
