from enum import Enum

class Direction(Enum):
    NONE = (None, None)
    LEFT = (0, -1)
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    ENTER = (0, 0)
    REPLACE = (None, 0)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_loc(self, loc):
        if self.x is None:
            return loc
        return (loc[0] + self.x, loc[1] + self.y)
