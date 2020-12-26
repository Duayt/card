from network import Network
import pygame


WIDTH, HEIGHT = 500, 500
BACKGROUND_COLOR = (100, 255, 100)

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Client')
pygame.font.init()
client_number = 0


def redraw_window(win, sprite_group):
    win.fill(BACKGROUND_COLOR)
    for sprite in sprite_group:
        sprite.draw(win)
    pygame.display.update()


# def main():
#     running = True
#     n = Network()
#     p = n.get_p()
#     clock = pygame.time.Clock()
#     all_players = pygame.sprite.Group()
#     all_players.add(p)

#     while running:
#         clock.tick(60)
#         p2 = n.send(p)

#         # all_players.add(p2)
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#                 pygame.quit()
#         p.move(WIDTH, HEIGHT)
#         redraw_window(win, all_players, p2)
def main():
    


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (255, 0, 0))
        win.blit(text, (100, 200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
    main()


if __name__ == "__main__":
    while True:
        menu_screen()
