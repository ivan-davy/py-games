from random import randrange
from tkinter import *


class PlayArea:
    def __init__(self, rt, cv):
        self.score = 0
        self.x_cells = 25
        self.y_cells = 25
        self.scale = 50
        self.gap = 1
        self.grid = []
        self.wdw = rt
        self.cv = cv
        self.gameOn = True

    def setup(self):
        self.wdw.title('Eat rectangular apples with a rectangular snake!')
        self.wdw.geometry(f'{self.x_cells * self.scale}x{self.y_cells * self.scale}')
        self.cv.pack(fill=BOTH, expand=1)
        self.cv.configure(background='black')
        for x_coord in range(self.x_cells):
            column = []
            for y_coord in range(self.y_cells):
                cur_cell = Cell(x_coord, y_coord, None)
                column.append(cur_cell)
            self.grid.append(column)
        return self

    def drawCell(self, cell):
        x0 = cell.x_pos * self.scale + self.gap
        y0 = cell.y_pos * self.scale + self.gap
        x1 = (cell.x_pos + 1) * self.scale - self.gap
        y1 = (cell.y_pos + 1) * self.scale - self.gap
        if cell.state is True:
            color = 'red'
        elif cell.state is False:
            color = 'orange'
        else:
            color = 'grey'
        self.cv.create_rectangle(x0, y0, x1, y1, fill=color)

    def render(self):
        self.cv.delete('all')
        for x in range(self.x_cells):
            for y in range(self.y_cells):
                self.drawCell(self.grid[x][y])


class Cell:
    def __init__(self, x, y, cell_state):
        self.x_pos = x
        self.y_pos = y
        self.state = cell_state


class Snake:
    def __init__(self, play_area):
        self.length = 3
        self.direction = 'RIGHT'
        self.play_area = play_area
        x0 = randrange(2, play_area.x_cells)
        y0 = randrange(play_area.y_cells)
        self.pos = [(x0, y0), (x0 - 1, y0), (x0 - 2, y0)]

    def refresh(self):
        for snake_cell in self.pos:
            self.play_area.grid[snake_cell[0]][snake_cell[1]].state = False

    def changeDirection(self, event):
        if event.keysym == 'w' and self.direction != 'DOWN':
            self.direction = 'UP'
        if event.keysym == 's' and self.direction != 'UP':
            self.direction = 'DOWN'
        if event.keysym == 'a' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        if event.keysym == 'd' and self.direction != 'LEFT':
            self.direction = 'RIGHT'

    def move(self):
        self.appleCollision()
        self.selfCollision()
        self.wallCollision()
        if self.direction == 'UP':
            self.pos.insert(0, (self.pos[0][0], self.pos[0][1] - 1))
        if self.direction == 'DOWN':
            self.pos.insert(0, (self.pos[0][0], self.pos[0][1] + 1))
        if self.direction == 'LEFT':
            self.pos.insert(0, (self.pos[0][0] - 1, self.pos[0][1]))
        if self.direction == 'RIGHT':
            self.pos.insert(0, (self.pos[0][0] + 1, self.pos[0][1]))
        last = self.pos.pop()
        self.play_area.grid[last[0]][last[1]].state = None
        # print(self.length, self.pos, self.direction)

    def getNextCell(self, current_cell):
        x = current_cell.x_pos
        y = current_cell.y_pos
        try:
            if self.direction == 'UP':
                next_cell = board.grid[x][y - 1]
            elif self.direction == 'DOWN':
                next_cell = board.grid[x][y + 1]
            elif self.direction == 'LEFT':
                next_cell = board.grid[x - 1][y]
            elif self.direction == 'RIGHT':
                next_cell = board.grid[x + 1][y]
            else:
                next_cell = None
        except IndexError:
            next_cell = None
        return next_cell

    def wallCollision(self):
        if self.direction == 'UP' and self.pos[0][1] == 0:
            if self.pos[0][0] == board.x_cells - 1:
                self.direction = 'LEFT'
            else:
                self.direction = 'RIGHT'
        if self.direction == 'RIGHT' and self.pos[0][0] == board.x_cells - 1:
            if self.pos[0][1] == board.y_cells - 1:
                self.direction = 'UP'
            else:
                self.direction = 'DOWN'
        if self.direction == 'DOWN' and self.pos[0][1] == board.y_cells - 1:
            if self.pos[0][0] == 0:
                self.direction = 'RIGHT'
            else:
                self.direction = 'LEFT'
        if self.direction == 'LEFT' and self.pos[0][0] == 0:
            if self.pos[0][1] == 0:
                self.direction = 'DOWN'
            else:
                self.direction = 'UP'

    def appleCollision(self):
        apple_cell = self.getNextCell(board.grid[self.pos[0][0]][self.pos[0][1]])
        try:
            if apple_cell.state is True:
                apple_cell.state = False
                board.score += 1
                self.length += 1
                self.pos.insert(0, (apple_cell.x_pos, apple_cell.y_pos))
                apple.respawn()
        except AttributeError:
            pass

    def selfCollision(self):
        try:
            next_cell = self.getNextCell(board.grid[self.pos[0][0]][self.pos[0][1]])
            x = next_cell.x_pos
            y = next_cell.y_pos
            if (x, y) in self.pos:
                board.gameOn = False
        except AttributeError:
            pass


class Apple:
    def __init__(self, play_area):
        self.pos = None
        self.play_area = play_area
        self.spawn()

    def spawn(self):
        done = False
        while not done:
            x = randrange(self.play_area.x_cells)
            y = randrange(self.play_area.y_cells)
            if self.play_area.grid[x][y].state is None:
                self.pos = [x, y]
                done = True
        self.refresh()

    def respawn(self):
        board.grid[self.pos[0]][self.pos[1]].state = None
        self.spawn()

    def refresh(self):
        self.play_area.grid[self.pos[0]][self.pos[1]].state = True


def gameplay(brd, snk, apl):
    if brd.gameOn is True:
        snk.move()
        apl.refresh()
        snk.refresh()
        brd.render()
        root.update()
        print(f'\rSCORE: {brd.score}', end='')
        canvas.bind('<KeyPress>', snk.changeDirection)
        root.after(100, gameplay, brd, snk, apl)
    else:
        print('\nGAME OVER!')


root = Tk()
canvas = Canvas(root)
canvas.focus_set()
board = PlayArea(root, canvas).setup()
snake = Snake(board)
apple = Apple(board)
root.after(0, gameplay, board, snake, apple)
root.mainloop()
