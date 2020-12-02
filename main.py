import pandas as pd
from forexconnect import ForexConnect
import time
import numpy as np
from ta import trend,volatility,momentum
import ta
# from Trader import configs
from datetime import datetime
import numpy as np
from ta import trend
from forexconnect import fxcorepy
from dingtalkchatbot.chatbot import DingtalkChatbot

def SMA(df, base, target, period):
    #base=收盘价的列名  target = 生成的列名  period = 需要什么样的周期
    df["%s%s" % (target,period)] = df[base].rolling(window=period).mean()
    df["%s%s" % (target,period)].fillna(np.nan, inplace=True)
    df["%s%s" % (target, period)] = df["%s%s" % (target,period)].round(2)
    return df


def dingtalk(webhook,message:str):
    secret = 'SEC11b9...这里填写自己的加密设置密钥'  # 可选：创建机器人勾选“加签”选项时使用
    # 初始化机器人小丁
    #xiaoding = DingtalkChatbot(webhook)  # 方式一：通常初始化方式
    # xiaoding = DingtalkChatbot(webhook, secret=secret)  # 方式二：勾选“加签”选项时使用（v1.5以上新功能）
    ding = DingtalkChatbot(webhook, pc_slide=True)
    ding.send_text(msg='监控:%s' % message, is_at_all=False)
    with open('log.txt', 'a') as f:
        print("保存文件")
        f.write(message)
        f.write("\n")
def status_callback(session: fxcorepy.O2GSession,
                    status: fxcorepy.AO2GSessionStatus.O2GSessionStatus):
    print("Trading session status: " + str(status))
    #return str(status)

def print_order_row(order_row, account_id):
    if order_row.table_type == ForexConnect.ORDERS:
        if not account_id or account_id == order_row.account_id:
            string = ""
            for column in order_row.columns:
                string += column.id + "=" + str(order_row[column.id]) + "; "
            print(string)
#dingtalk(webhook=configs.dinghook,message="监控:%s" % configs.instrument)
def main():
    now = ("%s"%time.strftime('%Y.%m.%d %H:%M:%S ',time.localtime(time.time())))

    history = fx.get_history(instrument=symbol, timeframe="m1", quotes_count=200)
    if history.size != 0:
        df = pd.DataFrame(history)
        df = df[['Date', 'BidOpen', 'BidHigh', 'BidLow', 'BidClose', 'Volume',]]
        df.rename(
            columns={'Date': "datetime", 'BidOpen': "open", "BidHigh": "high", "BidLow": "low", "BidClose": "close",
                     'Volume': "volume",}, inplace=True)

        df['ema_f_h'] = trend.ema(df.high, periods=34)
        df['ema_f_c'] = trend.ema(df.close, periods=34)
        df['ema_f_l'] = trend.ema(df.low, periods=34)
        df['ema_s_h'] = trend.ema(df.high, periods=144)
        df['ema_s_c'] = trend.ema(df.close, periods=144)
        df['ema_s_l'] = trend.ema(df.low, periods=144)

        # MACD(df, fast=55, slow=144, n=55)
        df["macd"] = trend.MACD(df.close, n_slow=144, n_fast=55, n_sign=55).macd()
        df["macd_signal"] = trend.MACD(df.close, n_slow=144, n_fast=34, n_sign=34).macd_signal()
        df['macd_postion'] = np.where(df.macd > df.macd_signal, int(1), int(-1))  # 上穿1，下穿-1

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
        df["close_postion"] = np.where((df['close'] > df['ema_f_c']) & (df['close'] > df['ema_s_c']), int(1),
                                       np.where((df['close'] < df['ema_f_c']) & (df['close'] < df['ema_s_c']), int(-1),
                                                int(0)))


        if df.iloc[-1]["macd_postion"] != df.iloc[-2]["macd_postion"]:
            message = " macd交叉 %s%s" % (now,symbol)
            dingtalk(webhook=dinghook,message="%s" % message)
            time.sleep(1)

        if (df.iloc[-1]["macd"] >0) & (df.iloc[-2]["macd"] <0):
            #当macd柱子向上穿越到零轴
            message = "macd柱向上突破零轴 %s%s " % (now,symbol)
            dingtalk(webhook=dinghook,message="%s" % message)
            time.sleep(1)
        if (df.iloc[-1]["macd"] <0) & (df.iloc[-2]["macd"] >0):
            #当macd柱子跌破零轴
            message = "macd柱向下跌破零轴 %s%s " % (now,symbol)
            dingtalk(webhook=dinghook,message=":%s" % message)
            time.sleep(1)
        if df.iloc[-1]["close_postion"] != df.iloc[-2]["close_postion"]:
            if df.iloc[-1]["close_postion"] == 1:
                message = "价格向上突破快慢线，做多 %s%s " % (now,symbol)
            if df.iloc[-1]["close_postion"] == 0:
                message = "价格位于快慢线之间，平仓 %s%s " % (now, symbol)
            if df.iloc[-1]["close_postion"] == -1:
                message = "价格位于跌破快慢线，做空 %s%s " % (now, symbol)

            dingtalk(webhook=dinghook,message="%s" % message)
            time.sleep(1)


        df = df.round(2)
        print("%s 收盘快慢线:%s macd状态:%s RSI状态：%s cci状态：%s "%(now,df.iloc[-1]["close_postion"],df.iloc[-1]["macd_postion"],df.iloc[-1]["rsi_postion"],df.iloc[-1]["cci_postion"]))
    #chart(main())

if __name__ == "__main__":
    symbol = "US30"
    USER = "D103403723"

    PASS = input("password:")
    URL = "http://www.fxcorporate.com/Hosts.jsp"
    ENV = "demo"  # or "real"
    dinghook = 'https://oapi.dingtalk.com/robot/send?access_token=0bc405cea1acf99a4de3a084bb9e99f5a19923a8fa5b6dd6eb185f511db67e91'
    fx = ForexConnect()
    fx.login(user_id=USER, password=PASS, url=URL, connection=ENV, session_status_callback=status_callback)
    while True:
        if datetime.now().second==59:
            main()