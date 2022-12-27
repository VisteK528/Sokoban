import pygame


class TextDimensionsError(Exception):
    def __init__(self, widget_dimensions, text_dimensions, message):
        super().__init__(message)
        self._widget_width = widget_dimensions
        self._text_width = text_dimensions


class InvalidAlignmentError(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)


class RGB:
    """
    Class RGB. Contains attributes:
    :param r: Red value in RGB code, from 0 to 255
    :type r: int
    :param g: Green value in RGB code, from 0 to 255
    :type g: int
    :param b: Blue value in RGB code, from 0 to 255
    :type b: int
    """
    def __init__(self, r: int, g: int, b: int):
        self.set_rgb(r, g, b)

    def set_rgb(self, r: int, g: int, b: int):
        """
        Sets r, g and b values of RGB code
        if value of any of given values is not in range
        from 0 to 255 raises ValueError
        """
        if 0 <= r <= 255:
            self._r = r
        else:
            raise ValueError("Red value should be between 0 and 255")

        if 0 <= g <= 255:
            self._g = g
        else:
            raise ValueError("Green value should be between 0 and 255")

        if 0 <= b <= 255:
            self._b = b
        else:
            raise ValueError("Blue value should be between 0 and 255")

    def rgb(self):
        """
        Returns tuple of r,g and b values of RGB code
        """
        return self._r, self._g, self._b


class Interface:
    """
    Class Interface
    """
    def __init__(self, resolution, window_title=None, default_font=None):
        self._resolution = resolution
        self._window = pygame.display.set_mode(self._resolution)
        if window_title is not None:
            pygame.display.set_caption(window_title)
        pygame.font.init()
        if default_font is None:
            self._default_font = "Textures/Retro_Gaming.ttf"
            self._default_font_size = 20
        else:
            self._default_font = default_font[0]
            self._default_font_size = default_font[1]

    def set_font(self, font):
        self._default_font, self._default_font_size = font

    def font(self):
        return self._default_font, self._default_font_size

    def get_window(self):
        return self._window

    def draw_grid(self, rows, columns, tile_size,
                  color=RGB(255, 255, 255), x=0, y=0):
        width = rows*tile_size
        height = columns*tile_size
        for row_count in range(rows+1):
            pygame.draw.line(
                self._window, color.rgb(),
                (x, row_count*tile_size),
                (x+width, row_count*tile_size))

        for column_count in range(columns+1):
            pygame.draw.line(
                self._window, color.rgb(),
                (column_count*tile_size, y),
                (column_count * tile_size, y+height))

    def draw_rectangle(
            self, x: int, y: int, width: int, height: int, color: RGB,
            anchor="NW", alpha=255):
        """
        Draws rectangle on the screen with specified parameters
        :param x: X coordinate of the rectangle
        :type x: int
        :param y: Y coordinate of the rectangle
        :type y: int
        :param width: Width of the rectangle
        :type width: int
        :param height: Height of the rectangle
        :type height: int
        :param color: Color of the rectangle in RGB
        :type color: RGB class
        :param anchor: Anchor of the (x, y) coordinates, default "NW",
                       available anchors: ''NE', 'NW', 'SE', 'SW' and 'CENTER'
        :type anchor: str
        """
        x, y = self._convert_coords_by_anchor(x, y, width, height, anchor)
        image = pygame.Surface((width, height))
        image.set_alpha(alpha)
        image.fill(color.rgb())
        rect = image.get_rect(topleft=(x, y))
        self._window.blit(image, (rect.x, rect.y))

    def _convert_coords_by_anchor(
            self, x: int, y: int, width: int, height: int, anchor: str):

        anchor = anchor.lower()
        if anchor not in ["ne", "nw", "se", "sw", "center"]:
            raise InvalidAlignmentError(
                "Invalid anchor selected, select from 'NE', 'NW',"
                " 'SE', 'SW' and 'CENTER'"
            )
        if anchor == "nw":
            return x, y
        elif anchor == "ne":
            return x-width, y
        elif anchor == "sw":
            return x, y-height
        elif anchor == "se":
            return x-width, y-height
        elif anchor == "center":
            return x-width//2, y-height//2

    def draw_text(
           self, text, x, y, color=RGB(255, 255, 255), anchor="NW", font=None):
        """
        Draws text on the screen on the given coordinates (x, y)
        :param color: Color of the text, default RGB(255, 255, 255) (white)
        :type color: RGB class
        :param anchor: Anchor of the (x, y) coordinates, default "NW",
                       available anchors: ''NE', 'NW', 'SE', 'SW' and 'CENTER'
        :type anchor: str
        :param font: Font used to display text, default (Liberation Serif, 24)
        :type font: pygame.font.Font
        """
        if font is None:
            font_name = self._default_font
            font_size = self._default_font_size
            font = pygame.font.Font(font_name, font_size)

        img = font.render(text, True, color.rgb())
        text_width, text_height = font.size(text)
        x, y = self._convert_coords_by_anchor(
            x, y, text_width, text_height, anchor)
        self._window.blit(img, (x, y))

    def fill_color(self, color=RGB(0, 0, 0)):
        """
        Fills the screen with single color
        :param color: RGB value of color
        :type color: RGB class
        """
        self._window.fill(color.rgb())

    def draw_sprites(self, sprites_list):
        """
        Draws on screen all sprites of each group in given list of sprites
        :param sprites_list: List of groups of pygame sprites
        :type sprites_list: list
        """
        for sprite_group in sprites_list:
            for sprite in sprite_group:
                sprite.update_visual(50)
            sprite_group.draw(self._window)


class Button:
    def __init__(self, x, y, width, height, text, font):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._font = font
        self._text = text
        self._text_size = self._font.size(text)
        if (self._text_size[0] > self._width or
                self._text_size[1] > self._height):
            raise TextDimensionsError(
                (self._width, self._height),
                self._text_size,
                "Text represented in given font is too big"
                " to fit Button with given dimensions"
            )

        self._text_color_1 = RGB(0, 0, 0)
        self._text_color_2 = RGB(255, 255, 255)
        self._background_color_1 = RGB(211, 211, 211)
        self._background_color_2 = RGB(0, 0, 0)
        self._text_color = self._text_color_1
        self._background_color = self._background_color_1

        self.image = pygame.Surface((self._width, self._height))
        self.image.fill(self._background_color.rgb())
        self.rect = self.image.get_rect(topleft=(self._x, self._y))

    def set_background_color(self, first_color: "RGB", second_color: "RGB"):
        self._background_color_1 = first_color
        self._background_color_2 = second_color

    def set_text_color(self, first_color: "RGB", second_color: "RGB"):
        self._text_color_1 = first_color
        self._text_color_2 = second_color

    def draw(self, window):
        text_img = self._font.render(self._text, True, self._text_color.rgb())
        text_width, text_height = self._font.size(self._text)
        x_offset = (self._width-text_width)//2
        y_offset = (self._height-text_height)//2
        self.image.fill(self._background_color.rgb())
        window.blit(self.image, (self.rect.x, self.rect.y))
        window.blit(
            text_img, (self._x+x_offset, self._y+y_offset))

    def action(self):
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            self._text_color = self._text_color_2
            self._background_color = self._background_color_2
            if pygame.mouse.get_pressed()[0]:
                return True
        else:
            self._text_color = self._text_color_1
            self._background_color = self._background_color_1
            return False
