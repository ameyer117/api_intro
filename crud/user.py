import sys
from datetime import datetime, timedelta
import os

from fastapi import Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from starlette import status

from db import users_collection
from schemas.user import UserInDB
import base64
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    stream=sys.stdout
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ALGORITHM = "HS256"
SECRET_KEY = os.getenv("SECRET_KEY")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def get_user(email: str):
    logger.info(f"Getting user {email}")
    user_dict = users_collection.find_one({"email": email})
    if user_dict:
        return UserInDB(**user_dict)

def insert_user(user: UserInDB):
    logger.info(f"Inserting user {user.email}")
    user_dict = user.model_dump()
    return users_collection.insert_one(user_dict)

def authenticate_user(email: str, password: str):
    logger.info(f"Authenticating user {email}")
    user = get_user(email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(auth_header: str = Header("Authorization")):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if " " not in auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header expected format 'SCHEME VALUE'",
            headers={"WWW-Authenticate": "Bearer"},
        )

    scheme, token = auth_header.strip().split(" ")

    try:
        if scheme.lower() == "bearer":
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                logger.error("Email wasn't found in the token")
                raise credentials_exception
        elif scheme.lower() == "basic":
            decoded = base64.b64decode(token).decode("utf-8")
            email, password = decoded.split(":")
            if not authenticate_user(email, password):
                logger.error(f"Invalid email or password for email {email}")
                raise credentials_exception
        else:
            logger.error(f"Invalid scheme {scheme}")
            raise credentials_exception
    except JWTError as e:
        logger.error(f"JWT Error: {e}")
        raise credentials_exception
    except Exception as e:
        logger.error(f"Error: {e}")
        raise credentials_exception
    user = get_user(email=email)
    if user is None:
        logger.error(f"User not found for email {email}")
        raise credentials_exception

    logger.info(f"User {user.email} authenticated")
    return user