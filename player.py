import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("Textures/Player.png")
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 50
        self._clicked = False

        self.moves = 0
        self.pushes = 0

        self.moves = 0
        self.pushes = 0

    def get_input(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_w] and not self._clicked:
            self.direction.x = 0
            self.direction.y = -1
            self._clicked = True
        elif key[pygame.K_s] and not self._clicked:
            self.direction.x = 0
            self.direction.y = 1
            self._clicked = True
        elif key[pygame.K_a] and not self._clicked:
            self.direction.x = -1
            self.direction.y = 0
            self._clicked = True
        elif key[pygame.K_d] and not self._clicked:
            self.direction.x = 1
            self.direction.y = 0
            self._clicked = True
        else:
            self.direction.x = 0
            self.direction.y = 0

        if not (key[pygame.K_a] or
                key[pygame.K_d] or
                key[pygame.K_w] or
                key[pygame.K_s]):
            self._clicked = False

    def update(self):
        self.get_input()
