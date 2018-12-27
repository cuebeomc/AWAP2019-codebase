from direction import Direction
from game import Game

g = Game("config.txt", "companies.txt")

moves = [Direction.LEFT, Direction.UP, Direction.RIGHT]
for booth in g.board.booths:
    print(booth.name)
for i in range(100):
    visible_board = g.make_move([moves])
    player_board, positions = visible_board[0]
    print(positions)
