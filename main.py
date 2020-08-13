import pygame, sys, random

size = (1000,650) # size[0]: Row; size[1]: Column
bg_color = (255,255,255)
tick = 10

# Game constant number
MAXENERMY = 3
MAXSPEED = 3
MAXPLAYERBULLET = 40
PLAYERBULLETDELAY = 400
MAXENERMYBULLET = 7
ENERMYBULLETDELAY = 400000000#400

# Initialization
pygame.init()
screen = pygame.display.set_mode(size)
screen.fill(bg_color)

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./pic/player/plane_1.png')
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (100,50)
        self.mask = pygame.mask.from_surface(self.image)
        self.shooting_CD = 0

    def move(self):
        self.pos = pygame.mouse.get_pos()
        self.height = self.rect.bottom - self.rect.top
        self.weith = self.rect.right - self.rect.left
        self.pos = list(self.pos)
        self.pos[0] -= self.weith/2
        self.pos[1] -= self.height/2
        if self.pos[0]<0:
            self.pos[0]=0
        if self.pos[0]>size[0]:
            self.pos[0]=size[0]
        if self.pos[1]<0:
            self.pos[1]=0
        if self.pos[1]>size[1]:
            self.pos[1]=size[1]
        self.rect.left, self.rect.top = self.pos

    def get_pos(self):
        #return [self.rect.left, self.rect.top]
        return [(self.pos[0]+self.weith/2),(self.pos[1]+self.height/2)]

    def death(self):
        if pygame.sprite.spritecollide(self, enermies, False, pygame.sprite.collide_mask):
            return True
        if pygame.sprite.spritecollide(self, boss.boss, False, pygame.sprite.collide_mask) and boss.first_able == True and boss.first_death == False:
            return True
        return False

class Enermy_Bullet(pygame.sprite.Sprite):
    def __init__(self, location, t):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./pic/enermy/bullet_1.png')
        self.rect = self.image.get_rect()
        self.rect = location
        self.t = t
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect = self.rect.move(self.t)

