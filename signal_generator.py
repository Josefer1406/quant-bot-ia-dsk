import pandas as pd
import numpy as np
from features import add_technical_features
from regime_detector import detect_market_regime, get_regime_multiplier
from ml_model import ml_model
import config

def generate_signal(symbol, df):
    if df is None or len(df) < 50:
        return None, 0.0, 0.0
    
    df_feat = add_technical_features(df)
    if df_feat is None or df_feat.empty:
        return None, 0.0, 0.0
    
    last = df_feat.iloc[-1]
    # Score técnico (0-1)
    tech_score = 0.0
    if last.get('sma_21', 0) > last.get('sma_50', 0):
        tech_score += 0.4
    if last.get('close', 0) > last.get('sma_21', 0):
        tech_score += 0.3
    if last.get('returns_5', 0) > 0:
        tech_score += 0.3
    
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
    
    print(f"📊 {symbol}: tech={tech_score:.2f} ml={ml_prob:.2f} prob={prob:.2f} score={score:.2f}")
    
    if prob >= config.SIGNAL_MIN_PROBABILITY and score >= config.SIGNAL_MIN_SCORE:
        print(f"✅ {symbol}: SEÑAL COMPRA!")
        return 'buy', prob, score
    return None, prob, score