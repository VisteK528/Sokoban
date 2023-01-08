from level_editor import LevelEditor
from settings import level_width, level_height

if __name__ == "__main__":
    editor = LevelEditor(level_width, level_height, "Levels/")
    editor.run()
