"""The main script.

This sets up a full game with the player code and should implement a class
Team with an __init__ and a step function. The game is set up with the
flags given to this file and plays the game.

Example:
    python test.py --debug

"""

from awap2019 import Direction, Game
from absl import app, flags

from player1.team import Team as P1

FLAGS = flags.FLAGS
flags.DEFINE_integer('num_moves', 300, 'The number of moves in a game.')
flags.DEFINE_integer('score_threshold', 200, 'The score needed to win the game')

flags.DEFINE_string('config', 'boards/sample.txt', 'The path to the config file.')
flags.DEFINE_string('companies', 'companies.txt', 'The path to the list of '
                                                  'companies.')
flags.DEFINE_string('log_file', 'logs/test.txt', 'The path to the log file.')
flags.DEFINE_boolean('debug', False, 'Debug mode')

IDLE_TIME = 10
TEAM_SIZE = 4

def main(_):
    g = Game(FLAGS.config, FLAGS.companies, FLAGS.log_file, False,
             FLAGS.debug, TEAM_SIZE)

    grid = g.generate_player_copy(init=True)

    player1 = P1(grid, FLAGS.team_size, g.get_companyinfo())

    grid = g.generate_player_copy(team=0)
    state = g.board.get_states(0)
    score = 0

    # for the first few moves, your bot will idle while the AI gets a head start
    for _ in range(IDLE_TIME):
        moves = [Direction.NONE for _ in range(FLAGS.team_size)]
        result = g.make_move([moves])

        grid, state, score = result[0]
        if FLAGS.debug:
            print("| Team states: %s" % str(state))
            print("| Score: {}".format(score))

    for x in range(FLAGS.num_moves):
        moves = player1.step(grid, state, score)
        result = g.make_move([moves])

        grid, state, score = result[0]
        if FLAGS.debug:
            print("| Team states: %s" % str(state))
            print("| Score: {}".format(score))
        if score >= FLAGS.score_threshold:
            print("Won with score {}, took {} moves:\nMoves:{}".format(score, x, x))
            return

    print("Timed out with score {}, took {} moves:\nScore:{}".format(score, x, score))

if __name__ == '__main__':
    app.run(main)
