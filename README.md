# dimensional_graphics
A ✨pure Python and Pygame✨ 3D renderer.

# Highlights
🚀 Is optimized to handle to large scenes 

🤝 Integrates directly with `pygame(-ce)` 

😃 Simple to use

# Install
In your root directory:
```bash
pip3 install pygame-ce
git clone https://github.com/simplyrohan/dimensional_graphics.git
```

# Usage
```py
from dimensional_graphics import Camera, Model, load
import pygame
pygame.init()

screen = pygame.display.set_mode([500, 500])
pygame.display.set_caption("Untitled Game")

clock = pygame.time.Clock()

camera = Camera()

size = 10
model = Model(load('path_to_file.obj'), size)

running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

  
    screen.fill((255, 255, 255)) # Background Color

    # Your game
    camera.render([model], screen)

    pygame.display.flip()
    clock.tick(60) # Change this to FPS

pygame.quit()
```
And that's it! Just a few lines of code and you've got your 3D application up and running.
