from abc import ABC, abstractmethod


class Transformer(ABC):
    def __init__(self, state):
        self.state = state

    @abstractmethod
    def handle(self, msg):
        pass
