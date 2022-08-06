from abc import ABC, abstractmethod
import numpy as np


class DataType(ABC):

    @abstractmethod
    def generate(self, row_count):
        ...

    def __init__(self, default):
        self.default = default


class Number(DataType):

    def generate(self, row_count):
        return [np.random.randint(self.default[0], self.default[1]) for i in range(row_count)]
