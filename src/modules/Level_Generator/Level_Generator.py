import pygame as pg
import os
import random as rand
import time

pg.init()
screen = pg.display.set_mode((450, 450))
pg.display.set_caption("")
clock = pg.time.Clock()

"""
Inspiration taken from Bob Nystrom (https://journal.stuffwithstuff.com/2014/12/21/rooms-and-mazes/)
I tried to follow their ideas, but with my own twists and parameters for things. (Thanks Bob)
"""

##  Stages of generation  ##
"""
1: Place rooms
2: Randomized flood-fill
"""

"""   TODO
Flood-fill:
    Choose starting point
"""

### GENERATION PARAMETERS ###
level_size: tuple[int, int] = (150, 150)  # (x, y)

# Normal rooms
room_placement_attempts: int = 100  # Attempts to place rooms
room_minimum_size: tuple[int, int] = (8, 8)  # Minimum room size (x, y)
room_maximum_size: tuple[int, int] = (20, 20)  # Maximum room size (x, y)

##  generation dictionary  ##
# 'X' = wall
# 'f' = floor   (may be replaced with special tile)
# 'r' = room
# 'h' = hallway (may be filled with X)

# Room colors (couldn't figure out how to import them)
_ROOMS: dict[int, pg.color.Color] = {
  0 :  pg.color.Color(255, 179, 198),
  1 :  pg.color.Color(255, 192, 159),
  2 :  pg.color.Color(255, 238, 147),
  3 :  pg.color.Color(252, 245, 199),
  4 :  pg.color.Color(160, 206, 217),
  5 :  pg.color.Color(173, 247, 182),
  6 :  pg.color.Color(128, 155, 206),
  7 :  pg.color.Color(149, 184, 209),
  8 :  pg.color.Color(184, 224, 210),
  9 :  pg.color.Color(214, 234, 223),
  10 : pg.color.Color(234, 196, 213),
  11 : pg.color.Color(232, 209, 197),
  12 : pg.color.Color(126, 196, 207),
  13 : pg.color.Color(82,  178, 207)
}

__areas = 0


def new_area():
    global __areas
    __areas += 1
    return __areas


class Room(object):
    def __init__(self, x, y, w, h):
        self.area = new_area()
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pg.rect.Rect(x, y, w, h)


