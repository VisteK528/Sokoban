import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.position = pygame.math.Vector2(x, y)

    def update_visual(self, tile_size: int):
        """
        Updates the screen position of the Entity
        based on current level position and size of one tile
        """
        self.rect.x = self.position.x * tile_size
        self.rect.y = self.position.y * tile_size


class Player(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.image = pygame.image.load("Textures/Player.png")
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.direction = pygame.math.Vector2(0, 0)

        self.moves = 0
        self.pushes = 0


class Tile(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.image = pygame.image.load("Textures/Tile.png")
        self.rect = self.image.get_rect(topleft=(0, 0))


class Box(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self._default_image = pygame.image.load("Textures/Box.png")
        self._change_image = pygame.image.load("Textures/Box_2.png")
        self.set_default_image()
        self.rect = self.image.get_rect(topleft=(0, 0))

    def set_default_image(self):
        self.image = self._default_image

    def set_change_image(self):
        self.image = self._change_image


class BoxTarget(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.image = pygame.image.load("Textures/Box_target.png")
        self.rect = self.image.get_rect(topleft=(0, 0))
