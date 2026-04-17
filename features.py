import pandas as pd
import numpy as np
import config

def add_technical_features(df):
    """Añade indicadores técnicos manuales (SMA, RSI, ATR, retornos, volumen)"""
    if df is None or len(df) < 30:
        return df
    df = df.copy()
    try:
        # Medias móviles simples (SMA)
        for period in [7, 14, 21, 50, 100, 200]:
            if len(df) >= period:
                df[f'sma_{period}'] = df['close'].rolling(window=period).mean()
        
        # RSI (14 periodos)
        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # ATR
        high_low = df['high'] - df['low']
        high_close = abs(df['high'] - df['close'].shift())
        low_close = abs(df['low'] - df['close'].shift())
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        df['atr'] = tr.rolling(window=config.DEFAULT_ATR_PERIOD).mean()
        
        # Retornos
        df['returns_1'] = df['close'].pct_change()
        df['returns_5'] = df['close'].pct_change(5)
        df['returns_10'] = df['close'].pct_change(10)
        
        # Volumen
        df['volume_sma'] = df['volume'].rolling(window=20).mean()
        df['volume_ratio'] = df['volume'] / (df['volume_sma'] + 1e-9)
        
        # Volatilidad (desviación de retornos)
        df['volatility'] = df['returns_1'].rolling(20).std()
        
        # Precio relativo a SMA21
        if 'sma_21' in df.columns:
            df['price_vs_sma21'] = (df['close'] - df['sma_21']) / df['sma_21']
        
        # Eliminar filas con NaN
        df = df.dropna()
        return df
    except Exception as e:
        print(f"Error en add_technical_features: {e}")
        return df

def get_feature_columns():
    """Devuelve lista de columnas de features usando un DataFrame sintético de 300 filas"""
    n = 300
    np.random.seed(42)
    close = 100 + np.cumsum(np.random.randn(n) * 0.5)
    high = close + np.abs(np.random.randn(n) * 0.3)
    low = close - np.abs(np.random.randn(n) * 0.3)
    volume = 1000 + np.random.randint(0, 500, n)
    
    sample = pd.DataFrame({
        'open': close + np.random.randn(n) * 0.2,
        'high': high,
        'low': low,
        'close': close,
        'volume': volume
    })
    sample_with_features = add_technical_features(sample)
    if sample_with_features is None or sample_with_features.empty:
        return ['sma_21', 'sma_50', 'rsi', 'atr', 'returns_1', 'returns_5', 'volume_ratio', 'volatility']
    exclude = ['open', 'high', 'low', 'close', 'volume']
    cols = [c for c in sample_with_features.columns if c not in exclude]
    return cols if cols else ['sma_21', 'sma_50', 'rsi', 'atr', 'returns_1', 'returns_5', 'volume_ratio', 'volatility']