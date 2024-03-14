import pygame as pg
import os

cwd = os.getcwd()
path = cwd + "/src/sprites/environ/"

NULL = pg.image.load(path + "NULL.png")

class Tile(object):
    def __init__(self, name: str, collide: bool, coordinates: tuple[int, int]):
        r"Creates a new Tile object."
        self._name: str = name
        self._collide: bool = collide
        self._coordinates: tuple[int, int] = coordinates
        self._rect = pg.rect.Rect(coordinates[0], coordinates[1], 16, 16)

        try:
            self._image = pg.image.load(path + name + ".png")
        except Exception:
            print(f"Tile: {name}  Not found (image)")
            self._image = NULL

    def draw(self, screen):
        r"Return: (image, rect)"
        return (self._image, self._rect)
