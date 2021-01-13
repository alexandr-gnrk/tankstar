from gameobject import GameObject


class Obstacle(GameObject):
    def __init__(self, pos):
        super().__init__(pos, None)
    
    def choose_next_update_action(self, matrix):
        self.next_update_action = None