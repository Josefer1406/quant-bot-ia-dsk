# ============================================
# BOT QUANT INSTITUCIONAL - VERSIÓN COINGECKO OPTIMIZADA
# ============================================

SIMULATION_MODE = True
DATA_SOURCE = "coingecko"

COINGECKO_API_KEY = "CG-kLdtAHJWmg3w684oGEbZgQHJ"  # <--- REEMPLAZA CON TU CLAVE

CAPITAL_INICIAL = 1000
MAX_POSICIONES = 3          # Reducido a 3 para menos operaciones
MAX_CAPITAL_USO = 0.60

TIMEFRAME = "5m"
CYCLE_SECONDS = 60          # Aumentado a 60 segundos para respetar rate limit
HISTORY_LIMIT = 100         # Solo 100 velas (suficiente para indicadores)

# Reducimos el universo a 5 activos (menos peticiones)
UNIVERSE = [
    "bitcoin", "ethereum", "solana", "cardano", "dogecoin"
]
SYMBOL_MAP = {
    "bitcoin": "BTC/USDT",
    "ethereum": "ETH/USDT",
    "solana": "SOL/USDT",
    "cardano": "ADA/USDT",
    "dogecoin": "DOGE/USDT"
}

# Resto de configuraciones igual...
ADX_PERIOD = 14
TREND_STRENGTH_THRESHOLD = 25

ML_RETRAIN_EVERY_TRADES = 30
ML_MIN_TRADES_FOR_TRAIN = 30
ML_FEATURES = ['rsi', 'macd', 'bb_width', 'volume_ratio', 'trend_strength', 'volatility']

DEFAULT_ATR_PERIOD = 14
DEFAULT_STOP_MULTIPLIER = 1.5
DEFAULT_TAKE_MULTIPLIER = 2.5
MAX_STOP_PERCENT = 0.05
MIN_STOP_PERCENT = 0.01

KELLY_FRACTION = 0.25
MAX_POSITION_SIZE_PCT = 0.15
MIN_POSITION_SIZE_PCT = 0.03

COOLDOWN_BASE = 20
COOLDOWN_MAX = 60
COOLDOWN_MIN = 10

MIN_VOLUME_USD = 10_000_000
MIN_PRICE_CHANGE_PCT = 0.5
MAX_VOLATILITY = 0.15

CORRELATION_GROUPS = {
    "L1": ["bitcoin", "ethereum"],
    "L2": ["solana"],
    "L3": ["cardano"],
    "MEME": ["dogecoin"],
}

SIGNAL_MIN_PROBABILITY = 0.65
SIGNAL_MIN_SCORE = 0.70

MODEL_PATH = "xgboost_model.pkl"
SCALER_PATH = "scaler.pkl"
TRADES_LOG = "trades.csv"
PORTFOLIO_STATE = "portfolio_state.json"