#!/bin/bash

BASE_URL=$1
USER_AGENT=$2

# Check if .env file exists
if [[ ! -f ".env" ]]; then
  echo "Warning: .env file not found. Proceeding without environment variables from .env file."
  ENV_FILE_OPTION=""
else
  echo ".env file found. Loading environment variables from .env file."
  ENV_FILE_OPTION="--env-file .env"
fi

if [[ -z "$BASE_URL" ]]; then
  echo "Error: Please provide a BASE_URL as the first argument in the format https://your_site.com/"
  exit 1
fi

# Pass in Chrome user agent if nothing is passed in.
if [[ -z "$USER_AGENT" ]]; then
  USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
fi

docker run -it --name cache-warmer -e BASE_URL="$BASE_URL" -e USER_AGENT="$USER_AGENT" $ENV_FILE_OPTION -v $(pwd)/app/csv/urls.csv:/app/urls.csv cache-warmer

docker cp cache-warmer:/output . 2>/dev/null

docker rm cache-warmer