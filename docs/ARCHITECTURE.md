# Architecture — CloudGoat-GCP (skeleton)

## Goals
- Reproducible GCP lab deployed with Terraform and Kubernetes (GKE).
- Clear separation: `portal` (public UI) and `challenges` (namespaced workloads).
- Minimal public attack surface; challenge exposure only when required by objective.

## High-level diagram (text)
- Terraform -> provisions: GCP Project (or uses provided), VPC, GKE cluster, Artifact Registry, static IP.
- GKE -> namespaces:
  - `portal`: React frontend + backend API (flag validation + leaderboard).
  - `challenges`: one or more namespaces containing challenge services.
- Ingress -> load-balances traffic to portal; challenge routes exposed selectively.
- Secrets -> stored in Secret Manager and mounted by backend during deploy.
- CI/CD -> GitHub Actions or Cloud Build to build images and apply manifests.

## Network & isolation
- Use Kubernetes NetworkPolicies per challenge to restrict egress/ingress.
- Default deny egress for challenge pods where applicable.
- Restrict GCP IAM service accounts used by cluster to least privilege.

## Flag lifecycle
- Flags generated or seeded at deploy time; stored only in Secret Manager.
- Backend validates flags via HMAC or lookup; never commit plaintext flags.

## Notes
- For grading reproducibility: include `deploy.sh` wrapper that runs `terraform apply`, builds images, and applies k8s manifests in correct order.
