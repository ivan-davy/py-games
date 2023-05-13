import random
from tkinter import *
import time
from math import dist


class World:
    def __init__(self):
        self.gameOn = True  # game state
        self.currentFrame = 0
        self.playerColor = 'cyan'
        self.enemyColor = 'red'
        self.foodColor = 'white'
        self.xWindowSize = 1500  # horizontal window size
        self.yWindowSize = 1000  # vertical window size
        self.scaling = 1
        self.xRenderSize = self.xWindowSize * (1 / self.scaling)  # horizontal level size
        self.yRenderSize = self.yWindowSize * (1 / self.scaling)  # vertical level size
        self.root = Tk()  # window
        self.canvas = Canvas()  # canvas
        self.player = None  # active player
        self.enemies = []
        self.foods = []
        self.foodsLimit = 250
        self.enemiesLimit = 7
        self.pressedStatus = {'w': False, 's': False, 'a': False, 'd': False}

    def setup(self, player):
        self.root.title('Consume and do not get consumed!')
        self.root.geometry(f'{self.xWindowSize}x{self.yWindowSize}')
        self.canvas.focus_set()
        self.canvas.pack(fill=BOTH, expand=1)
        self.canvas.configure(background='black')
        self.player = player

    def restart(self):
        self.canvas.delete('all')
        self.canvas.create_text(self.xWindowSize / 2, self.yWindowSize / 2,
                                text='GAME OVER', fill='white',
                                font=('Helvetica', f'{int(self.xWindowSize / 10)}', 'bold'), tags='ui')
        self.canvas.create_text(self.xWindowSize / 2, self.yWindowSize * 3 / 4,
                                text=f'SCORE: {int(self.player.size)}', fill='white',
                                font=('Helvetica', f'{int(self.xWindowSize / 20)}', 'bold'), tags='ui')
        self.gameOn = True
        self.enemies = []
        self.foods = []
        player = Player(self)
        self.setup(player)
        self.root.after(3000, gameplay, self)


