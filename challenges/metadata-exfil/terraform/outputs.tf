output "vm_name" {
  description = "Name of the created VM"
  value       = google_compute_instance.vm.name
}

output "external_ip" {
  description = "External IP of the VM"
  value       = google_compute_instance.vm.network_interface[0].access_config[0].nat_ip
}

output "service_account_email" {
  description = "Email of the service account attached to the VM"
  value       = google_service_account.metadata_exfil_sa.email
}
