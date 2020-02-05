from .base import Observer


# TODO: Throttle is bid and ask haven't moved in threshold
class OrderBookObserver(Observer):
    topic = 'order_book'

    def observe(self):
        if self.state.empty:
            return None

        tob_bid_price = self.state.tob_bid.price
        tob_ask_price = self.state.tob_ask.price
        tob_mid_price = (tob_bid_price + tob_ask_price) / 2

        return {
            'book_time': [self.current_time],
            'bid': [tob_bid_price],
            'ask': [tob_ask_price],
            'mid': [tob_mid_price],
        }
