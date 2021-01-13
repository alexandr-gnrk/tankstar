import operator
import random
from gameobject import GameObject
from projectile import Projectile
from functools import partial
from abc import abstractmethod

from astar import AStar


class Tank(GameObject):
    def __init__(self, pos, direction=None):
        direction = [1, 0] if direction is None else direction
        super().__init__(pos, direction)

    def turn(self, ACW=False): # ACW -> anticlockwise
        # swap components
        self.direction = self.rotate_direction(self.direction, ACW)

    def move(self, backward=False):
        if backward:
            self.pos = self.sub_lists(self.pos, self.direction)
        else:
            self.pos = self.add_lists(self.pos, self.direction)

    def shoot(self):
        proj = Projectile(self.pos, self.direction)
        proj.move()
        return proj

    def next_update_pos(self):
        return self.add_lists(self.pos, self.direction)


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
            possible_pos = cls.add_lists(pos, diff)
            if matrix[possible_pos[0]][possible_pos[1]] is None:
                return possible_pos

        # there is no free cell around
        return None

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

    def is_on_shooting_line(self, obj, matrix):
        next_pos = self.add_lists(self.pos, self.direction)

        while matrix[next_pos[0]][next_pos[1]] is None:
            next_pos = self.add_lists(next_pos, self.direction)

        if matrix[next_pos[0]][next_pos[1]] is obj:
            return True
        return False

    def get_turn_action(self, new_direction):
        if self.rotate_direction(self.direction) == new_direction:
            return partial(self.turn, ACW=False)
        else:
            return partial(self.turn, ACW=True)

    def get_shoot_action(self):
        return partial(self.shoot)

    def get_random_action(self):
        return random.choice([
            partial(self.turn, ACW=False),
            partial(self.turn, ACW=True),
            partial(self.move, backward=False),
            partial(self.move, backward=True),
            partial(self.shoot)])

    def get_action_according_next_pos(self, next_pos):
        # delta_pos = list(map(operator.sub, self.pos, pos))
        if self.add_lists(self.pos, self.direction) == list(next_pos):
            return partial(self.move, backward=False)

        if self.sub_lists(self.pos, self.direction) == list(next_pos):
            return partial(self.move, backward=True)

        new_direction = self.sub_lists(next_pos, self.pos)
        return self.get_turn_action(new_direction)

    def choose_next_update_action(self, matrix):
        if random.choices([True, False], [40, 60], k=1)[0]:
            self.next_update_action = None
            return

        player_tank = self.find_player(matrix)

        if self.is_on_shooting_line(player_tank, matrix):
            if random.choices([True, False], [50, 50], k=1)[0]:
                self.next_update_action = self.get_shoot_action()
                return

        manhattan_distance_to_target = \
            abs(player_tank.pos[0] - self.pos[0]) + \
            abs(player_tank.pos[1] - self.pos[1])

        if manhattan_distance_to_target == 1:
            if self.next_update_pos() == player_tank.pos:
                self.next_update_action = self.get_shoot_action()
            else:
                new_direction = self.sub_lists(player_tank.pos, self.pos)
                self.next_update_action = self.get_turn_action(new_direction)
        else:
            next_pos = self.define_next_pos(player_tank, matrix)

            if next_pos is None:
                self.next_update_action = self.get_random_action()
            else:
                self.next_update_action = self.get_action_according_next_pos(
                    next_pos)

    @abstractmethod
    def define_next_pos(self):
        pass

    def next_pos_to_player(self, player_tank, matrix, rear=False):
        # find pos in front of player tank
        if rear:
            next_pos = self.sub_lists(
                player_tank.pos,
                player_tank.direction)
        else:            
            next_pos = self.add_lists(
                player_tank.pos,
                player_tank.direction)

        next_cell = matrix[next_pos[0]][next_pos[1]]
        if next_cell is not None:
            next_pos = self.find_free_cell_around_pos(
                player_tank.pos, 
                matrix)
            if next_pos is None:
                return self.next_pos_primitive(player_tank, matrix)

        trace = AStar(
            self.pos, 
            next_pos, 
            self.covert_to_binary_matrix(matrix)).solve()

        if trace is None:
            return self.next_pos_primitive(player_tank, matrix)
        else:
            return trace[0]

    def next_pos_primitive(self, player_tank, matrix):
        next_pos = self.next_update_pos()
        if matrix[next_pos[0]][next_pos[1]] is None:
            return next_pos

        cw_pos = self.add_lists(
            self.pos, 
            self.rotate_direction(self.direction, ACW=False))
        acw_pos = self.add_lists(
            self.pos, 
            self.rotate_direction(self.direction, ACW=True))
        cw_cell = matrix[cw_pos[0]][cw_pos[1]]        
        acw_cell = matrix[acw_pos[0]][acw_pos[1]]

        if (cw_cell is None and acw_cell is None) or \
                (cw_cell is not None and acw_cell is not None):
            return random.choice([cw_pos, acw_pos])
        elif cw_cell is None:
            return cw_pos
        else:
            return acw_pos

class FrontTank(AITank):

    def define_next_pos(self, player_tank, matrix):
        return self.next_pos_to_player(player_tank, matrix)


class RearTank(AITank):

    def define_next_pos(self, player_tank, matrix):
        return self.next_pos_to_player(player_tank, matrix, rear=True)


class PrimitiveTank(AITank):

    def define_next_pos(self, player_tank, matrix):
        return self.next_pos_primitive(player_tank, matrix)
