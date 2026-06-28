#!/bin/sh

set -o allexport; source ./.env; set +o allexport

curl -s "https://openrouter.ai/api/v1/credits" \
  -H "Authorization: Bearer $OPENROUTER_APIKEY" \
  | jq '.data'

