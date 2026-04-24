import numpy as np
import config

def calculate_dynamic_stops(entry_price, atr, regime='lateral'):
    """
    Calcula stop loss y take profit dinámicos basados en ATR,
    con ajustes por régimen y límites mínimos.
    Ahora el TP siempre será al menos 2x el stop loss y >= MIN_TAKE_PERCENT.
    """
    # Ajuste de multiplicadores según régimen
    if regime == 'bull':
        sl_mult = config.DEFAULT_STOP_MULTIPLIER * 0.8
        tp_mult = config.DEFAULT_TAKE_MULTIPLIER * 1.2
    elif regime == 'bear':
        sl_mult = config.DEFAULT_STOP_MULTIPLIER * 1.2
        tp_mult = config.DEFAULT_TAKE_MULTIPLIER * 0.8
    else:  # lateral
        sl_mult = config.DEFAULT_STOP_MULTIPLIER
        tp_mult = config.DEFAULT_TAKE_MULTIPLIER

    # Cálculo base en porcentaje
    stop_pct = (atr * sl_mult) / entry_price
    take_pct = (atr * tp_mult) / entry_price

    # Aplicar límites al stop loss
    stop_pct = min(max(stop_pct, config.MIN_STOP_PERCENT), config.MAX_STOP_PERCENT)

    # Aplicar límites al take profit: mínimo configurable + al menos 2 veces el stop
    take_pct = max(take_pct, config.MIN_TAKE_PERCENT)  # mínimo 1.5%
    take_pct = max(take_pct, stop_pct * 2.0)           # al menos 2:1 riesgo/recompensa
    take_pct = min(take_pct, 0.10)                     # máximo 10% (techo)

    # Calcular precios
    stop_price = entry_price * (1 - stop_pct)
    take_price = entry_price * (1 + take_pct)

    return stop_price, take_price, stop_pct, take_pct

def position_size(capital, probability, historical_winrate=None, kelly_fraction=config.KELLY_FRACTION):
    """
    Calcula el tamaño de posición usando Kelly fraccional.
    """
    if historical_winrate is None:
        winrate = probability
        avg_win = 0.02
        avg_loss = 0.01
    else:
        winrate = historical_winrate
        avg_win = 0.02
        avg_loss = 0.01

    b = avg_win / avg_loss if avg_loss > 0 else 1
    kelly = (winrate * b - (1 - winrate)) / b
    kelly = max(0, min(kelly, 0.25))
    size_pct = kelly * kelly_fraction
    size_pct = max(min(size_pct, config.MAX_POSITION_SIZE_PCT), config.MIN_POSITION_SIZE_PCT)
    trade_capital = capital * size_pct
    return trade_capital, size_pct