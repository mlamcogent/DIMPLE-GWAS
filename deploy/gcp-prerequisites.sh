#!/usr/bin/env bash
# Owner-operated setup only. No workflow invokes this script.
set -euo pipefail
[[ "${1:-}" == --apply ]] || { echo 'Review DEPLOY_GCP.md, then pass --apply.' >&2; exit 2; }
: "${PROJECT:?Set PROJECT to your GCP project ID}"
REGION="${REGION:-asia-southeast1}"
: "${BUCKET:?Set BUCKET to your existing GCS bucket name}"
REPOSITORY="${REPOSITORY:-dimple}"
SA="dimple-batch-sa@${PROJECT}.iam.gserviceaccount.com"
# Owner runs this only after review; reuse existing account and bucket, never create replacements.
gcloud services enable batch.googleapis.com artifactregistry.googleapis.com iam.googleapis.com --project="$PROJECT"
gcloud services list --enabled --project="$PROJECT" --format='value(config.name)'
gcloud iam service-accounts describe "$SA" --project="$PROJECT" >/dev/null
for role in roles/batch.agentReporter roles/logging.logWriter; do
  gcloud projects add-iam-policy-binding "$PROJECT" --member="serviceAccount:$SA" --role="$role" --condition=None
 done
# Refuse a bucket belonging to another project/location before altering its policy.
PN="$(gcloud projects describe "$PROJECT" --format='value(projectNumber)')"
[[ "$(gcloud storage buckets describe "gs://$BUCKET" --format='value(project_number)')" == "$PN" ]]
LOC="$(gcloud storage buckets describe "gs://$BUCKET" --format='value(location)')"
[[ "$(printf %s "$LOC" | tr '[:upper:]' '[:lower:]')" == "$REGION" ]]
# Existing lifecycle, uniform-access and public-access settings are not modified.
gcloud storage buckets add-iam-policy-binding "gs://$BUCKET" --member="serviceAccount:$SA" --role=roles/storage.objectAdmin --project="$PROJECT"
if ! gcloud artifacts repositories describe "$REPOSITORY" --location="$REGION" --project="$PROJECT" >/dev/null 2>&1; then
  gcloud artifacts repositories create "$REPOSITORY" --repository-format=docker --location="$REGION" --project="$PROJECT"
fi
gcloud artifacts repositories add-iam-policy-binding "$REPOSITORY" --location="$REGION" --project="$PROJECT" \
  --member="serviceAccount:$SA" --role=roles/artifactregistry.reader
# No public IPs on workers; PGA provides Google APIs/GCS/Artifact Registry, not general internet.
gcloud compute networks subnets update default --region="$REGION" --project="$PROJECT" --enable-private-ip-google-access
[[ "$(gcloud compute networks subnets describe default --region="$REGION" --project="$PROJECT" --format='value(privateIpGoogleAccess)')" == True ]]
gcloud iam service-accounts get-iam-policy "$SA" --project="$PROJECT"
gcloud storage buckets get-iam-policy "gs://$BUCKET" --project="$PROJECT"
gcloud artifacts repositories get-iam-policy "$REPOSITORY" --location="$REGION" --project="$PROJECT"
printf 'Configured project=%s region=%s worker=%s bucket=%s\n' "$PROJECT" "$REGION" "$SA" "$BUCKET"
