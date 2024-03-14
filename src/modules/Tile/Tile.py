import pygame as pg
import os

cwd = os.getcwd()
path = cwd + "/src/sprites/environ/"

NULL = pg.image.load(path + "NULL.png")

class Tile(object):
    def __init__(self, name: str, collide: bool, coords: tuple[int, int]):
        self._name: str = name
        self._collide: bool = collide
        self._coords: tuple[int, int] = coords
        self._rect = pg.rect.Rect(coords[0], coords[1], 16, 16)
        try:
            self._image = pg.image.load(path + name + ".png")
        except Exception:
            print(f"Tile: {name}  Not found (image)")
            self._image = NULL

    def draw(self, screen):
        pg.draw.rect(screen, (50, 50, 50), self._rect, 4)
