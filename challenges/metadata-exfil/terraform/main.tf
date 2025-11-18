terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.0"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

resource "random_id" "lab" {
  byte_length = 4
}

# Service account for the vulnerable VM
resource "google_service_account" "metadata_exfil_sa" {
  account_id   = "metadata-exfil-sa-${random_id.lab.hex}"
  display_name = "Metadata Exfiltration Lab SA"
}

# Intentional over-permission for lab purposes.
resource "google_project_iam_binding" "sa_binding" {
  project = var.project_id
  role    = "roles/storage.admin"
  members = [
    "serviceAccount:${google_service_account.metadata_exfil_sa.email}"
  ]
}

# Firewall rule to allow SSH
resource "google_compute_firewall" "allow_ssh" {
  name    = "allow-ssh-cloudgoat-metadata-exfil-${random_id.lab.hex}"
  network = var.network

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["cloudgoat-metadata-exfil-${random_id.lab.hex}"]
}

data "template_file" "startup" {
  template = file("${path.module}/startup.tpl")
  vars = {
    flag_value = "FLAG{metadata-exfil-${random_id.lab.hex}}"
  }
}

# Compute instance
resource "google_compute_instance" "vm" {
  name         = var.vm_name
  machine_type = var.machine_type
  zone         = var.zone

  tags = ["cloudgoat-metadata-exfil-${random_id.lab.hex}"]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-12"
      size  = 20
    }
  }

  network_interface {
    network = var.network
    access_config { } # Ephemeral external IP
  }

  metadata = {
    ssh-keys = var.ssh_public_key
  }

  service_account {
    email  = google_service_account.metadata_exfil_sa.email
    scopes = ["https://www.googleapis.com/auth/cloud-platform"]
  }

  metadata_startup_script = data.template_file.startup.rendered
}

output "vm_name" {
  value = google_compute_instance.vm.name
}

output "vm_external_ip" {
  value = google_compute_instance.vm.network_interface[0].access_config[0].nat_ip
}

output "service_account_email" {
  value = google_service_account.metadata_exfil_sa.email
}
