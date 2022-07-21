from fastapi import status, Depends
from passlib.context import CryptContext
import jwt
from dotenv import dotenv_values
from fastapi.exceptions import HTTPException
from app.models import User
from jose import JWTError, jwt
from datetime import datetime, timedelta



ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120
SECRET_KEY = "01a2b41db6be32d8d2f83482bda6fb75f6f619629"


config_credential = dotenv_values(".env")
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def get_hashed_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)


async def verify_token(token:str):
    try:
        payload = jwt.decode(token,config_credential["SECRET"],algorithms=["HS256"])
        user = await User.get(id=payload.get("id"))
    except: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="Invalid token",
        headers={"WWW-Authenticate":"Bearer"})
    return user




async def authenticate_user(email,password):
    user = await User.get(email=email)
    if user and verify_password(password,user.password):
        return user
    return False

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET = "1a2b41db6be32d8d2f83482bda6fb75f6f619629"

async def token_generator(email:str,password:str):

    user = await authenticate_user(email,password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Email or Password", headers={"WWW-Authenticate":"Bearer"})



    token_data ={
        "id":user.id,
        "email":user.email

    }

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data.update({"exp":expire})
    
    token = jwt.encode(token_data,SECRET,algorithm=ALGORITHM)

    return token




# NEw Login version





async def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt