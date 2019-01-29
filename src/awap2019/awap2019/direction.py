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

    @classmethod
    def get_dir(cls, loc1, loc2):
        vector = (loc2[0] - loc1[0], loc2[1] - loc1[1])
        if vector == (0, -1):
            return cls.LEFT
        elif vector == (-1, 0):
            return cls.UP
        elif vector == (0, 1):
            return cls.RIGHT
        elif vector == (1, 0):
            return cls.DOWN
        else:
            return cls.NONE
