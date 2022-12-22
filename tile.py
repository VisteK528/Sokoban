import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("Textures/Tile.png")
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.position = pygame.math.Vector2(x, y)

    def update_visual(self, tile_size):
        self.rect.x = self.position.x * tile_size
        self.rect.y = self.position.y * tile_size