class Player:
    def __init__(self, world):
        self.size = world.yWindowSize / 5  # real size (score)
        self.renderSize = self.size  # visible size (px)
        self.x = world.xWindowSize / 2  # x coord
        self.y = world.yWindowSize / 2  # y coord
        self.vx = 0
        self.vy = 0
        self.mobility = 3
        self.world = world  # active world

    def render(self):
        self.world.canvas.delete('player')
        self.world.canvas.create_oval(self.x - self.renderSize / 2, self.y - self.renderSize / 2,
                                      self.x + self.renderSize / 2, self.y + self.renderSize / 2,
                                      fill=self.world.playerColor, tags='player')

    def moveWorld(self):
        if self.world.pressedStatus['w']:
            for food in self.world.foods:
                food.vy += self.mobility
            for enemy in self.world.enemies:
                enemy.vy += self.mobility
        if self.world.pressedStatus['s']:
            for food in self.world.foods:
                food.vy -= self.mobility
            for enemy in self.world.enemies:
                enemy.vy -= self.mobility
        if self.world.pressedStatus['d']:
            for food in self.world.foods:
                food.vx -= self.mobility
            for enemy in self.world.enemies:
                enemy.vx -= self.mobility
        if self.world.pressedStatus['a']:
            for food in self.world.foods:
                food.vx += self.mobility
            for enemy in self.world.enemies:
                enemy.vx += self.mobility

    def checkFoodCollision(self):
        for food in self.world.foods:
            if (food.x - self.x) ** 2 + (food.y - self.y) ** 2 <= (self.renderSize / 2 - food.renderSize / 2) ** 2:
                self.world.canvas.delete(f'{food.id}')
                food.despawn()
                self.size += food.nutricity

    def checkCollision(self):
        for enemy in self.world.enemies:
            if (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2 <= (self.renderSize / 2 + enemy.renderSize / 2) ** 2:
                if self.size >= enemy.size:
                    self.size += 5
                    enemy.size -= 5
                    if (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2 <= (
                            self.renderSize / 2 - enemy.renderSize / 2) ** 2:
                        enemy.despawn()
                else:
                    enemy.size += 5
                    self.size -= 5
                    if (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2 <= (
                            self.renderSize / 2 - enemy.renderSize / 2) ** 2:
                        self.world.gameOn = False

    def update(self):
        def pressed(event):
            self.world.pressedStatus[event.keysym] = True

        def released(event):
            self.world.pressedStatus[event.keysym] = False

        for item in ['w', 's', 'a', 'd']:
            self.world.canvas.bind("<KeyPress-%s>" % item, pressed)
            self.world.canvas.bind("<KeyRelease-%s>" % item, released)

        for food in self.world.foods:
            food.y += food.vy
            food.x += food.vx
        for enemy in self.world.enemies:
            enemy.y += enemy.vy
            enemy.x += enemy.vx

        if self.world.currentFrame % 100 == 0:
            self.size *= 0.99
        self.world.scaling = self.renderSize / self.size
        self.moveWorld()
        self.render()


class Enemy:
    def __init__(self, world):
        self.size = random.randint(int(world.player.size / 5), int(world.player.size * 2))
        self.renderSize = self.size * world.scaling
        self.x = None
        self.y = None
        self.vx = None
        self.vy = None
        self.id = world.currentFrame
        self.world = world

    def spawn(self):
        rand_side = random.random()
        if 0 <= rand_side < 0.25:
            self.x = random.randint(self.world.player.x - self.world.xRenderSize,
                                    self.world.player.x + self.world.xRenderSize)
            self.y = random.randint(self.world.player.y - self.world.yRenderSize, 0)
        elif 0.25 <= rand_side < 0.5:
            self.x = random.randint(self.world.player.x - self.world.xRenderSize,
                                    self.world.player.x + self.world.xRenderSize)
            self.y = random.randint(self.world.yWindowSize,
                                    self.world.player.y + self.world.yRenderSize)
        elif 0.5 <= rand_side < 0.75:
            self.x = random.randint(self.world.player.x - self.world.xRenderSize, 0)
            self.y = random.randint(self.world.player.y - self.world.yRenderSize,
                                    self.world.player.y + self.world.yRenderSize)
        else:
            self.x = random.randint(self.world.xWindowSize,
                                    self.world.player.x + self.world.xRenderSize)
            self.y = random.randint(self.world.player.y - self.world.yRenderSize,
                                    self.world.player.y + self.world.yRenderSize)
        self.vx = self.world.player.vx
        self.vy = self.world.player.vy
        return self

    def despawn(self):
        for index, obj in enumerate(self.world.enemies):
            if obj.id == self.id:
                self.world.canvas.delete(f'{self.id}')
                del self.world.enemies[index]
                break

    def render(self):
        self.world.canvas.delete(f'enemy{self.id}')
        self.world.canvas.create_oval(self.x - self.renderSize / 2, self.y - self.renderSize / 2,
                                      self.x + self.renderSize / 2, self.y + self.renderSize / 2,
                                      fill=self.world.enemyColor, tags=f'enemy{self.id}')

    def checkFoodCollision(self):
        for food in self.world.foods:
            if (food.x - self.x) ** 2 + (food.y - self.y) ** 2 <= (self.renderSize / 2 - food.renderSize / 2) ** 2 \
                    and self.size > 20:
                self.world.canvas.delete(f'{food.id}')
                food.despawn()
                self.size += food.nutricity

    def checkCollision(self):
        for enemy in self.world.enemies:
            if (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2 <= (self.renderSize / 2 + enemy.renderSize / 2) ** 2 \
                    and enemy is not self:
                if self.size >= enemy.size:
                    self.size += 5
                    enemy.size -= 5
                    if (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2 <= (
                            self.renderSize / 2 - enemy.renderSize / 2) ** 2:
                        enemy.despawn()
                else:
                    enemy.size += 5
                    self.size -= 5
                    if (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2 <= (
                            self.renderSize / 2 - enemy.renderSize / 2) ** 2:
                        self.despawn()

    def hunt(self):
        dists = []
        objs = []
        for food in self.world.foods:
            dists.append(dist((self.x, self.y), (food.x, food.y)))
            objs.append(food)
        index_min = min(range(len(dists)), key=dists.__getitem__)
        if self.x < objs[index_min].x:
            self.x += self.world.player.mobility / 1.2 + random.randint(-2, 2)
        else:
            self.x -= self.world.player.mobility / 1.2 + random.randint(-2, 2)
        if self.y < objs[index_min].y:
            self.y += self.world.player.mobility / 1.2 + random.randint(-2, 2)
        else:
            self.y -= self.world.player.mobility / 1.2 + random.randint(-2, 2)

    def fleePursue(self):  # fix
        if dist((self.x, self.y), (self.world.player.x, self.world.player.y)) < self.world.player.renderSize:
            if self.renderSize < self.world.player.renderSize:
                if self.x < self.world.player.x:
                    self.x -= self.world.player.mobility / 1.2 + random.randint(-2, 2)
                else:
                    self.x += self.world.player.mobility / 1.2 + random.randint(-2, 2)
                if self.y < self.world.player.y:
                    self.y -= self.world.player.mobility / 1.2 + random.randint(-2, 2)
                else:
                    self.y += self.world.player.mobility / 1.2 + random.randint(-2, 2)
            else:
                if self.x < self.world.player.x:
                    self.x += self.world.player.mobility / 1.2 + random.randint(-2, 2)
                else:
                    self.x -= self.world.player.mobility / 1.2 + random.randint(-2, 2)
                if self.y < self.world.player.y:
                    self.y += self.world.player.mobility / 1.2 + random.randint(-2, 2)
                else:
                    self.y -= self.world.player.mobility / 1.2 + random.randint(-2, 2)
        pass

    def update(self):
        if self.world.currentFrame % 100 == 0:
            self.size *= 0.99
        self.render()
        self.vx, self.vy = self.vx / 1.7, self.vy / 1.7
        self.renderSize = self.size * self.world.scaling
        self.hunt()
        self.fleePursue()


class Food:
    def __init__(self, world):
        self.nutricity = 5
        self.renderSize = 20 * world.scaling
        self.x = None
        self.y = None
        self.vx = None
        self.vy = None
        self.id = world.currentFrame
        self.world = world

    def render(self):
        self.world.canvas.delete(f'food{self.id}')
        self.world.canvas.create_oval(self.x - self.renderSize / 2, self.y - self.renderSize / 2,
                                      self.x + self.renderSize / 2, self.y + self.renderSize / 2,
                                      fill=self.world.foodColor, tags=f'food{self.id}')

    def spawn(self):
        self.x = random.randint(self.world.player.x - self.world.xRenderSize,
                                self.world.player.x + self.world.xRenderSize)
        self.y = random.randint(self.world.player.y - self.world.yRenderSize,
                                self.world.player.y + self.world.yRenderSize)
        self.vx = self.world.player.vx
        self.vy = self.world.player.vy
        return self

    def despawn(self):
        for index, food in enumerate(self.world.foods):
            if food.id == self.id:
                self.world.canvas.delete(f'{self.id}')
                del self.world.foods[index]
                break

    def update(self):
        self.render()
        self.vx, self.vy = self.vx / 1.7, self.vy / 1.7
        self.renderSize = 20 * self.world.scaling


def entitySpawner(world):
    if world.currentFrame % 5 == 0 and len(world.foods) < world.foodsLimit:
        food = Food(world)
        world.foods.append(food.spawn())
    if world.currentFrame % 50 == 0 and len(world.enemies) < world.enemiesLimit:
        enemy = Enemy(world)
        world.enemies.append(enemy.spawn())


def entityDespawner(world):
    for food in world.foods:
        if food.x < world.player.x - world.xRenderSize or food.x > world.player.x + world.xRenderSize or \
                food.y < world.player.y - world.yRenderSize or food.y > world.player.y + world.yRenderSize:
            food.despawn()
    for enemy in world.enemies:
        if enemy.x < world.player.x - world.xRenderSize or enemy.x > world.player.x + world.xRenderSize or \
                enemy.y < world.player.y - world.yRenderSize or enemy.y > world.player.y + world.yRenderSize \
                or world.player.renderSize < 20:
            enemy.despawn()
    if world.player.renderSize < 20:
        world.gameOn = False


def entityUpdater(world):
    for food in world.foods:
        food.update()
    for enemy in world.enemies:
        enemy.update()


def consumeCheck(world):
    world.player.checkFoodCollision()
    world.player.checkCollision()
    for enemy in world.enemies:
        enemy.checkFoodCollision()
        enemy.checkCollision()


def updateUI(world):
    world.canvas.delete('all')
    world.canvas.create_text(world.xWindowSize / 8, world.yWindowSize / 20,
                             fill='white', text=f'SCORE: {int(world.player.size)}',
                             font=(f'Helvetica', f'{int(world.xWindowSize / 30)}', 'bold'),
                             tags='ui')
    world.canvas.tag_raise('ui')


def gameplay(world):
    if world.gameOn is True:
        updateUI(world)
        world.player.update()
        entitySpawner(world)
        entityDespawner(world)
        entityUpdater(world)
        consumeCheck(world)
        world.currentFrame += 1
        world.root.after(10, gameplay, world)
    else:
        world.restart()


def main():
    world = World()
    player = Player(world)
    world.setup(player)
    gameplay(world)
    mainloop()


if __name__ == '__main__':
    main()
