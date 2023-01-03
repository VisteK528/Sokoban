from load_level import (
    LoadLevel,
    check_requirements,
    TooManyPlayersFoundError,
    InvalidDimensionsError,
    NoPlayerFoundError,
    UnmachtingBoxCountError
    )
from pytest import raises


def test_save_data_to_json():
    data = {"0": {"0": 1, "1": 0, "2": 3},
            "1": {"0": 1, "1": 0, "2": 5},
            "2": {"0": 1, "1": 0, "2": 2}}
    path = "Tests/test_save_level.json"
    load_level = LoadLevel()
    load_level.save_to_file(path, data)
    loaded_data = load_level.load_from_file(path)
    assert data == loaded_data


def test_check_requirements_with_no_player():
    data = {"0": {"0": 1, "1": 0, "2": 3},
            "1": {"0": 1, "1": 0, "2": 0},
            "2": {"0": 1, "1": 0, "2": 2}}
    rows = 3
    columns = 3
    with raises(NoPlayerFoundError):
        check_requirements(rows, columns, data)


def test_check_requirements_with_unmatching_number_of_boxes():
    data = {"0": {"0": 1, "1": 0, "2": 3},
            "1": {"0": 1, "1": 3, "2": 5},
            "2": {"0": 1, "1": 0, "2": 2}}
    rows = 3
    columns = 3
    with raises(UnmachtingBoxCountError):
        check_requirements(rows, columns, data)


def test_check_requirements_with_too_many_players():
    data = {"0": {"0": 1, "1": 0, "2": 3},
            "1": {"0": 5, "1": 0, "2": 5},
            "2": {"0": 1, "1": 0, "2": 2}}
    rows = 3
    columns = 3
    with raises(TooManyPlayersFoundError):
        check_requirements(rows, columns, data)


def test_check_requirements_with_unmatching_number_of_rows():
    data = {"0": {"0": 1, "1": 0, "2": 3},
            "1": {"0": 5, "1": 0, "2": 5},
            "2": {"0": 1, "1": 0, "2": 2},
            "3": {"0": 1, "1": 0, "2": 2}}
    rows = 3
    columns = 3
    with raises(InvalidDimensionsError):
        check_requirements(rows, columns, data)


def test_check_requirements_with_unmatching_number_of_columns():
    data = {"0": {"0": 1, "1": 0, "2": 3, "3": 0},
            "1": {"0": 5, "1": 0, "2": 5, "3": 0},
            "2": {"0": 1, "1": 0, "2": 2, "3": 0}}
    rows = 3
    columns = 3
    with raises(InvalidDimensionsError):
        check_requirements(rows, columns, data)
