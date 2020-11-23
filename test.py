import pandas as pd
import ta
import os

os.chdir(r"D:\Python_projects\trade_projects\tt")
print (os.getcwd())
df = pd.read_csv("df.csv")
df["macd"]=ta.trend.MACD(df.close,55,144,55).macd()
df["macd_signal"]=ta.trend.MACD(df.close,55,144,55).macd_signal()
# df.dropna(axis=0, how='any', inplace=True)


df = ta.add_all_ta_features(df, "open", "high", "low", "close",'volume',fillna=False)
print (df)