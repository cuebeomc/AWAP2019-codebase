from .board import Board

class Game(object):
    def __init__(self, config_file, companies, log_file, multiplayer=False, debug=False, team_size=4):
        """Initialize a game instance."""
        self.players = 2 if multiplayer else 1
        self.board = Board(config_file, companies, log_file, debug, team_size,
            2 if multiplayer else 1)
        self._copy()
        (self.board).init_bots()

        self.scoreboard = [0] * self.players

    def get_companyinfo(self):
        return self.board.company_info

    def _copy(self):
        """Copies the given board into a basic grid for player use."""
        grid = self.board.grid
        new_grid = []
        for row in grid:
            new_row = []
            for tile in row:
                new_tile = tile.copy()
                new_tile.end_of_line = False
                new_tile.visible = False
                new_row.append(new_tile)
            new_grid.append(new_row)
        self.basic_grid = new_grid

    def generate_player_copy(self, team=0, init=False):
        """Uses the basic grid and the visible locations to generate a new
        grid with tiles from basic grid if not visible and tiles from the
        board if visible. Should use copied tiles if visible."""
        visible_locs = (self.board).get_visible_locs(team)
        player_copy = []
        for row in self.board.grid:
            new_row = []
            for tile in row:
                loc = tile.get_loc()
                if loc in visible_locs and not init:
                    new_row.append(tile.copy())
                else:
                    obj = (self.basic_grid[loc[0]][loc[1]]).copy()
                    new_row.append(obj)
            player_copy.append(new_row)
        return player_copy

    def make_move(self, moves):
        """Update for multiplayer use later."""
        updated_scores = (self.board).step(moves)
        for i, score in enumerate(updated_scores):
            self.scoreboard[i] += score

        return [(self.generate_player_copy(i), (self.board).get_states(i),
                self.scoreboard[i]) for i in range(self.players)]
