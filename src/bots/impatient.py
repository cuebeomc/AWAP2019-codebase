import src.Bot as Bot
import random

'''
    ImpatientBot is a normal bot that will get out of line whenever they've been in line way too long.
'''
class ImpatientBot(Bot):

    ''' We initialize the number of turns in line to be zero. This variable will increase whenever the bot is in line and will increase until either the bot starts talking with the recruiter, or the bot reaches the max_turns in line, at which point it will exit.
    '''
    def __init__(self, position, step_gain, speed, max_turns = random.randint(5, 15)):
        super().__init__(self, position, step_gain, speed)
        self.turns_in_line = 0
        self.max_turns = max_turns
        self.visited_list = []
        self.last_visited = None

    '''
    We want to visit a tile if it is either not in the visited list or not the
    last visited company.
    '''
    def can_visit(self, tile):
        return ((tile not in visited_lsit) and (tile != last_visited))

    def get_company(self, tile, board):
        return search.bfs(tile, board, can_visit)

    def compute_step(self, board):
        if turns_in_line >= max_turns:
            self.last_visited = self.dest_tile
            self.dest_tile = None
            self.turns_in_line = 0
        else if self.dest_tile == self.get_location():
            append(self.visited_list, tile)
            self.dest_tile = None
            self.turns_in_line = 0
        
        dest = get_company(tile, board)
        if dest is None:
            self.dest_tile = dest
        

