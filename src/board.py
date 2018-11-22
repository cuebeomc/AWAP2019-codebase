from tile import Tile, Booth, Line
import numpy as np

class Board(object):
    def __init__(self, length, width):
        self.num_companies = getCompanyNumber(self, file)
        self.board = [][]
        """need to change this implementation -- may have MORE than 1 line per
        booth"""
        self.allLines = []
        self.allBooth = [] #index corresponds to unique company number
        parse()

        """
        Sample configuration file:
        6 8
        X  M4 M4 M4 M5 M5 M5 X
        S1  F  4  F E5  5  5 F
        S1 E1 E4  6  F  F  F F
        S2  2 E2  6  F E6  F X
        S2 E3  3  6  6  6  6 6
        X  S3 S3 L6 L6 L6 L6 X
        """

    def getCompanyNumber(self, file):
        max = 1
        with open(file, 'r') as f:
            dimensions = f.readline().strip().split(' ')
            rows = int(dimensions[0])
            columns = int(dimensions[1])
            if (rows <= 0 or cols <= 0):
                print('Invalid dimensions', file=sys.stderr)
                sys.exit
            try:
                for i in range(rows):
                    line = f.readline().strip().split(' ')
                    if columns != len(line):
                        raise IndexError
                    for j in range(columns):
                        char_val = line[j]
                        if (!char_val.isalpha()) && (!char_val.isdigit()):
                            num = char_val[1]
                            if num >= max:
                                max = num
        return max

    def parse(self, file):
        """
        Parses a configuration file into a matrix.
        File format is as follows:
        First line is of the form M N, where M and N are integers denoting the
        dimensions of the game board.
        The next M lines are of the form x1 x2 ... xN, where the xi are all
        characters denoting the type of element at the specific position in
        board. The characters are:
            S :: small company zone
            M :: medium company zone,
            L :: large company zone
            F :: free tile
            X :: blocked off, unaccessable
        @param file: the config File
        @ensures: rewrite me
        """
        with open(file, 'r') as f:
            dimensions = f.readline().strip().split(' ')
            rows = int(dimensions[0])
            columns = int(dimensions[1])
            checked in getCompanyNumber
            if (rows <= 0 or cols <= 0):
                print('Invalid dimensions', file=sys.stderr)
                sys.exit
            self.board = np.zeros((rows, columns))
            for i in range(rows):
                for j in range(cols):
                    self.board[i][j] = Tile(x, y)
            try:
                for eachCompany in range(self.num_companies):
                    self.allLines.append(Line(str(eachCompany), [], 0))

                    self.allBooths.append(Booth([], , name, wait_time))

                for i in range(rows):
                    line = f.readline().strip().split(' ')
                    if columns != len(line):
                        raise IndexError
                    for j in range(columns):
                        char_val = line[j]
                        if char_val.isalpha():
                            # either F or X
                            pass
                        else if char_val.isdigit():
                            # a line block 1, 2, 3...
                            self.board[i][j].line = # add this tile into the line!

                        else:
                            # S1, M2, or L3 or etc.
                            size = char_val[0]
                            num = char_val[1]
                            # this is end-of-line
                            if size == 'E':
                                self.board[i][j].
                            self.board[i][j].booth = # add this tile into the booth




                        self.board[i][j] = self.tile_classes.get(char)
                        if (self.board[i][j] == None):
                            print('Invalid character {}'.format(char),
                                  file=sys.stderr)
                            sys.exit
            except SystemExit:
                sys.exit
            except (EOFError, IOError, IndexError):
                print('Dimension mismatch', file=sys.stderr)
                sys.exit
