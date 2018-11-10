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

    def compute_step(self):
        """Calculates the next step for each of the bots in the line."""
        for bot in self.bots:
            bot.compute_step()
        for bot in self.bots_in_line:
            bot.compute_step()

    def execute_step(self):
        """Executes the precomputed step for each bot."""
        for bot in self.bots:
            bot.execute_step()
        for bot in self.bots_in_line:
            bot.execute_step()

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

    def set_line(self, ln, bth):
        """Only to be used in init. Sets the line and booth for this tile."""
        self.line = ln
        self.booth = bth

    def set_booth(self, bth):
        """Only to be used in init. Sets the booth for this tile."""
        self.line = None
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
    def __init__(self, booth_tiles, line_tiles, name, wait_time):
        """
        Booth handles the set of tiles that constitute a company's booth.
        It 
        booth_tiles: list of tiles that constitute the booth
        name: the name of the booth (that is, the name of the company)
            line_tiles: list of lists of tiles, each of which constitute
                an individual line
            wait_time: how long it takes to talk to a recruiter
        """
        self.tiles = booth_tiles
        for tile in booth_tiles:
            tile.set_booth(self)
        self.name = name
        self.lines = []
        for tiles in line_tiles:
            self.lines.append(Line(self.name, tiles, self.wait_time))
        self.WAIT_TIME = wait_time

    def compute_step():
        # again, we assume talking to recruiter's isn't affected
        # by the amount of people around them

    def execute_step(self):
        for line in self.lines:
            line.execute_step()

#handle people leaving in the middle
class Line(object):
    """Line is a collection of tiles
        Line is responsible for updating bots in lines,
        while Tile is responsible for updating bots not
        in the line
        """
    TIME_DECREASE_AMOUNT = 10

    def __init__(self,booth_name,tiles, wait_time):
        """booth_name: name of the booth
            tiles: list of tiles that constitute the line. Should be in order
            from front to end, where end is the last tile in the line.
            """
        self.booth_name = booth_name
        self.tiles = tiles
        for tile in tiles:
            tile.put_into_line(self)
        tiles[len(tiles) - 1].set_end_of_line(true)
        self.last_tile_index = 0
        self.time_left = wait_time

    def add_bot(self,bot):
        if (self.tiles[last_tile_index].line_max_capacity):
            last_tile_index++
        self.tiles[last_tile_index].add_bot(bot,True)

    def compute_step():
        # we don't really have to compute anything
        # since for now we assume that progress for
        # talking to recruiter is independent of
        # local population density

    def execute_step(self):
        time_left -= TIME_DECREASE_AMOUNT
        if (time_left <= 0):
            move_up()

    def _move_up(self):
        """Moves the whole line up by one"""
        index = 0
        kicked_bot = self.tiles[index].pop_line()
        kicked_bot.step() # note step needs to handle moving after getting out of line
        index += 1
        while (index <= self.last_tile_index):
            lucky_bot = self.tiles[index].pop_line()
            self.tiles[index - 1].add_bot(lucky_bot, True)
            index += 1
        if self.tiles[last_tile_index].empty_line() and last_tile_index != 0:
            self.last_tile_index -= 1
