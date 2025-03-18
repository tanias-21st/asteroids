# src/ship.py

import pygame
import math

class Ship:
    def __init__(self, width, height):
        self.position = pygame.Vector2(width / 2, height / 2)
        self.angle = 0
        self.velocity = pygame.Vector2(0, 0)
        self.width, self.height = width, height

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.angle += 5
        if keys[pygame.K_RIGHT]:
            self.angle -= 5
        if keys[pygame.K_UP]:
            self.velocity += pygame.Vector2(math.sin(math.radians(self.angle)),
                                            math.cos(math.radians(self.angle))) * 0.3
        self.position += self.velocity
        self.wrap_around()

    def draw(self, surface):
        # Neon Ship Polygon (Magenta + Cyan glow)
        points = []
        for offset in [(0, -20), (10, 10), (-10, 10)]:
            x = self.position.x + math.sin(math.radians(self.angle)) * offset[0] + math.cos(math.radians(self.angle)) * offset[1]
            y = self.position.y - math.cos(math.radians(self.angle)) * offset[0] + math.sin(math.radians(self.angle)) * offset[1]
            points.append((x, y))

        # Glow layer
        pygame.draw.polygon(surface, (0, 255, 255, 50), points, 6)  # Cyan outer glow
        pygame.draw.polygon(surface, (255, 0, 255), points, 2)      # Magenta core

    def wrap_around(self):
        if self.position.x > self.width: self.position.x = 0
        elif self.position.x < 0: self.position.x = self.width
        if self.position.y > self.height: self.position.y = 0
        elif self.position.y < 0: self.position.y = self.height
