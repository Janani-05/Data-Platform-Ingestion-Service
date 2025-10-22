
# terraform/main.tf
provider "google" {
  project = "your-gcp-project-id"
  region  = "us-central1"
}

resource "google_storage_bucket" "uploads" {
  name     = "your-project-uploads"
  location = "US"
}

resource "google_cloudfunctions_function" "gcs_to_bq" {
  name        = "gcs-to-bq-ingestor"
  runtime     = "python310"
  entry_point = "gcs_to_bq_ingestor"
  source_archive_bucket = google_storage_bucket.uploads.name
  trigger_http = true
}

output "bucket_name" {
  value = google_storage_bucket.uploads.name
}

