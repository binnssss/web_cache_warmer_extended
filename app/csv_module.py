import csv

from datetime import datetime

import app

class CSVModule:
    def csv_file_reader(file_path):
        try:
            with open(file_path, 'r', errors='ignore') as file:     
                if CSVModule.csv_has_header(file):
                    reader = CSVModule.csv_dict_reader(file)  
                    file.seek(0)    
                    column_name = input("Target Column (Case Sensitive): ")
                    data = [(row, row[column_name].strip()) for row in reader if row.get(column_name)]
                else:
                    print('Check the provided file if there are any column names. Reading first column for URLs...')
                    reader = csv.reader(file)
                    data = [(row, row[0].strip()) for row in reader if len(row) > 0]
            return data
        except FileNotFoundError:
            print(f"File {file_path} not found.")
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")

    def csv_reader(file):
        return csv.reader(file)

    def csv_has_header(file):
        try:
            reader = CSVModule.csv_dict_reader(file)
            if reader.fieldnames:
                file.seek(0)
                return True
        except:
            return False
    
    def csv_dict_reader(file):
        return csv.DictReader(file)
    
    def csv_set_dict_writer(temp_csv, fieldnames):
        return csv.DictWriter(temp_csv, fieldnames=fieldnames)
    
    def csv_write_header(writer):
        writer.writeheader()

    def csv_row_writer(writer, data):
        writer.writerows(data)

    def write_result_to_csv(temp_filename, final_filename=None):
        """Writes the results stored in the temp file to a CSV file."""
        if final_filename is None:
            now = datetime.now()
            final_filename = f'/output/URL_reports_{now.strftime('%Y-%m-%d_%H-%M-%S')}.csv'

        if app.os_.path.dirname(final_filename):
            app.os_.makedirs(app.os_.path.dirname(final_filename), exist_ok=True)

        with open(final_filename, mode='w', newline='') as final_csv:
            with open(temp_filename, 'r') as temp_file:
                final_csv.write(temp_file.read())

        print(f"Report saved as {final_filename}")