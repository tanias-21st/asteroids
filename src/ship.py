import pygame
import math

class Ship:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.position = pygame.Vector2(width / 2, height / 2)
        self.velocity = pygame.Vector2(0, 0)
        self.angle = 0
        self.thrust = 0.3

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.angle += 5
        if keys[pygame.K_RIGHT]:
            self.angle -= 5
        if keys[pygame.K_UP]:
            self.velocity += self.get_nose_vector() * self.thrust
        self.position += self.velocity
        self.wrap_around()

    def draw(self, surface):
        # Build ship points based on angle
        offsets = [(0, -20), (10, 10), (-10, 10)]
        points = []
        for dx, dy in offsets:
            x = self.position.x + math.sin(math.radians(self.angle)) * dx + math.cos(math.radians(self.angle)) * dy
            y = self.position.y - math.cos(math.radians(self.angle)) * dx + math.sin(math.radians(self.angle)) * dy
            points.append((x, y))

        pygame.draw.polygon(surface, (0, 255, 255, 50), points, 6)
        pygame.draw.polygon(surface, (255, 0, 255), points, 2)

    def wrap_around(self):
        if self.position.x > self.width: self.position.x = 0
        elif self.position.x < 0: self.position.x = self.width
        if self.position.y > self.height: self.position.y = 0
        elif self.position.y < 0: self.position.y = self.height

    def get_nose_vector(self):
        return pygame.Vector2(math.sin(math.radians(self.angle)),
                              math.cos(math.radians(self.angle)))

    def reset(self):
        self.position = pygame.Vector2(self.width / 2, self.height / 2)
        self.velocity = pygame.Vector2(0, 0)
        self.angle = 0
