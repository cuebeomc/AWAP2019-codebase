import numpy as np
import sys
import json

"""
How Board works:

Board will be our core class, hosting booths, lines, free tiles, and bots
We will have 2 parse files: companies and board layout

The board will parse in these two files and construct a numpy array that
can hold the state of our game

The board will be called for run in order to simulate the game

---------------------

        Sample company configuration file:
        6
        <<<Company 1 information>>>
        <<<Company 2 information>>>
        <<<Company 3 information>>>
        <<<Company 4 information>>>
        <<<Company 5 information>>>
        <<<Company 6 information>>>

        Sample board configuration file:
        6 8
        X  C4 C4 C4 C5 C5 C5  X
        C1  F  4  F E5  5  5  F
        C1 E1 E4  F  F  F  F  F
        C2  2 E2  F  F  F  F  X
        C2 E3  3  6  6  6  6 E6
        X  C3 C3 C6 C6 C6 C6  X

        In the board config file, we have the following guide
        X            :: Unaccessable
        F            :: Free space
        [0-9][0-9]*  :: Line for company id #
        C[0-9][0-9]* :: Company booth for company id #
        E[0-9][0-9]* :: End of line for company id #

        For now, lines are one continuous "snake" with a distinct head and tail
"""

class Board(object):
    """
        We need *more* documentation.

        Static Variables:
        tile_classes -- dictionary containing the different tile zones. The
            characters are:
                X :: blocked off, unaccessable  0
                F :: free tile                  1
                C :: company booth zone         2
                L :: line for a company         3

    """
    MAX_COMPANIES = 10
    MAX_ROWS = 100
    MAX_COLS = 100

    def __init__(self, company_config_file, board_config_file):
        """
        Uses a config file to initialize a board

        Keyword Arguments:
        company_config_file
        board_config_file
        """

        # Sets both the number of companies in the board and the board itself
        # type(self.num_companies) = dictionary where each entry has an
        #     integer corresponding to the number of booths it has
        # type(self.board) = numpy.ndarray (2D Array)
        self.board = None
        self.company_infos = []
        self.booths = []
        self.parse(company_config_file, board_config_file)

    def parse(self, company_config_file, board_config_file):
        self.parse_companies(company_config_file)
        self.parse_board(board_config_file)

    def parse_companies(self, file):
        def parse_indv_company(self, s):
            company = json.loads(s)
            return company

        with open(file, 'r') as f:
            num_companies = int(f.readline())
            if num_companies < 1 or num_companies > MAX_COMPANIES:
                raise Exception("Invalid num_companies", num_companies)

            companies = []

            for i in range(0, num_companies):
                companies.append(self.parse_indv_company(f.readline()))

            self.company_infos = companies
        return

    def parse_board(self, file):
        with open(file, 'r') as f:
            dimensions = f.readline().strip().split(' ')
            if len(dimensions) != 2:
                raise Exception("Expecting 2 dimensions", dimensions)

            num_rows = int(dimensions[0])
            num_cols = int(dimensions[1])

            if num_rows < 1 or num_rows > MAX_ROWS:
                raise Exception("num_rows out of range", num_rows,
                  "expect", 1, "to", MAX_ROWS)
            if num_cols < 1 or num_cols > MAX_COLS:
                raise Exception("num_cols out of range", num_cols,
                  "expect", 1, "to", MAX_COLS)

            board = np.zeros((num_rows, num_cols))

            # create all tiles
            for i in range(0, num_rows):
                for j in range(0, num_cols):
                    # TODO: Change from 0
                    board[i][j] = Tile(i, j, 0)

            # copy string for multiple passes
            board_copy = []
            for i in range(0, num_rows):
                line = f.readline().strip().split(' ')
                if num_cols != len(line):
                    raise Exception("Line width does not match row length",
                      len(line), "expect", num_cols, "for line", i)
                board_copy.append(line)

            # create all booths
            max_comp = 0
            max_line = 0
            seen_comp = set()
            seen_lines = set()

            for i in range(0, num_rows):
                for j in range(0, num_cols):
                    char = board_copy[i][j]
                    if char == "X":
                        pass
                    elif char == "F":
                        pass
                    elif len(char) < 1:
                        raise Exception("Got empty spot at", i, j)
                    elif char[0].isnumeric():
                        # we have a line
                        index = int(char)
                        max_line = max(index, max_line)
                        seen_lines.add(index)
                    elif char[0] == "C":
                        index = int(char[1:])
                        max_comp = max(index, max_comp)
                        seen_comp.add(index)
                    elif char[0] == "E":
                        index = int(char[1:])
                        max_line = max(index, max_line)
                        seen_lines.add(index)
                    else:
                        raise Exception("Unknown tile char at", i, j)

            if max_comp != max_line:
                raise Exception("Max company and max lines don't match, got",
                  max_comp, max_line)
            if max_comp > len(self.company_infos):
                raise Exception("Found more company spots than company informations",
                "got", max_comp, "expected at most", len(self.company_infos))
            seen_comp = sorted(list(seen_comp))
            seen_lines = sorted(list(seen_lines))

            if len(seen_comp) < 2 or (seen_comp[0] == 0 and
              seen_comp[-1] == max_comp and len(seen_comp) == max_comp):
                pass
            else:
                raise Exception("Missing company", seen_comp, "max", max_comp)

            if len(seen_lines) < 2 or (seen_lines[0] == 0 and
              seen_lines[-1] == max_lines and len(seen_lines) == max_lines):
                pass
            else:
                raise Exception("Missing lines", seen_lines, "max", max_line)


            # create all lines
            # we reserve the first index for the end
            lines = [[(-1, -1)] for i in range(max_line)]
            booths = [[] for i in range(max_comp)]

            for i in range(0, num_rows):
                for j in range(0, num_cols):
                    char = board_copy[i][j]
                    # should have correctness checked earlier
                    if char[0].isnumeric():
                        index = int(char)
                        lines[index].append((i, j))
                    elif char[0] == "C":
                        index = int(char[1:])
                        booths[index].append((i, j))
                    elif char[0] == "E":
                        index = int(char[1:])
                        if line[index][0][0] != -1 and line[index][0][1] != -1:
                            raise Exception("Multiple line endings for company",
                              index)
                        lines[index][0] = (i, j)

            # formats and sets lines/booths
            # our inputted lists are not well organized
            self.set_booths(booths)
            self.set_lines(lines)

            # set tiles with booths and lines
            for i in range(rows):
                line = f.readline().strip().split(' ')
                if num_cols != len(line):
                    raise Exception("Line width does not match row length",
                      len(line), num_cols)
                for j in range(0, columns):
                    char = line[j]
                    if char == "X":
                        raise Exception("Unmovable spots not implemented")
                    elif char == "F":
                        pass
                    elif char[0].isnumeric():
                        pass
                    elif char[0] == "C":
                        pass
                    elif char[0] == "E":
                        pass

            self.board = board

    def set_booths(self, booths):
        # we have a collection of booth coordinates, we need to find start/end
        def format_booth(booth):
            if len(booth) < 2:
                return booth

            booth_set = set(booth)
            start = (-1, -1)

            i = 0
            while not found and i < len(booth):
                cell = booth[i]
                neighbors = 0
                cell_ll = (cell[0], cell[1] - 1)
                cell_rr = (cell[0], cell[1] + 1)
                cell_dn = (cell[0] + 1, cell[1])
                cell_up = (cell[0] - 1, cell[1])

                if cell_up in booth_set:
                    neighbors += 1
                if cell_dn in booth_set:
                    neighbors += 1
                if cell_rr in booth_set:
                    neighbors += 1
                if cell_ll in booth_set:
                    neighbors += 1

                if neighbors == 0:
                    raise Exception("Got singleton island booth in multiple tiles",
                      booth)
                elif neighbors == 1:
                    start = cell
                    found = True
                elif neighbors == 2:
                    pass
                elif neighbors > 2:
                    raise Exception("Tree based booth structure?", booth)

                i += 1

            start_up = (start[0] + 1, start[1])
            start_dn = (start[0] - 1, start[1])
            start_rr = (start[0], start[1] + 1)
            start_ll = (start[0], start[1] - 1)

            dir = None
            if start_up in booth_set:
                dir = (1, 0)
            elif start_dn in booth_set:
                dir = (-1, 0)
            elif start_rr in booth_set:
                dir = (0, 1)
            elif start_ll in booth_set:
                dir = (0, -1)

            if dir == None:
                raise Exception("Can't find a direction for next block")

            curr = start
            booth_tiles_seen = set([curr])
            res = [curr]
            while curr in booth_set:
                curr = (curr[0] + dir[0], curr[1] + dir[1])
                booth_tiles_seen.add(curr)
                res.append(curr)

            if len(booth_tiles_seen) != len(booth):
                raise Exception("Haven't parsed every line tile",
                  "got", booth_tiles_seen, "expected", booth)

            return res

        self.booths = []
        for indv_booth in booths:
            self.booths.append(format_booth(indv_booth))

    def set_lines(self, lines):
        pass

    def check_if_visible(bot_locs, cur_loc):
        if cur_loc in bot_locs:
            return True
        for bot_loc in bot_locs:
            if bot_loc[0]-1 <= cur_loc[0] <= bot_loc[0]+1
                        and bot_loc[1]-1 <= cur_loc[1] <= bot_loc[1]+1:
                return True
        return False

    def generate_user_board(self):
        num_rows, num_cols = self.board.shape
        player_bot_locations = get_player_bot_locations() ##NEED TO FIX
        ###USE GETTER FUNCTION FROM BOARD CLASS TO GET BOT LOCALS
        visible_board = np.zeros((num_rows, num_cols))
        if self.board is None:
            return None

        for row in range(num_rows):
            for col in range(num_cols):
                cur_tile = self.board[row][col]
                cur_tile_loc = cur_tile.get_location()
                visible_board[row][col] = UserTile(row,col)
                new_user_tile = visible_board[row][col]
                if cur_tile.is_booth(): #check if current tile is a booth
                    new_user_tile.set_booth(True)
                if check_if_visible(player_bot_locations, tile.get_location()):
                    #checks if the tile should be visible to user
                    new_user_tile.set_visibility(True)
                if new_user_tile.get_visibility():
                    new_user_tile.set_bots_in_line(cur_tile.get_bots_in_line())
                    new_user_tile.set_bots(cur_tile.get_bots())
                    new_user_tile.set_end_of_line(cur_tile.get_end())##
                    new_user_tile.set_line(cur_tile.get_line())
        return visible_board
