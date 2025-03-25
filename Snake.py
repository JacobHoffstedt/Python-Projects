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
block_size = 20
snake_color = (0, 255, 0)
snake = [(300, 200), (280, 200), (260, 200)]

def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, snake_color, (segment[0], segment[1], block_size, block_size))


running = True
while running:  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((0, 0, 0)) #Color'
    draw_snake(snake)
    pygame.display.flip()
    clock.tick(15)

pygame.quit()
sys.exit()

