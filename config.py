# ============================================
# BOT QUANT INSTITUCIONAL - VERSIÓN FINAL
# ============================================

SIMULATION_MODE = True
DATA_SOURCE = "coingecko"   # coingecko, binance, okx, bybit (solo coingecko funciona 100%)

# API Key de CoinGecko (gratuita, regístrate en coingecko.com)
COINGECKO_API_KEY = "CG-kLdtAHJWmg3w684oGEbZgQHJ"  # <--- REEMPLAZA CON TU CLAVE

CAPITAL_INICIAL = 1000
MAX_POSICIONES = 4
MAX_CAPITAL_USO = 0.60

TIMEFRAME = "5m"           # 5m, 15m, 1h, 4h, 1d
CYCLE_SECONDS = 30         # Escaneo cada 30 segundos
HISTORY_LIMIT = 200        # Velas para análisis

# Universo de activos (IDs de CoinGecko)
UNIVERSE = [
    "bitcoin", "ethereum", "solana", "cardano", "dogecoin",
    "chainlink", "polkadot", "aave", "uniswap", "polygon"
]
# Símbolos para mostrar (opcional)
SYMBOL_MAP = {
    "bitcoin": "BTC/USDT",
    "ethereum": "ETH/USDT",
    "solana": "SOL/USDT",
    "cardano": "ADA/USDT",
    "dogecoin": "DOGE/USDT",
    "chainlink": "LINK/USDT",
    "polkadot": "DOT/USDT",
    "aave": "AAVE/USDT",
    "uniswap": "UNI/USDT",
    "polygon": "MATIC/USDT"
}

# ========== DETECCIÓN DE MERCADO ==========
ADX_PERIOD = 14
TREND_STRENGTH_THRESHOLD = 25

# ========== ML ==========
ML_RETRAIN_EVERY_TRADES = 30
ML_MIN_TRADES_FOR_TRAIN = 30
ML_FEATURES = ['rsi', 'macd', 'bb_width', 'volume_ratio', 'trend_strength', 'volatility']

# ========== RIESGO DINÁMICO ==========
DEFAULT_ATR_PERIOD = 14
DEFAULT_STOP_MULTIPLIER = 1.5
DEFAULT_TAKE_MULTIPLIER = 2.5
MAX_STOP_PERCENT = 0.05
MIN_STOP_PERCENT = 0.01

# ========== GESTIÓN DE CAPITAL ==========
KELLY_FRACTION = 0.25
MAX_POSITION_SIZE_PCT = 0.15
MIN_POSITION_SIZE_PCT = 0.03

# ========== COOLDOWN ==========
COOLDOWN_BASE = 20
COOLDOWN_MAX = 60
COOLDOWN_MIN = 10

# ========== FILTROS ANTIBASURA ==========
MIN_VOLUME_USD = 10_000_000
MIN_PRICE_CHANGE_PCT = 0.5
MAX_VOLATILITY = 0.15

# ========== CORRELACIÓN ==========
CORRELATION_GROUPS = {
    "L1": ["bitcoin", "ethereum"],
    "L2": ["solana"],
    "L3": ["cardano", "polygon"],
    "MEME": ["dogecoin"],
    "L4": ["chainlink", "polkadot"],
    "L5": ["aave", "uniswap"],
}

# ========== UMBRALES DE SEÑAL ==========
SIGNAL_MIN_PROBABILITY = 0.65
SIGNAL_MIN_SCORE = 0.70

# ========== ARCHIVOS ==========
MODEL_PATH = "xgboost_model.pkl"
SCALER_PATH = "scaler.pkl"
TRADES_LOG = "trades.csv"
PORTFOLIO_STATE = "portfolio_state.json"