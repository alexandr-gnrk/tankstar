import operator
from gameobject import GameObject
from projectile import Projectile
from functools import partial

from astar import AStar


class Tank(GameObject):
    def __init__(self, pos, direction=None):
        direction = [1, 0] if direction is None else direction
        super().__init__(pos, direction)

    def turn(self, ACW=False): # ACW -> anticlockwise
        # swap components
        self.direction = self.rotate_direction(self.direction, ACW)

    def move(self, backward=False):
        delta = [-1*x for x in self.direction] if backward else self.direction
        self.pos = self.move_pos_by_delta(self.pos, delta)

    def shoot(self):
        proj = Projectile(self.pos, self.direction)
        proj.move()
        return proj


class PlayerTank(Tank):
    def __init__(self, pos, direction=None):
        super().__init__(pos, direction)

    def choose_next_update_action(self, matrix):
        self.next_update_action = None


class AITank(Tank):
    @classmethod
    def find_player(cls, matrix):
        for line in matrix:
            for obj in line:
                if isinstance(obj, PlayerTank):
                    return obj

        raise Exception('Unable to find player')


    @classmethod
    def find_free_cell_around_pos(cls, pos, matrix):
        diffs = ((1, 0), (-1, 0), (0, 1), (0, -1))
        for diff in diffs:
            possible_pos = cls.move_pos_by_delta(pos, diff)
            if matrix[possible_pos[0]][possible_pos[1]] is None:
                return possible_pos

        raise Exception('There is no free cell around')

    @classmethod
    def covert_to_binary_matrix(cls, matrix):
        new_matrix = list()
        for line in matrix:
            new_matrix.append(list())
            for cell in line:
                if cell is None or isinstance(cell, Projectile):
                    new_matrix[-1].append(0)
                else:
                    new_matrix[-1].append(1)

        return new_matrix 
        
    def define_action_according_next_pos(self, next_pos):
        # delta_pos = list(map(operator.sub, self.pos, pos))
        if self.move_pos_by_delta(self.pos, self.direction) == next_pos:
            return partial(self.move, backward=False)

        antidirection = [-self.direction[0], -self.direction[1]]
        if self.move_pos_by_delta(self.pos, antidirection):
            return partial(self.move, backward=True)

        delta_pos = list(map(operator.sub, pos, self.pos))
        if self.rotate_direction(self.direction) == delta_pos:
            return partial(self.turn, ACW=False)
        elif self.rotate_direction(self.direction, ACW=True) == delta_pos:
            return partial(self.turn, ACW=True)

        raise Exception('No possible action found')


class FrontTank(AITank):
    def choose_next_update_action(self, matrix):
        self.player_tank = self.find_player(matrix)
        # find pos in front of player tank
        target_pos = self.move_pos_by_delta(
            self.player_tank.pos,
            self.player_tank.direction)
        if matrix[target_pos[0]][target_pos[1]] is not None:
            target_pos = self.find_free_cell_around_pos(
                self.player_tank.pos, 
                matrix)

        next_pos = AStar(
            self.pos, 
            target_pos, 
            self.covert_to_binary_matrix(matrix)).solve()[0]

        self.next_update_action = self.define_action_according_next_pos(
            next_pos)




# class RearTank(Tank):

#     def __init__(self, arg):
#         super(RearTank, self).__init__()
#         self.arg = arg
        
#         