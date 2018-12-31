"""This is a general template as to how the competitors will code.

They will be given the initial board (the 2D grid of tiles that contain
rudimentary information, allowing them to map out a path that they would like
to take), and at every step, they will be passed in a 2D grid with a board
with more information pertaining to their locations and a list of positions
that is ordered (index 0 contains the main bot's loc, index 1 contains
1st helper's loc, etc)."""

from awap2019 import Tile, Bot, Direction

class Team(object):
    def __init__(self, initial_board, team_size):
        # Feel free to do some work with the initial board!
        self.board = initial_board
        self.team_size = team_size

    def step(self, visible_board, positions, score):
        """This function should return a list of directions. For example,
        [Direction.RIGHT, Direction.LEFT, Direction.NONE]
        indicates that the main bot is told to go right, the first helper
        bot goes left, and the second helper bot does nothing.
        """
        moves = []
        for i in range(self.team_size):
            user_input = input("\nMovement {}: ".format(i))
            if user_input == 'left':
                moves.append(Direction.LEFT)
            elif user_input == 'right':
                moves.append(Direction.RIGHT)
            elif user_input == 'up':
                moves.append(Direction.UP)
            elif user_input == 'down':
                moves.append(Direction.DOWN)
            elif user_input == 'enter':
                moves.append(Direction.ENTER)
            elif user_input == 'replace':
                moves.append(Direction.REPLACE)
            else:
                moves.append(Direction.NONE)
        return moves
