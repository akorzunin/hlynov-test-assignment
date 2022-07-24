
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

user_fields = dict(
    personal_account="ЛицСч",
    full_name="ФИО",
    address="Адрес",
    period="Период",
    total="Сумма",
)
