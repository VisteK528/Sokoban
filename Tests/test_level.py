# from level import Level
from level import Level
# from load_level import LoadLevel
import pygame


def test_create_level():
    rows = 2
    columns = 2
    fake_level_data = {
        "0": {"0": 3, "1": 1},
        "1": {"0": 2, "1": 5}
        }
    Level(rows, columns, fake_level_data)


def test_create_level_with_negative_width():
    pass


def test_create_level_with_negative_height():
    pass


def test_create_level_with_negative_tile_size():
    pass


def test_get_level_dimensions():
    pass


def test_player_vertical_move(monkeypatch):
    def fake_input():
        keys = {i: False for i in range(512)}
        keys.update({pygame.K_w: True})
        return keys

    monkeypatch.setattr("pygame.key.get_pressed", fake_input)
    rows = 3
    columns = 3
    fake_level_data = {"0": {"0": 3, "1": 1, "2": 0},
                       "1": {"0": 2, "1": 0, "2": 0},
                       "2": {"0": 0, "1": 0, "2": 5}}
    level = Level(rows, columns, fake_level_data)
    level.setup()
    player = level.get_player()
    assert player.position.x == 2
    assert player.position.y == 2
    level.run()
    assert player.position.x == 2
    assert player.position.y == 1


def test_player_horizontal_move(monkeypatch):
    def fake_input():
        keys = {i: False for i in range(512)}
        keys.update({pygame.K_a: True})
        return keys

    monkeypatch.setattr("pygame.key.get_pressed", fake_input)
    rows = 3
    columns = 3
    fake_level_data = {"0": {"0": 3, "1": 1, "2": 0},
                       "1": {"0": 2, "1": 0, "2": 0},
                       "2": {"0": 0, "1": 0, "2": 5}}
    level = Level(rows, columns, fake_level_data)
    level.setup()
    player = level.get_player()
    assert player.position.x == 2
    assert player.position.y == 2
    level.run()
    assert player.position.x == 1
    assert player.position.y == 2


def test_player_horizontal_collision_with_wall(monkeypatch):
    def fake_input():
        keys = {i: False for i in range(512)}
        keys.update({pygame.K_a: True})
        return keys

    monkeypatch.setattr("pygame.key.get_pressed", fake_input)
    rows = 3
    columns = 3
    fake_level_data = {"0": {"0": 3, "1": 1, "2": 0},
                       "1": {"0": 2, "1": 0, "2": 0},
                       "2": {"0": 0, "1": 1, "2": 5}}
    level = Level(rows, columns, fake_level_data)
    level.setup()
    player = level.get_player()
    assert player.position.x == 2
    assert player.position.y == 2
    level.run()
    assert player.position.x == 2
    assert player.position.y == 2


def test_player_vertical_collision_with_wall(monkeypatch):
    def fake_input():
        keys = {i: False for i in range(512)}
        keys.update({pygame.K_w: True})
        return keys

    monkeypatch.setattr("pygame.key.get_pressed", fake_input)
    rows = 3
    columns = 3
    fake_level_data = {"0": {"0": 3, "1": 1, "2": 0},
                       "1": {"0": 2, "1": 0, "2": 1},
                       "2": {"0": 0, "1": 0, "2": 5}}
    level = Level(rows, columns, fake_level_data)
    level.setup()
    player = level.get_player()
    assert player.position.x == 2
    assert player.position.y == 2
    level.run()
    assert player.position.x == 2
    assert player.position.y == 2


def test_player_moves():
    pass


def test_player_pushes():
    pass


def test_number_of_completed_targets():
    pass


def test_box_move_vertically():
    pass


def test_box_move_horizontally():
    pass


def test_horizontal_box_collision_with_box():
    pass


def test_vertical_box_collision_with_box():
    pass


def test_vertical_box_collision_with_wall():
    pass


def test_horizontal_box_collision_with_wall():
    pass
