import pygame


class BoxTarget(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("Textures/Box_target.png")
        self.rect = self.image.get_rect(topleft=(x, y))
