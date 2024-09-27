from datetime import datetime, timedelta, timezone
import os

from dotenv import load_dotenv
import jwt
from passlib.context import CryptContext
from fastapi import Response
from ..schemas import Token


load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("JWT_SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    return encoded_jwt
                      
def decode_access_token(token):
    return jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])

def create_access_cookie(response: Response, email: str, id: int):
    access_token = create_access_token({ "sub": email, "user_id": id })
    response.set_cookie(key="jwt", value=access_token, httponly=True, secure=True, samesite="none")
    return Token(access_token=access_token, token_type="bearer")
