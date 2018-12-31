from .direction import Direction

class Bot(object):

    def __init__(self, board, loc, speed, id, team_id=None):
        """Initializes a basic bot."""
        if board:
            (board.get(loc)).add_bot(self)
        else:
            self.loc = loc
        self.board = board
        self.progress = 0
        self.speed = speed
        self.type = None
        self.id = id
        self.team = team_id

        self.direction = Direction.NONE
        self.new_direction = Direction.NONE

    def __str__(self):
        return "{}: {}".format(self.id, self.loc)

    def __repr__(self):
        return "{}: {}".format(self.id, self.loc)

    def copy(self):
        """Generate a copy of the bot for player copy."""
        new_bot = Bot(None, self.loc, self.speed, self.id)
        new_bot.progress = self.progress
        new_bot.type = self.type

        new_bot.direction = self.direction
        new_bot.new_direction = self.new_direction

        return new_bot

    def set_id(self, new_id):
        self.id = new_id

    def get_id(self):
        return self.id

    def get_team_id(self):
        return self.team

    def set_loc(self, loc):
        """DANGEROUS: do not use except in tile.py"""
        self.loc = loc

    def get_loc(self):
        """Returns the location of the bot."""
        return self.loc

    def set_new_direction(self, dir):
        """Set the direction of this bot if it is valid. Only should be used
        when setting direction specified from the player."""
        if type(dir) != Direction:
            self.new_direction = Direction.NONE
        else:
            self.new_direction = dir

    def compute_step(self):
        """Computes the next step and places it into self.new_direction."""
        raise "You must implement compute_step"

    def update_progress(self):
        """Updates the movement progress of the bot."""
        if self.direction == Direction.NONE:
            self.progress = 0
            return
        elif self.direction == Direction.ENTER:
            print("Entering line.")
            self.progress = 0
            self.board.get(self.loc).add_to_line(self)
            self.direction = Direction.NONE
            return
        self.progress += self.speed
        new_loc = (self.direction).get_loc(self.loc)
        dest_tile = (self.board).get(new_loc)
        if self.progress >= dest_tile.get_threshold():
            curr_tile = (self.board).get(self.loc)
            curr_tile.remove_bot(self)
            dest_tile.add_bot(self)
            self.direction = Direction.NONE
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
        """Checks if self.new_direction is a valid direction."""
        new_loc = (self.new_direction).get_loc(self.loc)
        if (0 <= new_loc[0] < (self.board).x_dim() and
           0 <= new_loc[1] < (self.board).y_dim()):
            dest_tile = (self.board).get(new_loc)
            if not dest_tile.get_booth():
                return True
        return False
