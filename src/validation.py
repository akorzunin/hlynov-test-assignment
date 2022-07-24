
from pydantic import BaseModel, validator

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
    name: str
    username: str
    password1: str
    password2: str
    
    personal_account: str
    full_name: str
    address: str
    period: str
    total: str
    @validator('name')
    def name_must_contain_space(cls, v):
        if ' ' not in v:
            raise ValueError('must contain a space')
        return v.title()

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password1' in values and v != values['password1']:
            raise ValueError('passwords do not match')
        return v

    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v