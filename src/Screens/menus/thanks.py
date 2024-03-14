# import pygame library under the abbreviation "pg" so I dont have to type "pygame"
import pygame as pg

# initialize pygame
pg.init()

# set screen and background values
background_color = (250, 250, 250)  # (178,99,27)

# different sized fonts
bigFont = pg.font.Font("Pixellettersfull-BnJ5.ttf", 100)
medFont = pg.font.Font("Pixellettersfull-BnJ5.ttf", 50)

# the text to be rendered and their colors
creditsTxt = bigFont.render("Thanks for playing!", (0, 0, 0))
exitText = medFont.render("Press any key to exit", (0, 0, 0))


def thanks_screen_function(screen):
    screen.fill(background_color)

    # write text to screen
    screen.blit(creditsTxt, (400 - (creditsTxt.get_width() / 2), 50))
    screen.blit(exitText, (400 - (exitText.get_width() / 2), 400))

    # update display
    pg.display.flip()

    while True:

        # gets all events
        for event in pg.event.get():
            # if the event type is the quit button at the top right corner
            if event.type == pg.QUIT:
                return True

            # if the event is a keypress
            if event.type == pg.KEYDOWN:
                return True
