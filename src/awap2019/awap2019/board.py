# THINGS TO DO

# Write proper threshold formula and add working crowd (make bots)

# Check and debug code!!


from .tile import Tile, Booth, Line
from .bots import *
from .state import State
from .direction import Direction
import numpy as np

import random

class Board(object):

    wait_time = 1
    major_reward = 10
    minor_reward = 5
    visible_range = 2

    # add constants regarding main player + min player scores?

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
    def __init__(self, config_file, company_file, log_file, debug, team_size, num_players):
        """Initializes the Board class.

        grid: Grid of tiles
        booths: The booth objects on the grid.
        players: The number of players playing on this board instance.
        player_bots: The bots associated with each player. Each element is
                     a list of 4 bots that correlate to its index's player #.
        dim: The dimensions of the board.
        """
        self.time_step = 0
        self.log_file = log_file
        self.team_size = team_size

        self.grid = []
        self.booths = dict()
        self.dim = (None, None)
        self.company_list = {'S': set(), 'M': set(), 'L': set()}
        self.chosen_companies = set()

        self.player_bots = []
        self.bots = []
        self.players = num_players
        self.start = None

        self.company_values = {}
        self.company_info = {}

        self._parse_companies(company_file)
        self._parse(config_file)

        self.debug = debug

        # 2 players at most
        self.scores = [0] * self.players
        self.rewards = [self.company_values.copy() for _ in range(self.players)]

    def dbg_print(self, str):
        if self.debug:
            print(str)

    def init_bots(self):
        """Places the bots onto the board."""
        # Do the initialization of multiple bots/place them!
        for i in range(self.players):
            # First bot in this list is main bot by standard.
            team_i = []
            for j in range(self.team_size):
                team_i.append(Bot(self, self.start, 1, j, team_id=i))
            (self.player_bots).append(team_i)

        # TODO: Initialize the crowd!

        start_id = 0
        for i in range(0, self.num_bots//10):
            num = i * 10
            self.bots.append(JitteryBot(self, self.start, 1, num))
            num += 1
            self.bots.append(JitteryBot(self, self.start, 1, num))
            num += 1
            self.bots.append(JitteryBot(self, self.start, 1, num))
            num += 1
            self.bots.append(ExtrovertBot(self, self.start, 1, num))
            num += 1
            self.bots.append(RandomBot(self, self.start, 1, num, "S"))
            num += 1
            self.bots.append(RandomBot(self, self.start, 1, num, "M"))
            num += 1
            self.bots.append(RandomBot(self, self.start, 1, num, "L"))
            num += 1
            self.bots.append(RandomBot(self, self.start, 1, num, "L"))
            num += 1
            self.bots.append(RandomBot(self, self.start, 1, num))
            num += 1
            self.bots.append(RandomBot(self, self.start, 1, num))
        #for i in range(start_id, start_id + 5):
            #self.bots.append(JitteryBot(self, self.start, 1, i))

        self._log('w')

    def x_dim(self):
        return self.dim[0]

    def y_dim(self):
        return self.dim[1]

    def get(self, loc):
        """Gets the tile at loc."""
        if 0 <= loc[0] < self.dim[0] and 0 <= loc[1] < self.dim[1]:
            return self.grid[loc[0]][loc[1]]
        else:
            return None

    # Note: you can only replace a main bot with a helper bot.
    # (Replacing a helper with a helper is functionally useless.)
    def step(self, team_moves):
        """Updates the whole board by one step."""
        for bot in self.bots:
            bot.compute_step()
        for team, moves in zip(self.player_bots, team_moves):
            if moves[0] == Direction.REPLACE:
                self.dbg_print("Replacing!")
                swap_index = -1
                invalid = False

                main_loc = team[0].get_loc()
                for i in range(1, self.team_size):
                    bot_loc = team[i].get_loc()
                    if moves[i] == Direction.REPLACE and bot_loc == main_loc:
                        if swap_index == -1:
                            self.dbg_print("Found the bot to replace with.")
                            swap_index = i
                        else:
                            self.dbg_print("Found another one; replace is invalid.")
                            moves[i] = Direction.NONE
                            invalid = True
                    elif moves[i] == Direction.REPLACE:
                        self.dbg_print("Found a replace not on the same location.")
                        moves[i] = Direction.NONE

                moves[0] = Direction.NONE
                if swap_index != -1:
                    moves[swap_index] = Direction.NONE
                    if not invalid:
                        self._swap(team, swap_index)
            self.dbg_print("Team: {}".format(team))
            self.dbg_print("New moves: {}".format(moves))

            for bot, move in zip(team, moves):
                bot.set_new_direction(move)

        for bot in self.bots:
            bot.execute_step()

        for team in self.player_bots:
            for bot in team:
                bot.execute_step()

        talked_booths = []
        for name in self.booths:
            booth = self.booths[name]
            val = booth.execute_step()
            if val:
                talked_booths.append(val)
        updated_scores = self._score(talked_booths)

        self.dbg_print(np.matrix(self.grid))
        self._update_board()
        self._log('a+')

        self.scores = updated_scores

        return updated_scores

    def _swap(self, arr, index):
        """Swaps bot at index 0 with bot at index index in arr."""
        arr[0], arr[index] = arr[index], arr[0]

        temp_id = arr[0].get_id()
        arr[0].set_id(arr[index].get_id())
        arr[index].set_id(temp_id)

    def _score(self, talked):
        scores = [0] * self.players
        for name, team_id, id in talked:
            # Change these values to add prioritization for
            # certain companies!
            reward_dict = self.rewards[team_id]
            (major, minor) = reward_dict[name]
            if id == 0:
                scores[team_id] += major
            else:
                scores[team_id] += minor
            reward_dict[name] = (major//2, minor//2)
        return scores

    def get_visible_locs(self, team):
        """Gets the visible locations for the specified team."""
        visible_locs = set()
        team_bots = self.player_bots[team]
        for bot in team_bots:
            x, y = bot.get_loc()
            for i in range(x-self.visible_range, x+self.visible_range+1):
                for j in range(y-self.visible_range, y+self.visible_range):
                    if 0 <= i < self.dim[0] and 0 <= j < self.dim[1]:
                        visible_locs.add((i, j))
        return list(visible_locs)

    def get_states(self, team):
        """Gets the states of the bots in the team."""
        team_bots = self.player_bots[team]
        return [State(bot) for bot in team_bots]

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
            company, size, value = split_line[0], split_line[1], int(split_line[2])
            self.company_list[size].add((company, value))

    def _pick_company(self, size):
        """Picks a company from the list of all companies."""
        companies = self.company_list[size]
        if len(companies) <= 0:
            raise Exception("Not enough companies for {}".format(size))
        chosen = random.sample(companies, 1)[0]
        companies.remove(chosen)
        self.chosen_companies.add(chosen)
        return chosen

    def _random_time(self, size):
        """Picks a random time. Currently 5, will change if we decide to add
        random times."""
        return Board.wait_time

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
                self.grid = np.empty(self.dim, dtype=object)
                for i in range(self.dim[0]):
                    #row = []
                    for j in range(self.dim[1]):
                        self.grid[i][j] = Tile(i, j)
                        #row.append(Tile(i, j))
                    #(self.grid).append(row)
                num_companies = int(dims[2])
                self.num_bots = int(dims[3])
                self.visible_range = int(dims[4])
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

        #print(len(list(filter(lambda x: x == "S", sizes))))
        #print(len(list(filter(lambda x: x == "M", sizes))))
        #print(len(list(filter(lambda x: x == "L", sizes))))

        for size, b_tiles, l_tiles in zip(sizes, booth_tiles, line_tiles):
            name, value = self._pick_company(size)
            self.company_info[name] = value
            self.company_values[name] = (value, value//2)
            time = self._random_time(size)
            (self.booths)[name] = Booth(name, size, b_tiles, l_tiles, time, value)

    def _log(self, mode):
        with open(self.log_file, mode) as log:
            if mode == 'w':
                team2 = self.team_size if self.players == 2 else 0
                log.write("{} {} {}\n".format(self.team_size, team2,
                                              len(self.bots)))
                for company in self.chosen_companies:
                    log.write("{}\n".format(company))
                log.write("\n")

            log.write("{} {} {}\n".format(self.time_step, self.scores[0], self.scores[1] if self.players > 1 else 0))
            for team in self.player_bots:
                for bot in team:
                    log.write("{}\n".format(State(bot).get_num_encoding()))
            for bot in self.bots:
                log.write("{}\n".format(State(bot).get_num_encoding()))
        self.time_step += 1
