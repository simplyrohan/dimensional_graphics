# A doom FPS clone using the dimensional_grpahics library
import dimensional_graphics as dimensional
import pygame
from settings import *

pygame.init()

screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption('DOOM')

clock = pygame.Clock()
dt = 0

objs = []
camera = Camera(objs)

running = True
while running:
    events = pygame.event.get()
  
    screen.fill(BG)
    camera.render(screen)
    pygame.display.flip()
pygame.quit()
