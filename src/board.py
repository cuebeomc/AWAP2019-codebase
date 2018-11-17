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

            for i in range(0, rows):
                for j in range(0, cols):
                    char = line[i][j]
                    if char == "X":
                        pass
                    elif char == "F":
                        pass
                    elif len(char) < 1:
                        raise Exception("Got empty spot at", i, j)
                    elif char[0].isnumeric():
                        # we have a line
                        max_line = max(int(char[0]), max_line)
                    elif char[0] == "C":
                        max_comp = max(int(char[1:]), max_comp)
                    elif char[0] == "E":
                        max_line = max(int(char[1:]), max_line)
                    else:
                        raise Exception("Unknown tile char at", i, j)

            if max_comp != max_line:
                raise Exception("Max company and max lines don't match, got",
                  max_comp, max_line)

            # create all lines

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
                    elif char == "":
                        raise Exception("Got empty spot")
                    elif char[0].isnumeric():
                        pass
                    elif char[0] == "C":
                        pass
                    elif char[0] == "E":
                        pass

            self.board = board
