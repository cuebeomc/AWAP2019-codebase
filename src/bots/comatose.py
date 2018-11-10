import src.Bot as Bot
import random

''' ComatoseBot does exactly what it sounds like, it doesnt like to move around
    so theres a low probability it decides to get off its ass and goes somewhere
'''
class ComatoseBot(Bot):

    motivation_probability = 0.0001

    '''
        motivation_probability = chance that the comatose bot
        decides to actually move out of the current tile at a
        given time step_gain, and it moves in a random cardinal direction
    '''

    def compute_step(self, board):
        curx, cury = tile.getLocation() # idk
        if (dest_tile != None and random.random() < motivation_probability)):
            if (random.random() < 0.5):
                if (random.random() < 0.5):
                    if cury < len(board[curx]) - 1:
                        dest_tile = board[curx][cury + 1]
                else:
                    if cury > 0:
                        dest_tile = board[curx][cury - 1]
            else:
                if (random.random() < 0.5):
                    if curx < len(board) - 1:
                        dest_tile = board[curx + 1][cury]
                else:
                    if curx > 0:
                        dest_tile = board[curx - 1][cury]
