from datetime import datetime

from pydantic import BaseModel, field_validator


class UserData(BaseModel):
    id: int
    name: str
    surname: str
    birth_date: str
    products: list['ProductData'] = []

    @field_validator('birth_date')
    def validate_date_format(cls, value: str) -> str:
        try:
            datetime.strptime(value, '%d.%m.%Y')
            return value
        except ValueError:
            raise ValueError('Дата должна быть в формате дд.мм.гггг')


class ProductData(BaseModel):
    id: int
    title: str
    description: str
    price: float
    user_id: int
