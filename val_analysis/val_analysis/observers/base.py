from abc import ABC, abstractmethod
import time


class Observer(ABC):
    def __init__(self, state):
        self.state = state

    @property
    def current_time(self):
        return time.time() * 1000

    @abstractmethod
    def observe(self):
        pass
