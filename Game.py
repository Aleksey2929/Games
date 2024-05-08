from pygame import *
from random import *


class GameSprite(sprite.Sprite):
    def __init__(my, input_image, size1, size2, x, y, speed):
        sprite.Sprite.__init__(my)
        my.size1 = size1
        my.size2 = size2
        my.image = transform.scale(image.load(input_image), (my.size1, my.size2))
        my.rect = my.image.get_rect()
        my.rect.x = x
        my.rect.y = y
        my.speed = speed
        # my.radius = size1/2

    def reset(my, window):
        window.blit(my.image, (my.rect.x, my.rect.y))


class Wall(GameSprite):
    def wall_update(my, name):
        keys = key.get_pressed()
        if keys[K_LEFT] or keys[K_a]:
            my.rect.x -= my.speed
            name.image = transform.rotate(90)
        if keys[K_RIGHT] or keys[K_d]:
            my.rect.x += my.speed


class Player(GameSprite):
    def go(my):
        my.rect.y += my.speed / 1.5
        my.speed += 0.1


walls = sprite.Group()
listx = [0, 400, 600, -400, 900, 1400, 1200, -200, -800, -1100, -1400, -1600, -1000, 1700, 2000]
for i in range(15):
    a = choice(listx)
    wall = Wall('downs.png', randint(100, 300), 50, a, randint(100, 450), 8)
    listx.remove(a)
    walls.add(wall)

ball = Player('red_ball.png', 50, 50, 400, 0, 20)

w = 700
h = 500
background = transform.scale(image.load('space.jpg'), (w, h))
win = display.set_mode((w, h))
display.set_caption('Red ball')
# win.blit(background, (0, 0))
# display.flip()
jump = False
finish = False
run = True
while run:
    for events in event.get():
        if events.type == QUIT:
            run = False
    if not finish:
        win.blit(background, (0, 0))
        ball.reset(win)
        keys = key.get_pressed()
        if not sprite.spritecollide(ball, walls, False):
            if jump:
                ball.rect.y -= ball.speed
                ball.speed -= 0.7
            else:
                ball.go()
                ball.speed = 20
        elif sprite.spritecollide(ball, walls, False):
            for c in walls:
                if ball.rect.x - c.rect.x >= -50 and ball.rect.x - c.rect.x <= c.size1:
                    ball.rect.y = c.rect.y - 50
            if keys[K_UP] and not jump:
                jump = True
                ball.rect.y -= 1
                ball.speed = 12.5
            elif jump == True:
                ball.speed = 20
                jump = False

        for s in walls:
            g = key.get_pressed()
            if g[K_LEFT] or g[K_a]:
                s.rect.x += s.speed
            if g[K_RIGHT] or g[K_d]:
                s.rect.x -= s.speed

        if ball.rect.y >= 750:
            finish = True

        walls.draw(win)

        display.update()
    time.delay(40)