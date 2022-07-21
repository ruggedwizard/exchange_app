
from pydantic import BaseModel
from typing import Optional

class LoginSchema(BaseModel):
    email:str
    password:str

class TokenSchema(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[str]

class ForgetPassword(BaseModel):
    email:str

class Resetpassword(BaseModel):
    reset_password_token:str
    new_password:str
    confirm_password:str
    email:str

class SendEth(BaseModel):
    receiver:str
    amount:float

class BuyTrade(BaseModel):
    quantity:float

class LimitTrade(BaseModel):
    quantity:float
    limit_price:float