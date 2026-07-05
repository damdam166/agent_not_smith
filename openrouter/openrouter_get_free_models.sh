#!/bin/sh

curl -s https://openrouter.ai/api/v1/models | jq '.data[] | select(.pricing.prompt == "0" and .pricing.completion == "0") | {id, name, context_length}'

