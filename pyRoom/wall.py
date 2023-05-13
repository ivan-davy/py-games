import math


class Wall:
    def __init__(self, x0, y0, x1, y1, world):
        self.p0 = [x0, y0]
        self.p1 = [x1, y1]
        self.length = math.dist(self.p0, self.p1)
        self.world = world

    def renderTop(self):
        self.world.canvas.create_line(*self.p0, *self.p1, tags='wall')
