from .board import Board

class Game(object):
    def __init__(self, config_file, companies, multiplayer, debug):
        """Initialize a game instance."""
        self.multiplayer = multiplayer
        self.board = Board(config_file, companies, debug)
        self._copy()
        (self.board).init_bots(multiplayer)

    def _copy(self):
        """Copies the given board into a basic grid for player use."""
        grid = self.board.grid
        new_grid = []
        for row in grid:
            new_row = []
            for tile in row:
                new_tile = tile.copy()
                new_tile.end_of_line = False
                new_row.append(new_tile)
            new_grid.append(new_row)
        self.basic_grid = new_grid

    def generate_player_copy(self, team=0, init=False):
        """Uses the basic grid and the visible locations to generate a new
        grid with tiles from basic grid if not visible and tiles from the
        board if visible. Should use copied tiles if visible."""
        team_positions = (self.board).get_positions(team)
        visible_locs = (self.board).get_visible_locs(team)
        player_copy = []
        for row in self.board.grid:
            new_row = []
            for tile in row:
                loc = tile.get_loc()
                if loc in visible_locs and not init:
                    new_row.append(tile.copy())
                else:
                    new_row.append((self.basic_grid[loc[0]][loc[1]]).copy())
            player_copy.append(new_row)
        return player_copy, team_positions

    def make_move(self, moves):
        """Update for multiplayer use later."""
        (self.board).step(moves)
        players = 1
        if self.multiplayer:
            players = 2
        return [self.generate_player_copy(i) for i in range(players)]
