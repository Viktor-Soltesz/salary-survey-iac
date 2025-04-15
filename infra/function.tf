resource "google_storage_bucket" "gcf_source_bucket" {
  name                        = "${var.project_id}-gcf-source-bucket"
  location                    = var.region
  uniform_bucket_level_access = true
  labels                      = local.resource_labels
  logging {
    # Reference the logging bucket defined in gcs.tf
    log_bucket        = google_storage_bucket.access_logs_bucket.name
    log_object_prefix = "gcf_source_bucket_logs/"
  }
}
resource "google_storage_bucket_object" "gcf_source_code" {
  name   = "function-source.zip"
  bucket = google_storage_bucket.gcf_source_bucket.name
  source = "function-source.zip"
}

resource "google_cloudfunctions2_function" "function" {
  name        = local.function_name
  location    = var.region
  description = "Load data from GCS to BQ"
  labels      = local.resource_labels
  
  build_config {
    runtime     = "python310"
    entry_point = "trigger_gcs" # Set the entry point in the code

    source {
      storage_source {
        bucket = google_storage_bucket.gcf_source_bucket.name
        object = google_storage_bucket_object.gcf_source_code.name
      }
    }
  }

  service_config {
    max_instance_count    = 1
    min_instance_count    = 0
    available_memory      = "512Mi"
    timeout_seconds       = 30
    service_account_email = google_service_account.function_sa.email
    environment_variables = {
      DW_PROJECT_ID      = var.project_id
      GCS_ARCHIVE_BUCKET = google_storage_bucket.archive_bucket.name
    }
  }

  event_trigger {
    trigger_region        = var.region
    event_type            = "google.cloud.storage.object.v1.finalized"
    retry_policy          = "RETRY_POLICY_DO_NOT_RETRY"
    service_account_email = google_service_account.function_sa.email
    event_filters {
      attribute = "bucket"
      value     = google_storage_bucket.upload_bucket.name
    }
  }

  depends_on = [
    google_project_iam_member.gcs_to_pubsub,
    google_project_iam_member.event_receiver
  ]
}

data "google_cloud_run_service" "run_service" {
  name     = google_cloudfunctions2_function.function.name
  location = var.region
}

resource "google_cloud_run_service_iam_member" "run_service_member" {
  location = data.google_cloud_run_service.run_service.location
  service  = data.google_cloud_run_service.run_service.name
  role     = "roles/run.invoker"
member  = "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com"
}
