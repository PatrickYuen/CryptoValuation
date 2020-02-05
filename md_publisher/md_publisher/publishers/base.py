from abc import ABC, abstractmethod
import asyncio
import zmq
from typing import Optional


class Publisher(ABC):
    def __init__(self, config):
        self._context: zmq.Context = zmq.Context()
        self._socket: Optional[zmq.Socket] = None  # self._context.socket(zmq.PUB)
        self.socket_connection = config["socket_connection"]

        self.connection = asyncio.Future()
        self.connect_handler = None

        self.is_connected = False

    @abstractmethod
    async def connect(self):
        pass

    async def start(self):
        try:
            await self.connect()
        except Exception as e:
            self.close(e)

    def send(self, topic: str, msg: str):
        print(msg)
        self._socket.send(f'{topic} {msg}'.encode('utf-8'), copy=False)

    def close(self, exception=None):
        if not self.connection.done():
            if exception:
                self.connection.set_exception(exception)
            else:
                self.connection.set_result(None)
        self.is_connected = False

    def __enter__(self):
        self._socket = self._context.socket(zmq.PUB)  # Why?
        self._socket.connect(self.socket_connection)
        self.connect_handler = asyncio.ensure_future(self.start())
        self.is_connected = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connect_handler.cancel()
        self._socket.close()
        self.close(exc_val)
