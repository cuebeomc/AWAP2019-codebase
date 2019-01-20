from ...direction import Direction
from ...board import Board

def BFS(board, src, dest):
    dirs = [Direction.LEFT, Direction.UP, Direction.RIGHT, Direction.DOWN]
    queue = [[src]]

    while queue:
        path = queue.pop(0)
        node = path[-1]
        if node == dest:
            return path
        locs = [direction.get_loc(src) for direction in dirs]
        for loc in locs:
            if board.get(loc).get_booth() == None:
                new_path = list(path)
                new_path.append(loc)
                queue.append(new_path)
