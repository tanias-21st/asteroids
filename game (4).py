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
        self.large_font = pygame.font.SysFont("Arial", 48)
        self.shoot_sound = pygame.mixer.Sound("assets/sounds/shoot.wav")
        self.explode_sound = pygame.mixer.Sound("assets/sounds/explode.wav")
        self.demo_mode = False
        self.play_again_button_rect = pygame.Rect(self.width // 2 - 100, self.height // 2 + 40, 200, 50)
        self.countdown_timer = 10 * 60  # 10 seconds in frames
        self.spawn_asteroids()

    def spawn_asteroids(self):
        self.asteroids = [Asteroid(self.width, self.height) for _ in range(4 + self.level)]

    def reset(self):
        self.__init__(self.width, self.height)

    def update(self):
        if self.demo_mode:
            return  # No updates in demo mode

        if self.game_over:
            self.countdown_timer -= 1
            if self.countdown_timer <= 0:
                self.demo_mode = True
            return

        keys = pygame.key.get_pressed()
        self.ship.update(keys)

        for asteroid in self.asteroids:
            asteroid.update()

        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.lifespan <= 0 or bullet.is_offscreen(self.width, self.height):
                self.bullets.remove(bullet)

        self.handle_collisions()

    def handle_collisions(self):
        bullets_to_remove = []
        asteroids_to_remove = []

        for bullet in self.bullets:
            for asteroid in self.asteroids:
                if bullet.position.distance_to(asteroid.position) < asteroid.get_radius():
                    bullets_to_remove.append(bullet)
                    asteroids_to_remove.append(asteroid)
                    self.explode_sound.play()
                    self.score += 100
                    if asteroid.size > 1:
                        pos_copy = asteroid.position.copy()
                        self.asteroids.append(Asteroid(self.width, self.height, pos=pos_copy, size=asteroid.size - 1))
                        self.asteroids.append(Asteroid(self.width, self.height, pos=pos_copy, size=asteroid.size - 1))
                    break

        for bullet in bullets_to_remove:
            if bullet in self.bullets:
                self.bullets.remove(bullet)

        for asteroid in asteroids_to_remove:
            if asteroid in self.asteroids:
                self.asteroids.remove(asteroid)

        for asteroid in self.asteroids:
            if self.ship.position.distance_to(asteroid.position) < asteroid.get_radius():
                self.game_over = True
                self.countdown_timer = 10 * 60

        if not self.asteroids and not self.game_over:
            self.level += 1
            self.spawn_asteroids()

    def draw(self, surface):
        if self.demo_mode:
            self.draw_demo_mode(surface)
            return

        self.ship.draw(surface)
        for asteroid in self.asteroids:
            asteroid.draw(surface)
        for bullet in self.bullets:
            bullet.draw(surface)
        self.draw_hud(surface)
        if self.game_over:
            self.show_game_over(surface)

    def draw_hud(self, surface):
        label = self.font.render("Score:", True, (255, 0, 0))
        surface.blit(label, (self.width - label.get_width() - 100, 10))
        points = self.font.render(f"{self.score}", True, (255, 255, 255))
        surface.blit(points, (self.width - points.get_width() - 10, 10))
        level_text = self.font.render(f"Level: {self.level}", True, (0, 255, 255))
        surface.blit(level_text, (self.width - level_text.get_width() - 10, 40))

    def show_game_over(self, surface):
        text = self.large_font.render("GAME OVER", True, (255, 0, 0))
        surface.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2 - 50))

        countdown = self.countdown_timer // 60
        timer_text = self.font.render(f"Auto-demo in {countdown}...", True, (255, 255, 0))
        surface.blit(timer_text, (self.width // 2 - timer_text.get_width() // 2, self.height // 2))

        pygame.draw.rect(surface, (50, 200, 50), self.play_again_button_rect)
        play_text = self.font.render("Play Again", True, (255, 255, 255))
        surface.blit(play_text, (self.play_again_button_rect.centerx - play_text.get_width() // 2,
                                 self.play_again_button_rect.centery - play_text.get_height() // 2))

    def draw_demo_mode(self, surface):
        surface.fill((0, 0, 0))
        demo_text = self.large_font.render("TAP TO BEGIN", True, (255, 255, 255))
        surface.blit(demo_text, (self.width // 2 - demo_text.get_width() // 2, self.height // 2))

    def shoot(self):
        if not self.game_over and not self.demo_mode:
            print("Bullet fired at angle", self.ship.angle)
            self.bullets.append(Bullet(self.ship.position, self.ship.angle))
            self.shoot_sound.play()

    def handle_click(self, pos):
        if self.game_over and self.play_again_button_rect.collidepoint(pos):
            self.reset()
        elif self.demo_mode:
            self.reset()
