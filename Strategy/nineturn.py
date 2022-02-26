import sys
import price 
import numpy as np
import plotly.graph_objects as go
Coin_Money = "BTCUSDT"
Interval = "15m"
Time_Interval = "4 week ago UTC"
klines = price.GetPrice(Coin_Money, Interval, Time_Interval)
Open = klines[0]
Close = klines[1]
High = klines[2]
Low = klines[3]
Volume = klines[4]
Trade = klines[5]
Av = klines[6]
Time = klines[7]
parm_1 = 2
parm_2 = 5
upsignal = 0
downsignal = 0
Buy = []
BuyTime = []
Sell = []
SellTime = []
buytime = 0
wintime = 0
selltime = 0
wintime2 = 0
for i in range(len(Open)):
    if i < parm_1:
        continue
    else:
        if Close[i] > Close[i-parm_1]:
            upsignal += 1
            downsignal = 0
        elif Close[i] < Close[i-parm_1]:
            downsignal += 1
            upsignal = 0
        if upsignal == parm_2:
            Buy.append(Close[i])
            BuyTime.append(Time[i])
            upsignal = 0
            buytime += 1
            #if Lose(Close, High, Low, i) == 0:
            #    wintime += 1
            if price.WinOrLose(Close, High, Low, i) == 1:
                wintime += 1
        if downsignal == parm_2:
            Sell.append(Close[i])
            SellTime.append(Time[i])
            downsignal = 0
            selltime += 1
            #if WinOrLose(Close, High, Low, i) == 1:
            #    wintime2 += 1
            if price.Lose(Close, High, Low, i) == 0:
                wintime2 += 1
plttime = 0
if(plttime == 0):
    Data = [go.Candlestick(x=klines[7], open=klines[0], high=klines[2], low=klines[3],
                        close=klines[1], increasing_line_color='red', decreasing_line_color='green'),go.Scatter(
        x=BuyTime,
        y=Buy,
        name='BuyPoint',
        mode='markers',
        marker=go.Marker(color='#00FFFF')
    ),go.Scatter(
        x=SellTime,
        y=Sell,
        name='SellPoint',
        mode='markers',
        marker=go.Marker(color='#FF00FF')
    )]
    fig = go.Figure(Data)

    fig.show()
    plttime = 1
print(f'buy:{buytime},win:{wintime}')
print(f'sell:{selltime},win:{wintime2}')
print(f'winrate:{(wintime+wintime2) * 100 / (buytime+selltime)}')