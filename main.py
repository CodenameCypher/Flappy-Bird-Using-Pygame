import pygame
import random
from pygame import mixer
import time

#initializing pygame
pygame.init()
screen = pygame.display.set_mode((500,550))

#title and icon
pygame.display.set_caption("Flappy Dog")
pygame.display.set_icon(pygame.image.load('images/dog.png'))

#bg surface image
bg_surface = pygame.image.load('images/bg_surface.png')
bg_imageX = 0
#bg floor image
bg_floor = pygame.image.load('images/bg_floor.png')
bg_floorX = 0

#player standing
standingDog = pygame.image.load('images/sitting.png')
standingDogX = 10
standingDogY = 435

#player jumping
jumpingDog = pygame.image.load('images/jumping.png')
jumpingDogX = standingDogX
jumpingDogY = 436
jumpingDogXChange = 0
jumpingDogYChange = 0

#obstacles
obstacleOne = pygame.image.load('images/obs.png')
obstacleTwo = pygame.image.load('images/ref_obs.png')
obsX = 200
obsY = 200
difference = 650

#score
score = 0
font = pygame.font.Font('fonts/Neuterous.otf',32)
scoreX = 0
scoreY = 0

#game over
gameOverfont = pygame.font.Font('fonts/Spooky Haunt.otf',50)
gameX = 250
gameY = 275

#button play again
playAgain = pygame.font.Font('fonts/Spooky Haunt.otf',50)
playAgainX = 20
playAgainY = 120

#quit text
quitText = pygame.font.Font('fonts/Spooky Haunt.otf',50)
quitX = 125
quitY = 175

def showSittingDog(x,y):
    screen.blit(standingDog,(x,y))

def showJumpingDog(x,y):
    screen.blit(jumpingDog,(x,y))

def drawObstacle(x,y,difference):
    screen.blit(obstacleOne,(x,y))
    screen.blit(obstacleTwo,(x,y-difference))

def collision(obsx,obsy,jumpingX,jumpingY,differ):
    if (obsy-50 <= jumpingY <= 436 or 0 <= jumpingY <= (obsy + 512 - differ)) and 103 >= obsx >= 20:
        return True 
    else: return False

def showScore(x,y):
    s = font.render("Score : "+str(score),True,(255,255,255))
    screen.blit(s,(x,y))

def gameOverText(x,y):
    s = gameOverfont.render("GAME OVER",True,(255,255,255))
    screen.blit(s,(x,y))

def quitText(x,y,colour):
    s = playAgain.render("Quit",True,colour)
    screen.blit(s,(x,y))

def playAgainText(x,y,colour):
    s = playAgain.render("Press Space to Play",True,colour)
    screen.blit(s,(x,y))

#bg music
mixer.music.load('sounds/bg_music.mp3')
mixer.music.set_volume(0.5)
mixer.music.play(-1)

dogRunning = False
running = True
while running:
    screen.fill((23,23,23))
    screen.blit(bg_surface,(bg_imageX,-90))
    drawObstacle(obsX+150,obsY,difference)
    screen.blit(bg_floor,(bg_floorX,500))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if quitX <= mouse[0] <= quitX + 50 and quitY <= mouse[1] <= quitY + 50:
                running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if dogRunning == False:
                    score = 0
                    standingDogX = 10
                    standingDogY = 435
                    jumpingX = standingDogX
                    jumpingDogY = 436
                    obsX = 200
                    obsY = random.randint(210,350)
                    difference = random.randint(650,750)
                    jumpingDogYChange = -3
                    jumpingDogXChange = 1
                    dogRunning = True
                else:
                    jumpingDogYChange = -3
                    jumpingDogXChange = 1
                    
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                jumpingDogYChange = 1
                jumpingDogXChange = 1


    if dogRunning:
        if jumpingDogX is 200: 
            bg_imageX -= 0.3
        if bg_imageX + 1801 < 900:
            pygame.transform.flip(bg_surface,True,False)
            bg_imageX = 0

        if jumpingDogX is 200:
            bg_floorX -= 0.5
        if bg_floorX + 1800 < 900:
            bg_floorX = 0
        
        obsX -= 0.5
        
        if obsX <= 4:
            obsX = 200
            obsY = random.randint(210,350)
            difference = random.randint(650,750)

        jumpingDogY += jumpingDogYChange
        jumpingDogX += jumpingDogXChange
        if jumpingDogX >= 200:
            jumpingDogX = 200
        if jumpingDogY >= 436:
            jumpingDogY = 436
            showSittingDog(jumpingDogX,jumpingDogY)
        else:
            showJumpingDog(jumpingDogX,jumpingDogY)
        if jumpingDogY <= 0:
            jumpingDogY = 0

        if collision(obsX,obsY,jumpingDogX,jumpingDogY,difference):
            mixer.Sound('sounds/fail.wav').play(0)
            gameOverText(gameX,gameY)
            pygame.display.update()
            time.sleep(1)
            dogRunning = False
            
        else:
            if obsX + 170 == 200 :
                score += 1
                mixer.Sound('sounds/success.wav').play(0)
                


    else:
        showSittingDog(standingDogX,standingDogY)
        #mouse movement
        mouse = pygame.mouse.get_pos()

        playAgainText(playAgainX,playAgainY,(255,255,255))
        
        if quitX <= mouse[0] <= 500 and quitY <= mouse[1] <= quitY + 50:
            quitText(quitX,quitY,(189, 32, 49 ))
        else:
            quitText(quitX,quitY,(255,255,255))
         
        


    showScore(scoreX,scoreY)
    pygame.display.update()