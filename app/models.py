from email.policy import default
from operator import index
from re import L
from unicodedata import decimal
import pydantic
from sqlalchemy import null
from tortoise import fields
from tortoise.models import Model
from pydantic import BaseModel
from datetime import datetime
from tortoise.contrib.pydantic import pydantic_model_creator

class User(Model):
    id = fields.IntField(pk=True, index=True)
    lastname = fields.CharField(max_length=25, null=False)
    firstname = fields.CharField(max_length=25, null=False)
    email = fields.CharField(max_length=250,null=False, unique=True)
    password = fields.CharField(max_length=250, null=False)
    is_verified = fields.BooleanField(default=False)
    date_joined = fields.DatetimeField(default=datetime.utcnow())

class Account(Model):
    id = fields.IntField(pk=True, index=True)
    profile_image = fields.CharField(null=True,max_length=355)
    profile_image_url = fields.CharField(null=True,max_length=5000,default="null.jpg")
    available_balance = fields.FloatField()
    phone_number = fields.IntField(null=True)
    is_verified = fields.BooleanField(default=False)
    owner = fields.ForeignKeyField("models.User",related_name="user_account")

class Py_codes(Model):
    id = fields.IntField(pk=True, index=True)
    email = fields.CharField(max_length=250,null=False)
    reset_code = fields.CharField(max_length=200,null=False)
    status = fields.BooleanField(default=False)

class BtcAddress(Model):
    wallet_id = fields.IntField(pk=True)
    wallet_address = fields.CharField(null=True,max_length=5000)
    wallet_identifier = fields.CharField(max_length=2000,null=False)
    account_network = fields.CharField(max_length=200,null=False)
    account_balance = fields.DecimalField(max_digits=200,decimal_places=15)
    lock_account_balance = fields.DecimalField(max_digits=200,decimal_places=15)
    owner = fields.ForeignKeyField("models.Account",related_name="btc_address")

class LiteCoinAddress(Model):
    wallet_id = fields.IntField(pk=True)
    wallet_address = fields.CharField(null=True,max_length=5000)
    wallet_identifier = fields.CharField(max_length=2000,null=False)
    account_network = fields.CharField(max_length=200,null=False)
    account_balance = fields.DecimalField(max_digits=200,decimal_places=15)
    lock_account_balance = fields.DecimalField(max_digits=200,decimal_places=15)
    owner = fields.ForeignKeyField("models.Account",related_name="litecoin_address")


class DashCoinAddress(Model):
    wallet_id = fields.IntField(pk=True)
    wallet_address = fields.CharField(null=True,max_length=5000)
    wallet_identifier = fields.CharField(max_length=2000,null=False)
    account_network = fields.CharField(max_length=200,null=False)
    account_balance = fields.DecimalField(max_digits=200,decimal_places=15)
    lock_account_balance = fields.DecimalField(max_digits=200,decimal_places=15)
    owner = fields.ForeignKeyField("models.Account",related_name="dashcoin_address")

class EthereiumAddress(Model):
    wallet_id = fields.IntField(pk=True,index=True)
    wallet_address = fields.CharField(max_length=5000,null=False)
    wallet_key = fields.CharField(max_length=5000,null=False)
    # remove this after testing ------------------------------------------------------------------------
    account_balance = fields.DecimalField(max_digits=200,decimal_places=15)
    lock_account_balance = fields.DecimalField(max_digits=200,decimal_places=15)
    owner = fields.ForeignKeyField("models.Account",related_name="eth_address")

class BNBAddress(Model):
    wallet_id = fields.IntField(pk=True,index=True)
    wallet_address = fields.CharField(max_length=5000,null=False)
    wallet_key = fields.CharField(max_length=5000,null=False)
    # remove this after demo----------------------------------------------------------------------
    account_balance = fields.DecimalField(max_digits=200,decimal_places=15)
    lock_account_balance = fields.DecimalField(max_digits=200,decimal_places=15)
    owner = fields.ForeignKeyField("models.Account",related_name="bnb_address")

class EtheriumTransactionHistory(Model):
    trasaction_id = fields.IntField(pk=True,index=True)
    value = fields.DecimalField(max_digits=1000,decimal_places=6)
    receiving_address = fields.CharField(max_length=5000,null=True,blank=True)
    owner = fields.ForeignKeyField("models.Account",related_name="eth_transactions")

class BTCTransactionHistory(Model):
    trasaction_id = fields.IntField(pk=True,index=True)
    value = fields.DecimalField(max_digits=1000,decimal_places=6)
    receiving_address = fields.CharField(max_length=5000,null=True,blank=True)
    owner = fields.ForeignKeyField("models.Account",related_name="btc_transactions")

