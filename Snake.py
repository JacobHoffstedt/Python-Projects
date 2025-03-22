#Snake 
#64x64 kanske vita plupp 1x8 först åker framåt, kan styras med upp höger vänster ned
#Behöver något som trackar dess position, om den träffar äpplet ökar den med +1 i baken och hastigheten ökar
#Behöver något som håller koll på vad som är del av ormen så att man vet ifall den träffar sig själv. 


import pygame
import sys

pygame.init()

screen_width = 600
screen_height = 400

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")


