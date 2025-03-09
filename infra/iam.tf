# Retrieves the current project details dynamically.
# This avoids hardcoding project metadata.
# Can be referenced elsewhere as:
data "google_project" "project" {}

resource "google_service_account" "function_sa" {
  account_id   = local.function_name
  display_name = "Cloud Function service account"
}

resource "google_project_iam_member" "storage_admin" {
  project = var.project_id
  role    = "roles/storage.admin"
  member  = "serviceAccount:${google_service_account.function_sa.email}"
}

resource "google_project_iam_member" "bq_admin" {
  project = var.project_id
  role    = "roles/bigquery.admin"
  member  = "serviceAccount:${google_service_account.function_sa.email}"
}

resource "google_project_iam_member" "iam_user" {
  project = var.project_id
  role    = "roles/iam.serviceAccountUser"
  member  = "serviceAccount:${google_service_account.function_sa.email}"
}

resource "google_project_iam_member" "event_receiver" {
  project = var.project_id
  role    = "roles/eventarc.eventReceiver"
  member  = "serviceAccount:${google_service_account.function_sa.email}"
}

resource "google_project_iam_member" "invoker" {
  project = var.project_id
  role    = "roles/run.invoker"
  member  = "serviceAccount:${google_service_account.function_sa.email}"
}

# Retrieves the default Cloud Storage service account for the project.
# Used to grant Pub/Sub permissions
data "google_storage_project_service_account" "gcs_account" {}

resource "google_project_iam_member" "gcs_to_pubsub" {
  project = var.project_id
  role    = "roles/pubsub.publisher"
  member  = "serviceAccount:${data.google_storage_project_service_account.gcs_account.email_address}"
}

resource "google_service_account_iam_member" "terraform_act_as_function_sa" {
  service_account_id = google_service_account.function_sa.id
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:${var.sa_email}"
}

# Fetch the Compute Engine default service account dynamically
data "google_compute_default_service_account" "default" {
  project = var.project_id
}

# Grant Terraform SA the ability to act as Compute Engine default SA
resource "google_service_account_iam_member" "terraform_act_as_compute_sa" {
  service_account_id = data.google_compute_default_service_account.default.email
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:${var.sa_email}"
}