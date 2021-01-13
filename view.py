import pygame
from obstacle import Obstacle
from projectile import Projectile
from tank import PlayerTank, FrontTank, RearTank, PrimitiveTank


class View():
    """"Class that displays model state and shows HUD"""

    BACKGROUND_COLOR = (0, 0, 0)

    FPS = 30
    UPDATE_TIME_DELAY = (1/5)*1000

    SPRITE_LEN = 64
    SPRITE_SIZE = (SPRITE_LEN, SPRITE_LEN)

    def __init__(self, model):
        pygame.init()
    
        self.model = model
        self.screen = pygame.display.set_mode((
            self.model.size[0]*self.SPRITE_LEN, 
            self.model.size[1]*self.SPRITE_LEN))
        self.width, self.height = self.screen.get_size()
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.time_from_last_update = 0

        self.imgs = {
            'brick': pygame.transform.scale(
                pygame.image.load('./sprites/brick.png'), self.SPRITE_SIZE),
            'projectile': pygame.transform.scale(
                pygame.image.load('./sprites/projectile.png'), self.SPRITE_SIZE),
            'gray_tank': pygame.transform.scale(
                pygame.image.load('./sprites/gray_tank.png'), self.SPRITE_SIZE),
            'green_tank': pygame.transform.scale(
                pygame.image.load('./sprites/green_tank.png'), self.SPRITE_SIZE),
            'red_tank': pygame.transform.scale(
                pygame.image.load('./sprites/red_tank.png'), self.SPRITE_SIZE),
            'yellow_tank': pygame.transform.scale(
                pygame.image.load('./sprites/yellow_tank.png'), self.SPRITE_SIZE),
        }
        # optimize images
        for img in self.imgs.values(): img.convert()

    def redraw(self):
        """Redraw screen according to model of game."""
        self.screen.fill(View.BACKGROUND_COLOR)

        for i in range(self.model.size[0]):
            for j in range(self.model.size[1]):
                obj = self.model.field[i][j]
                if obj is None:
                    continue

                img = self.obj_to_img(obj)
                rect = img.get_rect()
                rect.topleft = j*self.SPRITE_LEN, i*self.SPRITE_LEN
                self.screen.blit(img, rect)

        pygame.display.flip()
        # pygame.display.update()

    def obj_to_img(self, obj):
        img_mapping = {
            Obstacle: self.imgs['brick'],
            Projectile: self.imgs['projectile'],
            PlayerTank: self.imgs['green_tank'],
            FrontTank: self.imgs['red_tank'],
            RearTank: self.imgs['yellow_tank'],
            PrimitiveTank: self.imgs['gray_tank'],
        }
        degrees_mapping = {
            (-1, 0): 0,
            (1, 0): 180,
            (0, 1): -90,
            (0, -1): 90,
        }
        img = img_mapping[type(obj)]
        degrees = degrees_mapping[tuple(obj.direction)]
        rotated_img = pygame.transform.rotate(img, degrees)
        return rotated_img

    def is_player_alive(self):
        return isinstance(self.model.tanks[0], PlayerTank)

    def start(self):
        """Start game loop."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        exit()
                    elif event.key == pygame.K_r:
                        self.model.reset()
                    elif event.key == pygame.K_UP:
                        self.model.add_move_action(
                            self.model.player, backward=False)
                    elif event.key == pygame.K_DOWN:
                        self.model.add_move_action(
                            self.model.player, backward=True)
                    elif event.key == pygame.K_RIGHT:
                        self.model.add_turn_action(
                            self.model.player, ACW=False)
                    elif event.key == pygame.K_LEFT:
                        self.model.add_turn_action(
                            self.model.player, ACW=True)
                    elif event.key == pygame.K_SPACE:
                        self.model.add_shoot_action(self.model.player)

            self.redraw()
            if self.is_player_alive() and \
                    self.time_from_last_update >= self.UPDATE_TIME_DELAY:
                self.update()
                self.time_from_last_update = 0

            self.time_from_last_update += self.clock.tick(self.FPS)

    def update(self):
        self.model.update()

    def delta_time(self):
        return self.clock.tick(self.fps) / 1000