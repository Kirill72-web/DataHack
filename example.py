from datahack import *


class Table:
    string = String((['a', 'b', 'c'], 2))
    choice = SetChoice(['123', '456', 'hello'])
    mask = Mask(["123##456#", True, True])
    float = Float((1, 10), alias="hello_world")
    integer = Integer((1, 10))
    wchoice = WeighedChoice((['123', '456', 'hello'], [10, 20, 70]))
    date = DateTime(("2022-10-07 19:45:30", "2022-10-12 19:45:30", False))
    timestep = DateTime(("2022-10-07 19:45:30", "2022-10-12 19:45:30", True))
    a = Alias("hello_world")
