from fastapi import FastAPI, Request, HTTPException,status,Depends, File,UploadFile
from fastapi.responses import HTMLResponse
import uuid
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from app.models import *
from app.auth import *
from tortoise.signals import post_save
from typing import List,Optional,Type
from tortoise import BaseDBAsyncClient
from app.auth import get_hashed_password,verify_token,create_access_token
from fastapi.templating import Jinja2Templates
from app.utills import *
from app.cred import ForgetPassword, LoginSchema, Resetpassword, SendEth
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from PIL import Image
import secrets
import json
from requests import Session
from app.db import *
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from bitcoinlib.transactions import Input
from dotenv import dotenv_values
from bitcoinlib.wallets import Wallet
from app.candlesticks import * 
from app.icons import images_url
from app.converter import *
from app.cred import *

from fastapi_utils.tasks import repeat_every


# binance endpoints for candlestick
END_POINT ='https://api.binance.com'
PATH ='/api/v3/klines'
config_credentials = dotenv_values(".env")




app = FastAPI()
# allowed origins
origins = [
    "http://localhost:8000",
    "http://localhost:3000",
    "http://localhost:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/app/static",StaticFiles(directory="app/static"),name="app/static")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/token')

def get_current_token(token:str=Depends(oauth2_scheme)):
    return token


@app.post("/api/v1/token")
async def generate_token(request_form:OAuth2PasswordRequestForm = Depends()):

    token  = await token_generator(email=request_form.username,password=request_form.password)
    return {"access_token":token,"token_type":"bearer"}


async def get_current_user(token:str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token,config_credentials["SECRET"],algorithms=["HS256"])
        user = await User.get(id=payload.get("id"))
    except:
        raise HTTPException(status_code=401,detail="Invalid Username or Password", headers={"WWW-Authenticate":"Bearer"})
    return await user

@app.get('/')
async def welcome_page():
    return {"Welcome To Exchange Api by David Isaac, go to the url and add /docs to view the SWAGGER API version"}



@app.get("/api/v1/user/me")
async def user_profile(token:str=Depends(oauth2_scheme),user:user_pydanticIn = Depends(get_current_user)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    profile = await Account.get(owner= user)
    profile_image = profile.profile_image
    # profile.profile_image_url ="http://localhost:8000/static/images/" +profile_image
    
    if profile_image == None:
        profile.profile_image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTMq1hdTOg4EZMjART4Uj294FB9uTOhj7qpCcEHiLNRX_PBZRRAX9YtUSa_AofG-Lhj2NI&usqp=CAU"
    else:
        profile.profile_image_url ="https://localhost:8000/static/images/" +profile_image
    
    # print({"profile_image":profile.profile_image_url,})
    
    # get eth balance 
    eth_instance = await EthereiumAddress.get(owner=user)
    eth_address = eth_instance.wallet_address
    # un comment this balance --------------------------------------------------------------------========================================
    # eth_balance = get_account_balance(eth_address)
    eth_balance=eth_instance.account_balance
    eth_lock_balance = eth_instance.lock_account_balance
    # get btc balance 
    account = await BtcAddress.get(owner = user)
    identifier = account.wallet_identifier
    wallet_instance = Wallet(identifier)
    btc_address = account.wallet_address
    # un comment this balance ++===========================================================================================================
    # btc_balance = wallet_instance.as_dict()['main_balance']
    btc_balance= account.account_balance
    btc_lock_balance = account.lock_account_balance
    # get bnb account balance 
    # get eth balance s
    bnb_instance = await BNBAddress.get(owner=user)
    bnb_address = bnb_instance.wallet_address
    # un comment this balance --------------------------------------------------------------------========================================
    # eth_balance = get_account_balance(eth_address)
    bnb_balance=bnb_instance.account_balance
    bnb_lock_balance = bnb_instance.lock_account_balance
    # get lite balance 
    account = await LiteCoinAddress.get(owner = user)
    identifier = account.wallet_identifier
    lite_address = account.wallet_address
    wallet_instance = Wallet(identifier)
    # uncomment this for real balance ===================================================================================================
    # lite_balance = wallet_instance.as_dict()['main_balance']
    lite_balance=account.account_balance
    lite_lock_balance=account.lock_account_balance
    # get dash balance
    account = await DashCoinAddress.get(owner = user)
    identifier = account.wallet_identifier
    dash_address = account.wallet_address
    wallet_instance = Wallet(identifier)
    # un comment this for real balance =================================================================================================
    # dash_balance = wallet_instance.as_dict()['main_balance']
    dash_balance = account.account_balance
    dash_lock_balance = account.lock_account_balance

    # ================================================================ TOTAL BALANCE ======================================================= 
    usd_value = btc_usd(btc_balance) + eth_usd(eth_balance) + bnb_usd(bnb_balance) + ltc_usd(lite_balance) + dash_usd(dash_balance)

    # ================================================================ PERCENTAGE CALCULATION AND BALANCES=============================================

    btc_percent = (btc_usd(btc_balance) / usd_value) * 100
    eth_percent = (eth_usd(eth_balance)/usd_value) *100
    bnb_percent = (bnb_usd(bnb_balance)/usd_value) * 100
    dash_percent = (dash_usd(dash_balance)/usd_value) * 100
    
    data = {
        
    }
    print(data)
        # percentile = str(round(float(_['quote']['USD']['percent_change_24h']),2))+"%"



    return {
        "status":"ok",
        "data": {
            "email":user.email,
            "verified":user.is_verified,
            "display name":user.lastname + " " + user.firstname,
            "profile_image":profile.profile_image_url,
            "total_asset_value":usd_value,
            "eth_address":eth_address,
            "eth_balance":eth_balance,
            "eth_lock_balance":eth_lock_balance,
            "btc_address":btc_address,
            "btc_balance":btc_balance,
            "btc_lock_balance":btc_lock_balance,
            "bnb_address":bnb_address,
            "bnb_balance":bnb_balance,
            "bnb_lock_balance":bnb_lock_balance,
            "lite_address":lite_address,
            "lite_balance":lite_balance,
            "lite_lcok_balance":lite_lock_balance,
            "dash_address":dash_address,
            "dash_balance":dash_balance,
            "dash_lock_balance":dash_lock_balance
        },
        "assets_sum":[
        {
            'name':"btc",
            'percent':btc_percent
        },
        {
            'name':'eth',
            'percent':eth_percent
        },
        {
            'name':'bnb',
            'percent':bnb_percent
        },
        {
            'name':'dash',
            'percent':dash_percent
        }
        ]
    }

# create a new profile when a user is created 
@post_save(User)
async def create_profile(
    sender:"Type[User]",
    instance:User,
    created:bool,
    using_db:"Optional[BaseDBAsyncClient]",
    update_fields:List[str]
)->None:
    if created:
        account_obj= await Account.create(
            available_balance = 0.00,
            owner = instance
        )
        await account_pydantic.from_tortoise_orm(account_obj)
        # send mail
        await send_mail([instance.email],instance)
# creates a new Btc Account when the user is created
@post_save(Account)
async def create_btc_address(
    sender:"Type[Account]",
    instance:Account,
    created:bool,
    using_db:"Optional[BaseDBAsyncClient]",
    update_fields:List[str]
)->None:
    if created:
        random_string = get_random_string()
        btc_instance = create_bitcoin_wallet_for_user(random_string)
        btc_obj = await BtcAddress.create(
            # un comment for production--------------------------------------------------------------------------------
            # account_balance = btc_instance['wallet_balance'],
            account_balance = 100,
            lock_account_balance=0.00,
            account_network = btc_instance ['account_network'],
            wallet_identifier = btc_instance ['identifier'],
            wallet_address = btc_instance['address'],
            wallet_id = btc_instance['wallet_id'],
            owner = instance
        )
        await btc_pydanticIn.from_tortoise_orm(btc_obj)
# create a new Litecoin Account 
@post_save(Account)
async def create_lite_address(
    sender:"Type[Account]",
    instance:Account,
    created:bool,
    using_db:"Optional[BaseDBAsyncClient]",
    update_fields:List[str]
)->None:
    if created:
        random_string = get_random_string()
        lite_instance = create_litecoin_wallet_for_user(random_string)
        lite_obj = await LiteCoinAddress.create(
            # un comment for production --------------------------------------------------------------------------
            # account_balance = lite_instance['wallet_balance'],
            account_balance = 100,
            lock_account_balance = 0.00,
            account_network = lite_instance ['account_network'],
            wallet_identifier = lite_instance ['identifier'],
            wallet_address = lite_instance['address'],
            wallet_id = lite_instance['wallet_id'],
            owner = instance
        )
        await litecoin_pydanticIn.from_tortoise_orm(lite_obj)
# Create a new DashCoin Account 
@post_save(Account)
async def create_dash_address(
    sender:"Type[Account]",
    instance:Account,
    created:bool,
    using_db:"Optional[BaseDBAsyncClient]",
    update_fields:List[str]
)->None:
    if created:
        random_string = get_random_string()
        dash_instance = create_dash_wallet_for_user(random_string)
        dash_obj = await DashCoinAddress.create(
            # uncomment for prduction --------------------------------------------
            # account_balance = dash_instance['wallet_balance'],
            account_balance =100,
            lock_account_balance =0.00,
            account_network = dash_instance ['account_network'],
            wallet_identifier = dash_instance ['identifier'],
            wallet_address = dash_instance['address'],
            wallet_id = dash_instance['wallet_id'],
            owner = instance
        )
        await dashcoin_pydanticIn.from_tortoise_orm(dash_obj)

# Create a new Eth account
@post_save(Account)
async def create_eth_address(
    sender:"Type[Account]",
    instance:Account,
    created:bool,
    using_db:"Optional[BaseDBAsyncClient]",
    update_fields:List[str]
)->None:
    if created:
        eth_instance = create_eth_account()
        eth_obj = await EthereiumAddress.create(
            # remove this for production -------------------------------------------
            account_balance=100,
            lock_account_balance=0.00,
            wallet_address=eth_instance['account'],
            wallet_key= eth_instance['key'],
            owner = instance
        )
        await eth_pydancticIn.from_tortoise_orm(eth_obj)

# Create a BNB Account
@post_save(Account)
async def create_eth_address(
    sender:"Type[Account]",
    instance:Account,
    created:bool,
    using_db:"Optional[BaseDBAsyncClient]",
    update_fields:List[str]
)->None:
    if created:
        bnb_instance = create_bnb_account()
        bnb_obj = await BNBAddress.create(
            # remove this after testing and demo-------------------------------------
            account_balance=100,
            lock_account_balance=0.00,
            wallet_address=bnb_instance['account'],
            wallet_key= bnb_instance['key'],
            owner = instance
        )
        await bnb_pydancticIn.from_tortoise_orm(bnb_obj)
    
@app.get("/api/v1/")
async def welcome():
    return {"message":"if you can view this then it worksss"}

@app.post("/api/v1/register")
async def user_registeration(user:user_pydanticIn):
    user_info = user.dict(exclude_unset=True)
    # check if the email already exists
    email = user_info["email"]    
    user_instance =await User.filter(email=email).exists()
    if user_instance == True:
        raise HTTPException(status_code=422,detail=f"Account for {email} already exists!!")
    user_info["password"] = get_hashed_password(user_info["password"])
    user_obj = await User.create(**user_info)
    new_user = await user_pydantic.from_tortoise_orm(user_obj)
    return {
        "status":"ok",
        "data": f"Hello {new_user.email} thanks for choosing our service. Please check your email and complete your registration"
    }


# Setup 2FA for account =============================================================================================================================================================




# ==============================================================================================================================resend confirmation code to email during registration
@app.post('/api/v1/resend-verification-code-email')
async def resend_verification_code(user_email):
    # check if the user exists
    user_instance = await User.filter(email=user_email).exists()
    user = await User.get(email=user_email)
    if (user_instance == False):
        raise HTTPException(status_code=404, detail=f"No User with this email found,Please Check Your Email Address")

    # check if the user is already verified 
    if user.is_verified == True:
        raise HTTPException(status_code=400, detail=f"Your Account is already verified,Please proceed to login")

    # user exists 
    await send_mail([user.email],user)
    return {"message":"verification code sent"}


templates = Jinja2Templates(directory="app/templates")
@app.get("/api/v1/verification",response_class=HTMLResponse)
async def email_verification(request:Request, token:str):
    user = await verify_token(token)
    if user and not user.is_verified:
        user.is_verified = True
        await user.save()
        return templates.TemplateResponse("verification.html",{"request":request,"email":user.email})
    raise HTTPException(status_code=404,
        detail="Invalid token or Expired token",
        headers={"WWW-Authenticate":"Bearer"})


@app.post("/api/v1/user/uploadimage")
async def create_upload_file(token:str = Depends(oauth2_scheme),file:UploadFile=File(...),user:user_pydanticIn = Depends(get_current_user)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    FILEPATH = "./app/static/images/"
    filename = file.filename
    extension = filename.split(".")[1]

    if extension not in ["png","jpg","jpeg"]:
        return {"status":"error","detail":"file extension not allowed"}
    token_name = secrets.token_hex(16) + "." + extension
    generated_name =  FILEPATH + token_name
    file_content = await file.read()

    with open(generated_name,"wb") as file:
        file.write(file_content)

    img = Image.open(generated_name)
    img = img.resize(size=(200,200))
    img.save(generated_name)
    file.close()

    account = await Account.get(owner = user)
    owner = await account.owner
    if owner == user:
        account.profile_image = token_name
        await account.save()
    else:
        raise HTTPException(status_code=400,detail="Not Authorized to perform this action")
    file_url = "https://localhost:8000" + generated_name[1:]
    return {"status":"ok","filename":file_url}


# A Periodic endpoint that calls every 15 minutes upon startup of the server 
@app.on_event("startup")
@repeat_every(seconds=60*3)
async def get_live_data():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
  'start':'1',
  'limit':'50',
  'convert':'USD'
    }
    headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'f41f95d8-3b1e-4c51-af9d-623c339d9ffb',
    }

    session = Session()
    session.headers.update(headers)

    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    _data = data['data']
    data_dict = []
    print(data_dict)
    # check the database for current price list and clear existing list of data
    _current= await Livedata.all()
    if len(_current) > 0:
        await Livedata.all().delete()
    # save a new set of data
    for _ in _data:
        _price=float(_['quote']['USD']['percent_change_24h'])

        percentile = str(round(float(_['quote']['USD']['percent_change_24h']),2))+"%"
        current_price=_['quote']['USD']['price']
        if _price > current_price:
            arrow ='UP'
        else:
            arrow = 'DOWN'
        
        # IMAGES URL 
        symbol = _['symbol']
        if symbol == 'BTC':
            asset_url = images_url['BTC']
        elif symbol == 'ETH':
            asset_url = images_url['ETH']
        elif symbol == 'DASH':
            asset_url = images_url['DASHCOIN']
        elif symbol == 'LTC':
            asset_url = images_url['LITECOIN']
        elif symbol == 'BNB':
            asset_url = images_url['BNB']
        elif symbol == 'SHIB':
            asset_url = images_url['SHIB']
        elif symbol == 'TRX':
            asset_url = images_url['TRX']
        elif symbol == 'USDT':
            asset_url = images_url['USDT']
        elif symbol == 'DOGE':
            asset_url = images_url['DOGECOIN']
        elif symbol == 'BCH':
            asset_url = images_url['BITCOINCASH']
        else:
            asset_url= images_url['ERC20']
        


        option=await Livedata.create(name=_['name'],symbol=_['symbol'],current_price=_['quote']['USD']['price'],price_change=percentile,arrow=arrow,asset_url=asset_url)
        await live_dataIn.from_tortoise_orm(option)                   
        iten = {
            'name':_['name'],
            'symbol':_['symbol'],
            'current_price':_['quote']['USD']['price'],
            'price_change':float(_['quote']['USD']['price'])+float(_['quote']['USD']['percent_change_1h'])
        }
        data_dict.append(iten)
    
    # print(data_dict)
    return data_dict


