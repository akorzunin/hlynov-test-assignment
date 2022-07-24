
import os
from src.xml_file_parser import XMLFileParser
from src.csv_writer import CSVWriter
from src.logger import get_logger
from src.validation import Validator

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
        validator = Validator()

        # read xml
        xml_parser = XMLFileParser(
            file_path=self.file_path,
            user_fields=validator.user_fields
        )
        users = xml_parser.parse_xml(
            file_name=self._output_file_name,
            logger=self.logger,
        )
        self._encoding = xml_parser.encoding
        # call csv writer
        csv_writer = CSVWriter()
        csv_writer.write_csv(
            file_path=self._output_file_path,
            users=users,
            encoding=self.encoding,
        )
        self.logger.info(f"File {self._file_path} successfully parsed")
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

    def _validate_file_path(self,):
        '''Check if file path is valid if file not xml move it to /bad folder'''
        if os.path.isfile(self._file_path):
            extension = os.path.splitext(self._file_path)[1]
            if extension == '.xml':
                self.logger.info(f"Parse file {self._file_path}")
                return
            self.logger.warning(f"Not a xml file: {self._file_path}")
            os.makedirs(os.path.join(os.path.dirname(self._file_path), 'bad'),  
                exist_ok=True) 
            os.replace(
                self._file_path, 
                os.path.join(
                    os.path.dirname(self._file_path),
                    'bad',
                    os.path.basename(self._file_path)
                )
            )
        raise FileNotFoundError(self._file_path)

