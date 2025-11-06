# Terraform module (skeleton)

This folder will contain Terraform configs that provision the GCP environment.

## Variables to set before deploy
- `project_id` (required)
- `region` (default: us-central1)
- `zone` (default: us-central1-a)

## Typical flow
```bash
cd terraform
terraform init
terraform plan -var="project_id=<PROJECT_ID>"
terraform apply -var="project_id=<PROJECT_ID>"
