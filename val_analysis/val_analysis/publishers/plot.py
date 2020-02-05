from typing import Optional, Dict, Any

import zmq
import json


class PlotPublisher:
    def __init__(self, config):
        self._context: zmq.Context = zmq.Context()
        self._socket: Optional[zmq.Socket] = None
        self.socket_connection = config["pub_socket_connection"]

    def publish(self, topic: str, msg: Dict[str, Any]):
        print(msg)
        fmted_msg = json.dumps(msg)
        self._socket.send(f'{topic} {fmted_msg}'.encode('utf-8'), copy=False)

    def __enter__(self):
        self._socket = self._context.socket(zmq.PUB)  # Why?
        self._socket.bind(self.socket_connection)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._socket.close()
