from sdg.types import *


class Table1:
    integer = Integer((1, 10), alias="hello")
    label = Alias("hello")
    string = SetChoice(['hello', 'hi'], alias="set")


class TableData:

    key = Alias("hello")
    str = String(['abc', 'key', 'value'], 3)
    set = Alias("set")
