from datahack import *


class Table:
    choice = SetChoice(['123', '456', 'hello'])
    mask = Mask(["123##456#", True, True])
    wchoice = WeighedChoice((['123', '456', 'hello'], [10, 20, 70]))
