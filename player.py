import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("Textures/Player.png")
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 50

        self.moves = 0
        self.pushes = 0

    def get_input(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_w]:
            self.direction.x = 0
            self.direction.y = -1
        elif key[pygame.K_s]:
            self.direction.x = 0
            self.direction.y = 1
        elif key[pygame.K_a]:
            self.direction.x = -1
            self.direction.y = 0
        elif key[pygame.K_d]:
            self.direction.x = 1
            self.direction.y = 0
        else:
            self.direction.x = 0
            self.direction.y = 0

    def update(self):
        self.get_input()
