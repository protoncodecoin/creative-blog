from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

from ..db.database import QueryDatabase
from ..models.publisher import Publisher
from ..models.token import TokenData

from ..db.database import Settings

settings = Settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/publisher/signin")
database = QueryDatabase(Publisher)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("username")
        email: str = payload.get("email")
        if username is None or email is None:
            raise credentials_exception
        token_data = TokenData(email=email, username=username)
    except JWTError:
        raise credentials_exception
    user = await database.get_user_by_email(token_data.email)
    if user is None:
        raise credentials_exception
    return token_data


