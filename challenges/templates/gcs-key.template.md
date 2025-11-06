# Challenge: Public GCS Service Account Key

## Short description
A service account JSON key was accidentally uploaded to a public GCS bucket. Download the key, authenticate with `gcloud` or client libraries, and call a protected service to retrieve the flag.

## Learning objectives
- Identify public buckets and find sensitive objects.
- Understand how service account keys allow programmatic access and why they are dangerous.
- Learn mitigation: IAM restrictions, key rotation, and avoiding embedding keys in buckets.

## Setup notes
- Create a purposely public or misconfigured GCS bucket and upload a limited-use service account JSON.
- Create a small backend that returns a flag only when accessed using credentials derived from that key.

## Flag format
`FLAG{gcs-key-<random-suffix>}`

## Hints (tiered)
1. Hint 1: Public GCS buckets often have objects listed at `https://storage.googleapis.com/<bucket>`.
2. Hint 2: The service account key is a JSON file; use `gsutil` or curl to download it.
3. Hint 3: Authenticate locally `gcloud auth activate-service-account --key-file=key.json` then call the challenge endpoint.

## Verification
- Include a test script that uses the downloaded key to call the endpoint and fetch the flag.

