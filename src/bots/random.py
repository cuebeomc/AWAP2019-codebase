import src.Bot as Bot
import random

class RandumbBot(Bot):
"""
RandumbBot attempts to set destination tile to either its current tile or one
of its four adjacent tiles, regardless of validity for the given Board
"""

    def compute_step(self, board):
        curx, cury = self.tile.getLocation()

        dirx = 0
        diry = 0

        dir = random.randint(0, 4) #nothing, east, north, west, south

        if dir == 1:
            dirx = 1
        elif dir == 2:
            diry = -1
        elif dir == 3:
            dirx = -1
        elif dir == 4:
            diry = 1

        self.dest_tile = board[curx + dirx, cury + diry]
