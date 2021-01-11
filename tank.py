from operator import add


class Tank():

    DIRECTIONS = ([1, 0], [0, -1], [-1, 0], [0, 1])

    def __init__(self, pos, directon=None):
        self.pos = list(pos)
        self.directon = [1, 0] if directon is None else list(directon)

    def turn(self, ACW=False): # ACW -> anticlockwise
        # swap components
        self.directon = self.directon[::-1]
        
        if ACW:
            self.directon[0] *= -1
        else:
            self.directon[1] *= -1

    def move(self, backward=False):
        delta = [-1*x for x in self.directon] if backward else self.directon
        self.pos = list(map(add, self.pos, delta))
