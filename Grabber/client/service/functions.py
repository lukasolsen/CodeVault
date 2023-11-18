import os
import csv


def find_computerName():
    return os.environ['COMPUTERNAME']


cur_path = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(cur_path, os.pardir))


def saveAsDataTable(data, type):
    for browser_name, browser_data in data.items():
        for table_name, table_data in browser_data.items():
            if table_data:
                os.makedirs(
                    f"{root_path + '/' + find_computerName() + '/' + type +'/' + browser_name}", exist_ok=True)
                file_name = f"{root_path + '/' + find_computerName() +'/' + type +'/' + browser_name + '/' + browser_name}_{table_name}.csv"
                saveTableDataAsCSV(table_data, file_name)


def saveTableDataAsCSV(data, file_name):
    if data is not None:
        with open(file_name, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            # Write column names as the first row
            writer.writerow(data["columns"])
            # Write data rows
            try:
                writer.writerows(data["results"])
            except:
                pass
