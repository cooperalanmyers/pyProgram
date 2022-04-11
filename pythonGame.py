# Cooper Myers
# Python Breakout Program CIS 343
# 4/10/22

import sys
import pygame
import random

class Game():
    
    def main(self):
        
        # Setting Speeds 
        __horizontalSpeed = 2
        __verticalSpeed= 2
        bat_speed = 40
        xspeed = __horizontalSpeed
        yspeed = __verticalSpeed

        # Initialize Lives and Score        
        __max_lives = 3
        score = 0
        lives = __max_lives
        
        # Setting Size and Background Color
        background = 0xFF, 0xFF, 0xFF  # White Background        
        size = width, height = 800, 800
        pygame.init()            
        screen = pygame.display.set_mode(size)

        # Creating wall object and using helper method to build
        wall = Brick()
        wall.build_wall(width)

        # Setting up clock
        clock = pygame.time.Clock()
        
        # If a key is held down it will repeat the true value passed
        pygame.key.set_repeat(1,30)
        
        # Mouse is no longer appearing on game screen
        pygame.mouse.set_visible(0)
        
        Overlay()
        Paddle()
        Ball()
        
        # Sound
        
        sound = pygame.mixer.Sound('mixkit-futuristic-space-war-percussion-2787.wav')
        sound.set_volume(10)
        sound.play(0)

        hitSound = pygame.mixer.Sound('mixkit-acute-guitar-single-string-2325.wav')
        hitSound.set_volume(10)
        #hitSound.play(0)
        
        batrect = batrect.move((width / 2) - (batrect.right / 2), height - 60)
        ballrect = ballrect.move(width / 2, height / 2) 
        
        # Always True
        while 1: 
            
            # Refresh Rate
            clock.tick(60)

            # Key Clicks
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
        	            sys.exit()
                    if event.key == pygame.K_LEFT:                        
                        batrect = batrect.move(-bat_speed, 0)     
                        if (batrect.left < 0):                           
                            batrect.left = 0      
                    if event.key == pygame.K_RIGHT:                    
                        batrect = batrect.move(bat_speed, 0)
                        if (batrect.right > width):                            
                            batrect.right = width
                    if event.key == pygame.K_DOWN:
                        # Place New Ball

                # If bat has hit the ball  
                if ballrect.bottom >= batrect.top and ballrect.bottom <= batrect.bottom and ballrect.right >= batrect.left and ballrect.left <= batrect.right:
                    yspeed = -yspeed                
                    offset = ballrect.center[0] - batrect.center[0]
                  
                
                # offset > 0 means ball has hit RHS of bat                   
                # vary angle of ball depending on where ball hits bat                      
                if offset > 0:
                    if offset > 30:  
                        xspeed = 7
                    elif offset > 23:                 
                        xspeed = 6
                    elif offset > 17:
                        xspeed = 5 
                else:  
                    if offset < -30:                             
                        xspeed = -7
                    elif offset < -23:
                        xspeed = -6
                    elif xspeed < -17:
                        xspeed = -5     
                      
            # move bat/ball
            ballrect = ballrect.move(xspeed, yspeed)
            if ballrect.left < 0 or ballrect.right > width:
                xspeed = -xspeed                
            if ballrect.top < 0:
                yspeed = -yspeed                

            # check if ball has gone past bat - lose a life
            if ballrect.top > height:
                lives -= 1
                # start a new ball
                xspeed = horizontalSpeed
                rand = random.random()                
                if random.random() > 0.5:
                    xspeed = -xspeed 
                yspeed = verticalSpeed           
                ballrect.center = width * random.random(), height / 3                                
                if lives == 0:                    
                    msg = pygame.font.Font(None,70).render("Game Over", True, (0,255,255), background)
                    msgrect = msg.get_rect()
                    msgrect = msgrect.move(width / 2 - (msgrect.center[0]), height / 3)
                    screen.blit(msg, msgrect)
                    pygame.display.flip()
                    # process key presses
                    #     - ESC to quit
                    #     - any other key to restart game
                    while 1:
                        restart = False
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                sys.exit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                    	            sys.exit()
                                if not (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):                                    
                                    restart = True      
                        if restart:                   
                            screen.fill(background)
                            wall.build_wall(width)
                            lives = __max_lives
                            score = 0
                            break
            
            if xspeed < 0 and ballrect.left < 0:
                xspeed = -xspeed                                

            if xspeed > 0 and ballrect.right > width:
                xspeed = -xspeed                               
           
            # check if ball has hit wall
            # if yes yhen delete brick and change ball direction
            index = ballrect.collidelist(wall.brickrect)       
            if index != -1: 
                if ballrect.center[0] > wall.brickrect[index].right or \
                   ballrect.center[0] < wall.brickrect[index].left:
                    xspeed = -xspeed
                else:
                    yspeed = -yspeed                
                wall.brickrect[index:index + 1] = []
                score += 10
                          
            screen.fill(background)
            

            for i in range(0, len(wall.brickrect)):
                screen.blit(wall.brick, wall.brickrect[i])    

            # if wall completely gone then rebuild it
            if wall.brickrect == []:              
                wall.build_wall(width)                
                xspeed = __horizontalSpeed
                yspeed = __verticalSpeed               
                ballrect.center = width / 2, height / 3
         
            screen.blit(ball, ballrect)
            screen.blit(bat, batrect)
            pygame.display.flip()
            
class Overlay():
    scoretext = pygame.font.Font(None,40).render(str(score), True, (0,255,255), background)
    scoretextrect = scoretext.get_rect()
    scoretextrect = scoretextrect.move(width - scoretextrect.right, 0)
    screen.blit(scoretext, scoretextrect)
    
    livestext = pygame.font.Font(None,40).render(str(lives), True, (0,255,255), background)
    livestextrect = livestext.get_rect()
    livestextrect = livestextrect.move(width - livestextrect.right, 0)
    screen.blit(livestext, livestextrect)
    
    
class Paddle():
    bat = pygame.image.load("GameBar.png").convert()
    batrect = bat.get_rect()    
            
    #batrect = batrect.move((width / 2) - (batrect.right / 2), height - 60)
    #ballrect = ballrect.move(width / 2, height / 2)       

    
class Ball():
    ball = pygame.image.load("Ball.png").convert()
    ballrect = ball.get_rect()    
    
    #ballrect = ballrect.move(width / 2, height / 2)       

    
class Brick():

    def __init__(self):
        self.brick = pygame.image.load("brick.png").convert()
        brickrect = self.brick.get_rect()
                
        self.brickheight = brickrect.bottom - brickrect.top             
        self.bricklength = brickrect.right - brickrect.left       

    def build_wall(self, width):        
        x = 0
        y = 60
        adjust = 0
        self.brickrect = []
        for i in range (0, 33):           
            if x > width:
                if adjust == 0:
                    adjust = self.bricklength / 2
                else:
                    adjust = 0
                x = -adjust
                y += self.brickheight
                
            self.brickrect.append(self.brick.get_rect())    
            self.brickrect[i] = self.brickrect[i].move(x, y)
            x = x + self.bricklength

            
# Statement to Run Game
if __name__ == '__main__':
    start = Game()
    start.main()
