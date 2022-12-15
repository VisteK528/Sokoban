import pygame
import sys
from level import Level


class Game:
    def __init__(self, screen_width, screen_height, level=1):
        self._level = level
        self._fps = 15
        self._resolution = (screen_width, screen_height)
        self._background_color = "black"

    def run(self):
        clock = pygame.time.Clock()
        window = pygame.display.set_mode(self._resolution)
        level = Level(self._resolution[0], self._resolution[1], self._level)
        level.setup()
        while True:
            clock.tick(self._fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            window.fill("black")
            level.run(window)
            level.draw_grid(window)

            pygame.display.update()
