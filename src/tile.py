class Tile(object):

    MAX_PEOPLE_IN_LINE = 10

    def __init__(self,x,y,dx,dy):
        self.bots_in_line = []
        self.bots_not_in_line = []
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.end_of_line = false

    #moves all the bots in the line.
    def step():
        """ Represents movement after a single time step. """
        for bot in bots_in_line:
            bot.step(move_dampening())   #
        for bot in bots_not_in_line:
            bot.step(move_dampening())

    def add_bot(bot, to_line):
        if to_line:
            bots_in_line.append(bot)
        else:
            bots_not_in_line.append(bot)

    def empty_line():
        """True if no bots in line at this tile."""
        return len(bots_in_line) == 0

    def line_max_capacity():
        """ True if the number of bots in line is at the max. """
        return len(bots_in_line) == MAX_PEOPLE_IN_LINE

    def get_num_in_line():
        """ Return the number of bots in the line at this tile. """
        return len(bots_in_line)

    def pop_line():
        """ Kick the bot at the front of the line at this tile
        *(Not responsible for stepping the kicked bot!!!
        """
        bots_in_line.pop(0)

    #Moves bots a certain amount based on the number of bots in and out of line
    def move_dampening():
        return int(Math.log(2 * len(bots_in_line) + 3 * len(bots_not_in_line)))

#represents a block of tiles that are a booth. References 1 or 2 lines.
class Booth():

    def __init__(self, positions, name,lines):
        self.positions = positions
        self.name = name
        self.lines = lines




#handle people leaving in the middle
class Line():

    def __init__(self,positions,dx,dy,booth_name,tiles):
        self.positions = positions
        self.dx = dx
        self.dy = dy
        self.booth_name = booth_name
        self.tiles = tiles

    def add_bot():

    def move_up():
        index = 0
        kicked_bot = tiles[index].pop_line()
        kicked_bot.step() # note step needs to handle moving after getting out of line
        index++
        while (index < len(tiles)):
            lucky_bot = tiles[index].pop_line()
            tiles[index - 1].add_bot(lucky_bot, True)
            index++

    def extend_line():
