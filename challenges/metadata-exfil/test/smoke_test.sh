#!/usr/bin/env bash
set -euo pipefail

# Usage:
# ./smoke_test.sh --project <PROJECT> --zone <ZONE> --vm <VM_NAME>

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project) PROJECT="$2"; shift 2;;
    --zone) ZONE="$2"; shift 2;;
    --vm) VM="$2"; shift 2;;
    *) echo "Unknown arg: $1"; exit 1;;
  esac
done

: "${PROJECT:?Need --project}"
: "${ZONE:?Need --zone}"
: "${VM:?Need --vm}"

echo "[*] Running smoke test on VM ${VM} in ${PROJECT}/${ZONE}"

TOKEN_JSON=$(gcloud compute ssh --project "$PROJECT" --zone "$ZONE" "$VM" --command \
  "curl -s -H 'Metadata-Flavor: Google' 'http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token'")

echo "[*] Token JSON: $TOKEN_JSON"

ACCESS_TOKEN=$(echo "$TOKEN_JSON" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
if [[ -z "$ACCESS_TOKEN" ]]; then
  echo "[-] Could not extract access_token"
  exit 2
fi
echo "[*] Extracted token (truncated): ${ACCESS_TOKEN:0:20}..."

RESPONSE=$(gcloud compute ssh --project "$PROJECT" --zone "$ZONE" "$VM" --command \
  "curl -s -H 'Authorization: Bearer $ACCESS_TOKEN' http://127.0.0.1:8080/api/flag || true")

echo "[*] API response: $RESPONSE"

if echo "$RESPONSE" | grep -q "FLAG{"; then
  echo "[+] Smoke test succeeded. Flag returned:"
  echo "$RESPONSE" | sed -n 's/.*\\(\"flag\": \"\\(FLAG{[^}]*}\\)\"\\).*/\\2/p'
  exit 0
else
  echo "[-] Smoke test failed. Response did not contain flag."
  exit 3
fi
