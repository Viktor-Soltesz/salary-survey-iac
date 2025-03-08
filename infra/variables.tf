locals {
  function_name = "gcs-to-bq-trigger"
  resource_labels = merge(var.resource_labels, {
    deployed_by = "cloudbuild"
    repo        = "click-to-deploy-solutions"
    solution    = "cloud-composer-etl"
    terraform   = "true"
  })
}

# ID of the project in which you want to deploy the solution
variable "project_id" {
  type    = string
  description = "GCP Project ID"
  # default = "software-developer-salaries"
}

variable "sa_email" {
  description = "Email of the Terraform service account"
  type        = string
}

#Defines the deployment region for cloud resources.
variable "region" {
  type        = string
  description = "GCP region"
  # default = "europe-west9"
}

#Assigns a label to provisioned cloud resources
variable "resource_labels" {
  type        = map(string)
  description = "Resource labels"
  default     = {}
}
