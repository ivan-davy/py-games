from random import randrange
from tkinter import *


class World:
    def __init__(self):
        self.game_on = True  # game state
        self.start_frame = 150  # starting frame
        self.score = 0  # game score
        self.x_size = 800  # horizontal window size
        self.y_size = 800  # vertical window size
        self.color = 'black'  # bkg color
        self.root = Tk()  # window
        self.canvas = Canvas()  # canvas
        self.font_size = int(self.y_size / 25)  # font size
        self.bird = None  # active bird
        self.obstacles = []  # active obstacles

    def setup(self):
        self.root.title('Bounce off the floor for extra points!')
        self.root.geometry(f'{self.x_size}x{self.y_size}')
        self.canvas.focus_set()
        self.canvas.pack(fill=BOTH, expand=1)
        self.canvas.configure(background='black')
        self.updateScore()

    def updateScore(self):
        self.canvas.delete('score')
        self.canvas.create_text(self.font_size * 3, self.font_size,
                                text=f'SCORE: {self.score}', fill='white',
                                font=('Helvetica', str(self.font_size), 'bold'),
                                tags='score')
        self.canvas.tag_raise('score')

    def restart(self, event):
        if event.keysym == 'space':
            self.canvas.delete('all')
            self.score = 0
            self.updateScore()
            self.obstacles = []
            self.bird.y = self.y_size / 2
            self.game_on = True
            gameplay(self, self.bird, self.start_frame)


class Bird:
    def __init__(self, world):
        self.r = world.y_size / 50  # radius
        self.x = world.x_size / 3  # x coord
        self.y = world.y_size / 2  # y coord
        self.v = 0  # velocity
        self.a = 0.3  # acceleration
        self.f = 8  # jumping force
        self.world = world  # active world
        self.color = 'orange'  # fill color

    def render(self):
        self.world.canvas.delete('ball')
        x0 = self.x - self.r
        y0 = self.y - self.r
        x1 = self.x + self.r
        y1 = self.y + self.r
        self.world.canvas.create_oval(x0, y0, x1, y1, fill=self.color, outline='white', tags='ball')

    def checkBoundariesCollision(self):
        if self.y >= self.world.y_size - self.r:
            self.y = self.world.y_size - self.r
            self.v = -self.v + 1
            self.world.score += 3
            self.world.updateScore()
        if self.y <= self.r:
            self.y = self.r
            self.v = -self.v - 1
            self.world.score += 3
            self.world.updateScore()

    def checkObstaclesCollision(self):
        for wall in self.world.obstacles:
            if wall.passed is False:
                if wall.x < self.x < wall.x + wall.w:
                    if not (wall.y - self.r / 2 > self.y > wall.y - wall.g + self.r / 2):
                        self.world.game_on = False

    def jump(self, event):
        if event.keysym == 'space':
            self.v = -self.f

    def update(self):
        self.y += self.v
        self.v += self.a
        self.checkBoundariesCollision()
        self.checkObstaclesCollision()
        self.render()


class Obstacle:
    def __init__(self, world, bird, id_frame):
        self.x = world.x_size  # fixed x position
        self.w = world.x_size / 10  # obstacle width (thick part)
        self.t = self.w / 10  # width trim amount (thinner part)
        self.g = world.y_size / 4  # obstacle gap size
        self.s = world.y_size / 10  # safe zone size
        self.y = randrange(self.s + self.g, world.y_size - self.s)  # lower obstacle height
        self.v = 2  # velocity
        self.world = world  # active world
        self.bird = bird  # active bird
        self.id = str(id_frame)  # obstacle's ID – frame when it was created
        self.color = 'orange'  # obstacle fill color
        self.passed = False  # is it behind the bird?

    def render(self):
        self.world.canvas.delete(f'w{self.id}')
        self.world.canvas.create_rectangle(self.x, self.y,
                                           self.x + self.w, self.y + self.s,
                                           fill=self.color, outline='white', tags=f'w{self.id}')
        self.world.canvas.create_rectangle(self.x + self.t, self.y + self.s,
                                           self.x + self.w - self.t, self.world.y_size,
                                           outline='white', tags=f'w{self.id}')
        self.world.canvas.create_rectangle(self.x, self.y - self.g - self.s,
                                           self.x + self.w, self.y - self.g,
                                           fill=self.color, outline='white', tags=f'w{self.id}')
        self.world.canvas.create_rectangle(self.x + self.t, 0,
                                           self.x + self.w - self.t, self.y - self.g - self.s,
                                           outline='white', tags=f'w{self.id}')
        self.world.canvas.tag_lower(f'w{self.id}')

    def update(self):
        self.x += -self.v
        self.render()
        if self.x + self.w < self.bird.x and self.passed is False:
            self.passed = True
            self.world.score += 1
            self.world.updateScore()
        if self.x < -self.w:
            del self


def gameplay(world, bird, current_frame):
    current_frame += 1
    if world.game_on is True:
        bird.update()
        for wall in world.obstacles:
            wall.update()
        if current_frame % 200 == 0:
            world.obstacles.append(Obstacle(world, bird, current_frame))
        world.canvas.bind('<KeyPress>', bird.jump)
        # print(f'\rSCORE: {world.score}', end='')
        world.root.after(10, gameplay, world, bird, current_frame)
    else:
        world.canvas.create_text(world.x_size / 2, world.y_size / 2,
                                 text=f'GAME OVER', fill='red',
                                 font=('Helvetica', str(world.font_size * 3), 'bold'),
                                 tags='gameover')
        world.canvas.tag_raise('gameover')
        world.canvas.bind('<KeyPress>', world.restart)


def main():
    world = World()
    world.setup()
    bird = Bird(world)
    world.bird = bird
    gameplay(world, bird, current_frame=world.start_frame)
    mainloop()


if __name__ == '__main__':
    main()
