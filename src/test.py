from direction import Direction
from game import Game

g = Game("config.txt", "companies.txt")

moves = [Direction.NONE, Direction.NONE, Direction.NONE]
for booth in g.board.booths:
    print(booth.name)
for i in range(100):
    user_input = input("Movement: ")
    if user_input == 'left':
        moves = [Direction.LEFT] * 3
    elif user_input == 'right':
        moves = [Direction.RIGHT] * 3
    elif user_input == 'up':
        moves = [Direction.UP] * 3
    elif user_input == 'down':
        moves = [Direction.DOWN] * 3
    elif user_input == 'enter':
        moves = [Direction.ENTER] * 3
    else:
        moves = [Direction.NONE] * 3

    visible_board = g.make_move([moves])
    player_board, positions = visible_board[0]
    print(positions)
