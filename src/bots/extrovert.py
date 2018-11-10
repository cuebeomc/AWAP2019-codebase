import src.Bot as Bot

'''
    ExtrovertBot find the position in the map where there are the most amount
    of people.
'''
class ExtrovertBot(Bot):

    ''' We add this value to the population of the neighborhood tiles when
        deciding whether or to the change the destination tile to a different
        adjacent tile. This is added just in case our ExtrovertBot changes
        directions too often and ultimately does not move. Increase this
        value to ensure the bot moves more, decrese this value so that
        its more purely an extrovert.

        Example:
        Set this to zero if you always want to change your destination tile
        to the neighboring location with the most people.

        Example:
        Set this to one if one of the neighboring locations needs two more
        people on it for this bot the change their direction.
    '''
    reorient_cost = 2

    def find_most_people(self,board):
        curx,cury = tile.getLocation()
        neighbors = []
        if curx < len(board) - 1:
            neighbors.append(board[curx + 1][cury])
        if curx > 0:
            neighbors.append(board[curx - 1][cury])
        if cury < len(board[curx]) - 1:
            neighbors.append(board[curx][cury + 1])
        if cury > 0:
            neighbors.append(board[curx][cury - 1])
        most_populated_tile = neighbors[0]
        for i in range(1, len(neighbors)):
            if (most_populated_tile.getPopulation() < neighbors[i].getPopulation()):
                most_populated_tile = neighbors[i]
        return most_populated_tile

    def compute_step(self, board):
        most_populated_tile = find_most_people(self,board)
        if (dest_tile == None or
            most_populated_tile.getPopulation() + reorient_cost > dest_tile.getPopulation()):
            dest_Tile = most_populated_tile
