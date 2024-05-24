import pygame as pg
import os
import random
import time

pg.init()
screen = pg.display.set_mode((600, 600))
pg.display.set_caption("")
clock = pg.time.Clock()

"""
Inspiration taken from Bob Nystrom (https://journal.stuffwithstuff.com/2014/12/21/rooms-and-mazes/)
I tried to follow their ideas, but with my own twists and parameters for things. (Thanks Bob)
"""

##  Stages of generation  ##
"""
1: Place rooms
2: randomized flood-fill
"""

### GENERATION PARAMETERS ###
level_size: tuple[int, int] = (100, 100)  # (x, y)

# Room generation parameters
room_placement_attempts: int = 150    # Attempts to place rooms
room_min: tuple[int, int] = (5, 5)    # Minimum room size (x, y)
room_max: tuple[int, int] = (15, 15)  # Maximum room size (x, y)
room_doors: tuple[int, int] = (1, 3)  # The min and max number of doors per room

# Other parameters
hallway_sparsity: float = .30         # Percent of hallways to leave after introducing sparsity
hallway_smoothness: float = .30       # Percent of hallways to be "smoothed" after sparsity


##  generation dictionary  ##
# 'SP' = starting point     (spawn point for the player
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


class MapTile(object):
    def __init__(self, char='X', area=-1):
        self.char = char
        self.area = area


class Room(object):
    def __init__(self, x, y, w, h):
        r"""Creates a new Room. Mainly used to simplify \'Level.__test\'"""
        self.area = new_area()
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pg.rect.Rect(x, y, w, h)
        self.connections = 0
        self.max_connections = random.randint(room_doors[0], room_doors[1])

    def create_door(self, _map, _room_list):
        r"""Create doors between rooms/hallways (_map:Level._map)"""
        edges: list[tuple[int, int]] = []

        # Find the edges of rooms (NOT (y, x)!)
        for x in range(self.x, self.x + self.w):
            # Top
            if _map[self.y - 1][x].char == 'X':
                edges.append((x, self.y - 1))
            else: self.connections += 1
            # Bottom
            if _map[self.y + self.h][x].char == 'X':
                edges.append((x, self.y + self.h))
            else: self.connections += 1

        for y in range(self.y, self.y + self.h):
            # Left
            if _map[y][self.x - 1].char == 'X':
                edges.append((self.x - 1, y))
            else: self.connections += 1
            # Right
            if _map[y][self.x + self.w].char == 'X':
                edges.append((self.x + self.w, y))
            else: self.connections += 1

        random.shuffle(edges)

        def check_doors(crd):

            print(crd)
            right = _map[crd[1]][crd[0] + 1].char
            left = _map[crd[1]][crd[0] - 1].char
            up = _map[crd[1] - 1][crd[0]].char
            down = _map[crd[1] + 1][crd[0]].char

            r = (crd[0] + 1, crd[1])
            l = (crd[0] - 1, crd[1])
            u = (crd[0], crd[1] - 1)
            d = (crd[0], crd[1] + 1)

            ret = False

            if [right, left, up, down].count('X') == 2:
                ret = True

            def room_grabber_ting(crd_: tuple[int, int]):
                for room in _room_list:
                    if room.check_coordinate(crd_):
                        return room

            grabbed_room: Room | None = None

            if right == 'r' and self.x + self.w < r[0]:
                grabbed_room = room_grabber_ting(r)
                if grabbed_room.connections >= grabbed_room.max_connections:
                    ret = False

            if left == 'r' and self.x > l[0]:
                grabbed_room = room_grabber_ting(l)
                if grabbed_room.connections >= grabbed_room.max_connections:
                    ret = False

            if up == 'r' and self.y > u[1]:
                grabbed_room = room_grabber_ting(u)
                if grabbed_room.connections >= grabbed_room.max_connections:
                    ret = False

            if down == 'r' and self.y + self.h < d[1]:
                grabbed_room = room_grabber_ting(d)
                if grabbed_room.connections >= grabbed_room.max_connections:
                    ret = False

            return ret, grabbed_room

        # Send the coordinates to be carved as connections
        carve_doors: list[tuple[int, int]] = []
        while self.connections < self.max_connections and len(edges) > 0:
            checked = check_doors(edges[0])
            if checked[0]:
                if isinstance(checked[1], Room):
                    checked[1].connections += 1
                carve_doors.append(edges[0])
                self.connections += 1
            edges.pop(0)
        return carve_doors

    def check_coordinate(self, crd):
        r"""Check if /'crd/' is inside the room"""
        return (self.x <= crd[0] < self.x + self.w) and (self.y <= crd[1] < self.y + self.h)


class DispItem(object):
    def __init__(self, obj: pg.rect.Rect | Room, char: str):
        """Creates a new DispItem. Used to simplify \'Level.__test__\'"""
        self.obj: pg.rect.Rect | Room = obj
        self.char: str = char


