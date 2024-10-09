import csv

from datetime import datetime

import app

class CSVModule:
    def __init__(self):
        self.urls_total = 0

    def csv_reader(file_path):
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
    
    def csv_set_dict_writer(temp_csv, fieldnames):
        writer = csv.DictWriter(temp_csv, fieldnames=fieldnames)
        return writer
    
    def csv_write_header(writer):
        writer.writeheader()

    def csv_row_writer(writer, data):
        writer.writerows(data)

    def write_result_to_csv(temp_filename, final_filename=None):
        """Writes the results stored in the temp file to a CSV file."""
        if final_filename is None:
            now = datetime.now()
            final_filename = f'/output/URL_reports_{now.strftime('%Y-%m-%d_%H-%M-%S')}.csv'

        if app.system.path.dirname(final_filename):
            app.system.makedirs(app.system.path.dirname(final_filename), exist_ok=True)

        with open(final_filename, mode='w', newline='') as final_csv:
            with open(temp_filename, 'r') as temp_file:
                final_csv.write(temp_file.read())

        print(f"Report saved as {final_filename}")