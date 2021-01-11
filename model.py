import os

import pygame

from tank import Tank
from obstacle import Obstacle

class Model():
    """Class that represents game state."""

    def __init__(self, size):
        # create an empty field
        self.size = size
        self.field = [[None] * size[0] for _ in range(size[1])]
        
        self.player = Tank([0, 1])
        self.obstacles = [
            Obstacle([0, 2]),
            Obstacle([1, 2]),
            Obstacle([3, 2]),
            Obstacle([3, 1]),
            Obstacle([3, 0]),
        ]
        self.tanks = [
            self.player
        ]

        self.update_field()

    def update_field(self):
        self.field = [[None] * self.size[0] for _ in range(self.size[1])]
        objs = self.tanks + self.obstacles
        for obj in objs:
            self.field[obj.pos[0]][obj.pos[1]] = obj

    def move(self, tank, backward=False):
        tank.move(backward)
        if self.field[tank.pos[0]][tank.pos[1]] is not None:
            tank.move(not backward)

    def turn(self, tank, ACW=False):
        tank.turn(ACW)

    def dump(self):
        os.system('clear')
        self.update_field()
        def to_char(obj):
            if obj is None:
                return '◦'
            elif isinstance(obj, Obstacle):
                return '▩'
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