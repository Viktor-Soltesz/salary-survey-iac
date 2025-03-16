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
  #   field = "work_year"  # Could use this if partitioning is added later
  # }

  labels = local.resource_labels

  schema = <<EOF
[
  {
    "name": "work_year",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "experience_level",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "employment_type",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "job_title",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "job_category",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "salary",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "salary_currency",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "salary_in_usd",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "employee_residence",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "country",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "remote_ratio",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "company_location",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "company_size",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "company_size_category",
    "type": "STRING",
    "mode": "NULLABLE"
  }
]
EOF
}
