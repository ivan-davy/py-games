import random
import time
from random import randrange
from tkinter import *


class World:
    def __init__(self):
        self.game_on = True  # game state
        self.score_team1 = 0  # game score
        self.score_team2 = 0
        self.color_team1 = 'cyan'
        self.color_team2 = 'orange'
        self.x_size = 1600  # horizontal window size
        self.y_size = 800  # vertical window size
        self.safe_zone = int(self.x_size / 8)  # distance from the edge (horizontal safe zone)
        self.color = 'black'  # bkg color
        self.root = Tk()  # window
        self.canvas = Canvas()  # canvas
        self.font_size = int(self.y_size / 16)  # font size
        self.ball = None  # active ball
        self.rackets = []  # active rackets
        self.speed = 7
        self.pressedStatus = {'w': False, 's': False, 'Up': False, 'Down': False}

    def setup(self):
        self.root.title('Deflect the ball!')
        self.root.geometry(f'{self.x_size}x{self.y_size}')
        self.canvas.focus_set()
        self.canvas.pack(fill=BOTH, expand=1)
        self.canvas.configure(background='black')
        self.updateScore()

    def updateScore(self):
        self.canvas.delete('score')
        self.canvas.create_text(self.font_size * 2, self.font_size,
                                text=f'P1 / {self.score_team1}', fill='white',
                                font=('Helvetica', str(self.font_size), 'bold'),
                                tags='score')
        self.canvas.create_text(self.x_size - self.font_size * 2, self.font_size,
                                text=f'{self.score_team2} \ P2', fill='white',
                                font=('Helvetica', str(self.font_size), 'bold'),
                                tags='score')
        self.canvas.create_rectangle(0, 0,
                                     self.font_size / 3, int(self.font_size * 2),
                                     fill=self.color_team1, tags='scorebkg')
        self.canvas.create_rectangle(self.x_size - int(self.font_size / 3), 0,
                                     self.x_size, self.font_size * 2,
                                     fill=self.color_team2, tags='scorebkg')

        self.canvas.create_text(self.x_size / 2, self.font_size,
                                text=f'{self.score_team1 + self.score_team2 + 1}', fill='white',
                                font=('Helvetica', str(self.font_size), 'bold'),
                                tags='score')
        self.canvas.create_rectangle(self.x_size / 2 - self.font_size, self.font_size - int(self.font_size / 1.5),
                                     self.x_size / 2 + self.font_size, self.font_size + int(self.font_size / 1.5),
                                     outline='white', tags='scorebkg')
        self.canvas.tag_raise('score')

    def restart(self):
        self.canvas.delete('all')
        self.updateScore()
        self.rackets = [Racket(self, 1), Racket(self, 2)]
        self.ball.x = self.x_size / 2
        self.ball.y = self.y_size / 2
        if random.random() > 0.5:
            direction = 1
        else:
            direction = -1
        self.ball.vx = randrange(int(self.speed / 1.7), int(self.speed * 1.7)) * direction  # horizontal velocity
        self.ball.vy = randrange(-int(self.speed / 1.7), int(self.speed / 1.7))  # vertical velocity
        time.sleep(0.3)
        self.game_on = True


