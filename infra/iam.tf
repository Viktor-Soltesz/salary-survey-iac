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

data "google_storage_project_service_account" "gcs_account" {}

resource "google_project_iam_member" "gcs_to_pubsub" {
  project = var.project_id
  role    = "roles/pubsub.publisher"
  member  = "serviceAccount:${data.google_storage_project_service_account.gcs_account.email_address}"
}

resource "google_service_account_iam_member" "terraform_act_as_function_sa" {
  service_account_id = google_service_account.function_sa.id
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:${var.terraform_sa_email}"  # Assuming this variable holds your Terraform SA email
}