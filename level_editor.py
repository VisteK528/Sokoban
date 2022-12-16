from level import Level
import pygame
import sys
from settings import textures_id_dict
from interface import Interface, Button


class LevelEditor(Level):
    def __init__(self, width, height, level=1, tile_size=50):
        super().__init__(width, height, level, tile_size)
        self._tools_margin = 400
        self._resolution = (self._width+self._tools_margin, self._height)
        self._fps = 60

    def run(self):
        clock = pygame.time.Clock()
        interface = Interface(self._resolution)
        save_button = Button(
            self._width + 20, 280, "Textures/Save.png")
        load_button = Button(
            self._width + 20, 150, "Textures/Load.png")
        clicked = False
        self.setup()
        while True:
            clock.tick(self._fps)
            interface.fill_color("black")
            interface.draw_sprites(self.get_sprites())
            interface.draw_grid(self._rows, self._columns, self._tile_size)
            save_button.draw(interface.get_window())
            load_button.draw(interface.get_window())

            interface.draw_text(
                f'Level: {self._level}', self._width+20, 50)
            interface.draw_text(
                'Press UP or DOWN to change level', self._width+20, 70)

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
