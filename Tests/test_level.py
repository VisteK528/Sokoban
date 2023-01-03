# from level import Level
from level import Level
# from load_level import LoadLevel
import pygame


def test_create_level():
    rows = 2
    columns = 2
    test_level_data = {
        "0": {"0": 3, "1": 1},
        "1": {"0": 2, "1": 5}
        }
    Level(rows, columns, test_level_data)


def test_player_vertical_move():
    keyboard_input = {i: False for i in range(512)}
    keyboard_input.update({pygame.K_w: True})

    rows = 3
    columns = 3
    test_level_data = {"0": {"0": 3, "1": 1, "2": 0},
                       "1": {"0": 2, "1": 0, "2": 0},
                       "2": {"0": 0, "1": 0, "2": 5}}
    level = Level(rows, columns, test_level_data)
    player = level.get_player()
    assert player.position.x == 2
    assert player.position.y == 2
    level.run(keyboard_input)
    assert player.position.x == 2
    assert player.position.y == 1


def test_player_horizontal_move():
    keyboard_input = {i: False for i in range(512)}
    keyboard_input.update({pygame.K_a: True})

    rows = 3
    columns = 3
    test_level_data = {"0": {"0": 3, "1": 1, "2": 0},
                       "1": {"0": 2, "1": 0, "2": 0},
                       "2": {"0": 0, "1": 0, "2": 5}}
    level = Level(rows, columns, test_level_data)
    player = level.get_player()
    assert player.position.x == 2
    assert player.position.y == 2
    level.run(keyboard_input)
    assert player.position.x == 1
    assert player.position.y == 2


def test_player_horizontal_collision_with_wall_right():
    keyboard_input = {i: False for i in range(512)}
    keyboard_input.update({pygame.K_a: True})

    rows = 3
    columns = 3
    test_level_data = {"0": {"0": 3, "1": 1, "2": 0},
                       "1": {"0": 2, "1": 0, "2": 0},
                       "2": {"0": 5, "1": 1, "2": 0}}
    level = Level(rows, columns, test_level_data)
    player = level.get_player()
    assert player.position.x == 0
    assert player.position.y == 2
    level.run(keyboard_input)
    assert player.position.x == 0
    assert player.position.y == 2


def test_player_horizontal_collision_with_wall_left():
    keyboard_input = {i: False for i in range(512)}
    keyboard_input.update({pygame.K_a: True})

    rows = 3
    columns = 3
    test_level_data = {"0": {"0": 3, "1": 1, "2": 0},
                       "1": {"0": 2, "1": 0, "2": 0},
                       "2": {"0": 0, "1": 1, "2": 5}}
    level = Level(rows, columns, test_level_data)
    player = level.get_player()
    assert player.position.x == 2
    assert player.position.y == 2
    level.run(keyboard_input)
    assert player.position.x == 2
    assert player.position.y == 2


def test_player_vertical_collision_with_wall_up():
    keyboard_input = {i: False for i in range(512)}
    keyboard_input.update({pygame.K_w: True})

    rows = 3
    columns = 3
    test_level_data = {"0": {"0": 3, "1": 1, "2": 0},
                       "1": {"0": 2, "1": 0, "2": 1},
                       "2": {"0": 0, "1": 0, "2": 5}}
    level = Level(rows, columns, test_level_data)
    player = level.get_player()
    assert player.position.x == 2
    assert player.position.y == 2
    level.run(keyboard_input)
    assert player.position.x == 2
    assert player.position.y == 2


def test_player_vertical_collision_with_wall_down():
    keyboard_input = {i: False for i in range(512)}
    keyboard_input.update({pygame.K_w: True})

    rows = 3
    columns = 3
    test_level_data = {"0": {"0": 3, "1": 1, "2": 5},
                       "1": {"0": 2, "1": 0, "2": 1},
                       "2": {"0": 0, "1": 0, "2": 0}}
    level = Level(rows, columns, test_level_data)
    player = level.get_player()
    assert player.position.x == 2
    assert player.position.y == 0
    level.run(keyboard_input)
    assert player.position.x == 2
    assert player.position.y == 0


def test_player_moves():
    keyboard_input = {i: False for i in range(512)}
    keyboard_input.update({pygame.K_w: True})

    rows = 2
    columns = 2
    test_level_data = {
        "0": {"0": 3, "1": 0},
        "1": {"0": 2, "1": 5}
        }
    level = Level(rows, columns, test_level_data)
    player = level.get_player()
    assert player.moves == 0
    level.run(keyboard_input)
    assert player.moves == 1


