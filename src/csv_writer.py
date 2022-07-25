import csv
from typing import Iterator


class CSVWriter(object):
    '''Write to a csv file'''

    def __init__(self, ):
        super().__init__()

    def write_csv(self, file_path: str, users: Iterator[dict],
                  encoding: str = 'utf-8',):
        with open(file_path, 'w', encoding=encoding, newline='') as csvfile:
            csvfile_writer = csv.writer(
                csvfile,
                delimiter=';',
            )
            for user in users:
                csvfile_writer.writerow(list(user.values()))
