from app.utills import bnb_info,eth_info,ltc_info,dash_info ,_dash_usd,_ltc_usd,_bnb_usd,_btc_usd,_eth_usd
# conversion rate from the live market
def bnb_btc(bnb_value):
    btc_value = float(bnb_value) * float(bnb_info['price'])
    return btc_value

def eth_btc(eth_value):
    btc_value = float(eth_value) * float(eth_info['price'])
    return btc_value

def ltc_btc(ltc_valuue):
    btc_value=float(ltc_valuue) * float(ltc_info['price'])
    return btc_value

def dash_btc(dash_value):
    btc_value=float(dash_value) * float(dash_info['price'])
    return btc_value

# total balance in USD converter

def btc_usd(btc_value):
    usd_value = float(btc_value) * float(_dash_usd['price'])
    return usd_value 


def eth_usd(btc_value):
    usd_value = float(btc_value) * float(_eth_usd['price'])
    return usd_value 

def ltc_usd(ltc_value):
    usd_value = float(ltc_value) * float(_ltc_usd['price'])
    return usd_value

def bnb_usd(bnb_value):
    usd_value = float(bnb_value) * float(_bnb_usd['price'])
    return usd_value

def dash_usd(dash_value):
    usd_value = float(dash_value) * float(_dash_usd['price'])
    return usd_value