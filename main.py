from settings import (
    screen_height,
    screen_width,
    level)
from game import Game


if __name__ == "__main__":
    game = Game(screen_width, screen_height, level)
    game.run()
