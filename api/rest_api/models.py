from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    hashed_password: str


class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class AuthRequest(BaseModel):
    email: EmailStr
    password: str