def test_player_pushes():
    keyboard_input = {i: False for i in range(512)}
    keyboard_input.update({pygame.K_w: True})

    rows = 3
    columns = 3
    test_level_data = {"0": {"0": 0, "1": 1, "2": 3},
                       "1": {"0": 0, "1": 0, "2": 2},
                       "2": {"0": 0, "1": 0, "2": 5}}
    level = Level(rows, columns, test_level_data)
    player = level.get_player()
    assert player.moves == 0
    assert player.pushes == 0
    level.run(keyboard_input)
    assert player.moves == 1
    assert player.pushes == 1


def test_number_of_completed_targets():
    keyboard_input = {i: False for i in range(512)}
    keyboard_input.update({pygame.K_w: True})

    rows = 3
    columns = 3
    test_level_data = {"0": {"0": 0, "1": 1, "2": 3},
                       "1": {"0": 0, "1": 0, "2": 2},
                       "2": {"0": 0, "1": 0, "2": 5}}
    level = Level(rows, columns, test_level_data)
    player = level.get_player()
    assert player.moves == 0
    assert player.pushes == 0
    level.run(keyboard_input)
    assert player.moves == 1
    assert player.pushes == 1
    assert level.get_completed_targets() == 1


def test_box_move_vertically():
    keyboard_input = {i: False for i in range(512)}
    keyboard_input.update({pygame.K_w: True})

    rows = 3
    columns = 3
    test_level_data = {"0": {"0": 0, "1": 1, "2": 3},
                       "1": {"0": 0, "1": 0, "2": 2},
                       "2": {"0": 0, "1": 0, "2": 5}}
    level = Level(rows, columns, test_level_data)
    player = level.get_player()
    boxes = level.get_sprites()[2]
    box = boxes.sprites()[0]
    assert player.position.x == 2
    assert player.position.y == 2
    assert box.position.x == 2
    assert box.position.y == 1
    level.run(keyboard_input)
    assert player.position.x == 2
    assert player.position.y == 1
    assert box.position.x == 2
    assert box.position.y == 0


def test_box_move_horizontally():
    keyboard_input = {i: False for i in range(512)}
    keyboard_input.update({pygame.K_a: True})

    rows = 3
    columns = 3
    test_level_data = {"0": {"0": 0, "1": 1, "2": 0},
                       "1": {"0": 0, "1": 0, "2": 0},
                       "2": {"0": 3, "1": 2, "2": 5}}
    level = Level(rows, columns, test_level_data)
    player = level.get_player()
    boxes = level.get_sprites()[2]
    box = boxes.sprites()[0]
    assert player.position.x == 2
    assert player.position.y == 2
    assert box.position.x == 1
    assert box.position.y == 2
    level.run(keyboard_input)
    assert player.position.x == 1
    assert player.position.y == 2
    assert box.position.x == 0
    assert box.position.y == 2


def test_horizontal_collision_with_two_boxes():
    keyboard_input = {i: False for i in range(512)}
    keyboard_input.update({pygame.K_a: True})

    rows = 3
    columns = 3
    test_level_data = {"0": {"0": 0, "1": 1, "2": 0},
                       "1": {"0": 3, "1": 3, "2": 0},
                       "2": {"0": 2, "1": 2, "2": 5}}
    level = Level(rows, columns, test_level_data)
    player = level.get_player()
    boxes = level.get_sprites()[2]
    box, box2 = boxes.sprites()
    assert player.position.x == 2
    assert player.position.y == 2
    assert box.position.y == box2.position.y
    level.run(keyboard_input)
    assert player.position.x == 2
    assert player.position.y == 2
    assert box.position.y == box2.position.y


def test_vertical_collision_with_two_boxes():
    keyboard_input = {i: False for i in range(512)}
    keyboard_input.update({pygame.K_w: True})

    rows = 3
    columns = 3
    test_level_data = {"0": {"0": 0, "1": 1, "2": 2},
                       "1": {"0": 3, "1": 3, "2": 2},
                       "2": {"0": 0, "1": 0, "2": 5}}
    level = Level(rows, columns, test_level_data)
    player = level.get_player()
    boxes = level.get_sprites()[2]
    box, box2 = boxes.sprites()
    assert player.position.x == 2
    assert player.position.y == 2
    assert box.position.x == box2.position.x
    level.run(keyboard_input)
    assert player.position.x == 2
    assert player.position.y == 2
    assert box.position.x == box2.position.x


