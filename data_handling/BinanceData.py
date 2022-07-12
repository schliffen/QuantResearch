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
# sns.set();


exchange = ccxt.binance({
    'apiKey': 'qxNvpFUlJJOMAjScLxJAlPPco88zwOMN3PvfH7nNtAH0Nx4MLMMF0Bw2bdNTrft2',
    'secret': 'W23WJtitNKJP73fm9WPiaj0KnlrwNGrlVnPOMNUWI1xzZEaUSsyB9UR7pbJUvInL',
    'enableRateLimit': True,  # https://github.com/ccxt/ccxt/wiki/Manual#rate-limit
    'options': {
        'defaultType': 'spot',
    },
})


def get_data( symbol='BTC/USDT', freq='1h', limit=100):
    print('CCXT Version:', ccxt.__version__)

    exchange.set_sandbox_mode(True)  # comment if you're not using the testnet
    markets = exchange.load_markets()
    exchange.verbose = True  # debug output

    balance = exchange.fetch_balance()
    positions = balance['info']['balances']
    # pprint(positions)

    # anaysis of the data
    btc_ticker = exchange.fetch_ticker(symbol)
    #
    btc_usdt_ohlcv = exchange.fetch_ohlcv(symbol, freq, limit=limit)

    #
    orderbook_binance_btc_usdt = exchange.fetch_order_book('BTC/USDT')
    return np.array(btc_usdt_ohlcv), orderbook_binance_btc_usdt

def visualize(orderbook_binance_btc_usdt ):
    bids_binance = orderbook_binance_btc_usdt['bids']
    asks_binanace = orderbook_binance_btc_usdt['asks']

    df_bid_binance = pd.DataFrame(bids_binance, columns=['price','qty'])
    df_ask_binance = pd.DataFrame(asks_binanace, columns=['price','qty'])

    fig, (ax1, ax2) = plt.subplots(2, figsize=(10, 8), dpi=80)

    ax1.plot(df_bid_binance['price'], df_bid_binance['qty'],label='Binance',color='g')
    ax1.fill_between(df_bid_binance['price'], df_bid_binance['qty'],color='g')

    ax2.plot(df_ask_binance['price'], df_ask_binance['qty'],label='FTX',color='r')
    ax2.fill_between(df_bid_binance['price'], df_bid_binance['qty'],color='r')

    ax1.set_title('Ask Price vs Quantity for Binance')
    ax2.set_title('Bid Price vs Quantity for Binance')
    plt.show()




if __name__=="__main__":

    #
    btc_usdt_ohlcv, askbid = get_data("BTC/USDT", "1h", 1000)

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