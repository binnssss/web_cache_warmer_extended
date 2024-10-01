#!/bin/bash

BASE_URL=$1
USER_AGENT=$2


if [[ -z "$BASE_URL" ]]; then
  echo "Error: Please provide a BASE_URL as the first argument in the format https://your_site.com/"
  exit 1
fi

# Pass in Chrome user agent if nothing is passed in.
if [[ -z "$USER_AGENT" ]]; then
  USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
fi

docker run -it --name cache-warmer -e BASE_URL="$BASE_URL" -e USER_AGENT="$USER_AGENT" -v $(pwd)/cache_warmer/csv/urls.csv:/app/urls.csv cache-warmer

docker cp cache-warmer:/output .

docker rm cache-warmer