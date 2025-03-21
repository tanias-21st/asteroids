# main.py

import pygame
import sys
from game import Game

pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids Modular")

clock = pygame.time.Clock()
game = Game(WIDTH, HEIGHT)

def main_loop():
    while True:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.shoot()
                if event.key == pygame.K_r and game.game_over:
                    game.reset()

        game.update()
        game.draw(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main_loop()
