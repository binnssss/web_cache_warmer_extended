import datetime
import os
import csv
import sys
import requests
from multiprocessing import Pool
from io import StringIO

class HttpClient:
    def get(self, url, headers=None):
        return requests.get(url, headers=headers)

class CacheWarmer:
    def __init__(self, http_client, user_agent=None):
        self.http_client = http_client
        self.user_agent = user_agent
        self.csv_buffer = StringIO()
        self.data = []

    def warm_up_cache(self, csv_file_path, base_url):
        if not base_url:
            raise ValueError("Error: BASE_URL environment variable is not provided.")
        
        with open(csv_file_path, 'r', errors='ignore') as file:
            reader = csv.DictReader(file)
            urls = [row['New URL'].strip() for row in reader]

        num_processes = os.cpu_count() or 1

        with Pool(num_processes) as pool:
            results = pool.map(self.warm_up_urls, [(url if url.startswith('http://') or url.startswith('https://') 
                else (base_url + url if url != '/' else base_url)) 
                    for url in urls])
            
        # print(results)
        self.data.extend(results)

    def warm_up_urls(self, url):
        try:
            headers = {'User-Agent': self.user_agent} if self.user_agent else None
            response = self.http_client.get(url, headers=headers)
            if response.status_code == 200:
                code = response.status_code
                message = "OK"
                print(f"Status {message} [{code}]: {url}")
            else:
                code = response.status_code
                message = "FAILED"
                raise requests.exceptions.HTTPError(f"Status {message} [{code}]: {url}")
        except requests.exceptions.RequestException as e:
            print(f"Status {message} [{response.status_code}]: {url}")
            result = {'url': url, 'code': response.status_code}
            return result

    def write_result_to_csv(self, filename=None):
        """Writes the results stored in self.results to a CSV file."""
        if filename is None:
            current_date = datetime.datetime.now().strftime("%Y_%m_%d")
            filename = f'report_{current_date}.csv'

        if os.path.dirname(filename):
            os.makedirs(os.path.dirname(filename), exist_ok=True)
 
        with open(filename, mode='w', newline='') as file:
            fieldnames = ['url', 'code', 'status']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.data)

        print(f"Report saved as {filename}")   

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
    generate = input(f"Do you want to generate a report? (Yes/No): ")

    current_date = datetime.datetime.now().strftime("%Y_%m_%d")
    filename = f'/report_{current_date}.csv'
    
    if generate.lower() in ('yes', 'y'):
        cache_warmer.warm_up_cache(csv_file_path, base_url)
        save_report = input("Do you want to save the report? (Yes/No): ")
        current_directory = "~/"
        
        if save_report.lower() in ('yes', 'y'):
            os.environ['FILENAME'] = filename
            cache_warmer.write_result_to_csv(filename)
        else:
            print("Report generated but not saved.")
    else:
        print("Exiting without generating a report.")
        sys.exit(0)
