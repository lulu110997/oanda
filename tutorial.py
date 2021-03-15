import configparser
import pandas as pd
import numpy as np
import oandapyV20 as opy
import mplfinance as mpf
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.orders as orders

## Some important documentations
# https://pypi.org/project/mplfinance/

def csv_for_testing(df):
    df.to_csv('C:\\Users\\louis\\Downloads\\del\\csv.csv')


def create_order():
    '''
    Creates an order
    '''
    oanda, account_id = connect_to_server()
    req = orders.OrderCreate(account_id, data=data)
    client.request(req)
    print(req.response)


def connect_to_server():
    '''
    # Read the ini file to obtain the account id and access token
    '''

    config = configparser.ConfigParser()
    config.read('oanda.ini')
    account_id = config['oanda']['account_id']
    access_token = config['oanda']['access_token']
    environment = config['oanda']['environment']
    oanda = opy.API(access_token, environment)
    return oanda, account_id


def get_candles(granularity, instrument, count=100):
    '''
    Returns candlestick information based on given parameters.
    Information is returned as a pandas df
    '''

    params = {
      "count": count,
      "granularity": granularity
    }

    oanda, __ = connect_to_server()
    r = instruments.InstrumentsCandles(instrument="USD_CAD",
                                        params=params)
    oanda.request(r)
    candles = r.response['candles']

    for i in candles:
        i.pop('complete')
        olhc = i.pop('mid')
        i['Date'] = i.pop('time')
        i['Volume'] = i.pop('volume')
        i['Open'] = float(olhc['o'])
        i['High'] = float(olhc['h'])
        i['Low'] = float(olhc['l'])
        i['Close'] = float(olhc['c'])
        i['Volume'] = float(i['Volume'])

    df = pd.DataFrame(candles)
    df['Datetime'] = pd.DatetimeIndex(df['Date'])
    df = df.set_index('Datetime')
    df = df.drop(['Date'], axis=1)
    # csv_for_testing()
    return df

def calculate_wma(df, period):
    '''
    Calculate the weighted moving average to a list of candlestick
    prices.
    Returns a pandas dataframe with a columd for the wma 
    '''
    # Creates an array of weights for the wma calculation 
    weights = np.arange(1,period+1) 

    # Apply the wma calculation along the closing prices of df
    wma = df['Close'].rolling(period).apply(lambda closing_price: \
        np.dot(closing_price, weights)/weights.sum(), raw=True)

    # Add the calculated prices to the existing df
    new_column = str(period) + '-wma'
    df[new_column] = wma
    # csv_for_testing(df)
    return df

def plot_candlestick(df, new_column):
    '''
    To plot multiple candlestick charts with EMA + other technical indicators
    using threading.
    '''
    apdict = mpf.make_addplot(df[new_column])
    mpf.plot(df, type='candle', volume=True, addplot=apdict)

def main():
    periods = [10, 25, 51]
    new_columns = ['10-wma', '25-wma', '51-wma']
    data = get_candles('D', 'USD_CAD')
    for i in periods:
        data = calculate_wma(data, i)
    plot_candlestick(data, new_columns)

main()