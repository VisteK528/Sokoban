import pygame
import sys
from level import Level
from load_level import LoadLevel
from interface import Interface, Button, RGB
from time import sleep


class Game:
    def __init__(self, screen_width, screen_height, level=1):
        self._level = level
        self._fps = 120
        self._tile_size = 50
        self._info_width = 400
        self._resolution = (screen_width, screen_height)
        self._background_color = RGB(173, 216, 230)

        # Interface and Fonts
        self._interface = Interface(self._resolution, "Sokoban Game")
        self._header_font = pygame.font.Font(self._interface.font()[0], 40)
        self._text_font = pygame.font.Font(self._interface.font()[0], 15)
        self._button_font = pygame.font.Font(self._interface.font()[0], 20)

    def _load_level(self):
        width = self._resolution[0]-self._info_width
        height = self._resolution[1]
        path = f"Levels/Level{self._level}_data.json"

        load_level = LoadLevel(width, height, self._tile_size)

        level_data = load_level.load_level(path)
        level = Level(width, height, level_data, self._tile_size)
        level.setup()
        return level

    def run(self):
        clock = pygame.time.Clock()
        level = self._load_level()
        restart_btn = Button(
            self._resolution[0]-340, 300, 280, 80, "RESTART LEVEL",
            self._button_font)
        restart_btn.set_background_color(RGB(0, 0, 0), RGB(255, 255, 255))
        restart_btn.set_text_color(RGB(255, 255, 255), RGB(0, 0, 0))
        while True:
            clock.tick(self._fps)
            # Fill the screen with color
            self._interface.fill_color(self._background_color)

            # Menu
            self._interface.draw_rectangle(
                1000, 0, 400, 1000, RGB(65, 105, 225))

            title = "Sokoban Game"
            self._interface.draw_text(
                title, 1200, 40, RGB(0, 0, 0), anchor="CENTER",
                font=self._header_font)

            # Draw level number, restart button
            level_text = f"LEVEL: {self._level}"
            self._interface.draw_text(level_text, self._resolution[0]-340, 100)

            moves_text = f"MOVES: {level.get_player_moves()}"
            self._interface.draw_text(moves_text, self._resolution[0]-340, 150)

            push_text = f"PUSHES: {level.get_player_pushes()}"
            self._interface.draw_text(push_text, self._resolution[0]-340, 200)

            restart_btn.draw(self._interface.get_window())
            if restart_btn.action():
                level = self._load_level()

            # Uncomment to draw grid
            # rows, columns = level.get_dimensions()
            # interface.draw_grid(rows, columns, 50)
            if level.run():
                self._interface.draw_sprites(level.get_sprites())
                pygame.display.update()
                self._level += 1
                level = self._load_level()
                sleep(0.5)
            self._interface.draw_sprites(level.get_sprites())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