class LiteCoinTransactionHistory(Model):
    trasaction_id = fields.IntField(pk=True,index=True)
    value = fields.DecimalField(max_digits=1000,decimal_places=6)
    receiving_address = fields.CharField(max_length=5000,null=True,blank=True)
    owner = fields.ForeignKeyField("models.Account",related_name="litecoin_transactions")

class DashCoinTransactionHistory(Model):
    trasaction_id = fields.IntField(pk=True,index=True)
    value = fields.DecimalField(max_digits=1000,decimal_places=6)
    receiving_address = fields.CharField(max_length=5000,null=True,blank=True)
    owner = fields.ForeignKeyField("models.Account",related_name="dashcoin_transactions")

class BnbBtcTradeHistory(Model):
    order_id=fields.IntField(pk=True)
    quantity=fields.DecimalField(max_digits=10,decimal_places=8)
    side=fields.CharField(max_length=20,null=True,blank=True)
    symbol=fields.CharField(max_length=20,null=True,blank=True)
    trade_type=fields.CharField(max_length=20,null=True,blank=True)
    trade_status=fields.CharField(max_length=20,null=True,blank=True)
    lock_amount_for_transaction = fields.DecimalField(max_digits=10,decimal_places=8,default=0.000)
    asking_price = fields.CharField(max_length=10,null=True,blank=True,default='0.0000')
    owner = fields.ForeignKeyField("models.Account",related_name="bnb_trade_history")
    date_added = fields.DatetimeField(default=datetime.utcnow(),auto_now_add=True)

    
class EthBtcTradeHistory(Model):
    order_id=fields.IntField(pk=True)
    quantity=fields.DecimalField(max_digits=10,decimal_places=8)
    side=fields.CharField(max_length=20,null=True,blank=True)
    symbol=fields.CharField(max_length=20,null=True,blank=True)
    trade_type=fields.CharField(max_length=20,null=True,blank=True)
    trade_status=fields.CharField(max_length=20,null=True,blank=True)
    lock_amount_for_transaction = fields.DecimalField(max_digits=10,decimal_places=8,default=0.000)
    asking_price = fields.CharField(max_length=10,null=True,blank=True,default='0.0000')
    owner = fields.ForeignKeyField("models.Account",related_name="etn_trade_history")
    date_added = fields.DatetimeField(default=datetime.utcnow(),auto_now_add=True)

    
class LtcBtcTradeHistory(Model):
    order_id=fields.IntField(pk=True)
    quantity=fields.DecimalField(max_digits=10,decimal_places=8)
    side=fields.CharField(max_length=20,null=True,blank=True)
    symbol=fields.CharField(max_length=20,null=True,blank=True)
    trade_type=fields.CharField(max_length=20,null=True,blank=True)
    trade_status=fields.CharField(max_length=20,null=True,blank=True)
    lock_amount_for_transaction = fields.DecimalField(max_digits=10,decimal_places=8,default=0.000)
    asking_price = fields.CharField(max_length=10,null=True,blank=True,default='0.0000')
    owner = fields.ForeignKeyField("models.Account",related_name="ltc_trade_history")
    date_added = fields.DatetimeField(default=datetime.utcnow(),auto_now_add=True)


class Livedata(Model):
    name = fields.CharField(max_length=200,null=True,blank=True)
    symbol = fields.CharField(max_length=200,null=True,blank=True)
    current_price = fields.CharField(max_length=200,null=True,blank=True)
    price_change = fields.CharField(max_length=200,null=True)
    arrow = fields.CharField(max_length=100,null=True)
    asset_url=fields.CharField(max_length=2000,null=True,blank=True)


    

live_data=pydantic_model_creator(Livedata,name="Livedata")
live_dataIn=pydantic_model_creator(Livedata,name="LivedataIn")
live_dataOut=pydantic_model_creator(Livedata,name="LivedatOut")

user_pydantic = pydantic_model_creator(User,name="User",exclude=("is_verified"))
user_pydanticIn = pydantic_model_creator(User, name="UserIn",exclude_readonly=True,exclude=("is_verified","date_joined"))
user_pydanticOut =pydantic_model_creator(User,name="UserOut",exclude=("password"))

account_pydantic = pydantic_model_creator(Account,name="Account",exclude="is_verified")
account_pydanticIn = pydantic_model_creator(Account,name="AccountIn",exclude_readonly=True,exclude=("is_verified","owner"))
account_pydanticOut = pydantic_model_creator(Account,name="AccountOut",exclude=("owner","id"))

