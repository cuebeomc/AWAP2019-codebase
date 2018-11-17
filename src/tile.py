class Tile(object):
    """ Tile keeps track of everything on a tile.

    loc: the lattice position of the tile
    bots_in_line: the bots on this tile that are in a line (if a line exists)
    bots: the bots on this tile that are not in a line
    end_of_line: indicates true if this is the current "end of the line";
                 that is, bots enter the line on this tile.
    line: None if not part of a line, otherwise a Line object
    booth: None if free, otherwise a Booth object
    threshold: progress needed to move into this tile
    """
    def __init__(self, x, y, max):
        self.loc = (x, y)
        self.bots_in_line = []
        self.bots = []
        self.end_of_line = false
        self.line = None
        self.booth = None
        self.threshold = max

    def compute_step(self, board):
        """Calculates the next step for each of the bots in the line."""
        for bot in self.bots:
            bot.compute_step(board)
        for bot in self.bots_in_line:
            bot.compute_step(board)

    def execute_step(self):
        """Executes the precomputed step for each bot."""
        for bot in self.bots:
            bot.execute_step()
        for bot in self.bots_in_line:
            bot.execute_step()

    def get_location(self):
        return self.loc

    def get_population(self):
        return len(bots) + len(bots_in_line)

    def is_line(self):
        """Returns true if tile is part of line."""
        return (self.line != None)

    def get_line(self):
        """Returns the line if tile is part of the booth."""
        return self.line

    def is_booth(self):
        """Returns true if tile is part of booth. Line should not be set."""
        return (self.booth != None) and (self.line == None)

    def get_booth(self):
        """Returns the booth if tile is part of the booth."""
        if self.is_booth():
            return self.booth
        else:
            return None

    def set_line(self, ln):
        """Only to be used in init. Sets the line for this tile."""
        self.line = ln

    def set_booth(self, bth):
        """Only to be used in init. Sets the booth for this tile."""
        self.booth = bth

    def add_to_line(self, bot):
        """Adds bot to the line. Returns true if successful, false o/w."""
        if end_of_line:
            bots_in_line.append(bot)
            return True
        return False

    def add_to_tile(self, bot):
        """Adds bot to the tile. Returns true, for consistency."""
        bots.append(bot)
        return True

    def remove_from_line(self, bot):
        """Attempts to remove bot from line. True if successful."""
        try:
            self.bots_in_line = self.bots_in_line.remove(bot)
            return True
        except ValueError:
            return False

    def get_bots_in_line(self):
        return self.bots_in_line

    def remove_from_tile(self, bot):
        """Attempts to remove bot from tile. True if successful."""
        try:
            self.bots = self.bots.remove(bot)
            return True
        except ValueError:
            return False

    def set_end_of_line(self, end_of_line):
        """Updates this tile's status as the end of the line."""
        self.end_of_line = end_of_line

    def update_line(self, new_line):
        """Sets the line to an updated line. (Mass update)"""
        self.bots_in_line = new_line

    def get_threshold(self):
        """Gets the threshold limit of the tile."""
        return self.threshold

    def update_threshold(self):
        """Updates the threshold for movement into this tile."""
        self.threshold = int(Math.log(2.0 * len(self.bots_in_line)
                          + 3.0 * len(self.bots)))

#represents a block of tiles that are a booth. References 1 or 2 lines.
class Booth(object):
    def __init__(self, name, size, booth_tiles, lines, wait_time):
        """ Booth handles the set of tiles that constitute a company's booth.
        It initializes the lines and stores them under booth.

        booth_tiles: list of tiles that constitute the booth
        size: size of the company for the booth.
        name: the name of the booth (that is, the name of the company)
        line_tiles: list of lists of tiles, each of which constitute
                    an individual line. Should not be empty.
        """
        self.name = name
        self.size = size
        self.tiles = booth_tiles
        for tile in booth_tiles:
            tile.set_booth(self)
        self.lines = [Line(self.name, line, wait_time) for line in lines]

    def execute_step(self):
        for line in self.lines:
            line.execute_step()

class Line(object):
    """
    Line is a collection of tiles that are part of the "line zone".
    Line is responsible for moving the bots in a line if they choose
    to stay in the line.
    """
    TIME_DECREASE_AMOUNT = 10

    def __init__(self, name, tiles, wait_time, max_per_tile):
        """
        name: Name of the company the line is for.
        tiles: The list of tiles that constitute the line. Should be in order
               from front to end, where end is the last tile in the tile.
        recruiter_speed: The number of turns it takes to pop a person
                         off the line.
        progress: the current progress
        current_talker: the bot that is currently talking to the recruiter.
        """
        self.booth_name = name
        self.tiles = tiles
        for tile in tiles:
            tile.set_line(self)
        self.tiles[0].set_end_of_line(True)
        self.recruiter_speed = wait_time
        self.progress = 0
        self.current_talker = None
        self.max_per_tile = max_per_tile

    def execute_step(self):
        self.update_line()

    def update_line(self):
        full_line = []
        for tile in self.tiles:
            full_line += tile.get_bots_in_line()
        if full_line:
            front_of_line = full_line[0]
            if front_of_line == self.current_talker:
                self.progress += 1
                if self.progress >= self.recruiter_speed:
                    full_line.pop(0)
        try:
            self.current_talker = full_line[0]
        except:
            self.current_talker = None
        self.delegate(full_line)

    def delegate(self, line):
        last_tile = self.tiles[-1]
        for tile in self.tiles:
            if tile == last_tile:
                tile.update_line(line)
            else:
                mini_line = line[:self.max_per_tile]
                line = line[self.max_per_tile:]
                tile.update_line(mini_line)
