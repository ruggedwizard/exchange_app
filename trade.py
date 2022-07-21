# # Trading functionalities Breakdown 
# # # Check if the user account is greater than the amount they are trying to place in the market
# # # if its less than the amount they want to place then show insufficient funds
# # # if the account is greater than their ammount then transfer the funds to the main wallet (show receiving address of the main account and send there) 

# # # TRACKING THE FUNDS AND
API_KEY = "SHgH7j0CDHjvvA6SgmnaW0gPD6fWzl4IdcVCx6CdHQsNfac98TMUpylis3RKfKZl"

API_SECRET ="svMNhjBQywLS4UGfAUWu5CiZWNHyLF7qfQW1aOyDxYp1mRm4uzCQnP6FRXMoqolQ"

# # TEST_NET
# BINANCE_API_KEY = 'nYx4Rf2zwjkqWHV1eCLELOjqpLM7FAbG8ZJUI3BEB1uLUHoRFvRj4SaGOWRrXsQA'
# BINANCE_API_SECRET = 'LIcxMA6UePQprVfELQnhduhLXLjGfe40JdMUYaqRoRf9qVhxt3csH2mRhFLmMwcP'
# # test net 2
TEST_NET_API_KEY ='fOSZEwwZPVdWaNLXua0a1P8FKScZNagREQ6Gi2NqadVBQ4nOKCxJS4dem4pCPNQ3'
TEST_NET_API_SECRET = '5dclGiSfjKdk8xZppEWIU6ivkBN1LBvwmweM0sTP9imWnRVLBCwZMoeV4V4ul0Dk'
# # 

# from app.converter import bnb_btc
from binance.client import Client
from binance.enums import * 

# from binance.client import Client
client = Client(TEST_NET_API_KEY, TEST_NET_API_SECRET,testnet=True)
# client = Client(API_KEY, API_SECRET)


# to copy


# orders = client.get_all_margin_orders(symbol='BNBBTC')
# print(orders)

# eth_usd = client.get_margin_price_index(symbol='ETHUSDT')
# btc_usd = client.get_margin_price_index(symbol='BTCUSDT')
# bnb_usd = client.get_margin_price_index(symbol='BNBUSDT')
# ltc_usd = client.get_margin_price_index(symbol='LTCUSDT')
# dash_usd = client.get_margin_price_index(symbol='DASHUSDT')

# print(dash_usd)
# print(orders)
# # info = client.get_account()
# # print(info)
# # details = client.get_asset_details()
# # print(details)
# # order = client.create_order(
# #     symbol='BNBBTC',
# #     side=SIDE_BUY,
# #     type=ORDER_TYPE_LIMIT,
# #     timeInForce=TIME_IN_FORCE_GTC,
# #     quantity=0.04,
# #     price='0.009510',
# #     stopPrice='0.009510'
# # #     )
# # order = client.order_limit_buy(
# # #     symbol='BNBBTC',
# # #     quantity=1,
# # #     price='0.00960')
# # # print(order)

# # # # info = client.get_margin_price_index(symbol='DASHBTC')
# # # # print(info)
# # # # # print(float(info['price']))

# get transaction status
# order = client.get_order(
#     symbol='BNBBTC',
#     orderId='1921488')
# print(order)

# # # cancel an order
# # result = client.cancel_order(
# #     symbol='BNBBTC',
# #     orderId='132439')

# # print(result)

# # data= 'osso'
# # print(data.upper())
# # convert bnb to btc 

# # def bnb_btc(bnb_value):
# #     btc_value = float(bnb_value) * 0.0096
# #     return btc_value



# # print(bnb_btc((0.5)))

# order = client.order_limit_buy(
#     symbol='BNBBTC',
#     quantity=5,
#     price='0.010')
# print(order)
# order = client.order_limit_buy(
#     symbol='BNBBTC',
#     quantity=1,
#     price='0.009')

# order = client.order_market_buy(
#     symbol='BNBBTC',
#     quantity=3)
# print(order)

# # print(order)
# def buy_limit_order(symbol,quantity,price):
#     order = client.order_limit_buy(
#     symbol=symbol,
#     quantity=quantity,
#     price=price)
#     return order

# trade = buy_limit_order('BNBBTC',1,'0.03')

# print(trade)
# _price=trade['fills']

# for _ in _price:
#     print(_['price'])


# order = client.create_order(
#     symbol='BNBBTC',
#     side=SIDE_BUY,
#     type=ORDER_TYPE_LIMIT,
#     timeInForce=TIME_IN_FORCE_GTC,
#     quantity=1,
#     price='0.020')

# print(order)
# TEST_NET_API_KEY ='J20QkD4X4wrasyfEIGUjO8GTdhqISbDDqVTmAneDwb2kDt5LtNgVcyktR8GfoEEL'
# TEST_NET_API_SECRET = 'IvCjGzWWPwP2wJvKKyHv2IRwQehmDyDTeGQ5Zrv0fE8xSqD6pq1gqzTEuUhhRKWs'

# order = client.create_order(
#     symbol='BNBBTC',
#     side=SIDE_SELL,
#     type=ORDER_TYPE_TAKE_PROFIT_LIMIT,
#     timeInForce=TIME_IN_FORCE_GTC,
#     stopPrice='0.011',
#     quantity=2,
#     price='0.013')


# print(order)

# # def place_buy_stop_order(symbol,stopPrice,quantity,price):
# #     order = client.create_order(
# #     symbol=symbol,
# #     side=SIDE_BUY,
# #     type=ORDER_TYPE_TAKE_PROFIT_LIMIT,
# #     timeInForce=TIME_IN_FORCE_GTC,
# #     stopPrice=stopPrice,
# #     quantity=quantity,
# #     price=price)
# #     return order
# # # this returns order['symbol'] = 'TARDE SYMBOL'
# # # this returns order['orderId'] = 'ORDER ID'
# # # lock the user price price in BTC 
# # # 



# # def place_sell_stop_order(symbol,stopPrice,quantity,price):
# #     order = client.create_order(
# #     symbol=symbol,
# #     side=SIDE_SELL,
# #     type=ORDER_TYPE_TAKE_PROFIT_LIMIT,
# #     timeInForce=TIME_IN_FORCE_GTC,
# #     stopPrice=stopPrice,
# #     quantity=quantity,
# #     price=price)
# #     return order

# print(bnb_btc('1'))

# from twilio.rest import Client

# # # Your Account SID from twilio.com/console
# account_sid = "AC9c0be2e15cfd1b9a4cc80d70dea7fc27"
# # Your Auth Token from twilio.com/console
# auth_token  = "33f839de5310b9fdf171cec5cc7296e7"

# client = Client(account_sid, auth_token)

# message = client.messages.create(
#     to="+2348102492540", 
#     # from_="+19705572052",
#     from_="+19705572052",
#     body="Hello from Python!")

# print(message.sid)

# for sms in client.messages.list():
#   print(sms.to)

# To get all orders from the live market
# info = client.get_account()

# print(info)
# fees = client.get_trade_fee()
# orders = client.get_open_orders(symbol='BNBBTC')

# print(orders)