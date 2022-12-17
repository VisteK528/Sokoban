from player import Player
import pygame


def test_move_up(monkeypatch):
    def fake_input():
        keys = {i: False for i in range(512)}
        keys.update({pygame.K_w: True})
        return keys

    player = Player(0, 0)
    monkeypatch.setattr("pygame.key.get_pressed", fake_input)
    player.update()
    assert player.direction.x == 0
    assert player.direction.y == -1


def test_move_down(monkeypatch):
    def fake_input():
        keys = {i: False for i in range(512)}
        keys.update({pygame.K_s: True})
        return keys
    player = Player(0, 0)
    monkeypatch.setattr("pygame.key.get_pressed", fake_input)
    player.update()
    assert player.direction.x == 0
    assert player.direction.y == 1


def test_move_left(monkeypatch):
    def fake_input():
        keys = {i: False for i in range(512)}
        keys.update({pygame.K_a: True})
        return keys
    player = Player(0, 0)
    monkeypatch.setattr("pygame.key.get_pressed", fake_input)
    player.update()
    assert player.direction.x == -1
    assert player.direction.y == 0


def test_move_right(monkeypatch):
    def fake_input():
        keys = {i: False for i in range(512)}
        keys.update({pygame.K_d: True})
        return keys
    player = Player(0, 0)
    monkeypatch.setattr("pygame.key.get_pressed", fake_input)
    player.update()
    assert player.direction.x == 1
    assert player.direction.y == 0
