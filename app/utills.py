from typing import List
import sendgrid
import os 
from sendgrid.helpers.mail import  *
from dotenv import dotenv_values
config_credentials = dotenv_values(".env")
from app.models import User
import jwt
import string
import random
from bitcoinlib.wallets import Wallet
from web3 import Web3,HTTPProvider
URL = "https://mainnet.infura.io/v3/c965d518142747cd85d0fe46f8351cf9"
ETHERSCAN_API_KEY="3U9KDED62TUDHR48ZR5I2YBK2B98FHBITW"
# URL_GNACHE = "HTTP://127.0.0.1:7545"
BNB_ENDPOINT = "https://bsc-dataseed.binance.org/"
from random import randint

w3 = Web3(HTTPProvider(URL))

bnb = Web3(HTTPProvider(BNB_ENDPOINT))
from requests import get


# reset password token 
def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)




# ---------------------------------------------------------- WEB 3 Functionalities---------------------------------------------------
# Check if the eth node is connected
connected = w3.isConnected()
print(connected)


# Create a bitcoin address 
def create_bitcoin_wallet_for_user(unique_identifier:str):
    wallet_instance = Wallet.create(unique_identifier,network='bitcoin')
    wallet_data = wallet_instance.as_dict()
    # get some information from the wallet 
    identifier = wallet_data['name'] 
    account_network = wallet_data['main_network']
    main_balance =wallet_data['main_balance']
    wallet_id =wallet_data ['wallet_id']
    # Second way to get address 
    wallet = wallet_instance.get_key()
    address = wallet.address
    data = {"address":address,"identifier":identifier,"account_network":account_network,"wallet_balance":main_balance,"wallet_id":wallet_id}
    return data

# Create a litecoin address 
def create_litecoin_wallet_for_user(unique_identifier:str):
    wallet_instance= Wallet.create(unique_identifier,network='litecoin')
    # Get a huge dictionary data about the account created
    wallet_data = wallet_instance.as_dict()
    # get some information from the wallet 
    identifier = wallet_data['name'] 
    account_network = wallet_data['main_network']
    main_balance =wallet_data['main_balance']
    wallet_id =wallet_data ['wallet_id']
    # Second way to get address 
    wallet = wallet_instance.get_key()
    address = wallet.address
    data = {"address":address,"identifier":identifier,"account_network":account_network,"wallet_balance":main_balance,"wallet_id":wallet_id}
    return data


def create_dash_wallet_for_user(unique_identifier:str):
    wallet_instance= Wallet.create(unique_identifier,network='dash')
    # get a huge dictionary about the account just created
    wallet_data = wallet_instance.as_dict()
    # get some information from the wallet 
    identifier = wallet_data['name'] 
    account_network = wallet_data['main_network']
    main_balance =wallet_data['main_balance']
    wallet_id =wallet_data ['wallet_id']
    # Second way to get address 
    wallet = wallet_instance.get_key()
    address = wallet.address
    data = {"address":address,"identifier":identifier,"account_network":account_network,"wallet_balance":main_balance,"wallet_id":wallet_id}
    return data



# create eth address
def create_eth_account():
    new_account = w3.eth.account.create()
    # all_accounts = w3.eth.accounts
    account_key = new_account.privateKey.hex()
    account_address = new_account.address
    # private_key = w3.eth.get_code(account_address)
    data = {"account":account_address,"key":account_key}
    return data

# get the user balance in eth
def get_account_balance(account:str):
    balance = w3.eth.get_balance(account)
    eth_balance= w3.fromWei(balance,'ether')
    return float(eth_balance)

# send eth from user account to another account
def send_eth_transfer(sender:str,receiver:str,value):
    
    tx_hash = w3.eth.send_transaction({
    'to': receiver,
    'from': sender,
    'value': w3.toWei(value,'ether')
    })
  
    return w3.toHex(tx_hash)

def get_transaction_receipt(hash:str):
    receipt = w3.eth.get_transaction(hash)
    receipt_dict = dict(receipt)
    receiving_address = receipt_dict['to']
    value = w3.fromWei(receipt_dict['value'],'ether')
    print(receiving_address,value)
    data = {
        "value":float(value),
        "receiving_address":receiving_address
    }
    return data


