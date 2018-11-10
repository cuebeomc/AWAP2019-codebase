import abc

class Bot(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, position, step_gain, speed):
        self.tile = position
        self.step_gain = step_gain
        self.progress = 0
        self.dest_tile = None
        self.speed = speed

    def update_progress(self):
        if self.progress >= self.dest_tile.threshold:
            self.tile = self.dest_tile
            # TODO(Cuebeom): Update bots in tile class
            self.progress = 0
            self.dest_tile = None
        else:
            self.progress += self.speed

    @abc.abstractmethod
    def compute_step(self, board):
        """
        Bot should set dest_tile
        """
        raise "Superclass must implement compute_step"

    def compute_progress(self, board):
        new_dest = self.dest_tile
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        compute_step(self,board)
=======
        compute_step(self)
>>>>>>> Stashed changes
=======
        compute_step(self)
>>>>>>> Stashed changes
        if new_dest != self.dest_tile:
            self.progress = 0

    def execute_step(self, board, new_dest=None):
        if new_dest is not None:
            self.tile = new_dest
            self.dest_tile = None
            self.progress = 0
        elif dest_tile is not None:
            update_progress(self)
