import configparser
import pandas as pd
import numpy as np

import mplfinance as mpf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import oandapyV20 as opy
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.orders as orders
## Some important documentations
# https://pypi.org/project/mplfinance/

def csv_for_testing(df):
    '''
    Only used for testing
    '''
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


def get_candles(granularity, instrument="USD_CAD", count=100):
    '''
    Returns candlestick information based on given parameters.
    Information is returned as a pandas df
    '''

    params = {
      "count": count,
      "granularity": granularity
    }

    oanda, __ = connect_to_server()
    r = instruments.InstrumentsCandles(instrument,
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

def calculate_rsi(df, period=14):
    '''
    Calculate rsi of a dataframe. Returns the
    dataframe with the rsi included
    '''
    delta = df['Close'].diff()
    d_up, d_down = delta.copy(), delta.copy()
    d_up[d_up < 0] = 0
    d_down[d_down > 0] = 0
    rol_up = d_up.rolling(period).mean()
    rol_down = np.absolute(d_down.rolling(period).mean())
    rs = rol_up / rol_down
    rsi = 100.0 - (100.0 / (1.0 + rs))

    new_column = str(period) + '-rsi'
    df[new_column] = rsi
    csv_for_testing(df)
    return df

def plot_candlestick(df, new_column):
    '''
    To plot multiple candlestick charts with EMA + other technical indicators
    using threading.
    '''
    apdict = mpf.make_addplot(df[new_column])
    mpf.plot(df, type='candle', volume=True, addplot=apdict)

def plot_rsi(df, new_column='14-rsi'):
    '''
    Plots rsi values using matplotlib
    '''
    plt.plot(df.index, df[new_column])
    axes = plt.gca()
    axes.set_ylim([0,100])
    print(df.index)
    plt.plot(df.index, [30]*100, 'k-')
    plt.plot(df.index, [70]*100, 'r-')
    xfmt = mdates.DateFormatter('%d-%m-%y %H:%M')
    axes.xaxis.set_major_formatter(xfmt)

    plt.show()


def main():
    periods = [10, 25, 51]
    new_columns = ['10-wma', '25-wma', '51-wma']
    data = get_candles('H8', 'USD_CAD')
    for i in periods:
        data = calculate_wma(data, i)
    data = calculate_rsi(data)
    # plot_candlestick(data, new_columns)
    plot_rsi(data)



main()