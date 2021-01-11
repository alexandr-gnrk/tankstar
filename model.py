import os
import functools

import pygame

from tank import Tank
from obstacle import Obstacle
from projectile import Projectile

class Model():
    """Class that represents game state."""

    FIELD_TEMPLATE = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]

    def __init__(self):
        # create an empty field
        self.size = (len(self.FIELD_TEMPLATE), len(self.FIELD_TEMPLATE[0]))
        self.field = [[None] * self.size[0] for _ in range(self.size[1])]
        
        self.player = Tank([1, 1])
        self.obstacles = self.make_obstacles_from_template(self.FIELD_TEMPLATE)
        self.tanks = [
            self.player,
            Tank([1, 7])
        ]
        self.projectiles = list()

        self.actions_map = dict()

    def make_obstacles_from_template(self, template):
        obstacles = list()
        for i in range(len(template)):
            for j in range(len(template[i])):
                if template[i][j] == 1:
                    obstacles.append(Obstacle([i, j]))
        return obstacles

    def update_field_state(self):
        self.field = [[None] * self.size[0] for _ in range(self.size[1])]
        objs = self.tanks + self.obstacles + self.projectiles
        for obj in objs:
            self.field[obj.pos[0]][obj.pos[1]] = obj

    def is_outside(self, obj):
        if obj.pos[0] < 0 or obj.pos[0] >= self.size[0] or \
                obj.pos[1] < 0 or obj.pos[1] >= self.size[1]:
            return True
        return False

    def update(self):
        # eval actions
        for action in self.actions_map.values():
            action()
        
        # move tanks
        for tank in self.tanks:
            for obstacle in self.obstacles:
                if tank.pos == obstacle.pos:
                    last_backward_arg = self.actions_map[tank].args[0] 
                    tank.move(not last_backward_arg)

        # move projctiles
        for projectile in self.projectiles:
            for obstacle in self.obstacles:
                if projectile.pos == obstacle.pos:
                    self.projectiles.remove(projectile)

            for tank in self.tanks:
                if projectile.pos == tank.pos:
                    self.tanks.remove(tank)
                    self.projectiles.remove(projectile)

            for second_projectile in self.projectiles:
                if projectile is not second_projectile and \
                        projectile.pos == second_projectile.pos:
                    self.projectile.remove(projectile)
                    self.projectiles.remove(second_projectile)
        
        # remove all actions and actions to move projectiles in the
        # next update call
        self.actions_map.clear()
        for projectile in self.projectiles:
            self.add_move_action(projectile)

        self.update_field_state()

    def add_move_action(self, obj, backward=False):
        self.actions_map[obj] = functools.partial(obj.move, backward)

    def add_turn_action(self, tank, ACW=False):
        self.actions_map[tank] = functools.partial(tank.turn, ACW)

    def add_shoot_action(self, tank):
        def shoot(tank): self.projectiles.append(tank.shoot())
        self.actions_map[tank] = functools.partial(shoot, tank)

    def dump(self):
        os.system('clear')
        def to_char(obj):
            if obj is None:
                # return '◦'
                return ' '
            elif isinstance(obj, Obstacle):
                return '▩'
            elif isinstance(obj, Projectile):
                return '●'
            elif isinstance(obj, Tank):
                if obj.directon == [1, 0]:
                    return '▼'
                elif obj.directon == [-1, 0]:
                    return '▲'
                elif obj.directon == [0, -1]:
                    return '◀'
                elif obj.directon == [0, 1]:
                    return '▶'
            raise Exception()

        for i in range(self.size[0]):
            for j in range(self.size[1]):
                print(to_char(self.field[i][j]), end=' ')
            print()