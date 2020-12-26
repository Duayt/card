# %%
import pygame
from pathlib import Path
from cardgames.games import PokDeng, Pip, Suit, Card, PokDengRules, Deck, Stack
import logging
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
this_path = Path(__file__).parent
asset_dir = this_path / 'assets'
icon_dir = asset_dir / 'icon.png'
cards_dir = asset_dir/'cards'
sound_dir = this_path / 'sounds'

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

# Sounds
pygame.mixer.music.load(str(sound_dir / 'casino.wav'))
pygame.mixer.music.play(loops=-1)

#
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
screen.fill(BACKGROUND_COLOR)

pygame.display.set_caption("POK DENG")
pygame.display.set_icon(img_icon)

font_name = pygame.font.match_font('arial')

clock = pygame.time.Clock()

# Object

class pgHand(pygame.sprite.Sprite):
    def __init__(self, x, y, card_stack: Stack = None, pip_margin=20, n_cards=3):
        super(pgHand, self).__init__()
        self.surf = pygame.Surface(
            (CARD_WIDTH+pip_margin*n_cards, CARD_HEIGHT), pygame.SRCALPHA)
        self.rect = self.surf.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.pip_margin = pip_margin
        self.n_cards = n_cards
        self.card_stack = card_stack
        self.draw_card()

    def draw_card_boarder(self):
        for i in range(self.n_cards):
            pygame.draw.rect(self.surf, BLACK, pygame.Rect(0+i*self.pip_margin, 0,
                                                           CARD_WIDTH, CARD_HEIGHT), width=1)

    def draw_card(self):
        if self.card_stack is not None:
            for i, card in enumerate(self.card_stack):
                self.surf.blit(img_cards_dict[card.img_name], (0+i*self.pip_margin, 0,
                                                               CARD_WIDTH, CARD_HEIGHT))


# logging.basicConfig(level=logging.INFO)
seed = 1234
n_player = 4
PokDengRules.set_rules()
game = PokDeng.init_state(n_player=n_player, wallet=100)
# n_games = 2
# for i in range(n_games):
#     game.play(seed=i)
#     print(i)

deck = Deck(is_shuffle=True, seed=seed)
# deal 1 card each player including dealer
hands = 2
for i in range(hands):
    for p in game.all_players:
        deck.deal(p.hand, 1)
# Run until the user asks to quit
deal_area = pgHand(SCREEN_WIDTH//2,
                   SCREEN_HEIGHT*3//8, card_stack=game.dealer.hand)
play_area_list = [pgHand(int((SCREEN_WIDTH//(len(game.players)+1))*(i+1)),
                         SCREEN_HEIGHT*6//8, card_stack=player.hand) for i, player in enumerate(game.players)]
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # c = Card.new(1, 1)
    # screen.blit(img_cards_dict[c.img_name], (0, 0, 5, 5))
    screen.blit(deal_area.surf, deal_area.rect)
    for area in play_area_list:
        screen.blit(area.surf, area.rect)

    clock.tick(FPS)
    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()

# %%
