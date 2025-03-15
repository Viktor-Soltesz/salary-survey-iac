resource "google_bigquery_dataset" "surveys" {
  dataset_id  = "surveys"
  description = "Store survey data"
  location    = var.region
  labels      = local.resource_labels

  lifecycle {
    prevent_destroy = true
    ignore_changes  = all
  }
}

resource "google_bigquery_table" "developer_salaries" {
  dataset_id          = google_bigquery_dataset.surveys.dataset_id
  table_id            = "developer_salaries"
  description         = "Store developer salary survey data"
  deletion_protection = false

  # time_partitioning { # No partitioning for now, as dataset is small
  #   type  = "DAY"
  #   field = "action_time"
  # }

  labels = local.resource_labels

  schema = <<EOF
[
  {
    "name": "order_id",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "customer_email",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "action",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "action_time",
    "type": "STRING",
    "mode": "NULLABLE"
  }
]
EOF
}
