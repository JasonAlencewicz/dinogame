import pygame
import time
pygame.init()
screen_height = 425
screen_width = 500
screen = pygame.display.set_mode((screen_width, screen_height))
background = pygame.image.load('dinos/grass_bg.png')
gray_background = pygame.image.load('dinos/grass_bg_gray.png')
goldcoin = pygame.image.load('dinos/goldcoin.png')
ledgeimg = pygame.image.load('dinos/ledge.png')
gray_ledgeimg = pygame.image.load('dinos/ledge_gray.png')
egg_imgs = [pygame.image.load('dinos/eggR.png'),pygame.image.load('dinos/eggL.png')]
right_imgs= [pygame.image.load('dinos/WR'+str(x)+'.png') for x in range (1,11)]
left_imgs = [pygame.image.load('dinos/WL'+str(x)+'.png') for x in range (1,11)]
idle_imgs = [pygame.image.load('dinos/IR1.png'), pygame.image.load('dinos/IL1.png')]
zombie_right_imgs = [pygame.image.load('zombies/WR'+str(x)+'.png') for x in range (1,11)]
zombie_left_imgs = [pygame.image.load('zombies/WL'+str(x)+'.png') for x in range (1,11)]
dead_right_imgs = [pygame.image.load('dinos/DR'+str(x)+'.png') for x in range (1,9)]
dead_left_imgs = [pygame.image.load('dinos/DL'+str(x)+'.png') for x in range (1,9)]
dead_zombie_right_imgs = [pygame.image.load('zombies/DR'+str(x)+'.png') for x in range (1,13)]
dead_zombie_left_imgs = [pygame.image.load('zombies/DL'+str(x)+'.png') for x in range (1,13)]
coin_sound = pygame.mixer.Sound("dinos/coin_sound.wav")
gameover_sound = pygame.mixer.Sound("dinos/timeup.wav")
playerwins_sound = pygame.mixer.Sound("dinos/fireworks.wav")
pygame.mixer.music.load("dinos/music.wav")
pygame.mixer.music.set_volume(0.06)
pygame.mixer.music.play(-1)
pygame.display.set_caption('Deano the Dinosaur')
pygame.display.set_icon(idle_imgs[0])
clock = pygame.time.Clock()
gameover = False
time_left = 30

class Hero():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 35
        self.height = 50
        self.velocity = 5
        self.imgcount = 0
        self.coins = 0
        self.right = False
        self.left = False
        self.isjumping = False
        self.jumpcount = 8
        self.direction = 'Right'
        self.onledge = False
        self.midair = False
        self.collision = False
        self.isdead = False
        self.deadimgcount = 0
        
class Egg():
    def __init__(self, x, y, direction):
        self.x = x+10 if direction == 'Right' else x-10
        self.y = y
        self.velocity = 8
        self.direction = direction

class Coin():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.visible = True

class Ledge():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onledge = False

class Enemy():
    def __init__(self, x, y, width, height, direction):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 2
        self.direction = direction
        self.imgcount = 0
        self.health = 24
        self.isdead = False
        self.deadimgcount = 0
        self.counter = 0

egglist = []
hero = Hero(5, 250)
enemylist = [Enemy(450, 250, 45, 50, 'Left')]
coinlist = [Coin(80, 150), Coin(230, 90), Coin(380, 150)]
ledges = [Ledge(70, 210, 60, 18), Ledge(220, 150, 60, 18), Ledge(370, 210, 60, 18)]

def reset():
    global time_left
    time_left = 30
    hero.x = 5
    hero.y = 250
    hero.coins = 0
    hero.right = False
    hero.left = False
    hero.isjumping = False
    hero.jumpcount = 8
    hero.direction = 'Right'
    hero.onledge = False
    hero.midair = False
    hero.collision = False
    hero.isdead = False
    for enemy in enemylist:
        enemy.x  = 450
        enemy.isdead = False
        enemy.direction = 'Left'
        enemy.health = 24
        enemy.imgcount = 0
        enemy.deadimgcount = 0
        enemy.counter = 0
    for coin in coinlist:
        coin.visible = True
    for egg in egglist:
        remove(egg)
    return

