from abc import ABC, abstractmethod
import numpy as np
import os.path
import pickle
import time
import random

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


class Integer(DataType):

    def generate(self, row_count):
        return [np.random.randint(self.default[0], self.default[1]) for _ in range(row_count)]


class Float(DataType):

    def generate(self, row_count):
        return [np.random.uniform(self.default[0], self.default[1]) for _ in range(row_count)]


class Alias(DataType):

    def generate(self, row_count):
        return ALIAS_LIST[self.default]


class String(DataType):

    def generate(self, row_count):
        if type(self.default[1]) == int:
            symbols = self.default[0]
            return [''.join(
                str(x) for x in
                [symbols[np.random.randint(0, len(symbols), 1)[0]] for _ in range(int(self.default[1]))])
                for _ in range(row_count)]
        else:
            return [''.join(str(x) for x in
                            [self.default[np.random.randint(0, len(self.default), 1)[0]] for _ in
                             range(np.random.randint(1, 20, 1)[0])])
                    for _ in range(row_count)]


class SetChoice(DataType):

    def generate(self, row_count):
        return [np.random.choice(self.default) for _ in range(row_count)]


class WeighedChoice(DataType):
    def generate(self, row_count):
        return [np.random.choice(self.default[0], p=list(map(lambda x: x / 100, self.default[1]))) for _ in
                range(row_count)]


class Mask(DataType):
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                'u', 'v', 'w', 'x', 'y', 'z']
    digits = [i for i in range(10)]

    def generate(self, row_count):
        return [self.get_string(self.default[0]) for _ in range(row_count)]

    def get_string(self, mask):
        for i in range(len(mask)):
            if mask[i] == "#":
                if self.default[1] and self.default[2]:
                    mask = mask[:i] + str(np.random.choice(self.alphabet + self.digits)) + mask[i + 1:]
                elif self.default[1]:
                    mask = mask[:i] + str(np.random.choice(self.digits)) + mask[i + 1:]
                else:
                    mask = mask[:i] + str(np.random.choice(self.alphabet)) + mask[i + 1:]
        return mask


def str_time_prop(start, end, time_format, prop):
    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(time_format, time.localtime(ptime))


class TimeStamp(DataType):
    @staticmethod
    def random_date(start, end, prop):
        return str_time_prop(start, end, '%Y-%m-%d %H:%M:%S', prop)

    def generate(self, row_count):
        return [self.random_date(self.default[0], self.default[1], random.random()) for _ in range(row_count)]


class Date(DataType):
    @staticmethod
    def random_date(start, end, prop):
        return str_time_prop(start, end, '%Y-%m-%d', prop)

    def generate(self, row_count):
        return [self.random_date(self.default[0], self.default[1], random.random()) for _ in range(row_count)]
