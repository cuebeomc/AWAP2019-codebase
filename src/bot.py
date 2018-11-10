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
        check_sane(self.dest_tile)
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
        Bot should set dest_tile, but does not have to.
        This function sets the self.dest_tile to a new destination
        if the bot has a change of heart and decides to move elsewhere
        """
        raise "You must implement compute_step"

    def compute_progress(self, board):
        """
        Computes progress of a bot. If the destination does not change,
        continue progress (i.e. progress is unchanged). Otherwise,
        set the progress to 0, because we are moving to a new location.

        If dest_tile is set to None: We are set to not moving, so don't move
        If dest_tile is set to same as tile: We should enter the line at the position
        If dest_tile is not equal to prev dest: We are changing our position, change progress back to 0
        If dest_tile is unchanged: Continue movement in that direction
        """
        old_dest = self.dest_tile
        compute_step(self,board)
        check_sane(self.dest_tile) # TODO(Cuebeom): change this
        check_within_reach(self.tile, self.dest_tile) # TODO(Cuebeom): either within 1 or dest_tile = None
        if old_dest != self.dest_tile:
            self.progress = 0


    def execute_step(self, new_dest=None):
        """
        Executes a step
        """
        if new_dest is not None:
            check_sane(new_dest)
            self.tile = new_dest
            self.dest_tile = None
            self.progress = 0
        elif dest_tile is not None:
            update_progress(self)
