import ccxt
import config

class ExchangeConnector:
    def __init__(self):
        if config.EXCHANGE_NAME == "bybit":
            self.exchange = ccxt.bybit({'enableRateLimit': True})
        else:
            self.exchange = ccxt.bybit({'enableRateLimit': True})
    
    def fetch_ohlcv(self, symbol, timeframe, limit):
        return self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)

exchange = ExchangeConnector()