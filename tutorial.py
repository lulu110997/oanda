import configparser
import pandas as pd
from datetime import datetime
import oandapyV20 as opy
import oandapyV20.endpoints.instruments as instruments
import mplfinance as mpf
import dateutil.parser

# Read the ini file to obtain the account id and access token
config = configparser.ConfigParser()
config.read('oanda.ini')
account_id = config['oanda']['account_id']
access_token = config['oanda']['access_token']
environment = config['oanda']['environment']

oanda = opy.API(access_token, environment)

params = {
  "count": 5,
  "granularity": "H6"
}

r = instruments.InstrumentsCandles(instrument="USD_CAD",
                                    params=params)
oanda.request(r)
candles = r.response['candles']
for i in candles:
    i.pop('complete')
    i['time'] = dateutil.parser.isoparse(i['time'])
    i['time'] = datetime.timestamp(i['time'])
    olhc = i.pop('mid')
    i['Date'] = i.pop('time')
    i['Volume'] = i.pop('volume')
    i['Open'] = float(olhc['o'])
    i['High'] = float(olhc['h'])
    i['Low'] = float(olhc['l'])
    i['Close'] = float(olhc['c'])
    i['Volume'] = float(i['Volume'])

print(candles)
df = pd.DataFrame(candles)
df['Datetime'] = pd.to_datetime(df['Date'])
df = df.set_index('Datetime')
df = df.drop(['Date'], axis=1)
df.to_csv('C:\\Users\\louis\\Downloads\\del\\csv.csv')
mpf.plot(df,type='candle', mav=(3), volume=True)
