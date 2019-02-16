"""The main script.

This sets up a full game with the player code and should implement a class
Team with an __init__ and a step function. The game is set up with the
flags given to this file and plays the game.

Example:
    python test.py --debug

"""

from awap2019 import Direction, Game
from absl import app, flags

from player.team import Team as P

FLAGS = flags.FLAGS
flags.DEFINE_integer('num_moves', 300, 'The number of moves in a game.')
flags.DEFINE_integer('score_threshold', 200, 'The score needed to win the game')

flags.DEFINE_string('board_directory', 'boards/', 'The directory where the'
                                                  'the boards are stored.')
flags.DEFINE_string('log_directory', 'logs/', 'The path to the log file.')
flags.DEFINE_string('companies', 'companies.txt', 'The path to the list of '
                                                  'companies.')
flags.DEFINE_string('board_file', 'tiny', 'The name of the board file.')
flags.DEFINE_string('log_file', 'out', 'The file to output to.')
flags.DEFINE_boolean('debug', False, 'Debug mode')

IDLE_TIME = 10
TEAM_SIZE = 4

def main(_):
    board_file = "{}{}.txt".format(FLAGS.board_directory, FLAGS.board_file)
    log_file = "{}{}-{}.txt".format(FLAGS.log_directory, FLAGS.board_file, FLAGS.log_file)

    g = Game(board_file, FLAGS.companies, log_file, False,
             FLAGS.debug, TEAM_SIZE)

    grid = g.generate_player_copy(init=True)

    player1 = P(grid, TEAM_SIZE, g.get_companyinfo())

    grid = g.generate_player_copy(team=0)
    state = g.board.get_states(0)
    score = 0

    # for the first few moves, your bot will idle while the AI gets a head start
    for _ in range(IDLE_TIME):
        moves = [Direction.NONE for _ in range(TEAM_SIZE)]
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
