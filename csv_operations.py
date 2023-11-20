from datetime import datetime
from datetime import timedelta

import json_operations as jo

"""
Module : csv_operations
"""


def write_csv(name_file: str, name_dir: str):
    dict_for_csv = jo.load_json(name_file, name_dir)
    with open("bum.csv", "a", encoding="utf8") as file:
        for key, value in dict_for_csv.items():
            if '"' in key or "'" in key or ";" in key:
                key = key.replace('"', "**").replace("'", "*").replace(";", "***")
            if '"' in value or "'" in value or ";" in value:
                value = value.replace('"', "**").replace("'", "*").replace(";", "***")
            file.write(f'"{key}";"{value}"\n')


def read_csv(file_name: str):
    date_lst: list = []
    count: int = 0
    for i in range(10):
        date = datetime.today() - timedelta(days=i)
        date = date.strftime("%d-%m-%Y")
        date_lst.append(date)
    with open(file_name, "r", encoding="utf8") as file:
        for row in file:
            print(row)
            print(row[1:11])
            if row[1:11] in date_lst:
                count += 1
    return count




if __name__ == "__main__":
    pass
    # name_file = 'abbreviations.json'
    # name_dir = 'data'
    # write_csv(name_file, name_dir)
    # read_csv("bum.csv")
