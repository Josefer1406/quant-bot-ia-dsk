from features import add_technical_features
from regime_detector import detect_market_regime, get_regime_multiplier
from ml_model import ml_model
import config

def generate_signal(symbol, df):
    if df is None or len(df) < 100:
        return None, 0.0, 0.0
    df_feat = add_technical_features(df)
    if df_feat is None or df_feat.empty:
        return None, 0.0, 0.0
    last = df_feat.iloc[-1]
    trend_bull = last.get('ema_21', 0) > last.get('ema_50', 0) > last.get('ema_200', 0)
    price_above_ema = last.get('close', 0) > last.get('ema_21', 0)
    momentum_positive = last.get('returns_5', 0) > 0
    tech_score = (trend_bull * 0.4) + (price_above_ema * 0.3) + (momentum_positive * 0.3)
    ml_prob = ml_model.predict_probability(df)
    if ml_prob is None:
        ml_prob = 0.5
    combined_prob = 0.6 * ml_prob + 0.4 * tech_score
    regime = detect_market_regime(df)
    regime_factor = get_regime_multiplier(regime)
    adjusted_prob = combined_prob * regime_factor
    adjusted_prob = min(0.95, max(0.05, adjusted_prob))
    final_score = (adjusted_prob * 0.7) + (tech_score * 0.3)
    if adjusted_prob < config.SIGNAL_MIN_PROBABILITY or final_score < config.SIGNAL_MIN_SCORE:
        return None, adjusted_prob, final_score
    return 'buy', adjusted_prob, final_score