class Level(object):
    def __init__(self):
        r"""Create new level object with set 'GENERATION PARAMETERS' (Level_Generator.py)"""
        self._map = Level.blank_map()

        # Carve rooms
        self.__existing_rooms: list[Room] = []
        self.__disp_list: list[pg.rect.Rect | Room] = []
        self.carve_rooms()

        # self.carve_hallways()

        self.__test__(True, self._map)

    def carve(self, coordinate: tuple[int, int], new: str = ' ', disp_list=True):
        self._map[coordinate[1]][coordinate[0]] = new
        if disp_list:
          self.__disp_list.append(pg.rect.Rect(coordinate[1], 
                                               coordinate[0], 
                                               1, 1))

    # Stage 1
    def carve_rooms(self):
        r"""Attempt to carve room randomly"""
      
        for attempt in range(room_placement_attempts):
            # Generate possible room
            room_w: int = rand.randint(room_minimum_size[0], room_maximum_size[0])
            room_h: int = rand.randint(room_minimum_size[1], room_maximum_size[1])
            room_x: int = rand.randint(1, level_size[0] - room_w - 1)  # Level width  - 1
            room_y: int = rand.randint(1, level_size[1] - room_h - 1)  # Level height - 1

            current_room = Room(room_x, room_y, room_w, room_h)

            # Checking for collisions
            def check_room_collision() -> bool:

                # Create inflated version to prevent room adjacency
                testing_room = pg.rect.Rect(
                    current_room.x - 1,
                    current_room.y - 1,
                    current_room.w + 2,
                    current_room.h + 2
                )

                # Check actual collisions
                for checking_room in self.__existing_rooms:
                    if testing_room.colliderect(checking_room.rect):
                        return False
                return True

            # If room is NOT colliding
            if check_room_collision():

                # Carve room out of self._map
                for y in range(current_room.y, current_room.h + current_room.y + 1):
                    for x in range(current_room.x, current_room.w + current_room.x + 1):
                        self.carve((x, y), 'r', disp_list=False)

                self.__existing_rooms.append(current_room)
                self.__disp_list.append(current_room)


    # Stage 2
    def carve_hallways(self):
        r"""Carve the hallways"""

        def check_neighbors(crd, origin=None, preorigin=None) -> list[tuple[int, int]] | None:
            r"""Returns all carvable neighbors"""

            # Fixes some
            area = self._map
            if origin is not None:
                area[origin[1]][origin[0]] = 'X'
            if preorigin is not None:
                area[preorigin[1]][preorigin[0]] = 'X'
              
            # Section out a 3x3 area around the tile being checked
            # rows = self._map[crd[1] - 1: crd[1] + 2]
            # area = [row for row in rows[crd[0] - 1: crd[0] + 2]]


            # Find the coordinates of neighbors
            neighbors = []
            for y, y_row in enumerate(area[crd[1] - 1: crd[1] + 2]):
                for x, x_row in enumerate(y_row[crd[0] - 1: crd[0] + 2]):
                    if area[y][x] != 'X':
                        neighbors.append((x, y))

            # No neighbors
            if neighbors == []:
                return None

            # Return all neighbors
            return neighbors

        """
        XXXXXXXXXXXXX
        XXhXnXXXXXXXX
        XXhXhXXXXXXXX
        XXhhhXXXXXXXX
        XXXXXXXXXXXXX
        """

        # A list of all tiles that have carvable neighbors
        alive_tiles = []
        for y, y_axis in enumerate(self._map):
            for x, tile in enumerate(y_axis):
                if tile == 'X':
                    alive_tiles.append((x, y))

        start_coordinate = (1, 1)  # x, y of starting coordinate for floodfill
        while check_neighbors(start_coordinate) is None:
            start_coordinate = (start_coordinate[0] + 1, 1)

    @classmethod
    def blank_map(cls) -> list[list[str]]:
        _map: list = []
        for y in range(level_size[1]):
            x_axis: list[str] = []
            for x in range(level_size[0]):
                x_axis.append('X')
            _map.append(x_axis)
        return _map

    def __test__(self, constant, _map: list[list[str]]):
        r"""Run to visualize the current level."""

        # To incramentally show the generation as it happened
        next_disp_item = 0

        # Varies based on what type of item is displayed
        tick_speed = 60

        # Display loop
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()

            screen.fill((255, 255, 255))

            # For each item that was added to __disp_list. Incriments to look fancy
            for _disp_item in self.__disp_list[:next_disp_item]: 
              
                draw_color = (100, 100, 100)

                # If '_disp_item' is a PyGame Rect, treat it as such
                if isinstance(_disp_item, pg.rect.Rect):
                    # Check individual colors (won't differentiate between seperate hallways)
                    match self._map[_disp_item.y][_disp_item.x]:
                        case 'X':
                            tick_speed = 99999999
                            draw_color = (240, 240, 240)
                        case _:
                            tick_speed = 100
                            draw_color = (255, 0, 255)
              
                elif isinstance(_disp_item, Room):
                    tick_speed = 30
                    draw_color = _ROOMS[_disp_item.area % len(_ROOMS)]
                  

                disp_item = pg.rect.Rect(_disp_item.x * 3, 
                   _disp_item.y * 3, 
                   _disp_item.w * 3, 
                   _disp_item.h * 3)
              
                pg.draw.rect(screen, draw_color, disp_item)

            clock.tick(tick_speed)

            next_disp_item += 1

            pg.display.update()



def level_generator_function(screen):
    return Level()


level_generator_function(None)
