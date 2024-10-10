import time
import app
import json

from app.csv_module import CSVModule
from app.file_loader import FileLoader
from app.http_request import HttpClient

if __name__ == "__main__":
    
    with open('config.json', 'r') as file:
        data = json.load(file)

    if not app.base_url:
        print("Error: BASE_URL environment variable is not provided.")
        print("Please run the script with 'BASE_URL' environment variable set.")
        app.sys_.exit(1)

    if not app.user_agent:
        user_agent = input("Please enter the user agent: ")

    csv_file_path = app.current_directory + '/urls.csv'
    http_client = HttpClient()
    module = FileLoader()
    sanitize = False
    
    print(f"HTTP Request Test Tool v{data['version']}\n")
    for data in data['options']:
        print(data)
    operation = input("\nWhich function would you like to perform?: ")

    if operation == '1':
        print("Generating HTTP Reports...")
        pass
    elif operation == '2':
        app.sanitize = True
    else:
        print("Invalid Input")
        app.sys_.exit(1)

    start = time.time()
    temp_file = module.load_cache(csv_file_path, app.base_url, app.sanitize)
    print('Report took', "{:.2f}".format(time.time() - start), 'seconds to generate')

    save_report = input("Do you want to save the report? (Yes/No): ")

    if save_report.lower() in ('yes', 'y', '-y'):
        CSVModule.write_result_to_csv(temp_file)
    else:
        print("Report generated but not saved.")
