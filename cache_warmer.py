import os
import csv
import sys
import requests
from multiprocessing import Pool

class HttpClient:
    def get(self, url, headers=None):
        return requests.get(url, headers=headers)

class CacheWarmer:
    def __init__(self, http_client, user_agent=None):
        self.http_client = http_client
        self.user_agent = user_agent

    def warm_up_cache(self, csv_file_path, base_url):
        if not base_url:
            raise ValueError("Error: BASE_URL environment variable is not provided.")

        with open(csv_file_path, 'r', errors='ignore') as file:
            reader = csv.reader(file)
            urls = [row[0].strip() for row in reader]

        num_processes = os.cpu_count() or 1

        with Pool(num_processes) as pool:
            pool.map(self._warm_up_url, [(base_url + url if url != '/' else base_url) for url in urls])

    def _warm_up_url(self, url):
        try:
            headers = {'User-Agent': self.user_agent} if self.user_agent else None
            response = self.http_client.get(url, headers=headers)
            if response.status_code == 200:
                print(f"Successfully warmed up {url}")
            else:
                raise requests.exceptions.HTTPError(f"Failed to warm up {url}. HTTP status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to warm up {url}. Error: {str(e)}")

if __name__ == "__main__":
    base_url = os.environ.get('BASE_URL')
    user_agent = os.environ.get('USER_AGENT')

    if not base_url:
        print("Error: BASE_URL environment variable is not provided.")
        print("Please run the script with 'BASE_URL' environment variable set.")
        sys.exit(1)

    if not user_agent:
        user_agent = input("Please enter the user agent: ")

    csv_file_path = 'urls.csv'
    http_client = HttpClient()
    cache_warmer = CacheWarmer(http_client, user_agent=user_agent)
    cache_warmer.warm_up_cache(csv_file_path, base_url)
