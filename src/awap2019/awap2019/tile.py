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
    def __init__(self, x, y):
        self.loc = (x, y)
        self.bots_in_line = []
        self.bots = []
        self.end_of_line = False
        self.line = None
        self.booth = None
        self.update_threshold()

    def __str__(self):
        return "({}, {})".format(len(self.bots), len(self.bots_in_line))

    def __repr__(self):
        if not self.booth == None:
            return "BOOTH"
        if self.end_of_line:
            return "E%02d%02d" % (len(self.bots), len(self.bots_in_line))
        if not self.line == None:
            return "L%02d%02d" % (len(self.bots), len(self.bots_in_line))
        return "T%02d%02d" % (len(self.bots), len(self.bots_in_line))
        #return "({}, {})".format(len(self.bots), len(self.bots_in_line))

    # Getters that are available to players.
    def get_line(self):
        """
        If this tile is part of a line, returns the name of the company
        it is a line for. Otherwise, returns None."""
        return self.line

    def get_booth(self):
        """
        If this tile is part of a booth, returns the name of the company
        of the booth. Otherwise, returns None."""
        return self.booth

    def get_num_bots(self):
        """
        Returns the number of bots on this tile.
        
        If the tile is part of a line, the number of bots on the tile
        includes the number of bots in the line."""
        return len(self.bots) + len(self.bots_in_line)

    def is_end_of_line(self):
        """
        If the current end of the line is on this tile, returns True.
        Otherwise, returns False.
        
        Note that this method returns False even if this line is not
        part of a tile (tile.get_line() == None)."""
        return self.end_of_line

    # Setters used only in initialization
    def set_line(self, name):
        self.line = name

    def set_booth(self, name):
        self.booth = name

    # Functions available to non-players
    def get_threshold(self):
        return self.threshold

    def get_loc(self):
        """Returns the location of this tile."""
        return self.loc

    # Functions that will only be available to the internal game mechanics.
    def update_threshold(self):
        pop = self.get_num_bots()
        if pop == 0:
            self.threshold = 1
        elif pop == 1:
            self.threshold = 1
        elif pop == 2:
            self.threshold = 1
        elif pop == 3:
            self.threshold = 1
        elif pop == 4:
            self.threshold = 2
        elif pop == 5:
            self.threshold = 2
        elif pop == 6:
            self.threshold = 2
        elif pop == 7:
            self.threshold = 3
        elif pop == 8:
            self.threshold = 3
        else:
            self.threshold = 5

    def get_bots_in_line(self):
        return self.bots_in_line

    def set_end_of_line(self, value):
        self.end_of_line = value

    def update_line(self, line):
        self.bots_in_line = line
        for bot in line:
            bot.set_loc(self.loc)

    def add_bot(self, bot):
        (self.bots).append(bot)
        bot.set_loc(self.loc)

    def remove_bot(self, bot):
        try:
            (self.bots).remove(bot)
        except:
            (self.bots_in_line).remove(bot)

    def add_to_line(self, bot):
        if self.end_of_line and bot in self.bots:
            (self.bots_in_line).append(bot)
            self.remove_bot(bot)
            return True
        return False

    def copy(self):
        new_tile = Tile(self.loc[0], self.loc[1])
        new_tile.bots = [bot.copy() for bot in self.bots]
        new_tile.bots_in_line = [bot.copy() for bot in self.bots_in_line]
        new_tile.booth = self.booth
        new_tile.line = self.line
        new_tile.end_of_line = self.end_of_line
        new_tile.update_threshold()

        return new_tile

class Booth(object):
    def __init__(self, name, size, booth_tiles, line_tiles, wait_time, value):
        """Booth handles the set of tiles that constitute a company's booth.
        It initializes the lines and stores them.

        name: the name of the booth (that is, the name of the company)
        size: size of the company for the booth.
        booth_tiles: list of tiles that constitute the booth
        line_tiles: list of tiles which start with the tile that is
                    the end of the line.
        wait_time: the time it takes the recruiter to talk to the person
                   at the front of the line.
        """
        self.name = name
        self.size = size
        self.tiles = booth_tiles
        for tile in booth_tiles:
            tile.set_booth(name)
        self.line = Line(self.name, line_tiles, wait_time)
        self.value = value

    def get_size(self):
        """Gets the size of the company."""
        return self.size

    def execute_step(self):
        """Executes steps for the line."""
        return (self.line).execute_step()
    
    def get_end(self):
        return self.line.get_end()

class Line(object):
    """
    Line is a collection of tiles that are part of the "line zone".
    Line is responsible for moving the bots in a line if they choose
    to stay in the line.
    """
    def __init__(self, name, tiles, wait_time, max_per_tile=3):
        """
        name: Name of the company the line is for.
        tiles: The list of tiles that constitute the line. The first tile
               in the list should be
        wait_time: The number of turns it takes for the recruiter to talk
                   to the person at the front of the line.
        max_per_tile: The max number of people per tile.
        progress: The current progress of the recruiter.
        current_talker: the bot that is currently talking to the recruiter.
        """
        self.name = name
        for tile in tiles:
            tile.set_line(name)
        self._order(tiles)

        self.wait_time = wait_time
        self.progress = 0
        self.current_talker = None
        self.max_per_tile = max_per_tile

        self.end_of_line = tiles[0]
        self.tiles[0].set_end_of_line(True)

    def execute_step(self):
        """Compresses the line, updates the talker, and redelegates lines."""
        ret_val = None

        full_line = []
        for tile in self.tiles:
            full_line += tile.get_bots_in_line()
        if full_line:
            front_of_line = full_line[0]
            if front_of_line == self.current_talker:
                self.progress += 1
                if self.progress >= self.wait_time:
                    full_line.pop(0)
                    self.current_talker.in_line = False
                    self.current_talker.line_pos = None
                    self.current_talker.line_name = None
                    self.progress = 0
                    self.tiles[0].add_bot(self.current_talker)

                    team_id = self.current_talker.get_team_id()
                    if team_id is not None:
                        bot_id = self.current_talker.get_id()
                        ret_val = (self.name, team_id, bot_id)
            else:
                self.progress = 0
                self.current_talker = front_of_line
        else:
            self.current_talker = None
        for i, bot in enumerate(full_line):
            bot.in_line = True
            bot.line_pos = i
            bot.line_name = self.name

        self._delegate(full_line)
        return ret_val

    def _delegate(self, line):
        """Delegates the bots into the lines."""
        last_tile = self.tiles[-1]
        end = False
        for tile in self.tiles:
            if tile == last_tile:
                tile.update_line(line)
            else:
                mini_line = line[:self.max_per_tile]
                line = line[self.max_per_tile:]
                if len(mini_line) < self.max_per_tile and (not end):
                    end = True
                    self.end_of_line = tile
                    tile.set_end_of_line(True)
                else:
                    tile.set_end_of_line(False)
                tile.update_line(mini_line)

    def _order(self, tiles):
        if len(tiles) <= 1:
            self.tiles = tiles
        else:
            sort_index = None
            rev = False

            end_loc = tiles[0].get_loc()
            comp = tiles[1].get_loc()
            if end_loc[0] == comp[0]:
                sort_index = 1
            else:
                sort_index = 0
            if end_loc[sort_index] < comp[sort_index]:
                rev = True

            self.tiles = sorted(tiles,
                                key=lambda x: x.loc[sort_index],
                                reverse=rev)

    def get_end(self):
        """Returns the tile that is the end of the line."""
        return self.end_of_line
