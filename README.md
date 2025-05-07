[![Codacy Badge](https://api.codacy.com/project/badge/Grade/f34108759f0b47efb917df47d2e2d177)](https://app.codacy.com/gh/Viktor-Soltesz/salary-survey-iac/dashboard)
[![Codacy Coverage Badge](https://api.codacy.com/project/badge/Coverage/f34108759f0b47efb917df47d2e2d177)](https://app.codacy.com/gh/Viktor-Soltesz/salary-survey-iac/dashboard)

# End-to-End ELT Pipeline: Software developer salary survey

*An automated journey: from raw CSV to BigQuery to Tableau*

**GOAL:** Showcase Data Analytics, ELT, CI/CD, testing, and cloud engineering skills in an end-to-end project.

## Pipeline Overview

Survey data (.csv) → GCP Infrastructure-as-Code → BigQuery + DBT → Tableau Dashboard

## Project Structure

### 1. Infrastructure & CI/CD

- GitHub Actions deploys IaC:
  - Terraform + Python-based GCP Cloud Functions are the backbone.
  - **Python checks:** pip-audit, linting, type checks, unit & integration tests, code quality, coverage badge.
  - **Terraform checks:** detect state changes, init, plan, apply.

### 2. Data Input

- Raw salary survey data (.csv).
- GitHub Actions:
  - Uploads to Google Cloud Storage (GCS),
  - Validates format & schema,
  - Runs basic data checks.
- Successful upload triggers Python-based extract & transform.

### 3. Transform (Cloud Functions & Python)

- Extract data from GCS → process with `pandas`:
  - Correct typos, discard nulls, standardize entries.
- Unit and integration tested.

### 4. Load

- BigQuery tables
- Archive bucket

### 5. DBT Transformations (BigQuery)

- GitHub Actions builds the models, runs tests:
  - Categorizing free-text inputs.
  - Enriching with seed data (GDP, inflation, etc).
  - Flagging outliers, normalize values.
  - Loading into marts (cleaned + aggregated).
  - Tracking data quality metrics.

### 6. Visualization

- Tableau dashboard via direct BigQuery connection.

---

## Related Resources

- Statistical analysis and Predictive modeling repo: [salary_analysis](https://github.com/Viktor-Soltesz/salary_analysis)
- Dashboard (Tableau Public): [Software Developer Salaries](https://public.tableau.com/app/profile/viktor.solt.sz/viz/SoftwareDeveloperSalaries/Dashboard)

<br>
<br>
<br>
<br>

# Setup & Deployment

## **1: Prerequisites**

- **Google Cloud SDK** installed (`gcloud`)
- **Terraform** installed (`terraform -v`)
- **GitHub Actions** configured with GCP credentials

## **2: Run Initial Setup**

1. **Manually create a GCP project & enable billing**
2. **Run `prereq.sh`** to:
    - Enable required GCP APIs
    - Create a Terraform service account
    - Grant necessary IAM roles
3. **Manually generate & store credentials in GitHub Secrets**

## 3. **Run GitHub Actions workflows**

 - `terraform_deploy.yaml` - to deploy infrastructure with Terraform,
 - `upload_csv_to_bucket.yaml` - to run the csv through GCP into BigQuery,
 - `dbt_run.yaml` - to run the Transformation layer with DBT.

  That's it! Everything else is taken care of by GitHub Actions.