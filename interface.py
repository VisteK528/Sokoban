import pygame


class Interface:
    def __init__(self, resolution):
        self._resolution = resolution
        self._window = pygame.display.set_mode(self._resolution)
        pygame.font.init()
        self._font = pygame.font.SysFont('Liberation Serif', 24)

    def get_window(self):
        return self._window

    def draw_grid(self, rows, columns, tile_size,
                  color=(255, 255, 255), x=0, y=0):
        width = rows*tile_size
        height = columns*tile_size
        for row_count in range(rows+1):
            pygame.draw.line(
                self._window, color,
                (x, row_count*tile_size),
                (x+width, row_count*tile_size))

        for column_count in range(columns+1):
            pygame.draw.line(
                self._window, color,
                (column_count*tile_size, y),
                (column_count * tile_size, y+height))

    def draw_text(self, text, x, y, color=(255, 255, 255)):
        img = self._font.render(text, True, color)
        self._window.blit(img, (x, y))

    def fill_color(self, color="black"):
        self._window.fill(color)

    def draw_sprites(self, sprites_list):
        for sprite_group in sprites_list:
            sprite_group.draw(self._window)


class Button:
    def __init__(self, x, y, image_path):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def action(self):

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                return True
        return False
