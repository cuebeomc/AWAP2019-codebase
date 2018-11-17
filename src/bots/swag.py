from .. import Bot
from .. import algorithms as alg

class SwagBot(Bot):

    """
    Swagbot aims for the big companies because it wants to get cool swags and
    big companies usually have great swags. It also wants  multiple swags so
    it won't visit the same company, so it will mark the companies it already
    visited. It uses a bfs to search for the closest big company and move
    towards that direction. it should find a company and retrieve the path
    """

    """
    TO DO: access the information about the size of the company
    """
    def if_visited(self,tile):
        if tile not in self.visited_list:
            return 0
        else:
            return 1
    def if_big_company(self,tile):
        big_company_size = 3
        if tile.size == big_company_size:
            return 1
        else:
            return 0

    def find_big_company(self,board):
        return alg.BFS.bfs(self.get_location(), board, if_big_company)

    def compute_step(self,board):
        dest = find_big_company(board)
        if self.dest_tile == self.get_location():
            append(self.visited_list, tile)
            self.dest_tile = None
        if dest is None:
            self.dest_tile=dest
