import pygame, sys
import random
from pygame.locals import *



def main():
    pygame.init()

    pygame.display.set_caption("Spacedash")

    DISPLAY=pygame.display.set_mode((1000,600),0,32)

    WHITE = (255,255,255)
    BLUE = (0,0,255)

    player = pygame.Vector2()
    player.xy = 200,200
    playerVel = 0.6
    playerAccel = 0.03

    groundHeight = DISPLAY.get_height() - DISPLAY.get_height() / 8
    
    MIN_AST_CLEARANCE = 80
    astClearance = MIN_AST_CLEARANCE

    ast = pygame.Vector2()

    ast.xy = DISPLAY.get_width(), random.randint(astClearance, int(groundHeight - astClearance))
    astVel = 1.5

   


    while True:

        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()

        DISPLAY.fill(WHITE)

        #Create random obstical BOTTOM
        if ast.x < -50:
            ast.y = random.randint(astClearance, int(groundHeight - astClearance))
            ast.x = DISPLAY.get_width()

        pygame.draw.rect(DISPLAY, "red", (ast.x, ast.y, 50, DISPLAY.get_height() - ast.y))
        pygame.draw.rect(DISPLAY, "red", (ast.x, 0, 50, ast.y - astClearance))

        ast.x = ast.x - astVel

        #Create random obstical TOP


        #Player
        pygame.draw.rect(DISPLAY, BLUE, (player.x, player.y, 50, 50))
        player.y = player.y + playerVel
        playerVel += playerAccel

        #Ground
        pygame.draw.rect(DISPLAY, "black", (0, groundHeight, DISPLAY.get_width(), 10))

        #Slide on ground
        if player.y + 50 > groundHeight:
            player.y = groundHeight - 50

        keys = pygame.key.get_pressed()
        if keys[K_SPACE]:
            playerVel = 0.6
            player.y -= 3.5 #4
            
        
        if player.y < 0:
            player.y = 0
       



        pygame.draw.rect(DISPLAY, "white", (0, groundHeight + 10, DISPLAY.get_width(), DISPLAY.get_height() - groundHeight))
        pygame.display.update()
        pygame.time.delay(10)

    def checkPlayerCollision(x1, y1, x2, y2):
        # return x - radius < player_pos.x + 10 and ball_pos.x - radius > player_pos.x and ball_pos.y + radius > player_pos.y and ball_pos.y - radius < player_pos.y + 50
        pass

main()