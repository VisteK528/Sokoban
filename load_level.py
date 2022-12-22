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
    def __init__(self, width, height, tile_size):
        if width < 0 or height < 0:
            raise InvalidDimensionsError(
                "Level width or height cannot be negative")
        if tile_size <= 0:
            raise InvalidTileSizeError(
                "Tile size cannot be negative"
            )
        if width % tile_size != 0 or height % tile_size != 0:
            raise InvalidDimensionsError(
                "Level width height must be multiple of tile size"
            )
        self._width = width
        self._height = height
        self._tile_size = tile_size
        self._columns = self._width // self._tile_size
        self._rows = self._height // self._tile_size

    def _check_requirements(self, data):
        player_required_count = 1
        player_count = 0
        box_count = 0
        box_target_count = 0

        if len(data.keys()) != self._rows:
            raise InvalidDimensionsError(
                "Level has to have the same dimensions as specified")

        for row in data.values():
            if len(row.keys()) != self._columns:
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
        if player_count > player_required_count:
            raise TooManyPlayersFoundError(player_count)
        if player_count == 0:
            raise NoPlayerFoundError(
                "Level cannot be initialized without player")
        if box_count != box_target_count:
            raise UnmachtingBoxCountError(
                "Number of boxes on the level must "
                "be equal to number of box targets")

    def load_empty_level(self):
        level_data = {str(i): {
                    str(j): 0 for j in range(self._columns)
                    } for i in range(self._rows)}
        return level_data

    def load_level(self, path):
        try:
            with open(path, "r") as file_handle:
                data = self._read_from_json(file_handle)
        except FileNotFoundError:
            raise LevelNotFoundError(path)
        self._check_requirements(data)
        return data

    def save_level(self, path, data):
        self._check_requirements(data)
        with open(path, "w") as file_handle:
            self._write_to_json(file_handle, data)

    def _read_from_json(self, file_handle):
        return json.load(file_handle)

    def _write_to_json(self, file_handle, data):
        json.dump(data, file_handle)
