from pytdx.exhq import TdxExHq_API
from pytdx.exhq import TDXParams
import pandas as pd
from ta import trend,momentum
import numpy as np
from pytdx.config.hosts import hq_hosts
api = TdxExHq_API(heartbeat=True)
import time
symol = "YL8"
with api.connect('124.74.236.94', 7721):
    #[print (i) for i in api.get_markets()]
    while True:
        time.sleep(1)
        now = ("%s" % time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time())))
        call = []


        df = api.get_instrument_bars(category = TDXParams.KLINE_TYPE_1MIN,
                                market = 29,
                                code = symol,
                                start = 0,
                                count=200)
        df = pd.DataFrame(df)
        df = df[['datetime','open', 'high', 'low', 'close',]]
        print (df)

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

        if df.iloc[-1]["macd_across"] != df.iloc[-2]["macd_across"]:
            if df.iloc[-1]["macd_across"] ==1:

                message = " macd上穿 %s%s" % (now, symol)
                call.append(message)
                #dingtalk(webhook=dinghook, message="%s" % message)
                #time.sleep(1)
            if df.iloc[-1]["macd_across"] == -1:
                message = " macd下穿 %s%s" % (now, symol)
                call.append(message)
        if (df.iloc[-1]["macd"] > 0) & (df.iloc[-2]["macd"] < 0):
            # 当macd柱子向上穿越到零轴
            message = "macd柱向上突破零轴 %s%s " % (now, symol)
            call.append(message)
        if (df.iloc[-1]["macd"] < 0) & (df.iloc[-2]["macd"] > 0):
            # 当macd柱子跌破零轴
            message = "macd柱向下跌破零轴 %s%s " % (now, symol)
            call.append(message)
        if df.iloc[-1]["ema_across"] != df.iloc[-2]["ema_across"]:
            if df.iloc[-1]["ema_across"] == 1:
                message = "ma34 > ma144 %s%s " % (now, symol)
                call.append(message)
            if df.iloc[-1]["ema_across"] == -1:
                message = "ma34 < ma144  %s%s " % (now, symol)
                call.append(message)


            # if df.iloc[-1]["close_postion"] != df.iloc[-2]["close_postion"]:
            #     if df.iloc[-1]["close_postion"] == 1:
            #         message = "价格向上突破快慢线，做多 %s%s " % (now,symbol)
            #     if df.iloc[-1]["close_postion"] == 0:
            #         message = "价格位于快慢线之间，平仓 %s%s " % (now, symbol)
            #     if df.iloc[-1]["close_postion"] == -1:
            #         message = "价格位于跌破快慢线，做空 %s%s " % (now, symbol)

            # dingtalk(webhook=dinghook, message="%s" % message)
            # time.sleep(1)
        df.dropna(axis=0, how='any', inplace=True)
        df = df.round(2)
        print (df)
        print ("message:%s" % (call))
        print (df.columns)
