from datahack import *


class Table:
    string = String((['a', 'b', 'c'], 2))
    choice = SetChoice(['123', '456', 'hello'])
    mask = Mask(["123##456#", True, True], alias="mask_alias")
    float = Float((1, 10), alias="hello_world")
    integer = Integer((1, 10))
    wchoice = WeighedChoice((['123', '456', 'hello'], [10, 20, 70]))
    date = Date(("2022-10-07", "2022-10-12"))
    timestep = TimeStep(("2022-10-07 19:45:30", "2022-10-12 19:45:30"))
    a = Alias("hello_world")
