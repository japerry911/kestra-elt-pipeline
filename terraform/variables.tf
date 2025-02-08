variable "gcp_project_id" {
  type        = string
  sensitive   = true
  description = "The GCP project ID"
}

variable "gcp_creds" {
  type        = string
  sensitive   = true
  description = "The GCP credentials"
}
