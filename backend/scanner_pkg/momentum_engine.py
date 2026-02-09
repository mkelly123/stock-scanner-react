import time
from collections import deque

class MomentumEngine:
    def __init__(self):
        self.history = {}  # symbol → deque of (timestamp, price, volume)

    def update(self, symbol, price, volume):
        now = time.time()

        if symbol not in self.history:
            self.history[symbol] = deque(maxlen=60)

        self.history[symbol].append((now, price, volume))

        return self.compute(symbol)

    def compute(self, symbol):
        data = list(self.history[symbol])
        if len(data) < 5:
            return None

        # Latest
        t_now, p_now, v_now = data[-1]

        # 10 seconds ago
        t_old, p_old, v_old = data[0]

        price_momentum = p_now - p_old
        volume_delta = v_now - v_old

        score = price_momentum * max(volume_delta, 1)

        return {
            "symbol": symbol,
            "price": p_now,
            "volume": v_now,
            "momentum": price_momentum,
            "volumeDelta": volume_delta,
            "score": score
        }
