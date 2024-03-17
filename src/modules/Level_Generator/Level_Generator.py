import pygame as pg
import os
import random as rand

pg.init()


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
level_size: tuple[int, int]        = (150, 150) # (x, y)

# Normal rooms
room_placement_attempts: int        = 100        # Attempts to place rooms
room_minimum_size: tuple[int, int] = (5, 5)     # Minimum room size (x, y)
room_maximum_size: tuple[int, int] = (20, 20)   # Maximum room size (x, y)


##  generation dictionary  ##
# 'X' = wall
# 'f' = floor   (may be replaced with special tile)
# 'r' = room
# 'h' = hallway (may be filled with X)


__areas = 0
def new_area():
    global __areas
    __areas += 1
    return __areas


class Room(object):
    def __init__(self, x, y, w, h):
        self.area = new_area()
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self.rect = pg.rect.Rect(x, y, w, h)
        

class Level(object):
    def __init__(self):
        r"""Create new level object with set 'GENERATION PARAMETERS' (Level_Generator.py)"""
        self._map = Level.blank_map()

        
        # Attempts {room_placement_attempts} times to carve rooms
        self.__existing_rooms = []
        self.carve_rooms()

            
        self.__test__()

    def carve(self, coordinate: tuple[int, int], new: str = ' '):
        self._map[coordinate[1]][coordinate[0]] = new

    # Stage 1
    def carve_rooms(self):
        r"""Attempt to carve room randomly"""
        
        for attempt in range(room_placement_attempts):
            
            # Generate possible room
            room_w: int = rand.randint(room_minimum_size[0], room_maximum_size[0])
            room_h: int = rand.randint(room_minimum_size[1], room_maximum_size[1])
            room_x: int = rand.randint(1, level_size[0] - room_w - 1)  # Level width  - 1
            room_y: int = rand.randint(1, level_size[1] - room_h - 1)  # Level height - 1
    
            current_room = pg.rect.Rect(room_x, room_y, room_w, room_h)
    
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
                    if testing_room.colliderect(checking_room):
                        return False
                return True
    
            # If room is colliding (not allowed)
            if not check_room_collision():
                continue
            # Else: Room can be placed. 'pg.rect.Rect' used for 'colliderect' convenience

            self.__existing_rooms.append(current_room)
    
            # Carve room out of self._map
            for y in range(current_room.y, current_room.h + 1):
                for x in range(current_room.x, current_room.w + 1):
                    self.carve((x, y), 'r')
    

    # Stage 2
    def carve_hallways(self):
        r"""Carve the hallways"""
                        
        def check_neighbors(crd, origin, preorigin=None) -> list[tuple[int, int]] | None:
            r"""Return the value of """
                        
            # Section out a 3x3 area around the tile being checked
            rows = self._map[crd[1] - 1: crd[1] + 2]
            area = [row for row in rows[crd[0] - 1: crd[0] + 2]]
                        
            area[origin[1]][origin[0]] = 'X'
            if preorigin is not None:
                area[preorigin[1]][preorigin[0]] = 'X'

            # Find the coordinates of neighbors
            neighbors = []
            for y, y_row in enumerate(area):
                for x, x_row in enumerate(y_row):
                    if area[y][x] != 'X':
                         neighbors.append((x, y))

            # No neighbors
            if neighbors == []:
                return None

            # Return all neighbors
            return neighbors

        
            
            

    @classmethod
    def blank_map(cls) -> list[list[str]]:
        _map: list = []
        for y in range(level_size[1]):
            x_axis: list[str] = []
            for x in range(level_size[0]):
                x_axis.append('X')
            _map.append(x_axis)
        return _map


    def __test__(self) -> NoReturn:
        r"""Run to visualize the current level."""
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


def level_generator_function(screen):
    return Level()

level_generator_function(None)
