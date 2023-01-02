import pygame
from typing import Tuple
import sys


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
    Class Interface Contains attributes:
    :param resolution: Resolution of the display in pixels (width, height)
    :type resoultion: tuple of integers
    :param window_title: Tile of the displayed window
    :type window_title: str
    :param default_font: Default font and font size used in the interface,
    default - Retro_Gaming, 20. Format - (path, size)
    :type default_font: tuple of str and int
    """
    def __init__(self, resolution: Tuple[int, int], window_title=None,
                 default_font=None):
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

    def set_font(self, font: Tuple[str, int]):
        self._default_font, self._default_font_size = font

    def font(self) -> Tuple[str, int]:
        return self._default_font, self._default_font_size

    def get_window(self) -> pygame.display:
        """
        Returns Interface's display object
        """
        return self._window

    def draw_grid(self, rows, columns, tile_size,
                  color=RGB(255, 255, 255), x=0, y=0):
        """
        Draws grid on the screen with specified parameters
        :param rows: Number of rows in the grid
        :type rows: int
        :param columns: Number of columns in the grid
        :type columns: int
        :param tile_size: Size of one cell in the grid (which is a square)
        :type tile_size: int
        :param color: Color of grid's lines in RGB format
        :type color: RGB class
        :param x: X-coordinate of the grid (anchor=NW), default x=0
        :type x: int
        :param y: Y-coorindate of the grind(anchor=NW), default y=0
        """
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
        :param alpha: Opacity of the rectangle, default alpha=255
        :type alpha: int
        """
        x, y = self._convert_coords_by_anchor(x, y, width, height, anchor)
        image = pygame.Surface((width, height))
        image.set_alpha(alpha)
        image.fill(color.rgb())
        rect = image.get_rect(topleft=(x, y))
        self._window.blit(image, (rect.x, rect.y))

    def _convert_coords_by_anchor(self, x: int, y: int, width: int,
                                  height: int, anchor: str) -> Tuple[int, int]:
        """
        Converts NW oriented x, y coordinates in order to move
        object's anchor one of different anchors

        Parameters
        ----------
        :param x: X coordinate of NW oriented object
        :type x: int
        :param y: Y cooridnate of NW oriented object
        :type y: int
        :param width: Width of an object
        :type width: int
        :param height: Height of an object
        :type height: int
        :param anchor: One of 5 possible object's anchors
                       1. NW - North-West
                       2. NE - North-East
                       3. SW - South-West
                       4. SE - South-East
                       5. CENTER - Center
        :type anchor: str
        """

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

    def draw_text(self, text, x, y, color=RGB(255, 255, 255),
                  anchor="NW", font=None) -> None:
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

    def draw_message(self, x: int, y: int, width: int, height: int, bg: RGB,
                     text_color: RGB, message: str,
                     font: pygame.font.Font) -> None:
        """
        Displays message on the screen,
        stays in loop as long as user does not accept the message

        Parameters
        ----------

        :param x: X coordinate of message, anchor=CENTER
        :type x: int
        :param y: Y cooridnate of message, anchor=CENTER
        :type y: int
        :param width: Width of the message
        :type width: int
        :param height: Height of the message
        :type height: int
        :param bg: Background color of the message, RGB format
        :type bg: RGB class
        :param text_color: Color of the message, RGB format
        :type text_color: RGB class
        :param message: Message
        :type message: str
        :param font: Font used to display message
        :type font: pygame.font.Font
        """
        text_size = font.size(message)
        if (text_size[0] > width or
                text_size[1] > height):
            raise TextDimensionsError(
                (width, height), text_size,
                "Text represented in given font is too big"
                " to fit rectangle with given dimensions"
            )
        self.draw_rectangle(x, y, width, height, bg, "CENTER")
        self.draw_text(message, x, y-40, text_color, "CENTER", font)

        button_width = 100
        button_height = 50
        button_x = x-button_width//2
        button_y = y+40-button_height//2
        button_text = "OK"
        button_font = pygame.font.Font(*self.font())
        ok_button = Button(button_x, button_y, button_width,
                           button_height, button_text, button_font)

        while True:
            ok_button.draw(self._window)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            if ok_button.action():
                break

    def fill_color(self, color=RGB(0, 0, 0)) -> None:
        """
        Fills the screen with single color
        :param color: RGB value of color
        :type color: RGB class
        """
        self._window.fill(color.rgb())

    def draw_sprites(self, sprites_list) -> None:
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
    """
    Class Button

    Parameters
    ----------

    :param x: X coordinate of button
    :type x: int
    :param y: Y coordinate of button
    :type y: int
    :param width: Width of button
    :type width: int
    :param height: Height of button
    :type height: int
    :param text: Text displayed on button
    :type text: str
    :param font: Font used to display text on button
    :type font: pygame.font.Font
    """
    def __init__(self, x: int, y: int, width: int, height: int,
                 text: str, font: pygame.font.Font):
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

    def set_background_color(
            self, first_color: "RGB", second_color: "RGB") -> None:
        """
        Sets button's default color and color when it collides with mouse
        """
        self._background_color_1 = first_color
        self._background_color_2 = second_color

    def set_text_color(self, first_color: "RGB", second_color: "RGB") -> None:
        """
        Sets button's text default color and text color
        when it collides with mouse
        """
        self._text_color_1 = first_color
        self._text_color_2 = second_color

    def draw(self, window: pygame.display) -> None:
        """
        Draws button on the given display
        """
        text_img = self._font.render(self._text, True, self._text_color.rgb())
        text_width, text_height = self._font.size(self._text)
        x_offset = (self._width-text_width)//2
        y_offset = (self._height-text_height)//2
        self.image.fill(self._background_color.rgb())
        window.blit(self.image, (self.rect.x, self.rect.y))
        window.blit(
            text_img, (self._x+x_offset, self._y+y_offset))

    def action(self) -> bool:
        """
        Checks if user mouse collided with button object.
        If user mouse collided with button object
        and user used left-button then returns True.
        Otherwise returns False.
        """
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
