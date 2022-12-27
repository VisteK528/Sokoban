from level import Level
from load_level import (
    LoadLevel,
    check_requirements,
    NoPlayerFoundError,
    LevelNotFoundError,
    UnmachtingBoxCountError
    )
import pygame
import sys
from settings import textures_id_dict
from interface import Interface, Button, RGB


class LevelEditor:
    def __init__(self, width, height, level=1, tile_size=50):
        # Interface and Fonts
        self._resolution = (width, height)
        self._info_width = 400
        self._fps = 120
        self._interface = Interface(self._resolution, "Sokoban LEVEL Editor")
        self._tile_size = tile_size
        self._header_font = pygame.font.Font(self._interface.font()[0], 24)
        self._text_font = pygame.font.Font(self._interface.font()[0], 15)
        self._button_font = pygame.font.Font(self._interface.font()[0], 20)

        # Logic
        self._level_number = level
        self._level_width = self._resolution[0] - self._info_width
        self._level_height = self._resolution[1]
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

    def _draw_menu(self):
        self._interface.draw_rectangle(1000, 0, 400, 1000, RGB(180, 122, 255))
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

    def _save_level(self):
        path = f"Levels/Level{self._level_number}_data.json"
        level_data = self._level.get_level_data()
        check_requirements(self._rows, self._columns, level_data)
        self.load_level.save_to_file(path, level_data)

    def _load_level(self):
        path = f"Levels/Level{self._level_number}_data.json"
        try:
            self._level_data = self.load_level.load_from_file(path)
            check_requirements(self._rows, self._columns, self._level_data)
        except (NoPlayerFoundError, LevelNotFoundError):
            self._level_data = self.load_level.load_empty_level(
                self._rows, self._columns)
        except UnmachtingBoxCountError:
            pass

        self._level = Level(self._rows, self._columns, self._level_data)
        self._level.setup()

    def _get_mouse_coords_on_grid(self):
        position = pygame.mouse.get_pos()
        row = position[1] // self._tile_size
        column = position[0] // self._tile_size
        return row, column

    def run(self):
        clock = pygame.time.Clock()
        self._level.setup()
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
