from .bot import Bot
from ..direction import Direction
from ..tile import Booth
from .algs import BFS

class RealisticBot(Bot):
    """
    RealisticBot aims for the smaller companies because it has the best
    chance of getting a job from a smaller company. It will not visit the
    same company twice, because there is no point in handing a resume out
    twice so it will mark the companies it has visited. It uses a bfs to
    search for the closest small company and move towards that direction.
    It should find a company and retrieve the path.
    """
    def __init__(self, board, loc, speed, id):
        super().__init__(board, loc, speed, id)
        self.queue = []
        self.to_visit = "S"
        self.visited = set()
    
    def update_to_visit(self):
        if self.to_visit == "S":
            self.to_visit = "M"
        elif self.to_visit == "M":
            self.to_visit = "L"
        else:
            self.to_visit = "S"
    
    def compute_step(self):
        if not self.is_in_line():
            src = self.loc
            self.queue = BFS(self.board, src, 
                             lambda tile: \
                             self.board.booths.get(tile.get_booth()) and \
                             self.board.booths.get(tile.get_booth()).get_size() == self.to_visit \
                             and tile.get_booth() not in self.visited)
            while self.queue is None:
                self.update_to_visit()
                self.visited = set()
                self.queue = BFS(self.board, src, 
                                 lambda tile: \
                                 self.board.booths.get(tile.get_booth()) and \
                                 self.board.booths.get(tile.get_booth()).get_size() == self.to_visit \
                                 and tile.get_booth() not in self.visited)
            self.queue = BFS(self.board, src, lambda tile: tile.get_line() == self.board.get(self.queue[-1]).get_booth())

        if self.queue:
            if self.loc == self.queue[0]:
                self.queue.pop(0)
            if self.queue:
                first_tile = self.queue[0]
                self.new_direction = Direction.get_dir(self.loc, first_tile)
            else:
                self.new_direction = Direction.ENTER
                self.visited.add(self.board.get(self.loc).get_line())
