import json
import time
import numpy as np
from collections import deque
import config

class Portfolio:
    def __init__(self):
        self.capital_initial = config.CAPITAL_INICIAL
        self.capital = config.CAPITAL_INICIAL
        self.positions = {}
        self.trades_history = []
        self.last_trade_time = 0
        self.cooldown = config.COOLDOWN_BASE
        self.load_state()
        self.winrate_history = deque(maxlen=50)
    
    def save_state(self):
        state = {
            'capital': self.capital,
            'positions': self.positions,
            'trades_history': self.trades_history[-200:],
            'last_trade_time': self.last_trade_time,
            'cooldown': self.cooldown
        }
        with open(config.PORTFOLIO_STATE, 'w') as f:
            json.dump(state, f, indent=2, default=str)
    
    def load_state(self):
        try:
            with open(config.PORTFOLIO_STATE, 'r') as f:
                state = json.load(f)
            self.capital = state.get('capital', self.capital_initial)
            self.positions = state.get('positions', {})
            self.trades_history = state.get('trades_history', [])
            self.last_trade_time = state.get('last_trade_time', 0)
            self.cooldown = state.get('cooldown', config.COOLDOWN_BASE)
            print(f"📀 Estado cargado: Capital ${self.capital:.2f}, {len(self.positions)} posiciones, {len(self.trades_history)} trades")
        except:
            pass
    
    def update_cooldown(self):
        if len(self.trades_history) < 10:
            self.cooldown = config.COOLDOWN_BASE
            return
        recent = self.trades_history[-10:]
        winrate = sum(1 for t in recent if t['pnl'] > 0) / len(recent)
        if winrate < 0.4:
            self.cooldown = min(config.COOLDOWN_MAX, self.cooldown + 5)
        elif winrate > 0.6:
            self.cooldown = max(config.COOLDOWN_MIN, self.cooldown - 2)
        else:
            self.cooldown = config.COOLDOWN_BASE
    
    def get_historical_winrate(self):
        if not self.trades_history:
            return None
        recent = self.trades_history[-50:]
        return sum(1 for t in recent if t['pnl'] > 0) / len(recent)
    
    def get_average_pnl_ratio(self):
        if not self.trades_history:
            return 0.02, 0.01
        wins = [t['pnl'] for t in self.trades_history if t['pnl'] > 0]
        losses = [t['pnl'] for t in self.trades_history if t['pnl'] <= 0]
        avg_win = np.mean(wins) if wins else 0.02
        avg_loss = abs(np.mean(losses)) if losses else 0.01
        return avg_win, avg_loss
    
    def add_position(self, coin_id, entry_price, quantity, stop_loss, take_profit, score, timestamp):
        if len(self.positions) >= config.MAX_POSICIONES:
            return False
        self.positions[coin_id] = {
            'entry': entry_price,
            'quantity': quantity,
            'investment': quantity * entry_price,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'max_price': entry_price,
            'score': score,
            'open_time': timestamp
        }
        self.capital -= quantity * entry_price
        self.last_trade_time = timestamp
        self.save_state()
        return True
    
    def close_position(self, coin_id, exit_price, reason):
        pos = self.positions.pop(coin_id)
        pnl = (exit_price - pos['entry']) / pos['entry']
        self.capital += pos['quantity'] * exit_price
        trade_record = {
            'symbol': coin_id,
            'entry': pos['entry'],
            'exit': exit_price,
            'pnl': pnl,
            'score': pos['score'],
            'reason': reason,
            'timestamp': time.time(),
            'capital': self.capital
        }
        self.trades_history.append(trade_record)
        self.winrate_history.append(1 if pnl > 0 else 0)
        self.save_state()
        print(f"   🔴 CERRAR {coin_id} | PnL {pnl*100:.2f}% | {reason} | Capital: ${self.capital:.2f}")
        return pnl
    
    def update_positions(self, current_prices):
        for coin_id, pos in list(self.positions.items()):
            price = current_prices.get(coin_id)
            if price is None:
                continue
            if price > pos['max_price']:
                pos['max_price'] = price
            if price <= pos['stop_loss']:
                self.close_position(coin_id, price, 'stop_loss')
            elif price >= pos['take_profit']:
                self.close_position(coin_id, price, 'take_profit')

portfolio = Portfolio()