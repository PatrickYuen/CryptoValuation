from .base import Observer
from .util import SMA, EMA


class MovingAverageCrossObserver(Observer):
    topic = 'ma'

    def __init__(self, state):
        super().__init__(state)

        self.sma_short = SMA(window_size=60)
        self.sma_long = SMA(window_size=300)

        self.ema_short = EMA(window_size=60)
        self.ema_long = EMA(window_size=300)

    def observe(self):
        if self.state.empty:
            return None

        tob_bid_price = self.state.tob_bid.price
        tob_ask_price = self.state.tob_ask.price
        tob_mid_price = (tob_bid_price + tob_ask_price) / 2

        self.sma_short.update(tob_mid_price)
        self.sma_long.update(tob_mid_price)
        self.ema_short.update(tob_mid_price)
        self.ema_long.update(tob_mid_price)

        return {
            "ma_time": [self.current_time],
            "sma_short": [self.sma_short.sma],
            "sma_long": [self.sma_long.sma],
            "ema_short": [self.ema_short.ema],
            "ema_long": [self.ema_long.ema],
        }
