#!/bin/bash

BASE_URL=$1

if [[ -z "$BASE_URL" ]]; then
  echo "Error: Please provide a BASE_URL as an argument in the format https://your_site.com/"
  exit 1
fi

docker run --name web-cache-warmer -e BASE_URL="$BASE_URL" -v $(pwd)/csv/urls.csv:/app/urls.csv cache-warmer
docker rm web-cache-warmer

