from board import Board
from direction import Direction
from bot import Bot

b = Board("config.txt")
p1 = Bot(b, (1, 1), 2)
b.player_bots = [[p1]]
b.step([[Direction.LEFT]])
print(p1.progress)
