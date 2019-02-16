from .bot import Bot
from ..direction import Direction
from .algs import BFS
import random

class RandomBot(Bot):
    '''
    Defines a bot which goes to a random company of the given size.
    The possible sizes are None, S, M, L. If the size is None then all companies
    are allowed, otherwise only companies of the same size are allowed.
    After exiting a line for a company, the bot will again randomly select a company.
    '''
    def __init__(self, board, loc, speed, id, size=None):
        super().__init__(board, loc, speed, id)
        self.queue = []
        self.choices = None
        self.choices = [name for name in self.board.booths if self.board.booths[name].get_size() == size]
        if len(self.choices) == 0:
            self.choices = [name for name in self.board.booths]
        self.booth = None
    
    def compute_step(self):
        if not self.is_in_line():
            src = self.loc
            if not self.queue:
                self.booth = random.choice(self.choices)
                self.queue = BFS(self.board, src, lambda tile: tile.is_end_of_line() and tile.get_line() == self.booth)

        if self.queue:
            if self.loc == self.queue[0]:
                self.queue.pop(0)
            if self.queue:
                first_tile = self.queue[0]
                self.new_direction = Direction.get_dir(self.loc, first_tile)
            else:
                self.new_direction = Direction.ENTER
