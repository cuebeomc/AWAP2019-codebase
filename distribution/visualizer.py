from controller import Controller

from absl import app, flags
from scipy.interpolate import interp1d

import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import numpy as np
import random
import sys

FLAGS = flags.FLAGS
flags.DEFINE_string("board_directory", "boards/", "Directory of boards.")
flags.DEFINE_string("board_file", "sample", "The board file to read from.")
flags.DEFINE_string("log_directory", "logs/", "Directory of logs.")
flags.DEFINE_string("log_file", "out", "Log file to read from.")

flags.DEFINE_integer("speed", 40, "# of intervals between one turn in the game.")

FLAGS(sys.argv)

board_file = "{}{}.txt".format(FLAGS.board_directory, FLAGS.board_file)
log_file = "{}{}-{}.txt".format(FLAGS.log_directory, FLAGS.board_file, FLAGS.log_file)

########################
## Parsing board file ##
########################

first_line = True
dim = None
booth_tiles = []
line_tiles = []
y = 0

fig = plt.figure(figsize=(8, 6))

with open(board_file, 'r') as config:
    for line in config:
        if first_line:
            f = line.split()
            dim = (int(f[1]), int(f[0]))
            n = int(f[2])
            booth_tiles  = [[] for _ in range(n)]
            line_tiles = [[] for _ in range(n)]
            first_line = False
        else:
            row = line.split()
            for x, tile in enumerate(row):
                if tile[0] == 'S' or tile[0] == 'M' or tile[0] == 'L':
                    i = int(tile[1:])
                    booth_tiles[i].append((x, y))
                elif tile[0] == 'E':
                    i = int(tile[1:])
                    line_tiles[i].insert(0, (y, x))
                elif tile[0] != 'F' and tile[0] != 'B':
                    i = int(tile)
                    line_tiles[i].append((y, x))
            y += 1

ax = plt.axes(xlim=(0, dim[0] * 3), ylim=(0, dim[1] * 3))

lines = []
directions = []

###################
## Sorting lines ##
###################

for i, line in enumerate(line_tiles):
    direction = "none"
    if len(line) > 1:
        sort_index = None
        rev = False

        end_loc = line[0]
        comp = line[1]
        if end_loc[0] == comp[0]:
            sort_index = 1
        else:
            sort_index = 0
        if end_loc[sort_index] < comp[sort_index]:
            rev = True

        if sort_index == 1 and rev:
            direction = "left"
        elif sort_index == 1 and not rev:
            direction = "right"
        elif sort_index == 0 and rev:
            direction = "up"
        else:
            direction = "down"

        new_tiles = sorted(line,
                           key=lambda x: x[sort_index],
                           reverse=rev)
        lines.append(new_tiles)
    directions.append(direction)

line_dic = {}

for n, line in enumerate(lines):
    for i, tile in enumerate(line):
        line_dic[tile] = (n, i)

#########################
## Creating rectangles ##
#########################

rect_colors = {'#8b8989', '#7259ff', '#ff4c38', '#ffa75a', '#9bff49', '#65ffc9'}

booth_rects = []
for booth in booth_tiles:
    lx, ly = booth[0]
    ux, uy = booth[-1]
    w, h = (ux - lx + 1) * 3, (uy - ly + 1) * 3

    booth_color = random.sample(rect_colors, 1)[0]
    booth_rects.append(plt.Rectangle((lx * 3, ly * 3), w, h, edgecolor='k', facecolor=booth_color))

######################
## Parsing log file ##
######################

sec1 = True   # First section is # of bots
sec2 = False  # Second section is the names of the companies
sec3 = False  # Third section is the actual bot movements.

colors = ['#191970', '#b22222', '#eee9e9']

bots = []
company_names = []

time_step = 0
board = None

scores = []

with open(log_file, 'r') as log:
    for line in log:
        if sec1:
            num_bots = [int(x) for x in line.split()]
            for i, n in enumerate(num_bots):
                team = [plt.Circle((0, 0), 0.3, edgecolor='k', 
                                   facecolor=colors[i]) for _ in range(n)]
                if team:
                    bots.append(team)
            sec1, sec2, sec3 = False, True, False
        elif sec2:
            controller = Controller(bots, dim, line_dic, directions)
            if line == "\n":
                sec1, sec2, sec3 = False, False, True
            else:
                company_names += line.split()
        elif sec3:
            bot_status = line.split()
            if len(bot_status) == 3:
                time_step = bot_status[0]
                scores.append(bot_status[1])
                controller.update(time_step)
            else:
                controller.parse_bot_state(bot_status)

