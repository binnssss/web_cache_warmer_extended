import os
import csv
import sys
import requests

def cache_warmer(csv_file_path, base_url):
    if not base_url:
        print("Error: BASE_URL environment variable is not provided.")
        print("Please run the Docker container with '-e BASE_URL=https://your_site.com' argument")
        print("docker run -e BASE_URL=https://your_site.com -v /csv/urls.csv:/app/urls.csv cache-warmer")
        sys.exit(1)

    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            for url in row:
                if url.strip():
                    full_url = base_url + url.strip()
                    if url == '/':
                        full_url = base_url
                    try:
                        response = requests.get(full_url)
                        # Raise an exception for non-200 status codes
                        response.raise_for_status()
                        print(f"Successfully warmed up {full_url}")
                    except requests.exceptions.RequestException as e:
                        print(f"Failed to warmup {full_url}. Error: {str(e)}")

if __name__ == "__main__":
    csv_file_path = 'urls.csv'
    base_url = os.environ.get('BASE_URL')
    cache_warmer(csv_file_path, base_url)

