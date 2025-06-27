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
    def __init__(self, player_image, player_x, player_y, player_speed, delay = 500, miss_score = 0, score = 0):
        super().__init__()
        self.image = transform.scale(image.load(resource_path(player_image)), (100, 100))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.miss_score = 0
        self.score = 0
        self.delay = 500

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
        if self.rect.y >= screen_height:
            orda.remove(i)
            enemy = Enemy('ufo.png', randint(150, screen_width - 150), 0, randint(2, 4))
            orda.append(enemy)
            self.miss_score += 1

class Bullet(GameSprite):
    def move(self):
        self.rect.y -= self.speed
        for i in orda:
            if sprite.collide_rect(bullet, i):
                orda.remove(i)
                enemy = Enemy('ufo.png', randint(150, screen_width - 150), 0, randint(2, 4))
                orda.append(enemy)
                magazin.remove(bullet)
                self.score += 1

class Upgrade(GameSprite):
    def move(self):
        if self.rect.y < screen_height:
            self.rect.y += self.speed
        if self.rect.y >= screen_height:
            up_list.remove(c)

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

FPS = 60

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire = mixer.Sound('fire.ogg')

seredina_x = screen_height / 2
seredina_y = screen_width / 2
y = screen_height - 100

player = Player('rocket.png',seredina_x,y,10)
orda = []
magazin = []
up_list = []

for _ in range(5):
    enemy = Enemy('ufo.png', randint(150,screen_width-150),0,randint(2,4))
    orda.append(enemy)

game = True

last_shot = 0
delay = 500
miss = 0
score = 0
kd_spawn = 10
finish = False

while game == True:
    window.blit(background, (0, 0))

    if finish == False:
        player.reset()
        keys_pressed = key.get_pressed()

        current_time = time.get_ticks()
        if keys_pressed[K_SPACE] and current_time - last_shot > delay or len(magazin) > 2:
            bullet = Bullet('bullet.png', player.rect.x, player.rect.y, 20)
            magazin.append(bullet)
            last_shot = current_time
            fire.play()

        player.move()

        for i in orda:
            i.move()
            i.reset()
            miss += i.miss_score
            b = font1.render(
                'Пропущено: ' + str(miss), True, (255, 255, 255)
            )
            window.blit(b, (0, 50))

        for bullet in magazin:
            bullet.move()
            bullet.reset()
            if bullet.rect.y <= 0:
                magazin.remove(bullet)
            score += bullet.score

        if score % 10 == 0 and score != 0 and len(up_list) == 0:
            upgrade = Upgrade('up-arrow.png', randint(150, screen_width - 150), 0, 3)
            up_list.append(upgrade)

        if len(up_list) != 0:
            for c in up_list:
                c.move()
                c.reset()
                if sprite.collide_rect(player,c):
                    if delay >= 200:
                        delay -= 50
                    up_list.remove(c)


        a = font1.render(
            "Счёт: " + str(score), True, (255, 255, 255)
        )
        window.blit(a, (0, 0))

    if score == 50:
        finish = True
        win = font1.render(
            'Ты победил', True, (0, 255,155)
        )
        window.blit(win, (seredina_x, seredina_y))

    if miss == 5:
        finish = True
        lose = font1.render(
            'Ты проиграл', True, (255, 255, 255)
        )
        window.blit(lose,(seredina_x,seredina_y))

    for i in orda:
        if sprite.collide_rect(player, i):
            finish = True
            lose = font1.render(
                'Ты проиграл', True, (255, 255, 255)
            )
            window.blit(lose, (seredina_x, seredina_y))

    for e in event.get():
        if e.type == QUIT:
            game = False

    display.update()
    clock.tick(FPS)
