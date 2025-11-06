resource "google_service_account" "metadata_exfil_sa" {
  account_id   = "metadata-exfil-sa"
  display_name = "Metadata Exfiltration Lab SA"
}

resource "google_project_iam_binding" "sa_binding" {
  project = var.project_id
  role    = "roles/storage.admin"
  members = [
    "serviceAccount:${google_service_account.metadata_exfil_sa.email}"
  ]
}
