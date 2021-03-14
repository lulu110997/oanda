'''
import json
from oandapyV20 import API    # the client
import oandapyV20.endpoints.trades as trades

client = API(access_token=access_token)

# request trades list
r = trades.TradesList(accountID)
rv = client.request(r)
print("RESPONSE:{escape_char}n{}".format(json.dumps(rv, indent=2)))
 '''
import configparser
# import pandas as pd
# import json
# import oandapyV20.endpoints.accounts as accounts
import datetime
import oandapyV20 as opy
import oandapyV20.endpoints.instruments as instruments

# Read the ini file to obtain the account id and access token
config = configparser.ConfigParser()
config.read('oanda.ini')
account_id = config['oanda']['account_id']
access_token = config['oanda']['access_token']
environment = config['oanda']['environment']

oanda = opy.API(access_token, environment)

## Instruments that this account is allowed to trade ##
# req = accounts.AccountInstruments(account_id)
# rcv = oanda.request(req)
# print(json.dumps(rcv, indent=2))
## End ##

params = {
  "count": 5,
  "granularity": "H6"
}

r = instruments.InstrumentsCandles(instrument="USD_CAD",
                                    params=params)
oanda.request(r)
print(r.response['candles'][1]['time'])
timestamp = datetime.datetime.fromtimestamp(1500000000)
print(timestamp.strftime('%Y-%m-%d %H:%M:%S'))