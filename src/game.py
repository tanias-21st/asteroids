import pygame
from ship import Ship
from asteroid import Asteroid
from bullet import Bullet

class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.ship = Ship(width, height)
        self.bullets = []
        self.score = 0
        self.level = 1
        self.game_over = False
        self.font = pygame.font.SysFont("Arial", 24)
        self.shoot_sound = pygame.mixer.Sound("assets/sounds/shoot.wav")
        self.explode_sound = pygame.mixer.Sound("assets/sounds/explode.wav")
        self.spawn_asteroids()

    def spawn_asteroids(self):
        self.asteroids = [Asteroid(self.width, self.height) for _ in range(4 + self.level)]

    def reset(self):
        self.__init__(self.width, self.height)

    def update(self):
        if self.game_over:
            return

        keys = pygame.key.get_pressed()
        self.ship.update(keys)

        for asteroid in self.asteroids:
            asteroid.update()

        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.lifespan <= 0:
                self.bullets.remove(bullet)

        self.handle_collisions()

    def handle_collisions(self):
        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if bullet.position.distance_to(asteroid.position) < asteroid.size * 10:
                    self.bullets.remove(bullet)
                    self.asteroids.remove(asteroid)
                    self.explode_sound.play()
                    self.score += 100
                    if asteroid.size > 1:
                        self.asteroids.append(Asteroid(self.width, self.height, pos=asteroid.position, size=asteroid.size - 1))
                        self.asteroids.append(Asteroid(self.width, self.height, pos=asteroid.position, size=asteroid.size - 1))
                    break

        for asteroid in self.asteroids:
            if self.ship.position.distance_to(asteroid.position) < asteroid.size * 10:
                self.game_over = True

        if not self.asteroids and not self.game_over:
            self.level += 1
            self.spawn_asteroids()

    def draw(self, surface):
        self.ship.draw(surface)
        for asteroid in self.asteroids:
            asteroid.draw(surface)
        for bullet in self.bullets:
            bullet.draw(surface)
        self.draw_hud(surface)
        if self.game_over:
            self.show_game_over(surface)

    def draw_hud(self, surface):
        # "Score" label in red
        label = self.font.render("Score:", True, (255, 0, 0))
        surface.blit(label, (self.width - label.get_width() - 100, 10))
        # Points value in white
        points = self.font.render(f"{self.score}", True, (255, 255, 255))
        surface.blit(points, (self.width - points.get_width() - 10, 10))

        # Optional: Level indicator in cyan below score
        level_text = self.font.render(f"Level: {self.level}", True, (0, 255, 255))
        surface.blit(level_text, (self.width - level_text.get_width() - 10, 40))

    def show_game_over(self, surface):
        text = self.font.render("GAME OVER - Press R to Restart", True, (255, 0, 0))
        surface.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2))

    def shoot(self):
        if not self.game_over:
            self.bullets.append(Bullet(self.ship.position, self.ship.angle))
            self.shoot_sound.play()
