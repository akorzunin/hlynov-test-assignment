from xml.etree import ElementTree
from xml.dom import minidom
# from src.validation import user_fields

class XMLFileParser(object): 
    '''Parse xml file'''
    def __init__(self, file_path: str, user_fields: dict):
        super().__init__()
        self.file_path = file_path
        self.xml_root = None
        self.user_fields = user_fields

        self._get_file_encoding()
        
    def parse_xml(self, file_name: str, logger) -> ElementTree.Element:
        xml = ElementTree.parse(self.file_path)
        self.xml_root = xml.getroot()
        # collect satic values
        self.date = xml.find("./СлЧаст/ОбщСвСч/ИдФайл/ДатаФайл").text

        self.user_set = set()
        for user in xml.iter('Плательщик'):
            if user:
                # merge static values w/ data from user
                user_dict = dict(registry_name=file_name, date=self.date,)\
                    | {k: user.find(v).text for k, v in self.user_fields.items()} 

                if self._is_valid_user(user_dict):
                    # handle invvalid field for critical/non critical
                    ...

                    # no duplicate user
                    if self._is_uniqiue_user(user_dict):
                        # warn that we skipped the user
                        ...
                        yield user_dict
                    logger.warning(f'Duplicate user is skipped: {user_dict} ')


    def _get_file_encoding(self):
        with open(self.file_path, 'rb') as f:
            line = f.readline()
            header = minidom.parseString(f'{line.decode()}<a></a>')
            self.encoding = header.encoding

    def _is_valid_user(self, user: ElementTree.Element):
        return 1

    def _is_uniqiue_user(self, user: dict) -> bool:
        '''check if user have unique personal_account and period fields'''
        unique_pair = user['personal_account']+"_"+user['period'] 
        if unique_pair in self.user_set:
            return False
        self.user_set.add(unique_pair)
        return True

