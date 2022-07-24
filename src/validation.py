
from typing import Optional
from pydantic import BaseModel, validator
import re
col_descriptions = dict(
    registry_name='Имя файла реестра',
    date='Дата', 
    personal_account='Лицевой счет',
    full_name='ФИО',
    address='Адрес',
    period='Период',
    total='Сумма',
)

class Validator(object): 
    '''docstring for Validator'''
    def __init__(self, ):
        super().__init__()

    @property
    def user_fields(self):
        return dict(
            personal_account="ЛицСч",
            full_name="ФИО",
            address="Адрес",
            period="Период",
            total="Сумма",
        )

class UserModel(BaseModel):   
    registry_name: str 
    date: str 
    personal_account: str 
    full_name: str 
    address: Optional[str] 
    period: str 
    total: Optional[str] 

    @validator('registry_name')
    def file_ext_must_be_xml(cls, v):
        assert re.search(r'^(.)+.xml$', v)
        return v
    @validator('date')
    def validate_date_format(cls, v):
        # DD.MM.YYYY
        assert re.search(r'\d{2}.\d{2}.\d{4}', v)
        return v
    @validator('period')
    def validate_period(cls, v):
        # MMYYYY
        assert re.search(r'(0[1-9]|10|11|12)[0-9]{4}$', v)
        return v
    @validator('total')
    def tatal_must_be_unsigned_float(cls, v):
        v_float = float(v)
        assert float(v) >= 0
        return f"{v_float:.2f}"  