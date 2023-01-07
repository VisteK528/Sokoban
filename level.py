import pygame
from classes import Box, Player, BoxTarget, Tile, Entity
from settings import textures_id_dict
from typing import Tuple


class Level:
    """
    Class Level. Contains attributes:
    :param rows: Number of rows in the level
    :type rows: int
    :param columns: Number of columns in the level
    :type columns: int
    :param level_data: Level data
    :type level_data: dict
    """
    def __init__(self, rows: int, columns: int, level_data: dict):
        self._rows = rows
        self._columns = columns
        self._level_data = level_data

        self._completed_targets = 0
        self.setup()

    def get_completed_targets(self) -> None:
        return self._completed_targets

    def set_level_data(self, level_data) -> None:
        self._level_data = level_data

    def get_level_data(self) -> dict:
        return self._level_data

    def get_player_moves(self) -> int:
        return self._player.sprite.moves

    def get_player_pushes(self) -> int:
        return self._player.sprite.pushes

    def get_player(self) -> Player:
        return self._player.sprite

    def get_sprites(self) -> Tuple[pygame.sprite.Group]:
        return self._tiles, self._boxes_targets, self._boxes, self._player

    def setup(self) -> None:
        """
        Reads the given level data and then creates specific
        objects based in the given coordinates
        """
        self._tiles = pygame.sprite.Group()
        self._boxes = pygame.sprite.Group()
        self._boxes_targets = pygame.sprite.Group()
        self._player = pygame.sprite.GroupSingle()

        for row in range(self._rows):
            for column in range(self._columns):
                texture_id = self._level_data[str(row)][str(column)]
                y = row
                x = column
                if texture_id == textures_id_dict["player"]:
                    # Player
                    self._player.add(Player(x, y))
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

    def _check_if_on_the_map(self, sprite, direction) -> bool:
        """
        Checks if sprite will be on the map after
        making move with current direction
        """
        position = sprite.position.copy()
        position.x += direction.x
        position.y += direction.y
        if position.x < 0 or position.x > self._columns - 1:
            return False
        elif position.y < 0 or position.y > self._rows - 1:
            return False
        return True

    def _two_entities_collision(
            self, entity1: Entity, entity2: Entity) -> bool:
        """
        Checks the collision between two game entities
        """
        x1 = entity1.position.x
        x2 = entity2.position.x
        y1 = entity1.position.y
        y2 = entity2.position.y
        if (x1 == x2) and (y1 == y2):
            return True
        else:
            return False

    def _horizontal_collision(self) -> None:
        """
        Checks horizontal collisions between entities
        """
        self._collision(0)

    def _vertical_collision(self) -> None:
        """
        Checks vertical collisions between entities
        """
        self._collision(1)

    def _collision(self, key: int) -> None:
        """
        Checks the collisions between entities in given direction

        Parameters
        ----------

        :param key: Direction key
                    if direction=x then key=0
                    if direction=y then key=1
        :type key: int
        """
        player = self._player.sprite
        box_move = False
        move_value = player.direction[key]
        if move_value != 0:
            player_move = True
        else:
            player_move = False
        player.position[key] += move_value

        boxes = self._boxes.sprites()
        for box in boxes:
            if self._two_entities_collision(box, player):
                if self._check_if_on_the_map(box, player.direction):
                    box_move = True
                    player_move = True
                    box.position[key] += move_value
                    if player.direction[key] < 0:
                        box.position[key] = player.position[key] - 1
                    elif player.direction[key] > 0:
                        box.position[key] = player.position[key] + 1
                else:
                    player.position[key] -= move_value
                    player_move = False
                    box_move = False

        for i, box in enumerate(boxes):
            for box2 in boxes[i+1:]:
                if self._two_entities_collision(box, box2):
                    box_move = False
                    player_move = False
                    player.position[key] -= move_value
                    if player.direction[key] < 0:
                        box.position[key] = box2.position[key] + 1
                    elif player.direction[key] > 0:
                        box.position[key] = box2.position[key] - 1

        for tile in self._tiles.sprites():
            if self._two_entities_collision(player, tile):
                player_move = False
                if player.direction[key] < 0:
                    player.position[key] = tile.position[key] + 1
                elif player.direction[key] > 0:
                    player.position[key] = tile.position[key] - 1

            for box in boxes:
                if self._two_entities_collision(box, tile):
                    player_move = False
                    box_move = False
                    player.position[key] -= move_value
                    if player.direction[key] < 0:
                        box.position[key] = tile.position[key] + 1
                    elif player.direction[key] > 0:
                        box.position[key] = tile.position[key] - 1

        if player_move:
            player.moves += 1
        if box_move:
            player.pushes += 1

    def _box_collision_with_target(self) -> None:
        """
        Checks collision between boxes and targets
        Number of collisons is assigned to self._completed_targets variable
        """
        boxes = self._boxes
        targets = self._boxes_targets
        completed_boxes = 0
        for box in boxes:
            box.set_default_image()
            for target in targets:
                if self._two_entities_collision(box, target):
                    box.set_change_image()
                    completed_boxes += 1

        self._completed_targets = completed_boxes

    def _update_player(self, keyboard_input: dict) -> None:
        """
        Updates player's move direction value
        based on the given keyboard_input
        """
        player = self._player.sprite

        if keyboard_input[pygame.K_w]:
            player.direction.x = 0
            player.direction.y = -1
        elif keyboard_input[pygame.K_s]:
            player.direction.x = 0
            player.direction.y = 1
        elif keyboard_input[pygame.K_a]:
            player.direction.x = -1
            player.direction.y = 0
        elif keyboard_input[pygame.K_d]:
            player.direction.x = 1
            player.direction.y = 0
        else:
            player.direction.x = 0
            player.direction.y = 0

    def run(self, keyboard_input) -> bool:
        """
        Runs the level in one round
        """
        self._update_player(keyboard_input)
        player = self._player.sprite
        if self._check_if_on_the_map(player, player.direction):
            self._horizontal_collision()
            self._vertical_collision()

            self._box_collision_with_target()
            if self._completed_targets == len(self._boxes_targets):
                return True
        return False
