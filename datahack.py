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
        return [np.random.uniform(self.default[0], self.default[1]) for i in range(row_count)]


class Alias(DataType):

    def generate(self, row_count):
        return ALIAS_LIST[self.default]


class String(DataType):

    def generate(self, row_count):
        symbols = self.default[0]
        l = len(symbols)
        return [''.join(str(x) for x in [symbols[np.random.randint(0, l, 1)[0]] for j in range(self.default[1])])
                for w in range(row_count)]


class SetChoice(DataType):

    def generate(self, row_count):
        return [np.random.choice(self.default) for i in range(row_count)]


class Mask(DataType):
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                'u', 'v', 'w', 'x', 'y', 'z']
    digits = [i for i in range(10)]

    def generate(self, row_count):
        mask = self.default[0]
        ifInt = self.default[1]
        ifStr = self.default[2]

        return [self.get_string(mask, ifInt, ifStr) for j in range(row_count)]

    def get_string(self, mask, ifInt, ifStr):
        for i in range(len(mask)):
            if mask[i] == "#":
                if ifInt and ifStr:
                    mask = mask[:i]+str(np.random.choice(self.alphabet + self.digits))+mask[i+1:]
                elif ifInt:
                    mask = mask[:i]+str(np.random.choice(self.digits))+mask[i+1:]
                else:
                    mask = mask[:i]+str(np.random.choice(self.alphabet))+mask[i+1:]
        return mask
