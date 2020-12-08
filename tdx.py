# frequency -> K线种类
# > 0 5分钟K线 1 15分钟K线 2 30分钟K线 3 1小时K线 4 日K线 5 周K线 6 月K线
# > 7 1分钟K线 8 1分钟K线 9 日K线 10 季K线 11 年K线
# https://mootdx.readthedocs.io/zh/latest/api/quote1/
#mootdx bestip -v -w
from mootdx.quotes import Quotes
client = Quotes.factory(market='std')
client.quotes(symbol=["002075", "600300"])
client.bars(symbol='002075', frequency=3, offset=10)
from mootdx.quotes import Quotes
from mootdx.consts import KLINE_DAILY
client.bars(frequency=KLINE_DAILY, market=47, symbol="47#IF1709", start=0, offset=100)
# 简写方式
client.bars(frequency=KLINE_DAILY, symbol="47#IF1709", start=0, offset=100)