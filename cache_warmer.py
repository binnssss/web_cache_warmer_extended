import os
import csv
import sys
import requests

class HttpClient:
    def get(self, url):
        return requests.get(url)

class CacheWarmer:
    def __init__(self, http_client):
        self.http_client = http_client

    def warm_up_cache(self, csv_file_path, base_url):
        if not base_url:
            raise ValueError("Error: BASE_URL environment variable is not provided.")

        with open(csv_file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                self._warm_up_urls(row, base_url)

    def _warm_up_urls(self, urls, base_url):
        for url in urls:
            url = url.strip()
            if url:
                full_url = base_url + url if url != '/' else base_url
                self._warm_up_url(full_url)

    def _warm_up_url(self, url):
        try:
            response = self.http_client.get(url)
            if response.status_code == 200:
                print(f"Successfully warmed up {url}")
            else:
                raise requests.exceptions.HTTPError(f"Failed to warm up {url}. HTTP status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to warm up {url}. Error: {str(e)}")


if __name__ == "__main__":
    base_url = os.environ.get('BASE_URL')
    if not base_url:
        print("Error: BASE_URL environment variable is not provided.")
        print("Please run the script with 'BASE_URL' environment variable set.")
        sys.exit(1)

    csv_file_path = 'urls.csv'
    http_client = HttpClient()
    cache_warmer = CacheWarmer(http_client)
    cache_warmer.warm_up_cache(csv_file_path, base_url)