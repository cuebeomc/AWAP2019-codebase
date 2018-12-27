# THINGS TO DO

# Add bot replacement technique for players
# Make an overall game sequence in game.py
# Add scoring mechanism

# Check and debug code!!

from tile import Tile, Booth, Line
from bot import Bot
import numpy as np

import random

class Board(object):
    """
    Sample configuration file:
    6 8 6
    F  M3 M3 M3 M4 M4 M4 F
    S0  0 E0  3 E5  4  F F
    S0 E1 E2  3  5  4  F F
    S1  1  2  3  5  4  F B
    S1  F  2 E3  5 E4  F F
    F  S2 S2 L5 L5 L5 L5 F
    """
    def __init__(self, config_file, company_file):
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
        self.dim = (None, None)
        self.company_list = {'S': set(), 'M': set(), 'L': set()}

        self.player_bots = []
        self.bots = []
        self.players = 1
        self.start = None

        self._parse_companies(company_file)
        self._parse(config_file)

    def init_bots(self, multiplayer):
        """Places the bots onto the board.

        NOTE: I plan on adding unique ID's to each bot, especially each player
        bot to make visualization easier."""
        if multiplayer:
            self.players = 2
        # Do the initialization of multiple bots/place them!
        for i in range(self.players):
            # First bot in this list is main bot by standard.
            # No scoring mechanism has been created yet to prioritize first bot.
            # Will be done when UID's are added as well.
            team_i = [Bot(self, self.start, 2) for _ in range(3)]
            (self.player_bots).append(team_i)

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

        self._update_board()

    def get_visible_locs(self, team):
        """Gets the visible locations for the specified team."""
        visible_locs = set()
        team_bots = self.player_bots[team]
        for bot in team_bots:
            x, y = bot.get_loc()
            for i in [x-1, x, x+1]:
                for j in [y-1, y, y+1]:
                    if 0 <= i < self.dim[0] and 0 <= j < self.dim[1]:
                        visible_locs.add((i, j))
        return list(visible_locs)

    def get_positions(self, team):
        """Gets the positions of the bots in the team."""
        team_bots = self.player_bots[team]
        return [bots.get_loc() for bots in team_bots]

    def _update_board(self):
        """Updates the thresholds."""
        for row in self.grid:
            for tile in row:
                tile.update_threshold()

    def _parse_companies(self, file_path):
        """Parses the company file."""
        file = open(file_path, "r")
        for line in file:
            split_line = line.split()
            company, size = split_line[0], split_line[1]
            self.company_list[size].add(company)

    def _pick_company(self, size):
        """Picks a company from the list of all companies."""
        companies = self.company_list[size]
        if len(companies) < 0:
            raise "Not enough companies"
        chosen = random.sample(companies, 1)[0]
        companies.remove(chosen)
        return chosen

    def _random_time(self, size):
        """Picks a random time. Currently 10, will change if we decide to add
        random times."""
        return 10

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
                    elif letter == 'B':
                        self.start = (r, c)
                    elif letter != 'F':
                        number = int(tile)
                        curr_line = line_tiles[number]
                        curr_line.append(self.grid[r][c])
                    c += 1
                r += 1
        for size, b_tiles, l_tiles in zip(sizes, booth_tiles, line_tiles):
            name = self._pick_company(size)
            time = self._random_time(size)
            (self.booths).append(Booth(name, size, b_tiles, l_tiles, time))
