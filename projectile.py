from operator import add

from gameobject import GameObject


class Projectile(GameObject):
    def __init__(self, pos, direction):
        super().__init__(pos, direction)

    def move(self, backward=False):
        if backward == True:
            raise Exception('Bullet can not move backward')
        self.pos = self.add_lists(self.pos, self.direction)
    
    def choose_next_update_action(self, matrix):
        self.next_update_action = self.move