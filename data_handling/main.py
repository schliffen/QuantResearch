#
"""
start of developing data processing



"""
import numpy as np
import ccxt
from pprint import pprint
import pandas as pd
import matplotlib.pyplot as plt
from hurst import compute_Hc, random_walk
import seaborn as sns
import yfinance as yf
import plotly.graph_objs as go

# sns.set();



def get_data( symbol='JPYAUD=X', freq='1h', limit='1d'):


    data = yf.download(tickers = symbol ,period =limit, interval = freq)


    return data

def visualize( data ):
    #declare figure
    fig = go.Figure()

    #Candlestick
    fig.add_trace(go.Candlestick(x=data.index,
                                 open=data['Open'],
                                 high=data['High'],
                                 low=data['Low'],
                                 close=data['Close'], name = 'market data'))

    # Add titles
    fig.update_layout(
        title='Japanese Yen/Australian Dollar')

    #Show
    fig.show()



if __name__=="__main__":

    #
    data = get_data( 'EURUSD=X', freq='1d', limit='max')

    # trying to test algorithm
    # ------------------------------------
    # check if its stationary
    # ------------------------------------




    # series = np.cumprod(btc_usdt_ohlcv[:,1])
    H, c, result = compute_Hc(btc_usdt_ohlcv[:,4], kind='price', simplified=True)

    plt.rcParams['figure.figsize'] = 10, 5
    f, ax = plt.subplots()
    _ = ax.plot(result[0], c*result[0]**H)
    _ = ax.scatter(result[0], result[1])
    _ = ax.set_xscale('log')
    _ = ax.set_yscale('log')
    _ = ax.set_xlabel('log(time interval)')
    _ = ax.set_ylabel('log(R/S ratio)')


    print("H={:.3f}, c={:.3f}".format(H,c))
    plt.show()








print("Finished! ")