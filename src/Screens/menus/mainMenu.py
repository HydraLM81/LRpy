# import pygame library
import pygame as pg
import os
from ...modules.Colors import Colors as c
# init pygame
pg.init()

# setting background color and the actual display (so that it exists)
background_color = (150, 150, 150)

font_path = os.getcwd() + "/src/Screens/menus/Pixellettersfull-BnJ5.ttf"

# creating different sized fonts for things
fontSmall = pg.font.Font(font_path, 50)
fontBig = pg.font.Font(font_path, 100)
fontVerySmall = pg.font.Font(font_path, 25)

# creating text for the logo and buttons
t_text = fontBig.render("LABRYNTH RECALL", 0, c.BLACK)

p_text = fontSmall.render("Play", 0, c.BLACK)
c_text = fontSmall.render("Credits", 0, c.BLACK)
q_text = fontSmall.render("Quit", 0, c.BLACK)

# subtext
subText = fontVerySmall.render("Use arrow keys to select, enter/return to continue.", 0, c.BLACK)
subTextTwo = fontVerySmall.render("Made by Noah Balderston and Mateo Rose", 0, c.BLACK)

# the different button "boxes". I didn't want to compute these at run-time
playButton = pg.rect.Rect(300, 150, 200, 50)
creditButton = pg.rect.Rect(300, 250, 200, 50)
quitButton = pg.rect.Rect(300, 350, 200, 50)


def main_menu_function(screen):
    r"Shows the Main Menu and returns the selected option."

    # which box is highlighted
    box = 1

    while True:

        # detecting "events".
        for event in pg.event.get():
            # if the "X" button at top-right of window is clicked, then kill the program
            if event.type == pg.QUIT:
                exit(0)

            # if the event was a key press
            if event.type == pg.KEYDOWN:

                # if the key press was the enter or return key
                if event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER:

                    match box:
                        case 1:
                            print("Main Menu PLAY")
                            return "Main Menu PLAY"
                        case 2:
                            print("Main Menu CREDITS")
                            return "Main Menu CREDITS"
                        case 3:
                            print("Main Menu QUIT")
                            return "Main Menu QUIT"
                        case _:
                            print("Main Menu 'box' out of bounds on selection")
                            # just for error prevention
                            exit("Main Menu 'box' out of bounds on selection")

                # if the keypress was the up arrow, then move the "highlight" box up one
                elif event.key == pg.K_UP:
                    if box != 1:
                        box -= 1
                    else:
                        # change if there are more than 3 options
                        box = 3

                # if the keypress was the down arrow, move "highlight" box down one
                elif event.key == pg.K_DOWN:
                    if box != 3:
                        box += 1
                    else:
                        box = 1

            if event.type == pg.MOUSEMOTION:
                mouse_pos = pg.mouse.get_pos()
                if playButton.collidepoint(mouse_pos):
                    box = 1
                elif creditButton.collidepoint(mouse_pos):
                    box = 2
                elif quitButton.collidepoint(mouse_pos):
                    box = 3

            if event.type == pg.MOUSEBUTTONUP:
                mouse_pos = pg.mouse.get_pos()
                if playButton.collidepoint(mouse_pos):
                    print("Main Menu PLAY")
                    return "Main Menu PLAY"
                elif creditButton.collidepoint(mouse_pos):
                    print("Main Menu CREDITS")
                    return "Main Menu CREDITS"
                elif quitButton.collidepoint(mouse_pos):
                    print("Main Menu QUIT")
                    return "Main Menu QUIT"

        screen.fill(c.WHITE)

        # drawing the grey rectangles behind the button text (it's the "buttons")
        pg.draw.rect(screen, (100, 100, 100), playButton)
        pg.draw.rect(screen, (100, 100, 100), creditButton)
        pg.draw.rect(screen, (100, 100, 100), quitButton)

        # Labrynth Recall (the big text at the top of the screen)
        screen.blit(t_text, (400 - (t_text.get_width() / 2), 50))

        # the text on top of the buttons
        screen.blit(p_text, (400 - (p_text.get_width() / 2), 175 - (p_text.get_height() / 2)))
        screen.blit(c_text, (400 - (c_text.get_width() / 2), 275 - (c_text.get_height() / 2)))
        screen.blit(q_text, (400 - (q_text.get_width() / 2), 375 - (q_text.get_height() / 2)))

        # subtext
        screen.blit(subText, (5, 410))
        screen.blit(subTextTwo, (5, 428))

        # drawing the "highlight" box
        if box == 1:
            pg.draw.rect(screen, (25, 25, 25), (300, 150, 200, 50), 5)
        if box == 2:
            pg.draw.rect(screen, (25, 25, 25), (300, 250, 200, 50), 5)
        if box == 3:
            pg.draw.rect(screen, (25, 25, 25), (300, 350, 200, 50), 5)

        # update screen
        pg.display.flip()
