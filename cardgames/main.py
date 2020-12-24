# %%
import pygame
from pathlib import Path
from cardgames.games import PokDeng, Pip, Suit, Card
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


# Game constant
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

CARD_SCALE = 8
CARD_WIDTH = 691 // CARD_SCALE
CARD_HEIGHT = 1056 // CARD_SCALE
BACKGROUND_COLOR = (100, 255, 100)
FPS = 144

# Define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Path
asset_dir = Path(__file__).parent / 'assets'
icon_dir = asset_dir / 'icon.png'
cards_dir = asset_dir/'cards'

# Load images
img_icon = pygame.image.load(str(icon_dir))

# Load cards
img_cards_dict = {}
for p in Pip:
    for s in Suit:
        key = str(p)+str(s.name[0])
        img = pygame.image.load(
            str(cards_dir / f'{key}.png'))
        img = pygame.transform.scale(
            img, (CARD_WIDTH, CARD_HEIGHT))
        img_cards_dict[key] = img
# Init
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
screen.fill(BACKGROUND_COLOR)

pygame.display.set_caption("POK DENG")
pygame.display.set_icon(img_icon)

font_name = pygame.font.match_font('arial')

clock = pygame.time.Clock()

# Object


class HandArea(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(HandArea, self).__init__()
        self.surf = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
        self.rect = self.surf.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.bottom = SCREEN_HEIGHT - 10

        pygame.draw.rect(self.surf, BLACK, pygame.Rect(
            CARD_WIDTH//10, CARD_HEIGHT//10, 4, 4), width=1)


deal_area = HandArea(50, 50)
# Run until the user asks to quit
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    c = Card.new(1, 1)
    screen.blit(img_cards_dict[c.img_name], (0, 0, 5, 5))
    screen.blit(deal_area.surf, deal_area.rect)
    clock.tick(FPS)
    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()

# %%
