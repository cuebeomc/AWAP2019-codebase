from .bot import Bot
from ..direction import Direction
from .algs import BFS

class ExtrovertBot(Bot):
    '''
    ExtrovertBot find the position in the map where there are the most amount
    of people.
    '''

    ''' 
    We add this value to the population of the neighborhood tiles when
    deciding whether or to the change the destination tile to a different
    adjacent tile. This is added just in case our ExtrovertBot changes
    directions too often and ultimately does not move. Increase this
    value to ensure the bot moves more, decrese this value so that
    its more purely an extrovert.
    Example:
    Set this to zero if you always want to change your destination tile
    to the neighboring location with the most people.
    Example:
    Set this to one if one of the neighboring locations needs two more
    people on it for this bot the change their direction.
    '''
    REORIENT_COST = 2

    def __init__(self, board, loc, speed, id):
        super().__init__(board, loc, speed, id)
        self.queue = []

    def find_big_brain(self):
        '''
        Finds the tile with the most people.
        '''
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

