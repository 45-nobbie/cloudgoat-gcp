# Challenge: Metadata API Secret Exfiltration

## Summary
This lab demonstrates how a compute instance's metadata server can leak an OAuth access token for its attached service account. The token can be used to call protected internal APIs or Google APIs that the service account is allowed to access.

## Learning objectives
- Query the GCP metadata server to obtain service account tokens.
- Use tokens to access protected resources.
- Understand why least-privilege and Workload Identity matter.

## High-level flow
1. SSH into the provided GCE VM (credentials/output provided by Terraform).
2. Retrieve the access token from the metadata endpoint:
   ```bash
   curl -H "Metadata-Flavor: Google" \
     "http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token"
