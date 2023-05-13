import math
from numpy import linspace


class Player:
    def __init__(self, world):
        self.size = 25  # radius
        self.x = world.x_level_size / 2  # x coord
        self.y = world.y_level_size / 3  # y coord
        self.phi = 0  # direction
        self.mobility = 1.5
        self.vx = 0  # x-coord velocity
        self.vy = 0  # y-coord velocity
        self.v_lim = 30  # velocity limit
        self.rayDirections = linspace(self.phi-world.fov/2, self.phi+world.fov/2, int(world.rayQty))
        self.world = world  # active world

    def wallCollision(self):
        pass

    def renderTop(self):
        self.world.canvas.delete('player')
        self.world.canvas.create_oval(self.x - 10, self.y - 10,
                                      self.x + 10, self.y + 10,
                                      fill='red', tags='player')

    def move(self):
        self.vx, self.vy = self.vx / 1.2, self.vy / 1.2
        if self.world.pressedStatus['w']:
            self.vx += self.mobility * math.sin(self.phi - math.pi)
            self.vy += self.mobility * math.cos(self.phi - math.pi)
        if self.world.pressedStatus['s']:
            self.vx -= self.mobility * math.sin(self.phi - math.pi)
            self.vy -= self.mobility * math.cos(self.phi - math.pi)
        if self.world.pressedStatus['d']:
            self.vx += self.mobility * math.sin(self.phi - math.pi / 2)
            self.vy += self.mobility * math.cos(self.phi - math.pi / 2)
        if self.world.pressedStatus['a']:
            self.vx += self.mobility * math.sin(self.phi + math.pi / 2)
            self.vy += self.mobility * math.cos(self.phi + math.pi / 2)
        if self.world.pressedStatus['Left']:
            self.phi -= self.mobility / 50
        if self.world.pressedStatus['Right']:
            self.phi += self.mobility / 50

    def update(self, view):
        def pressed(event):
            self.world.pressedStatus[event.keysym] = True

        def released(event):
            self.world.pressedStatus[event.keysym] = False

        for item in ['w', 's', 'a', 'd', 'Left', 'Right']:
            self.world.canvas.bind("<KeyPress-%s>" % item, pressed)
            self.world.canvas.bind("<KeyRelease-%s>" % item, released)

        self.move()
        self.y += self.vy
        self.x += self.vx
        self.rayDirections = linspace(self.phi-self.world.fov/2,
                                      self.phi+self.world.fov/2,
                                      int(self.world.rayQty))
        self.wallCollision()
        if view == 'top':
            self.renderTop()
