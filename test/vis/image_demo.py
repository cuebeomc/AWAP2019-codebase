"""
Animation of Elastic collisions with Gravity

author: Jake Vanderplas
email: vanderplas@astro.washington.edu
website: http://jakevdp.github.com
license: BSD
Please feel free to use and modify this, but keep the above information. Thanks!
"""
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from matplotlib._png import read_png

#------------------------------------------------------------
arr_hand = read_png('python_logo.png')
imagebox = OffsetImage(arr_hand, zoom=.05)
xy = [-10, -10]               # coordinates to position this image

# adds the literal box to the picture
ab = AnnotationBbox(imagebox,
    xy=xy,
    #xybox=(2.0, 2.0), # don't know why we need this
    #xycoords='data',
    boxcoords="offset points")

#------------------------------------------------------------
# set up figure and animation
fig = plt.figure()
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                     xlim=(-3.2, 3.2), ylim=(-2.4, 2.4))
# return value is same as ab
ax.add_artist(ab)

def init():
    """initialize animation"""
    global ab
    ab.xy = [0, 0]
    return []

def animate(i):
    """perform animation step"""
    global ab
    print(i, ax.axes, ab.xy)
    new_x = ab.xy[0] + 0.1
    if new_x > 2.0:
        new_x = -2.0
    ab.xy = [new_x, ab.xy[1]]
    return [ab]

ani = animation.FuncAnimation(fig, animate, frames=20,
                              interval=100, blit=True, init_func=init)


# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
#ani.save('particle_box.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()
