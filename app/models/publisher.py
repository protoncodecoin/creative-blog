from beanie import Document
from pymongo import IndexModel, DESCENDING
from pydantic import Field, EmailStr, BaseModel

from typing import Optional, List


class Publisher(Document):
    first_name: str
    last_name: str
    username: str
    email: EmailStr = Field(..., unique=True)
    password: str
    # articles: Optional[List[Article]] = []

    class Settings:
        name = "publishers"
        indexes = [
            IndexModel([("username", DESCENDING)]),
            IndexModel([("email", DESCENDING)], unique=True),
        ]


class UserSignIn(BaseModel):
    email: EmailStr = Field(..., unique=True)
    password: str


class UserResponse(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "username": "Jon Doe",
                "email": "jondoe@example.com",
                "password": "strong!!"
            }
        }

