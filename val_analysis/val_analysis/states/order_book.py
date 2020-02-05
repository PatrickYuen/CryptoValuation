from dataclasses import dataclass

from sortedcontainers import SortedDict


@dataclass
class OrderBookLevel:
    price: float
    size: float


class OrderBookState:
    """
    State of Order Book
    """

    def __init__(self):
        self.bids: SortedDict[float, OrderBookLevel] = SortedDict()
        self.asks: SortedDict[float, OrderBookLevel] = SortedDict()

        self.empty = True

    @property
    def tob_bid(self):
        if self.empty:
            return None
        return self.bids.peekitem(index=-1)[1]

    @property
    def tob_ask(self):
        if self.empty:
            return None
        return self.asks.peekitem(index=0)[1]
