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
        self.user_fields = dict(
            personal_account="ЛицСч",
            full_name="ФИО",
            address="Адрес",
            period="Период",
            total="Сумма",
        )
        self._get_file_encoding()
        
    def parse_xml(self, file_name: str) -> ElementTree.Element:
        xml = ElementTree.parse(self.file_path)
        self.xml_root = xml.getroot()
                    # collect satic values
        self.date = xml.find("./СлЧаст/ОбщСвСч/ИдФайл/ДатаФайл").text

        for user in xml.iter('Плательщик'):
            if user:
                # merge static values w/ data from user
                user_dict = dict(registry_name=file_name, date=self.date,)\
                    | {k: user.find(v).text for k, v in self.user_fields.items()} 

                if not self._validate_user(user_dict):
                    # handle invvalid field for critical/non critical
                    ...

                # no duplicate user
                if not self._uniqiue_user_fields(user_dict):
                    # warn that we skipped the user
                    ...

                # add a new row to csv file
                yield user_dict
        # return self.xml_root


    def _get_file_encoding(self):
        with open(self.file_path, 'rb') as f:
            line = f.readline()
            header = minidom.parseString(f'{line.decode()}<a></a>')
            self.encoding = header.encoding

    

    def _validate_user(self, user: ElementTree.Element):
        return 1

    def _uniqiue_user_fields(self, user):
        return 0