def test_vertical_box_collision_with_wall():
    keyboard_input = {i: False for i in range(512)}
    keyboard_input.update({pygame.K_w: True})

    rows = 3
    columns = 3
    test_level_data = {"0": {"0": 0, "1": 1, "2": 1},
                       "1": {"0": 3, "1": 0, "2": 2},
                       "2": {"0": 0, "1": 0, "2": 5}}
    level = Level(rows, columns, test_level_data)
    player = level.get_player()
    boxes = level.get_sprites()[2]
    box = boxes.sprites()[0]
    assert player.position.x == 2
    assert player.position.y == 2
    assert box.position.x == 2
    assert box.position.y == 1
    level.run(keyboard_input)
    assert player.position.x == 2
    assert player.position.y == 2
    assert box.position.x == 2
    assert box.position.y == 1


def test_horizontal_box_collision_with_wall():
    keyboard_input = {i: False for i in range(512)}
    keyboard_input.update({pygame.K_a: True})

    rows = 3
    columns = 3
    test_level_data = {"0": {"0": 0, "1": 1, "2": 0},
                       "1": {"0": 3, "1": 0, "2": 0},
                       "2": {"0": 1, "1": 2, "2": 5}}
    level = Level(rows, columns, test_level_data)
    player = level.get_player()
    boxes = level.get_sprites()[2]
    box = boxes.sprites()[0]
    assert player.position.x == 2
    assert player.position.y == 2
    assert box.position.x == 1
    assert box.position.y == 2
    level.run(keyboard_input)
    assert player.position.x == 2
    assert player.position.y == 2
    assert box.position.x == 1
    assert box.position.y == 2


def test_move_beyond_the_map_right():
    keyboard_input = {i: False for i in range(512)}
    keyboard_input.update({pygame.K_d: True})

    rows = 3
    columns = 3
    test_level_data = {"0": {"0": 2, "1": 1, "2": 0},
                       "1": {"0": 3, "1": 0, "2": 0},
                       "2": {"0": 0, "1": 0, "2": 5}}
    level = Level(rows, columns, test_level_data)
    player = level.get_player()
    assert player.position.x == 2
    assert player.position.y == 2
    level.run(keyboard_input)
    assert player.position.x == 2
    assert player.position.y == 2


def test_move_beyond_the_map_left():
    keyboard_input = {i: False for i in range(512)}
    keyboard_input.update({pygame.K_a: True})

    rows = 3
    columns = 3
    test_level_data = {"0": {"0": 2, "1": 1, "2": 0},
                       "1": {"0": 3, "1": 0, "2": 0},
                       "2": {"0": 5, "1": 0, "2": 0}}
    level = Level(rows, columns, test_level_data)
    player = level.get_player()
    assert player.position.x == 0
    assert player.position.y == 2
    level.run(keyboard_input)
    assert player.position.x == 0
    assert player.position.y == 2


def test_move_beyond_the_map_up():
    keyboard_input = {i: False for i in range(512)}
    keyboard_input.update({pygame.K_w: True})

    rows = 3
    columns = 3
    test_level_data = {"0": {"0": 2, "1": 1, "2": 5},
                       "1": {"0": 3, "1": 0, "2": 0},
                       "2": {"0": 0, "1": 0, "2": 0}}
    level = Level(rows, columns, test_level_data)
    player = level.get_player()
    assert player.position.x == 2
    assert player.position.y == 0
    level.run(keyboard_input)
    assert player.position.x == 2
    assert player.position.y == 0


def test_move_beyond_the_map_down():
    keyboard_input = {i: False for i in range(512)}
    keyboard_input.update({pygame.K_s: True})

    rows = 3
    columns = 3
    test_level_data = {"0": {"0": 2, "1": 1, "2": 0},
                       "1": {"0": 3, "1": 0, "2": 0},
                       "2": {"0": 5, "1": 0, "2": 5}}
    level = Level(rows, columns, test_level_data)
    player = level.get_player()
    assert player.position.x == 2
    assert player.position.y == 2
    level.run(keyboard_input)
    assert player.position.x == 2
    assert player.position.y == 2
