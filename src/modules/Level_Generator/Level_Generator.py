import pygame as pg
import os
import random
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
2: randomomized flood-fill
"""

"""   TODO
Flood-fill:
    Choose starting point
"""

### GENERATION PARAMETERS ###
level_size: tuple[int, int]  = (150, 150)  # (x, y)

# Room generation parameters
room_placement_attempts: int = 50        # Attempts to place rooms
room_min: tuple[int, int]    = (8, 8)    # Minimum room size (x, y)
room_max: tuple[int, int]    = (20, 20)  # Maximum room size (x, y)
room_doors: tuple[int, int]  = (1, 4)    # The min and max number of doors per room

##  generation dictionary  ##
# 'X'  = wall
# 'f'  = floor              (may be replaced with special tile)
# 'r'  = room
# 'h'  = hallway            (may be filled with 'X')
# 'ch' = connecting hallway (will be filled with 'h')
# 'c'  = connector          (door or open passage)
# 'd'  = door               (treated as an openable door)
# 'od' = open door          (take a guess)
# 'op' = open passage       (an open connection, like a door)

# Room colors (couldn't figure out how to import them)
_ROOMS: dict[int, pg.color.Color] = {
    0: pg.color.Color(255, 179, 198),
    1: pg.color.Color(255, 192, 159),
    2: pg.color.Color(255, 238, 147),
    3: pg.color.Color(252, 245, 199),
    4: pg.color.Color(160, 206, 217),
    5: pg.color.Color(173, 247, 182),
    6: pg.color.Color(128, 155, 206),
    7: pg.color.Color(149, 184, 209),
    8: pg.color.Color(184, 224, 210),
    9: pg.color.Color(214, 234, 223),
    10: pg.color.Color(234, 196, 213),
    11: pg.color.Color(232, 209, 197),
    12: pg.color.Color(126, 196, 207),
    13: pg.color.Color(82, 178, 207)
}

__areas = 0


def new_area():
    global __areas
    __areas += 1
    return __areas


class Room(object):
    def __init__(self, x, y, w, h):
        r"""Creates a new Room. Used to simplify \'Level.__test\'"""
        self.area = new_area()
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pg.rect.Rect(x, y, w, h)
        self.connections = 0

    def create_door(self):
        edges: list[tuple[int, int]] = []

        for x in range(self.x, self.x + self.w):
            edges.append((x + self.x, self.y))
            edges.append((x + self.x, self.y + self.h))
        for y in range(self.y, self.y + self.h):
            edges.append((self.x, y + self.y))
            edges.append((self.x + self.w, y + self.y))

        random.shuffle(edges)

        _map = self._map

        def check_doors(crd):
            right = (crd[0] + 1, crd[1])
            left = (crd[0] - 1, crd[1])
            up = (crd[0], crd[1] - 1)
            down = (crd[0], crd[1] + 1)

            # Horizontal:
            if _map[left[1]][left[0]] != 'X' and _map[right[1]][right[0]] != 'X':
                return True
            # Vertical
            if _map[up[1]][up[0]] != 'X' and _map[down[1]][down[0]] != 'X':
                return True
            return False

        door_num = random.randint(room_doors[0], room_doors[1])


class DispItem(object):
    def __init__(self, obj: pg.rect.Rect | Room, char: str):
        """Creates a new DispItem. Used to simplify \'Level.__test__\'"""
        self.obj: pg.rect.Rect | Room = obj
        self.char: str = char


