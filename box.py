import pygame


class Box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self._default_image = pygame.image.load("Textures/Box.png")
        self._change_image = pygame.image.load("Textures/Box_2.png")
        self.set_default_image()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 50

    def set_default_image(self):
        self.image = self._default_image

    def set_change_image(self):
        self.image = self._change_image
