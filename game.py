import pygame
import sys
from level import Level
from load_level import LoadLevel, check_requirements
from interface import Interface, Button, RGB
from time import sleep


class Game:
    def __init__(
            self, screen_width, screen_height, level, max_level, tile_size=50):
        # Interface and Fonts
        self._resolution = (screen_width, screen_height)
        self._interface = Interface(self._resolution, "Sokoban Game")
        self._header_font = pygame.font.Font(self._interface.font()[0], 40)
        self._text_font = pygame.font.Font(self._interface.font()[0], 15)
        self._button_font = pygame.font.Font(self._interface.font()[0], 20)
        self._background_color = RGB(173, 216, 230)
        self._info_width = 400
        self._tile_size = 50
        self._fps = 120
        self._tile_size = tile_size

        self._restart_btn = Button(
            self._resolution[0]-340, 300, 280, 80, "RESTART LEVEL",
            self._button_font)
        self._restart_btn.set_background_color(
            RGB(0, 0, 0), RGB(255, 255, 255))
        self._restart_btn.set_text_color(RGB(255, 255, 255), RGB(0, 0, 0))

        # Logic
        self._level = level
        self._max_level = max_level
        self._game_on = True
        self._level_width = self._resolution[0] - self._info_width
        self._level_height = self._resolution[1]
        self._rows = self._level_height // self._tile_size
        self._columns = self._level_width // self._tile_size
        self._key_clicked = False

    def _display_victory_message(self):
        text = "Congratulations!"
        text2 = "You have finished the Sokoban Game!"
        self._interface.draw_rectangle(
            0, 0, self._level_width, self._level_height,
            RGB(255, 255, 255), alpha=150)
        self._interface.draw_text(
            text, self._level_width//2, self._level_height//2-25,
            color=RGB(0, 0, 0), anchor="CENTER", font=self._header_font)
        self._interface.draw_text(
            text2, self._level_width//2, self._level_height//2+25,
            color=RGB(0, 0, 0), anchor="CENTER", font=self._header_font)

    def _load_level(self):
        path = f"Levels/Level{self._level}_data.json"

        load_level = LoadLevel()
        level_data = load_level.load_from_file(path)
        check_requirements(self._rows, self._columns, level_data)

        level = Level(self._rows, self._columns, level_data)
        level.setup()
        return level

    def _update_key_clicked(self, keyboard_input):
        if not (keyboard_input[pygame.K_a] or
                keyboard_input[pygame.K_d] or
                keyboard_input[pygame.K_w] or
                keyboard_input[pygame.K_s]):
            self._key_clicked = False
        else:
            self._key_clicked = True

    def run(self):
        clock = pygame.time.Clock()
        level = self._load_level()
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
            self._restart_btn.draw(self._interface.get_window())

            if self._game_on:
                if self._restart_btn.action():
                    level = self._load_level()

                keyboard_input = pygame.key.get_pressed()
                if not self._key_clicked:
                    if level.run(keyboard_input):
                        self._level += 1
                        if self._level > self._max_level:
                            self._game_on = False
                        else:
                            self._interface.draw_sprites(level.get_sprites())
                            pygame.display.update()
                            level = self._load_level()
                            sleep(0.5)

                self._update_key_clicked(keyboard_input)

            self._interface.draw_sprites(level.get_sprites())
            if self._level > self._max_level:
                self._display_victory_message()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
