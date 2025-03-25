#Snake 
#64x64 kanske vita plupp 1x8 först åker framåt, kan styras med upp höger vänster ned
#Behöver något som trackar dess position, om den träffar äpplet ökar den med +1 i baken och hastigheten ökar
#Behöver något som håller koll på vad som är del av ormen så att man vet ifall den träffar sig själv. 


import pygame
import sys

pygame.init() #Initiating the game and associated functions. 

screen_width = 600
screen_height = 400

screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE) #Applying screen size and making it adjustable. 
pygame.display.set_caption("Snake Game") #Setting name in title bar

clock = pygame.time.Clock() #Sets up the framerate of the game  
#Initiates the black box (the game screen) it runs until its crossed manually. 
#Snake
block_size = 20 #Size of each piece of the snake
snake_color = (0, 255, 0) #Green color
snake = [(300, 200), (280, 200), (260, 200)] #Initial snake as x and y coordinates. 
direction = (block_size, 0)  # Sets the direction of the snake movement, moves 20 pixels per frame at 15 frames per second. 
#Sets X to block size and Y to 0. 


#Drawing the snake
#for block in snake: Loops over each of the coordinates in the snake variable.
#pygame.draw.rect: Draws a rectangle using ()
#screen is the created earlier
#snake_color is defined earlier
#block[0] and block[1] refers to the x and y values of the snake, calls the coordinates in the snake variable created.
#block_size is the width and height of the snake.
def draw_snake(snake): 
    for block in snake:
        pygame.draw.rect(screen, snake_color, (block[0], block[1], block_size, block_size)) #pygame.draw.rect(SURFACE, COLOR, (x, y, width, height))



#New_head: Moves the snake to the right by adding x and y coordinates each frame. 
#x value is updated to the head of the snake representing 300 in (300, 200) and thus snake[0][0](first value of first tuple)
#y value is updated to the head of the snake representing 200 in (300, 200) and thus snake[0][1](second value of first tuple)
#The direction represents how the new head adds to the latest head and is represented by the direction variable, calling direction[0] calls the 
#block_size value. and direction[1] the 0 value. So, the snake moves 20 pixels per frame to the right, and not vertically. 
#snake.insert(0, new_head): list.insert(index, value) Adds the new head to the beginning of the list in front of the old head. 
#snake.pop just removes the last value in the list, the last tail. 

running = True
while running:      
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, block_size):
                direction = (0, -block_size)
            elif event.key == pygame.K_DOWN and direction != (0, -block_size):
                direction = (0, block_size)
            elif event.key == pygame.K_LEFT and direction != (block_size, 0):
                direction = (-block_size, 0)
            elif event.key == pygame.K_RIGHT and direction != (-block_size, 0):
                direction = (block_size, 0)
            
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    snake.insert(0, new_head)
    snake.pop()


    
    screen.fill((0, 0, 0)) #Color
    draw_snake(snake)
    pygame.display.flip()
    clock.tick(15)

pygame.quit()
sys.exit()