def get_transactions(address):
    get_transaction_url = f"""https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&page=1&offset=10&sort=asc&apikey={ETHERSCAN_API_KEY}"""
    response = get(get_transaction_url)
    data = response.json()
    transactions = data["result"]
    return transactions



def create_bnb_account():
    new_account = bnb.eth.account.create()
    # all_accounts = w3.eth.accounts
    account_key = new_account.privateKey.hex()
    account_address = new_account.address
    # private_key = w3.eth.get_code(account_address)
    return {"account":account_address,"key":account_key}

# print(create_eth_account())

# get the user balance
def get_bnb_balance(account:str):
    balance = bnb.eth.get_balance(account)
    eth_balance= bnb.fromWei(balance,'ether')
    return eth_balance

# send eth
def send_bnb(sender:str,receiver:str,value:int):
    tx_hash = bnb.eth.send_transaction({
    'to': receiver,
    'from': sender,
    'value': bnb.toWei(value,'ether')
    })
  
    return bnb.toHex(tx_hash)


def get_bnb_transaction_receipt(hash:str):
    receipt = bnb.eth.get_transaction(hash)
    receipt_dict = dict(receipt)
    receiving_address = receipt_dict['to']
    value = bnb.fromWei(receipt_dict['value'],'ether')
    print(receiving_address,value)
    data = {
        "value":float(value),
        "receiving_address":receiving_address
    }
    return data


# ----------------------------------------------------------------- SEND GRID FUNCTIOALITIES -------------------------------------------------------------------------------

# function that send mails
async def send_mail(email:List,instance:User):
    token_data ={
        "id":instance.id,
        "email":instance.email
    }
    token = jwt.encode(token_data,config_credentials["SECRET"])
    template = f"""
        <!DOCTYPE html>
        <html>

        <head>
            <title></title>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        </head>

        <body style="background-color: #f4f4f4; margin: 0 !important; padding: 0 !important;">
            <!-- HIDDEN PREHEADER TEXT -->
            <div style="display: none; font-size: 1px; color: #fefefe; line-height: 1px; font-family: 'Lato', Helvetica, Arial, sans-serif; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden;"> We're thrilled to have you here! Get ready to dive into your new account.
            </div>
            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                <!-- LOGO -->
                <tr>
                    <td bgcolor="#3bff69" align="center">
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">
                            <tr>
                                <td align="center" valign="top" style="padding: 40px 10px 40px 10px;"> </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td bgcolor="#3bff69" align="center" style="padding: 0px 10px 0px 10px;">
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">
                            <tr>
                                <td bgcolor="#ffffff" align="center" valign="top" style="padding: 40px 20px 20px 20px; border-radius: 4px 4px 0px 0px; color: #111111; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 48px; font-weight: 400; letter-spacing: 4px; line-height: 48px;">
                                    <h1 style="font-size: 48px; font-weight: 400; margin: 2;">Welcome!</h1> <img src=" https://img.icons8.com/clouds/100/000000/handshake.png" width="125" height="120" style="display: block; border: 0px;" />
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td bgcolor="#f4f4f4" align="center" style="padding: 0px 10px 0px 10px;">
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">
                            <tr>
                                <td bgcolor="#ffffff" align="left" style="padding: 20px 30px 40px 30px; color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;">
                                    <p style="margin: 0;">We're excited to have you get started. First, you need to confirm your account. Just press the button below.</p>
                                </td>
                            </tr>
                            <tr>
                                <td bgcolor="#ffffff" align="left">
                                    <table width="100%" border="0" cellspacing="0" cellpadding="0">
                                        <tr>
                                            <td bgcolor="#ffffff" align="center" style="padding: 20px 30px 60px 30px;">
                                                <table border="0" cellspacing="0" cellpadding="0">
                                                    <tr>
                                                        <td align="center" style="border-radius: 3px;" bgcolor="#3bff69"><a href=https://cryptoexchangeapi.herokuapp.com/api/v1/verification/?token={token}" target="_blank" style="font-size: 20px; font-family: Helvetica, Arial, sans-serif; color: #ffffff; text-decoration: none; color: #ffffff; text-decoration: none; padding: 15px 25px; border-radius: 2px; border: 1px solid #3bff69; display: inline-block;">Confirm Account</a></td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr> <!-- COPY -->
                            <tr>
                                <td bgcolor="#ffffff" align="left" style="padding: 0px 30px 0px 30px; color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;">
                                    <p style="margin: 0;">If that doesn't work, copy and paste the following link in your browser:</p>
                                </td>
                            </tr> <!-- COPY -->
                            <tr>
                                <td bgcolor="#ffffff" align="left" style="padding: 20px 30px 20px 30px; color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;">
                                    <p style="margin: 0;"><a href="https://cryptoexchangeapi.herokuapp.com/api/v1/verification/?token={token}" target="_blank" style="color: #3bff69;">https://cryptoexchangeapi.herokuapp.com/api/v1/verification/?token={token}"></a></p>
                                </td>
                            </tr>
                            <tr>
                                <td bgcolor="#ffffff" align="left" style="padding: 0px 30px 20px 30px; color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;">
                                    <p style="margin: 0;">If you have any questions, just reply to this email&mdash;we're always happy to help out.</p>
                                </td>
                            </tr>
                            <tr>
                                <td bgcolor="#ffffff" align="left" style="padding: 0px 30px 40px 30px; border-radius: 0px 0px 4px 4px; color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;">
                                    <p style="margin: 0;">Cheers,<br>Exchange App/p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <!-- <tr>
                    <td bgcolor="#f4f4f4" align="center" style="padding: 30px 10px 0px 10px;">
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">
                            <tr>
                                <td bgcolor="#FFECD1" align="center" style="padding: 30px 30px 30px 30px; border-radius: 4px 4px 4px 4px; color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;">
                                    <h2 style="font-size: 20px; font-weight: 400; color: #111111; margin: 0;">Need more help?</h2>
                                    <p style="margin: 0;"><a href="#" target="_blank" style="color: #FFA73B;">We&rsquo;re here to help you out</a></p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr> -->
                <tr>
                    <td bgcolor="#f4f4f4" align="center" style="padding: 0px 10px 0px 10px;">
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">
                            <tr>
                                <td bgcolor="#f4f4f4" align="left" style="padding: 0px 30px 30px 30px; color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 14px; font-weight: 400; line-height: 18px;"> <br>
                                    <p style="text-align: center;">&copy;david isaac</p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>

        </html>
    """
    from email.mime.text import MIMEText
    import smtplib


    fromaddr = "davidisaac081@gmail.com"
    toaddr = email[0]


    # html = template
    msg = MIMEText(template, 'html')
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Exchange App"

    debug = False
    if debug:
        print(msg.as_string())
    else:
        server = smtplib.SMTP_SSL('smtp.gmail.com',465)
        server.login("davidisaac081@gmail.com", "zsutyjkknvncqatc")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()


