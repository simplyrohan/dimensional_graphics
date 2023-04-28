import main

import pygame

pygame.init()

screen = pygame.display.set_mode([500, 500])
pygame.display.set_caption("Untitled Game")

clock = pygame.time.Clock()

objs = []

camera = main.Camera(objs)

with open('faces.txt') as f:
    model = main.Model(eval(f.read()), 200)

objs.append(model)

PLAYER_SPEED = 0.001

dt = 0

running = True
while running:

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                camera.position[0] += PLAYER_SPEED*dt
            elif event.key == pygame.K_RIGHT:
                camera.position[0] -= PLAYER_SPEED*dt
            
            if event.key == pygame.K_UP:
                camera.position[2] -= PLAYER_SPEED*dt
            elif event.key == pygame.K_DOWN:
                camera.position[2] += PLAYER_SPEED*dt

        elif event.type == pygame.MOUSEMOTION:
            camera.rotation[1] = (event.pos[0]-250)/50
            camera.rotation[0] = (event.pos[1]-250)/50

    pygame.key.set_repeat(1)

  
    screen.fill((255, 255, 255)) # Background Color

    # Content to draw
    camera.render(screen)

    # objs[0].rotation[0] += 0.001*dt

    pygame.display.flip()
    dt = clock.tick(60) # Change this to FPS

pygame.quit()