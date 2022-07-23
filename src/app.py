
import os
from src.xml_file_parser import XMLFileParser

class App(object): 
    '''docstring for App'''
    def __init__(self, ):
        super().__init__()

    def parse_file(self, file_path: str) -> None:
        self._file_path = file_path
        self._validate_file_path()
        # read xml

        # call csv writer

        return 1


    def _validate_file_path(self,):
        if os.path.isfile(self._file_path):
            extension = os.path.splitext(self._file_path)[1]
            if extension == '.xml':
                return
            raise FileNotFoundError("Invalid XML file")        
        raise FileNotFoundError(self._file_path)