class Level(object):
    def __init__(self):
        r"""Create new level object with set 'GENERATION PARAMETERS' (Level_Generator.py)"""
        self._map = Level.blank_map()

        # Carve rooms
        self.__existing_rooms: list[Room] = []
        self.__disp_list: list[DispItem] = []
        self.carve_rooms()

        self.carve_hallways()

        self.__test__(self._map)

    def carve(self, coordinate: tuple[int, int], new: str, disp_list: bool):
        self._map[coordinate[1]][coordinate[0]] = new
        if disp_list:
            self.__disp_list.append(DispItem(pg.rect.Rect(coordinate[1],
                                                          coordinate[0],
                                                          1, 1),
                                             new))

    # Stage 1
    def carve_rooms(self):
        r"""Attempt to carve room randomomly"""

        for attempt in range(room_placement_attempts):
            # Generate possible room (odd only, makes maze look better)
            room_w: int = (random.randint(room_min[0] // 2, room_max[0] // 2) * 2) + 1
            room_h: int = (random.randint(room_min[1] // 2, room_max[1] // 2) * 2) + 1
            room_x: int = (random.randint(1, (level_size[0] - room_w - 1) // 2) * 2) - 1
            room_y: int = (random.randint(1, (level_size[1] - room_h - 1) // 2) * 2) - 1

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
                for y in range(current_room.y, current_room.h + current_room.y):
                    for x in range(current_room.x, current_room.w + current_room.x):
                        self.carve((y, x), 'r', False)

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

            # If all the tiles around it are 'X' (carvable), return True
            area[1][1] = 'X'
            if area[0].count('X') == area[1].count('X') == area[2].count('X') == 3:
                return True

            return False

        # Return a list of adjacent coordinates. Allows for random.shuffle()
        def _crdlist(crd):
            return [((crd[0] + 2, crd[1]), (crd[0] + 1, crd[1])),
                    ((crd[0] - 2, crd[1]), (crd[0] - 1, crd[1])),
                    ((crd[0], crd[1] - 2), (crd[0], crd[1] - 1)),
                    ((crd[0], crd[1] + 2), (crd[0], crd[1] + 1))]

        # A list of all cells that can be branched from
        alive_cells: list[tuple[tuple[int, int], tuple[int, int]]] = []  # (crd, came_from)
        # The starting point for the maze (could be varied, I'm lazy)
        alive_cells.append(((1, 1), (1, 1)))

        ctime = time.time()  # Time how long generation takes

        print("Starting loop")

        while len(alive_cells) > 0:
            # Print the length of the cell list
            print(f"Len cells: {len(alive_cells)}")

            # Define some extra variables for ease of reading
            _current_cell = alive_cells[-1]
            current_cell = _current_cell[0]  # The current cell
            last_cell = _current_cell[1]  # The "in-between" cell where 'current' came from

            if self._map[current_cell[1]][current_cell[0]] == 'X':
                self.carve(current_cell, 'ch', True)

            crdlist = _crdlist(current_cell)

            # The "random" part of random DFS
            random.shuffle(crdlist)

            # Check the neighboring coordinates. If carvable, then go there.
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

            # No carvable neighbors, current_cell is dead, remove from list.
            else:
                self.carve(current_cell, 'h', True)
                self.carve(last_cell, 'h', True)
                alive_cells.pop(-1)

        # Print some fun statistic, because why not...
        print("Loop done")
        print(f"Time taken in loop: {time.time() - ctime}")
        print(f"disp_list length after hallways: {len(self.__disp_list)}")

    def carve_connections(self):
        r"""Carve the connections between passages"""
        c_list: list[tuple[int, int]] = []

        def check_connection(crd: tuple[int, int]):
            r"""Check if \'crd\' should be marked \'c\'"""

            """_map = self._map
            right  = (crd[0] + 1, crd[1])
            left   = (crd[0] - 1, crd[1])
            up     = (crd[0], crd[1] - 1)
            down   = (crd[0], crd[1] + 1)

            # Horizontal:
            if _map[right[1]][right[0]] != _map[left[1]][left[0]] 
                and _map[right[1]][right[0]] != 'X':
                    c_list.append(crd)
            """
            rows = self._map[1:-1]
            _map = [row[1:-1] for row in rows]
            for y, y_axis in enumerate(_map):
                for x, tile in enumerate(y_axis):
                    if tile == 'X':
                        # Horizontal
                        lr = (_map[y][x - 1], _map[y][x + 1])
                        if lr[0] != lr[1] and lr[0] != 'X' and lr[1] != 'X':
                            c_list.append((x, y))
                        ud = (_map[y - 1][x], _map[y + 1][x])
                        if ud[0] != ud[1] and ud[0] != 'X' and ud[1] != 'X':
                            c_list.append((x, y))

    # Creates a blank map for 'self._map'
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

        # Display loop
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()

            screen.fill((0, 0, 0))

            # For each item that was added to __disp_list. Increments to look fancy
            for _disp_item in self.__disp_list[:next_disp_item]:

                draw_color = (100, 100, 100)

                # If '_disp_item' is a PyGame Rect, treat it as such
                if isinstance(_disp_item.obj, pg.rect.Rect):
                    # Check individual colors (won't differentiate between separate hallways)
                    match _disp_item.char:
                        case 'X':
                            draw_color = (0, 0, 0)
                        case "ch":
                            draw_color = (0, 200, 240)
                        case 'h':
                            draw_color = (100, 0, 240)
                        case _:
                            print(f"Uncaught: \'{_disp_item.char}\'")
                            draw_color = (255, 0, 255)

                # If 'disp_item' is a 'Room' object (different from Rect)
                elif isinstance(_disp_item.obj, Room):
                    draw_color = _ROOMS[_disp_item.obj.area % len(_ROOMS)]

                disp_item = pg.rect.Rect(_disp_item.obj.x * 3,
                                         _disp_item.obj.y * 3,
                                         _disp_item.obj.w * 3,
                                         _disp_item.obj.h * 3)

                pg.draw.rect(screen, draw_color, disp_item)

            next_disp_item += 100

            pg.display.update()


def level_generator_function():
    return Level()


level_generator_function()
