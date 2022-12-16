from level import Level
import pygame
from interface_elements import Button
import sys
from settings import textures_id_dict


class LevelEditor(Level):
    def __init__(self, width, height, level=1, tile_size=50):
        super().__init__(width, height, level, tile_size)
        self._tools_margin = 400
        self._fps = 60
        self._text_color = (255, 255, 255)
        pygame.font.init()
        self._font = pygame.font.SysFont('Liberation Serif', 24)

    def run(self):
        clock = pygame.time.Clock()
        window = pygame.display.set_mode(
            (self._width+self._tools_margin, self._height))
        save_button = Button(
            self._width + 20, 280, "Textures/Save.png")
        load_button = Button(
            self._width + 20, 150, "Textures/Load.png")
        clicked = False
        self.setup()
        while True:
            clock.tick(self._fps)
            window.fill("black")
            super().draw_level(window)
            self.draw_grid(window)
            save_button.draw(window)
            load_button.draw(window)

            self.draw_text(
                window, f'Level: {self._level}',
                self._font, self._text_color, self._width+20, 50)
            self.draw_text(
                window, 'Press UP or DOWN to change level',
                self._font, self._text_color, self._width+20, 70)

            if save_button.action():
                self.save_level(
                    f"Levels/Level{self._level}_data.json", self._level_data)

            elif load_button.action():
                self._level_data = self.load_level(
                    f"Levels/Level{self._level}_data.json")
                self.setup()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and not clicked:
                    clicked = True
                    pos = pygame.mouse.get_pos()
                    x = pos[0] // self._tile_size
                    y = pos[1] // self._tile_size
                    if x < self._columns and y < self._rows:
                        x = str(x)
                        y = str(y)
                        if not self._player_placed:
                            textures_number = len(textures_id_dict.keys()) - 1
                        else:
                            textures_number = len(textures_id_dict.keys()) - 2

                        if pygame.mouse.get_pressed()[0] == 1:
                            self._level_data[y][x] += 1
                            if self._level_data[y][x] > textures_number:
                                self._level_data[y][x] = 0
                            self.setup()
                        elif pygame.mouse.get_pressed()[2] == 1:
                            self._level_data[y][x] -= 1
                            if self._level_data[y][x] < 0:
                                self._level_data[y][x] = textures_number
                            self.setup()
                if event.type == pygame.MOUSEBUTTONUP:
                    clicked = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self._level += 1
                    elif event.key == pygame.K_DOWN and self._level > 1:
                        self._level -= 1
            pygame.display.update()
