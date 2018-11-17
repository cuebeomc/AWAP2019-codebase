import src.Bot as bot
import src.algorithms.bfs as search

class RealisticBot(Bot):

    """
    Realisticbot aims for the smaller companies because it has the best
    chance of getting a job from a smaller company. It will not visit the
    same company twice, because there is no point in handing a resume out
    twice so it will mark the companies it has visited. It uses a bfs to
    search for the closest small company and move towards that direction.
    It should find a company and retrieve the path.
    """

    def if_visited(self, tile):
        if tile in visited_list:
            return True
        return False

    def is_small_company(self, tile):
        if tile.size == small_company_size:
            return True
        return False

    def get_small_company(self, tile, board):
        return search.bfs(tile, board, is_small_company)

    def compute_step(self, tile, board):
        dest = get_small_company(tile, board)
        if self.dest_tile == self.get_location():
            append(self.visited_list, tile)
            self.dest_tile = None
        if dest is None:
            self.dest_tile = dest
