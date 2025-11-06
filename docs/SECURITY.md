# Security & Ethical Guidance

This lab is intentionally vulnerable. Follow these rules to avoid accidental mayhem.

## Deployment isolation
- Deploy the lab in a dedicated GCP project with billing alerts and a budget cap.
- Label the project clearly: `name: cloudgoat-gcp`, `env: intentionally-vulnerable`.

## Secrets & credentials
- Never commit secrets. Use GitHub Secrets for CI and Secret Manager for runtime secrets.
- Terraform state: store remote state in a secure backend (e.g., GCS with restricted ACLs).

## Network controls
- Apply NetworkPolicies to limit challenge pod egress.
- Use Cloud Armor or HTTP(S) load balancer rules if you must restrict inbound traffic to trusted IPs.

## Responsible usage
- This environment is for controlled learning. Do not connect it to production systems.
- If you find an accidental data leak or credential exposure, notify maintainers immediately (see `MAINTAINERS.md`).

## Teardown
- Provide `scripts/teardown.sh` that safely runs `terraform destroy` and removes cloud resources.
- Document expected monthly cost and recommended minimum billing alerts.

