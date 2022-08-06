from abc import ABC, abstractmethod
import numpy as np
import os.path
import pickle

ALIAS_LIST = {}


def init():
    global ALIAS_LIST
    if os.path.exists("alias.pk"):
        with open("alias.pk", 'rb') as file:
            ALIAS_LIST = pickle.load(file)
    return ALIAS_LIST


class DataType(ABC):

    @abstractmethod
    def generate(self, row_count):
        ...

    def __init__(self, default, alias=None):
        self.default = default
        self.alias = alias


class Number(DataType):

    def generate(self, row_count):
        return [np.random.randint(self.default[0], self.default[1]) for i in range(row_count)]


class Alias(DataType):

    def generate(self, row_count):
        return ALIAS_LIST[self.default]
