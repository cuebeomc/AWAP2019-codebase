from direction import Direction
from game import Game

g = Game("config.txt", "companies.txt")

team_size = 13
moves = [Direction.NONE, Direction.NONE, Direction.NONE]
for booth in g.board.booths:
    print(booth.name)
for i in range(100):
    user_input = input("Movement: ")
    if user_input == 'left':
        moves = [Direction.LEFT] * team_size
    elif user_input == 'right':
        moves = [Direction.RIGHT] * team_size
    elif user_input == 'up':
        moves = [Direction.UP] * team_size
    elif user_input == 'down':
        moves = [Direction.DOWN] * team_size
    elif user_input == 'enter':
        moves = [Direction.ENTER] * team_size
    else:
        moves = [Direction.NONE] * team_size

    visible_board = g.make_move([moves])
    player_board, positions = visible_board[0]
    print(positions)
