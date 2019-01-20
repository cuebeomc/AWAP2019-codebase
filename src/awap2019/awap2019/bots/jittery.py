from .bot import Bot
from ..direction import Direction
import random

LINE_PROB = 0.6

class JitteryBot(Bot):
    def __init__(self, board, loc, speed, id):
        super().__init__(board, loc, speed, id)
        self.next_loc = self.loc

        self.directions = [Direction.LEFT, Direction.UP, Direction.RIGHT, Direction.DOWN]
    
    def compute_step(self):
        if self.in_line:
            self.next_loc = self.loc
        elif self.loc == self.next_loc:
            rand_num = random.uniform(0, 1)
            curr_tile = self.board.get(self.loc)
            if curr_tile.is_end_of_line() and rand_num <= LINE_PROB:
                self.new_direction = Direction.ENTER
            else: 
                random.shuffle(self.directions)
                for direction in self.directions:
                    if self._is_valid(direction):
                        self.new_direction = direction
                        break
                self.next_loc = self.new_direction.get_loc(self.loc)
