'''
此版本為真實下單
'''
import os
from binance.client import Client
import time
from decimal import Decimal
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')
client = Client(api_key, api_secret)


def Float(money):
    money = str(money)
    money = Decimal(money).quantize(Decimal('0.00000'))
    return float(money)


def abs(number):
    if number < 0:
        return -number
    else:
        return number


def main():
    while(True):
        time.sleep(1)
        OpenList = []
        CloseList = []
        HighList = []
        LowList = []
        Time = []
        Num = 0
        for kline in client.get_historical_klines("ETHUSDT", Client.KLINE_INTERVAL_3MINUTE,  "30 minutes ago UTC"):
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
        計算rsi
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
        計算Rvi
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
        j = Num - 1
        rvi = RviList[j]
        rvi_1 = RviList[j-1]
        signal = SignalList[j]
        signal_1 = SignalList[j-1]
        rsi = RsiList[j]
        info = client.get_account()
        balances = info["balances"]
        ETH = float(balances[2]['free'])
        USDT = float(balances[11]['free'])
        DealPrice = 0
        prices = client.get_all_tickers()
        for index in prices:
            if(index["symbol"] == "ETHUSDT"):
                price = index["price"]
        print("ETH: ", ETH, "USDT: ", USDT)
        print("Rsi: ", rsi)
        print("Rvi: ", rvi)
        print("Signal: ", signal)
        print("Price: ", price)
        print("DealPrice: ", DealPrice)

        if(rsi > 0.5):
            if(rvi_1 < -0.15):
                if(rvi > signal and USDT > 0.000000000001):
                    if(signal_1 > rvi_1):
                        print("buy")
                        DealPrice = prices
                        Quan = Float(USDT/price*0.9995)
                        order = client.order_market_buy(
                            symbol='ETHUSDT', quantity=Quan)
            if(signal_1 > 0.15):
                if(rvi < signal and ETH > 0.000000000001):
                    if(signal_1 > rvi_1):
                        print("sell")
                        DealPrice = prices
                        Quan = Float(ETH * 0.9995)
                        order = client.order_market_sell(
                            symbol='ETHUSDT', quantity=Quan)


main()
