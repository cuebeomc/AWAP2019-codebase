import src.Bot as Bot
import src.algorithms.BFS

class VanillaBot(Bot):

    def booth_wrapper(tile):
        return tile.is_booth()

    def find_closest_booth(self,board):
        """
        find the closest booth in the neighbors. Make sure it's not visited already
        use BFS.
        """
        self.closest = BFS.bfs(self.tile, board, booth_wrapper)
        return self.closest

    def if_visited(self, tile):
        if tile in visited_list:
            return True
        return False

    def compute_step(self, tile, board):
        dest = get_small_company(tile, board)
        if self.dest_tile == self.get_location():
            append(self.visited_list, tile)
            self.dest_tile = None
        if dest is None:
            self.dest_tile = dest
