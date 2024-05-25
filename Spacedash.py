import pygame, sys
import random
from pygame.locals import *

def main():

    gameVel = 1.5
    
    pygame.init()
    myFont = pygame.font.Font(None, 200)
    myFontRest = pygame.font.Font(None, 72)
    myFontSmall = pygame.font.Font(None, 40)

    pygame.display.set_caption("Spacedash")

    DISPLAY=pygame.display.set_mode((1000,600),0,32)

    WHITE = (255,255,255)
    BLUE = (0,0,255)

    player = pygame.Vector2()
    player.xy = 200,200
    playerVel = 0.6
    playerAccel = 0.03

    groundHeight = DISPLAY.get_height() - DISPLAY.get_height() / 8
    
    MIN_WALL_CLEARANCE = 80
    wallClearance = 150

    wall = pygame.Vector2()

    wall.xy = DISPLAY.get_width(), random.randint(75+wallClearance, int(groundHeight - 75))

    pointsScored = 0
    hasScored = False

    collectable = pygame.Vector2()
    collectable.xy = random.randint(DISPLAY.get_width(), DISPLAY.get_width() + int(DISPLAY.get_width() / 2) ), random.randint(15, int(groundHeight - 15))
    collectableScore = 0

    dead = False

    inverse = False

    while True:

        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key==K_UP:
                inverse = True

        DISPLAY.fill(WHITE)

        #Create random obstical BOTTOM
        if wall.x < -50:
            wall.y = random.randint(75+wallClearance, int(groundHeight - 75)) # - wallClearance
            wall.x = DISPLAY.get_width()
            hasScored = False

        pygame.draw.rect(DISPLAY, "red", (wall.x, wall.y, 50, DISPLAY.get_height())) # Bottom
        pygame.draw.rect(DISPLAY, "red", (wall.x, 0, 50, wall.y - wallClearance)) # Top

        wall.x = wall.x - gameVel

        #Player
        pygame.draw.rect(DISPLAY, BLUE, (player.x, player.y, 50, 50))
        player.y = player.y + playerVel
        if not inverse:
            playerVel += playerAccel
        else:
            playerVel -= playerAccel

        #Ground
        pygame.draw.rect(DISPLAY, "black", (0, groundHeight, DISPLAY.get_width(), 10))

        #Slide on ground
        if player.y + 50 > groundHeight:
            player.y = groundHeight - 50
        
        #Slide on Ceiling
        if player.y < 0:
            player.y = 0

        keys = pygame.key.get_pressed()

        #Flying
        if keys[K_SPACE]and not dead and not inverse:
            playerVel = 0.6
            player.y -= 3.5 #4
        elif keys[K_SPACE] and not dead:
            playerVel = -0.6
            player.y += 3.5


        

        #Die
        if checkWallCollision(player.x, player.y, wall.x, wall.y, wallClearance):
            gameVel = 0
            playerVel = 0
            dead = True
            resetText = myFontRest.render("Press P to Reset", True, "black")
            DISPLAY.blit(resetText, (DISPLAY.get_width() / 2 - 150, DISPLAY.get_height() / 2))
        
        #Reset
        if dead and keys[K_p]:
            gameVel = 1.5
            playerVel = 0.6
            player.xy = 200,200
            wall.xy = DISPLAY.get_width(), random.randint(75+wallClearance, int(groundHeight - 75))
            pointsScored = 0
            hasScored = False
            dead = False
            collectable.xy = random.randint(DISPLAY.get_width(), DISPLAY.get_width() + int(DISPLAY.get_width() / 2) ), random.randint(15, int(groundHeight - 15))
            collectableScore = 0
            inverse = False

        if player.x > wall.x + 50 and not hasScored:
            pointsScored += 1
            hasScored = True
            gameVel += 1.5*0.1

        #Collectable
        pygame.draw.rect(DISPLAY, "green", (collectable.x, collectable.y, 15, 15))
        collectable.x -= gameVel

        if(collectable.x < 0):
            collectable.xy = random.randint(DISPLAY.get_width(), DISPLAY.get_width() + int(DISPLAY.get_width() / 2) ), random.randint(15, int(groundHeight - 15))
        
        if checkCollision(player.x, player.y, 50, 50, collectable.x, collectable.y, 15, 15):
            collectableScore = collectableScore + 1
            collectable.x = random.randint(DISPLAY.get_width(), DISPLAY.get_width() + int(DISPLAY.get_width() / 2))
            collectable.y = random.randint(15, int(groundHeight - 15))
        
        if checkWallCollision(collectable.x, collectable.y, wall.x, wall.y, wallClearance):
            collectable.x = collectable.x - 100
        
        #Score Display
        scoreText = myFont.render(str(pointsScored), True, "grey")
        DISPLAY.blit(scoreText, (DISPLAY.get_width() / 2 - 50, 0))

        #Collectable Counter Display
        collectableText = myFontSmall.render("Counter: " + str(collectableScore), True, "black")
        DISPLAY.blit(collectableText, (0,0))


        pygame.draw.rect(DISPLAY, "white", (0, groundHeight + 10, DISPLAY.get_width(), DISPLAY.get_height() - groundHeight))
        pygame.display.update()
        pygame.time.delay(10)

def checkWallCollision(x1, y1, x2, y2, wallClearance):
    return (x2 <= x1 + 50 and x1 <= x2 + 50) and (y1 + 50 >= y2 or y1 <= y2 - wallClearance)

def checkCollision(x1, y1, width_1, height_1, x2, y2, width_2, height_2):
    return x1 + width_1 >= x2 and x1 <= x2 + width_2 and y1 + width_1 >= y2 and y1 <= y2 + height_2
    
main()