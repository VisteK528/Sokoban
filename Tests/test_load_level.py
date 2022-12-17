from load_level import (
    LoadLevel,
    InvalidTileSizeError,
    InvalidDimensionsError,
    )
from pytest import raises


def test_save_data_to_json():
    data = {0: {0: 1, 1: 0, 2: 3},
            1: {0: 1, 1: 0, 2: 4},
            2: {0: 1, 1: 0, 2: 2}}
    with open("Tests/test_save_level.json", "w") as fp:
        LoadLevel.write_to_json(fp, data)


def test_loadlevel_negative_dimensions():
    with raises(InvalidDimensionsError):
        LoadLevel(-50, 1000, 50)


def test_loadlevel_with_negative_tile_size():
    with raises(InvalidTileSizeError):
        LoadLevel(1000, 1000, 0)


def test_loadlevel_with_invalid_dimensions():
    with raises(InvalidDimensionsError):
        LoadLevel(1001, 1001, 50)
