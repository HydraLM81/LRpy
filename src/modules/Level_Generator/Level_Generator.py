import pygame as pg
import os
import random as rand

pg.init()


"""
Inspiration taken from Bob Nystrom (https://journal.stuffwithstuff.com/2014/12/21/rooms-and-mazes/)
I tried to follow their ideas, but with my own twists and parameters for things. (Thanks Bob)
"""


### GENERATION PARAMETERS ###
level_size: tuple[int, int]        = (400, 400) # (x, y)

room_placement_attemps: int        = 200        # Attempts to place rooms
room_minimum_size: tuple[int, int] = (10, 10)     # Minimum room size (x, y)
room_maximum_size: tuple[int, int] = (30, 30)   # Maximum room size (x, y)

##  generation dictionary  ##
# 'X' = wall
# ' ' = floor
# '█' = disp character (shouldn't show)


class Level(object):
    def __init__(self):
        r"""Create new level object with set 'GENERATION PARAMETERS' (Level_Generator.py)"""
        self._map = Level.blank_map()

        # Attempts {room_placement_attemps} times to carve rooms
        self.__existing_rooms = []
        for attempt in range(room_placement_attemps):
            self.carve_room()

        def test():
            screen = pg.display.set_mode((800, 450))
            pg.display.set_caption("")
            clock = pg.time.Clock()

            print(self.__existing_rooms)

            while True:
                print('aa')
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        exit()

                screen.fill((255, 255, 255))

                for rect in self.__existing_rooms:
                    pg.draw.rect(screen, (100, 100, 100), rect)

                clock.tick(5)
                pg.display.update()
        test()

    def carve(self, coordinate: tuple[int, int], new: str = ' '):
        self._map[coordinate[1]][coordinate[0]] = new

    def carve_room(self):
        r"""Attempt to carve room randomly"""

        # Generate possible room
        room_w: int = rand.randint(room_minimum_size[0], room_maximum_size[0])
        room_h: int = rand.randint(room_minimum_size[1], room_maximum_size[1])
        room_x: int = rand.randint(1, 399 - room_w - 1)  # Screen width  - 1
        room_y: int = rand.randint(1, 399 - room_h - 1)  # Screen height - 1

        current_room = pg.rect.Rect(room_x, room_y, room_w, room_h)

        # Checking for collisions
        def check_room_collision():
            testing_room = current_room

            # Inflate room by 1 to preserve walls
            testing_room.x -= 1
            testing_room.y -= 1
            testing_room.w += 2
            testing_room.h += 2

            # Check
            for checking_room in self.__existing_rooms:
                if testing_room.colliderect(checking_room):
                    return False
            return True

        # If room is colliding (not allowed)
        if not check_room_collision():
            return
        # Else: Room can be placed. 'pg.rect.Rect' used for 'colliderect' convenience

        self.__existing_rooms.append(current_room)

        # Carve room out of self._map
        for y in range(current_room.y, current_room.h + 1):
            for x in range(current_room.x, current_room.w + 1):
                self.carve((x, y))




    @classmethod
    def blank_map(cls):
        _map = []
        for y in range(level_size[1]):
            x_axis = []
            for x in range(level_size[0]):
                x_axis.append('X')
            _map.append(x_axis)
        return _map


def level_generator_function(screen):
    return Level()

level_generator_function(None)
