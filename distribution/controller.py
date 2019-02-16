import numpy as np
import random

class Controller(object):
    def __init__(self, teams, dim, lines, direction):
        self.step = 0
        self.bots = []
        self.dim = dim
        self.map = np.empty((dim[1], dim[0]), dtype=object)
        self.lines = lines
        for bots in teams:
            team = []
            for _ in bots:
                team.append(Bot(self))
            self.bots.append(team)
        
        for i in range(dim[1]):
            for j in range(dim[0]):
                d = None
                pos = None
                if (i, j) in lines:
                    c, lp = lines[(i, j)]
                    d = direction[c]
                    pos = lp
                self.map[i][j] = Tile(i, j, d, pos)
    
    def update(self, step):
        self.step = step
    
    def parse_bot_state(self, status):
        tid, uid, x, y, state, _, _, lp = status
        self.bots[int(tid)][int(uid)].set_state(int(x), int(y), state, int(lp), int(self.step), (int(tid), int(uid))) 
    
    def assign_pos(self, old_pos, new_pos, uid):
        if old_pos:
            self.map[old_pos[0]][old_pos[1]].remove(uid)
        vp = self.map[new_pos[0]][new_pos[1]].assign(uid)
        return vp

    def assign_lp(self, old_pos, new_pos, line_pos, uid):
        self.map[old_pos[0]][old_pos[1]].remove(uid)
        vp = self.map[new_pos[0]][new_pos[1]].assign_lp(uid, line_pos)
        return vp

    def get_bot_positions(self, x, y):
        return self.bots[x][y].positions

class Bot(object):
    def __init__(self, controller):
        self.loc = None
        self.state = None
        self.line_pos = None
        self.time_step = -1
        self.positions = {}
        self.controller = controller

    def set_state(self, x, y, state, lp, time_step, uid):
        vp = None
        if self.time_step != -1:
            if self.loc == (x, y) and self.state == state == "none":
                self.positions[time_step] = None
            elif self.state == state == "inline":
                if self.line_pos == lp:
                    self.positions[time_step] = None
                elif self.line_pos != lp:
                    vp = self.controller.assign_lp(self.loc, (x, y), lp, uid)
            elif state == "inline":
                vp = self.controller.assign_lp(self.loc, (x, y), lp, uid)
            elif self.state == "inline" and state != "inline":
                vp = self.controller.assign_pos(self.loc, (x, y), uid)
            elif self.loc != (x, y):
                vp = self.controller.assign_pos(self.loc, (x, y), uid)
        else:
            self.positions[time_step] = self.controller.assign_pos(None, (x, y), uid)
        
        if vp:
            self.positions[time_step] = vp
        
        self.loc = (x, y)
        self.state = state
        self.line_pos = lp
        self.time_step = time_step

class Tile(object):
    def __init__(self, x, y, direction=None, line_pos=None, side=3):
        self.is_line = line_pos != None
        self.direction = direction
        self.lp_low = 0
        self.lp_high = 0
        if self.is_line:
            self.lp_low = side * line_pos
            self.lp_high = side * (line_pos + 1)
        self.length = side
        self.loc = (x, y)
        self.bots = {}
        self.positions = [0 for _ in range(side * side)]
    
    def remove(self, uid):
        num = self.bots.pop(uid)
        self.positions[num] -= 1
    
    def pick(self, valid_nums):
        num_people = [self.positions[i] for i in valid_nums]
        min_value = min(num_people)

        chooseable = []
        for i, num in enumerate(num_people):
            if num == min_value:
                chooseable.append(valid_nums[i])
        return random.choice(chooseable)

    def assign(self, uid):
        "hardcoded. make sure to change if changing tile size."
        valid_nums = None
        if self.is_line:
            if self.direction == "right" or self.direction == "left":
                valid_nums = [0, 1, 2, 6, 7, 8]
            else:
                valid_nums = [0, 2, 3, 5, 6, 8]
        else:
            valid_nums = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        pos = self.pick(valid_nums)
        self.positions[pos] += 1
        self.bots[uid] = pos

        return self.get_visual_pos(pos)

    def assign_lp(self, uid, line_pos):
        actual_pos = line_pos % self.length
        if self.is_line and not self.lp_low <= line_pos < self.lp_high:
            actual_pos = 2
        num_arr = None
        if self.direction == "right":
            num_arr = [3, 4, 5]
        elif self.direction == "left":
            num_arr = [5, 4, 3]
        elif self.direction == "up":
            num_arr = [7, 4, 1]
        elif self.direction == "down":
            num_arr = [1, 4, 7]
        pos = num_arr[actual_pos]
        self.positions[pos] += 1
        self.bots[uid] = pos
        
        return self.get_visual_pos(pos)
            
    
    def get_visual_pos(self, num):
        dim0 = num // self.length
        dim1 = num % self.length

        return ((3 * self.loc[0]) + dim0 + 0.5 + random.uniform(-0.15, 0.15), (3 * self.loc[1]) + dim1 + 0.5 + random.uniform(-0.15, 0.15))