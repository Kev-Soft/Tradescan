import talib
from math import pi
import yfinance as yf
from flask import Flask, render_template, jsonify
from bokeh.plotting import figure
from bokeh.embed import components
import numpy as np
import pandas as pd
app = Flask(__name__)


data = yf.download("BTC-USD", start="2021-01-01", end="2021-05-01")

morning_star = talib.CDLMORNINGSTAR(data['Open'], data['High'], data['Low'], data['Close'])
engulfing = talib.CDLENGULFING(data['Open'], data['High'], data['Low'], data['Close'])

data['Morning Star'] = morning_star
data['Engulfing'] = engulfing
data['Date'] = data.index

morning_stars = data[data['Morning Star'] != 0]

#putting data into Pandas Dataframe
df = pd.DataFrame(data)[:50]

print(df)

@app.route("/", methods=['GET', 'POST'])
def index():

    plot = figure(x_axis_type="datetime", width=1000, title = "BTC Candlestick")
    plot.xaxis.major_label_orientation = pi/4
    plot.grid.grid_line_alpha=0.7
    plot.line(df.Date,df.Close)

    inc = df.Close > df.Open
    dec = df.Open > df.Close
    w = 12*60*60*1000 # half day in ms???

    #Inject Candle-data
    plot.segment(df.Date, df.High, df.Date, df.Low, color="black")
    #Color of Candlesticks
    plot.vbar(df.Date[inc], w, df.Open[inc], df.Close[inc], fill_color="#D5E1DD", line_color="black")
    plot.vbar(df.Date[dec], w, df.Open[dec], df.Close[dec], fill_color="#F2583E", line_color="black")


    #Site/HTML Adjustments
    script, div = components(plot)
    kwargs = {'script': script, 'div': div}
    kwargs['title'] = 'Analyse'    
    return render_template('index.html', **kwargs)   


        
#starting flask webapp
if __name__ =='__main__':
    app.run(host="0.0.0.0", debug=True)
