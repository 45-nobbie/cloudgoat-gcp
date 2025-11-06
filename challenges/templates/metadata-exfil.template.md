# Challenge: Metadata API Secret Exfiltration (template)

## Short description
A VM or service-account-enabled workload reveals a token via the compute metadata API. Use the token to access an internal service that returns the flag.

## Learning objectives
- Understand GCP metadata API and how to retrieve instance/service account tokens.
- Use stolen tokens to call internal APIs and list or read sensitive resources.
- Appreciate least-privilege and the principle of narrow IAM bindings.

## Setup notes (for implementer)
- Deploy a workload (Cloud Run or GCE instance) with an attached service account that has excessive permissions (e.g., roles/storage.admin).
- Expose a challenge backend that only returns the flag when called with an Authorization: Bearer <valid-token> header.

## Flag format
`FLAG{metadata-exfil-<random-suffix>}`

## Hints (tiered)
1. Hint 1: The metadata server is reachable at http://169.254.169.254/
2. Hint 2: `curl "http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token" -H "Metadata-Flavor: Google"`
3. Hint 3: Use the token in `Authorization: Bearer <token>` to call the internal challenge endpoint.

## Verification
- Test script should simulate token retrieval and call the protected endpoint, returning the expected flag.

