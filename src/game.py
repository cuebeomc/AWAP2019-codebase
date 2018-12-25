from board import Board

class Game(object):
    def __init__(self, file, multiplayer=False):
        """Initialize a game instance."""
        self.board = Board(file)
        self._copy()
        board.init_bots(multiplayer)

    def _copy(self):
        grid = self.board.grid
        new_grid = []
        for row in grid:
            new_row = []
            for tile in row:
                new_tile = tile.copy()
                new_tile.end_of_line = False
            new_grid.append(new_row)
        self.basic_grid = new_grid

    def generate_player_copy(self, team):
        visible_locs = (self.board).get_visible_locs(team)
        player_copy = []
        for row in self.board.grid:
            new_row = []
            for tile in row:
                loc = tile.get_loc()
                if loc in visible_locs:
                    new_row.append(tile)
                else:
                    new_row.append(self.basic_grid[loc[0]][loc[1]])
            player_copy.append(new_row)
        return player_copy

    def make_move(self, moves):
        return 0
