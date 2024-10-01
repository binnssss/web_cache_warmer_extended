import time
import os
import csv
import sys
import requests
import tempfile
from multiprocessing import Pool, Manager
from datetime import datetime
from requests.exceptions import RequestException

class HttpClient:
    def get(self, url, headers=None):
        return requests.get(url, headers=headers)

class CacheWarmer:
    def __init__(self, http_client, user_agent=None):
        self.http_client = http_client
        self.user_agent = user_agent
        self.urls_total = 0

    def warm_up_cache(self, csv_file_path, base_url):
        if not base_url:
            raise ValueError("Error: BASE_URL environment variable is not provided.")

        urls = self.csv_reader(csv_file_path)
        self.urls_total = len(urls)
        num_processes = os.cpu_count() or 1

        with Manager() as manager:
            self.urls_count = manager.Value('i', 0)
            self.lock = manager.Lock()

            with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".csv", prefix="temp_cache_warmer_", dir=".") as temp_file:
                temp_filename = temp_file.name
                with open(temp_filename, mode='w', newline='') as temp_csv:
                    fieldnames = ['url', 'status', 'error']
                    writer = csv.DictWriter(temp_csv, fieldnames=fieldnames)
                    writer.writeheader()

                    with Pool(num_processes) as pool:
                        results = pool.map(self.warm_up_urls, [(url if url.startswith('http://') or url.startswith('https://') 
                        else (base_url + url if url != '/' else base_url),) 
                            for url in urls])
                
                    valid_data = [row for row in results if row is not None]
                    print(f"Total number of URLs: {len(urls)}")    
                    print(f"Number of failed URLs: {len(valid_data)}")  
                    
                    writer.writerows(valid_data)

        return temp_filename

    def csv_reader(self, file_path):
        try:
            with open(file_path, 'r', errors='ignore') as file:
                has_header = csv.Sniffer().has_header(file.read())
                file.seek(0)

                if has_header:
                    reader = csv.DictReader(file)
                    first_column = reader.fieldnames[0]
                    urls = [row[first_column].strip() for row in reader if row.get(first_column)]
                else:
                    reader = csv.reader(file)
                    urls = [row[0].strip() for row in reader if len(row) > 0]

                return urls

        except FileNotFoundError:
            print(f"File {file_path} not found.")
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")

    def get_error_status(self, error):
        return type(error).__name__

    def warm_up_urls(self, url_data):
        url = url_data[0]
        response = None
        with self.lock:
            self.urls_count.value += 1
            counter = f"({self.urls_count.value}/{self.urls_total})"
        try:
            headers = {'User-Agent': self.user_agent} if self.user_agent else None
            response = self.http_client.get(url, headers=headers)
            if response.status_code == 200:
                message = "OK"
                print(f"{counter} Status {message} [{response.status_code}]: {url}")
            else:
                raise requests.exceptions.HTTPError(f"Error [{response.status_code}]")
        except RequestException as e:
            message = "FAILED"
            status = response.status_code if response is not None else self.get_error_status(e)
            print(f"{counter} Status {message} [{status}]: {url} {e}")
            result = {'url': url, 'status': status, 'error': f"{e}"}
            return result

    def write_result_to_csv(self, temp_filename, final_filename=None):
        """Writes the results stored in the temp file to a CSV file."""
        if final_filename is None:
            now = datetime.now()
            final_filename = f'/output/URL_reports_{now.strftime('%Y-%m-%d_%H-%M-%S')}.csv'

        if os.path.dirname(final_filename):
            os.makedirs(os.path.dirname(final_filename), exist_ok=True)

        with open(final_filename, mode='w', newline='') as final_csv:
            with open(temp_filename, 'r') as temp_file:
                final_csv.write(temp_file.read())

        print(f"Report saved as {final_filename}")

if __name__ == "__main__":
    base_url = os.environ.get('BASE_URL')
    user_agent = os.environ.get('USER_AGENT')

    if not base_url:
        print("Error: BASE_URL environment variable is not provided.")
        print("Please run the script with 'BASE_URL' environment variable set.")
        sys.exit(1)

    if not user_agent:
        user_agent = input("Please enter the user agent: ")

    current_directory = os.getcwd()

    csv_file_path = current_directory + '/urls.csv'
    http_client = HttpClient()
    cache_warmer = CacheWarmer(http_client, user_agent)

    start = time.time()
    temp_file = cache_warmer.warm_up_cache(csv_file_path, base_url)
    print('Report took', "{:.2f}".format(time.time() - start), 'seconds to generate')

    save_report = input("Do you want to save the report? (Yes/No): ")

    if save_report.lower() in ('yes', 'y', '-y'):
        cache_warmer.write_result_to_csv(temp_file)
    else:
        print("Report generated but not saved.")
