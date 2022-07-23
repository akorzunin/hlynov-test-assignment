from xml.etree import ElementTree as ET
import csv

class CSVWriter(object): 
    '''docstring for CSVWriter'''
    def __init__(self, ):
        super().__init__()

    def write_csv(self, file_path: str, users, encoding: str = 'utf-8',):
        with open(file_path, 'w', encoding=encoding) as csvfile:
            csvfile_writer = csv.writer(
                csvfile,
                delimiter =';',
            )
            for user in users:
                csvfile_writer.writerow(user.values())