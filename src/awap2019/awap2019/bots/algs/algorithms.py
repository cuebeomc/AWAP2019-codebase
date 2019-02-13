from ...direction import Direction
from random import shuffle

def BFS(board, src, p):
    dirs = [Direction.LEFT, Direction.UP, Direction.RIGHT, Direction.DOWN]

    queue = [[src]]
    visited = set()

    while queue:
        path = queue.pop(0)
        node = path[-1]

        tile = board.get(node)

        if p(tile):
            return path
        if node not in visited:
            visited.add(node)
        else:
            continue

        shuffle(dirs)
        locs = [direction.get_loc(node) for direction in dirs]
        for loc in locs:
            tile = board.get(loc)
            if tile != None and p(tile):
                return list(path) + [loc]
            if tile != None and tile.get_booth() is None:
                new_path = list(path)
                new_path.append(loc)
                queue.append(new_path)
