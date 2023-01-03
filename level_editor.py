from level import Level
from load_level import (
    LoadLevel,
    check_requirements,
    NoPlayerFoundError,
    LevelNotFoundError,
    UnmachtingBoxCountError,
    InvalidDimensionsError
    )
import pygame
import sys
from settings import textures_id_dict
from interface import Interface, Button, RGB
from typing import Tuple


class LevelEditor:
    """
    Class LevelEditor

    Parameters
    ----------

    :param width: Width of the level in pixels, max_width=1000
    :type width: int
    :param height: Height of the level in pixels, max_width=1000
    :type height: int
    :param level_path: Path to which levels will be saved
                       and from which will be loaded
    :type level_path: str
    :param level: Starting level of the editor, default level=1
    :type level: int
    :param tile_size: Size of one square texture in pixels,
                      default tile_size=50
    :type tile_size: int
    """
    def __init__(self, width: int, height: int, level_path: str,
                 level=1, tile_size=50) -> None:
        # Interface and Fonts
        self._info_width = 400
        self._resolution = (
            min(width+self._info_width, 1400), min(height+300, 1000))
        self._fps = 120
        self._interface = Interface(self._resolution, "Sokoban LEVEL Editor")
        self._tile_size = tile_size
        self._header_font = pygame.font.Font(self._interface.font()[0], 24)
        self._text_font = pygame.font.Font(self._interface.font()[0], 15)
        self._button_font = pygame.font.Font(self._interface.font()[0], 20)

        # Logic
        self._level_path = level_path
        self._level_number = level
        self._level_width = width
        self._level_height = height
        self._rows = self._level_height // self._tile_size
        self._columns = self._level_width // self._tile_size
        self.load_level = LoadLevel()

        self._level_data = self.load_level.load_empty_level(
            self._rows, self._columns)

        self._level = Level(self._rows, self._columns, self._level_data)

        # Buttons
        self._save_button = Button(
            self._level_width + 40, 150, 140, 50, "SAVE", self._button_font)
        self._load_button = Button(
            self._level_width + 220, 150, 140, 50, "LOAD", self._button_font)

    def _draw_menu(self) -> None:
        """
        Draws menu on the right side of the screen
        """
        _, height = self._resolution
        self._interface.draw_rectangle(
            self._level_width, 0, self._info_width, height, RGB(180, 122, 255))
        self._interface.draw_grid(self._rows, self._columns, self._tile_size)

        title = "Sokoban Level Editor"
        level_text = f'Level: {self._level_number}'
        level_info = 'Press UP or DOWN to change level'

        self._interface.draw_text(title, self._level_width+200, 30,
                                  anchor="CENTER", font=self._header_font)
        self._interface.draw_text(level_text, self._level_width+45,
                                  50, font=self._button_font)
        self._interface.draw_text(level_info, self._level_width+45,
                                  80, font=self._text_font)

        self._save_button.draw(self._interface.get_window())
        self._load_button.draw(self._interface.get_window())

    def _display_error_message(self, message: str) -> None:
        """
        Displays given error message on the screen
        """
        x = self._level_width//2
        y = self._level_height//2
        width = self._header_font.size(message)[0] + 50
        height = 200
        box_color = RGB(255, 255, 255)
        text_color = RGB(0, 0, 0)
        self._interface.draw_message(
            x, y, width, height, box_color,
            text_color, message, self._header_font)

    def _save_level(self) -> None:
        """
        Saves newly created level to path
        if it matches level requirements.

        Otherwise displays message to user
        """
        path = f"{self._level_path}/Level{self._level_number}_data.json"
        level_data = self._level.get_level_data()
        try:
            check_requirements(self._rows, self._columns, level_data)
            self.load_level.save_to_file(path, level_data)
        except NoPlayerFoundError:
            self._display_error_message(
                "Level cannot be saved, no player found!")
        except UnmachtingBoxCountError:
            self._display_error_message(
                "Box count doesn't match the target count!"
            )

    def _load_level(self) -> None:
        """
        Loads level from path,
        if Level is not found or has invalid dimensions
        displays mesage to user
        """
        path = f"{self._level_path}/Level{self._level_number}_data.json"
        try:
            data = self.load_level.load_from_file(path)
            check_requirements(self._rows, self._columns, data)
            self._level_data = data
            self._level = Level(self._rows, self._columns, self._level_data)
        except LevelNotFoundError:
            self._display_error_message(
                "Level with given name or with given path doesn't exits"
            )
        except InvalidDimensionsError:
            self._display_error_message(
                "Loaded level has different dimensions and cannot be loaded"
            )
        except Exception:
            pass

    def _get_mouse_coords_on_grid(self) -> Tuple[int, int]:
        """
        Gets the position of mouse's cursor on the grid
        and returns in which row and column it is
        """
        position = pygame.mouse.get_pos()
        row = position[1] // self._tile_size
        column = position[0] // self._tile_size
        return row, column

    def run(self) -> None:
        """
        Starts the LevelEditor
        """
        clock = pygame.time.Clock()
        while True:
            clock.tick(self._fps)

            self._interface.fill_color()
            self._draw_menu()
            self._interface.draw_sprites(self._level.get_sprites())

            if self._save_button.action():
                self._save_level()

            elif self._load_button.action():
                self._load_level()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    row, column = self._get_mouse_coords_on_grid()
                    if column < self._columns and row < self._rows:
                        column = str(column)
                        row = str(row)

                        if self._level.get_player() is None:
                            textures_number = len(textures_id_dict.keys()) - 1
                        else:
                            textures_number = len(textures_id_dict.keys()) - 2

                        if pygame.mouse.get_pressed()[0]:
                            self._level_data[row][column] += 1
                            if self._level_data[row][column] > textures_number:
                                self._level_data[row][column] = 0
                            self._level.set_level_data(self._level_data)
                            self._level.setup()
                        elif pygame.mouse.get_pressed()[2]:
                            self._level_data[row][column] -= 1
                            if self._level_data[row][column] < 0:
                                self._level_data[row][column] = textures_number
                            self._level.set_level_data(self._level_data)
                            self._level.setup()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self._level_number += 1
                    elif event.key == pygame.K_DOWN and self._level_number > 1:
                        self._level_number -= 1
            pygame.display.update()
