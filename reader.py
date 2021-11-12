from pybit import WebSocket, HTTP
import time
import pandas as pd
import talib
from datetime import datetime

def insertBB(data):
            #getting some indicator/strats val
            upperbb, middlebb, lowerbb = talib.BBANDS(data['c'], 5, 2, 2)
            df['bb_upper'] = upperbb
            df['bb_lower'] = lowerbb  

def buySignal(df):
    df['l'] = df['l'].astype(float)
    df['h'] = df['h'].astype(float)
    df['c'] = df['c'].astype(float)
    df['bb_lower'] = df['bb_lower'].astype(float)
    if df.iloc[-3]['l'] < df.iloc[-3]['bb_lower'] and df.iloc[-2]['c'] > df.iloc[-2]['bb_lower']:
        
        print("buy @: "+ str(df.iloc[-1]['t'])) 
        print("l:"+str(df.iloc[-3]['l'])+" bb_l:"+str(df.iloc[-3]['bb_lower']))
        print("c:"+str(df.iloc[-2]['c'])+" bb_l:"+str(df.iloc[-2]['bb_lower']))

    else:
        print("no signal @: "+ str(df.iloc[-1]['t']))
        print("l:"+str(df.iloc[-3]['l'])+" bb_l:"+str(df.iloc[-3]['bb_lower']))
        print("c:"+str(df.iloc[-2]['c'])+" bb_l:"+str(df.iloc[-2]['bb_lower']))       

#getting hist. data up to now
session = HTTP("https://api-testnet.bybit.com",
               spot=True)
df = pd.DataFrame(session.query_kline(
    symbol="BTCUSDT",
    interval="1m",
    limit="200"  
)["result"], columns=['t','o','h','l','c','v','1','2','3','4','5'])

#after creation of pd, deleting non relevant rows
df = df.drop(columns=['1', '2', '3', '4', '5'])



#subscription settings for websocket
subs = [
    """{
        "topic": "kline",
        "event": "sub",
        "params": {
            "symbol": "BTCUSDT",
            "binary": false,
            "klineType": "1m"
        }
    }"""
]
ws = WebSocket(
    "wss://stream.bybit.com/spot/quote/ws/v2",
    subscriptions=subs
)
while True:
    data = ws.fetch(subs[0])
    if data:
        
        #compare with last timestamp 
        #if incoming data has a new timestamp-> new df
        if data["t"] > df['t'].iloc[-1]:
            
            
            #putting new websocket data into pd
            newData = pd.DataFrame([data])
        
            df = df.append({'t':data['t'], 
                            'o':data['o'], 
                            'h':data['h'], 
                            'l':data['l'], 
                            'c':data['c'], 
                            'v':data['v']}, 
                            ignore_index=True)
            
            insertBB(df)    
            buySignal(df)              
            #print(df[-10:])
            time.sleep(1)


        #if incoming data has the same timestamp->upd df
        else:
            df.iloc[-1] = {'t':data['t'], 
                            'o':data['o'], 
                            'h':data['h'], 
                            'l':data['l'], 
                            'c':data['c'], 
                            'v':data['v']}

            insertBB(df)
                                        
            #print(df[-10:])
            time.sleep(10)

       
       