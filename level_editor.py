from level import Level
from load_level import NoPlayerFoundError
import pygame
import sys
from settings import textures_id_dict
from interface import Interface, Button, RGB


class LevelEditor(Level):
    def __init__(self, width, height, level=1, tile_size=50):
        super().__init__(width, height, level, tile_size)
        self._tools_margin = 400
        self._resolution = (self._width+self._tools_margin, self._height)
        self._fps = 120

        self._interface = Interface(self._resolution, "Sokoban LEVEL Editor")
        self._header_font = pygame.font.Font(self._interface.font()[0], 24)
        self._text_font = pygame.font.Font(self._interface.font()[0], 15)
        self._button_font = pygame.font.Font(self._interface.font()[0], 20)

        self._save_button = Button(
            self._width + 40, 150, 140, 50, "SAVE", self._button_font)
        self._load_button = Button(
            self._width + 220, 150, 140, 50, "LOAD", self._button_font)

    def _draw_menu(self):
        self._interface.fill_color()
        self._interface.draw_rectangle(1000, 0, 400, 1000, RGB(180, 122, 255))
        self._interface.draw_sprites(self.get_sprites())
        self._interface.draw_grid(self._rows, self._columns, self._tile_size)

        title = "Sokoban Level Editor"
        level_text = f'Level: {self._level}'
        level_info = 'Press UP or DOWN to change level'

        self._interface.draw_text(
            title, 1200, 30, anchor="CENTER", font=self._header_font)
        self._interface.draw_text(
            level_text, self._width+45, 50, font=self._button_font)
        self._interface.draw_text(
            level_info, self._width+45, 80, font=self._text_font)

        self._save_button.draw(self._interface.get_window())
        self._load_button.draw(self._interface.get_window())

    def _save_level(self):
        path = f"Levels/Level{self._level}_data.json"
        super().save_level(path, self._level_data)

    def _load_level(self):
        path = f"Levels/Level{self._level}_data.json"
        try:
            self._level_data = super().load_level(path)
        except NoPlayerFoundError:
            self._level_data = {
                str(i): {
                    str(j): 0 for j in range(self._columns)
                    } for i in range(self._rows)}
        self.setup()

    def _get_mouse_coords_on_grid(self):
        position = pygame.mouse.get_pos()
        row = position[1] // self._tile_size
        column = position[0] // self._tile_size
        return row, column

    def run(self):
        clock = pygame.time.Clock()
        self.setup()
        while True:
            clock.tick(self._fps)

            self._draw_menu()

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

                        if not self._player_placed:
                            textures_number = len(textures_id_dict.keys()) - 1
                        else:
                            textures_number = len(textures_id_dict.keys()) - 2

                        if pygame.mouse.get_pressed()[0]:
                            self._level_data[row][column] += 1
                            if self._level_data[row][column] > textures_number:
                                self._level_data[row][column] = 0
                            self.setup()
                        elif pygame.mouse.get_pressed()[2]:
                            self._level_data[row][column] -= 1
                            if self._level_data[row][column] < 0:
                                self._level_data[row][column] = textures_number
                            self.setup()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self._level += 1
                    elif event.key == pygame.K_DOWN and self._level > 1:
                        self._level -= 1
            pygame.display.update()
