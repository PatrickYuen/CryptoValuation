class SMA:
    def __init__(self, window_size):
        self.window_size = window_size
        self._window = []
        self._running_sum = 0

        assert window_size > 0, "Choose larger window size"

    @property
    def sma(self):
        return self._running_sum / len(self._window)

    def update(self, val):
        self._running_sum += val
        self._window.append(val)

        if len(self._window) > self.window_size:
            self._running_sum -= self._window.pop(0)


class EMA:
    """
    EMA=Price(t)×k+EMA(y)×(1−k)
    where:
    t=today
    y=yesterday
    N=number of days in EMA
    k=2÷(N+1)
    """

    def __init__(self, window_size):
        self.window_size = window_size
        self.ema = None
        self._k = 2 / (window_size + 1)

        assert window_size > 0, "Choose larger window size"

    def update(self, val):
        if self.ema is None:
            self.ema = val
            return

        self.ema = val * self._k + self.ema * (1 - self._k)

