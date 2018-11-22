from absl import flags
from absl import app

from board import Board

class Game(object):
    def __init__(self):
        self.test = 0

def main(_):
    print("Hello!")

if __name__ == '__main__':
    app.run(main)
