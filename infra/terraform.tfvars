/*
  Purpose: Specifies the geographical location where cloud resources (e.g., virtual machines, databases) will be deployed.
  Considerations: Factors like network latency, data residency regulations, and cost may influence region selection.
*/
#region = "europe-west9"

/*
  Purpose: Adds metadata to resources, aiding in organization and filtering.
  Common uses: Distinguishing environments (development, staging, production), tracking costs, or assigning ownership.
*/
resource_labels = {
  env = "sandbox"
}