class Ball:
    def __init__(self, world):
        self.r = world.x_size / 100  # radius
        self.x = world.x_size / 2  # x coord
        self.y = world.y_size / 2  # y coord
        if random.random() > 0.5:
            self.direction = 1
        else:
            self.direction = -1
        self.vx = randrange(int(world.speed / 1.7), int(world.speed * 1.7)) * self.direction  # horizontal velocity
        self.vy = randrange(-int(world.speed / 1.7), int(world.speed / 1.7))  # vertical velocity
        self.vy_lim = world.speed
        self.world = world  # active world
        self.color = 'white'  # fill color

    def render(self):
        self.world.canvas.delete('ball')
        x0 = self.x - self.r
        y0 = self.y - self.r
        x1 = self.x + self.r
        y1 = self.y + self.r
        self.world.canvas.create_oval(x0, y0, x1, y1, fill=self.color, tags='ball')

    def checkBoundariesCollision(self):
        if self.y >= self.world.y_size - self.r:
            self.y = self.world.y_size - self.r
            self.vy = -self.vy + 1
        if self.y <= self.r:
            self.y = self.r
            self.vy = -self.vy - 1
        if self.x >= self.world.x_size - self.r:
            self.x = self.world.x_size - self.r
            self.vx = 0
            self.world.score_team1 += 1
            self.world.restart()
        if self.x <= self.r:
            self.x = self.r
            self.vx = 0
            self.world.score_team2 += 1
            self.world.restart()

    def checkRacketCollision(self):
        # if self.x < self.world.safe_zone * 2 or self.x > (self.world.x_size - self.world.safe_zone * 2):
        for racket in self.world.rackets:
            if (racket.team == 1 and racket.x - racket.t/2 < self.x - self.r < racket.x + racket.t / 2) or (
                    racket.team == 2 and racket.x + racket.t > self.x + self.r > racket.x - racket.t):
                if racket.y - racket.l / 2 - self.r / 2 < self.y < racket.y + racket.l / 2 + self.r / 2:
                    self.vx = -self.vx
                    self.vy = racket.vy / 2

    def update(self):
        if abs(self.vy) > self.vy_lim:
            self.vy = self.vy_lim * self.vy / abs(self.vy)
        self.y += self.vy
        self.x += self.vx
        self.checkBoundariesCollision()
        self.checkRacketCollision()
        self.render()


class Racket:
    def __init__(self, world, team):
        self.team = team

        self.t = world.x_size / 100  # thickness
        self.l = int(world.y_size / 8)  # size (length)
        if self.team == 1:
            self.x = world.safe_zone + self.t  # horizontal position (center)
        else:
            self.x = world.x_size - world.safe_zone - self.t
        self.y = world.y_size / 2  # vertical position (center)
        self.vy = 0
        self.world = world  # active world

    def render(self):
        self.world.canvas.delete(f'r{self.team}')
        if self.team == 1:
            clr = self.world.color_team1
        else:
            clr = self.world.color_team2
        self.world.canvas.create_rectangle(self.x - self.t / 2, self.y - self.l / 2,
                                           self.x + self.t / 2, self.y + self.l / 2,
                                           fill=clr, outline=clr, tags=f'r{self.team}')

    def move(self):
        self.vy = self.vy / 1.2
        if self.world.pressedStatus['w'] and self.team == 1:
            self.vy = -self.world.speed
        if self.world.pressedStatus['s'] and self.team == 1:
            self.vy = self.world.speed
        if self.world.pressedStatus['Up'] and self.team == 2:
            self.vy = -self.world.speed
        if self.world.pressedStatus['Down'] and self.team == 2:
            self.vy = self.world.speed

    def update(self):
        def pressed(event):
            self.world.pressedStatus[event.keysym] = True

        def released(event):
            self.world.pressedStatus[event.keysym] = False

        for item in ['w', 's', 'Up', 'Down']:
            self.world.canvas.bind("<KeyPress-%s>" % item, pressed)
            self.world.canvas.bind("<KeyRelease-%s>" % item, released)
        self.move()
        self.y += self.vy
        self.render()


def gameplay(world, current_frame):
    if world.game_on is True:
        world.ball.update()
        for racket in world.rackets:
            racket.update()
        current_frame += 1
        world.root.after(10, gameplay, world, current_frame)
    else:
        world.restart()


def main():
    world = World()
    world.setup()
    ball = Ball(world)
    racket1, racket2 = Racket(world, 1), Racket(world, 2)
    world.ball = ball
    world.rackets = [racket1, racket2]
    gameplay(world, current_frame=0)
    mainloop()


if __name__ == '__main__':
    main()
