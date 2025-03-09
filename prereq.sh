#!/bin/bash
set -e

# Helper function to add IAM roles
add_iam_member() {
  gcloud projects add-iam-policy-binding "$PROJECT_ID" --member="$1" --role="$2"
}

# Prompt for Project ID if not set
if [ -z "$PROJECT_ID" ]; then
  echo "What Project ID do you want to use?"
  read -r var_project_id
  export PROJECT_ID="$var_project_id"
fi

echo "Setting project to $PROJECT_ID..."
gcloud config set project "$PROJECT_ID"

# Create Terraform state bucket
TF_STATE_BUCKET="$PROJECT_ID-tf-state"
BUCKET_NAME="gs://$TF_STATE_BUCKET"
if gsutil ls "$BUCKET_NAME" 2>/dev/null; then
  echo "Terraform state bucket $BUCKET_NAME already exists!"
else
  echo "Creating Terraform state bucket $BUCKET_NAME..."
  gsutil mb -p "$PROJECT_ID" -l europe-west9 "$BUCKET_NAME"
  echo "Enabling versioning on the bucket..."
  gsutil versioning set on "$BUCKET_NAME"
fi

# Enable required APIs
echo "Enabling required APIs..."
gcloud services enable \
  storage.googleapis.com \
  bigquery.googleapis.com \
  cloudfunctions.googleapis.com \
  iam.googleapis.com \
  eventarc.googleapis.com \
  pubsub.googleapis.com \
  run.googleapis.com \
  cloudresourcemanager.googleapis.com \
  compute.googleapis.com \
  --project "$PROJECT_ID"

# Create Terraform service account (if not exists)
TF_SA="terraform-sa@$PROJECT_ID.iam.gserviceaccount.com"
if ! gcloud iam service-accounts describe "$TF_SA" --project "$PROJECT_ID" 2>/dev/null; then
  echo "Creating Terraform service account..."
  gcloud iam service-accounts create terraform-sa \
    --display-name="Terraform Service Account" \
    --project "$PROJECT_ID"
fi

# Grant Terraform SA permissions
echo "Granting Terraform SA permissions..."
add_iam_member "serviceAccount:$TF_SA" "roles/storage.admin"
add_iam_member "serviceAccount:$TF_SA" "roles/serviceusage.serviceUsageAdmin"
add_iam_member "serviceAccount:$TF_SA" "roles/resourcemanager.projectIamAdmin"
add_iam_member "serviceAccount:$TF_SA" "roles/cloudfunctions.admin"
add_iam_member "serviceAccount:$TF_SA" "roles/bigquery.admin"
add_iam_member "serviceAccount:$TF_SA" "roles/iam.serviceAccountAdmin"
add_iam_member "serviceAccount:$TF_SA" "roles/pubsub.admin"
#add_iam_member "serviceAccount:221846650138-compute@developer.gserviceaccount.com" "roles/iam.serviceAccountUser"

# Grant GCS SA permissions for Eventarc
GCS_SA="$(gsutil kms serviceaccount -p "$PROJECT_ID")"
add_iam_member "serviceAccount:$GCS_SA" "roles/pubsub.publisher"

echo "Setup complete!"
echo "Next steps:"
echo "1. Generate a key for $TF_SA in the GCP Console (IAM & Admin > Service Accounts)."
echo "2. Store the key in GitHub Secrets as GOOGLE_CREDENTIALS."
echo "3. Store PROJECT_ID ($PROJECT_ID) and TERRAFORM_SERVICE_ACCOUNT_EMAIL ($TF_SA) in GitHub Secrets or Environment variables."