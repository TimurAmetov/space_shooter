from math import gamma

from pygame import *

import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

font.init()
font = font.Font(None, 70)

window = display.set_mode((0, 0), FULLSCREEN)
display.set_caption('Космос')

screen_width, screen_height = window.get_size()

background = transform.scale(
    image.load(resource_path('galaxy.jpg')),
    (screen_width, screen_height)
)

clock = time.Clock()

win = font.render(
                'YOU WIN!', True, (255, 215, 0)
            )

lose = font.render(
                    'YOU LOSE!', True, (255, 0, 0)
                )

FPS = 60

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

game = True

while game == True:
    display.update()
    clock.tick(FPS)