paths = []
for a, team in enumerate(bots):
    team_paths = []
    for b, bot in enumerate(team):
        positions = controller.get_bot_positions(a, b)

        prev_state = None
        prev_tstep = None
        is_none = False
        prev_is_none = False

        point_list = []
        speeds = []
        nones = []
        curr_points = []
        curr_speeds = []
        curr_nones = []

        max_tstep = 0
        for tstep, loc in positions.items():
            state = None
            if loc:
                state = (loc[1], loc[0])
            if tstep == 0:
                prev_state = state
                prev_tstep = tstep
                curr_points.append(prev_state)
                continue
            
            if state == None:
                if curr_points and not prev_is_none:
                    point_list.append(curr_points)
                    curr_points = [prev_state]
                    speeds.append(curr_speeds)
                    curr_speeds = []
                if prev_is_none:
                    curr_nones.append(prev_state)
                else:
                    if curr_nones:
                        nones.append(curr_nones)
                        curr_nones = [prev_state]
                    else:
                        curr_nones = [prev_state]
                prev_tstep = tstep
                prev_is_none = True
            else:
                curr_points.append(state)
                speed = tstep - prev_tstep
                curr_speeds.append(speed)

                prev_state = state
                prev_tstep = tstep
                prev_is_none = False
            
            max_tstep = tstep
        if curr_points and not prev_is_none:
            point_list.append(curr_points)
        if curr_speeds and not prev_is_none:
            speeds.append(curr_speeds)
        if curr_nones:
            nones.append(curr_nones)

        total_points = []

        prev_point = None
        for i, points in enumerate(point_list):
            if len(points) == 1:
                total_points.append([points[0]])
                continue
            elif len(points) == 2:
                sample_space = FLAGS.speed * speeds[i][0]
                x1, y1 = points[0]
                x2, y2 = points[1]
                x_coords = np.linspace(x1, x2, sample_space, endpoint=False)
                y_coords = np.linspace(y1, y2, sample_space, endpoint=False)
                points = np.array([x_coords, y_coords]).T
                total_points.append(points)
                continue

            # print(points)
            np_points = np.array(points)
            distance = np.cumsum(np.sqrt(np.sum(np.diff(np_points, axis=0)**2, axis=1)))
            distance = np.insert(distance, 0, 0)/distance[-1]

            speed = speeds[i]
            alpha = np.array([])

            for x in range(len(distance) - 1):
                new_section = np.linspace(distance[x], distance[x+1], FLAGS.speed * speed[x], endpoint=False)
                alpha = np.concatenate((alpha, new_section))
            
            interpolator = interp1d(distance, points, kind='quadratic', axis=0)
            np_points = interpolator(alpha)
            total_points.append(np_points)

        path = np.empty(shape=(0, 2))
        for i, step in enumerate(total_points):
            if len(step) == 1:
                for _ in nones[i]:
                    still_frames = [step[0] for _ in range(FLAGS.speed)]
                    path = np.concatenate((path, still_frames))
                continue

            path = np.concatenate((path, step))    
            try:
                for loc in nones[i]:
                    still_frames = [loc for _ in range(FLAGS.speed)]
                    path = np.concatenate((path, still_frames))
            except:
                continue
        team_paths.append(path)
    paths.append(team_paths)

# Removing ticks on axes and starting (0, 0) at top right.
ax.set_xticks([])
ax.set_yticks([])
ax.invert_yaxis()

flattened = [bot for team in reversed(bots) for bot in reversed(team)]
flat_paths = [path for team_paths in reversed(paths) for path in reversed(team_paths)]
num_frames = (max_tstep + 1) * FLAGS.speed

for i, path in enumerate(flat_paths):
    flat_paths[i] = np.pad(path, pad_width=(0, num_frames-len(path)), mode='edge')

score_text = ax.text(0.1, 0.3, 'cuebeommmm', fontsize=10)
running_total = 0
running_arr = []
for score in scores:
    running_total += int(score)
    running_arr.append(running_total)

scores = []
for score in running_arr:
    for _ in range(FLAGS.speed):
        scores.append(str(score))

def init():
    for rect in booth_rects:
        ax.add_patch(rect)
    for bot in flattened:
        ax.add_patch(bot)
    score_text.set_text(scores[0])
    return flattened + booth_rects + [score_text]

def animate(i):
    index = i % num_frames
    for j, bot in enumerate(flattened):
        bot.center = flat_paths[j][index]

    score_text.set_text(scores[i])
    return flattened + booth_rects + [score_text]

anim = animation.FuncAnimation(fig, animate,
                               frames=num_frames,
                               init_func=init,
                               interval=20,
                               blit=True,
                               repeat=False)

#anim.save('output/animation.gif', writer='imagemagick')
plt.show()

