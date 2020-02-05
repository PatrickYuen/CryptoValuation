from .base import Observer
from .util import EMA
from enum import Enum


class Trend(Enum):
    BULL = True
    BEAR = False

    def __str__(self):
        return self.name


class MACDObserver(Observer):
    topic = 'macd'

    def __init__(self, state):
        super().__init__(state)

        self.ema_short = EMA(window_size=12 * 60)
        self.ema_long = EMA(window_size=26 * 60)
        self.signal_base = EMA(window_size=9 * 60)
        self.trend = None

    def observe(self):
        if self.state.empty:
            return None

        tob_bid_price = self.state.tob_bid.price
        tob_ask_price = self.state.tob_ask.price
        tob_mid_price = (tob_bid_price + tob_ask_price) / 2

        self.ema_short.update(tob_mid_price)
        self.ema_long.update(tob_mid_price)

        macd = self.ema_short.ema - self.ema_long.ema
        self.signal_base.update(macd)

        # Fire signal
        trend = Trend(macd >= self.signal_base.ema)
        fire = trend != self.trend
        self.trend = trend

        return {
            "macd": macd,
            "macd_base": self.signal_base.ema,
            "fire": fire,
            "trend": str(trend),
        }
