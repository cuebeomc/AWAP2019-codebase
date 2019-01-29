"""The main script.

This sets up a full game with the player code (which should be in the folders
player1 and player2, respectively) and should implement a class Team with an
__init__ and a step function. We set up the game with the flags given to
this file, and we play out the game.

Example:

    python test.py -debug -m -team_size 5
"""

from awap2019 import Direction, Game

from absl import flags
from absl import app

from player1.team import Team as P1
from player2.team import Team as P2

FLAGS = flags.FLAGS
flags.DEFINE_boolean('m', False, 'Play in multiplayer mode.')
flags.DEFINE_integer('num_moves', 300, 'The number of moves in a game.')

flags.DEFINE_string('config', 'config.txt', 'The path to the config file.')
flags.DEFINE_string('companies', 'companies.txt', 'The path to the list of '
                                                  'companies.')
flags.DEFINE_string('log_file', 'log.txt', 'The path to the log file.')
flags.DEFINE_boolean('debug', False, 'Debug mode')
flags.DEFINE_integer('team_size', 3, 'The team size.')

def main(_):
    g = Game(FLAGS.config, FLAGS.companies, FLAGS.log_file,
             FLAGS.m, FLAGS.debug, FLAGS.team_size)
    print("Companies: ")
    for booth in g.board.booths:
        print(booth.name)
    print()

    grid = g.generate_player_copy(init=True)

    player1 = P1(grid, FLAGS.team_size)
    if FLAGS.m:
        player2 = P2(grid, FLAGS.team_size)

    grid1, state1, score1 = (g.generate_player_copy(team=0),
                             g.board.get_states(0), 0)
    if FLAGS.m:
        grid2, state2, score2 = (g.generate_player_copy(team=1),
                                 g.board.get_states(1), 0)

    for _ in range(FLAGS.num_moves):
        moves = [player1.step(grid1, state1, score1)]
        if FLAGS.m:
            moves.append(player2.step(grid2, state2, score2))

        result = g.make_move(moves)
        grid1, state1, score1 = result[0]
        if FLAGS.m:
            grid2, state2, score2 = result[1]
        if FLAGS.debug:
            print("Team 1 states: {}".format(state1))
            print("Score: {}".format(score1))
            if FLAGS.m:
                print("Team 2 states: {}".format(state2))
                print("Score: {}".format(score2))

if __name__ == '__main__':
    app.run(main)
