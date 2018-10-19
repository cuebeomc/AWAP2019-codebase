class Tile(object):

    MAX_PEOPLE_IN_LINE = 10

    def __init__(self,x,y,end_of_line):
        self.bots_in_line = []
        self.bots_not_in_line = []
        self.x = x
        self.y = y
        self.end_of_line = end_of_line
        self.line = None
        self.booth = None

    def compute_step(self):
        """ Represents movement after a single time step. """
        for bot in self.bots_not_in_line:
            bot.compute_step(compute_threshold())

    def execute_step(self):
        for bot in self.bots_not_in_line:
            bot.execute_step(compute_threshold())

    def add_bot(self,bot, to_line):
        """ to_line true if adding bot into the lines
                    false if adding bot not as a line""""
        if to_line:
            if not self.line :
                raise TileIsNotInLine
            if (not self.end_of_line) and len(self.bots_in_line) < MAX_PEOPLE_IN_LINE:
                raise TooManyPeopleInLine
            self.bots_in_line.append(bot)
        else:
            self.bots_not_in_line.append(bot)

    def empty_line(self):
        """True if no bots in line at this tile."""
        if not self.line:
            raise TileIsNotInLine
        return len(self.bots_in_line) == 0

    def line_max_capacity(self):
        """ True if the number of bots in line is at the max. """
        if not self.line:
            raise TileIsNotInLine
        return len(self.bots_in_line) == MAX_PEOPLE_IN_LINE

    def get_num_in_line(self):
        """ Return the number of bots in the line at this tile. """
        if not self.line:
            raise TileIsNotInLine
        return len(self.bots_in_line)

    def pop_line(self):
        """ Kick the bot at the front of the line at this tile
            *(Not responsible for stepping the kicked bot!!!
        """
        if not self.line:
            raise TileIsNotInLine
        self.bots_in_line.pop(0)

    def put_into_line(self,line):
        """ Give a reference to the line """
        self.line = line

    def get_line(self):
        return self.line

    def label_booth(self,booth):
        self.booth = booth

    def get_booth(self):
        if not self.booth:
            raise TileIsNotInBooth
        return self.booth

    #Moves bots a certain amount based on the number of bots in and out of line
    def compute_threshold(self):
        return int(Math.log(2.0 * len(self.bots_in_line) + 3.0 * len(self.bots_not_in_line)))

class TooManyPeopleInLine(Exception):
    """ Raised when a bot is added to a tile that is not the end of a line
        and the max capacity has already been reached
    """
    pass

class TileIsNotInLine(Exception):
    """" Raised when we try to do shit even though the tile is not part of a line
    """"
    pass

class TileIsNotInBooth(Exception):
    """" Raised when we try to do shit even though the tile is not part of a booth
    """"
    pass

#represents a block of tiles that are a booth. References 1 or 2 lines.
class Booth():

    def __init__(self, booth_tiles, line_tiles, name, wait_time):
        """ booth_tiles: list of tiles that constitute the booth already
            name : booth_name
            line_tiles: list of lists of tiles, each of which constitute
                an individual line
            wait_time: how long it takes to talk to a recruiter
            """
        self.tiles = booth_tiles
        for tile in booth_tiles:
            tile.label_booth(self)
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

    def add_bot(self,bot, line_index):
        self.line[line_index].add_bot(bot)

#handle people leaving in the middle
class Line():
    """Line is a collection of tiles
        Line is responsible for updating bots in lines,
        while Tile is responsible for updating bots not
        in the line
        """

    def __init__(self,booth_name,tiles, wait_time):
        """booth_name: name of the booth
            tiles: list of tiles that constitute the line
            """
        self.booth_name = booth_name
        self.tiles = tiles
        for tile in tiles:
            tile.put_into_line(self)
        self.last_tile_index = 0
        self.time_left = wait_time

    def add_bot(self,bot):
        self.tiles[last_tile_index].add_bot(bot,True)

    def compute_step:
        # we don't really have to compute anything
        # since for now we assume that progress for
        # talking to recruiter is independent of
        # local population density

    def execute_step(self):
        for tile in self.tiles:
            tile.compute_step()

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
        if bot.empty_line() and last_tile_index != 0:
            self.last_tile_index--;
