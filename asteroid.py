# asteroid.py

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
        pygame.draw.circle(surface, (200, 200, 200), (int(self.position.x), int(self.position.y)), self.size * 10, 2)

    def wrap_around(self):
        if self.position.x > self.width: self.position.x = 0
        elif self.position.x < 0: self.position.x = self.width
        if self.position.y > self.height: self.position.y = 0
        elif self.position.y < 0: self.position.y = self.height
