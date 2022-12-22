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

    def get_player_moves(self):
        return self._player.sprite.moves

    def get_player_pushes(self):
        return self._player.sprite.pushes

    def get_dimensions(self):
        return self._rows, self._columns

    def setup(self):
        self._tiles = pygame.sprite.Group()
        self._boxes = pygame.sprite.Group()
        self._boxes_targets = pygame.sprite.Group()
        self._player = pygame.sprite.GroupSingle()
        self._player_placed = False
        for row in range(self._rows):
            for column in range(self._columns):
                texture_id = self._level_data[str(row)][str(column)]
                y = row
                x = column
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
                elif texture_id == textures_id_dict["box_target_with_box"]:
                    self._boxes_targets.add(BoxTarget(x, y))
                    box = Box(x, y)
                    box.set_change_image()
                    self._boxes.add(box)
                elif texture_id == textures_id_dict["tile"]:
                    # Tile
                    self._tiles.add(Tile(x, y))

    def horizontal_collision(self):
        player = self._player.sprite
        box_move = False
        move_value = player.direction.x
        if move_value != 0:
            player_move = True
        else:
            player_move = False
        player.position.x += move_value

        boxes = self._boxes.sprites()
        for box in boxes:
            if box.position == player.position:
                box_move = True
                player_move = True
                box.position.x += move_value
                if player.direction.x < 0:
                    box.position.x = player.position.x - 1
                elif player.direction.x > 0:
                    box.position.x = player.position.x + 1

        for i, box in enumerate(boxes):
            for box2 in boxes[i+1:]:
                if box.position == box2.position:
                    box_move = False
                    player_move = False
                    box.position.x -= move_value
                    player.position.x -= move_value
                    if (box.position.x - 1) == box2.rect.x:
                        box.position.x = box2.position.x - 1
                    else:
                        box.position.x = box2.position.x + 1

        for tile in self._tiles.sprites():
            if player.position == tile.position:
                player_move = False
                if player.direction.x < 0:
                    player.position.x = tile.position.x + 1
                elif player.direction.x > 0:
                    player.position.x = tile.position.x - 1

            for box in boxes:
                if box.position == tile.position:
                    player_move = False
                    box_move = False
                    player.position.x -= move_value
                    if player.direction.x < 0:
                        box.position.x = tile.position.x + 1
                    elif player.direction.x > 0:
                        box.position.x = tile.position.x - 1

        if player_move:
            player.moves += 1
        if box_move:
            player.pushes += 1

    def vertical_collision(self):
        player = self._player.sprite
        box_move = False
        move_value = player.direction.y
        if move_value != 0:
            player_move = True
        else:
            player_move = False
        player.position.y += move_value

        boxes = self._boxes.sprites()
        for box in boxes:
            if box.position == player.position:
                box_move = True
                player_move = True
                box.position.y += move_value
                if player.direction.y < 0:
                    box.position.y = player.position.y - 1
                elif player.direction.y > 0:
                    box.position.y = player.position.y + 1

        for i, box in enumerate(boxes):
            for box2 in boxes[i+1:]:
                if box.position == box2.position:
                    box_move = False
                    player_move = False
                    box.position.y -= move_value
                    player.position.y -= move_value
                    if (box.position.y - 1) == box2.rect.y:
                        box.position.y = box2.position.y - 1
                    else:
                        box.position.y = box2.position.y + 1

        for tile in self._tiles.sprites():
            if player.position == tile.position:
                player_move = False
                if player.direction.y < 0:
                    player.position.y = tile.position.y + 1
                elif player.direction.y > 0:
                    player.position.y = tile.position.y - 1

            for box in boxes:
                if box.position == tile.position:
                    player_move = False
                    box_move = False
                    player.position.y -= move_value
                    if player.direction.y < 0:
                        box.position.y = tile.position.y + 1
                    elif player.direction.y > 0:
                        box.position.y = tile.position.y - 1

        if player_move:
            player.moves += 1
        if box_move:
            player.pushes += 1

    def box_collision_with_target(self):
        boxes = self._boxes
        targets = self._boxes_targets
        completed_boxes = 0
        for box in boxes:
            box.set_default_image()
        for box in boxes:
            for target in targets:
                if box.position == target.position:
                    box.set_change_image()
                    completed_boxes += 1
        if completed_boxes == len(targets):
            return True
        else:
            return False

    def run(self):
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

        if self.box_collision_with_target():
            return True
        else:
            return False

    def get_sprites(self):
        return self._tiles, self._boxes_targets, self._boxes, self._player
