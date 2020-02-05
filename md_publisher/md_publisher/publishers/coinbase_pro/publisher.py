import json
from typing import Dict, Any

import websockets
from ..base import Publisher


class CoinbaseProMDPublisher(Publisher):
    """
    Connect and stream to pub sub

    TODO: Create DAO instead of json/Munch?
    TODO: Deadman switch
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)

        self.ws_endpoint = config["websocket_endpoint"]
        self.currency_pairs = config["currency_pairs"]
        self.channels = config["channels"]

        self.topic = config["channel_topic"]

    @property
    def subscription_msg(self) -> str:
        return json.dumps(
            {
                "type": "subscribe",
                "product_ids": self.currency_pairs,
                "channels": self.channels,
            }
        )

    async def connect(self):
        async with websockets.connect(self.ws_endpoint) as ws_client:
            await ws_client.send(self.subscription_msg)

            while self.connection:
                msg = await ws_client.recv()
                self.send(self.topic, msg)
