#import pygame library
import pygame as pg
import os
from ...modules.Colors import Colors as c

# initialize pygame
pg.init()

# set background and screen
background_color = (250, 250, 250)  # (178,99,27)

font_path = os.getcwd() + "/src/screens/menus/Pixellettersfull-BnJ5.ttf"

# different sized fonts
bigFont = pg.font.Font(font_path, 100)
medFont = pg.font.Font(font_path, 50)
smallFont = pg.font.Font(font_path, 30)
VerySmallFont = pg.font.Font(font_path, 15)

# render the text
creditsTxt = bigFont.render("Credits", 0, c.BLACK)

lineOne = smallFont.render("Made by Noah Balderston and Mateo Rose for a school project.", 0, c.BLACK)
lineTwo = VerySmallFont.render("Design: Both of us", 0, c.BLACK)
lineThree = VerySmallFont.render("Textures and PyGame: Noah", 0, c.BLACK)
lineThreeOne = VerySmallFont.render("PyGame embedding: Noah", 0, c.BLACK)
lineFour = VerySmallFont.render("Backend: Both of us", 0, c.BLACK)
lineFive = VerySmallFont.render("Map generation: Mateo", 0, c.BLACK)
lineSix = VerySmallFont.render("Sound design: Mainly Mateo", 0, c.BLACK)
lineSeven = VerySmallFont.render("More nights spent: Noah 100%", 0, c.BLACK)

exitText = medFont.render("Press any key to exit", 0, c.BLACK)


def credits_menu_function(screen):
    r"""Shows credit screen. Waits for input -> return | exit."""
    # set background color
    screen.fill(background_color)

    # print the text to screen
    screen.blit(creditsTxt, (400 - (creditsTxt.get_width() / 2), 50))

    screen.blit(lineOne, (400 - lineOne.get_width() / 2), 155)
    screen.blit(lineTwo, (400 - lineTwo.get_width() / 2), 220)
    screen.blit(lineThree, (400 - lineThree.get_width() / 2), 240)
    screen.blit(lineThreeOne, (400 - lineThreeOne.get_width() / 2), 260)
    screen.blit(lineFour, (400 - lineFour.get_width() / 2), 280)
    screen.blit(lineFive, (400 - lineFive.get_width() / 2), 300)
    screen.blit(lineSix, (400 - lineSix.get_width() / 2), 320)
    screen.blit(lineSeven, (400 - lineSeven.get_width() / 2), 360)

    screen.blit(exitText, (400 - exitText.get_width() / 2), 400)

    # update display
    pg.display.flip()

    while True:

        # get all events
        for event in pg.event.get():
            # if the player closed the window
            if event.type == pg.QUIT:
                exit(0)

            # if the event was a keypress
            if event.type == pg.KEYDOWN:
                return True
