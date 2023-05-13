from tkinter import *


class World:
    def __init__(self):
        self.game_on = True  # game state
        self.current_frame = 0
        self.wall_color = 'white'
        self.ground_color = 'black'
        self.sky_color = 'blue'
        self.x_level_size = 800  # horizontal level size
        self.y_level_size = 800  # vertical level size
        self.x_window_size = 1440  # horizontal window size
        self.y_window_size = 800  # vertical window size
        self.level = None  # walls
        self.root = Tk()  # window
        self.canvas = Canvas()  # canvas
        self.player = None  # active player
        self.view = 'pov'
        self.fov = 0.6
        self.rayQty = self.x_window_size / 5
        self.pressedStatus = {'w': False, 's': False, 'a': False, 'd': False,
                              'Left': False, 'Right': False}

    def setup(self, player, level):
        self.root.title('Walk around, I guess?')
        self.root.geometry(f'{self.x_level_size if self.view == "top" else self.x_window_size}x'
                           f'{self.y_level_size if self.view == "top" else self.y_window_size}')
        self.canvas.focus_set()
        self.canvas.pack(fill=BOTH, expand=1)
        self.canvas.configure(background='black')
        self.player = player
        self.level = level
        if self.view == 'pov':
            self.canvas.create_rectangle(0, 0,
                                         self.x_window_size, self.y_window_size / 2,
                                         fill=self.sky_color, tags='bkg')
            self.canvas.create_rectangle(0, self.y_window_size / 2,
                                         self.x_window_size, self.y_window_size,
                                         fill=self.ground_color, tags='bkg')
            self.canvas.tag_lower('bkg')
        if self.view == 'top':
            for wall in self.level:
                wall.renderTop()

    def updateLevel(self):
        self.canvas.delete('level')
        self.canvas.tag_raise('level')

    def restart(self):
        self.canvas.delete('all')
        self.player.x, self.player.y = 0, 0
        self.game_on = True
