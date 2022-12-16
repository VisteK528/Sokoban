import pygame
import sys
from level import Level
from interface import Interface, Button


class Game:
    def __init__(self, screen_width, screen_height, level=1):
        self._level = level
        self._fps = 20
        self._info_width = 400
        self._resolution = (screen_width, screen_height)
        self._background_color = "black"

    def load_level(self):
        level = Level(self._resolution[0]-self._info_width,
                      self._resolution[1], self._level)
        level.setup()
        return level

    def run(self):
        clock = pygame.time.Clock()
        interface = Interface(self._resolution)
        level = self.load_level()
        restart_btn = Button(self._resolution[0]-300, 200, "Textures/Save.png")
        while True:
            clock.tick(self._fps)
            # Fill the screen with color
            interface.fill_color()

            # Draw level number, restart button
            text = f"Level: {self._level}"
            interface.draw_text(text, self._resolution[0]-300, 100)
            restart_btn.draw(interface.get_window())
            if restart_btn.action():
                level = self.load_level()

            # Logic
            rows, columns = level.get_dimensions()
            interface.draw_grid(rows, columns, 50)
            if level.run():
                self._level += 1
                level = self.load_level()
            interface.draw_sprites(level.get_sprites())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
