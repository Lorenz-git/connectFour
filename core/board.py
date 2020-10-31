from typing import Tuple, Optional

import pygame

from core.constants import COLOR_BG, HEIGHT, WIDTH, TILES_X, TILES_Y, TILE_SIZE, COLOR_EMPTY, COLOR_P1, COLOR_P2, \
    COLOR_P1_HIGHLIGHT, COLOR_P2_HIGHLIGHT, CONNECT, COLOR_TEXT, TEXT_HEIGHT, COLOR_TEXT_BG
from core.utils import grid_to_pixel_coord, center_coord, pixel_to_grid_coord


class Board:
    def __init__(self):
        self.coins = [[0] * TILES_Y for _ in range(TILES_X)]
        self.player_to_move = 1
        self.highlight: Tuple[int, int] = None

    def mouse_move(self, pos: Tuple[int, int]):
        col = pixel_to_grid_coord(pos)[0]
        coin = self.get_first_empty(col)
        if coin is not None:
            self.highlight = (col, coin)

    def set_coin(self, pos: Tuple[int, int]):
        col = pixel_to_grid_coord(pos)[0]
        coin = self.get_first_empty(col)
        if coin is not None:
            self.coins[col][coin] = self.player_to_move
            self.highlight = None

    def get_first_empty(self, col: int) -> Optional[int]:
        for i, coin in enumerate(self.coins[col]):
            if coin == 0:
                return i
        return None

    def check_winner(self) -> int:
        for x, cols in enumerate(self.coins):
            for y, coin in enumerate(cols):
                if coin == self.player_to_move:
                    game_over = (
                            self.win_horizontal((x, y))
                            or self.win_vertical((x, y))
                            or self.win_diagonal_one((x, y))
                            or self.win_diagonal_two((x, y))
                    )
                    if game_over:
                        return 1 if self.player_to_move == 1 else 2
        if self.is_draw():
            return 3
        return 0

    def is_draw(self):
        for cols in self.coins:
            for coin in cols:
                if coin == 0:
                    return False
        return True

    def win_horizontal(self, coin: Tuple[int, int]) -> bool:
        connected = 1
        # check left
        x = coin[0] - 1
        while x >= 0:
            if self.coins[x][coin[1]] == self.player_to_move:
                connected += 1
                x -= 1
            else:
                break
        # check right
        x = coin[0] + 1
        while x < TILES_X:
            if self.coins[x][coin[1]] == self.player_to_move:
                connected += 1
                x += 1
            else:
                break
        return True if connected >= CONNECT else False

    def win_vertical(self, coin: Tuple[int, int]) -> bool:
        connected = 1
        # check down
        y = coin[1] - 1
        while y >= 0:
            if self.coins[coin[0]][y] == self.player_to_move:
                connected += 1
                y -= 1
            else:
                break
        # check up
        y = coin[1] + 1
        while y < TILES_Y:
            if self.coins[coin[0]][y] == self.player_to_move:
                connected += 1
                y += 1
            else:
                break
        return True if connected >= CONNECT else False

    def win_diagonal_one(self, coin: Tuple[int, int]) -> bool:
        connected = 1
        # check up left
        x = coin[0] - 1
        y = coin[1] + 1
        while y < TILES_Y and x >= 0:
            if self.coins[x][y] == self.player_to_move:
                connected += 1
                y += 1
                x -= 1
            else:
                break
        # check down right
        x = coin[0] + 1
        y = coin[1] - 1
        while y >= 0 and x < TILES_X:
            if self.coins[x][y] == self.player_to_move:
                connected += 1
                y -= 1
                x += 1
            else:
                break
        return True if connected >= CONNECT else False

    def win_diagonal_two(self, coin: Tuple[int, int]) -> bool:
        connected = 1
        # check up right
        x = coin[0] + 1
        y = coin[1] + 1
        while y < TILES_Y and x < TILES_X:
            if self.coins[x][y] == self.player_to_move:
                connected += 1
                y += 1
                x += 1
            else:
                break
        # check down left
        x = coin[0] - 1
        y = coin[1] - 1
        while y >= 0 and x >= 0:
            if self.coins[x][y] == self.player_to_move:
                connected += 1
                y -= 1
                x -= 1
            else:
                break
        return True if connected >= CONNECT else False

    def next_turn(self):
        self.player_to_move = 2 if self.player_to_move == 1 else 1

    def draw(self, screen):
        # draw bg
        pygame.draw.rect(screen, COLOR_BG, pygame.Rect(0, 0, WIDTH, HEIGHT))
        # draw coins / holes
        for x, cols in enumerate(self.coins):
            for y, coin in enumerate(cols[::-1]):
                color = COLOR_EMPTY
                if coin == 1:
                    color = COLOR_P1
                elif coin == 2:
                    color = COLOR_P2
                pygame.draw.circle(screen, color, center_coord(grid_to_pixel_coord((x, y))), TILE_SIZE // 3)
        # draw highlighted slot
        if self.highlight is not None:
            pygame.draw.circle(
                screen, (COLOR_P1_HIGHLIGHT if self.player_to_move == 1 else COLOR_P2_HIGHLIGHT),
                center_coord(grid_to_pixel_coord((self.highlight[0], TILES_Y - 1 - self.highlight[1]))), TILE_SIZE // 3
            )

    def show_winner(self, screen, winner):
        self.draw(screen)
        # draw winner screen
        font = pygame.font.Font(pygame.font.get_default_font(), 36)
        winner_text = None
        if winner == 1:
            winner_text = "Player 1 Wins!"
        elif winner == 2:
            winner_text = "Player 2 Wins!"
        else:
            winner_text = "Draw!"
        text_surface = font.render(winner_text, False, COLOR_TEXT)
        text_rect = text_surface.get_rect()
        text_rect.center = (WIDTH // 2, HEIGHT // 2)
        text_bg = pygame.Rect(0, 0, text_rect.width + 50, text_rect.height + 50)
        text_bg.center = text_rect.center
        pygame.draw.rect(screen, COLOR_TEXT_BG, text_bg)
        screen.blit(text_surface, text_rect)
