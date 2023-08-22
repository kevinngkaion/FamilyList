from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from starlette import status
from model import User, CreateUser, Token, TokenData, UserInDB
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from config import JWT_SECRET, JWT_ALGORITHM
from database import create, fetch_one, fetch_user
from .jwt_handler import create_access_token, decodeJWT

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(user:CreateUser):
    user.password = pwd_context.hash(user.password)
    response = await create('user', user.dict())
    response = await fetch_one('user', response.inserted_id)
    if response:
        return response
    raise HTTPException(400, "Something went wrong / Bad request")

@router.post("/token", response_model=Token)
async def login_for_access_token(data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(data.username, data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    token = create_access_token(user['username'], user['_id'], timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}

async def authenticate_user(username, password):
    user = await fetch_user(username)
    if not user:
        return False
    if not pwd_context.verify(password, user["password"]):
        return False
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = decodeJWT(token)
        uid: str = payload.get("id")
        if uid is None:
            raise credential_exception
        token_data = TokenData(user_id=uid)
    except JWTError:
        raise credential_exception
    
    user = await fetch_one('user', token_data.user_id)
    if user is None:
        raise credential_exception
    
    return user

async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if not current_user["is_active"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is currently inactive")
    return current_user