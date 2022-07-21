import requests
END_POINT ='https://api.binance.com'
PATH ='/api/v3/klines'
    
# ==============================================================BTC TO USD ====================================================================================
def get_1_mins_btcusd_candle_stick():
    PARAMS = '?symbol=BTCUSDT&interval=1m'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_5_mins_btcusd_candle_stick():
    PARAMS = '?symbol=BTCUSDT&interval=5m'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_30_mins_btcusd_candle_stick():
    PARAMS = '?symbol=BTCUSDT&interval=30m'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_1_hr_btcusd_candle_stick():
    PARAMS = '?symbol=BTCUSDT&interval=1h'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_2_hrs_btcusd_candle_stick():
    PARAMS = '?symbol=BTCUSDT&interval=2h'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_4_hrs_btcusd_candle_stick():
    PARAMS = '?symbol=BTCUSDT&interval=4h'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_6_hrs_btcusd_candle_stick():
    PARAMS = '?symbol=BTCUSDT&interval=6h'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_8_hrs_btcusd_candle_stick():
    PARAMS = '?symbol=BTCUSDT&interval=8h'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_12_hrs_btcusd_candle_stick():
    PARAMS = '?symbol=BTCUSDT&interval=12h'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_1_day_btcusd_candle_stick():
    PARAMS = '?symbol=BTCUSDT&interval=1d'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_3_days_btcusd_candle_stick():
    PARAMS = '?symbol=BTCUSDT&interval=3d'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_1_week_btcusd_candle_stick():
    PARAMS = '?symbol=BTCUSDT&interval=1w'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_1_month_btcusd_candle_stick():
    PARAMS = '?symbol=BTCUSDT&interval=1m'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

# ============================================================= ETH TO USDT ================================================================================================
def get_1_mins_ethusd_candle_stick():
    PARAMS = '?symbol=ETHUSDT&interval=1m'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_5_mins_ethusd_candle_stick():
    PARAMS = '?symbol=ETHUSDT&interval=5m'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_30_mins_ethusd_candle_stick():
    PARAMS = '?symbol=ETHUSDT&interval=30m'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_1_hr_ethusd_candle_stick():
    PARAMS = '?symbol=ETHUSDT&interval=1h'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_2_hrs_ethusd_candle_stick():
    PARAMS = '?symbol=ETHUSDT&interval=2h'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_4_hrs_ethusd_candle_stick():
    PARAMS = '?symbol=ETHUSDT&interval=4h'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_6_hrs_ethusd_candle_stick():
    PARAMS = '?symbol=ETHUSDT&interval=6h'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_8_hrs_ethusd_candle_stick():
    PARAMS = '?symbol=ETHUSDT&interval=8h'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_12_hrs_ethusd_candle_stick():
    PARAMS = '?symbol=ETHUSDT&interval=12h'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_1_day_ethusd_candle_stick():
    PARAMS = '?symbol=ETHUSDT&interval=1d'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_3_days_ethusd_candle_stick():
    PARAMS = '?symbol=ETHUSDT&interval=3d'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_1_week_ethusd_candle_stick():
    PARAMS = '?symbol=ETHUSDT&interval=1w'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_1_month_ethusd_candle_stick():
    PARAMS = '?symbol=ETHUSDT&interval=1m'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

# ================================================================================ BNB TO USDT ========================================================================
def get_1_mins_bnbusd_candle_stick():
    PARAMS = '?symbol=BNBUSDT&interval=1m'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_5_mins_bnbusd_candle_stick():
    PARAMS = '?symbol=BNBUSDT&interval=5m'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_30_mins_bnbusd_candle_stick():
    PARAMS = '?symbol=BNBUSDT&interval=30m'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_1_hr_bnbusd_candle_stick():
    PARAMS = '?symbol=BNBUSDT&interval=1h'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_2_hrs_bnbusd_candle_stick():
    PARAMS = '?symbol=BNBUSDT&interval=2h'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_4_hrs_bnbusd_candle_stick():
    PARAMS = '?symbol=BNBUSDT&interval=4h'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_6_hrs_bnbusd_candle_stick():
    PARAMS = '?symbol=BNBUSDT&interval=6h'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_8_hrs_bnbusd_candle_stick():
    PARAMS = '?symbol=BNBUSDT&interval=8h'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_12_hrs_bnbusd_candle_stick():
    PARAMS = '?symbol=BNBUSDT&interval=12h'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_1_day_bnbusd_candle_stick():
    PARAMS = '?symbol=BNBUSDT&interval=1d'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_3_days_bnbusd_candle_stick():
    PARAMS = '?symbol=BNBUSDT&interval=3d'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_1_weeks_bnbusd_candle_stick():
    PARAMS = '?symbol=BNBUSDT&interval=1w'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_1_month_bnbusd_candle_stick():
    PARAMS = '?symbol=BNBUSDT&interval=1m'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

# ====================================================================== LITECOIN TO USDT ====================================================================================
def get_1_mins_ltcusd_candle_stick():
    PARAMS = '?symbol=LTCUSDT&interval=1m'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_5_mins_ltcusd_candle_stick():
    PARAMS = '?symbol=LTCUSDT&interval=5m'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_30_mins_ltcusd_candle_stick():
    PARAMS = '?symbol=LTCUSDT&interval=30m'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_1_hr_ltcusd_candle_stick():
    PARAMS = '?symbol=LTCUSDT&interval=1h'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_2_hrs_ltcusd_candle_stick():
    PARAMS = '?symbol=LTCUSDT&interval=2h'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_4_hrs_ltcusd_candle_stick():
    PARAMS = '?symbol=LTCUSDT&interval=4h'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_6_hrs_ltcusd_candle_stick():
    PARAMS = '?symbol=LTCUSDT&interval=6h'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_8_hrs_ltcusd_candle_stick():
    PARAMS = '?symbol=LTCUSDT&interval=8h'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_12_hrs_ltcusd_candle_stick():
    PARAMS = '?symbol=LTCUSDT&interval=12h'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_1_day_ltcusd_candle_stick():
    PARAMS = '?symbol=LTCUSDT&interval=1d'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_3_days_ltcusd_candle_stick():
    PARAMS = '?symbol=LTCUSDT&interval=3d'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_1_weeks_ltcusd_candle_stick():
    PARAMS = '?symbol=LTCUSDT&interval=1w'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()

def get_1_month_ltcusd_candle_stick():
    PARAMS = '?symbol=LTCUSDT&interval=1m'
    r= requests.get(END_POINT+PATH+PARAMS)
    return r.json()



