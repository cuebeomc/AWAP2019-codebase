from direction import Direction

class Bot(object):

    def __init__(self, board, loc, speed):
        """Initializes a basic bot."""
        self.loc = loc
        board.grid[loc[0]][loc[1]].add_bot(self)
        self.board = board
        self.progress = 0
        self.speed = speed
        self.type = None

        self.direction = Direction.NONE
        self.new_direction = Direction.NONE

    def copy(self):
        new_bot = Bot(None, self.loc, self.speed)
        new_bot.progress = self.progress
        new_bot.type = self.type

        new_bot.direction = self.direction
        new_bot.new_direction = self.new_direction

        return new_bot

    def get_loc(self):
        return self.loc

    def set_new_direction(self, dir):
        # Should check that dir is a type defined by Direction
        self.new_direction = dir

    def compute_step(self):
        """Computes the next step and places it into self.new_direction."""
        raise "You must implement compute_step"

    def update_progress(self):
        """Updates the movement progress of the bot."""
        if self.direction == Direction.NONE:
            self.progress = 0
            return
        self.progress += self.speed
        new_loc = (self.direction).get_loc(self.loc)
        dest_tile = (self.board).get(new_loc)
        if self.progress >= dest_tile.get_threshold():
            curr_tile = (self.board).get(self.loc)
            curr_tile.remove_from_tile(self)
            dest_tile.add_to_tile(self)
            self.loc = new_loc
            self.progress = 0

    def execute_step(self):
        """Executes the computed step, if valid."""
        if self.new_direction != self.direction:
            if not self._is_valid():
                self.new_direction = Direction.NONE
            self.direction = self.new_direction
            self.progress = 0
        self.update_progress()

    def _is_valid(self):
        new_loc = (self.new_direction).get_loc(self.loc)
        if (0 <= new_loc[0] < (self.board).x_dim() and
           0 <= new_loc[1] < (self.board).y_dim()):
            dest_tile = (self.board).get(new_loc)
            print(dest_tile)
            if not dest_tile.get_booth():
                return True
        return False
