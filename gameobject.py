from abc import ABC, abstractmethod
from operator import add


class GameObject(ABC):
    @abstractmethod
    def __init__(self, pos, direction):
        self.pos = list(pos)
        self.direction = None if direction is None else list(direction)
        self.next_update_action = None

    @abstractmethod
    def choose_next_update_action(self, matrix):
        pass
        
    def make_action(self):
        if self.next_update_action is not None:
            return self.next_update_action()
        return None

    @classmethod
    def move_pos_by_delta(cls, pos, delta):
        return list(map(add, pos, delta))

    @classmethod
    def rotate_direction(cls, direction, ACW=False):
        direction = list(direction)[::-1]
        
        if ACW:
            direction[0] *= -1
        else:
            direction[1] *= -1
        
        return direction