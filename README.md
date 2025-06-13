[![Codacy Badge](https://api.codacy.com/project/badge/Grade/f34108759f0b47efb917df47d2e2d177)](https://app.codacy.com/gh/Viktor-Soltesz/salary-survey-iac/dashboard)
[![Codacy Coverage Badge](https://api.codacy.com/project/badge/Coverage/f34108759f0b47efb917df47d2e2d177)](https://app.codacy.com/gh/Viktor-Soltesz/salary-survey-iac/dashboard)

# Ingestion & Infrastructure (Stage 1 of 5)

This repository sets up the GCP infrastructure and implements the ETL pipeline to process raw, free-text salary survey data. It uses Terraform to define infrastructure, Python Cloud Functions for data transformation, and GitHub Actions for automation.  
It is part of a broader, modular data stack designed for salary analysis and insight generation from global developer survey responses.

---

## Project Overview

This project is split into modular repositories, each handling one part of the full ELT and analytics pipeline:

| Stage | Name                        | Description                                | Link |
|-------|-----------------------------|--------------------------------------------|------------|
| **▶️1** | **Ingestion & Infrastructure**  | **Terraform + Python Cloud Functions** | **[salary-survey-iac (GitHub)](https://github.com/Viktor-Soltesz/salary-survey-iac)** |
| ㅤ2     | Data Transformation   | DBT data models and testing               | [salary-survey-dbt (GitHub)](https://github.com/Viktor-Soltesz/salary-survey-dbt) <br> ㅤ⤷ [DBT docs](https://viktor-soltesz.github.io/salary-survey-dbt-docs/index.html#!/overview)|
| ㅤ3     | Data Observability  | Great Expectations & Elementary, <br> model monitoring and data observability     | [salary-survey-gx (GitHub)](https://github.com/Viktor-Soltesz/salary-survey-gx) <br> ㅤ⤷ [GX log](https://viktor-soltesz.github.io/salary-survey-gx/gx_site/index.html) <br> ㅤ⤷ [Elementary report](https://viktor-soltesz.github.io/salary-survey-dbt/elementary_report.html#/report/dashboard) |
| ㅤ4     | Statistical Modeling    | ANOVA, multiregressions, prediction   | [salary-survey-analysis (GitHub)](https://github.com/Viktor-Soltesz/salary-survey-analysis) |
| ㅤ5     | Dashboards          | •ㅤInteractive salary exploration <br> •ㅤData Health metrics, gathered during runs <br> •ㅤBilling report, live export from GCP <br> •ㅤBigQuery report, from GCP logging |ㅤ🡢 [Tableau Public](https://public.tableau.com/app/profile/viktor.solt.sz/viz/SoftwareDeveloperSalaries/Dashboard) <br>ㅤ🡢 [Looker Studio](https://lookerstudio.google.com/s/mhwL6JfNlaw)<br>ㅤ🡢 [Looker Studio](https://lookerstudio.google.com/s/tp8jUo4oPRs)<br>ㅤ🡢 [Looker Studio](https://lookerstudio.google.com/s/v2BIFW-_Jak)|
| ㅤ+     | Extra material | •ㅤPresentation <br> •ㅤData Dictionary <br>  •ㅤSLA Table <br>  •ㅤMy LinkedIn<br>  •ㅤMy CV|ㅤ🡢 [Google Slides](https://docs.google.com/presentation/d/1BHC6QnSpObVpulEcyDLXkW-6YLo2hpnwQ3miQg43iBg/edit?slide=id.g3353e8463a7_0_28#slide=id.g3353e8463a7_0_28) <br>ㅤ🡢 [Google Sheets](https://docs.google.com/spreadsheets/d/1cTikHNzcw3e-gH3N8F4VX-viYlCeLbm5JkFE3Wdcnjo/edit?gid=0#gid=0) <br>ㅤ🡢 [Google Sheets](https://docs.google.com/spreadsheets/d/1r85NlwsGV1DDy4eRBfMjZgI-1_uyIbl1fUazgY00Kz0/edit?usp=sharing) <br>ㅤ🡢 [LinkedIn](https://www.linkedin.com/in/viktor-soltesz/) <br>ㅤ🡢 [Google Docs](https://www.linkedin.com/in/viktor-soltesz/)|

---

## Repository Scope

This repository handles:
- **Infrastructure setup** using Terraform
- **CSV ingestion and validation** via GitHub Actions
- **ETL pipeline** using modular Python Cloud Functions
- **CI/CD workflows** for infrastructure and data logic
- **Unit and integration testing** for transformation steps

The goal is to reliably ingest messy CSVs, apply standardized cleaning steps, and load the transformed results into BigQuery — all reproducibly and securely.

---
---

# Detailed Breakdown

### 1. Infrastructure (Terraform)

Defines and deploys:
- GCS buckets: `raw`, `archive`, `temp`
- BigQuery datasets for staging and processing
- Cloud Function for ETL
- IAM roles and service accounts (least privilege)

**Deployed via GitHub Actions**:
- Detects changes in state bucket
- Runs `terraform init`, `plan`, `apply`

---

### 2. Data Upload & Validation (GitHub Actions)

- Uploads raw CSV files to GCS
- Validates:
  - File format (CSV)
  - Column names and types
  - Basic sanity checks (nulls, date ranges, invalid values)
- Triggers Cloud Function on success

---

### 3. ETL Logic (Python Cloud Functions)

- **Extract**: Loads file into memory using `pandas`
- **Transform**:
  - Standardizes column names
  - Applies typo corrections and type coercions
  - Drops or flags invalid entries
  - All transformations are modular and composable (each `df -> df`)
- **Load**:
  - Outputs final DataFrame to BigQuery
  - Saves cleaned file to archive bucket

Testing:
- **Unit tests**: Each transform step
- **Integration test**: Entire pipeline with edge-case data

---

### 4. CI/CD Pipeline (GitHub Actions)

**Python pipeline:**
- `pip-audit` security checks
- Code linting and formatting
- Static type checks (`mypy`)
- Unit and integration tests
- Code coverage badge

**Terraform pipeline:**
- Plan/apply with safety checks
- Output diff and status reporting

---
---

# Deployment Instructions

## Prerequisites

- GCP project with billing enabled
- gcloud CLI installed and authenticated
- Terraform CLI (>= 1.3.9) installed
- GitHub account with access to this repository

## Step 1: Set Up GCP Resources

Run the following script to configure your project:

```
bash prereq.sh
```

This will:
- Prompt for your PROJECT_ID
- Create a Terraform state bucket: PROJECT_ID-tf-state
- Enable required APIs
- Create the terraform-sa service account and assign necessary roles

## Step 2: Prepare GitHub Secrets

1. In GCP Console, create a key for terraform-sa
2. Copy the contents of the JSON key and add it as a GitHub Secret named GOOGLE_CREDENTIALS
3. In repository settings, add the following variables or secrets:
    - PROJECT_ID
    - TERRAFORM_SERVICE_ACCOUNT_EMAIL (e.g., terraform-sa@PROJECT_ID.iam.gserviceaccount.com)

## Step 3: Deploy via GitHub Actions

1. Navigate to the Actions tab in GitHub
2. Select Deploy Infrastructure
3. Click Run workflow to start the deployment

The workflow will:
- Run Python code checks and tests
- Initialize and apply Terraform infrastructure
- Import existing GCP resources into state if needed
- Optionally notify Slack on success or failure (requires SLACK_WEBHOOK secret)

## Result

The deployment provisions:
- GCS buckets for function source, uploads, and archive
- Cloud Functions and Pub/Sub triggers
- BigQuery datasets and tables
The infrastructure is fully managed through Terraform and CI/CD pipelines.