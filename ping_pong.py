from pygame import *
import time as tm

init()
font.init()
window = display.set_mode((600,600))
clock = time.Clock()
FPS = 60
window.fill((50,150,150))
game = True

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

class Player(GameSprite):
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y>10:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y<400:
            self.rect.y+= self.speed

    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y>10:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y<400:
            self.rect.y+= self.speed
class Ball(GameSprite):
    def __init__ (self, player_image,player_x,player_y,x_size,y_size,player_speed,player_speed_y):
        super().__init__(player_image,player_x,player_y,x_size,y_size,player_speed)
        self.speed_y = player_speed_y
    def update(self):
        self.rect.x+=self.speed
        self.rect.y+=self.speed_y
        if self.rect.x>=5 and self.rect.y>=5:
            self.rect.x+=self.speed
            self.rect.y+=self.speed_y
        if self.rect.x<=595 and self.rect.y<=595:
            self.rect.x-=self.speed
            self.rect.y-=self.speed_y
left_plaer = Player('roket.png',20,300,30,200,10)
right_plaer = Player('roket.png',560,300,30,200,10)
ball = Ball('Ball.png',300,300,30,30,5,5)

speed_x = 3
speed_y = 3

points_left = 0
points_right = 0

points_font = font.SysFont('Arial',30)
end_game_font =  font.SysFont('Arial',55)

finish = False

while game:
    left_points_text = points_font.render(str(points_left),1,(0,0,0))
    right_points_text = points_font.render(str(points_right),1,(0,0,0))
    left_win_text = end_game_font.render('Левый выйграл! ',1,(0,255,0))
    right_win_text=end_game_font.render('Правый выйграл! ',1,(0,255,0))
    left_lose_text = end_game_font.render('Левый проиграл ',1,(255,0,0))
    right_lose_text=end_game_font.render('Правый Проиграл ',1,(255,0,0))


    for e in event.get():
  
        if e.type == QUIT:
            game = False
    if finish ==False:
        window.fill((50,150,150))
        window.blit(left_points_text,(10,10))
        window.blit(right_points_text,(570,10))
        left_plaer.reset()
        right_plaer.reset()
        ball.reset()
        left_plaer.update_l()
        right_plaer.update_r()
        ball.update()
        if ball.rect.x>=600:
            ball.rect.x=300
            ball.rect.y=300
            points_left+=1
        if ball.rect.x<=5:
            ball.rect.x=300
            ball.rect.y=300
            points_right+=1
        if sprite.collide_rect(ball,left_plaer) or sprite.collide_rect(ball,right_plaer):
            ball.speed*=-1
            ball.speed_y *=1
            
        if ball.rect.y>=590:
            ball.speed_y*=-1
        if ball.rect.y<=5:
            #ball.speed*=-1
            ball.speed_y*=-1
        if points_left==5:
            window.blit(left_win_text,(200,300))
            window.blit(right_lose_text,(200,250))
            finish =True

        if points_right==5:
            window.blit(right_win_text,(200,300))
            window.blit(left_lose_text,(200,250))
            finish =True

    display.update()
    clock.tick(FPS)