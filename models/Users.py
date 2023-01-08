from pydantic import BaseModel, Field, validator
from utils import get_password_hash


class RegisterUser(BaseModel):
    username: str = Field(min_length=3, max_length=25)
    email: str = Field(regex="^([\w.%+-]+)@([\w-]+\.)+([\w]{2,})$")
    password: str = Field(min_length=3)

    @validator('password')
    def hash_password(cls, v):
        return get_password_hash(v)


class User(BaseModel):
    username: str
    email: str | None = None


class UserInDB(User):
    hashed_password: str


class LoginUser(BaseModel):
    username: str
    password: str


