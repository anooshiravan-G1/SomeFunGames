import pygame
import random
from constants import *


# --- PARTICLE & EXPLOSION ---
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.color = color
        self.life = 30
        self.max_life = 30

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.vy += 0.1  # Gravity

    def draw(self, screen):
        if self.life > 0:
            alpha = self.life / self.max_life
            size = int(3 * alpha)
            if size > 0:
                pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), size)


class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.particles = []
        colors = [RED, ORANGE, YELLOW, WHITE]
        for _ in range(15):
            color = random.choice(colors)
            self.particles.append(Particle(x, y, color))
        self.life = 60

    def update(self):
        for particle in self.particles[:]:
            particle.update()
            if particle.life <= 0:
                self.particles.remove(particle)
        self.life -= 1

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)

    def is_dead(self):
        return len(self.particles) == 0 or self.life <= 0


# --- BULLET ---
class Bullet:
    def __init__(self, x, y, direction=1):
        self.x = x
        self.y = y
        self.direction = direction  # 1 for up, -1 for down
        self.speed = BULLET_SPEED
        self.width = 3
        self.height = 8

    def update(self):
        self.y -= self.speed * self.direction

    def draw(self, screen):
        color = GREEN if self.direction == 1 else RED
        pygame.draw.rect(
            screen,
            color,
            (
                self.x - self.width // 2,
                self.y - self.height // 2,
                self.width,
                self.height,
            ),
        )

    def get_rect(self):
        return pygame.Rect(
            self.x - self.width // 2, self.y - self.height // 2, self.width, self.height
        )


# --- POWER-UP ---
class PowerUp:
    def __init__(self, x, y, type_):
        self.x = x
        self.y = y
        self.type = type_  # 'rapid_fire', 'multi_shot', 'shield'
        self.speed = 2
        self.width = 20
        self.height = 20
        self.colors = {"rapid_fire": YELLOW, "multi_shot": BLUE, "shield": PURPLE}

    def update(self):
        self.y += self.speed

    def draw(self, screen):
        color = self.colors.get(self.type, WHITE)
        pygame.draw.rect(
            screen,
            color,
            (
                self.x - self.width // 2,
                self.y - self.height // 2,
                self.width,
                self.height,
            ),
        )
        # Draw symbol
        if self.type == "rapid_fire":
            pygame.draw.polygon(
                screen,
                BLACK,
                [
                    (self.x, self.y - 8),
                    (self.x - 6, self.y + 6),
                    (self.x + 6, self.y + 6),
                ],
            )
        elif self.type == "multi_shot":
            for i in range(3):
                pygame.draw.circle(screen, BLACK, (self.x - 6 + i * 6, self.y), 2)
        elif self.type == "shield":
            pygame.draw.circle(screen, BLACK, (self.x, self.y), 8, 2)

    def get_rect(self):
        return pygame.Rect(
            self.x - self.width // 2, self.y - self.height // 2, self.width, self.height
        )


# --- ENEMY ---
class Enemy:
    def __init__(self, x, y, enemy_type=0, speed=ENEMY_BASE_SPEED):
        self.x = x
        self.y = y
        self.type = enemy_type
        self.width = 30
        self.height = 20
        self.speed = speed
        self.direction = 1
        self.shoot_timer = 0
        self.shoot_delay = random.randint(ENEMY_SHOOT_DELAY_MIN, ENEMY_SHOOT_DELAY_MAX)
        self.animation_frame = 0
        self.colors = [GREEN, BLUE, PURPLE, RED]
        self.points = [10, 20, 30, 50]

    def update(self, move_down=False, direction=1):
        self.animation_frame += 1
        self.shoot_timer += 1

        if move_down:
            self.y += 20
            self.direction = direction
        else:
            self.x += self.speed * self.direction

    def draw(self, screen):
        color = self.colors[self.type % len(self.colors)]
        frame = (self.animation_frame // 30) % 2

        # Body
        pygame.draw.rect(screen, color, (self.x - 15, self.y - 10, 30, 20))

        # Eyes
        eye_color = WHITE if frame == 0 else RED
        pygame.draw.rect(screen, eye_color, (self.x - 10, self.y - 5, 4, 4))
        pygame.draw.rect(screen, eye_color, (self.x + 6, self.y - 5, 4, 4))

        # Legs
        leg_offset = 2 if frame == 0 else -2
        pygame.draw.rect(screen, color, (self.x - 12, self.y + 8, 3, 8 + leg_offset))
        pygame.draw.rect(screen, color, (self.x - 3, self.y + 8, 3, 6 + leg_offset))
        pygame.draw.rect(screen, color, (self.x + 6, self.y + 8, 3, 6 + leg_offset))
        pygame.draw.rect(screen, color, (self.x + 12, self.y + 8, 3, 8 + leg_offset))

    def get_rect(self):
        return pygame.Rect(self.x - 15, self.y - 10, 30, 20)

    def can_shoot(self):
        if self.shoot_timer >= self.shoot_delay:
            self.shoot_timer = 0
            self.shoot_delay = random.randint(
                ENEMY_SHOOT_DELAY_MIN, ENEMY_SHOOT_DELAY_MAX
            )
            return True
        return False

    def get_points(self):
        return self.points[self.type % len(self.points)]


# --- PLAYER ---
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 30
        self.speed = PLAYER_SPEED
        self.lives = 3
        self.shield = 0
        self.rapid_fire = 0
        self.multi_shot = 0
        self.shoot_cooldown = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed

        # Keep player on screen
        self.x = max(20, min(SCREEN_WIDTH - 20, self.x))

        # Update power-up timers
        if self.shield > 0:
            self.shield -= 1
        if self.rapid_fire > 0:
            self.rapid_fire -= 1
        if self.multi_shot > 0:
            self.multi_shot -= 1

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def draw(self, screen):
        if self.shield > 0:
            pygame.draw.circle(screen, BLUE, (int(self.x), int(self.y)), 25, 3)

        # Main body
        pygame.draw.rect(screen, WHITE, (self.x - 15, self.y - 10, 30, 20))
        # Cockpit
        pygame.draw.rect(screen, BLUE, (self.x - 8, self.y - 15, 16, 10))
        # Wings
        pygame.draw.polygon(
            screen,
            WHITE,
            [
                (self.x - 20, self.y + 5),
                (self.x - 15, self.y - 5),
                (self.x - 15, self.y + 10),
            ],
        )
        pygame.draw.polygon(
            screen,
            WHITE,
            [
                (self.x + 20, self.y + 5),
                (self.x + 15, self.y - 5),
                (self.x + 15, self.y + 10),
            ],
        )
        # Engine
        pygame.draw.rect(screen, RED, (self.x - 5, self.y + 8, 10, 6))

    def get_rect(self):
        return pygame.Rect(self.x - 20, self.y - 15, 40, 30)

    def can_shoot(self):
        cooldown = 10 if self.rapid_fire > 0 else 20
        if self.shoot_cooldown <= 0:
            self.shoot_cooldown = cooldown
            return True
        return False

    def apply_powerup(self, powerup_type):
        duration = POWERUP_DURATION.get(powerup_type, 0)
        if powerup_type == "rapid_fire":
            self.rapid_fire = duration
        elif powerup_type == "multi_shot":
            self.multi_shot = duration
        elif powerup_type == "shield":
            self.shield = duration
