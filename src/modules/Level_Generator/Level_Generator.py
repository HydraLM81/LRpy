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

# Room generation parameters
room_placement_attempts: int = 0  # Attempts to place rooms
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


class DispItem(object):
    def __init__(self, obj: pg.rect.Rect | Room, char: str):
        self.obj: pg.rect.Rect | Room = obj
        self.char: str = char


class Level(object):
    def __init__(self):
        r"""Create new level object with set 'GENERATION PARAMETERS' (Level_Generator.py)"""
        self._map = Level.blank_map()

        # Carve rooms
        self.__existing_rooms: list[Room] = []
        self.__disp_list: list[DispItem] = []
        # self.carve_rooms()

        self.carve_hallways()

        self.__test__(self._map)

    def carve(self, coordinate: tuple[int, int], new: str = ' ', disp_list=True):
        self._map[coordinate[1]][coordinate[0]] = new
        if disp_list:
            self.__disp_list.append(DispItem(pg.rect.Rect(coordinate[1],
                                             coordinate[0],
                                             1, 1),
                                             new))
    
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
                self.__disp_list.append(DispItem(current_room, 'r'))

    # Stage 2
    def carve_hallways(self):
        r"""Carve the hallways"""
        
        def check_neighbors(crd):
            r"""Check if a tile has any neighbors directly around it."""
            # Check out of bounds
            if crd[0] <= 0 or crd[0] >= level_size[0] - 2:
                return False
            if crd[1] <= 0 or crd[1] >= level_size[1] - 1:
                return False

            # Get a 3x3 area around crd
            rows = self._map[crd[1] - 1: crd[1] + 2]
            area = [row[crd[0] - 1: crd[0] + 2] for row in rows]

            area[1][1] = 'X'
            if area[0].count('X') == area[1].count('X') == area[2].count('X') == 3:
                return True
            return False

        def _crdlist(crd):
            return [((crd[0] + 2, crd[1]), (crd[0] + 1, crd[1])),
                    ((crd[0] - 2, crd[1]), (crd[0] - 1, crd[1])),
                    ((crd[0], crd[1] - 2), (crd[0], crd[1] - 1)),
                    ((crd[0], crd[1] + 2), (crd[0], crd[1] + 1))]

        alive_cells: list[tuple[tuple[int, int], tuple[int, int]]] = []  # (crd, came_from)
        alive_cells.append(((1, 1), (1, 1)))
        ctime = time.time()
        print("Starting loop")
        while len(alive_cells) > 0:
            print(f"Len cells: {len(alive_cells)}")
            _current_cell = alive_cells[-1]
            current_cell = _current_cell[0]
            last_cell = _current_cell[1]
            
            if self._map[current_cell[1]][current_cell[0]] == 'X':
                self.carve(current_cell, 'ch')
            
            crdlist = _crdlist(current_cell)

            rand.shuffle(crdlist)

            if check_neighbors(crdlist[0][0]):
                self.carve(crdlist[0][1], 'ch', True)
                alive_cells.append(crdlist[0])
                
            elif check_neighbors(crdlist[1][0]):
                self.carve(crdlist[1][1], 'ch', True)
                alive_cells.append(crdlist[1])
            
            elif check_neighbors(crdlist[2][0]):
                self.carve(crdlist[2][1], 'ch', True)
                alive_cells.append(crdlist[2])
            
            elif check_neighbors(crdlist[3][0]):
                self.carve(crdlist[3][1], 'ch', True)
                alive_cells.append(crdlist[3])
            
            else:
                self.carve(current_cell, 'h', True)
                self.carve(last_cell, 'h', True)
                alive_cells.pop(-1)
        print("Loop done")
        print(f"Time taken in loop: {time.time() - ctime}")
        print(f"disp_list length after hallways: {len(self.__disp_list)}")
            

    @classmethod
    def blank_map(cls) -> list[list[str]]:
        _map: list = []
        for y in range(level_size[1]):
            x_axis: list[str] = []
            for x in range(level_size[0]):
                x_axis.append('X')
            _map.append(x_axis)
        return _map

    def __test__(self, _map: list[list[str]]):
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

            # For each item that was added to __disp_list. Increments to look fancy
            for _disp_item in self.__disp_list[:next_disp_item]: 
              
                draw_color = (100, 100, 100)
                
                # If '_disp_item' is a PyGame Rect, treat it as such
                if isinstance(_disp_item.obj, pg.rect.Rect):
                    # Check individual colors (won't differentiate between separate hallways)
                    match _disp_item.char:
                        case 'X':
                            tick_speed = 99999999
                            draw_color = (0, 0, 0)
                        case "ch":
                            tick_speed = 250
                            draw_color = (0, 200, 240)
                        case 'h':
                            tick_speed = 250
                            draw_color = (100, 0, 240)
                        case _:
                            print(f"Uncaught: \'{_disp_item.char}\'")
                            tick_speed = 100
                            draw_color = (255, 0, 255)
              
                elif isinstance(_disp_item.obj, Room):
                    tick_speed = 30
                    draw_color = _ROOMS[_disp_item.obj.area % len(_ROOMS)]

                disp_item = pg.rect.Rect(_disp_item.obj.x * 3,
                                         _disp_item.obj.y * 3,
                                         _disp_item.obj.w * 3,
                                         _disp_item.obj.h * 3)
              
                pg.draw.rect(screen, draw_color, disp_item)

            clock.tick(tick_speed)

            next_disp_item += 1

            pg.display.update()


def level_generator_function():
    return Level()


level_generator_function()
