#Создай собственный Шутер!

from pygame import *
from random import randint
import time as tm
init()
font.init()
mixer.init()
kick = mixer.Sound('fire.ogg')
window = display.set_mode((700,500))
background = transform.scale(image.load('galaxy.jpg'),(700,500))
clock = time.Clock()
FPS = 60
mixer.music.load('space.ogg')
mixer.music.play()
mixer.music.set_volume(0.1)
kick.set_volume(0.1)
run = True

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,x_size,y_size,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(x_size,y_size))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Bullet(GameSprite):
    def update(self):
        self.rect.y+= self.speed
        if self.rect.y<=0:
            self.kill()
    

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x>5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x<650:
            self.rect.x+= self.speed
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx,self.rect.top,20,20,-15)
        bullets.add(bullet)
        
        
lost = 0
killed = 0
hearts = 3
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y+=self.speed
        if self.rect.y>= 500:
            self.rect.y = 0
            self.rect.x = randint(10,690)
            lost += 1
class Asteroid (GameSprite):
    def update(self):
        self.rect.y+=self.speed
        if self.rect.y>= 500:
            self.rect.y = 0
            self.rect.x = randint(10,690)
font1 =  font.SysFont('Arial',30)
font2 =  font.SysFont('Arial',55)


player = Player('rocket.png',350,400,50,70,10)
monsers = sprite.Group()
monster1 = Enemy('ufo.png',randint(10,640),10,65,65,randint(2,7))
monster2 = Enemy('ufo.png',randint(10,640),10,65,65,randint(2,7))
monster3 = Enemy('ufo.png',randint(10,640),10,65,65,randint(2,7))
monster4 = Enemy('ufo.png',randint(10,640),10,65,65,randint(2,7))
monster5 = Enemy('ufo.png',randint(10,640),10,65,65,randint(2,7))
asteroid1 = Asteroid('asteroid.png',randint(10,640),10,65,65,randint(2,7))
asteroid2 = Asteroid('asteroid.png',randint(10,640),10,65,65,randint(2,7))
asteroid3 = Asteroid('asteroid.png',randint(10,640),10,65,65,randint(2,7))

bullets = sprite.Group()
asteroids = sprite.Group()

monsers.add(monster1)
monsers.add(monster2)
monsers.add(monster3)
monsers.add(monster4)
monsers.add(monster5)
asteroids.add(asteroid1)
asteroids.add(asteroid2)
asteroids.add(asteroid3)
finish = False
player_collide = 0
num_fire = 0
rel_time = False
while run :
    text_lose = font1.render("Пропущено:"+str(lost),1,(255,255,255))
    text_kills = font1.render('Убито:'+str(killed),1,(255,255,255))
    text_win = font2.render('YOU WIN',1,(255,255,255))
    text_end_game = font2.render('YOU LOSE',1,(255,255,255))
    hearts_text = font2.render(str(hearts),1,(255,255,255))
    text_reload = font1.render('Wait, reload',1,(255,0,0))
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN and num_fire<5:
            if e.key == K_SPACE and num_fire< 5 and rel_time != True:
                player.fire()
                kick.play()
                num_fire+=1
            if num_fire>=5 and rel_time !=True:
                rel_time =True
                st_time = tm.time()

                
    window.blit(hearts_text,(670,10))  
    if finish == False:
        window.blit(background,(0,0))
        monsers.draw(window)
        asteroids.draw(window)
        window.blit(text_lose,(20,10))
        window.blit(text_kills,(20,40))
        monsers.update()
        asteroids.update()
        player.reset()
        player.update()
        bullets.draw(window)
        bullets.update()
        if rel_time == True:
            now_time = tm.time()
            if now_time - st_time <3:
                window.blit(text_reload,(330,450))
            else:
                num_fire = 0
                rel_time = False




        sprite_group_list = sprite.groupcollide(monsers,bullets,True,True)
        for i in sprite_group_list:
            killed+=1
            monster1= Enemy('ufo.png',randint(10,640),10,65,65,randint(2,7))
            monsers.add(monster1)
        sprite_player_monsters = sprite.spritecollide(player,monsers,False)
        for q in sprite_player_monsters:
            player_collide+=1
            hearts -=1
            q.kill()
            monster1= Enemy('ufo.png',randint(10,640),10,65,65,randint(2,7))
            monsers.add(monster1)
        sprite_player_asteroids = sprite.spritecollide(player,asteroids,False)
        for e in sprite_player_asteroids:
            player_collide+=1
            hearts-=1
            e.kill()
            asteroid1 = Asteroid('asteroid.png',randint(10,640),10,65,65,randint(2,7))
            asteroids.add(asteroid1)
           

    if killed >=10:
        finish= True
        window.blit(text_win,(300,250))
        mixer.music.stop()
    if lost>=30:
        finish = True
        window.blit(text_end_game,(260,230))
        mixer.music.stop()
        
    if player_collide>=3:
        hearts = 0
        finish = True
        window.blit(text_end_game,(260,230))
        mixer.music.stop()

    
    display.update()
    clock.tick(FPS)
    