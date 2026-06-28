#!/bin/sh

set -o allexport; source ./.env; set +o allexport

curl https://openrouter.ai/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENROUTER_APIKEY" \
  -d '{
  "model": "cohere/north-mini-code:free",
  "messages": [
    {
      "role": "user",
      "content": "What is the meaning of life?"
    }
  ]
}'

