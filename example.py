from datahack import *


class Table:
    string = String((['a', 'b', 'c'], 2))
    choice = SetChoice(['123', '456', 'hello'])
    mask = Mask(["123##456#", True, True])
    float = Float((1, 10), alias="hello_world")
    integer = Integer((1, 10), )
