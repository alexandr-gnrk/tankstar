import pygame

from tank import Tank

class Model():
    """Class that represents game state."""

    def __init__(self, size):
        # list of all objects
        self.objs = list()
        # create an empty field
        self.size = size
        self.field = [[None] * size[0] for _ in range(size[1])]
        
        self.player = Tank([0, 1])
        self.objs.append(self.player)
        self.update_field()

    def update_field(self):
        self.field = [[None] * self.size[0] for _ in range(self.size[1])]
        for obj in self.objs:
            self.field[obj.pos[0]][obj.pos[1]] = obj

    def dump(self):
        self.update_field()
        def to_char(obj):
            if obj is None:
                return '◦'
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