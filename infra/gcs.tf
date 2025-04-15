resource "google_storage_bucket" "upload_bucket" {
  name                        = "${var.project_id}-upload"
  location                    = var.region
  uniform_bucket_level_access = true
  force_destroy               = true
  labels                      = local.resource_labels
  logging {
    log_bucket        = google_storage_bucket.access_logs_bucket.name
    log_object_prefix = "upload_bucket_logs/"
  }
  lifecycle {
    prevent_destroy = true
    ignore_changes  = all
  }
}

resource "google_storage_bucket" "archive_bucket" {
  name                        = "${var.project_id}-archive"
  location                    = var.region
  uniform_bucket_level_access = true
  force_destroy               = true
  labels                      = local.resource_labels
  logging {
    log_bucket        = google_storage_bucket.access_logs_bucket.name
    log_object_prefix = "archive_bucket_logs/"
  }
  lifecycle {
    prevent_destroy = true
    ignore_changes  = all
  }
}

# Bucket specifically for storing access logs from other buckets
resource "google_storage_bucket" "access_logs_bucket" {
  name                        = "${var.project_id}-access-logs"
  location                    = var.region
  uniform_bucket_level_access = true
  labels                      = local.resource_labels
  lifecycle {
    prevent_destroy = true # Protect log data from accidental deletion
  }
  # Retention policy or lifecycle rules for logs
  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30
    }
  }
}