@app.get("/api/v1/live-data")
async def get_live_price():
    # data = await get_live_data() 
    _price = await Livedata.all()
    # print(_price)
    return {'price':_price}
             
@app.post("/api/v1/login")
async def login_user(user_credentials:LoginSchema):
    user = await User.get(email=user_credentials.email).first()
    # un comment this for production =============================================================================== VIEW THIS BEFORE UPLOADING TO SERVER================
    if user.is_verified == False:
        raise HTTPException(status_code=400,detail="Your account has not been verified")
    if not user:
        raise HTTPException(status_code=404,detail=f"Invalid Login Credential")
    if not verify_password(user_credentials.password,user.password):
        raise HTTPException(status_code=404,detail=f"Invalid Login Credential")
    token  = await token_generator(email=user_credentials.email,password=user_credentials.password)   
    return {"access_token":token,"token_type":"bearer"}

@app.post("/api/v1/logout")
async def logout_user(token:str=Depends(get_current_token),user:user_pydanticIn=Depends(get_current_user)):
    if add_blacklist_token(token):
        return ({'result': True,"message":"User Logged out successfully"})
    

@app.post("/api/v1/forget-password")
async def forget_password(request:ForgetPassword):
    result = await User.get(email=request.email)
    # print(result)
    if not result:
        return HTTPException(status_code=404,detail="User not found")
    reset_code = random_with_N_digits(6)
    await Py_codes.create(email=request.email,reset_code=reset_code)
    print(request.email)
    send_reset_password(request.email,reset_code)
    # print(result.email)
    return {"status":"Okay","reset code":reset_code}

@app.patch("/api/v1/reset-password")
async def reset_password(request:Resetpassword):
    reset_token = await Py_codes.get(reset_code=request.reset_password_token)
    if not reset_token:
        raise HTTPException(status_code=404,detail=f"Invalid Request")
    if request.new_password != request.confirm_password:
        raise HTTPException(status_code=404,detail=f"The Password entered does not match")
    # new hashed password
    new_hashed_password = get_hashed_password(request.new_password)
    # gets the current user
    user_field = await User.get(email=request.email)
    # update the password there
    user_field.password = new_hashed_password
    # save the password
    await user_field.save()
    if not user_field:
        raise HTTPException(status_code=404,detail="User Does not exist")
    return {"message":"password reset sucessfully"}


