terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 5.0"
    }
  }
  required_version = ">= 1.3.0"
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_container_cluster" "autopilot" {
  name     = "guinness-autopilot"
  location = var.region
  enable_autopilot = true
  deletion_protection = false
}


# Configure Kubernetes provider using GKE credentials (with alias)
provider "kubernetes" {
  alias                  = "gke"
  host                   = google_container_cluster.autopilot.endpoint
  token                  = data.google_client_config.default.access_token
  cluster_ca_certificate = base64decode(google_container_cluster.autopilot.master_auth[0].cluster_ca_certificate)
}

# Get GCP credentials for Kubernetes provider
data "google_client_config" "default" {}


# Helm provider
provider "helm" {}

# Deploy Helm chart
resource "helm_release" "rate_my_guinness" {
  name       = "rate-my-guinness"
  chart      = "../chart"
  namespace  = "default"
  dependency_update = true

  depends_on = [google_container_cluster.autopilot]
}
