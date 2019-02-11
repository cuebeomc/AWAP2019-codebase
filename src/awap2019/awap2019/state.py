from enum import Enum
from .direction import Direction

class State(object):
    def __init__(self, bot):
        team_id = bot.get_team_id()
        loc = bot.get_loc()
        self.dir = bot.direction
        self.team_id = -1 if team_id is None else team_id
        self.id = bot.get_id()
        self.x = loc[0]
        self.y = loc[1]
        self.progress = bot.progress
        self.threshold = bot.board.get(self.dir.get_loc(loc)).get_threshold()
        self.line_pos = -1 if bot.line_pos is None else bot.line_pos

        if bot.is_in_line():
            self.state = "inline"
        elif bot.direction == Direction.LEFT:
            self.state = "left"
        elif bot.direction == Direction.RIGHT:
            self.state = "right"
        elif bot.direction == Direction.DOWN:
            self.state = "down"
        elif bot.direction == Direction.UP:
            self.state = "up"
        else:
            self.state = "none"

    def __repr__(self):
        return "TID_%02d ID_%02d @%02d.%02d P_%02d_T_%02d_L_%02d" % (self.team_id,
            self.id, self.x, self.y, self.progress, self.threshold, self.line_pos)

    # self.state is None?
    def get_num_encoding(self):
        return "{} {} {} {} {} {} {} {}".format(self.team_id, self.id, self.x,
                                               self.y, self.state, 
                                               self.progress, self.threshold,
                                               self.line_pos)