@app.post('/api/v1/send-btc')
async def send_btc_coin(receivers_account:str,amount:str,user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    # get the current user details from the database 
    account = await BtcAddress.get(owner = user)
    identifier = account.wallet_identifier
    # get the current user bitcoin wallet
    wallet_instance = Wallet(identifier)
    # get balane and see if its greater than the sending amount
    current_balance = wallet_instance.as_dict()['main_balance']
    if float(current_balance) < float(amount):
        return {"message":"inSufficient Funds, Please Fund your account!!","available_balance":current_balance}
    wallet_instance.scan()
    wallet_instance.send_to(receivers_account,amount, network='bitcoin')
    wallet_instance.info()
    data = wallet_instance.info()
    obj = await BTCTransactionHistory.create(value=amount,receiving_address=receivers_account,owner=user)
    await btc_transaction_pydanticIn.from_tortoise_orm(obj)
    return {"message":"Your Transaction is on its way!!","data":data.as_dict()}

@app.post('/api/v1/send-lite-coin')
async def send_lite_coin(receivers_account:str,amount:str,user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    # get the current user details from the database 
    account = await LiteCoinAddress.get(owner = user)
    identifier = account.wallet_identifier
    # get the current user bitcoin wallet
    wallet_instance = Wallet(identifier)
    current_balance = wallet_instance.as_dict()['main_balance']
    if float(current_balance) < float(amount):
        return {"message":"inSufficient Funds, Please Fund your account!!","available_balance":current_balance}
    # get Senders/ User address
    wallet_instance.send_to(receivers_account,amount, network='litecoin')
    # transaction = Input()
    wallet_instance.scan()
    wallet_instance.info()
    data = wallet_instance.info()
    obj = await LiteCoinTransactionHistory.create(value=amount,receiving_address=receivers_account,owner=user)
    await lite_transaction_pydanticIn.from_tortoise_orm(obj)
    return {"message":"Your Transaction is on its way!!","data":data.as_dict()}


@app.post('/api/v1/send-dash-coin')
async def send_dash_coin(receivers_account:str,amount:str,user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    # get the current user details from the database 
    account = await DashCoinAddress.get(owner = user)
    identifier = account.wallet_identifier
    # get the current user bitcoin wallet
    wallet_instance = Wallet(identifier)
    current_balance = wallet_instance.as_dict()['main_balance']
    if float(current_balance) < float(amount):
        return {"message":"inSufficient Funds, Please Fund your account!!","available_balance":current_balance}
    wallet_instance.send_to(receivers_account,amount)
    wallet_instance.scan()
    data = wallet_instance.info()
    obj = await DashCoinTransactionHistory.create(value=amount,receiving_address=receivers_account,owner=user)
    await dash_transaction_pydanticIn.from_tortoise_orm(obj)
    return {"message":"Your Transaction is on its way!!","data":data.as_dict()}


@app.post('/api/v1/send-eth')
async def send_eth(receiver,amount,user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    account = await EthereiumAddress.get(owner=user)
    sender = account.wallet_address
    print(sender)
    balance = get_account_balance(sender)
    print(balance)
    if balance < float(amount):
        return {"message":"Insufficient Funds!!","avaialable_balance":balance}
    hash = send_eth_transfer(sender,receiver,amount)
    receipt = get_transaction_receipt(hash)
    obj = await EtheriumTransactionHistory.create(value=receipt['value'],receiving_address=receipt['receiving_address'],owner=user)
    await eth_transaction_pydanticIn.from_tortoise_orm(obj)
    return {"message":"your transaction is on its way","receipt":receipt}


@app.post('/api/v1/send-bnb')
async def send_eth(receiver,amount,user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    account = await BNBAddress.get(owner=user)
    sender = account.wallet_address
    print(sender)
    balance = get_account_balance(sender)
    print(balance)
    if balance < float(amount):
        return {"message":"Insufficient Funds!!","avaialable_balance":balance}
    hash = send_bnb(sender,receiver,amount)
    receipt = get_bnb_transaction_receipt(hash)
    return {"message":"your transaction is on its way","receipt":receipt}

@app.get('/api/v1/receive-btc-coin')
async def receive_btc_coin(user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    account = await BtcAddress.get(owner = user)
    identifier = account.wallet_identifier
    # # get the current user bitcoin wallet
    wallet_instance = Wallet(identifier)
    btc_balance = wallet_instance.as_dict()['main_balance']
    # # get Senders/ User address
    address = wallet_instance.addresslist()[0]
    print(address)
    return {"address":"Please send to the account to avoid loss, We Will not be responsible for your loss","account":address,"expecting_coin":"BTC","Available_balance":btc_balance}


@app.get('/api/v1/receive-lite-coin')
async def receive_lite_coin(user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    # Filter the database for the wallet
    account = await LiteCoinAddress.get(owner = user)
    identifier = account.wallet_identifier
    # # get the current user bitcoin wallet
    wallet_instance = Wallet(identifier)
    # User address
    lite_balance = wallet_instance.as_dict()['main_balance']
    address = wallet_instance.addresslist()[0]
    # print(address)
    return {"address":"Please send to the account to avoid loss, We Will not be responsible for your loss","account":address,"expecting_coin":"Litecoin","Available_balance":lite_balance}

@app.get('/api/v1/receive-dash-coin')
async def receive_dash_coin(user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    # Filter the database for the wallet
    account = await DashCoinAddress.get(owner = user)
    identifier = account.wallet_identifier
    # # get the current user bitcoin wallet
    wallet_instance = Wallet(identifier)
    # User address
    dash_balance = wallet_instance.as_dict()['main_balance']
    address = wallet_instance.addresslist()[0]
    print(address)
    return {"message":"Please send to the account to avoid loss, We Will not be responsible for your loss","account":address,"expecting_coin":"Dash Coin","Available_balance":dash_balance}

@app.get('/api/v1/receive-eth')
async def receive_eth(user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    account = await EthereiumAddress.get(owner=user)
    address = account.wallet_address
    eth_balance = get_account_balance(address)
    return {"message":"Please Send ETH to this address to avoid loss, We Will not be responsible for your loss", "account":address,"expecting_coin":"ETH","Available_balance":eth_balance}

@app.get('/api/v1/receive-bnb')
async def receive_bnb(user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    account = await BNBAddress.get(owner=user)
    address = account.wallet_address
    bnb_balance = get_bnb_balance(address)
    return {"message":"Please Send BNB to this address to avoid loss, We Will not be responsible for your loss", "account":address,"expecting_coin":"BNB","Available_balance":bnb_balance}

# Get all Transaction History
@app.get('/api/v1/get-eth-history')
async def get_eth_history(user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    account = await EthereiumAddress.get(owner=user)
    address = account.wallet_address
    balance = get_account_balance(address)
    transaction_history = get_transactions(address)
    return {"balance":balance,"message":"Transaction History","transactions":transaction_history}



# Get all Transaction History
@app.get('/api/v1/get-bnb-history')
async def get_bnb_history(user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    account = await BNBAddress.get(owner=user)
    address = account.wallet_address
    balance = get_bnb_balance(address)
    transaction_history = get_transactions(address)
    if len(transaction_history) == 0:
        return {"message":"No Transactions performed yet all your transactions will appear here"}
    return {"balance":balance,"message":"Transaction History","transactions":transaction_history}




@app.get('/api/v1/get-btc-transaction-history')
async def get_btc_history(user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    account = await BtcAddress.get(owner = user)
    identifier = account.wallet_identifier
    # # get the current user bitcoin wallet
    wallet_instance = Wallet(identifier)
    # data = wallet_instance.as_dict()
    transactions = wallet_instance.transactions(identifier)
    if len(transactions) == 0:
        return {"message":"No Transactions performed yet all your transactions will appear here"}
    return {"message":"Transaction History","transactions":transactions}

@app.get('/api/v1/get-dash-history')
async def get_dash_history(user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    account = await DashCoinAddress.get(owner = user)
    identifier = account.wallet_identifier
    # # get the current user bitcoin wallet
    wallet_instance = Wallet(identifier)
    # data = wallet_instance.as_dict()
    transactions = wallet_instance.transactions(identifier)
    if len(transactions) == 0:
        return {"message":"No Transactions performed yet all your transactions will appear here"}
    return {"message":"Transaction History","transactions":transactions}

@app.get('/api/v1/get-lite-history')
async def get_lite_history(user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    account = await LiteCoinAddress.get(owner = user)
    identifier = account.wallet_identifier
    # # get the current user bitcoin wallet
    wallet_instance = Wallet(identifier)
    # data = wallet_instance.as_dict()
    transactions = wallet_instance.transactions(identifier)
    if len(transactions) == 0:
        return {"message":"No Transactions performed yet all your transactions will appear here"}
    return {"message":"Transaction History","transactions":transactions}






# candle sticks endpoints
@app.get('/api/v1/klines/')
async def btc_to_usdt():
    return {"message":"This enpoints get klines/candlesticks"} 

    
@app.get('/api/v1/klines-test/{currency}/{interval}')
async def test_end_point(currency:str,interval:str):
    upper = currency.upper()
    PARAMS = f'?symbol={upper}&interval={interval}'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

# ========================================================================================================================================================================
# TEST TRADE

@app.post('/api/v1/trade/market/buy-test-trade-bnbbtc')
async def buy_test_trade(quantity,user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    owner = await Account.get(owner=user)
    # get biitcoin_dummy_account 
    btc_account_instance = await BtcAddress.get(owner=user)
    btc_balance = btc_account_instance.account_balance

    # get bnb_dummby_account
    bnb_account_instance = await BNBAddress.get(owner=user)
    bnb_balance = bnb_account_instance.account_balance

    if quantity[::-1].find('.') > 2:
        raise HTTPException(status_code=400,detail="Maximum is 2 Decimal place")
    if float(quantity) < 0.02:
        raise HTTPException(status_code=400,detail="Minimum Vaue is 0.3")
    order = buy_order(quantity,'BNBBTC')

    # convert bnb to btc and remove from the btc acoount 
    btc_remove = bnb_btc(quantity)

    new_btc_balance = float(btc_balance) - btc_remove
    btc_balance=new_btc_balance
    action = await BtcAddress.filter(owner=user).update(account_balance=new_btc_balance)

    # asking price 
    _asking=bnb_info
    # update the bnb account balance
    new_bnb_balance= float(bnb_balance) + float(quantity)
    bnb_balance = new_bnb_balance
    action = await BNBAddress.filter(owner=user).update(account_balance=new_bnb_balance)

    # save a copy of the trade for transaction history purpose
    trade_obj = await BnbBtcTradeHistory.create(
        symbol=order['symbol'],
        side = order['side'],
        trade_status=order['status'],
        quantity=order['origQty'],
        order_id=order['orderId'],
        trade_type=order['type'], 
        asking_price=_asking['price'],
        owner = owner
    )
    await bnb_trade_history_pydantic.from_tortoise_orm(trade_obj)
    return {"status":"success","order_id":order['orderId'],'symbol':order['symbol'],'buy_quantity':order['origQty'],"bnb_balance":bnb_balance,"btc_balance":btc_balance,'trade_type':order['type']}

@app.post('/api/v1/trade/market/sell-test-trade-bnbbtc')
async def sell_test_trade(quantity,user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    owner = await Account.get(owner=user)
    # get biitcoin_dummy_account 
    btc_account_instance = await BtcAddress.get(owner=user)
    btc_balance = btc_account_instance.account_balance
    
    # get bnb_dummby_account
    bnb_account_instance = await BNBAddress.get(owner=user)
    bnb_balance = bnb_account_instance.account_balance


    if quantity[::-1].find('.') > 2:
        raise HTTPException(status_code=400,detail="Maximum is 2 Decimal place")

    if float(quantity) < 0.02:
        raise HTTPException(status_code=400,detail="Minimum Vaue is 0.3")
    order = sell_order(quantity,'BNBBTC')
    # convert bnb to btc and remove from the btc acoount 
    btc_remove = bnb_btc(quantity)
    new_btc_balance = float(btc_balance) + btc_remove
    _asking=bnb_info
    btc_balance=new_btc_balance
    action = await BtcAddress.filter(owner=user).update(account_balance=new_btc_balance)
    # update the bnb account balance
    new_bnb_balance= float(bnb_balance) - float(quantity)
    bnb_balance=new_bnb_balance
    action = await BNBAddress.filter(owner=user).update(account_balance=new_bnb_balance)

    # save a copy of the trade for transaction history purpose
    trade_obj = await BnbBtcTradeHistory.create(
        symbol=order['symbol'],
        side = order['side'],
        trade_status=order['status'],
        quantity=order['origQty'],
        order_id=order['orderId'],
        trade_type=order['type'],
        asking_price=_asking['price'],
        owner = owner
    )
    await bnb_trade_history_pydantic.from_tortoise_orm(trade_obj)
    return {"status":"success","order_id":order['orderId'],'symbol':order['symbol'],'sell_quantity':order['origQty'],"bnb_balance":bnb_balance,"btc_balance":btc_balance,'trade_type':order['type']}



@app.post('/api/v1/trade/market/buy-test-trade-ethbtc')
async def buy_test_trade(quantity,user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    owner = await Account.get(owner=user)
    # get biitcoin_dummy_account 
    btc_account_instance = await BtcAddress.get(owner=user)
    btc_balance = btc_account_instance.account_balance

    # get bnb_dummby_account
    eth_account_instance = await EthereiumAddress.get(owner=user)
    eth_balance = eth_account_instance.account_balance
    _asking=eth_info

    if BuyTrade.quantity[::-1].find('.') > 2:
        raise HTTPException(status_code=400,detail="Maximum is 2 Decimal place")
    if float(quantity) < 0.02:
        raise HTTPException(status_code=400,detail="Minimum Vaue is 0.3")
    order = buy_order(quantity,'ETHBTC')

    # convert eth to btc and remove from the btc acoount 
    btc_remove = eth_btc(quantity)

    new_btc_balance = float(btc_balance) - btc_remove
    btc_balance=new_btc_balance
    action = await BtcAddress.filter(owner=user).update(account_balance=new_btc_balance)

    # update the eth account balance
    new_eth_balance= float(eth_balance) + float(quantity)
    eth_balance = new_eth_balance
    action = await EthereiumAddress.filter(owner=user).update(account_balance=new_eth_balance)

    # save a copy of the trade for transaction history purpose
    trade_obj = await EthBtcTradeHistory.create(
        symbol=order['symbol'],
        side = order['side'],
        trade_status=order['status'],
        quantity=order['origQty'],
        order_id=order['orderId'], 
        asking_price=_asking['price'],
        trade_type=order['type'],
        owner = owner
    )
    await eth_trade_history_pydantic.from_tortoise_orm(trade_obj)
    return {"status":"success","order_id":order['orderId'],'symbol':order['symbol'],'buy_quantity':order['origQty'],"eth_balance":eth_balance,"btc_balance":btc_balance,'trade_type':order['type']}



@app.post('/api/v1/trade/market/sell-test-trade-ethbtc')
async def sell_test_trade(quantity,user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    owner = await Account.get(owner=user)
    # get biitcoin_dummy_account 
    btc_account_instance = await BtcAddress.get(owner=user)
    btc_balance = btc_account_instance.account_balance

    # get bnb_dummby_account
    eth_account_instance = await EthereiumAddress.get(owner=user)
    eth_balance = eth_account_instance.account_balance

    if quantity[::-1].find('.') > 2:
        raise HTTPException(status_code=400,detail="Maximum is 2 Decimal place")
    if float(quantity) < 0.02:
        raise HTTPException(status_code=400,detail="Minimum Vaue is 0.3")
    order = sell_order(quantity,'ETHBTC')

    # convert eth to btc and remove from the btc acoount 
    btc_remove = eth_btc(quantity)

    new_btc_balance = float(btc_balance) + btc_remove
    btc_balance=new_btc_balance
    action = await BtcAddress.filter(owner=user).update(account_balance=new_btc_balance)
    _asking=eth_info

    # update the eth account balance
    new_eth_balance= float(eth_balance) - float(quantity)
    eth_balance = new_eth_balance
    action = await EthereiumAddress.filter(owner=user).update(account_balance=new_eth_balance)

    # save a copy of the trade for transaction history purpose
    trade_obj = await EthBtcTradeHistory.create(
        symbol=order['symbol'],
        side = order['side'],
        quantity=order['origQty'],
        trade_status=order['status'],
        order_id=order['orderId'], 
        asking_price=_asking['price'],
        trade_type=order['type'],
        owner = owner
    )
    await eth_trade_history_pydantic.from_tortoise_orm(trade_obj)
    return {"status":"success","order_id":order['orderId'],'symbol':order['symbol'],'sell_quantity':order['origQty'],"eth_balance":eth_balance,"btc_balance":btc_balance,'trade_type':order['type']}

@app.post('/api/v1/trade/market/buy-test-trade-ltcbtc')
async def buy_test_trade(quantity,user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    owner = await Account.get(owner=user)
    # quantity=BuyTrade.quantity
    # get biitcoin_dummy_account 
    btc_account_instance = await BtcAddress.get(owner=user)
    btc_balance = btc_account_instance.account_balance

    # get ltc_dummby_account
    ltc_account_instance = await LiteCoinAddress.get(owner=user)
    ltc_balance = ltc_account_instance.account_balance

    if quantity[::-1].find('.') > 2:
        raise HTTPException(status_code=400,detail="Maximum is 2 Decimal place")
    if float(quantity) < 0.02:
        raise HTTPException(status_code=400,detail="Minimum Vaue is 0.3")
    order = buy_order(quantity,'LTCBTC')

    _asking=ltc_info

    # convert ltc to btc and remove from the btc acoount 
    btc_remove = ltc_btc(quantity)

    new_btc_balance = float(btc_balance) - btc_remove
    btc_balance=new_btc_balance
    action = await BtcAddress.filter(owner=user).update(account_balance=new_btc_balance)

    # update the eth account balance
    new_lite_balance= float(ltc_balance) + float(quantity)
    ltc_balance = new_lite_balance
    action = await LiteCoinAddress.filter(owner=user).update(account_balance=new_lite_balance)

    # save a copy of the trade for transaction history purpose
    trade_obj = await LtcBtcTradeHistory.create(
        symbol=order['symbol'],
        side = order['side'],
        quantity=order['origQty'],
        trade_status=order['status'],
        order_id=order['orderId'], 
        trade_type=order['type'],
        asking_price=_asking['price'],
        owner = owner
    )
    await ltc_trade_history_pydantic.from_tortoise_orm(trade_obj)
    return {"status":"success","order_id":order['orderId'],'symbol':order['symbol'],'buy_quantity':order['origQty'],"ltc_balance":ltc_balance,"btc_balance":btc_balance,'trade_type':order['type']}


@app.post('/api/v1/trade/market/sell-test-trade-ltcbtc')
async def sell_test_trade(quantity,user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    owner = await Account.get(owner=user)
    # quantity=BuyTrade.quantity
    # get biitcoin_dummy_account 
    btc_account_instance = await BtcAddress.get(owner=user)
    btc_balance = btc_account_instance.account_balance

    # get ltc_dummby_account
    ltc_account_instance = await LiteCoinAddress.get(owner=user)
    ltc_balance = ltc_account_instance.account_balance

    if quantity[::-1].find('.') > 2:
        raise HTTPException(status_code=400,detail="Maximum is 2 Decimal place")
    if float(quantity) < 0.02:
        raise HTTPException(status_code=400,detail="Minimum Vaue is 0.3")
    order = sell_order(quantity,'LTCBTC')

    # convert eth to btc and remove from the btc acoount 
    btc_add = ltc_btc(quantity)
    _asking=ltc_info
    
    new_btc_balance = float(btc_balance) + btc_add
    btc_balance=new_btc_balance
    action = await BtcAddress.filter(owner=user).update(account_balance=new_btc_balance)

    # update the ltc account balance
    new_ltc_balance= float(ltc_balance) - float(quantity)
    ltc_balance = new_ltc_balance
    action = await LiteCoinAddress.filter(owner=user).update(account_balance=new_ltc_balance)

    # save a copy of the trade for transaction history purpose
    trade_obj = await LtcBtcTradeHistory.create(
        symbol=order['symbol'],
        side = order['side'],
        quantity=order['origQty'],
        trade_status=order['status'],
        order_id=order['orderId'], 
        trade_type=order['type'],
        asking_price=_asking['price'],
        owner = owner
    )
    await ltc_trade_history_pydantic.from_tortoise_orm(trade_obj)
    return {"status":"success","order_id":order['orderId'],'symbol':order['symbol'],'sell_quantity':order['origQty'],"ltc_balance":ltc_balance,"btc_balance":btc_balance,'trade_type':order['type']}


# limit trading=====================================================================================================================================================================
@app.post('/api/v1/trade/limit/buy-test-trade-bnbbtc')
async def buy_test_trade(quantity,limit_price,user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    owner = await Account.get(owner=user)
    # get biitcoin_dummy_account 
    btc_account_instance = await BtcAddress.get(owner=user)
    btc_balance = btc_account_instance.account_balance
    lock_balance= btc_account_instance.lock_account_balance
    # place the order
    try:
        order=buy_limit_order('BNBBTC',quantity,limit_price)
    except:
        raise HTTPException(status_code=400,detail=f"Please Check the Price and Quantity Then Try Again")
    # get the current accountof btc and lock it 
    lock_btc_amount = bnb_btc(float(quantity))
    # remove the amount from the main account and place it in the lock account
    remain_btc_balance = float(btc_balance)-float(lock_btc_amount)
    _asking=bnb_info

    lock_balance=float(lock_btc_amount)+float(lock_balance)
    action = await BtcAddress.filter(owner=user).update(account_balance=remain_btc_balance,lock_account_balance=lock_balance)
    # add it to transaction history 
    trade_obj = await BnbBtcTradeHistory.create(
        symbol=order['symbol'],
        side = order['side'],
        quantity=order['origQty'],
        trade_status=order['status'],
        order_id=order['orderId'], 
        trade_type=order['type'],
        asking_price=_asking['price'],
        lock_amount_for_transaction = float(lock_btc_amount),
        owner = owner
    )
    await bnb_trade_history_pydantic.from_tortoise_orm(trade_obj)
    return {"status":"success","order_id":order['orderId'],'symbol':order['symbol'],'buy_quantity':order['origQty'],"lock_BTC_balance":lock_balance,"btc_balance":btc_balance,'trade_type':order['type']}


# =====================================================================================================================================================================================
@app.post('/api/v1/trade/limit/buy-test-trade-ethbtc')
async def buy_test_trade(quantity,limit_price,user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    owner = await Account.get(owner=user)
    # get biitcoin_dummy_account 
    btc_account_instance = await BtcAddress.get(owner=user)
    btc_balance = btc_account_instance.account_balance
    lock_balance= btc_account_instance.lock_account_balance
    # place the order
    try:
        order=buy_limit_order('ETHBTC',quantity,limit_price)
    except:
        raise HTTPException(status_code=400, detaul=f"Please Check The Price and Quantity Then Try Again")
    # get the current accountof btc and lock it 
    lock_btc_amount = eth_btc(float(quantity))
    # remove the amount from the main account and place it in the lock account
    remain_btc_balance = float(btc_balance)-float(lock_btc_amount)
    _asking=eth_info

    lock_balance=float(lock_btc_amount)+float(lock_balance)
    action = await BtcAddress.filter(owner=user).update(account_balance=remain_btc_balance,lock_account_balance=lock_balance)
    # add it to transaction history 
    trade_obj = await EthBtcTradeHistory.create(
        symbol=order['symbol'],
        side = order['side'],
        quantity=order['origQty'],
        trade_status=order['status'],
        order_id=order['orderId'], 
        trade_type=order['type'],
        asking_price=_asking['price'],
        lock_amount_for_transaction = float(lock_btc_amount),
        owner = owner
    )
    await eth_trade_history_pydantic.from_tortoise_orm(trade_obj)
    return {"status":"success","order_id":order['orderId'],'symbol':order['symbol'],'buy_quantity':order['origQty'],"lock_BTC_balance":lock_balance,"btc_balance":btc_balance,'trade_type':order['type']}


# =====================================================================================================================================================================================
@app.post('/api/v1/trade/limit/buy-test-trade-ltcbtc')
async def buy_test_trade(quantity,limit_price,user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    owner = await Account.get(owner=user)
    # get biitcoin_dummy_account 
    btc_account_instance = await BtcAddress.get(owner=user)
    btc_balance = btc_account_instance.account_balance
    lock_balance= btc_account_instance.lock_account_balance
    # place the order
    try:
        order=buy_limit_order('LTCBTC',quantity,limit_price)
    except:
        raise HTTPException(status_code=f"Please Check the Price and Quantity Then Try Again")
    # get the current accountof btc and lock it 
    lock_btc_amount = ltc_btc(float(quantity))
    # remove the amount from the main account and place it in the lock account
    remain_btc_balance = float(btc_balance)-float(lock_btc_amount)
    _asking=ltc_info

    lock_balance=float(lock_btc_amount)+float(lock_balance)
    action = await BtcAddress.filter(owner=user).update(account_balance=remain_btc_balance,lock_account_balance=lock_balance)
    # add it to transaction history 
    trade_obj = await LtcBtcTradeHistory.create(
        symbol=order['symbol'],
        side = order['side'],
        trade_status=order['status'],
        quantity=order['origQty'],
        order_id=order['orderId'], 
        trade_type=order['type'],
        asking_price=_asking['price'],
        lock_amount_for_transaction = float(lock_btc_amount),
        owner = owner
    )
    await ltc_trade_history_pydantic.from_tortoise_orm(trade_obj)
    return {"status":"success","order_id":order['orderId'],'symbol':order['symbol'],'buy_quantity':order['origQty'],"lock_BTC_balance":lock_balance,"btc_balance":btc_balance,'trade_type':order['type']}

# ===================================================================================================================================================================================

@app.post('/api/v1/trade/limit/sell-test-trade-bnbbtc')
async def buy_test_trade(quantity,limit_price,user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    owner = await Account.get(owner=user)
    # get bnb account
    bnb_account_instance=await BNBAddress.get(owner=user)
    bnb_balance=bnb_account_instance.account_balance
    bnb_lock_balance= bnb_account_instance.lock_account_balance
    try:
    # place the order
        order=sell_limit_order('BNBBTC',quantity,limit_price)
    except:
        raise HTTPException(status_code=400,detail=f"Please Check The Price and Quantity then Try Again")
    # get the current accountof btc and lock it 
    lock_bnb_value = float(bnb_lock_balance)+float(quantity)
    remaining_bnb_balance = float(bnb_balance) -float(quantity)
    _asking=bnb_info

    # remove the amount from the main account and place it in the lock account
    action = await BNBAddress.filter(owner=user).update(account_balance=remaining_bnb_balance,lock_account_balance=lock_bnb_value)
    # add it to transaction history 
    trade_obj = await BnbBtcTradeHistory.create(
        symbol=order['symbol'],
        side = order['side'],
        trade_status=order['status'],
        quantity=order['origQty'],
        order_id=order['orderId'], 
        trade_type=order['type'],
        asking_price=_asking['price'],
        lock_amount_for_transaction =float(quantity),
        owner = owner
    )
    await bnb_trade_history_pydantic.from_tortoise_orm(trade_obj)
    return {"status":"success","order_id":order['orderId'],'symbol':order['symbol'],'sell_quantity':order['origQty'],"lock_balance":lock_bnb_value,"bnb_balance":bnb_balance,'trade_type':order['type']}

# ====================================================================================================================================================================================
@app.post('/api/v1/trade/limit/sell-test-trade-ethbtc')
async def buy_test_trade(quantity,limit_price,user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    owner = await Account.get(owner=user)

    # get bnb account
    eth_account_instance=await EthereiumAddress.get(owner=user)
    eth_balance=eth_account_instance.account_balance
    eth_lock_balance= eth_account_instance.lock_account_balance  
    try:
    # place the order
        order=sell_limit_order('ETHBTC',quantity,limit_price)
    except:
        raise HTTPException("Please Check The Price and Quantity then Try Again")
    # get the current accountof btc and lock it 
    lock_eth_value = float(eth_lock_balance)+float(quantity)
    remaining_eth_balance = float(eth_balance) -float(quantity)
    _asking=eth_info

    # remove the amount from the main account and place it in the lock account
    action = await EthereiumAddress.filter(owner=user).update(account_balance=remaining_eth_balance,lock_account_balance=lock_eth_value)
    # add it to transaction history 
    trade_obj = await EthBtcTradeHistory.create(
        symbol=order['symbol'],
        side = order['side'],
        quantity=order['origQty'],
        trade_status=order['status'],
        order_id=order['orderId'], 
        trade_type=order['type'],
        asking_price=_asking['price'],
        lock_amount_for_transaction =float(quantity),
        owner = owner
    )
    await eth_trade_history_pydantic.from_tortoise_orm(trade_obj)
    return {"status":"success","order_id":order['orderId'],'symbol':order['symbol'],'sell_quantity':order['origQty'],"lock_balance":lock_eth_value,"eth_balance":eth_balance,'trade_type':order['type']}

# ======================================================================================================================================================================================
@app.post('/api/v1/trade/limit/sell-test-trade-ltcbtc')
async def buy_test_trade(quantity,limit_price,user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    owner = await Account.get(owner=user)
   
    # get bnb account
    ltc_account_instance=await LiteCoinAddress.get(owner=user)
    ltc_balance=ltc_account_instance.account_balance
    ltc_lock_balance= ltc_account_instance.lock_account_balance  

    # place the order
    try:
        order=sell_limit_order('LTCBTC',quantity,limit_price)
    except: 
        raise HTTPException(status_code=400,detail=f"Please Check the Limit Price and Try Again")
    # get the current accountof btc and lock it 
    lock_ltc_value = float(ltc_lock_balance)+float(quantity)
    remaining_ltc_balance = float(ltc_balance) - float(quantity)
    _asking=ltc_info

    # remove the amount from the main account and place it in the lock account
    action = await LiteCoinAddress.filter(owner=user).update(account_balance=remaining_ltc_balance,lock_account_balance=lock_ltc_value)
    # add it to transaction history 
    trade_obj = await LtcBtcTradeHistory.create(
        symbol=order['symbol'],
        side = order['side'],
        quantity=order['origQty'],
        trade_status=order['status'],
        order_id=order['orderId'], 
        trade_type=order['type'],
        asking_price=_asking['price'],
        lock_amount_for_transaction =float(quantity),
        owner = owner
    )
    await ltc_trade_history_pydantic.from_tortoise_orm(trade_obj)
    return {"status":"success","order_id":order['orderId'],'symbol':order['symbol'],'sell_quantity':order['origQty'],"lock_balance":lock_ltc_value,"ltc_balance":ltc_balance,'trade_type':order['type']}

# ==============================================================================================================================================================================
@app.post('/api/v1/trade/limit/status-bnbbtc')
async def get_trade_status(order_id,user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    # get btc address 
    btc_account = await BtcAddress.get(owner=user)
    btc_main_account = btc_account.account_balance
    btc_locked_account = btc_account.lock_account_balance

    # get bnb address
    bnb_account = await BNBAddress.get(owner=user)
    bnb_main_account = bnb_account.account_balance 
    bnb_locked_account = bnb_account.lock_account_balance

    # fetch that transaction history from db and get the lock value that was kept 
    history = await BnbBtcTradeHistory.get(order_id=order_id)
    locked_amount = history.lock_amount_for_transaction

    status=order_status(order_id,'BNBBTC')
    print(status)
    executed_quantity = status['executedQty']
    original_quantity = status['origQty']
    order_symbol = status['symbol']
    order_side=status['side']

    if status['status']=='FILLED':
        if order_side == 'BUY' and order_symbol == 'BNBBTC':
            update_btc_balance = float(btc_main_account + locked_amount) - float(bnb_btc(executed_quantity))
            update_bnb_balance = float(bnb_main_account) + float(executed_quantity)
            lock_balance = float(btc_locked_account) -float(locked_amount)

            bnb_action = await BNBAddress.filter(owner=user).update(account_balance=update_bnb_balance) 
            btc_action = await BtcAddress.filter(owner=user).update(account_balance=update_btc_balance,lock_account_balance=lock_balance)

            data = {
            "status":status['status'],
            "price":status['price'],
            "order_type":status['type'],
            "order_quantity":status['origQty'],
            "symbol":order_symbol
            }
            return {"data":data}
            

        if order_side == 'SELL' and order_symbol == 'BNBBTC':
            update_btc_balance = float(btc_main_account) +float(bnb_btc(executed_quantity))
            update_bnb_balance = float(bnb_main_account) + float(locked_amount -executed_quantity)
            lock_balance = float(bnb_locked_account) - float(locked_amount)
            
            bnb_action = await BNBAddress.filter(owner=user).update(account_balance=update_bnb_balance,lock_account_balance=lock_balance) 
            btc_action = await BtcAddress.filter(owner=user).update(account_balance=update_btc_balance)
            data = {
            "status":status['status'],
            "price":status['price'],
            "order_type":status['type'],
            "order_quantity":status['origQty'],
            "symbol":order_symbol
            }
            return {"data":data}
        
    if status['status']=='CANCELED':
        data = {
            "status":status['status'],
            "price":status['price'],
            "order_type":status['type'],
            "order_quantity":status['origQty'],
            "symbol":order_symbol
            }
        return {"data":data}
        
    if status['status']=='NEW':
        data = {
            "status":status['status'],
            "price":status['price'],
            "order_type":status['type'],
            "order_quantity":status['origQty'],
            "symbol":order_symbol
            }
        return {"data":data}
# =========================================================================================================================================================================
@app.post('/api/v1/trade/limit/status-ethbtc')
async def get_trade_status(order_id,user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    # get btc address 
    btc_account = await BtcAddress.get(owner=user)
    btc_main_account = btc_account.account_balance
    btc_locked_account = btc_account.lock_account_balance

    # get bnb address
    eth_account = await EthereiumAddress.get(owner=user)
    eth_main_account = eth_account.account_balance 
    eth_locked_account = eth_account.lock_account_balance

    # fetch that transaction history from db and get the lock value that was kept 
    history = await EthBtcTradeHistory.get(order_id=order_id)
    locked_amount = history.lock_amount_for_transaction

    status=order_status(order_id,'ETHBTC')
    # print(status)
    executed_quantity = status['executedQty']
    original_quantity = status['origQty']
    order_symbol = status['symbol']
    order_side=status['side']

    if status['status']=='FILLED':
        if order_side == 'BUY' and order_symbol == 'ETHBTC':
            update_btc_balance = float(btc_main_account + locked_amount) - float(eth_btc(executed_quantity))
            update_eth_balance = float(eth_main_account) + float(executed_quantity)
            lock_balance = float(btc_locked_account) -float(locked_amount)

            bnb_action = await EthereiumAddress.filter(owner=user).update(account_balance=update_eth_balance) 
            btc_action = await BtcAddress.filter(owner=user).update(account_balance=update_btc_balance,lock_account_balance=lock_balance)

            data = {
            "status":status['status'],
            "price":status['price'],
            "order_type":status['type'],
            "order_quantity":status['origQty'],
            "symbol":order_symbol
            }
            return {"data":data}
            

        if order_side == 'SELL' and order_symbol == 'ETHBTC':
            update_btc_balance = float(btc_main_account) +float(eth_btc(executed_quantity))
            update_eth_balance = float(eth_main_account) + float(locked_amount -executed_quantity)
            lock_balance = float(eth_locked_account) - float(locked_amount)
            
            eth_action = await EthereiumAddress.filter(owner=user).update(account_balance=update_eth_balance,lock_account_balance=lock_balance) 
            btc_action = await BtcAddress.filter(owner=user).update(account_balance=update_btc_balance)
            data = {
            "status":status['status'],
            "price":status['price'],
            "order_type":status['type'],
            "order_quantity":status['origQty'],
            "symbol":order_symbol
            }
            return {"data":data}
        
    if status['status']=='CANCELED':
        data = {
            "status":status['status'],
            "price":status['price'],
            "order_type":status['type'],
            "order_quantity":status['origQty'],
            "symbol":order_symbol
            }
        return {"data":data}
        
    if status['status']=='NEW':
        data = {
            "status":status['status'],
            "price":status['price'],
            "order_type":status['type'],
            "order_quantity":status['origQty'],
            "symbol":order_symbol
            }
        return {"data":data}
# =========================================================================================================================================================================
@app.post('/api/v1/trade/limit/status-ltcbtc')
async def get_trade_status(order_id,user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    # get btc address 
    btc_account = await BtcAddress.get(owner=user)
    btc_main_account = btc_account.account_balance
    btc_locked_account = btc_account.lock_account_balance

    # get bnb address
    ltc_account = await LiteCoinAddress.get(owner=user)
    ltc_main_account = ltc_account.account_balance 
    ltc_locked_account = ltc_account.lock_account_balance

    # fetch that transaction history from db and get the lock value that was kept 
    history = await LtcBtcTradeHistory.get(order_id=order_id)
    locked_amount = history.lock_amount_for_transaction

    status=order_status(order_id,'LTCBTC')
    # print(status)
    executed_quantity = status['executedQty']
    original_quantity = status['origQty']
    order_symbol = status['symbol']
    order_side=status['side']

    if status['status']=='FILLED':
        if order_side == 'BUY' and order_symbol == 'LTCBTC':
            update_btc_balance = float(btc_main_account + locked_amount) - float(ltc_btc(executed_quantity))
            update_ltc_balance = float(ltc_main_account) + float(executed_quantity)
            lock_balance = float(btc_locked_account) -float(locked_amount)

            bnb_action = await LiteCoinAddress.filter(owner=user).update(account_balance=update_ltc_balance) 
            btc_action = await BtcAddress.filter(owner=user).update(account_balance=update_btc_balance,lock_account_balance=lock_balance)

            data = {
            "status":status['status'],
            "price":status['price'],
            "order_type":status['type'],
            "order_quantity":status['origQty'],
            "symbol":order_symbol
            }
            return {"data":data}
            

        if order_side == 'SELL' and order_symbol == 'LTCBTC':
            update_btc_balance = float(btc_main_account) +float(ltc_btc(executed_quantity))
            update_ltc_balance = float(ltc_main_account) + float(locked_amount -executed_quantity)
            lock_balance = float(ltc_locked_account) - float(locked_amount)
            
            ltc_action = await LiteCoinAddress.filter(owner=user).update(account_balance=update_ltc_balance,lock_account_balance=lock_balance) 
            btc_action = await BtcAddress.filter(owner=user).update(account_balance=update_btc_balance)
            data = {
            "status":status['status'],
            "price":status['price'],
            "order_type":status['type'],
            "order_quantity":status['origQty'],
            "symbol":order_symbol
            }
            return {"data":data}
        
    if status['status']=='CANCELED':
        data = {
            "status":status['status'],
            "price":status['price'],
            "order_type":status['type'],
            "order_quantity":status['origQty'],
            "symbol":order_symbol
            }
        return {"data":data}
        
    if status['status']=='NEW':
        data = {
            "status":status['status'],
            "price":status['price'],
            "order_type":status['type'],
            "order_quantity":status['origQty'],
            "symbol":order_symbol
            }
        return {"data":data}
# Stop limit Trade ==================================================================================================================================STOP LIMIT TRADE=========
@app.post('/api/v1/trade/stop-limit/buy-test-trade-bnbbtc')
async def buy_test_trade(quantity,limit_price,stop_price,user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    owner = await Account.get(owner=user)
    # get biitcoin_dummy_account 
    btc_account_instance = await BtcAddress.get(owner=user)
    btc_balance = btc_account_instance.account_balance
    lock_balance= btc_account_instance.lock_account_balance
    # place the order
    try:
        _order=place_buy_stop_order('BNBBTC',stop_price,quantity,limit_price)
    except:
        raise HTTPException(status_code=400,detail=f"Check the Price and Stop price then try again")
    order = order_status(_order['orderId'],_order['symbol'])
    # get the current accountof btc and lock it 
    lock_btc_amount = bnb_btc(float(quantity))
    # remove the amount from the main account and place it in the lock account
    remain_btc_balance = float(btc_balance)-float(lock_btc_amount)
    _asking=bnb_info

    lock_balance=float(lock_btc_amount)+float(lock_balance)
    action = await BtcAddress.filter(owner=user).update(account_balance=remain_btc_balance,lock_account_balance=lock_balance)
    # add it to transaction history 
    trade_obj = await BnbBtcTradeHistory.create(
        symbol=order['symbol'],
        side = order['side'],
        quantity=order['origQty'],
        order_id=order['orderId'], 
        trade_status=order['status'],
        asking_price=_asking['price'],
        trade_type='STOP_LIMIT',
        lock_amount_for_transaction = float(lock_btc_amount),
        owner = owner
    )
    await bnb_trade_history_pydantic.from_tortoise_orm(trade_obj)
    return {"status":"success","order_id":order['orderId'],'symbol':order['symbol'],'buy_quantity':order['origQty'],"lock_BTC_balance":lock_balance,"btc_balance":btc_balance,'trade_type':'STOP_LIMIT_BUY'}


@app.post('/api/v1/trade/stop-limit/buy-test-trade-ethbtc')
async def buy_test_trade(quantity,limit_price,stop_price,user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    owner = await Account.get(owner=user)
    # get biitcoin_dummy_account 
    btc_account_instance = await BtcAddress.get(owner=user)
    btc_balance = btc_account_instance.account_balance
    lock_balance= btc_account_instance.lock_account_balance
    # place the order
    try:
        _order=place_buy_stop_order('ETHBTC',stop_price,quantity,limit_price)
    except:
        raise HTTPException(status_code=400, detail=f"Please Check The Price and Quantity Then Try Again")
    order=order_status(_order['orderId'],_order['symbol'])
    # get the current accountof btc and lock it 
    lock_btc_amount = eth_btc(float(quantity))
    # remove the amount from the main account and place it in the lock account
    remain_btc_balance = float(btc_balance)-float(lock_btc_amount)
    _asking=eth_info

    lock_balance=float(lock_btc_amount)+float(lock_balance)
    action = await BtcAddress.filter(owner=user).update(account_balance=remain_btc_balance,lock_account_balance=lock_balance)

    # ASKING PRICE
    

    # add it to transaction history 
    trade_obj = await EthBtcTradeHistory.create(
        symbol=order['symbol'],
        side = order['side'],
        quantity=order['origQty'],
        order_id=order['orderId'], 
        trade_status=order['status'],
        asking_price=_asking['price'],
        trade_type='STOP_LIMIT',
        lock_amount_for_transaction = float(lock_btc_amount),
        owner = owner
    )
    await eth_trade_history_pydantic.from_tortoise_orm(trade_obj)
    return {"status":"success","order_id":order['orderId'],'symbol':order['symbol'],'buy_quantity':order['origQty'],"lock_BTC_balance":lock_balance,"btc_balance":btc_balance,'trade_type':'STOP_LIMIT'}

@app.post('/api/v1/trade/stop-limit/buy-test-trade-ltcbtc')
async def buy_test_trade(quantity,limit_price,stop_price,user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    owner = await Account.get(owner=user)
    # get biitcoin_dummy_account 
    btc_account_instance = await BtcAddress.get(owner=user)
    btc_balance = btc_account_instance.account_balance
    lock_balance= btc_account_instance.lock_account_balance
    # place the order
    try:
        _order=place_buy_stop_order('LTCBTC',stop_price,quantity,limit_price)
    except:
        raise HTTPException(status_code=f"Please Check the Price and Quantity Then Try Again")
    # get the current accountof btc and lock it 
    order= order_status(_order['orderId'],_order['symbol'])
    lock_btc_amount = ltc_btc(float(quantity))
    # remove the amount from the main account and place it in the lock account
    remain_btc_balance = float(btc_balance)-float(lock_btc_amount)
    _asking=ltc_info

    lock_balance=float(lock_btc_amount)+float(lock_balance)
    action = await BtcAddress.filter(owner=user).update(account_balance=remain_btc_balance,lock_account_balance=lock_balance)
    # add it to transaction history 
    trade_obj = await LtcBtcTradeHistory.create(
        symbol=order['symbol'],
        side = order['side'],
        quantity=order['origQty'],
        order_id=order['orderId'], 
        trade_status=order['status'],
        asking_price=_asking['price'],
        trade_type='STOP_LIMIT',
        lock_amount_for_transaction = float(lock_btc_amount),
        owner = owner
    )
    await ltc_trade_history_pydantic.from_tortoise_orm(trade_obj)
    return {"status":"success","order_id":order['orderId'],'symbol':order['symbol'],'buy_quantity':order['origQty'],"lock_BTC_balance":lock_balance,"btc_balance":btc_balance,'trade_type':'STOP_LIMIT'}



# ================================================================================================================================================================ STOP LIMIT SELL TRADE
@app.post('/api/v1/trade/stop-limit/sell-test-trade-bnbbtc')
async def buy_test_trade(quantity,limit_price,stop_price,user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    owner = await Account.get(owner=user)

    # get bnb account
    bnb_account_instance=await BNBAddress.get(owner=user)
    bnb_balance=bnb_account_instance.account_balance
    bnb_lock_balance= bnb_account_instance.lock_account_balance

    # place the order
    try:
        _order= place_sell_stop_order('BNBBTC',stop_price,quantity,limit_price)
    except:
        raise HTTPException(status_code=400,detail=f"Check the Price and Stop price then try again")
    order = order_status(_order['orderId'],_order['symbol'])
    # get the current accountof btc and lock it 
    lock_bnb_value = float(bnb_lock_balance)+float(quantity)
    remaining_bnb_balance = float(bnb_balance) -float(quantity)
    _asking=bnb_info

    # remove the amount from the main account and place it in the lock account
    action = await BNBAddress.filter(owner=user).update(account_balance=remaining_bnb_balance,lock_account_balance=lock_bnb_value)
    # add it to transaction history 
    trade_obj = await BnbBtcTradeHistory.create(
        symbol=order['symbol'],
        side = order['side'],
        quantity=order['origQty'],
        order_id=order['orderId'], 
        trade_status=order['status'],
        asking_price=_asking['price'],
        trade_type='STOP_LIMIT_SELL',
        lock_amount_for_transaction =float(quantity),
        owner = owner
    )
    await bnb_trade_history_pydantic.from_tortoise_orm(trade_obj)
    return {"status":"success","order_id":order['orderId'],'symbol':order['symbol'],'sell_quantity':order['origQty'],"lock_balance":lock_bnb_value,"bnb_balance":bnb_balance,'trade_type':'STOP_LIMIT_SELL'}

@app.post('/api/v1/trade/stop-limit/sell-test-trade-ethbtc')
async def buy_test_trade(quantity,limit_price,stop_price,user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    owner = await Account.get(owner=user)

    # get bnb account
    eth_account_instance=await EthereiumAddress.get(owner=user)
    eth_balance=eth_account_instance.account_balance
    eth_lock_balance= eth_account_instance.lock_account_balance  
    try:
    # place the order
        _order=place_sell_stop_order('ETHBTC',stop_price,quantity,limit_price)
    except:
        raise HTTPException(status_code=400,detail="Please Check The Stop Price and Limit Price then Try Again")
    
    order=order_status(_order['orderId'],_order['symbol'])
    # get the current accountof btc and lock it 
    lock_eth_value = float(eth_lock_balance)+float(quantity)
    remaining_eth_balance = float(eth_balance) -float(quantity)

    # remove the amount from the main account and place it in the lock account
    action = await EthereiumAddress.filter(owner=user).update(account_balance=remaining_eth_balance,lock_account_balance=lock_eth_value)
    _asking=eth_info
    
    # add it to transaction history 
    trade_obj = await EthBtcTradeHistory.create(
        symbol=order['symbol'],
        side = order['side'],
        quantity=order['origQty'],
        order_id=order['orderId'], 
        trade_status=order['status'],
        asking_price=_asking['price'],
        trade_type="STOP_LIMIT",
        lock_amount_for_transaction =float(quantity),
        owner = owner
    )
    await eth_trade_history_pydantic.from_tortoise_orm(trade_obj)
    return {"status":"success","order_id":order['orderId'],'symbol':order['symbol'],'sell_quantity':order['origQty'],"lock_balance":lock_eth_value,"eth_balance":eth_balance,'trade_type':'STOP_LIMIT'}


@app.post('/api/v1/trade/stop-limit/sell-test-trade-ltcbtc')
async def buy_test_trade(quantity,limit_price,stop_price,user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    owner = await Account.get(owner=user)

    # get bnb account
    ltc_account_instance=await LiteCoinAddress.get(owner=user)
    ltc_balance=ltc_account_instance.account_balance
    ltc_lock_balance= ltc_account_instance.lock_account_balance  

    # place the order
    try:
        _order=place_sell_stop_order('LTCBTC',stop_price,quantity,limit_price)
    except: 
        raise HTTPException(status_code=400,detail=f"Please Check the Limit Price and Try Again")
    order = order_status(_order['orderId'],_order['symbol'])
    _asking=ltc_info

    # get the current accountof btc and lock it 
    lock_ltc_value = float(ltc_lock_balance)+float(quantity)
    remaining_ltc_balance = float(ltc_balance) - float(quantity)

    # remove the amount from the main account and place it in the lock account
    action = await LiteCoinAddress.filter(owner=user).update(account_balance=remaining_ltc_balance,lock_account_balance=lock_ltc_value)
    # add it to transaction history 
    trade_obj = await LtcBtcTradeHistory.create(
        symbol=order['symbol'],
        side = order['side'],
        quantity=order['origQty'],
        trade_status=order['status'],
        order_id=order['orderId'], 
        asking_price=_asking['price'],
        trade_type='STOP_LIMIT',
        lock_amount_for_transaction =float(quantity),
        owner = owner
    )
    await ltc_trade_history_pydantic.from_tortoise_orm(trade_obj)
    return {"status":"success","order_id":order['orderId'],'symbol':order['symbol'],'sell_quantity':order['origQty'],"lock_balance":lock_ltc_value,"ltc_balance":ltc_balance,'trade_type':'STOP_LIMIT'}



# ==========================================================================================================================================================================  
@app.post('/api/v1/cancel-trade-bnbbtc')
async def cancel_a_trade(order_id,user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    # get the bnb account of the user 
    bnb_account_instance = await BNBAddress.get(owner=user)
    bnb_account_balance = bnb_account_instance.account_balance
    bnb_locked_balance = bnb_account_instance.lock_account_balance

    # get btc account of the user 
    btc_account_instance = await BtcAddress.get(owner=user)
    btc_account_balance = btc_account_instance.account_balance
    btc_locked_balance = btc_account_instance.lock_account_balance 

    # fileter the lock value from the database of the trade history 
    history = await BnbBtcTradeHistory.get(order_id=order_id)
    locked_value = history.lock_amount_for_transaction

    # get the order status
    status=order_status(order_id,'BNBBTC')
    if status['side'] == 'BUY':
        new_btc_balance = float(btc_account_balance) + float(locked_value)
        new_btc_locked_balance = float(btc_locked_balance) - float(locked_value)
        action = await BtcAddress.filter(owner=user).update(account_balance=new_btc_balance,lock_account_balance=new_btc_locked_balance)
    
    if status['side'] == 'SELL':
        new_bnb_balance = float(bnb_account_balance) + float(locked_value)
        new_bnb_locked_balance = float(bnb_locked_balance) - float(locked_value)
        action = await BNBAddress.filter(owner=user).update(account_balance=new_bnb_balance,lock_account_balance=new_bnb_locked_balance)
    
    # update the transaction on the user account
    data = {
            "status":status['status'],
            "price":status['price'],
            "order_type":status['type'],
            "order_quantity":status['origQty'],
            "symbol":status['symbol']
        }

    if status['status'] == 'FILLED' or status['status'] == 'CANCELED':
        return {"message":"This Order cannot be cancelled","data":data}

    return {"message":"Order Canceled","data":data}

# ===================================================================================================================================================================================   
@app.post('/api/v1/cancel-trade-ethbtc')
async def cancel_a_trade(order_id,user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    # get the bnb account of the user 
    eth_account_instance = await EthereiumAddress.get(owner=user)
    eth_account_balance = eth_account_instance.account_balance
    eth_locked_balance = eth_account_instance.lock_account_balance

    # get btc account of the user 
    btc_account_instance = await BtcAddress.get(owner=user)
    btc_account_balance = btc_account_instance.account_balance
    btc_locked_balance = btc_account_instance.lock_account_balance 

    # fileter the lock value from the database of the trade history 
    history = await EthBtcTradeHistory.get(order_id=order_id)
    locked_value = history.lock_amount_for_transaction

    # get the order status
    status=order_status(order_id,'ETHBTC')
    if status['side'] == 'BUY':
        new_btc_balance = float(btc_account_balance) + float(locked_value)
        new_btc_locked_balance = float(btc_locked_balance) - float(locked_value)
        action = await BtcAddress.filter(owner=user).update(account_balance=new_btc_balance,lock_account_balance=new_btc_locked_balance)
    
    if status['side'] == 'SELL':
        new_eth_balance = float(eth_account_balance) + float(locked_value)
        new_eth_locked_balance = float(eth_locked_balance) - float(locked_value)
        action = await BNBAddress.filter(owner=user).update(account_balance=new_eth_balance,lock_account_balance=new_eth_locked_balance)
    
    # update the transaction on the user account
    data = {
            "status":status['status'],
            "price":status['price'],
            "order_type":status['type'],
            "order_quantity":status['origQty'],
            "symbol":status['symbol']
        }

    if status['status'] == 'FILLED' or status['status'] == 'CANCELED':
        return {"message":"This Order cannot be cancelled","data":data}

    return {"message":"Order Canceled","data":data}

# ========================================================================================================================================================================
@app.post('/api/v1/cancel-trade-ltcbtc')
async def cancel_a_trade(order_id,user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    # get the bnb account of the user 
    ltc_account_instance = await LiteCoinAddress.get(owner=user)
    ltc_account_balance = ltc_account_instance.account_balance
    ltc_locked_balance = ltc_account_instance.lock_account_balance

    # get btc account of the user 
    btc_account_instance = await BtcAddress.get(owner=user)
    btc_account_balance = btc_account_instance.account_balance
    btc_locked_balance = btc_account_instance.lock_account_balance 

    # fileter the lock value from the database of the trade history 
    history = await LtcBtcTradeHistory.get(order_id=order_id)
    locked_value = history.lock_amount_for_transaction

    # get the order status
    status=order_status(order_id,'LTCBTC')
    if status['side'] == 'BUY':
        new_btc_balance = float(btc_account_balance) + float(locked_value)
        new_btc_locked_balance = float(btc_locked_balance) - float(locked_value)
        action = await BtcAddress.filter(owner=user).update(account_balance=new_btc_balance,lock_account_balance=new_btc_locked_balance)
    
    if status['side'] == 'SELL':
        new_ltc_balance = float(ltc_account_balance) + float(locked_value)
        new_ltc_locked_balance = float(ltc_locked_balance) - float(locked_value)
        action = await BNBAddress.filter(owner=user).update(account_balance=new_ltc_balance,lock_account_balance=new_ltc_locked_balance)
    
    # update the transaction on the user account
    data = {
            "status":status['status'],
            "price":status['price'],
            "order_type":status['type'],
            "order_quantity":status['origQty'],
            "symbol":status['symbol']
        }

    if status['status'] == 'FILLED' or status['status'] == 'CANCELED':
        return {"message":"This Order cannot be cancelled","data":data}

    return {"message":"Order Canceled","data":data}


# Trade History Endpoints==================================================================================================================================
@app.get('/api/v1/get-bnbbtc-trade-history')
async def get_trade_history(user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    history = await BnbBtcTradeHistory.filter(owner=user)
    if len(history) <= 0:
        raise HTTPException(status_code=200,detail="No Trade Perform yet")
    return history

@app.get('/api/v1/get-ethbtc-trade-history')
async def get_trade_history(user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    history = await EthBtcTradeHistory.filter(owner=user)
    if len(history) <= 0:
        raise HTTPException(status_code=200,detail="No Trade Perform yet")
    return history

@app.get('/api/v1/get-ltcbtc-trade-history')
async def get_trade_history(user:user_pydanticIn = Depends(get_current_user),token:str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401,detail=f"You are currently logged out")
    history = await LtcBtcTradeHistory.filter(owner=user)
    if len(history) <= 0:
        raise HTTPException(status_code=200,detail="No Trade Perform yet")
    return history



register_tortoise(
    app,
    # db_url="postgres://postgres:password@localhost:5432/btc_nation",
    db_url = "sqlite://app/memory.sqlite",
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

