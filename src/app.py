
import os
from src.xml_file_parser import XMLFileParser
from src.csv_writer import CSVWriter
from src.logger import get_logger

class App(object): 
    '''docstring for App'''
    def __init__(self, ):
        super().__init__()
        self._encoding = 'utf-8'


    def parse_file(self, file_path: str) -> None:
        self._file_path = file_path
        self._setup_logger()
        self._validate_file_path()
        self._get_output_path()
        # read xml
        xml_parser = XMLFileParser(self.file_path)
        users = xml_parser.parse_xml(
            file_name=self._output_file_name,
        )
        self._encoding = xml_parser.encoding
        # call csv writer
        csv_writer = CSVWriter()
        csv_writer.write_csv(
            file_path=self._output_file_path,
            users=users,
            encoding=self.encoding,
        )

        return self._output_file_path

    @property
    def file_path(self):
        return self._file_path
    
    @property
    def encoding(self):
        return self._encoding

    def _get_output_path(self):
        '''Parse the output file path based on given input file path'''
        base = os.path.splitext(os.path.basename(self.file_path))[0]
        self._output_file_name = f'{base}.csv'
        self._output_file_path = os.path.join(
            os.path.dirname(self.file_path), self._output_file_name)

    def _setup_logger(self):
        '''Setup logging for current file'''
        folder = os.path.dirname(self._file_path)
        self.logger = get_logger(
            os.path.join(
                os.path.abspath(folder), 'log', 'parser.log'
            )
        )
        self.logger.info(f"Logs setup complete for file {self._file_path}")


    def _validate_file_path(self,):
        if os.path.isfile(self._file_path):
            extension = os.path.splitext(self._file_path)[1]
            if extension == '.xml':
                # logger.info(f"Parse file {self._file_path}")
                return
            # TODO move to bad folder
            raise FileNotFoundError("Invalid XML file")        
        raise FileNotFoundError(self._file_path)

