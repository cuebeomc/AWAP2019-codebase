"""The main script.

This sets up a full game with the player code (which should be in the folders
player1 and player2, respectively) and should implement a class Team with an
__init__ and a step function. We set up the game with the flags given to
this file, and we play out the game.

TODO: Still have to implement a scoring system. This will be passed along to
this script through the Game class' function make_move.
"""

from awap2019 import Direction, Game

from absl import flags
from absl import app

FLAGS = flags.FLAGS
flags.DEFINE_boolean('m', False, 'Play in multiplayer mode.')
flags.DEFINE_integer('num_moves', 300, 'The number of moves in a game.')

flags.DEFINE_string('config', 'config.txt', 'The path to the config file.')
flags.DEFINE_string('companies', 'companies.txt', 'The path to the list of '
                                                  'companies.')
flags.DEFINE_boolean('debug', False, 'Debug mode')
from player1.team import Team as P1
from player2.team import Team as P2

def main(_):
    g = Game(FLAGS.config, FLAGS.companies, FLAGS.m, FLAGS.debug)
    print("Companies: ")
    for booth in g.board.booths:
        print(booth.name)
    print()

    grid = g.generate_player_copy(init=True)

    player1 = P1(grid)
    if FLAGS.m:
        player2 = P2(grid)

    grid1, pos1 = g.generate_player_copy(team=0), g.board.get_positions(0)
    if FLAGS.m:
        grid2, pos2 = g.generate_player_copy(team=1), g.board.get_positions(1)

    for i in range(FLAGS.num_moves):
        moves = [player1.step(grid1, pos1)]
        if FLAGS.m:
            moves.append(player2.step(grid2, pos2))

        result = g.make_move(moves)
        grid1, pos1 = result[0]
        if FLAGS.m:
            grid2, pos2 = result[1]
        if FLAGS.debug:
            print("Team 1 positions: {}".format(pos1))
            print("Team 2 positions: {}".format(pos2))

if __name__ == '__main__':
    app.run(main)
