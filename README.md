# Salary Survey Infrastructure as Code (IaC)

This repository contains the **Terraform-based Infrastructure as Code (IaC)** setup for the **Salary Survey Data Pipeline** on **Google Cloud Platform (GCP)**.

## Overview
This project automates the provisioning of cloud resources needed for a **data analytics pipeline**, using:
- **Terraform** for infrastructure management
- **Google Cloud Build & GitHub Actions** for CI/CD
- **Cloud Functions, BigQuery, and Cloud Storage** for event-driven data processing

## Workflow
1. **Manually create a GCP project & enable billing**
2. **Run `prereq.sh`** to:
   - Enable required GCP APIs
   - Create a Terraform service account
   - Grant necessary IAM roles
3. **Manually generate & store credentials in GitHub Secrets**
4. **Run GitHub Actions workflow** to deploy infrastructure with Terraform

## 📂 Project Structure
├── infra/ # Terraform configurations
│ ├── provider.tf # GCP provider setup 
│ ├── iam.tf # IAM role assignments
│ ├── function.tf # Cloud Function deployment
│ ├── gcs.tf # Storage bucket definitions
│ ├── variables.tf # Terraform variables 
├── .github/workflows/ # CI/CD workflows for Terraform deployment 
├── prereq.sh # Shell script to set up initial IAM & APIs 
└── README.md # Project documentation


## Setup & Deployment
### **1️⃣ Prerequisites**
- **Google Cloud SDK** installed (`gcloud`)
- **Terraform** installed (`terraform -v`)
- **GitHub Actions** configured with GCP credentials

### **2️⃣ Run Initial Setup**
bash prereq.sh
