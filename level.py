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

    def horizontal_collision(self):
        player = self._player.sprite
        player.rect.x += player.direction.x * player.speed

        boxes = self._boxes.sprites()
        for i, box in enumerate(boxes):
            if box.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    box.rect.x += player.direction.x * player.speed
                    player.rect.left = box.rect.right
                elif player.direction.x > 0:
                    box.rect.x += player.direction.x * player.speed
                    player.rect.right = box.rect.left

        for i, box in enumerate(boxes):
            for box2 in boxes[i+1:]:
                if box.rect.colliderect(box2):
                    player.rect.x -= player.direction.x * player.speed
                    box.rect.x -= player.direction.x * player.speed
                    if (box.rect.x - box.rect.width) == box2.rect.x:
                        box.rect.left = box2.rect.right
                    else:
                        box.rect.right = box2.rect.left

        for tile in self._tiles.sprites():
            if tile.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = tile.rect.right
                elif player.direction.x > 0:
                    player.rect.right = tile.rect.left
            for box in boxes:
                if tile.rect.colliderect(box.rect):
                    player.rect.x -= player.direction.x * player.speed
                    if player.direction.x < 0:
                        box.rect.left = tile.rect.right
                    elif player.direction.x > 0:
                        box.rect.right = tile.rect.left

    def vertical_collision(self):
        player = self._player.sprite
        player.rect.y += player.direction.y * player.speed

        boxes = self._boxes.sprites()
        for box in boxes:
            if box.rect.colliderect(player.rect):
                if player.direction.y < 0:
                    box.rect.y += player.direction.y * player.speed
                    player.rect.top = box.rect.bottom
                elif player.direction.y > 0:
                    box.rect.y += player.direction.y * player.speed
                    player.rect.bottom = box.rect.top

        for i, box in enumerate(boxes):
            for box2 in boxes[i+1:]:
                if box.rect.colliderect(box2):
                    player.rect.y -= player.direction.y * player.speed
                    box.rect.y -= player.direction.y * player.speed
                    if (box.rect.y - box.rect.height) == box2.rect.y:
                        box.rect.top = box2.rect.bottom
                    else:
                        box.rect.bottom = box2.rect.top

        for tile in self._tiles.sprites():
            if tile.rect.colliderect(player.rect):
                if player.direction.y < 0:
                    player.rect.top = tile.rect.bottom
                elif player.direction.y > 0:
                    player.rect.bottom = tile.rect.top
            for box in boxes:
                if tile.rect.colliderect(box.rect):
                    player.rect.y -= player.direction.y * player.speed
                    if player.direction.y < 0:
                        box.rect.top = tile.rect.bottom
                    elif player.direction.y > 0:
                        box.rect.bottom = tile.rect.top

    def box_collision_with_target(self):
        boxes = self._boxes
        targets = self._boxes_targets
        completed_boxes = 0
        for box in boxes:
            box.set_default_image()
        for box in boxes:
            for target in targets:
                if box.rect.x == target.rect.x and box.rect.y == target.rect.y:
                    box.set_change_image()
                    completed_boxes += 1
        if completed_boxes == len(targets):
            return True
        else:
            return False

    def run(self, window):
        self.horizontal_collision()
        self.vertical_collision()
        # tiles
        self._tiles.update()

        # boxes targets
        self._boxes_targets.update()

        # boxes
        self._boxes.update()

        # player
        self._player.update()

        self.draw_level(window)

        if self.box_collision_with_target():
            return True
        else:
            return False

    def draw_level(self, window):
        self._tiles.draw(window)
        self._boxes_targets.draw(window)
        self._boxes.draw(window)
        self._player.draw(window)