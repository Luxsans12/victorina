from pygame import *
from random import *

destroed = 0
live = 0

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play(-1)

fire = mixer.Sound("fire.ogg")

razreshenie = 1200, 628
clock = time.Clock()
FPS = 60

window = display.set_mode((razreshenie))
game = True
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (razreshenie))


class GameSprite(sprite.Sprite):
    def __init__(self, image_p, speed, rect_x, rect_y, width, height):
        super().__init__()
        self.image = transform.scale(image.load(image_p), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = rect_x
        self.rect.y = rect_y
        self.width = width
        self.height = height

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if key_pressed[K_RIGHT] and self.rect.x < 1200 - 60 - 5:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("bullet.png", -5, self.rect.centerx - 7, self.rect.top, 15, 20)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        global live
        self.rect.y += self.speed
        if self.rect.y > 628:
            live += 1
            self.rect.y = 0
            self.rect.x = randint(0, 1200 - 65)


bullets = sprite.Group()
monsters = sprite.Group()

enemy = Enemy("ufo.png", randint(5, 9), randint(0, 1200 - 65), 0, 65, 65)
enemy2 = Enemy("ufo.png", randint(5, 9), randint(0, 1200 - 65), 0, 65, 65)
enemy3 = Enemy("ufo.png", randint(5, 10), randint(0, 1200 - 65), 0, 65, 65)
enemy4 = Enemy("ufo.png", randint(5, 12), randint(0, 1200 - 65), 0, 65, 65)
enemy5 = Enemy("ufo.png", 5, randint(0, 1200 - 65), 0, 65, 65)
enemy6 = Enemy("ufo.png", randint(9, 10), randint(0, 1200 - 65), 0, 65, 65)
enemy7 = Enemy("ufo.png", randint(5, 8), randint(0, 1200 - 65), 0, 65, 65)

monsters.add(enemy)
monsters.add(enemy2)
monsters.add(enemy3)
monsters.add(enemy4)
monsters.add(enemy5)
monsters.add(enemy6)
monsters.add(enemy7)

font.init()
font1 = font.SysFont('Arial', 40)
font2 = font.SysFont('Arial', 20)
win = font1.render('you win', True, (0, 255, 0))
lose = font1.render('you lose', True, (255, 0, 0))

rocket = Player("rocket.png", 10, 400, 500, 60, 80)

finish = False

while game:
    if finish != True:
        window.blit(background, (0, 0))
        rocket.reset()
        rocket.update()
        monsters.draw(window)
        monsters.update()

        bullets.draw(window)
        bullets.update()

        if sprite.spritecollide(rocket, monsters, False):
            window.blit(lose, (500, 500))
            finish = True

        list_killed = sprite.groupcollide(bullets, monsters, True, True)
        for e in list_killed:
            destroed += 1
            enemy = Enemy("ufo.png", randint(5, 9), randint(0, 1200 - 65), 0, 65, 65)
            monsters.add(enemy)

        if destroed == 20:
            window.blit(win, (500, 500))
            finish = True

        if live == 30:
            window.blit(lose, (500, 500))
            finish = True

        text_destroyed = font2.render('РЕЗНЯ: ' + str(destroed), True, (255, 255, 255))
        text_live = font2.render('Как ты мог пропустить??? ' + str(live), True, (255, 255, 255))

        window.blit(text_destroyed, (50, 50))
        window.blit(text_live, (50, 100))

    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()

    display.update()
    clock.tick(FPS)
