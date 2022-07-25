import os
from typing import Iterator, Set
from lxml import etree as ElementTree
from xml.dom import minidom
from pydantic import ValidationError
from loguru._logger import Logger

from src.validation import UserModel, Validator


class XMLFileParser(object):
    '''Parse xml file'''

    def __init__(self, file_path: str, logger: Logger):
        super().__init__()
        self.file_path = file_path
        self.xml_root = None
        self.logger = logger

        self._get_file_encoding()

    def parse_xml(self, ) -> Iterator[dict]:
        xml = ElementTree.parse(self.file_path)
        self.xml_root = xml.getroot()
        # collect satic values
        self.date = xml.find("./СлЧаст/ОбщСвСч/ИдФайл/ДатаФайл").text
        self.user_set: Set[str] = set()
        # allocate scatic objects to cunstruct user data from models
        validator = Validator()
        base_file = os.path.basename(self.file_path)
        for user in xml.iter('Плательщик'):
            if user:
                # collect values from xml fields if they exist
                user_data = {
                    k: user.find(v).text
                    for k, v in validator.user_fields.items()
                    if user.find(v) is not None
                }
                # merge static values w/ data from user
                user_dict = dict(registry_name=base_file, date=self.date,)\
                    | user_data

                try:
                    valid_user = UserModel(**user_dict).dict()
                except ValidationError as e:
                    self._handle_invalid_user(e, validator, user, user_dict)
                    continue
                if self._is_uniqiue_user(user_dict):
                    yield valid_user
                # no duplicate user
                self.logger.warning(
                    f'♊ Duplicate user is skipped: {user_dict} ')

    def _get_file_encoding(self):
        with open(self.file_path, 'rb') as f:
            line = f.readline()
            header = minidom.parseString(f'{line.decode()}<a></a>')
            self.encoding = header.encoding

    def _handle_invalid_user(self, e: ValidationError, validator: Validator,
                             user: ElementTree._Element, user_dict: dict):
        # get field name
        err_field_name = e.errors()[0]['loc'][0]
        if err_field_name in validator.critical_fields.keys():
            # special handling for critical fields
            self.logger.warning(
                f"🛑 Сторка номер {user.sourceline} не "
                f"имеет одного из ключевых реквизитов. "
                f"Поле: {validator.csv_fields[err_field_name]} "
                f"значение: {user_dict.get(err_field_name)}"
            )
        else:
            # non critical
            self.logger.warning(
                f"🤚 ValidationError at field: "
                f"{validator.csv_fields[err_field_name]} "
                f"got value: {user_dict.get(err_field_name)}"
            )

    def _is_uniqiue_user(self, user: dict) -> bool:
        '''check if user have unique personal_account and period fields'''
        unique_pair = user['personal_account']+"_"+user['period']
        if unique_pair in self.user_set:
            return False
        self.user_set.add(unique_pair)
        return True
