import pygame
import random
from entities import *
from constants import *
from utils import load_high_score, save_high_score


class SpaceInvadersGame:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invaders")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = "menu"  # 'menu', 'playing', 'game_over', 'paused'

        # Game objects
        self.player = None
        self.enemies = []
        self.player_bullets = []
        self.enemy_bullets = []
        self.explosions = []
        self.powerups = []

        # Game stats
        self.score = 0
        self.wave = 1
        self.high_score = load_high_score()

        # Enemy movement
        self.enemy_direction = 1

        # Stars background
        self.stars = [
            (
                random.randint(0, SCREEN_WIDTH),
                random.randint(0, SCREEN_HEIGHT),
                random.randint(1, 3),
            )
            for _ in range(100)
        ]

        self.create_enemies()

    def create_enemies(self):
        self.enemies = []
        current_speed = ENEMY_BASE_SPEED + (self.wave - 1) * ENEMY_SPEED_INCREASE
        for row in range(5):
            for col in range(10):
                enemy_type = row
                x = 80 + col * 60
                y = 80 + row * 50
                self.enemies.append(Enemy(x, y, enemy_type, current_speed))
        self.enemy_direction = 1

    def reset_game(self):
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.enemies = []
        self.player_bullets = []
        self.enemy_bullets = []
        self.explosions = []
        self.powerups = []
        self.score = 0
        self.wave = 1
        self.enemy_direction = 1
        self.create_enemies()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if self.game_state == "menu":
                    if event.key == pygame.K_SPACE:
                        self.game_state = "playing"
                        self.reset_game()

                elif self.game_state == "playing":
                    if event.key == pygame.K_SPACE:
                        if self.player.can_shoot():
                            if self.player.multi_shot > 0:
                                for i in range(-1, 2):
                                    bullet = Bullet(
                                        self.player.x + i * 10, self.player.y - 20
                                    )
                                    self.player_bullets.append(bullet)
                            else:
                                bullet = Bullet(self.player.x, self.player.y - 20)
                                self.player_bullets.append(bullet)
                    if event.key == pygame.K_p:
                        self.game_state = "paused"

                elif self.game_state == "game_over":
                    if event.key == pygame.K_r:
                        self.game_state = "playing"
                        self.reset_game()
                    elif event.key == pygame.K_m:
                        self.game_state = "menu"

                elif self.game_state == "paused":
                    if event.key == pygame.K_p:
                        self.game_state = "playing"

    def update(self):
        if self.game_state == "playing":
            self.update_game()

    def update_game(self):
        self.player.update()

        # Update bullets
        for bullet in self.player_bullets[:]:
            bullet.update()
            if bullet.y < 0:
                self.player_bullets.remove(bullet)

        for bullet in self.enemy_bullets[:]:
            bullet.update()
            if bullet.y > SCREEN_HEIGHT:
                self.enemy_bullets.remove(bullet)

        move_down = False
        if self.enemies:  # Only check if enemies exist
            leftmost = min(enemy.x for enemy in self.enemies)
            rightmost = max(enemy.x for enemy in self.enemies)

            if leftmost <= 30 and self.enemy_direction == -1:
                move_down = True
                self.enemy_direction = 1
            elif rightmost >= SCREEN_WIDTH - 30 and self.enemy_direction == 1:
                move_down = True
                self.enemy_direction = -1

        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update(move_down, self.enemy_direction)

            # Enemy shooting
            if enemy.can_shoot() and random.random() < ENEMY_SPAWN_CHANCE:
                bullet = Bullet(enemy.x, enemy.y + 20, -1)
                self.enemy_bullets.append(bullet)

            # Check if any enemy reached bottom
            if enemy.y > SCREEN_HEIGHT - 100:
                self.player.lives = 0

        # Update explosions
        for explosion in self.explosions[:]:
            explosion.update()
            if explosion.is_dead():
                self.explosions.remove(explosion)

        # Update power-ups
        for powerup in self.powerups[:]:
            powerup.update()
            if powerup.y > SCREEN_HEIGHT:
                self.powerups.remove(powerup)

        # Collision detection
        self.check_collisions()

        # Win condition
        if not self.enemies:
            self.wave += 1
            self.create_enemies()
            if random.random() < 0.3:
                powerup_type = random.choice(["rapid_fire", "multi_shot", "shield"])
                powerup = PowerUp(
                    random.randint(50, SCREEN_WIDTH - 50), -20, powerup_type
                )
                self.powerups.append(powerup)

        # Game over
        if self.player.lives <= 0:
            if self.score > self.high_score:
                self.high_score = self.score
                save_high_score(self.high_score)
            self.game_state = "game_over"

    def check_collisions(self):
        # Player bullets vs enemies
        for bullet in self.player_bullets[:]:
            for enemy in self.enemies[:]:
                if bullet.get_rect().colliderect(enemy.get_rect()):
                    self.explosions.append(Explosion(enemy.x, enemy.y))
                    self.score += enemy.get_points()
                    self.player_bullets.remove(bullet)
                    self.enemies.remove(enemy)

                    # Chance to drop power-up
                    if random.random() < POWERUP_SPAWN_CHANCE:
                        powerup_type = random.choice(
                            ["rapid_fire", "multi_shot", "shield"]
                        )
                        powerup = PowerUp(enemy.x, enemy.y, powerup_type)
                        self.powerups.append(powerup)
                    break

        # Enemy bullets vs player
        if self.player.shield <= 0:
            for bullet in self.enemy_bullets[:]:
                if bullet.get_rect().colliderect(self.player.get_rect()):
                    self.explosions.append(Explosion(self.player.x, self.player.y))
                    self.player.lives -= 1
                    self.enemy_bullets.remove(bullet)
                    break
        else:
            for bullet in self.enemy_bullets[:]:
                if bullet.get_rect().colliderect(self.player.get_rect()):
                    self.enemy_bullets.remove(bullet)

        # Player vs power-ups
        for powerup in self.powerups[:]:
            if powerup.get_rect().colliderect(self.player.get_rect()):
                self.player.apply_powerup(powerup.type)
                self.powerups.remove(powerup)

    def draw(self):
        self.screen.fill(BLACK)

        # Draw stars
        for star in self.stars:
            pygame.draw.circle(self.screen, WHITE, (star[0], star[1]), star[2])

        if self.game_state == "menu":
            self.draw_menu()
        elif self.game_state == "playing":
            self.draw_game()
        elif self.game_state == "game_over":
            self.draw_game_over()
        elif self.game_state == "paused":
            self.draw_game()
            self.draw_pause()

        pygame.display.flip()

    def draw_menu(self):
        font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)

        title = font_large.render("SPACE INVADERS", True, GREEN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)

        start_text = font_medium.render("Press SPACE to Start", True, WHITE)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
        self.screen.blit(start_text, start_rect)

        high_score_text = font_medium.render(
            f"High Score: {self.high_score}", True, YELLOW
        )
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, 400))
        self.screen.blit(high_score_text, high_score_rect)

    def draw_game(self):
        self.player.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        for bullet in self.player_bullets:
            bullet.draw(self.screen)

        for bullet in self.enemy_bullets:
            bullet.draw(self.screen)

        for explosion in self.explosions:
            explosion.draw(self.screen)

        for powerup in self.powerups:
            powerup.draw(self.screen)

        # Draw UI
        font = pygame.font.Font(None, FONT_SIZE_MEDIUM)

        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        lives_text = font.render(f"Lives: {self.player.lives}", True, WHITE)
        self.screen.blit(lives_text, (10, 50))

        wave_text = font.render(f"Wave: {self.wave}", True, WHITE)
        self.screen.blit(wave_text, (SCREEN_WIDTH - 150, 10))

        y_offset = 90
        if self.player.rapid_fire > 0:
            rapid_text = font.render("RAPID FIRE", True, YELLOW)
            self.screen.blit(rapid_text, (10, y_offset))
            y_offset += 30

        if self.player.multi_shot > 0:
            multi_text = font.render("MULTI SHOT", True, BLUE)
            self.screen.blit(multi_text, (10, y_offset))
            y_offset += 30

        if self.player.shield > 0:
            shield_text = font.render("SHIELD", True, PURPLE)
            self.screen.blit(shield_text, (10, y_offset))

    def draw_game_over(self):
        self.draw_game()  # Draw game state behind overlay

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)

        game_over_text = font_large.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(game_over_text, game_over_rect)

        final_score_text = font_medium.render(f"Final Score: {self.score}", True, WHITE)
        final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, 280))
        self.screen.blit(final_score_text, final_score_rect)

        if self.score == self.high_score and self.score > 0:
            new_high_text = font_medium.render("NEW HIGH SCORE!", True, YELLOW)
            new_high_rect = new_high_text.get_rect(center=(SCREEN_WIDTH // 2, 320))
            self.screen.blit(new_high_text, new_high_rect)

        restart_text = font_medium.render(
            "Press R to Restart or M for Menu", True, WHITE
        )
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, 380))
        self.screen.blit(restart_text, restart_rect)

    def draw_pause(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        font = pygame.font.Font(None, FONT_SIZE_LARGE)
        pause_text = font.render("PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(pause_text, pause_rect)

        font_small = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        continue_text = font_small.render("Press P to Continue", True, WHITE)
        continue_rect = continue_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
        )
        self.screen.blit(continue_text, continue_rect)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
