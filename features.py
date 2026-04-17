import pandas as pd
import numpy as np
import config

def add_technical_features(df):
    """Versión simple que nunca falla"""
    if df is None or len(df) < 30:
        return df
    df = df.copy()
    # SMA 21 y 50 (solo dos, suficientes)
    df['sma_21'] = df['close'].rolling(21).mean()
    df['sma_50'] = df['close'].rolling(50).mean()
    # RSI
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    df['rsi'] = 100 - (100 / (1 + gain / loss))
    # ATR
    tr = pd.concat([df['high'] - df['low'],
                    abs(df['high'] - df['close'].shift()),
                    abs(df['low'] - df['close'].shift())], axis=1).max(axis=1)
    df['atr'] = tr.rolling(14).mean()
    # Retornos
    df['returns_1'] = df['close'].pct_change()
    df['returns_5'] = df['close'].pct_change(5)
    # Volumen
    df['volume_sma'] = df['volume'].rolling(20).mean()
    df['volume_ratio'] = df['volume'] / (df['volume_sma'] + 1e-9)
    # Volatilidad
    df['volatility'] = df['returns_1'].rolling(20).std()
    # Limpiar NaN
    df = df.dropna()
    return df

def get_feature_columns():
    # Devolvemos una lista fija (para que ML funcione)
    return ['sma_21', 'sma_50', 'rsi', 'atr', 'returns_1', 'returns_5', 'volume_ratio', 'volatility']