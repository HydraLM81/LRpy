if __name__ != "__main__":
    exit(1)
    
import pygame as pg
from src.modules.Tile.Tile import Tile
from src.Screens.menus.mainMenu import main_menu_function

"""
---------- Labyrinth Recall ----------

16x16 pixel tiles

"""


pg.init()
screen = pg.display.set_mode((800, 450))
pg.display.set_caption("")

mapp = []

for y in range(50):
    temp = []
    for x in range(50):
        temp.append(Tile("blank", False, (x * 16, y * 16)))
    mapp.append(temp)

# Game Loop

main_menu_function(screen)

while True:

    for y, yaxis in enumerate(mapp):
        for x, tile in enumerate(yaxis):
            coords = (tile._rect.x, tile._rect.y)
            """tile._rect.x = coords[0] +
            tile."""

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
