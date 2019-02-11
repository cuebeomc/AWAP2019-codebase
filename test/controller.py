import numpy as np

class Controller(object):
    def __init__(self, teams, dim, lines, direction):
        self.bots = []
        self.dim = dim
        self.map = np.empty((dim[1], dim[0]), dtype=object)
        for n in teams:
            team = [Bot() for _ in range(n)]
            if team:
                self.bots.append(team)
        
        for i in range(dim[1]):
            for j in range(dim[0]):
                if (i, j) in lines:
                    c, lp = lines[(i, j)]
                self.map[i][j] = Tile(i, j, direction[c], lp)
    
    def parse_bot_state(self, status):
        tid, uid, x, y, state, p, t, lp = status
        self.bots[tid][uid].set_state(x, y, state, p, t, lp)

class Bot(object):
    def __init__(self):
        self.loc = None
        self.state = None
        self.line_pos = None
        self.visualizer_loc = None
    
    def set_state(self, x, y, state, p, t, lp):
        self.loc = (x, y)
        self.state = state
        self.progress = (p, t)
        self.line_pos = lp

class Tile(object):
    def __init__(self, x, y, direction=None, line_pos=None, side=3):
        self.direction = direction
        self.line_pos = line_pos
        self.length = side
        self.loc = (x, y)
        self.positions = [0 for _ in range(side * side)]
    
    def get_visual_pos(self, num):
        x = num % self.length
        y = num / self.length
        return ()