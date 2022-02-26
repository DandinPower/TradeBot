from price import GetPrice,WinOrLose,Lose,GetEma
import numpy as np
import plotly.graph_objects as go
def ShowKlines(klines,ema4,ema12,ema50,Points):
    plttime = 0
    if(plttime == 0):
        Data = [go.Candlestick(x=klines[7], open=klines[0], high=klines[2], low=klines[3],
                            close=klines[1], increasing_line_color='green', decreasing_line_color='red'),
                go.Scatter(
            x=klines[7],
            y=ema4,
            name='EMA_4',
            mode='lines',
            line=go.Line(
                color='#FFFF00'
            )
        ),
                go.Scatter(
            x=klines[7],
            y=ema12,
            name='EMA_12',
            mode='lines',
            line=go.Line(
                color='#FF00FF'
            )
        ),
                go.Scatter(
            x=klines[7],
            y=ema50,
            name='EMA_50',
            mode='lines',
            line=go.Line(
                color='#000000'
            )
        ),go.Scatter(
        x=Points[1],
        y=Points[0],
        name='LittleBuy',
        mode='markers',
        marker=go.Marker(color='#00FF00')
    ),go.Scatter(
        x=Points[3],
        y=Points[2],
        name='BigBuy',
        mode='markers',
        marker=go.Marker(color='#00FF00')
    ),go.Scatter(
        x=Points[5],
        y=Points[4],
        name='LittleSell',
        mode='markers',
        marker=go.Marker(color='#FF0000')
    ),go.Scatter(
        x=Points[7],
        y=Points[6],
        name='BigSell',
        mode='markers',
        marker=go.Marker(color='#FF0000')
    )]
        fig = go.Figure(Data)

        fig.show()
        plttime = 1

def CheckIsBigThrough(a,b,c,d):
    return c >= a and b > d

def CheckIsSmallThrough(a,b,c,d):
    return a >= c and b < d

def FindBuyPoint(klines,ema4,ema12,ema50):
    Time = klines[7]
    Close = klines[1]
    LittleBuy = []
    LittleBuyTime = []
    BigBuy = []
    BigBuyTime = []
    LittleSell = []
    LittleSellTime = []
    BigSell = []
    BigSellTime = []
    for i in range(len(klines[0])):
        if i < 50:
            continue
        else:
            ema4Last = ema4[i-1]
            ema4now = ema4[i]
            ema12Last = ema12[i-1]
            ema12now = ema12[i]
            ema50Last = ema50[i-1]
            ema50now = ema50[i]
            if CheckIsBigThrough(ema4Last,ema4now, ema12Last, ema12now):
                LittleBuy.append(Close[i])
                LittleBuyTime.append(Time[i])
            if CheckIsBigThrough(ema4Last,ema4now, ema50Last, ema50now):
                BigBuy.append(Close[i])
                BigBuyTime.append(Time[i])
            if CheckIsSmallThrough(ema4Last,ema4now, ema12Last, ema12now):
                LittleSell.append(Close[i])
                LittleSellTime.append(Time[i])
            if CheckIsSmallThrough(ema4Last,ema4now, ema50Last, ema50now):
                BigSell.append(Close[i])
                BigSellTime.append(Time[i])
    Points = [LittleBuy,LittleBuyTime,BigBuy,BigBuyTime,LittleSell,LittleSellTime,BigSell,BigSellTime]
    ShowKlines(klines, ema4, ema12, ema50,Points)

def main():
    Coin_Money = "BTCUSDT"
    Interval = "1d"
    Time_Interval = "12 month ago UTC"
    REVERSELEN = 25
    klines = GetPrice(Coin_Money, Interval, Time_Interval)
    ema50 = GetEma(klines[1], 50)
    ema12 = GetEma(klines[1], 12)
    ema4 = GetEma(klines[1], 4)
    original = len(klines[0])
    FindBuyPoint(klines, ema4, ema12, ema50)
    
    

if __name__ == "__main__":
    main()