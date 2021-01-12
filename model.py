import os
import functools

from tank import Tank, PlayerTank, FrontTank, RearTank
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
    FIELD_TEMPLATE = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]
        


    def __init__(self):
        # create an empty field
        self.size = (len(self.FIELD_TEMPLATE), len(self.FIELD_TEMPLATE[0]))
        self.field = [[None] * self.size[0] for _ in range(self.size[1])]
        self.player = PlayerTank([4, 1])
        self.obstacles = self.make_obstacles_from_template(self.FIELD_TEMPLATE)
        self.tanks = [
            self.player,
            FrontTank([4, 7]),
            RearTank([5, 7])
        ]
        self.projectiles = list()
        self.update_field_state()

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
        new_projectiles = list()
        for tank in self.tanks:
            obj = tank.make_action()
            if obj is not None:
                new_projectiles.append(obj)

        # move tanks
        for tank in self.tanks:
            for obstacle in self.obstacles:
                if tank.pos == obstacle.pos:
                    last_backward_arg = tank.next_update_action.keywords['backward']
                    tank.move(not last_backward_arg)

        # move projctiles
        for projectile in self.projectiles:
            positions = [
                projectile.pos, 
                projectile.add_lists(
                    projectile.pos,
                    projectile.direction)]
            for obstacle in self.obstacles:
                if obstacle.pos in positions:
                    self.projectiles.remove(projectile)

            for tank in self.tanks:
                if tank.pos in positions:
                    self.tanks.remove(tank)
                    self.projectiles.remove(projectile)

            for second_projectile in self.projectiles:
                if projectile is not second_projectile and \
                        second_projectile.pos in positions:
                    self.projectile.remove(projectile)
                    self.projectiles.remove(second_projectile)

        for projectile in self.projectiles: projectile.make_action()

        self.update_field_state()

        # remove all actions and actions to move projectiles in the
        # next update call
        for tank in self.tanks: tank.choose_next_update_action(self.field)
        for projectile in self.projectiles: projectile.choose_next_update_action(self.field)


        self.projectiles.extend(new_projectiles)

    def add_move_action(self, obj, backward=False):
        obj.next_update_action = functools.partial(obj.move, backward=backward)

    def add_turn_action(self, obj, ACW=False):
        obj.next_update_action = functools.partial(obj.turn, ACW=ACW)

    def add_shoot_action(self, obj):
        obj.next_update_action = functools.partial(obj.shoot)

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
                if obj.direction == [1, 0]:
                    return '▼'
                elif obj.direction == [-1, 0]:
                    return '▲'
                elif obj.direction == [0, -1]:
                    return '◀'
                elif obj.direction == [0, 1]:
                    return '▶'
            raise Exception()

        for i in range(self.size[0]):
            for j in range(self.size[1]):
                print(to_char(self.field[i][j]), end=' ')
            print()
        # print(self.tanks[-1].next_update_action)