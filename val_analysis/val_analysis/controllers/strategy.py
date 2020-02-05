from val_analysis.states import OrderBookState
from val_analysis import transformers, observers
from collections import defaultdict
import json


class StrategyController:
    def __init__(self, app_config, publisher):
        self.publisher = publisher

        # State -- Do Better with master state?
        self.state = OrderBookState()

        # Transformers
        self.handlers = defaultdict(lambda: None)
        for msg_type, handler_name in app_config['handlers'].items():
            handler_class = getattr(transformers, handler_name)
            self.handlers[msg_type] = handler_class(self.state)

        # Observers
        self.observers = []
        for observer_name in app_config['observers']:
            observer_class = getattr(observers, observer_name)
            self.observers.append(observer_class(self.state))

    @staticmethod
    def parse_msg(raw_msg: bytes):
        """
        b'coinbase_pro_book {"type":"l2update","product_id":"BTC-USD","changes":[["buy","8531.90","0.00000000"]],"time":"2019-11-17T22:47:58.913000Z"}'
        """
        str_msg = raw_msg.decode('utf-8')
        split_ind = str_msg.index(" ")
        return str_msg[:split_ind], json.loads(str_msg[split_ind:])

    def dispatch(self, msg_batch):
        for raw_msg in msg_batch:
            msg_type, msg = self.parse_msg(raw_msg)
            handler = self.handlers[msg_type]
            if handler:
                handler.handle(msg)

        # Can parallelize
        for strat in self.observers:
            info_msg = strat.observe()
            if info_msg:
                self.publisher.publish(strat.topic, info_msg)