token_pydantic = pydantic_model_creator(Py_codes,name="Py_codes")
token_pydanticIn = pydantic_model_creator(Py_codes,name="Py_codesIn")
token_pydanticOut = pydantic_model_creator(Py_codes,name="Py_codesOut")

btc_pydantic = pydantic_model_creator(BtcAddress,name="BtcAddress")
btc_pydanticIn = pydantic_model_creator(BtcAddress,name="BtcAddressIn")
btc_pydanticOut = pydantic_model_creator(BtcAddress,name="BtcAddressOut")

litecoin_pydantic = pydantic_model_creator(LiteCoinAddress,name="LiteCoinAddress")
litecoin_pydanticIn = pydantic_model_creator(LiteCoinAddress,name="LiteCoinAddressIn")
litecoin_pydanticOut = pydantic_model_creator(LiteCoinAddress,name="LiteCoinAddressOut")

dashcoin_pydantic = pydantic_model_creator(DashCoinAddress,name="DashCoinAddress")
dashcoin_pydanticIn = pydantic_model_creator(DashCoinAddress,name="DashCoinAddressIn")
dashcoin_pydanticOut = pydantic_model_creator(DashCoinAddress,name="DashCoinAddressOut")

eth_pydanctic = pydantic_model_creator(EthereiumAddress,name="EthAddress")
eth_pydancticIn = pydantic_model_creator(EthereiumAddress,name="EthAddressIn")
eth_pydancticOut = pydantic_model_creator(EthereiumAddress,name="EthAddressOut")
# BNB CODES
bnb_pydanctic = pydantic_model_creator(BNBAddress,name="BNBAddress")
bnb_pydancticIn = pydantic_model_creator(BNBAddress,name="BNBAddressIn")
bnb_pydancticOut = pydantic_model_creator(BNBAddress,name="BNBAddressOut")

eth_transaction_pydantic = pydantic_model_creator(EtheriumTransactionHistory,name="EthereiumTransaction")
eth_transaction_pydanticIn = pydantic_model_creator(EtheriumTransactionHistory,name="EthereiumTransactionIn")
eth_transaction_pydanticOut = pydantic_model_creator(EtheriumTransactionHistory,name="EthereiumTransactionOut")

btc_transaction_pydantic = pydantic_model_creator(BTCTransactionHistory,name="BTCTransaction")
btc_transaction_pydanticIn = pydantic_model_creator(BTCTransactionHistory,name="BTCTransactionIn")
btc_transaction_pydanticOut = pydantic_model_creator(BTCTransactionHistory,name="BTCTransactionOut")

dash_transaction_pydantic = pydantic_model_creator(DashCoinTransactionHistory,name="DashCoinTransaction")
dash_transaction_pydanticIn = pydantic_model_creator(DashCoinTransactionHistory,name="DashCoinTransactionIn")
dash_transaction_pydanticOut = pydantic_model_creator(DashCoinTransactionHistory,name="DashCoinTransactionOut")

lite_transaction_pydantic = pydantic_model_creator(LiteCoinTransactionHistory,name="LiteCoinTransaction")
lite_transaction_pydanticIn = pydantic_model_creator(LiteCoinTransactionHistory,name="LiteCoinTransactionIn")
lite_transaction_pydanticOut = pydantic_model_creator(LiteCoinTransactionHistory,name="LiteCoinTransactionOut")



# BTC TRADES
bnb_trade_history_pydantic = pydantic_model_creator(BnbBtcTradeHistory,name="BnbBtcTradeHistory")
bnb_trade_history_pydanticIn = pydantic_model_creator(BnbBtcTradeHistory,name="BnbBtcTradeHistoryIn",exclude_readonly=True,exclude=("date_added"))
bnb_trade_history_pydanticOut = pydantic_model_creator(BnbBtcTradeHistory,name="BnbBtcTradeHistoryOut")

eth_trade_history_pydantic = pydantic_model_creator(EthBtcTradeHistory,name="EthBtcTradeHistory")
eth_trade_history_pydanticIn = pydantic_model_creator(EthBtcTradeHistory,name="EthBtcTradeHistoryIn",exclude_readonly=True,exclude=("date_added"))
eth_trade_history_pydanticOut = pydantic_model_creator(EthBtcTradeHistory,name="EthBtcTradeHistoryOut",)

ltc_trade_history_pydantic = pydantic_model_creator(LtcBtcTradeHistory,name="LtcBtcTradeHistory")
ltc_trade_history_pydanticIn = pydantic_model_creator(LtcBtcTradeHistory,name="LtcBtcTradeHistoryIn",exclude_readonly=True,exclude=("date_added"))
ltc_trade_history_pydanticOut = pydantic_model_creator(LtcBtcTradeHistory,name="LtcBtcTradeHistoryOut")