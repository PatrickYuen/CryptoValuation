from .base import Transformer
from collections import defaultdict
from val_analysis.states import OrderBookLevel


class CoinbaseProBookTransformer(Transformer):

    def __init__(self, state):
        super().__init__(state)
        self.dispatch_handlers = defaultdict(
            lambda: self.noop,
            {
                "snapshot": self.snapshot,
                "l2update": self.update,
            }
        )
        
        self._side_map = {
            "buy": self.state.bids,
            "sell": self.state.asks,
        }

    def handle(self, msg):
        msg_type = msg["type"]
        self.dispatch_handlers[msg_type](msg)

    @staticmethod
    def noop(msg):
        pass

    def snapshot(self, msg):
        """
        {
            "type": "snapshot",
            "product_id": "BTC-USD",
            "bids": [["10101.10", "0.45054140"], ...],
            "asks": [["10102.55", "0.57753524"], ...]
        }
        """
        for price, size in msg["bids"]:
            price, size = float(price), float(size)
            self.state.bids[price] = OrderBookLevel(price, size)

        for price, size in msg["asks"]:
            price, size = float(price), float(size)
            self.state.asks[price] = OrderBookLevel(price, size)

        self.state.empty = False

    def update(self, msg):
        """
        {
            "type":"l2update",
            "product_id":"BTC-USD",
            "changes":[["buy","9338.30","0.02000000"]],
            "time":"2019-11-03T03:10:43.661000Z"},
        }
        """
        for side, price, size in msg["changes"]:
            price, size = float(price), float(size)
            book_side = self._side_map[side]
    
            if size == 0:
                # Delete Level
                del book_side[price]
                return

            book_side[price] = OrderBookLevel(price, size)
