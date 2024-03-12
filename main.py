if __name__ != "__main__":
    exit(1)
    
import pygame as pg

pg.init()
screen = pg.display.set_mode((600, 450))
pg.display.set_caption("")


class Tile(object):
    def __init__(self, name, collide, coords):
        self._name = name
        self._collide = collide
        self._coords = coords
        self._rect = pg.rect.Rect(coords, 16, 16)
        self._image =

    def draw(self, screen):
        pg.draw.rect(screen, (50, 50, 50), self._rect, 4)

mapp = []

for y in range(50):
    temp = []
    for x in range(50):
        temp.append(Tile("blank", False, (x, y)))
    mapp.append(temp)

# Game Loop

while True:
    # checking for event
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    keys = pg.key.get_pressed()

    if keys[pg.K_UP]:
        playerRotation = 0
        # if
        playerVelocityY = -1
    elif keys[pg.K_DOWN]:
        playerRotation = 180
        playerVelocityY = 1
    else:
        playerVelocityY = 0

    if keys[pg.K_RIGHT]:
        playerRotation = 270
        playerVelocityX = 1
    elif keys[pg.K_LEFT]:
        playerRotation = 90
        playerVelocityX = -1
    else:
        playerVelocityX = 0

    if playerVelocityX != 0 and playerVelocityY != 0:
        playerVelocityY *= .7071
        playerVelocityX *= .7071
