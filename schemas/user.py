from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class CreateUserRequest(BaseModel):
    email: str
    full_name: str
    password: str

class LoginUserRequest(BaseModel):
    email: str
    password: str


class User(BaseModel):
    email: str
    full_name: str


class UserInDB(User):
    hashed_password: str