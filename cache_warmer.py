import datetime
import time
import os
import csv
import sys
import requests
import tempfile
from multiprocessing import Pool
from requests.exceptions import RequestException

class HttpClient:
    def get(self, url, headers=None):
        return requests.get(url, headers=headers, verify=certifi.where())

class CacheWarmer:
    def __init__(self, http_client, user_agent=None):
        self.http_client = http_client
        self.user_agent = user_agent
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
            
        valid_data = [row for row in results if row is not None]
        print(f"Total number of URLs: {len(urls)}")    
        print(f"Number of failed URLs: {len(valid_data)}")  
        self.data.extend(valid_data)

    def get_error_status(self, error):
        return type(error).__name__

    def warm_up_urls(self, url):
        response = None
        try:
            headers = {'User-Agent': self.user_agent} if self.user_agent else None
            response = self.http_client.get(url, headers=headers)
            if response.status_code == 200:
                message = "OK"
                print(f"Status {message} [{response.status_code}]: {url}")
            else:
                raise requests.exceptions.HTTPError(f"Error [{response.status_code}]")
        except RequestException as e:
            message = "FAILED"
            if response is not None:
                print(response.status_code)
                status = response.status_code
            else:
                status = self.get_error_status(e)
            print(f"Status {message} [{status}]: {url} {e}")
            result = {'url': url, 'status': status, 'error': e}
            return result

    def write_result_to_csv(self, filename=None):
        """Writes the results stored in self.results to a CSV file."""
        if filename is None:
            current_date = datetime.datetime.now().strftime("%Y_%m_%d")
            filename = f'report_{current_date}.csv'

        if os.path.dirname(filename):
            os.makedirs(os.path.dirname(filename), exist_ok=True)
 
        with open(filename, mode='w', newline='') as file:
            fieldnames = ['url', 'status', 'error']
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

    current_date = datetime.datetime.now().strftime("%Y_%m_%d")
    filename = f'/URL_reports.csv'

    start = time.time()
    cache_warmer.warm_up_cache(csv_file_path, base_url)
    print ('Report took', "{:.2f}".format(time.time()-start) ,' seconds to generate')
    save_report = input("Do you want to save the report? (Yes/No): ")
    
    if save_report.lower() in ('yes', 'y'):
        cache_warmer.write_result_to_csv(filename)
    else:
        print("Report generated but not saved.")
