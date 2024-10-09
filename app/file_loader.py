import tempfile
import app

from app.csv_module import CSVModule
from app.http_request import HttpClient

from multiprocessing import Pool, Manager

class FileLoader:
    def __init__(self):
        FileLoader.urls_total = 0

    def load_cache(self, csv_file_path, base_url):
        if not base_url:
            raise ValueError("Error: BASE_URL environment variable is not provided.")

        urls = CSVModule.csv_reader(csv_file_path)
        FileLoader.urls_total = len(urls)

        with Manager() as manager:
            FileLoader.urls_count = manager.Value('i', 0)
            FileLoader.lock = manager.Lock()

            with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".csv", prefix="temp_cache_warmer_", dir=".") as temp_file:
                temp_filename = temp_file.name
                with open(temp_filename, mode='w', newline='') as temp_csv:
                    fieldnames = ['url', 'status', 'error']
                    
                    writer = CSVModule.csv_set_dict_writer(temp_csv, fieldnames)
                    CSVModule.csv_write_header(writer)

                    with Pool(app.num_processes) as pool:
                        results = pool.map(FileLoader.load_urls, [(url if url.startswith('http://') or url.startswith('https://') 
                            else (base_url + url if url != '/' else base_url),) 
                                for url in urls])
                
                    valid_data = [row for row in results if row is not None]
                    print(f"Total number of URLs: {len(urls)}")    
                    print(f"Number of failed URLs: {len(valid_data)}")  
                    
                    CSVModule.csv_row_writer(writer, valid_data)

        return temp_filename
    
    def load_urls(url_data):
        url = url_data[0]
        with FileLoader.lock:
            FileLoader.urls_count.value += 1
            counter = f"({FileLoader.urls_count.value}/{FileLoader.urls_total})"
        result = HttpClient.http_request(url, counter)

        return result