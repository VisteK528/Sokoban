from settings import (
    level_width,
    level_height,
    level,
    max_level)
from game import Game


if __name__ == "__main__":
    game = Game(level_width, level_height, level, max_level)
    game.run()
