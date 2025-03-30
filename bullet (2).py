import pygame
import math

class Bullet:
    def __init__(self, pos, angle):
        self.position = pygame.Vector2(pos)
        self.velocity = pygame.Vector2(math.sin(math.radians(angle)),
                                       math.cos(math.radians(angle))) * 7
        self.lifespan = 60

    def update(self):
        self.position += self.velocity
        self.lifespan -= 1

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 0), (int(self.position.x), int(self.position.y)), 4)

    def is_offscreen(self, width, height):
        return (
            self.position.x < 0 or self.position.x > width or
            self.position.y < 0 or self.position.y > height
        )
