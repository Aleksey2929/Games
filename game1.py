from pygame import *
from random import randint



'''
Подсказки:
1 - pygame.transform.rotate(sprite, "Угол") - поворот персонажа на угол
2 - pygame.transform.smoothscale() - масштабирует спрайт сглаживанием.



'''


class GameSprite(sprite.Sprite):
 #конструктор класса
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, speedx):
       #Вызываем конструктор класса (Sprite):
       sprite.Sprite.__init__(self)
       #каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
       self.speedx = speedx
       #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       # создаём выше квадрат для персонажа
       self.rect.x = player_x
       self.rect.y = player_y
 #метод, отрисовывающий героя на окне
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))


#класс главного игрока
class Player(GameSprite):
    #метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    #метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire1(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15, 0)
        bullets.add(bullet)
    def fire2(self):
        keys = key.get_pressed()
        if keys[K_SPACE]:
            bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15, randint(-5, 5))
            bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            self.speed = randint(2, 3)
            if self.speed > 7:
                self.speed -= 3


#класс спрайта-пули
class Bullet(GameSprite):
    # движение врага
    def update(self):
        self.rect.y += self.speed
        if self.speedx != 0 and self.speedx != 180:
            self.image = transform.rotate(self.image, self.speedx/2)
        self.rect.x += self.speedx
        # исчезает, если дойдет до края экрана
        if self.rect.y < 0:
            self.kill()
        if self.rect.y > 510:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        self.speed += 0.01
        if self.rect.y > 500:
            self.rect.y = -100
            self.rect.x = randint(80, win_width - 80)
        if self.speed < 20:
            self.speed = 4

class Money(GameSprite):
    def update(self):
        self.rect.y += self.speed
        self.rect.x += randint(-5, 5)
        if self.rect.y > 500:
            self.rect.y = -100
            self.rect.x = randint(80, win_width - 80)

font.init()
font = font.SysFont('Arial', 36)
destroy = font.render('Сбито: 0', True, (255, 255, 255))
lose = font.render('Пропущено: 0', True, (255, 255, 255))

#фоновая музыка
# mixer.init()
#!mixer.init()
#!sound = mixer.Sound('space.ogg')
# mixer.music.load('space.ogg')
# mixer.music.play()
# fire_sound = mixer.Sound('fire.ogg')
#нам нужны такие картинки:
img_back = "space.jpg" #фон игры
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
asteroid = Asteroid('asteroid.png', randint(100, 600), -300, 70, 70, 4, 0)
money = Money('money.png', randint(100, 600), -100, 40, 40, 4, 0)
ship = Player('rocket.png', 5, win_height - 100, 80, 90, 10, 0)
monsters = sprite.Group()
glasses = sprite.Group()
for i in range(5):
    enemy = Enemy('UFO.png', randint(80, win_width-80), -40, 80, 50, randint(2, 3), 0)
    monsters.add(enemy)
for i in range(2):
    glass = Enemy('shield.png', randint(80, win_width-80), -40, 50, 50, randint(2, 3), 0)
    glasses.add(glass)
bullets = sprite.Group()
lost_score = 0
destroy_score = 0
finish = False
run = True #флаг сбрасывается кнопкой закрытия окна
d = 0
#переменная счёта
time_fire = 0
while run:
    #событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if time_fire >= 1:
                    ship.fire1()
                    time_fire = 0
    if not finish:
        #обновляем фон
        window.blit(background,(0,0))
        ship.reset()
        money.reset()
        if destroy_score > 10:
            asteroid.reset()
        ship.update()
        money.update()
        time_fire += 0.2
        # ship.fire2()
        monsters.update()
        bullets.update()
        glasses.update()
        monsters.draw(window)
        bullets.draw(window)
        glasses.draw(window)
        if destroy_score > 10:
            asteroid.update()
        window.blit(destroy, (10, 10))
        window.blit(lose, (10, 56))
        for m in monsters:
            if m.rect.y == win_height:
                lost_score += 1
        colides = sprite.groupcollide(monsters, bullets, True, True)
        if sprite.collide_rect(ship, asteroid) or sprite.spritecollide(ship, monsters, False):
            gameOver = font.render('Game over', True, (186, 25, 13))
            window.blit(gameOver, (100, 100))
            finish = True
        collides = sprite.spritecollide(money, bullets, False)
        colides1 = sprite.spritecollide(asteroid, bullets, False)
        colides2 = sprite.spritecollide(asteroid, monsters, False)
        collidesotr = sprite.groupcollide(bullets, glasses, False, False)
        for a in collidesotr:
            a.speed = randint(8, 15)
            a.image = transform.rotate(a.image, 180)
            a.speedx = randint(-20, 20)
        for l in colides2:
            l.kill()
            enemy = Enemy('UFO.png', randint(80, win_width-80), -40, 80, 50, randint(2, 3),0)
            monsters.add(enemy)
            destroy_score += 1
        for n in colides1:
            n.kill()
        for g in collides:
            money.rect.y = -100
            money.rect.x = randint(100, 600)
            g.kill()
            destroy_score += 5
        for c in colides:
            enemy = Enemy('UFO.png', randint(80, win_width-80), -40, 80, 50, randint(2, 3),0)
            monsters.add(enemy)
            destroy_score += 1
        for u in sprite.spritecollide(money, monsters, False):
            u.speed = 5
            u.speedx = 5
        destroy = font.render(f'Очки: {destroy_score}', True, (255, 255, 255))
        lose = font.render(f'Пропущено: {lost_score}', True, (255, 255, 255))
        #!sound.play()
        display.update()
    #цикл срабатывает каждые 0.05 секунд
    time.delay(40)
