# ivandavy 2022

import random
import time
from numpy import *
from tkinter import *
from world import *
from player import *
from wall import *
from ray import *


def cleanup(world):
    world.canvas.delete('ray')
    world.canvas.delete('intersect')
    world.canvas.delete('strip')


def gameplay(world):
    if world.game_on is True:
        world.player.update(world.view)
        cleanup(world)
        ray_num = 0
        for ang in world.player.rayDirections:
            ray = Ray(world, ang)
            if world.view == 'top':
                ray.renderTop()
                ray.shade()
            if world.view == 'pov':
                ray.shade()
                ray.renderPov(ray_num)
            ray_num += 1
        world.current_frame += 1
        print(world.player.x, world.player.y)
        world.root.after(10, gameplay, world)
    else:
        world.restart()


def main():
    world = World()
    level = [
        Wall(world.x_level_size / 4, 0.1, world.x_level_size, 0.1, world),
        Wall(0.1, world.y_level_size / 4, 0.1, world.y_level_size, world),
        Wall(0.1, world.y_level_size / 4, world.x_level_size / 4, world.y_level_size / 4, world),
        Wall(world.x_level_size / 4, world.y_level_size / 4, world.x_level_size / 4, 0.1, world),

        Wall(0.1, world.y_level_size, 3 * world.x_level_size / 4, world.y_level_size, world),
        Wall(3 * world.x_level_size / 4, world.y_level_size, 3 * world.x_level_size / 4, world.y_level_size / 2, world),
        Wall(3 * world.x_level_size / 4, world.y_level_size / 2, world.x_level_size, world.y_level_size / 2, world),
        Wall(world.x_level_size, 0.1, world.x_level_size, world.y_level_size, world),
    ]
    player = Player(world)
    world.setup(player, level)
    gameplay(world)
    mainloop()


if __name__ == '__main__':
    main()
