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
import pandas as pd
import oandapyV20 as opy
import oandapyV20.endpoints.accounts as accounts
import json


# Read the ini file to obtain the account id and access token
config = configparser.ConfigParser()
config.read('oanda.ini')
account_id = config['oanda']['account_id']
access_token = config['oanda']['access_token']
environment = config['oanda']['environment']

oanda = opy.API(access_token, environment)
r = accounts.AccountInstruments(account_id)
rv = oanda.request(r)
print(json.dumps(rv, indent=2))

