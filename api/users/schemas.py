from pydantic import BaseModel, validator
from typing import List, Optional
import re


class CreateUserScheme(BaseModel):
    first_name: str
    last_name: str
    third_name: str
    e_mail: str
    password: str

    class Config:
        orm = True

    @validator('password')
    def pass_valid(cls, value):
        pattern = r'^(?=.*[aA-zZ]){1}(?=.*\d){1}[A-Za-z\d]{6,}$'
        if re.match(pattern, value) is None:
            raise ValueError('Пароль должен быть не менее 6 символов и содержать хотя бы 1 букву и одну цифру')
        return value

    @validator('e_mail')
    def email_valid(cls, value):
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.match(pattern, value) is None:
            raise ValueError('Не валидный email')
        return value


class UpdateUserScheme(CreateUserScheme):
    user_id: int
    first_name: Optional[str]
    last_name: Optional[str]
    third_name: Optional[str]
    e_mail: Optional[str]
    password: Optional[str]


class SearchUserScheme(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    third_name: Optional[str]
    e_mail: Optional[str]