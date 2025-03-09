terraform { # This block specifies that backend should be remote. Further details injected by the deployment pipeline.
  backend "gcs" {
  }

  required_providers {
    google = {
      version = "4.77.0"
    }
  }

  provider_meta "google" {
    module_name = "salary-survey-iac/terraform-deployment-v1"
  }
}

# While GitHub Actions overrides variables dynamically, Terraform still expects these variables to be defined somewhere. 
# If Terraform is run outside of GitHub Actions, Terraform needs a fallback mechanism.
provider "google" { 
  project = var.project_id
  region  = var.region
}