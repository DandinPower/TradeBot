'''
此版本為回測工具
'''
import os
import matplotlib.pyplot as plt
from binance.client import Client
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')
client = Client(api_key, api_secret)  # 用自己創立的Key,Secret登入binance帳戶
Coin = "ETH"    # 設定貨幣為"..."
Money = "USDT"  # 設定法幣為為"...""
Coin_Money = Coin + Money
Interval = Client.KLINE_INTERVAL_3MINUTE
Time_Interval = "1 day ago UTC"
wallet = {Coin: 0, Money: 20}  # 設定錢包


def buy(price, wallet):  # 此Function為模擬購買
    if(wallet[Money] != 0):  # 當錢包有法幣時才能購買
        wallet[Money] = wallet[Money] * 0.9995  # 將法幣扣除手續費
        TempCoin = wallet[Money]/price  # TempCoin為買到的貨幣量
        wallet[Money] = 0  # 清空錢包的法幣
        wallet[Coin] = wallet[Coin] + TempCoin  # 將買到的TempCoin儲存起來
    return wallet


def sell(price, wallet):  # 此Function為模擬賣出
    if(wallet[Coin] != 0):  # 當錢包有貨幣時才能賣出
        wallet[Coin] = wallet[Coin] * 0.9995  # 將貨幣扣除手續費
        TempMoney = wallet[Coin] * price  # 得到賣出的法幣量
        wallet[Coin] = 0  # 清空貨幣
        wallet[Money] = wallet[Money] + TempMoney  # 儲存法幣
    return wallet


def abs(number):  # 取絕對值function
    if number < 0:
        return -number
    else:
        return number


'''
這部分為將K線存進各個陣列
'''
OpenList = []
CloseList = []
HighList = []
LowList = []
Time = []
Num = 0

# 讀取K線
for kline in client.get_historical_klines(Coin_Money, Interval,  Time_Interval):
    Open = float(kline[1])
    OpenList.append(Open)
    High = float(kline[2])
    HighList.append(High)
    Low = float(kline[3])
    LowList.append(Low)
    Close = float(kline[4])
    CloseList.append(Close)
    Time.append(Num)
    Num += 1
'''
計算rsi,將計算結果存進RsiList
'''
rsi_k = 6
RsiList = []
for j in range(Num):
    if (j >= rsi_k):
        TempUp = 0
        TempDown = 0
        for i in range(rsi_k):
            TempValue = CloseList[j-i] - OpenList[j-i]
            if TempValue >= 0:
                TempUp += TempValue
            else:
                TempDown += TempValue
        TempUp = TempUp/rsi_k
        TempDown = abs(TempDown/rsi_k)
        TempRsi = TempUp/(TempDown+TempUp)
        RsiList.append(TempRsi)
    else:
        RsiList.append(0)
'''
計算Rvi,將結果存進RviList跟SignalList
'''
RviList = []
SignalList = []
for j in range(Num):
    if(j >= 3):
        Open = OpenList[j]
        Open_1 = OpenList[j-1]
        Open_2 = OpenList[j-2]
        Open_3 = OpenList[j-3]
        Close = CloseList[j]
        Close_1 = CloseList[j-1]
        Close_2 = CloseList[j-2]
        Close_3 = CloseList[j-3]
        High = HighList[j]
        High_1 = HighList[j-1]
        High_2 = HighList[j-2]
        High_3 = HighList[j-3]
        Low = LowList[j]
        Low_1 = LowList[j-1]
        Low_2 = LowList[j-2]
        Low_3 = LowList[j-3]
        TempMov = ((Close - Open) + (2 * (Close_1-Open_1)) +
                   (2 * (Close_2-Open_2)) + (Close_3 - Open_3))/6
        TempRange = ((High - Low) + (2 * (High_1-Low_1)) +
                     (2 * (High_2-Low_2)) + (High_3 - Low_3))/6
        TempRVI = TempMov/TempRange
        RviList.append(TempRVI)
    else:
        RviList.append(0)
for j in range(Num):
    if(j >= 3):
        Rvi = RviList[j]
        Rvi_1 = RviList[j-1]
        Rvi_2 = RviList[j-2]
        Rvi_3 = RviList[j-3]
        TempSignal = (Rvi + (2 * Rvi_1) + (2 * Rvi_2) + Rvi_3)/6
        SignalList.append(TempSignal)
    else:
        SignalList.append(0)

'''
模擬購買
'''
BuyTimeList = []
BuyList = []
SellTimeList = []
SellList = []
buystate = True
sellstate = False
for j in range(1, Num):

    rvi = RviList[j]
    rvi_1 = RviList[j-1]

    signal = SignalList[j]
    signal_1 = SignalList[j-1]
    price = OpenList[j]
    rsi = RsiList[j]
    if(rsi > 0.5):
        if(rvi_1 < -0.15):
            if(rvi > signal and buystate):
                if(signal_1 > rvi_1):
                    wallet = buy(CloseList[j], wallet)
                    buystate = False
                    sellstate = True
                    BuyTimeList.append(j)
                    BuyList.append(price)
                    print(wallet)
        if(signal_1 > 0.15):
            if(rvi < signal and sellstate):
                if(signal_1 > rvi_1):
                    wallet = sell(CloseList[j], wallet)
                    buystate = True
                    sellstate = False
                    SellTimeList.append(j)
                    SellList.append(price)
                    print(wallet)
for j in range(Num):
    for x in range(len(BuyTimeList)):
        if BuyTimeList[x] == j:
            print("buy", j, BuyList[x], RsiList[j])
    for x in range(len(SellTimeList)):
        if SellTimeList[x] == j:
            print("sell", j, SellList[x], RsiList[j])

if(sellstate):
    print(wallet[Coin]*OpenList[-1])


'''
印出圖表
'''

plt.figure(figsize=(15, 10), dpi=100, linewidth=2)
plt.plot(Time, SignalList, 's-', color='r')
plt.plot(Time, RviList, 'o-', color='g')


plt.figure(figsize=(15, 10), dpi=100, linewidth=2)
plt.plot(Time, OpenList, 's-', color='b')
plt.plot(BuyTimeList, BuyList, '^', color='g')
plt.plot(SellTimeList, SellList, '^', color='r')
plt.show()