def send_reset_password(email:List,reset_code:str):
    template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title></title>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        </head>

        <body style="background-color: #f4f4f4; margin: 0 !important; padding: 0 !important;">
            <!-- HIDDEN PREHEADER TEXT -->
            <div style="display: none; font-size: 1px; color: #fefefe; line-height: 1px; font-family: 'Lato', Helvetica, Arial, sans-serif; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden;"> We're thrilled to have you here! Get ready to dive into your new account.
            </div>
            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                <!-- LOGO -->
                <tr>
                    <td bgcolor="#3bff69" align="center">
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">
                            <tr>
                                <td align="center" valign="top" style="padding: 40px 10px 40px 10px;"> </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td bgcolor="#3bff69" align="center" style="padding: 0px 10px 0px 10px;">
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">
                            <tr>
                                <td bgcolor="#ffffff" align="center" valign="top" style="padding: 40px 20px 20px 20px; border-radius: 4px 4px 0px 0px; color: #111111; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 48px; font-weight: 400; letter-spacing: 4px; line-height: 48px;">
                                    <h1 style="font-size: 20px; font-weight: 100; margin: 2;">PASSWORD RESET EXCHANGE APP/h1> <img src=" https://europetalks.lango.io/theme/image.php/lango/theme/1585128165/images/forgot-pwd-icon" width="125" height="120" style="display: block; border: 0px;" />
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td bgcolor="#f4f4f4" align="center" style="padding: 0px 10px 0px 10px;">
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">
                            <tr>
                                <td bgcolor="#ffffff" align="left" style="padding: 20px 30px 40px 30px; color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;">
                                    <p style="margin: 0;">It Seems you are having Trouble Logging in? Below is your Password Reset Code, This Code Will Expire in 30 Minutes</p>
                                </td>
                            </tr>
                            <tr>
                                <td bgcolor="#ffffff" align="left">
                                    <table width="100%" border="0" cellspacing="0" cellpadding="0">
                                        <tr>
                                            <td bgcolor="#ffffff" align="center" style="padding: 20px 30px 60px 30px;">
                                                <table border="0" cellspacing="0" cellpadding="0">
                                                    <tr>
                                                        <td align="center" style="border-radius: 3px;" bgcolor="#3bff69"><p style="font-size: 20px; font-family: Helvetica, Arial, sans-serif; color: #ffffff; text-decoration: none; color: #ffffff; text-decoration: none; padding: 15px 25px; border-radius: 2px; border: 1px solid #3bff69; display: inline-block;">{reset_code}</p></td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr> <!-- COPY -->
                            <tr>
                                <td bgcolor="#ffffff" align="left" style="padding: 0px 30px 20px 30px; color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;">
                                    <p style="margin: 0;">If you have any questions, just reply to this email&mdash;we're always happy to help out.</p>
                                </td>
                            </tr>
                            <tr>
                                <td bgcolor="#ffffff" align="left" style="padding: 0px 30px 40px 30px; border-radius: 0px 0px 4px 4px; color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;">
                                    <p style="margin: 0;">Cheers,<br>BTC Nation Team</p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <!-- <tr>
                    <td bgcolor="#f4f4f4" align="center" style="padding: 30px 10px 0px 10px;">
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">
                            <tr>
                                <td bgcolor="#FFECD1" align="center" style="padding: 30px 30px 30px 30px; border-radius: 4px 4px 4px 4px; color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;">
                                    <h2 style="font-size: 20px; font-weight: 400; color: #111111; margin: 0;">Need more help?</h2>
                                    <p style="margin: 0;"><a href="#" target="_blank" style="color: #FFA73B;">We&rsquo;re here to help you out</a></p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr> -->
                <tr>
                    <td bgcolor="#f4f4f4" align="center" style="padding: 0px 10px 0px 10px;">
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">
                            <tr>
                                <td bgcolor="#f4f4f4" align="left" style="padding: 0px 30px 30px 30px; color: #666666; font-family: 'Lato', Helvetica, Arial, sans-serif; font-size: 14px; font-weight: 400; line-height: 18px;"> <br>
                                    <p style="text-align: center;">&copy; EXCHANGE APP 2022</p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>

    
    """
    from email.mime.text import MIMEText
    import smtplib


    fromaddr = "davidisaac081@gmail.com"
    toaddr = email[0]


    html = template
    msg = MIMEText(template, 'html')
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Exchange App"

    debug = False
    if debug:
        print(msg.as_string())
    else:
        server = smtplib.SMTP_SSL('smtp.gmail.com',465)
        server.login("davidisaac081@gmail.com", "zsutyjkknvncqatc")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()


# Create a bitcoin address 
def create_bitcoin_wallet_for_user(unique_identifier:str):
    wallet_instance = Wallet.create(unique_identifier,network='bitcoin')
    wallet_data = wallet_instance.as_dict()
    # get some information from the wallet 
    identifier = wallet_data['name'] 
    account_network = wallet_data['main_network']
    main_balance =wallet_data['main_balance']
    wallet_id =wallet_data ['wallet_id']
    # Second way to get address 
    wallet = wallet_instance.get_key()
    address = wallet.address
    data = {"address":address,"identifier":identifier,"account_network":account_network,"wallet_balance":main_balance,"wallet_id":wallet_id}
    return data

# Create a litecoin address 
def create_litecoin_wallet_for_user(unique_identifier:str):
    wallet_instance= Wallet.create(unique_identifier,network='litecoin')
    # Get a huge dictionary data about the account created
    wallet_data = wallet_instance.as_dict()
    # get some information from the wallet 
    identifier = wallet_data['name'] 
    account_network = wallet_data['main_network']
    main_balance =wallet_data['main_balance']
    wallet_id =wallet_data ['wallet_id']
    # Second way to get address 
    wallet = wallet_instance.get_key()
    address = wallet.address
    data = {"address":address,"identifier":identifier,"account_network":account_network,"wallet_balance":main_balance,"wallet_id":wallet_id}
    return data


def create_dash_wallet_for_user(unique_identifier:str):
    wallet_instance= Wallet.create(unique_identifier,network='dash')
    # get a huge dictionary about the account just created
    wallet_data = wallet_instance.as_dict()
    # get some information from the wallet 
    identifier = wallet_data['name'] 
    account_network = wallet_data['main_network']
    main_balance =wallet_data['main_balance']
    wallet_id =wallet_data ['wallet_id']
    # Second way to get address 
    wallet = wallet_instance.get_key()
    address = wallet.address
    data = {"address":address,"identifier":identifier,"account_network":account_network,"wallet_balance":main_balance,"wallet_id":wallet_id}
    return data


def get_random_string():
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(26))
    return result_str


# Trading functionalities 
# TEST_NET
from binance.enums import * 
from binance.client import Client
# secret key
BINANCE_API_KEY = 'N73Y7LwZLzUmRn8d2Qznt024zqrJp4BCjAEefQgZmsBj72I3hcA7Nh7DabAlkcK1'
BINANCE_API_SECRET = '7stpscCgIHFphe3ULgVRlN07zOzO9uNMlCbVz8yTqTs3S8XvwixkhGb3KSIgfpnn'

client = Client(BINANCE_API_KEY, BINANCE_API_SECRET,testnet=True)

# MARKET ORDER
def buy_order(quantity,symbol):
    order = client.create_order(
        symbol=symbol,
        side=SIDE_BUY,
        type=ORDER_TYPE_MARKET,
        quantity=quantity,
        )
    return order

def sell_order(quantity,symbol):
    order = client.create_order(
        symbol=symbol,
        side=SIDE_SELL,
        type=ORDER_TYPE_MARKET,
        quantity=quantity,
        )
    return order


def buy_limit_order(symbol,quantity,price):
    order = client.order_limit_buy(
    symbol=symbol,
    quantity=quantity,
    price=price)
    return order



def place_buy_stop_order(symbol,stopPrice,quantity,price):
    order = client.create_order(
    symbol=symbol,
    side=SIDE_BUY,
    type=ORDER_TYPE_TAKE_PROFIT_LIMIT,
    timeInForce=TIME_IN_FORCE_GTC,
    stopPrice=stopPrice,
    quantity=quantity,
    price=price)
    return order

def place_sell_stop_order(symbol,stopPrice,quantity,price):
    order = client.create_order(
    symbol=symbol,
    side=SIDE_SELL,
    type=ORDER_TYPE_TAKE_PROFIT_LIMIT,
    timeInForce=TIME_IN_FORCE_GTC,
    stopPrice=stopPrice,
    quantity=quantity,
    price=price)
    return order



def sell_limit_order(symbol,quantity,price):
    order = client.order_limit_sell(
    symbol=symbol,
    quantity=quantity,
    price=price)
    return order


def order_status(orderid,symbol):
    status=client.get_order(
    symbol=symbol.upper(),
    orderId=orderid)
    return status

def cancel_order(orderid,symbol):
    result = client.cancel_order(
        symbol=symbol.upper(),
        orderId=orderid)
    return result








# MAIN NET
API_KEY = "SHgH7j0CDHjvvA6SgmnaW0gPD6fWzl4IdcVCx6CdHQsNfac98TMUpylis3RKfKZl"
API_SECRET ="svMNhjBQywLS4UGfAUWu5CiZWNHyLF7qfQW1aOyDxYp1mRm4uzCQnP6FRXMoqolQ"
main_client = Client(API_KEY,API_SECRET)

eth_info = main_client.get_margin_price_index(symbol='ETHBTC')
bnb_info = main_client.get_margin_price_index(symbol='BNBBTC')
ltc_info = main_client.get_margin_price_index(symbol='LTCBTC')
dash_info = main_client.get_margin_price_index(symbol='DASHBTC')

# converter utilites
_eth_usd = main_client.get_margin_price_index(symbol='ETHUSDT')
_btc_usd = main_client.get_margin_price_index(symbol='BTCUSDT')
_bnb_usd = main_client.get_margin_price_index(symbol='BNBUSDT')
_ltc_usd = main_client.get_margin_price_index(symbol='LTCUSDT')
_dash_usd = main_client.get_margin_price_index(symbol='DASHUSDT')

