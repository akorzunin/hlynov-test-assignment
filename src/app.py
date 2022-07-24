
import os
from src.xml_file_parser import XMLFileParser
from src.csv_writer import CSVWriter
from src.logger import get_logger

class App(object): 
    '''docstring for App'''
    def __init__(self, move_file: bool = False):
        super().__init__()
        self.move_file = move_file
        self._encoding = 'utf-8'


    def parse_file(self, file_path: str):
        self._file_path = file_path
        self._setup_logger()
        self._get_output_path()
        if not self._is_valid_file_path(): 
            return self._output_file_path

        # read xml
        xml_parser = XMLFileParser(
            file_path=self.file_path,
            logger=self.logger,
        )
        users = xml_parser.parse_xml()
        self._encoding = xml_parser.encoding
        # call csv writer
        csv_writer = CSVWriter()
        csv_writer.write_csv(
            file_path=self._output_file_path,
            users=users,
            encoding=self.encoding,
        )
        self.logger.info(f"✅ File {self._file_path} successfully parsed")
        if self.move_file:
            self._move_file_to_folder("arh")
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

    def _is_valid_file_path(self,):
        '''Check if file path is valid if file not xml move it to /bad folder'''
        if os.path.isfile(self._file_path):
            extension = os.path.splitext(self._file_path)[1]
            if extension == '.xml':
                self.logger.info(f"▶ Parse file {self._file_path}")
                return True
            self.logger.warning(f"⛔ Not a xml file: {self._file_path}")
            if self.move_file:
                self._move_file_to_folder("bad")
            return False
        raise FileNotFoundError(self._file_path)

    def _move_file_to_folder(self, folder_name: str):
        os.makedirs(os.path.join(os.path.dirname(self._file_path), folder_name),  
            exist_ok=True) 
        os.replace(
            self._file_path, 
            os.path.join(
                os.path.dirname(self._file_path),
                folder_name,
                os.path.basename(self._file_path)
            )
        )

