import pygame
import random

class Asteroid:
    def __init__(self, width, height, pos=None, size=3):
        self.size = size
        self.position = pos or pygame.Vector2(random.randint(0, width), random.randint(0, height))
        self.velocity = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
        self.width, self.height = width, height

    def update(self):
        self.position += self.velocity
        self.wrap_around()

    def draw(self, surface):
        # Neon-style asteroid with cyan glow
        radius = self.size * 10
        pygame.draw.circle(surface, (0, 255, 255, 50), (int(self.position.x), int(self.position.y)), radius + 4, 4)
        pygame.draw.circle(surface, (0, 255, 255), (int(self.position.x), int(self.position.y)), radius, 2)

    def wrap_around(self):
        if self.position.x > self.width: self.position.x = 0
        elif self.position.x < 0: self.position.x = self.width
        if self.position.y > self.height: self.position.y = 0
        elif self.position.y < 0: self.position.y = self.height
