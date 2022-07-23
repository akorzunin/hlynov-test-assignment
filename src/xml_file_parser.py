from xml.etree import ElementTree
from xml.dom import minidom
import csv
from os import PathLike

class XMLFileParser(object): 
    '''Parse xml file'''
    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path
        self.xml_root = None

    def parse_xml(self,) -> ElementTree.Element:
        xml = ElementTree.parse(self.file_path)
        self._get_file_encoding()
        self.xml_root = xml.getroot()
        return self.xml_root

    def _get_file_encoding(self):
        with open(self.file_path, 'rb') as f:
            line = f.readline()
            header = minidom.parseString(f'{line.decode()}<a></a>')
            self.encoding = header.encoding

