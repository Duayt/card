import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (100,255,100)
# Set up the drawing window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
# Fill the background with white
screen.fill(BACKGROUND_COLOR)
surf = pygame.Surface((50, 50))
surf.fill((0, 0, 0))
rect = surf.get_rect()

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    
    
    screen.blit(surf,(SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
    # Draw a solid blue circle in the center
    pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()