from board import Board

class Game(object):
    def __init__(self, directory, status=False):
        """Initialize a game instance.

        directory: If playing offline, it will look in this directory for
                   a config file.
        status: if true, connect to our servers to play the game. Otherwise,
                play offline. If a connection cannot be reached, play offline.

        """
        self.online = status # CHANGE
        self.test = 0

    def make_move(self, moves):
        return 0
