from datahack import *


class Table:
    string = String((['a', 'b', 'c'], 2))
    choice = SetChoice(['123', 456, 'hello'])
    mask = Mask(["123##456#", True, True])
    number = Number((1, 10), alias="hello_world")
    something = Alias("hello_world")
