from operator import add

class Projectile():
    def __init__(self, pos, direction):
        self.pos = list(pos)
        self.direction = list(direction)

    def move(self, backward=False):
        if backward == True:
            raise Exception('Bullet can not move backward')
        self.pos = list(map(add, self.pos, self.direction))
        