def redraw():
    #background
    screen.blit(background,(0,0))

    #text
    font1 = pygame.font.Font(pygame.font.get_default_font(), 24)
    text1 = font1.render("Coins: "+str(hero.coins), True, (0,0,0))
    screen.blit(text1, (10, screen_height-30))
    font2 = pygame.font.Font(pygame.font.get_default_font(), 48)
    if time_left >= 0 and time_left < 1:
        time_read = '00'
    elif str(time_left)[1] == '.':
        time_read = '0'+str(time_left)[0]
    else:
        time_read = str(time_left)[0]+str(time_left)[1]
    text2 = font2.render(time_read, True, (235,235,235))
    screen.blit(text2, ((screen_width/2) - (text2.get_width()/2), 15))

    #enemy
    for enemy in enemylist:
        if enemy.isdead == False:
            if enemy.imgcount == len(zombie_right_imgs):
                enemy.imgcount = 0
            if enemy.direction == 'Right':
                screen.blit(zombie_right_imgs[enemy.imgcount], (enemy.x,enemy.y))
            elif enemy.direction == 'Left':
                screen.blit(zombie_left_imgs[enemy.imgcount], (enemy.x,enemy.y))
        else:
            if enemy.direction == 'Right':
                screen.blit(dead_zombie_right_imgs[enemy.deadimgcount], (enemy.x,enemy.y))
            elif enemy.direction == 'Left':
                screen.blit(dead_zombie_left_imgs[enemy.deadimgcount], (enemy.x,enemy.y))
    #hero
    if hero.imgcount == len(right_imgs):
        hero.imgcount = 0
    if hero.right:
        screen.blit(right_imgs[hero.imgcount], (hero.x,hero.y))
        hero.imgcount += 1
    elif hero.left:
        screen.blit(left_imgs[hero.imgcount], (hero.x,hero.y))
        hero.imgcount += 1
    else:
        if hero.isdead == False:
            if hero.direction == 'Right':
                screen.blit(idle_imgs[0], (hero.x,hero.y))
            elif hero.direction == 'Left':
                screen.blit(idle_imgs[1], (hero.x,hero.y))
            hero.img = 0
        else:
            if hero.direction == 'Right':
                screen.blit(dead_right_imgs[hero.deadimgcount], (hero.x,hero.y))
            elif hero.direction == 'Left':
                screen.blit(dead_left_imgs[hero.deadimgcount], (hero.x,hero.y))
    #coins
    for coin in coinlist:
        if coin.visible:
            screen.blit(goldcoin, (coin.x, coin.y))
    #eggs
    for egg in egglist:
        if egg.direction == 'Right':
            screen.blit(egg_imgs[0], (egg.x, egg.y))
        elif egg.direction == 'Left':
            screen.blit(egg_imgs[1], (egg.x, egg.y))
    #ledges
    for ledge in ledges:
        screen.blit(ledgeimg, (ledge.x, ledge.y))

    pygame.display.update()
    return

def redraw_resetting():
    screen.blit(gray_background,(0,0))
    for ledge in ledges:
        screen.blit(gray_ledgeimg, (ledge.x, ledge.y))
    string = 'Player Wins!' if hero.coins == 3 else 'Player Loses!'
    font3 = pygame.font.Font(pygame.font.get_default_font(), 64)
    text3 = font3.render(string, True, (0,0,0))
    screen.blit(text3, ((screen_width/2)-(text3.get_width()/2), (screen_height/2)-(text3.get_height()/2)))
    font4 = pygame.font.Font(pygame.font.get_default_font(), 18)
    text4 = font4.render("(Press Enter to Respawn)", True, (0,0,0))
    screen.blit(text4, ((screen_width/2)-(text4.get_width()/2), (screen_height/2)-(text3.get_height()/2)+75))
    pygame.display.update()
    return
        
