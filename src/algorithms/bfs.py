from collections import deque

class BFS(object):

    def get_neighbors(loclayer, board):
        """
        Gets the neighbors of the current location layer, where loclayer
        stores both the current x and y coordinates and the layer in the BFS.

        Returns the list of valid neighbors, with properly updated layers
        """
        l = []
        x, y = loclayer[0].get_location()
        layer = loclayer[1]
        if x + 1 < len(board):
            l.append((board[x+1][y], layer + 1))
        if x - 1 >= 0:
            l.append((board[x - 1][y], layer + 1))
        if y + 1 < len(board[x]):
            l.append((board[x][y + 1], layer + 1))
        if y - 1 >= 0:
            l.append((board[x][y - 1], layer + 1))
        return l

    def bfs(tile, board, p):
        """
        Conducts a general BFS to search for the nearest object which
        satisfies the condition p.

        tile: Tile
        Board: numpy.ndarray of size (r, c)
        p: Tile -> bool

        returns a tuple of the shortest distance to the Tile
        and the Tile object itself.
        """
        r, c = board.shape

        marked_board = [[False for _ in range(c)] for _ in range(r)]
        start_loc = (tile,0)

        queue = deque([start_loc])

        shortest_distance = r*c # an upper bound
        nearest_object = None

        while queue: # returns true if non-empty
            elem = queue.popleft()
            pop_tile = elem[0]
            x, y = pop_tile.get_location()
            if marked_board[x][y]: # don't reuse locations
                continue
            marked_board[x][y] = True

            layer = elem[1]
            if layer < shortest_distance and p(pop_tile):
                shortest_distance = layer
                nearest_object = pop_tile

            neighbors = get_neighbors(pop_tile, board)
            for neighbor in neighbors:
                queue.append(neighbor)


        return nearest_object
