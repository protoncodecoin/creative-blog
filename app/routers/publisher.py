from fastapi import APIRouter, HTTPException, status, Depends
from ..models.publisher import Publisher, UserResponse
from ..db.database import QueryDatabase
from ..auth import utility
from fastapi.security import OAuth2PasswordRequestForm
from beanie import PydanticObjectId
from ..auth.jwt_handler import create_access_token

from typing import List
from datetime import timedelta

from ..models.token import Token

from ..db.database import Settings

publisher_route = APIRouter(tags=['publisher'])

database = QueryDatabase(Publisher)
password_utility = utility.HashPassword()

settings = Settings()


@publisher_route.post("/signup", status_code=201)
async def signup_publisher(publisher_data: Publisher):
    """ verifies user password and saves the hash password into the database"""
    user_exit = await Publisher.find_one(Publisher.email == publisher_data.email)
    if user_exit:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials. Email Already Exists.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if publisher_data.password is None or len(publisher_data.password) < 8:
        raise HTTPException(
            detail="Password cannot be None or length of password cannot be less than 8",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    hash_password = password_utility.create_hash_password(password=publisher_data.password)
    publisher_data.password = hash_password

    await database.save(publisher_data)

    return publisher_data


@publisher_route.post("/signin", response_model=Token)
async def signin_publisher(form_data: OAuth2PasswordRequestForm = Depends()):
    """ validate credentials and returns a jwt token if true"""
    user_exist = await database.get_user_by_email(form_data.username)
    if user_exist is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    if not password_utility.verify_hashed_password(form_data.password, user_exist.password):
        raise HTTPException(
            detail="Invalid Credentials",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user_exist.username, "email": user_exist.email}, expire_delta=access_token_expires
    )
    return {
        "access_token": access_token, "token_type": "bearer"
    }


@publisher_route.get("/accounts/general")
async def get_all_accounts() -> List[Publisher]:
    """Get all created accounts"""
    users = await database.get_all()
    if users is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No Users in Database"
        )
    return users


@publisher_route.get("/account/{id}")
async def get_publisher_by_id(id: PydanticObjectId):
    """ Delete user from database based on provided PydanticObjectId"""
    user_exit = await database.get_by_id(id)
    if user_exit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist",
        )

    return user_exit


@publisher_route.get("/account/email/{email}", response_model=UserResponse)
async def get_publisher_by_email(email: str):
    """Get account by email provided.
        For Debugging"""
    users = await database.get_user_by_email(email)
    # print(users)

    if users is None:
        raise HTTPException(
            detail="User is not found",
            status_code=status.HTTP_404_NOT_FOUND
        )

    return users


@publisher_route.delete("/account/delete/all")
async def delete_all_publishers():
    """Delete all publishers account from Database"""
    await database.delete_all()
    return {
        "message": "All Publishers accounts cleared"
    }


@publisher_route.delete("/account/delete/{id}")
async def delete_by_id(id: PydanticObjectId):
    """Get account using the provided Pydantic Object id"""
    account = await database.get_by_id(id)
    if account is None:
        raise HTTPException(
            detail="Publisher Account not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
    await account.delete()
    return {
        "message": "User account successfully deleted."
    }