game_running = True  
while game_running:
    #timer
    clock.tick(30)
    if time_left <= 0:
        if hero.isdead == False and gameover == False:
            pygame.mixer.Sound.play(gameover_sound)
        hero.isdead = True
        gameover = True
        pygame.mixer.music.stop()
    else:
        if hero.isdead == False:
            time_left = time_left - .02 if time_left - .02 > 0 else 0

    #keystrokes 
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            game_running = False
    if game_running == False:
        break
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and hero.isdead == False:
        if len(egglist) == 0:
            egglist.append(Egg(hero.x, hero.y, hero.direction))

    if keys[pygame.K_LEFT] and hero.x > 0 and hero.isdead == False:
        hero.x -= hero.velocity
        hero.left = True
        hero.right = False
        hero.direction = 'Left'
        for ledge in ledges:
            if ledge.onledge == True:
                if  hero.x < ledge.x  - (ledge.width/2):
                    ledge.onledge = False
                    hero.onledge = False
    elif keys[pygame.K_RIGHT] and (hero.x + hero.width) < screen_width and hero.isdead == False:
        hero.left = False
        hero.right = True
        hero.x += hero.velocity
        hero.direction = 'Right'
        for ledge in ledges:
            if ledge.onledge == True:
                if hero.x-(hero.width/2) > ledge.x  + (ledge.width/2):
                    ledge.onledge = False
                    hero.onledge = False            
    else:
        hero.left = False
        hero.right = False
        hero.imgcount = 0

    if not hero.isjumping:
        if keys[pygame.K_UP] and hero.midair == False:
            hero.onledge = False
            hero.isjumping = True           
    else:
        if hero.jumpcount >= -8 and hero.isdead == False:
            hero.y = hero.y - (hero.jumpcount * abs(hero.jumpcount)) * .5
            hero.jumpcount -= 1
        else:
            hero.isjumping = False
            hero.jumpcount = 8
        
    #ledges
    for ledge in ledges:
        if hero.jumpcount < 0 or hero.midair == True:
            if hero.x >= ledge.x - (ledge.width/2) and hero.x <= ledge.x + (ledge.width):
                if hero.y+hero.height <= ledge.y+(ledge.height/2) and (ledge.y + (ledge.height/2)) - (hero.y+hero.height) < 20:
                    ledge.onledge = True
                    hero.y = ledge.y-hero.height
                    hero.onledge = True
                    hero.midair = False
                    hero.isjumping = False
                    hero.jumpcount = 8
                    
    #used here so hero falls incrementally if dropping from ledge to grass    
    if hero.isjumping == False and hero.onledge == False:
        if hero.y < 250:
            hero.midair = True
            hero.y = hero.y + 15 if (hero.y+15) < 250 else 250
        else:
            hero.midair = False

    #detects collision with enemy
    for enemy in enemylist:
        if hero.direction == 'Right' and enemy.isdead == False:
            if hero.x > enemy.x and hero.x < enemy.x+(enemy.width/2):
                if hero.y <= enemy.y and hero.y >= enemy.y-(enemy.height/2):
                    hero.collision = True
                    hero.y = 250
        elif hero.direction == 'Left' and enemy.isdead == False:
            if hero.x < enemy.x  and hero.x > enemy.x-(enemy.width/2):
                if hero.y <= enemy.y and hero.y >= enemy.y-(enemy.height/2):
                    hero.collision = True
                    hero.y = 250

    #hero dying sequence
    if hero.isdead == True:
        hero.deadimgcount = hero.deadimgcount + 1 if hero.deadimgcount < len(dead_right_imgs)-1  else len(dead_right_imgs)-1    

    #ends game upon collision
    if hero.collision:
        if hero.isdead == False and gameover == False:
            pygame.mixer.Sound.play(gameover_sound)
        hero.isdead = True
        gameover = True
        pygame.mixer.music.stop()

    #enemy
    for enemy in enemylist:
        if enemy.direction == 'Left' and enemy.isdead == False:
            enemy.x -= enemy.velocity
            if enemy.x == 0:
                enemy.direction = 'Right'
                enemy.imgcount = 0
            else:
                enemy.imgcount += 1
        elif enemy.direction == 'Right' and enemy.isdead == False:
            enemy.x += enemy.velocity
            if enemy.x > screen_width - enemy.width:
                enemy.direction = 'Left'
                enemy.imgcount = 0
            else:
                enemy.imgcount += 1
        else:
            enemy.deadimgcount = enemy.deadimgcount + 1 if enemy.deadimgcount < len(dead_zombie_right_imgs)-1 else len(dead_zombie_right_imgs)-1

    for enemy in enemylist:
        if enemy.isdead == True and enemy.counter < 100:
            enemy.imgcount = 0
            enemy.health = 24
            enemy.counter += .5
        elif enemy.counter == 100:
            enemy.deadimgcount = 0
            enemy.counter = 0
            enemy.isdead = False

    #coins
    for coin in coinlist:
        if hero.x >= coin.x - (coin.width * 0.5) and hero.x <= coin.x + (coin.width * 0.5):
            if hero.y >= coin.y -(coin.height * 0.5) and hero.y <= coin.y + (coin.height * 0.5):
                if coin.visible:
                    hero.coins += 1
                    pygame.mixer.Sound.play(coin_sound)
                    coin.visible = False

    #eggs
    for egg in egglist:
        if egg.direction == 'Right' and egg.x < screen_width:
            egg.x += egg.velocity
            for enemy in enemylist:
                if not enemy.isdead and egg.x > enemy.x and egg.x < enemy.x+(enemy.width/2):
                    if egg.y <= enemy.y and egg.y >= enemy.y-(enemy.height/2):
                        egglist.remove(egg)
                        enemy.health -= 8
                        if enemy.health <= 0:
                            enemy.isdead = True
        elif egg.direction == 'Left' and egg.x > 0:
            egg.x -= egg.velocity
            for enemy in enemylist:
                if not enemy.isdead and egg.x < enemy.x+(enemy.width/2) and egg.x > enemy.x-(enemy.width/2):
                    if egg.y <= enemy.y and egg.y >= enemy.y-(enemy.height/2):
                        egglist.remove(egg)
                        enemy.health -= 8
                        if enemy.health <= 0:
                            enemy.isdead = True
        else:
            egglist.remove(egg)
    #end game
    if hero.coins == 3:
        if gameover == False:
            pygame.mixer.Sound.play(playerwins_sound)
        gameover = True
        pygame.mixer.music.stop()
        
    #resets game
    if keys[pygame.K_RETURN] and gameover == True:
        reset()
        gameover = False
        pygame.mixer.music.play(-1)

    #redraws background
    if gameover == True:
        redraw_resetting()
    else:
        redraw()
