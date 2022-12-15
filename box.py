import pygame


class Box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("Textures/Box.png")
        self.rect = self.image.get_rect(topleft=(x, y))
