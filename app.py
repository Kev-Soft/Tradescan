import talib
from math import pi
import numpy as np
import pandas as pd
from pybit import HTTP, WebSocket



session = HTTP("https://api-testnet.bybit.com")
data = session.query_kline(
    symbol="BTCUSDT",
    interval=1,
    limit=2,
    from_time=1581231260
)

#data = yf.download("BTC-USD", start="2020-01-01", end="2021-05-01")

#morning_star = talib.CDLMORNINGSTAR(data['Open'], data['High'], data['Low'], data['Close'])
#engulfing = talib.CDLENGULFING(data['Open'], data['High'], data['Low'], data['Close'])
#upper, middle, lower = talib.BBANDS(data['Close'], 20, 2, 2)

##data['BB-Up'] = upper
#data['BB-Low'] = lower
#data['Morning Star'] = morning_star
#data['Engulfing'] = engulfing
#data['Date'] = data.index

#morning_stars = data[data['Morning Star'] != 0]

#putting data into Pandas Dataframe
df = pd.json_normalize(data)[:50]

print(df)

