import asyncio
from typing import Optional

import zmq
from zmq.asyncio import Context

from val_analysis.controllers import StrategyController


class MarketReactor:
    def __init__(self, config, controller: StrategyController, reactor_cycle=1):
        self._context: Context = Context()
        self._socket: Optional[zmq.Socket] = None
        self.socket_connection = config["sub_socket_connection"]

        self.connection = asyncio.Future()
        self.is_connected = False

        self.connect_handler = None
        self.reactor_handler = None

        self.controller = controller
        self._reactor_cycle = reactor_cycle

        self._batch = []  # Can I do better?

    async def connect(self):
        while self.connection:
            msg = await self._socket.recv()
            self._batch.append(msg)

    async def flush(self):
        while self.connection:
            self.controller.dispatch(self._batch)
            if self._batch:
                self._batch = []  # Clear batch
            await asyncio.sleep(self._reactor_cycle)

    async def start(self, func):
        try:
            await func()
        except Exception as e:
            self.close(e)

    def close(self, exception=None):
        if not self.connection.done():
            if exception:
                self.connection.set_exception(exception)
            else:
                self.connection.set_result(None)
        self.is_connected = False

    def __enter__(self):
        self._socket = self._context.socket(zmq.SUB)
        self._socket.bind(self.socket_connection)
        self._socket.setsockopt(zmq.SUBSCRIBE, b"")
        self.connect_handler = asyncio.ensure_future(self.start(self.connect))
        self.reactor_handler = asyncio.ensure_future(self.start(self.flush))
        self.is_connected = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.reactor_handler.cancel()
        self.connect_handler.cancel()
        self._socket.close()
        self.close(exc_val)
