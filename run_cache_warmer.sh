#!/bin/bash

BASE_URL=$1
USER_AGENT=$2
current_date=$(date +"%Y_%m_%d")

if [[ -z "$BASE_URL" ]]; then
  echo "Error: Please provide a BASE_URL as the first argument in the format https://your_site.com/"
  exit 1
fi

# Pass in Chrome user agent if nothing is passed in.
if [[ -z "$USER_AGENT" ]]; then
  USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
fi

docker run -it --name cache-warmer -e BASE_URL="$BASE_URL" -e USER_AGENT="$USER_AGENT" -v $(pwd)/csv/urls.csv:/app/urls.csv cache-warmer
docker cp cache-warmer:URL_reports.csv ~/
docker rm cache-warmer