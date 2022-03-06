# 自動交易機器人

## 專案說明

### 專案動機

由於加密貨幣的性質，很適合進行短線交易，但不想每天花這麼多時間進行盯盤操作，因此就產生了做這個專案的想法，使用著名交易所binance製作的python api，搭配使先制定好的策略即可進行全自動交易

### 專案架設

本專案分為兩個面向，一個面向是實際串接第三方api的過程，透過連接交易所的帳號錢包來進行幣價的查詢或者是基本的買賣單，另一個面向是透過python來進行各式各樣的策略回測，以嘗試在大數據的情況下是否能找到較好的下注策略

### 環境安裝

```bash
pip install matplotlib
pip install python-dotenv
pip install python-binance
pip install numpy
pip install pandas 
pip install plotly
```

### API設置

- 在目錄新增.env 並輸入幣安的相關api設定
    
    ```
    API_KEY = 
    API_SECRET = 
    ```
    

### 下單相關

- 運行模擬下單功能
    
    ```bash
    python account.py
    ```
    
- 運行真實下單功能
    
    ```bash
    python version_1.py
    ```
    

### 策略相關

- 顯示翻亞當
    
    ```bash
    python Strategy/adam.py
    ```
    
- 均線策略
    
    ```bash
    python Stategy/ema.py
    ```
    
- 九轉序列策略
    
    ```bash
    python Stategy/nineturn.py
    ```
    
- Rvi策略
    
    ```bash
    python Stategy/rvi.py
    ```
