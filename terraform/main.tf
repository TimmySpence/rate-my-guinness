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
}

resource "google_container_node_pool" "default" {
  count    = 0 # No node pools for autopilot
}