terraform {
  cloud {

    organization = "Kestra-ELT-Pipeline"

    workspaces {
      name = "main"
    }
  }

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.19.0"
    }
  }
}

provider "google" {
  project     = var.gcp_project_id
  region      = "us-central1"
  credentials = var.gcp_creds
}

# Create a GCS bucket for the Kestra ELT pipeline
resource "google_storage_bucket" "landing_bucket" {
  name     = "kestra_landing_bucket_1234567890"
  location = "us-central1"

  lifecycle_rule {
    condition {
      age = 7
    }
    action {
      type = "Delete"
    }
  }
}

# Create a BigQuery dataset for landing data
resource "google_bigquery_dataset" "landing_dataset" {
  dataset_id = "landing_dataset"
  location   = "us-central1"
}

# Create a BigQuery table for landing Location data
resource "google_bigquery_table" "location_table" {
  dataset_id = google_bigquery_dataset.landing_dataset.dataset_id
  table_id   = "location_table"
  schema     = file("${path.module}/bq_table_schemas/location.json")
}

# Create a BigQuery table for landing Episode data
resource "google_bigquery_table" "episode_table" {
  dataset_id = google_bigquery_dataset.landing_dataset.dataset_id
  table_id   = "episode_table"
  schema     = file("${path.module}/bq_table_schemas/episode.json")
}

# Create a BigQuery table for landing Character data
resource "google_bigquery_table" "character_table" {
  dataset_id = google_bigquery_dataset.landing_dataset.dataset_id
  table_id   = "character_table"
  schema     = file("${path.module}/bq_table_schemas/character.json")
}
