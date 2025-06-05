from datetime import datetime

from pydantic import BaseModel, field_validator

from app.models.product import Product


class User(BaseModel):
    id: int
    name: str
    surname: str
    birth_date: str
    products: list['Product'] = []

    @field_validator('birth_date')
    def validate_date_format(cls, value: str) -> str:
        try:
            datetime.strptime(value, '%d.%m.%Y')
            return value
        except ValueError:
            raise ValueError('Дата должна быть в формате дд.мм.гггг')
