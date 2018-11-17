import src.Bot as Bot
import algorithms.BFS

'''nervous people waits in the line until they reach the recruiter, but
leaves the line after that because they don't want to talk to the recruiter'''

def is_at_end(self, board):
    x, y = tile.getLocation()
    if (x < len(board) - 1):
        # checks if that is line end
        if (board[x + 1][y].is_end()):
            return true;
    if (x > 0):
        if (board[x - 1][y].is_end()):
            return true;
    if (y < len(board[curx]) - 1):
        if (board[x][y + 1].is_end()):
            return true;
    if (y > 0):
        if (board[x][y - 1].is_end()):
            return true;
    return false;

def find_next_booth(self, board):
    (dis, obj) = bfs(self, board, is_line())
    return obj


def compute_step(self, board):
    if (is_at_end(self, board)):
        dest_tile = find_closest_booth()

    else:
        dest_tile = obj
