from level_editor import LevelEditor
from settings import screen_height, screen_width

if __name__ == "__main__":
    editor = LevelEditor(screen_width, screen_height)
    editor.run()