class Level(object):
    def __init__(self):
        r"""Create new level object with set 'GENERATION PARAMETERS' (Level_Generator.py)"""
        self._map: list[list[MapTile]] = Level.blank_map()

        # Carve rooms
        self.__existing_rooms: list[Room] = []
        self.__disp_list: list[DispItem] = []
        self.carve_rooms()

        self.carve_hallways()

        self.carve_connections()

        self.sparsify()
        #self.smoothify()

        self.__test__()

    def carve(self, coordinate: tuple[int, int], new: str, disp_list: bool, area=None):
        r"""COORDINATE IS (x, y) except for rooms? idfk anymore"""
        self._map[coordinate[1]][coordinate[0]].char = new

        if area is not None:
            self._map[coordinate[1]][coordinate[0]].area = area

        if disp_list:
            self.__disp_list.append(DispItem(pg.rect.Rect(coordinate[0],  # ISTG FOR >7 HOURS I SWAPPED THESE
                                                          coordinate[1],  # WHY DO I DO THIS TO MYSELF
                                                          1, 1),
                                             new))

    # Stage 1
    def carve_rooms(self):
        r"""Attempt to carve room randomly"""

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

                self.__existing_rooms.append(current_room)
                self.__disp_list.append(DispItem(current_room, 'r'))

                # Carve room out of self._map
                for y in range(current_room.y, current_room.h + current_room.y):
                    for x in range(current_room.x, current_room.w + current_room.x):
                        self.carve((x, y), 'r', False, area=1)

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
            _area = [row[crd[0] - 1: crd[0] + 2] for row in rows]
            area = [[tile.char for tile in row] for row in _area]

            # If all the surrounding tiles are 'X' (carvable), return True
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

        # Create a starting point for the maze (must be carveable)
        __done = False
        for y in range(1, len(self._map), 2):
            if __done: break
            for x in range(1, len(self._map[0]), 2):
                if self._map[y][x].char == 'X':
                    alive_cells.append(((x, y), (x, y)))
                    self._map[y][x].char = 'S'
                    __done = True
                    break

        ctime = time.time()  # Time how long generation takes

        print("Starting loop")

        while len(alive_cells) > 0:
            # Print the length of the cell list
            #print(f"Len cells: {len(alive_cells)}")

            # Define some extra variables for ease of reading
            _current_cell = alive_cells[-1]
            current_cell = _current_cell[0]  # The current cell
            last_cell = _current_cell[1]  # The "in-between" cell where 'current' came from

            if self._map[current_cell[1]][current_cell[0]].char == 'X':
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

    # Stage 3
    def carve_connections(self):
        r"""Carve the connections between passages"""

        # First run from the rooms
        _connections: list[list[tuple[int, int]]] = []
        for room in self.__existing_rooms:
            for connections in room.create_door(self._map, self.__existing_rooms):
                self.carve(connections,
                           'd' if random.randint(0, 1) == 0 else 'h',
                           True)

        print('done done')

    # Stage 4
    def sparsify(self):
        r""""""
        def count_hallways():
            r"""Count the number of hallway tiles"""
            _count = 0
            for _row in self._map:
                for _tile in _row:
                    if _tile.char == 'h':
                        _count += 1
            return _count

        # The current number of hallways
        cut_count = 0

        # Number of hallways left after cutting
        cutting_count = count_hallways() * hallway_sparsity

        # List for cutting (similar to 'alive_cells' in hallway generation)
        cutting_list: list[tuple[int, int]] = []

        def surrounding_tiles(crd: tuple[int, int]):
            right = self._map[crd[1]][crd[0] + 1].char
            left = self._map[crd[1]][crd[0] - 1].char
            up = self._map[crd[1] - 1][crd[0]].char
            down = self._map[crd[1] + 1][crd[0]].char
            return [right, left, up, down]

        def recheck_list():
            for y, row in enumerate(self._map):
                for x, tile in enumerate(row):
                    if tile.char == 'h' and surrounding_tiles((x, y)).count('X') == 3:
                        cutting_list.append((x, y))

        recheck_list()

        random.shuffle(cutting_list)
        print(len(cutting_list))
        while cut_count < cutting_count and len(cutting_list) > 0:
            current_crd = cutting_list[0]
            cutting_list.pop(0)

            self.carve(current_crd, 'X', True)

            cut_count += 1

            if len(cutting_list) == 0:
                recheck_list()

        print(f"len{len(cutting_list)} {cutting_count} {cut_count}")

    # Creates a blank map for 'self._map'
    @classmethod
    def blank_map(cls) -> list[list[MapTile]]:
        _map: list = []
        for y in range(level_size[1]):
            x_axis: list[MapTile] = []
            for x in range(level_size[0]):
                x_axis.append(MapTile('X'))
            _map.append(x_axis)
        return _map

    def __test__(self):
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
                            #print(f"Uncaught: \'{_disp_item.char}\'")
                            draw_color = (255, 0, 255)

                # If 'disp_item' is a 'Room' object (different from Rect)
                elif isinstance(_disp_item.obj, Room):
                    draw_color = _ROOMS[_disp_item.obj.area % len(_ROOMS)]

                disp_item = pg.rect.Rect(_disp_item.obj.x * 6,
                                         _disp_item.obj.y * 6,
                                         _disp_item.obj.w * 6,
                                         _disp_item.obj.h * 6)

                pg.draw.rect(screen, draw_color, disp_item)

            clock.tick(30)

            next_disp_item += 10000

            pg.display.update()


def level_generator_function():
    return Level()


level_generator_function()
