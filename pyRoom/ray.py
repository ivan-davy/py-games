import math


class Ray:
    def __init__(self, world, phi):
        self.src0 = [world.player.x, world.player.y]
        self.phi = phi
        self.reach = 700
        self.src1 = [self.src0[0] + self.reach * math.sin(self.phi + math.pi),
                     self.src0[1] + self.reach * math.cos(self.phi + math.pi)]
        self.intersection = []
        self.intDist = 0
        self.world = world

    def renderTop(self):
        self.world.canvas.create_line(*self.src0, *self.src1, tags='ray')

    def renderPov(self, ray_num):
        self.intDist *= math.cos(self.phi - self.world.player.phi)
        try:
            strip_height = 1 / (self.intDist * math.cos(self.phi - self.world.player.phi)) * 20000
        except ZeroDivisionError:
            strip_height = 0
        self.world.canvas.create_rectangle(ray_num * self.world.x_window_size / self.world.rayQty,
                                           self.world.y_window_size / 2 - strip_height,
                                           (ray_num + 1) * self.world.x_window_size / self.world.rayQty,
                                           self.world.y_window_size / 2 + strip_height,
                                           tags='strip', fill='white', outline='white')
        self.world.canvas.tag_raise('strip')
        pass

    def shade(self):
        for wall in self.world.level:

            def det(a, b):
                return a[0] * b[1] - a[1] * b[0]

            def ccw(A, B, C):
                return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

            def intersect(A, B, C, D):  # Returns true if line segments AB and CD intersect
                return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

            xdiff = (self.src0[0] - self.src1[0], wall.p0[0] - wall.p1[0])
            ydiff = (self.src0[1] - self.src1[1], wall.p0[1] - wall.p1[1])
            div = det(xdiff, ydiff)
            d = (det(self.src0, self.src1), det(wall.p0, wall.p1))

            if intersect(self.src0, self.src1, wall.p0, wall.p1):
                self.intersection = [det(d, xdiff) / div, det(d, ydiff) / div]
                self.intDist = math.dist(self.src0, self.intersection)
                if self.world.view == 'top':
                    self.world.canvas.create_oval(self.intersection[0] - 10, self.intersection[1] - 10,
                                                  self.intersection[0] + 10, self.intersection[1] + 10,
                                                  fill='cyan', tags='intersect')
                return self.intDist
