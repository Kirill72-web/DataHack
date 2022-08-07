from datahack import *


class Table:
    string = String((['a', 'b', 'c'], 2))
    choice = SetChoice(['123', '456', 'hello'])
    mask = Mask(["123##456#", True, True])
    key_1 = Alias("key_1")
    key_2 = Alias("key_2")
    wchoice = WeighedChoice((['123', '456', 'hello'], [10, 20, 70]))
    date = Date(("2022-10-07", "2022-10-12"))
    key_3 = Alias("key_3")