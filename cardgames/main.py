import pygame
from pygame.locals import *
pygame.init()

DISPLAY = pygame.display.set_mode((800,800))
pygame.display.set_caption("thing")
clock = pygame.time.Clock()

run = True
while run:
    clock.tick(60)

    # handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

    # clear display
    DISPLAY.fill(0)

    # draw scene
    pygame.draw.rect(DISPLAY, (200,200,200), pygame.Rect(0,400,800,400))

    # update display
    pygame.display.flip()
    pygame.display.update()

pygame.quit()
exit()