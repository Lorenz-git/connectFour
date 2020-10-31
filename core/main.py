import pygame

from core.board import Board
from core.constants import FPS, WIDTH, HEIGHT

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("connect4")
clock = pygame.time.Clock()

board = Board()
winner = 0

# game loop
running = True
while running:
    # keep loop at right speed
    clock.tick(FPS)

    # process input events
    for event in pygame.event.get():

        # check for closing window
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEMOTION:
            if winner == 0:
                board.mouse_move(pygame.mouse.get_pos())
        if event.type == pygame.MOUSEBUTTONDOWN:
            if winner == 0:
                board.set_coin(pygame.mouse.get_pos())
                winner = board.check_winner()
                board.next_turn()
            else:
                board = Board()
                winner = 0

    # render
    if winner == 0:
        board.draw(screen)
    else:
        # show winner screen
        board.show_winner(screen, winner)

    # after drawing everything, display prepared image
    pygame.display.flip()

pygame.quit()


def main():
    return 0


if __name__ == "__main__":
    main()
