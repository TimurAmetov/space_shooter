from pygame import *
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(resource_path(player_image)), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def move(self):
        keys_pressed = key.get_pressed()

        if keys_pressed[K_RIGHT] and self.rect.x < screen_width:
            self.rect.x += self.speed
            self.image = transform.scale(image.load(resource_path('rocket.png')), (60, 60))
        if keys_pressed[K_LEFT] and self.rect.x > screen_width:
            self.image = transform.scale(image.load(resource_path('rocket.png')), (60, 60))
            self.rect.x -= self.speed

class Enemy(GameSprite):
    def move(self):
        if self.rect.y < screen_height:
            self.rect.y -= self.speed
            self.image = transform.scale(image.load(resource_path('cyborgL.png')), (60, 60))

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
#mixer.music.play()

seredina = screen_width / 2

player = Player('rocket.png',screen_height,seredina,10)

game = True

while game == True:
    window.blit(background, (0, 0))
    player.reset()
    player.move()

    display.update()
    clock.tick(FPS)