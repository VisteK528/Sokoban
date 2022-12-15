import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("Textures/Tile.png")
        self.rect = self.image.get_rect(topleft=(x, y))
