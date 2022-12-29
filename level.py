import pygame
from classes import Box, Player, BoxTarget, Tile, Entity
from settings import textures_id_dict


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

        self._tiles = pygame.sprite.Group()
        self._boxes = pygame.sprite.Group()
        self._boxes_targets = pygame.sprite.Group()
        self._player = pygame.sprite.GroupSingle()

    def get_completed_targets(self):
        return self._completed_targets

    def set_level_data(self, level_data):
        self._level_data = level_data

    def get_level_data(self):
        return self._level_data

    def get_player_moves(self):
        return self._player.sprite.moves

    def get_player_pushes(self):
        return self._player.sprite.pushes

    def get_player(self):
        return self._player.sprite

    def get_sprites(self):
        return self._tiles, self._boxes_targets, self._boxes, self._player

    def setup(self):
        """
        Reads the given level data and then creates specific
        objects based in the given coordinates
        """
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

    @staticmethod
    def two_entities_collision(entity1: Entity, entity2: Entity) -> bool:
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

    def _horizontal_collision(self):
        """
        Checks the horizontal collision between entities
        """
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
            if self.two_entities_collision(box, player):
                box_move = True
                player_move = True
                box.position.x += move_value
                if player.direction.x < 0:
                    box.position.x = player.position.x - 1
                elif player.direction.x > 0:
                    box.position.x = player.position.x + 1

        for i, box in enumerate(boxes):
            for box2 in boxes[i+1:]:
                if self.two_entities_collision(box, box2):
                    box_move = False
                    player_move = False
                    player.position.x -= move_value
                    if player.direction.x < 0:
                        box.position.x = box2.position.x + 1
                    elif player.direction.x > 0:
                        box.position.x = box2.position.x - 1

        for tile in self._tiles.sprites():
            if self.two_entities_collision(player, tile):
                player_move = False
                if player.direction.x < 0:
                    player.position.x = tile.position.x + 1
                elif player.direction.x > 0:
                    player.position.x = tile.position.x - 1

            for box in boxes:
                if self.two_entities_collision(box, tile):
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

    def _vertical_collision(self):
        """
        Checks the vertical collision between entities
        """
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
            if self.two_entities_collision(box, player):
                box_move = True
                player_move = True
                box.position.y += move_value
                if player.direction.y < 0:
                    box.position.y = player.position.y - 1
                elif player.direction.y > 0:
                    box.position.y = player.position.y + 1

        for i, box in enumerate(boxes):
            for box2 in boxes[i+1:]:
                if self.two_entities_collision(box, box2):
                    box_move = False
                    player_move = False
                    player.position.y -= move_value
                    if player.direction.y < 0:
                        box.position.y = box2.position.y + 1
                    elif player.direction.y > 0:
                        box.position.y = box2.position.y - 1

        for tile in self._tiles.sprites():
            if self.two_entities_collision(player, tile):
                player_move = False
                if player.direction.y < 0:
                    player.position.y = tile.position.y + 1
                elif player.direction.y > 0:
                    player.position.y = tile.position.y - 1

            for box in boxes:
                if self.two_entities_collision(box, tile):
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

    def _box_collision_with_target(self):
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
                if self.two_entities_collision(box, target):
                    box.set_change_image()
                    completed_boxes += 1

        self._completed_targets = completed_boxes

    def _update_player(self, keyboard_input: dict):
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
        # player
        self._player.update()

        self._horizontal_collision()
        self._vertical_collision()
        # tiles
        self._tiles.update()

        # boxes targets
        self._boxes_targets.update()

        # boxes
        self._boxes.update()

        self._box_collision_with_target()
        if self._completed_targets == len(self._boxes_targets):
            return True
        else:
            return False
