import pygame
from box import Box
from box_target import BoxTarget
from player import Player
from tile import Tile
from load_level import LoadLevel
from settings import textures_id_dict


class Level(LoadLevel):
    def __init__(self, width, height, level=1, tile_size=50):
        super().__init__(width, height, tile_size)
        self._level = level

        if level is None:
            self._level_data = {
                row: {
                    col: 0 for col in range(self._columns)
                    } for row in range(self._rows)}
        else:
            self._level_data = self.load_level(
                f"Levels/Level{self._level}_data.json")

    def draw_grid(self, window, color="white"):
        for row_count in range(self._rows+1):
            pygame.draw.line(
                window, color,
                (0, row_count * self._tile_size),
                (self._width, row_count*self._tile_size))
        for column_count in range(self._columns+1):
            pygame.draw.line(
                window, color,
                (column_count*self._tile_size, 0),
                (column_count * self._tile_size, self._height))

    def draw_text(self, window, text, font, color,  x, y):
        img = font.render(text, True, color)
        window.blit(img, (x, y))

    def setup(self):
        self._tiles = pygame.sprite.Group()
        self._boxes = pygame.sprite.Group()
        self._boxes_targets = pygame.sprite.Group()
        self._player = pygame.sprite.GroupSingle()
        self._player_placed = False
        for row in range(self._rows):
            for column in range(self._columns):
                texture_id = self._level_data[str(row)][str(column)]
                y = row * self._tile_size
                x = column * self._tile_size
                if texture_id == textures_id_dict["player"]:
                    # Player
                    self._player.add(Player(x, y))
                    self._player_placed = True
                elif texture_id == textures_id_dict["box_target"]:
                    # BoxTarget
                    self._boxes_targets.add(BoxTarget(x, y))
                elif texture_id == textures_id_dict["box"]:
                    # Box
                    self._boxes.add(Box(x, y))
                elif texture_id == textures_id_dict["tile"]:
                    # Tile
                    self._tiles.add(Tile(x, y))

    def run(self, window):
        self._boxes_targets.update()
        self._player.update()
        self._boxes.update()
        self._tiles.update()
        self._boxes_targets.draw(window)
        self._player.draw(window)
        self._boxes.draw(window)
        self._tiles.draw(window)
