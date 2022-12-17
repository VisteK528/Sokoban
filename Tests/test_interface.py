from interface import Button, RGB, TextDimensionsError
from pytest import raises
import pygame


def test_create_button():
    pygame.font.init()
    font = pygame.font.SysFont("Calibri", 24)
    Button(0, 0, 100, 50, "Test", font)


def test_create_button_with_too_long_text():
    pygame.font.init()
    font = pygame.font.SysFont("Calibri", 24)
    with raises(TextDimensionsError):
        Button(
            0, 0, 100, 50, "This is too long text", font)


def test_create_rgb_class():
    rgb = RGB(200, 200, 200)
    assert rgb.rgb() == (200, 200, 200)


def test_create_rgb_with_invalid_values():
    with raises(ValueError):
        RGB(-10, 260, 300)


def test_set_rgb_class():
    rgb = RGB(150, 150, 150)
    assert rgb.rgb() == (150, 150, 150)
    rgb.set_rgb(255, 255, 255)
    assert rgb.rgb() == (255, 255, 255)
