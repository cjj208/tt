import pandas as pd
import ta
import os
import numpy as np
from datetime import datetime
from ta import trend
import time
os.chdir(r"D:\Python_projects\trade_projects\tt")
print (os.getcwd())
df = pd.read_csv("df.csv")
df["macd"]=ta.trend.MACD(df.close,55,144,55).macd()
df["macd_signal"]=ta.trend.MACD(df.close,55,144,55).macd_signal()
# df.dropna(axis=0, how='any', inplace=True)
# df['stoch'] = ta.momentum.stoch(high=df["high"], low=df["low"], close=df["close"], n=144)
# df['stoch_signal'] = ta.momentum.stoch_signal(high=df["high"], low=df["low"], close=df["close"], n=144)
# df["stoch_sig"] = np.where(df["stoch"] > df["stoch_signal"], 1, 0)
# df["stoch_sig_shfit"] = df["stoch_sig"].shift(1)
df = trend.ema_indicator(close=df.high, window=34)
now = str(datetime.now())

now = str(datetime.now())
time.sleep(3)
with open('log.txt', 'a') as f:

    print("进来了")
    f.write(now)
    f.write("\n")

print (now)



import pytz, datetime
local = pytz.timezone ("America/Los_Angeles")
naive = datetime.datetime.strptime ("2001-2-3 10:11:12", "%Y-%m-%d %H:%M:%S")
local_dt = local.localize(naive, is_dst=None)
utc_dt = local_dt.astimezone(pytz.utc)