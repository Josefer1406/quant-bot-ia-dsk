import pandas as pd
import numpy as np
from features import add_technical_features
from regime_detector import detect_market_regime, get_regime_multiplier
from ml_model import ml_model
import config

def generate_signal(symbol, df):
    if df is None or len(df) < 100:
        return None, 0.0, 0.0
    
    df_feat = add_technical_features(df)
    if df_feat is None or df_feat.empty or len(df_feat) < 2:
        print(f"   ⚠️ {symbol}: features vacías")
        return None, 0.0, 0.0
    
    last = df_feat.iloc[-1]
    # Valores seguros
    sma21 = last.get('sma_21', 0)
    sma50 = last.get('sma_50', 0)
    sma200 = last.get('sma_200', 0)
    close = last.get('close', 0)
    returns5 = last.get('returns_5', 0)
    
    # Score técnico
    trend_bull = (sma21 > sma50 > sma200) if sma50 != 0 and sma200 != 0 else False
    price_above_sma = close > sma21 if sma21 != 0 else False
    momentum = returns5 > 0 if not pd.isna(returns5) else False
    tech_score = (trend_bull * 0.4) + (price_above_sma * 0.3) + (momentum * 0.3)
    
    # ML
    ml_prob = ml_model.predict_probability(df)
    if ml_prob is None:
        ml_prob = 0.5
    
    combined = 0.6 * ml_prob + 0.4 * tech_score
    regime = detect_market_regime(df)
    regime_factor = get_regime_multiplier(regime)
    prob = combined * regime_factor
    prob = min(0.95, max(0.05, prob))
    score = (prob * 0.7) + (tech_score * 0.3)
    
    print(f"   📊 {symbol}: tech={tech_score:.2f} ml={ml_prob:.2f} prob={prob:.2f} score={score:.2f}")
    
    if prob < config.SIGNAL_MIN_PROBABILITY or score < config.SIGNAL_MIN_SCORE:
        return None, prob, score
    print(f"   ✅ {symbol}: SEÑAL COMPRA!")
    return 'buy', prob, score