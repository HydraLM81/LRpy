import pygame as pg
import os

cwd = os.getcwd()
path = cwd + "/src/sprites/player/"


class Player(object):
    # Every possible state of player included
    def __init__(self, currency: int):
        self._currency = currency

    @classmethod
    def create_new_player(cls):
        # DEFAULT PARAMS:
        # (0)
        return Player(0)

    @classmethod
    def load_past_player(cls, name):
        pass
