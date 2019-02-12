from .bot import Bot
from ..direction import Direction
from .algs import BFS

class ExtrovertBot(Bot):
    def __init__(self, board, loc, speed, id):
        super().__init__(board, loc, speed, id)
        self.queue = []
        self.REORIENT_COST = 2

    def find_big_brain(self):
        max_pop = 0
        max_point = None

        for i in range(self.board.x_dim()):
            for j in range(self.board.y_dim()):
                if self.board.get((i,j)).get_num_bots() > max_pop:
                    max_pop = self.board.get((i,j)).get_num_bots()
                    max_point = (i, j)
        return max_point

    
    def compute_step(self):
        dest = self.find_big_brain() 
        path = BFS(self.board, self.loc, lambda tile: tile.get_loc() == dest)
        if not self.queue or \
           self.board.get(self.queue[-1]).get_num_bots() + self.REORIENT_COST < \
           self.board.get(path[-1]).get_num_bots():
            self.queue = path
        
        if self.queue:
            if self.loc == self.queue[0]:
                self.queue.pop(0)
            if self.queue:
                first_tile = self.queue[0]
                self.new_direction = Direction.get_dir(self.loc, first_tile)

