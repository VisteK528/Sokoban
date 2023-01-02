import json
from settings import textures_id_dict


class InvalidDimensionsError(Exception):
    def __init__(self, message="") -> None:
        super().__init__(message)


class InvalidTileSizeError(Exception):
    def __init__(self, tile_size, message="") -> None:
        super().__init__(message)
        self._tile_size = tile_size


class UnmachtingBoxCountError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class NoPlayerFoundError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class TooManyPlayersFoundError(Exception):
    def __init__(self, players_number) -> None:
        super().__init__(
            "There is too many player instances on the same level")
        self._player_number = players_number


class LevelNotFoundError(Exception):
    def __init__(self, path) -> None:
        super().__init__("Level with that name or path does not exist")
        self._path = path


class LoadLevel:
    def load_empty_level(self, rows: int, columns: int):
        """
        Loads empty level with specified dimensions
        """
        level_data = {str(i): {
                    str(j): 0 for j in range(columns)
                    } for i in range(rows)}
        return level_data

    def load_from_file(self, path: str) -> dict:
        """
        Loads level data from given path
        Throws LevelNotFoundEror when level cannot be found under given path
        """
        try:
            with open(path, "r") as file_handle:
                data = self._read_from_json(file_handle)
            return data
        except FileNotFoundError:
            raise LevelNotFoundError(path)

    def save_to_file(self, path: str, data: dict):
        """
        Saves level data to given path
        """
        with open(path, "w") as file_handle:
            self._write_to_json(file_handle, data)

    def _read_from_json(self, file_handle):
        return json.load(file_handle)

    def _write_to_json(self, file_handle, data):
        json.dump(data, file_handle)


def check_requirements(rows: int, columns: int, data: dict):
    """
    Checks if level data matches game requirements

    Raises
    ------
    InvalidDimensinsError: Level data dimensions differ from expected
                            dimensions
    TooManyPlayersFoundError: If Level has more than 1 player
    NoPlayerFoundError: If Level has no player declared
    UnmachingBoxCountError: Number of boxes found in the level vary
                            from expected level of targets
    """
    player_count_required = 1
    player_count = 0
    box_count = 0
    box_target_count = 0

    if len(data.keys()) != rows:
        raise InvalidDimensionsError(
            "Level has to have the same dimensions as specified")

    for row in data.values():
        if len(row.keys()) != columns:
            raise InvalidDimensionsError(
                "Level has to have the same dimensions as specified")
        for value in row.values():
            if value == textures_id_dict["player"]:
                player_count += 1
            elif value == textures_id_dict["box"]:
                box_count += 1
            elif value == textures_id_dict["box_target"]:
                box_target_count += 1
            elif value == textures_id_dict["box_target_with_box"]:
                box_count += 1
                box_target_count += 1
    if player_count > player_count_required:
        raise TooManyPlayersFoundError(player_count)
    if player_count == 0:
        raise NoPlayerFoundError(
            "Level cannot be initialized without player")
    if box_count != box_target_count:
        raise UnmachtingBoxCountError(
            "Number of boxes on the level must "
            "be equal to number of box targets")
