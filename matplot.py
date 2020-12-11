import pandas as pd
from forexconnect import ForexConnect
from forexconnect import fxcorepy
import time
import numpy as np
from ta import trend,volatility,momentum
import ta
import mplfinance as mpf

def status_callback(session: fxcorepy.O2GSession,
                    status: fxcorepy.AO2GSessionStatus.O2GSessionStatus):
    print("Trading session status: " + str(status))


def bar():

    history = fx.get_history(instrument=symbol, timeframe="m1", quotes_count=300)
    # print (history)
    if history.size != 0:
        df = pd.DataFrame(history)
        df = df[['Date', 'BidOpen', 'BidHigh', 'BidLow', 'BidClose', 'Volume', ]]
        df.rename(
            columns={'Date': "datetime", 'BidOpen': "open", "BidHigh": "high", "BidLow": "low",
                     "BidClose": "close",
                     'Volume': "volume", }, inplace=True)

        df['ema_f_h'] = trend.ema(df.high, periods=34)
        df['ema_f_c'] = trend.ema(df.close, periods=34)
        df['ema_f_l'] = trend.ema(df.low, periods=34)
        df['ema_s_h'] = trend.ema(df.high, periods=144)
        df['ema_s_c'] = trend.ema(df.close, periods=144)
        df['ema_s_l'] = trend.ema(df.low, periods=144)
        df['ema_across'] = np.where(df.ema_f_c > df.ema_s_c, int(1), int(-1))  # 上穿1，下穿-1
        # MACD(df, fast=55, slow=144, n=55)
        df["macd"] = trend.MACD(df.close, n_slow=144, n_fast=34, n_sign=34).macd()
        df["macd_signal"] = trend.MACD(df.close, n_slow=144, n_fast=34, n_sign=34).macd_signal()
        df['macd_across'] = np.where(df.macd > df.macd_signal, int(1), int(-1))  # 上穿1，下穿-1

        df['rsi'] = momentum.rsi(df.close, n=34, )
        df['emarsi'] = trend.ema(df.rsi, periods=34)
        df['rsi_postion'] = np.where(df.rsi > df.emarsi, int(1), int(-1))  # 上穿1，下穿-1

        # df['stoch'] = momentum.stoch(high=df["high"],low=df["low"],close=df["close"],n=144)
        # df['stoch_signal'] = momentum.stoch_signal(high=df["high"],low=df["low"],close=df["close"],n=144)
        # df["stoch_sig"] = np.where(df["stoch"] > df["stoch_signal"], 1, 0)
        # df["stoch_sig_shfit"] = df["stoch_sig"].shift(1)

        df['cci'] = trend.cci(df.high, df.low, df.close, n=55, )
        df['emacci'] = trend.ema(df.cci, periods=55)
        df['cci_postion'] = np.where(df.cci > df.emacci, int(1), int(-1))  # 上穿1，下穿-1

        # 价格为于快线与慢线之上则为1，快慢线之下则为-1，其它为0
        df["close_postion"] = np.where((df['close'] > df['ema_f_c']) & (df['close'] > df['ema_s_c']),
                                       int(1),
                                       np.where(
                                           (df['close'] < df['ema_f_c']) & (df['close'] < df['ema_s_c']),
                                           int(-1),
                                           int(0)))
        return df
def matplot(df):
    df.set_index('datetime', inplace=True)
    ap0 = [
        mpf.make_addplot(df['ema_f_h'], color='gray', width=0.7),
        mpf.make_addplot(df['ema_f_c'], color='gray', width=0.7, linestyle='dotted'),
        mpf.make_addplot(df['ema_f_l'], color='gray', width=0.7),
        mpf.make_addplot(df['ema_s_h'], color='gray', width=0.7),
        mpf.make_addplot(df['ema_s_c'], color='gray', width=0.7, linestyle='dotted'),
        mpf.make_addplot(df['ema_s_l'], color='gray', width=0.7),
        mpf.make_addplot(df['macd'], type='bar', color='gray', width=0.5, panel=1),  # 柱子
        mpf.make_addplot(df['macd_signal'], width=0.3, color='r', panel=1, alpha=1),  # 信號線
        mpf.make_addplot(df['rsi'], color='gray', width=0.7, panel=2),
        mpf.make_addplot(df['emarsi'], color='red', width=0.5, panel=2),
        mpf.make_addplot(df['cci'], color='k', width=0.5, panel=3),
        mpf.make_addplot(df['emacci'], color='red', width=0.5, panel=3),
        # mpf.make_addplot(df['close_postion'], color='red', width=0.5, panel=1),
    ]
    pl = mpf.plot(df, type='candle',
                  volume=False,
                  ylabel='price',
                  # savefig='%s' % (symbol) + '.jpg',
                  addplot=ap0, panel_ratios=(1, 0.3, 0.3, 0.3, 0.3), num_panels=5, style='binance',
                  )


    #mpf.show()
if __name__ == "__main__":

    USER = "D103403723"
    PASS = "qwe123@@"
    URL = "http://www.fxcorporate.com/Hosts.jsp"
    ENV = "demo"  # or "real"
    fx = ForexConnect()
    fx.login(user_id=USER, password=PASS, url=URL, connection=ENV, session_status_callback=status_callback)
    symlist = symbolList = ['HKG33','USOil',"NAS100",'US30','SPX500','UK100','JPN225','XAG/USD','XAU/USD','CHN50','BTC/USD','USDOLLAR','USD/JPY',]
    symbol = symlist[-3]
    df = bar()
    matplot(df)
    # bar("BTC/USD")


