from price import GetPrice,WinOrLose,Lose
import numpy as np
import plotly.graph_objects as go

def ShowKlines(klines,centerparm):
    plttime = 0
    if(plttime == 0):
        Data = [go.Candlestick(x=klines[0], open=klines[1], high=klines[3], low=klines[4],
                            close=klines[2], increasing_line_color='green', decreasing_line_color='red'),go.Scatter(
        x=centerparm[0],
        y=centerparm[1],
        name='CenterPoint',
        mode='markers',
        marker=go.Marker(color='#00FFFF')
    )]
        fig = go.Figure(Data)

        fig.show()
        plttime = 1

def Adam(klines,REVERSELEN,timepoint):
    Open = klines[0][0:timepoint]
    Close = klines[1][0:timepoint]
    High = klines[2][0:timepoint]
    Low = klines[3][0:timepoint]
    Volume = klines[4][0:timepoint]
    Trade = klines[5][0:timepoint]
    Av = klines[6][0:timepoint]
    Time = klines[7][0:timepoint]
    Num = len(Open)
    time_copy = Num-1
    center = Close[-1]
    centerparm = [[time_copy],[center]]
    for i in range(Num-1,Num-REVERSELEN-1,-1):
        tempOpen = 2*center - Close[i]
        tempClose = 2*center - Open[i]
        tempHigh = 2*center - Low[i]
        tempLow = 2*center - High[i]
        time_copy += 1
        Open.append(tempOpen)
        Close.append(tempClose)
        High.append(tempHigh)
        Low.append(tempLow)
        Time.append(time_copy)
    Klines = [Time,Open,Close,High,Low]
    ShowKlines(Klines,centerparm)

def main():
    Coin_Money = "BTCUSDT"
    Interval = "4h"
    Time_Interval = "1 month ago UTC"
    REVERSELEN = 25
    klines = GetPrice(Coin_Money, Interval, Time_Interval)
    original = len(klines[0])
    Adam(klines,REVERSELEN,173)

if __name__ == "__main__":
    main()

#60 close進場 50%
#63 close進場 50%
#80 close出場
#97 close出場



