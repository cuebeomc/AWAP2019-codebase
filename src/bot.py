class Bot(object):

    def __init__(self,x,y,step_gain):
        self.x = x
        self.y = y
        self.step_gain = step_gain
        self.progress = 0
        self.should_advance = false

    def set_destinations(self, dest_x, dest_y):
        self.dest_x = dest_x
        self.dest_y = dest_y

    def set_progress(self, progress):
        self.progress = progress

    def compute_step(self,threshold):
        self.progress += self.step_gain
        if self.progress >= threshold:
            should_advance = true

    def execute_step(self):
        #needs to know next tile, will code later
