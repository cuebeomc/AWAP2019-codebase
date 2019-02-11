from .bot import Bot
from ..direction import Direction
from .algs import BFS

class LineFollower(Bot):
    def __init__(self, board, loc, speed, id):
        super().__init__(board, loc, speed, id)
        self.queue = []
    
    def compute_step(self):
        if not self.queue:
            src = self.loc
            dest = (4, 1)
            self.queue = BFS(self.board, src, dest)

        if self.queue:
            if self.loc == self.queue[0]:
                self.queue.pop(0)
            if self.queue:
                first_tile = self.queue[0]
                self.new_direction = Direction.get_dir(self.loc, first_tile)
