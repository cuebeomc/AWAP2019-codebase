# THINGS TO DO

# Add company picker/randomizer
# Add bot replacement technique for players
# Make an overall game sequence in game.py
# Add scoring mechanism

# ADD TYPECHECK AND INPUT CHECKING MECHANISMS
# MAKE SURE NO MALICIOUS CODE CAN KILL THE GAME

# Check and debug code!!

from tile import Tile, Booth, Line
import numpy as np

class Board(object):
    """
    Sample configuration file:
    6 8 6
    F  M3 M3 M3 M4 M4 M4 F
    S0  0 E0  3 E5  4  F F
    S0 E1 E2  3  5  4  F F
    S1  1  2  3  5  4  F F
    S1  F  2 E3  5 E4  F F
    F  S2 S2 L5 L5 L5 L5 F
    """
    def __init__(self, file):
        """Initializes the Board class.

        grid: Grid of tiles
        booths: The booth objects on the grid.
        players: The number of players playing on this board instance.
        player_bots: The bots associated with each player. Each element is
                     a list of 4 bots that correlate to its index's player #.
        dim: The dimensions of the board.
        """
        self.grid = []
        self.booths = []
        self.players = 1
        self.player_bots = []
        self.bots = []
        self.dim = (None, None)
        self._parse(file)

    def init_bots(self, multiplayer):
        """Places the bots onto the board."""
        if multiplayer:
            self.players = 2
        # Do the initialization of multiple bots/place them!
        # Initialize the player bots!

    def x_dim(self):
        return self.dim[0]

    def y_dim(self):
        return self.dim[1]

    def get(self, loc):
        """Gets the tile at loc."""
        return self.grid[loc[0]][loc[1]]

    def step(self, team_moves):
        """Updates the whole board by one step."""
        for bot in self.bots:
            bot.compute_step()
        for team, moves in zip(self.player_bots, team_moves):
            for bot, move in zip(team, moves):
                bot.set_new_direction(move)

        for bot in self.bots:
            bot.execute_step()
        for team in self.player_bots:
            for bot in team:
                bot.execute_step()
        for booth in self.booths:
            booth.execute_step()

    def get_visible_locs(self, team):
        visible_locs = set()
        team_bots = self.player_bots[team]
        for bot in team_bots:
            x, y = bot.get_loc()
            for i in [x-1, x, x+1]:
                for j in [y-1, y, y+1]:
                    if 0 <= i < self.dim[0] and 0 <= j < self.dim[1]:
                        visible_locs.add((i, j))
        return list(visible_locs)

    def _parse(self, file_path):
        """Parses a config file into a grid of tiles and booths."""
        file = open(file_path, "r")

        first_line = True
        r = 0
        sizes = []
        booth_tiles = []
        line_tiles = []

        for line in file:
            if first_line:
                dims = line.split()
                self.dim = (int(dims[0]), int(dims[1]))
                for i in range(self.dim[0]):
                    row = []
                    for j in range(self.dim[1]):
                        row.append(Tile(i, j))
                    (self.grid).append(row)
                num_companies = int(dims[2])
                sizes = [None] * num_companies
                booth_tiles = [[] for _ in range(num_companies)]
                line_tiles = [[] for _ in range(num_companies)]
                first_line = False
            else:
                c = 0
                tiles = line.split()
                for tile in tiles:
                    letter = tile[0]
                    if letter == 'S' or letter == 'M' or letter == 'L':
                        number = int(tile[1:])
                        if not sizes[number]:
                            sizes[number] = letter
                        curr_booth = booth_tiles[number]
                        curr_booth.append(self.grid[r][c])
                    elif letter == 'E':
                        number = int(tile[1:])
                        curr_line = line_tiles[number]
                        curr_line.insert(0, self.grid[r][c])
                    elif letter != 'F':
                        number = int(tile)
                        curr_line = line_tiles[number]
                        curr_line.append(self.grid[r][c])
                    c += 1
                r += 1
        for size, b_tiles, l_tiles in zip(sizes, booth_tiles, line_tiles):
        #    name = pick_company()
        #    time = random_time(size)
            name = "test"
            time = 5
            (self.booths).append(Booth(name, size, b_tiles, l_tiles, time))

        return
