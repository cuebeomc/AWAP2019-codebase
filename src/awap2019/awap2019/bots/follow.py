from .bot import Bot
from ..direction import Direction
from .algs import BFS

class LineFollower(Bot):
    def __init__(self, board, loc, speed, id):
        super().__init__(board, loc, speed, id)
        self.queue = []
        self.visited = set()
    
    def compute_step(self):
        if not self.is_in_line():
            src = self.loc
            self.queue = BFS(self.board, src, 
                             lambda tile: tile.is_end_of_line() \
                             and tile.get_line() not in self.visited)
            if self.queue is None:
                self.visited = set()
                self.queue = BFS(self.board, src, 
                             lambda tile: tile.is_end_of_line() \
                             and tile.get_line() not in self.visited)

        if self.queue:
            if self.loc == self.queue[0]:
                self.queue.pop(0)
            if self.queue:
                first_tile = self.queue[0]
                self.new_direction = Direction.get_dir(self.loc, first_tile)
            else:
                self.new_direction = Direction.ENTER
                self.visited.add(self.board.get(self.loc).get_line())
