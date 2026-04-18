import yfinance as yf
import pandas as pd
import time
from datetime import datetime, timedelta
import config

class YahooFinanceFetcher:
    def __init__(self):
        self.last_request_time = 0
        self.min_interval = 0.5  # 0.5 segundos entre peticiones
    
    def _rate_limit_wait(self):
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_request_time = time.time()
    
    def fetch_ohlcv(self, symbol, period="7d", interval="5m"):
        """
        Obtiene velas de Yahoo Finance.
        symbol: 'BTC-USD', 'ETH-USD', etc.
        interval: '1m', '5m', '15m', '30m', '1h', '1d', etc.
        """
        self._rate_limit_wait()
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period, interval=interval)
            if df.empty:
                print(f"⚠️ Sin datos para {symbol}")
                return None
            # Reset index para tener timestamp como columna
            df = df.reset_index()
            df.rename(columns={
                'Datetime': 'timestamp',
                'Open': 'open',
                'High': 'high',
                'Low': 'low',
                'Close': 'close',
                'Volume': 'volume'
            }, inplace=True)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            # Tomar solo las últimas 'limit' velas
            if len(df) > config.HISTORY_LIMIT:
                df = df.tail(config.HISTORY_LIMIT)
            print(f"📥 {symbol}: {len(df)} velas ({interval})")
            return df
        except Exception as e:
            print(f"❌ Error {symbol}: {e}")
            return None
    
    def fetch_current_price(self, symbol):
        self._rate_limit_wait()
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d", interval="1m")
            if not data.empty:
                return float(data['Close'].iloc[-1])
            return 0
        except:
            return 0

fetcher = YahooFinanceFetcher()