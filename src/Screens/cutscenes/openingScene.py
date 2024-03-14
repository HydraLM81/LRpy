#import pygame library
import pygame as pg
import os
#import moviepy for video playback
from moviepy.editor import *

#initialize pygame
pg.init()

#set screen
(screenWidth, screenHeight) = (800, 450)
screen = pg.display.set_mode((screenWidth, screenHeight))

#i think this is here just to prevent things from moving too fast
clock=pg.time.Clock()

#sets "application" name
pg.display.set_caption('Labrynth Recall (opening cutscene)')

#import the video
opening_scene = VideoFileClip(os.getcwd() + "/src/Screens/cutscenes/videos/soap.mp4")
#edit it to be better sized/timed
opening_scene = opening_scene.resize((800, 450))
opening_scene = opening_scene.fx(vfx.speedx, 0.465)
opening_scene = opening_scene.subclip(0, 2)

def opening_cutscene_video():
    r"""Plays the opening cutscene video."""
    #shows the video
    opening_scene.preview()
    return True
