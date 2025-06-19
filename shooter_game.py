from itertools import count

from pygame import *
import sys
import os
from random import randint

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(resource_path(player_image)), (100, 100))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def move(self):
        keys_pressed = key.get_pressed()

        if keys_pressed[K_RIGHT] and self.rect.x + self.rect.width < screen_width:
            self.rect.x += self.speed
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed

class Enemy(GameSprite):
    def move(self):
        if self.rect.y < screen_height:
            self.rect.y += self.speed

font.init()
font1 = font.Font(None, 70)

window = display.set_mode((0, 0), FULLSCREEN)
display.set_caption('Космос')

screen_width, screen_height = window.get_size()

background = transform.scale(
    image.load(resource_path('galaxy.jpg')),
    (screen_width, screen_height)
)

clock = time.Clock()

win = font1.render(
                'YOU WIN!', True, (255, 215, 0)
            )

lose = font1.render(
                    'YOU LOSE!', True, (255, 0, 0)
                )

number = 0
score = font1.render(
    "Счёт: " + str(number), True, (255, 255, 255)
)

a = 0
miss = font1.render(
    'Пропущено: '+str(a),True, (255, 255, 255)
)

FPS = 60

mixer.init()
mixer.music.load('space.ogg')
#mixer.music.play()

seredina = screen_height / 2
y = screen_height - 100

player = Player('rocket.png',seredina,y,10)
enemy1 = Enemy('ufo.png', randint(150,screen_width-150),100,randint(2,4))
enemy2 = Enemy('ufo.png', randint(150,screen_width-150),100,randint(2,4))
enemy3 = Enemy('ufo.png', randint(150,screen_width-150),100,randint(2,4))
enemy4 = Enemy('ufo.png', randint(150,screen_width-150),100,randint(2,4))
enemy5 = Enemy('ufo.png', randint(150,screen_width-150),100,randint(2,4))

orda = [enemy1,enemy5,enemy4,enemy2,enemy3]

game = True

while game == True:
    window.blit(background, (0, 0))
    player.reset()
    window.blit(score,(0,0))
    window.blit(miss, (0,50))

    for i in orda:
        i.reset()

    for e in event.get():
        if e.type == QUIT:
            game = False

    player.move()

    for i in orda:
        i.move()

    display.update()
    clock.tick(FPS)