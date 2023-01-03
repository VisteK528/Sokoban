from level_editor import LevelEditor
from settings import level_width, level_height

if __name__ == "__main__":
    editor = LevelEditor(level_height, level_width, "Levels/")
    editor.run()