class First(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./pic/First/plane.png')
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (500,100)
        self.t = [0,0]
        self.mask = pygame.mask.from_surface(self.image)
        self.blood = 1000
        self.direction_CD = 0
    
    def move(self):
        if self.direction_CD <= 0:
            self.t = [(random.randint(-1,1))*5,(random.randint(-1,1))*5]
            self.direction_CD = 100
        if self.rect.top <= 0 or self.rect.bottom >= 250:
            if self.rect.top <= 0 and self.t[1] < 0:
                self.t[1]*=-1
            elif self.rect.bottom >= 250 and self.t[1] > 0:
                self.t[1]*=-1
        if self.rect.left <= 0 or self.rect.right >= size[0]:
            if self.rect.left <= 0 and self.t[0] < 0:
                self.t[0]*=-1
            elif self.rect.right >= size[0] and self.t[0] > 0:
                self.t[0]*=-1
        self.rect = self.rect.move(self.t)
        self.direction_CD -= 1

    def animate(self):
        self.move()
        screen.blit(self.image, self.rect)
        if pygame.sprite.spritecollide(self, player_bullets, True, pygame.sprite.collide_mask):
            self.blood -= 100
    
    def __del__(self):
        print('First Die')

class Enermy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./pic/enermy/plane_1.png')
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (random.randint(1,size[0]-(self.rect.right-self.rect.left)),-100)
        self.t = [0,random.randint(1,MAXSPEED)]
        self.mask = pygame.mask.from_surface(self.image)
        self.shooting_CD = 0
        #self.bullets = pygame.sprite.Group()

    def move(self):
        self.rect = self.rect.move(self.t)

    def out(self):
        if self.rect.top > size[1]:
            return True
        return False

    def shooting(self):
        if self.shooting_CD <= 0:
            for i in range(0, MAXENERMYBULLET):
                enermy_bullets.add(Enermy_Bullet(self.rect, [random.randint(2,6)*(1 if(random.randint(0,1)) else -1),random.randint(2,6)*(1 if(random.randint(0,1)) else -1)]))
                #self.bullets.add(Enermy_Bullet(self.rect, [random.randint(2,6)*(1 if(random.randint(0,1)) else -1),random.randint(2,6)*(1 if(random.randint(0,1)) else -1)]))
            self.shooting_CD = ENERMYBULLETDELAY

class Player_Bullet(pygame.sprite.Sprite):
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./pic/player/bullet_1.png')
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.t = [0,-7]
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect = self.rect.move(self.t)

    def out(self):
        if self.rect.bottom < 0:
            return True
        return False

    def hit(self):
        if pygame.sprite.spritecollide(self, enermies, True, pygame.sprite.collide_mask):
            return True
        return False

class Boss:
    def __init__(self):
        self.first_able = False
        self.first_death = False
        self.first = First()
        self.boss = pygame.sprite.Group()
        self.boss.add(self.first)

boss = Boss()

# Game variable number
player_bullet_num = 0
enermy_num = 0
running = True
font = pygame.font.SysFont('arial', 40)
player = Player()
enermy_able = True

# Game lists
enermy_bullets = pygame.sprite.Group() # Enermy Bullets
enermies = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()

# Score
score = 0
miss = 0

def death():
    screen.fill((200,0,0))
    for enermy in enermies:
        screen.blit(enermy.image, enermy.rect)
        for enermy_bullet in enermy_bullets:
            screen.blit(enermy_bullet.image, enermy_bullet.rect)
    for player_bullet in player_bullets:
        screen.blit(player_bullet.image, player_bullet.rect)
    screen.blit(player.image, player.rect)
    losefont = font.render('You lose!', False, (255,40,40))
    screen.blit(losefont, (size[0]/2-90,size[1]/2-50))
    pygame.display.flip()

def animate():
    global enermy_num, player_bullet_num, score, miss, font, running, boss, enermy_able
    screen.fill(bg_color)
    # Enermy
    for enermy in enermies:
        enermy.move()
        enermy.shooting()
        enermy.shooting_CD -= 1
        screen.blit(enermy.image, enermy.rect)
        if pygame.sprite.spritecollide(player, enermy_bullets, True, pygame.sprite.collide_mask):
            death()
            running = False
        if enermy.out():
            enermies.remove(enermy)
            enermy_num -= 1
            miss += 1
    # Player Bullet
    for player_bullet in player_bullets:
        player_bullet.move()
        if player_bullet.hit():
            score += 1
            enermy_num -= (enermy_num - len(enermies))
            player_bullets.remove(player_bullet)
            player_bullet_num -= 1
            continue
        screen.blit(player_bullet.image, player_bullet.rect)
        if player_bullet.out():
            player_bullets.remove(player_bullet)
            player_bullet_num -= 1
    # Enermy Bullets
    for bullet in enermy_bullets:
            bullet.move()
            screen.blit(bullet.image, bullet.rect)
    # Player
    player.move()
    if player.death():
        death()
        running = False
    screen.blit(player.image, player.rect)
    # Boss First
    if boss.first_able == True and boss.first_death == False:
        boss.first.animate()
        if boss.first.blood <= 0:
            boss.first_able = False
            boss.first_death = True
            del boss.first
    # Other Generation
    if enermy_able == True:
        for i in range(enermy_num, MAXENERMY):
            enermies.add(Enermy())
            enermy_num += 1
    for i in range(player_bullet_num, MAXPLAYERBULLET):
        if player.shooting_CD <= 0:
            player_bullets.add(Player_Bullet(player.get_pos()))
            player_bullet_num += 1
            player.shooting_CD = PLAYERBULLETDELAY
        player.shooting_CD -= 1
    # Font
    hitting = font.render('Score: '+str(score),False,(0,233,233))
    screen.blit(hitting, (10,10))
    missing = font.render('Miss: '+str(miss),False,(233,233,0))
    screen.blit(missing, (10,45))
    pygame.display.flip()
    pygame.time.delay(tick)

def present():
    global enermy_able
    if score >= 3 and boss.first_death == False:
        boss.first_able = True
        enermy_able = False
    if boss.first_death == True:
        boss.first_able = False
        enermy_able = True

# Main loop
while running:
    animate()
    present()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()
sys.exit()