from .bot import Bot
from ..direction import Direction
from .algs import BFS

class StillBot(Bot):
    """Simple class to test BFS"""
    def __init__(self, board, loc, speed, id):
        super().__init__(board, loc, speed, id)
        self.move = Direction.NONE
    
    def compute_step(self):
        src = self.loc
        dest = (4, 1)
        x = BFS(self.board, src, lambda tile: tile.get_loc() == dest)
        print("BFS list: {}".format(x))
        return self.move

